class TimeoutException(BaseException):
    """
    Exception raised when the wait time for GPT or Atlas MongoDB Cluster 
    exceeds the set timeout
    """
    # def __init__(self, raised_in_function):
    #     super().__init__()
    #     print('Raised in function: ' + str(raised_in_function))
    def __init__(self):
        print("Timeout Exception")
        # super().__init__()
        # pri

class AttributeErrorException(BaseException):
    """
    Exception raised when the given atrribute is of wrong type
    """
    def __init__(self, raised_in_function):
        super().__init__()
        print('Raised in function: ' + str(raised_in_function))
        return 'lala'

class WrongPathException(BaseException):
    """
    Exception raised when the given path doesn't exist
    """
    def __init__(self, raised_in_function):
        super().__init__()
        print('Raised in function: ' + str(raised_in_function))

class DockerAPIException(BaseException):
    """
    Exception raised when the given path doesn't exist
    """
    def __init__(self, raised_in_function):
        super().__init__()
        print('Raised in function: ' + str(raised_in_function))
        return 'lala'

class ExectionHandlers:
    def __init__(self):
        pass

    def timeout_handler(self, raised_in_function):   # Custom signal handler
        raise TimeoutException()
    
    def attribute_error_handler(self, raised_in_function):
        raise AttributeErrorException(raised_in_function)
        
