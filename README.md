# Retrieving-words-from-a-URL

Clone the repo to your terminal

Running the application
To run this application on a linux box, execute the following command.

    $ cd into the root directory on your terminal
    $ virtualenv venv
    $ source virtenv/bin/activate on macOs venv\Scripts\activate on windows
    $ pip install -r requirements.txt
    $ python manage.py db init
    $ python manage.py db migrate
    $ python manage.py db upgrade
    $ python manage.py runserver
    
    Open browser and run http://localhost:5000/ and input url
