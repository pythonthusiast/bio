import os

class Config(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') if os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL') else os.environ.get('LOCAL_DB_URL')
    CSRF_ENABLED = True
    SECRET_KEY = 'rahasiabesar'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "static/upload")
    ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg', 'gif'])