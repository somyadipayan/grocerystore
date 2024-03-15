class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'veryyysecret'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025