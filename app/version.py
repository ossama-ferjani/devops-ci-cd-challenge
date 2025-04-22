import os
def get_version():
    return os.environ.get("APP_VERSION", "undefined")