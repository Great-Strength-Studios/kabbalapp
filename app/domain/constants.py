# Domain model types
DOMAIN_MODEL_TYPES = [
    'entity',
    'value_object'
]

# Type constants
STR_TYPE =  'str'
INT_TYPE = 'int'
FLOAT_TYPE = 'float'
BOOL_TYPE = 'bool'
DATETIME_TYPE = 'datetime'
DATE_TYPE = 'date'
TIMESTAMP_TYPE = 'timestamp'
LIST_TYPE = 'list'
DICT_TYPE = 'dict'
POLY_TYPE = 'poly'
MODEL_TYPE = 'model'

DOMAIN_PROPERTY_TYPES = [
    STR_TYPE,
    INT_TYPE,
    FLOAT_TYPE,
    BOOL_TYPE,
    DATETIME_TYPE,
    DATE_TYPE,
    TIMESTAMP_TYPE,
    LIST_TYPE,
    DICT_TYPE,
    POLY_TYPE,
    MODEL_TYPE
]

# Dependency types
PROPERTY_DEPENDENCY = 'property'
BASE_TYPE_DEPENDENCY = 'base_type'
METHOD_DEPENDENCY = 'method'
METHOD_PARAMETER_DEPENDENCY = 'method_parameter'

DOMAIN_MODEL_DEPENDENCY_TYPES = [
    PROPERTY_DEPENDENCY,
    BASE_TYPE_DEPENDENCY,
    METHOD_DEPENDENCY,
    METHOD_PARAMETER_DEPENDENCY
]

TAB = '    '