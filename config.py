# config.py
import os, secrets

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost:3306/proyecto_f'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = secrets.token_hex(16)
    SQLALCHEMY_ECHO = True  # Esto mostrará las consultas SQL en la consola
    
    
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