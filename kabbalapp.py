import os
from app import CmdAppBuilder, CmdAppContext, args, constants

  

# Pop env from args using default app env if not provided
env = args.args.pop('env', constants.DEFAULT_APP_ENV)

# Pop debug from args using false if not provided
debug = args.args.pop('debug', False)

# Preprocess
os.environ[constants.APP_ENV] = env

builder = CmdAppBuilder().create_new_app('kabbalapp')

app_context: CmdAppContext = builder.build()

app_context.run(
    endpoint = args.endpoint,
    args=args.args, 
    env=env,
    debug=debug)