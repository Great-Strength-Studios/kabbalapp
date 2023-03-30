import os

from app import load_app_config, load_container_config, constants
from app.endpoints.cmd import CmdAppBuilder, CmdAppContext, arguments as args

  
# Remove system arguments
env = args.args.pop('env', constants.DEFAULT_APP_ENV)
debug = args.args.pop('debug', False)

# Preprocess
os.environ[constants.APP_ENV] = env

builder = CmdAppBuilder().create_new_app('kabbalapp')
load_app_config(builder)
load_container_config(builder)

app_context: CmdAppContext = builder.build()

app_context.run(
    endpoint = args.endpoint,
    args=args.args, 
    env=env,
    debug=debug)