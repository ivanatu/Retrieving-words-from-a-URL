from flask import render_template, redirect, flash, Flask
# from app import app
import requests 
from bs4 import BeautifulSoup 
import operator 
import os
from app import url_app
from collections import Counter
from app.forms import LoginForm
from app.models import Url
import psycopg2
import uuid
import hashlib
import base64
import logging

from cryptography.exceptions import UnsupportedAlgorithm
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet

# key = Fernet.generate_key() # Store this key or get if you already have it
# f = Fernet(key)

password = b"password"
salt = os.urandom(16)
kdf = PBKDF2HMAC(
	 algorithm=hashes.SHA256(),
	 length=32,
	 salt=salt,
	 iterations=100000,
	 backend=default_backend()
	 )
key = base64.urlsafe_b64encode(kdf.derive(password))
f = Fernet(key)

private_key = rsa.generate_private_key(
	public_exponent=65537,
	key_size=2048,
	backend=default_backend()
)
public_key = private_key.public_key()

@url_app.route('/', methods=['POST', 'GET'])
@url_app.route('/index', methods=['POST', 'GET'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		flash('Login requested for user {}'.format(
			form.username.data))
	# empty list to store the contents of  
	# the website fetched from our web-crawler
		word_list = []
		source_code = requests.get(form.username.data).text
			
	# BeautifulSoup object which will 
	# ping the requested url for data 
		soup = BeautifulSoup(source_code, 'html.parser')
		for each_text in soup.findAll('div', {'class':'entry-content'}):
			content = each_text.text

		 # use split() to break the sentence into  
		# words and convert them into lowercase
			words = content.lower().split()
			for each_word in words:
				symbols = '!@#$%^&*()_-+={[}]|\;:"<>?/., '
				for i in range (0, len(symbols)):
					each_word = each_word.replace(symbols[i], '')
				if len(each_word) > 0:
					word_list.append(each_word)
		create_dictionary(word_list)
		return redirect('/index')
	return render_template('login.html', title='Sign In', form=form)

@url_app.route('/lists', methods=['GET'])
def lists():
	conn = psycopg2.connect("host=localhost dbname=url2 user=postgres password=1234")
	cur = conn.cursor()
	cur.execute("SELECT username, word_count FROM url")
	
	database_words = cur.fetchall()
	database_encrypted_words = {}
	frequent_words = {}
	database_encrypted_words.update(database_words)

	c = Counter(database_encrypted_words) 
	top = c.most_common()
	frequent_words.update(top)
	# return render_template('list.html', title='List of words', list=frequent_words)
	return render_template('list.html', title='List of words', list=frequent_words)

# Creates a dictionary conatining each word's  
# count and stores the keys or values onto the database
def create_dictionary(word_list): 
	word_count = {} 
	red = {}
	 
	for word in word_list: 
		if word in word_count: 
			word_count[word] += 1
		else: 
			word_count[word] = 1
	c = Counter(word_count) 
	top = c.most_common(100)
	red.update(top)

	conn = psycopg2.connect("host=localhost dbname=url2 user=postgres password=1234")
	cur = conn.cursor()
	cur.execute("SELECT username, word_count FROM url")
	
	database_words = cur.fetchall()
	database_encrypted_words = {}
	database_encrypted_words.update(database_words)
	words_in_database = []
	for word_database in database_encrypted_words.keys():
		words_in_database.append(word_database)
	
	# uuid is used to generate a random number
	salt = uuid.uuid4().hex
	for word in red:
		if word in words_in_database:
			total = word_count[word] + database_encrypted_words[word]
			cur.execute("UPDATE url SET word_count=%s WHERE word_count=%s", (total, database_encrypted_words[word]))      
			conn.commit()
		else:
			word_salted = hashlib.sha256(salt.encode() + word.encode()).hexdigest() + ':' + salt
			# word_encrypted = asymmetric_string_encryption(word)
			word_encoded = word.encode('utf-8')
			word_encryp = f.encrypt(word_encoded)
			cur.execute('INSERT INTO url VALUES (%s, %s, %s)', (word_salted, word, word_count[word]))
			conn.commit()

def asymmetric_string_encryption(plain_text):
	"""
	- Generation of public and private RSA 4096 bit keypair
	- RSA encryption and decryption of text using OAEP and MGF1 padding
	- BASE64 encoding as representation for the byte-arrays
	- UTF-8 encoding of Strings
	- Exception handling
	"""
	# ENCRYPTION
	cipher_text_bytes = public_key.encrypt(
		plaintext=plain_text.encode('utf-8'),
		padding=padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA512(),
			label=None
		)
	)

	cipher_text_encrypted = base64.urlsafe_b64encode(cipher_text_bytes)
	return str(cipher_text_bytes)
	
def string_decryption(cipher_text):
		
	# DECRYPTION
	decrypted_cipher_text_bytes = private_key.decrypt(
		 cipher_text = base64.b64decode(cipher_text.encode("utf-8") ),
		padding=padding.OAEP(
			mgf=padding.MGF1(algorithm=hashes.SHA256()),
			algorithm=hashes.SHA512(),
			label=None
		)
	)
	decrypted_cipher_text = decrypted_cipher_text_bytes.decode('utf-8')
	return str(decrypted_cipher_text)
