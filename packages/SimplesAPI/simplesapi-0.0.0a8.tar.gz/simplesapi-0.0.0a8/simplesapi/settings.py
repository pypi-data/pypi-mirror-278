from os import getenv

#########################################################################
#   DATABASE                                                            #
#########################################################################
SIMPLESAPI_DB_CONN = getenv("SIMPLESAPI_DB_CONN", None)

#########################################################################
#   REDIS                                                               #
#########################################################################
SIMPLESAPI_REDIS_URL = getenv("SIMPLESAPI_REDIS_URL", None)
SIMPLESAPI_REDIS_SSL = str(getenv("SIMPLESAPI_REDIS_SSL", "true")).lower() in ["1","true"]

#########################################################################
#   AWS                                                                 #
#########################################################################
AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY", None)
AWS_DEFAULT_REGION = getenv("AWS_DEFAULT_REGION", None)

