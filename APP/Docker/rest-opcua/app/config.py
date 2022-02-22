import os

class BaseConfig(object):

    PROJECT = "Notifier endpoint"
    opcua_host = "opc.tcp://host.docker.internal:4840/freeopcua/server/"


class DevelopmentConfig(BaseConfig):

    # Statement for enabling the development environment
    DEBUG = True
    ENV = "DEVELOPMENT"
    
class ProductionConfig(BaseConfig):
    # Statement for enabling the development environment
    DEBUG = False
    ENV = "PRODUCTION"

def get_config(MODE):
    SWITCH = {
        'DEVELOPMENT': DevelopmentConfig,
        'PRODUCTION': ProductionConfig
    }
    return SWITCH[MODE]