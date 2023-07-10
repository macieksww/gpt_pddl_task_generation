class TimeoutException(Exception):
    """
    Exception raised when the wait time for GPT or Atlas MongoDB Cluster 
    exceeds the set timeout
    """
    def __init__(self, raised_in_function):
        super().__init__(self.raised_in_function)
        print('Raised in function: ' + str(raised_in_function))

class ExectionHandlers:
    def __init__(self):
        pass
    
    def timeout_handler(self, signum, frame):   # Custom signal handler
        raise TimeoutException
