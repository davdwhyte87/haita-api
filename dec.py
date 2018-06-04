

def decorator_function(original_function):
    def wrapper_function():
        print("decorator function started")
        return original_function()
    return wrapper_function()

@decorator_function
def display():
    print ("display function")
    return