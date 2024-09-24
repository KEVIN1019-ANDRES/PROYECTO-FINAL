# config.py
import os, secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/proyecto_f'
    #SQLALCHEMY_DATABASE_URI = 'mysql+mysqlclient://root:2hefbFfDEc-HFd1fhc2DhBCCgh-HCB65@monorail.proxy.rlwy.net:20020/Libreria1'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = secrets.token_hex(16)
    
    
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_KEY_PREFIX = 'miapp_'
    
    MAIL_SERVER = 'smtp.example.com'      
    MAIL_PORT = 587                       
    MAIL_USE_TLS = True                   
    MAIL_USERNAME = 'tu_email@example.com' 
    MAIL_PASSWORD = 'tu_password'         
    MAIL_DEFAULT_SENDER = 'noreply@demo.com'