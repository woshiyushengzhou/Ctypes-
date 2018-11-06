
class ConnectError(Exception):
    def __init__(self,err='connect...err'):
        Exception.__init__(self,err)
