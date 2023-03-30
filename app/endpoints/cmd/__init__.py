from ...core import *

class CmdAppContext(AppContext):

    def run(self, **kwargs):

        context = MessageContext()

        # Remove necessary arguments
        endpoint = kwargs.pop('endpoint')
        args = kwargs.pop('args')
        
        endpoint_config = self.endpoints[endpoint]
        handler = EndpointHandler(endpoint_config)
        handler.handle(context, args, self, **kwargs)


class CmdAppBuilder(AppBuilder):
    
    def build(self):
        return CmdAppContext(
            self._current_session.name,
            self._current_session.app_config,
            self._current_session.container_config
        )
