import os
from app import CmdAppBuilder, CmdAppContext, args, constants, ContainerConfiguration

  

# Pop env from args using default app env if not provided
env = args.args.pop('env', constants.DEFAULT_APP_ENV)

# Pop debug from args using false if not provided
debug = args.args.pop('debug', False)

# Preprocess
os.environ[constants.APP_ENV] = env

# Create builder
builder = CmdAppBuilder().create_new_app('kabbalapp')

# Set container configuration to builder
container_config = ContainerConfiguration()
container_config.app_project_filepath = os.getenv(constants.PROJECTS_FILE_PATH, None)
builder.set_container_config(container_config)

# Build app context.
app_context: CmdAppContext = builder.build()

# Run app context.
app_context.run(
    command = args.command,
    subcommands = args.subcommands,
    args=args.args, 
    env=env,
    debug=debug)