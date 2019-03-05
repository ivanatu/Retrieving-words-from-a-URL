from app import app, db, url_app
from app.models import Url

if __name__ == '__main__':
    url_app.run(debug=True)