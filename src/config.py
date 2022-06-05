from distutils.command.config import config
import sqlite3

class Config:
    SECRET_KEY = 'Y-3XC9JsqV4ZS'

class DevelopmentConfig(Config):
    DEBUG = True

config={
    'development':DevelopmentConfig
}