from ...core import *

class CmdAppContext(AppContext):

    def run(self, **kwargs):

        context = MessageContext()

        # Remove necessary arguments
        command = kwargs.pop('command')
        function = kwargs.pop('function')
        args = kwargs.pop('args')

        # Format endpoint.
        function_str = '.'.join(function)
        
        # Load endpoint configuration.
        try:
            endpoint_config = self.endpoints[endpoint]
        except (TypeError, KeyError):
            raise AppError(ENDPOINT_NOT_FOUND.format_message(command, function_str))
        
        # Create endpoint handler.
        handler = EndpointHandler(endpoint_config)
        
        # Handle message context.
        handler.handle(context, args, self, **kwargs)


class CmdAppBuilder(AppBuilder):
    
    def build(self):
        return CmdAppContext(
            self._current_session.name,
            self._current_session.app_config,
            self._current_session.container_config
        )
