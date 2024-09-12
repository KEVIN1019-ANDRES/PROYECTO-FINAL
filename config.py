# config.py

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/proyecto_f'
    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlclient://root:2hefbFfDEc-HFd1fhc2DhBCCgh-HCB65@monorail.proxy.rlwy.net:20020/Libreria1'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'miapp_'