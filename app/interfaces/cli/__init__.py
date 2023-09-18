from ...core import *
from ...features import *

INTERFACE = 'cli'

class CliAppContext(AppContext):

    def run(self, **kwargs):

        # Remove necessary arguments
        command = kwargs.pop('command')
        function = kwargs.pop('function')
        args = kwargs.pop('args')

        
        # Load endpoint configuration.
        try:
            endpoint_config = self.modules[command].features[function]
        except (TypeError, KeyError):
            raise AppError(self.errors.ENDPOINT_NOT_FOUND.format_message(command, function))
        
        # Create endpoint handler.
        handler = FeatureHandler(endpoint_config)
        
        # Handle message context.
        try:
            result = handler.handle(args, self, **kwargs)
        except AppError as e:
            exit(str(e.to_dict()))

        # Print result if not empty.
        if result:
            import json
            print(json.dumps(result, indent=4, sort_keys=True))


class CliAppBuilder(AppBuilder):
    
    def build(self):
        return CliAppContext(
            self._current_session.name,
            INTERFACE,
            self._current_session.app_config,
            self._current_session.container_config
        )
