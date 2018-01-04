class Config(object):
	"""
	Common configuration
	"""

	DEBUG = True

class DevelopmentConfig(Config):
	"""
	Development configurations
	"""
	SQLALCHEMY_ECHO = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = "p1Bv<2Eid9%$i01"
	SQLALCHEMY_DATABASE_URI = "postgresql://cruduser:crudpassword@localhost/crudappdb"

class ProductionConfig(Config):
	"""
	Production configurations
	"""
	DEBUG = False

class TestingConfig(Config):
	"""
	Testing configurations
	"""
	"""
	DEBUG = False because "By default if the application is in debug mode 
  the request context is not popped on exceptions to enable debuggers to introspect the data.
  - OR -  
  PRESERVE_CONTEXT_ON_EXCEPTION = False
	"""
	DEBUG = False  
	TESTING = True 

	"""
	NEED TO include form.csrf_token() in jinja!!!
	"""
	SECRET_KEY = "flask-testing-secretkey"

app_config = {
	"development": DevelopmentConfig,
	"production": ProductionConfig,
	"testing": TestingConfig
}
