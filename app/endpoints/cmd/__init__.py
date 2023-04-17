from ...core import *

class CmdAppContext(AppContext):

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
            handler.handle(args, self, **kwargs)
        except AppError as e:
            exit(str(e.to_dict()))


class CmdAppBuilder(AppBuilder):
    
    def build(self):
        return CmdAppContext(
            self._current_session.name,
            self._current_session.app_config,
            self._current_session.container_config
        )
