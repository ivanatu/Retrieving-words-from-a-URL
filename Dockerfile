FROM alpine:3.1
ADD my_script.py /
# Update
RUN apk add --update python py-pip

# Install app dependencies
RUN pip install -r requirements.txt
RUN set DATABASE_URL='postgresql://postgres:1234@localhost:5432/url'
RUN python manage.py db init
RUN python manage.py db migrate
RUN python manage.py db upgrade

# Bundle app source
# COPY simpleapp.py /manage.py

EXPOSE  5000
CMD ["python", "/manage.py runserver", "-p 5000"]