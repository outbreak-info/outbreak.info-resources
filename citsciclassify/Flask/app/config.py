class Config(object):
    pass

class ProductionConfig(Config):
    MYSQL_DATABASE_DB = 'citsciclassify'
    MYSQL_DATABASE_PASSWORD = 's/v8$@B2Tt84B['
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_HOST = 'db'

class DevelopmentConfig(Config):
    MYSQL_DATABASE_DB = 'citsciclassify'
    MYSQL_DATABASE_PASSWORD = '7%jqpwB{#G+D9j'
    MYSQL_DATABASE_USER = 'root'
    MYSQL_DATABASE_HOST = 'db'