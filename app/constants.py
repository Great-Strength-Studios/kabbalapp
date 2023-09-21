
# Environment
APP_ENV = 'APP_ENV'
DEFAULT_APP_ENV = 'prod'
PROJECTS_FILE_PATH = 'PROJECTS_FILE_PATH'
DEBUG = 'DEBUG'

# Configuration file
APP_CONFIGURATION_FILE = 'app/app.yml'

# Configuration
CONFIGS = 'configs' 
ENDPOINTS = 'endpoints'
ERRORS = 'errors'

# Domain constants
DOMAIN_ROLE_TYPES = ['blacklist', 'whitelist']

# Printing file content
REQUIREMENTS_CONTENT = """
schematics>=2.1.1
pyyaml>= 6.0
"""


APP_CONFIG_CONTENT = {
    'endpoints': {},
    'errors': {},
    'events': {},
    'mappings': {
        'data': {},
        'header': {},
        'service': {}
    },
    'modules': {},
    'services': {},
}

