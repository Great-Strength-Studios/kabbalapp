import os
from app import CliAppBuilder, CliAppContext, args, constants, ContainerConfiguration

  

# Pop env from args using default app env if not provided
env = args.args.pop('env', constants.DEFAULT_APP_ENV)

# Pop verbose from args using false if not provided
debug = args.args.pop('verbose', False)

# Preprocess
os.environ[constants.APP_ENV] = env

# Create builder
builder = CliAppBuilder().create_new_app('kabbalapp')

# Set container configuration to builder
container_config = ContainerConfiguration()
container_config.app_project_filepath = os.getenv(constants.PROJECTS_FILE_PATH, os.path.join(os.getcwd(), 'projects.yml'))
builder.set_container_config(container_config)

# Build app context.
app_context: CliAppContext = builder.build()

# Run app context.
app_context.run(
    command = args.command,
    function = args.subcommand,
    args=args.args, 
    env=env,
    debug=debug)