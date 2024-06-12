'''
A lunarcord extension consisting of all the exceptions that might be raised by lunarcord in case of an error.
This is for internal usage only.
'''

class LunarcordError(Exception):    
    def __init__(self, error: str = None):
        '''Base exception class for all Lunarcord Exceptions.
        You can catch all lunarcord-related errors by doing so:
        
        ```
        try:
            ...
        except LunarcordError:
            ...
        ```
        '''
        
        if error is None:
            error = 'Unhandled Lunarcord Error'
        super().__init__(error)
        
class ParameterError(LunarcordError):
    def __init__(self, typeOrValue):
        '''
        Invalid parameter
        '''
        
        super().__init__(f'Invalid parameter type or value: {typeOrValue}')
        
class InteractionError(LunarcordError):
    def __init__(self, message):
        '''
        Interaction error
        '''
        
        super().__init__(message)
        
class InteractionRespondedError(InteractionError):
    def __init__(self):
        '''
        Interaction has already been responded to before
        '''
        
        super().__init__('Interaction has already been responded to before')
        
class InteractionNotRespondedError(InteractionError):
    def __init__(self):
        '''
        Interaction has not been responded to before
        '''
        
        super().__init__('Interaction has not been responded to before')
        
class RequestError(LunarcordError):
    def __init__(self, code: int, message: str, method: str = 'get'):
        '''
        HTTP Request Error
        '''
        
        #method = method.lower()
        
        self.code    = code
        self.message = message
        self.method  = method
        
        if self.code is None:
            ... #self.message = f'{self.message} ({self.method.upper()})'

        self.message = message.removesuffix(".")
        
        super().__init__(self.message)
        
class ActionError(LunarcordError):
    def __init__(self, message):
        '''
        Invalid request action
        '''
        
        
        super().__init__(message)
        
class UnauthorizedError(LunarcordError):
    def __init__(self):
        '''
        Invalid token
        '''
        
        super().__init__('Invalid token')
        
class PermissionsError(LunarcordError):    
    def __init__(self):
        '''
        Not enough permissions
        '''
        
        super().__init__('Not enough permissions')
        
class StatusError(LunarcordError):
    def __init__(self, type: int = 0):
        '''
        Invalid custom bot status
        '''
        
        if type == 0:
            type = 'Custom Activity'
        elif type == 1:
            type = 'Status Type'
            
        message = f'Invalid {type} used in your bot\'s custom status!'
        
        super().__init__(message)
        
class IllegalError(LunarcordError):
    
    def __init__(self, message: str):
        
        '''
        Illegal action
        '''
        
        super().__init__(message)
        
        
class RegisterError(LunarcordError):
    
    def __init__(self, type: str):
        
        type = type.lower()
        
        if type == 'registered':

            super().__init__('Object has already been registered')
            
        if type == 'notregistrable':
        
            name = object.__name__
            super().__init__(f'Object of type {name} is not registrable')
            
        if type == 'noattribute':
        
            name = object.__name__
            super().__init__(f'Object of type {name} has no __register__ attribute')
            
            
class UnregisterError(LunarcordError):
    
    def __init__(self, type: str):
        
        type = type.lower()
        
        if type == 'notregistered':

            super().__init__('Object has not been registered before')
            
        if type == 'notregistrable':
        
            name = object.__name__
            super().__init__(f'Object of type {name} is not registrable')
            
        if type == 'noattribute':
        
            name = object.__name__
            super().__init__(f'Object of type {name} has no __unregister__ attribute')
        

        
class ReregisterError(LunarcordError):
    
    def __init__(self, type: str):
        
        type = type.lower()
        
        if type == 'notregistered':

            super().__init__('Object has not been registered before')
            
        if type == 'notregistrable':
        
            name = object.__name__
            super().__init__(f'Object of type {name} is not registrable')
            
        if type == 'noattribute':
        
            name = object.__name__
            super().__init__(f'Object of type {name} has no __reregister__ attribute')
            
class NotRegisteredError(LunarcordError):

    def __init__(self, view):

        super().__init__(f"View {view.name} was never registered")
            
class ConnectionClosedError(LunarcordError):
    
    def __init__(self):
        
        super().__init__('Gateway connection has been closed.')