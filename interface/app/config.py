import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'b0a5ce4da1704a056cd2939fc28090e31caf34c9173977ee9ee49aa0a9208ca1'
    ENGINE_CONFIG = "C:\\Users\\djord\\source\\repos\\IRS-SearchEngine\\sri\\config.txt"