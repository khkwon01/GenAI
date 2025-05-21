class AskMEException(Exception):
    pass

class BackendConfigurationException(AskMEException):
    pass

class BackendConnectionException(AskMEException):
    pass

class BackendExecutionException(AskMEException):
    pass

class UnknownException(AskMEException):
    pass
