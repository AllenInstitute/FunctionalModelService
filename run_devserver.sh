#! /bin/bash 
export FLASK_APP=run.py
export FLASK_ENV=development
export AUTH_URI=global.daf-apis.com/auth
export STICKY_AUTH_URL=global.daf-apis.com/sticky_auth
export FUNCTIONALMODELSERVICE_SETTINGS=$PWD/functionalmodelservice/instance/dev_config.py
python run.py
