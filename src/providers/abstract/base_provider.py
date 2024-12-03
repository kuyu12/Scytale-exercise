import abc


class BaseProvider():
    __metaclass = abc.ABCMeta
    """ Provider to work with a external service provider """

    def __init__(self, display_name):
        self.display_name = display_name
        self._auth_obj = self._get_auth_obj()

    def _get_auth_obj(self):
        """  Obtain an authorized connection object to interact with an external service provider"""
        return {}
