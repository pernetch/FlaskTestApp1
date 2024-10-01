import os
basedir = os.path.abspath(os.path.dirname(__file__))



SECRET_KEY='f74922ce0a3c106262ea5e0c5922f8d7'
DATABASE='data.sqlite'
SQLALCHEMY_DATABASE_URI=''
SQLALCHEMY_TRACK_MODIFICATIONS=False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
FLASK_DEBUG=1