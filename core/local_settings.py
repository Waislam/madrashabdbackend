import os
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-wg(wplo(x!$a(l$rzw5k!tr4v#k9zxy5=o_7*9@a(_q4f&3s&8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_REGEX_WHITELIST = [
    # r"^https://\w+\.workior\.com$",  # Match subdomain of teamshape.io
    r"http://localhost:3000",
    r"http://0.0.0.0:3000",
    r"http://192.168.0.105:8000",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://0.0.0.0:3000",
    "http://192.168.0.105:8000",
]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': 'mh123456',
#         'HOST': 'localhost',
#         'PORT': '5434',
#     }
# }

# DATABASES = {
#     "default": {
#         "ENGINE": os.environ.get("SQL_ENGINE"),
#         "NAME": os.environ.get("SQL_DATABASE"),
#         "USER": os.environ.get("SQL_USER"),
#         "PASSWORD": os.environ.get("SQL_PASSWORD"),
#         "HOST": os.environ.get("SQL_HOST"),
#         "PORT": os.environ.get("SQL_PORT"),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'sqlite3',
    }
}
