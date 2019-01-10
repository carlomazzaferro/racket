TEMPLATE_PROJECT_DIRS = [
    'serialized/base/1/variables/'
]

TEMPLATE_PROJECT_FILES = [
    'template/.gitignore',
    'template/docker-compose.yaml',
    'template/Dockerfile',
    'template/classification.py',
    'template/serialized/base/1/variables/variables.data-00000-of-00001',
    'template/serialized/base/1/variables/variables.index',
    'template/serialized/base/1/saved_model.pb',
    'template/serialized/base_1.h5',
    'template/serialized/base_1.json',
]

CONFIG_FILE_TEMPLATE = """
version: 1

logging:
    level: INFO

# Project Name
name: 'racket-server'

# Where to store your serialized models
saved-models: 'serialized'


# Database connection
db: 
    type: 'sqlite'
    connection: 'sqlite.db'

# Dashboard config
dashboard:
    FLASK_SERVER_NAME: '0.0.0.0'
    FLASK_SERVER_PORT: 8000
    FLASK_DEBUG: True  # Do not use debug mode in production

restplus:
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION: 'list'
    RESTPLUS_VALIDATE: True
    RESTPLUS_MASK_SWAGGER: False
    RESTPLUS_ERROR_404_HELP: False

# tf.txt client settings
tensorflow:
    TF_SERVER_NAME: '172.17.0.2'
    TF_SERVER_PORT: 9000
    TF_MODEL_NAME: 'default'
    TF_MODEL_SIGNATURE_NAME: 'helpers'
    TF_MODEL_INPUTS_KEY: 'states'

"""
