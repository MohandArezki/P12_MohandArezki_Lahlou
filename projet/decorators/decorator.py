def requires_connection(func):
    """
    Decorator to require authentication for a specific function.
    :param func: The function to be decorated.
    :return: The decorated function.
    """

    def wrapper(*args, **kwargs):
        from controllers.authenticate import AuthManager
        from controllers.database import DBManager       
        
        if AuthManager.validate_token():

            return func(*args, **kwargs)
        else:
            print("Authentication failed. Please log in again.")
        return None

    return wrapper

def requires_customer( func):
    """
    Decorator to ensure a activated user is from the commercial department.

    :param func: The function to be decorated.
    :return: The decorated function.
    """
    def wrapper(*args, **kwargs):        
        from controllers.database import DBManager
        if DBManager.activated_customer is not None:
            return func(*args, **kwargs)
        else:
            print("Activate a customer. Type <Help activate> to get more details")

    return wrapper

def requires_signed_contract(func):
    """
    Decorator to ensure that the activated contract is signed before executing the decorated function.

    Args:
        func: The function to be decorated.

    Raises:
        Exception: If the contract is not signed.
    """
    def wrapper(*args, **kwargs):
        from controllers.database import DBManager
        if DBManager.activated_contract is not None and DBManager.activated_contract.signed:
            return func(*args, **kwargs)
        else: 
             print("activate signed contract first.Type <Help activate> to get more details")
    return wrapper

def requires_commercial( func):
    """
    Decorator to ensure a activated user is from the commercial department.

    :param func: The function to be decorated.
    :return: The decorated function.
    """
    def wrapper(*args, **kwargs):        
        from controllers.database import DBManager
        if DBManager.activated_commercial is not None:
            return func(*args, **kwargs)
        else:
            print("Activate a user from the commercial department. Type <Help activate> to get more details")

    return wrapper

def requires_support( func):
    """
    Decorator to ensure a activated user is from the support department.

    :param func: The function to be decorated.
    :return: The decorated function.
    """
    def wrapper(*args, **kwargs):        
        from controllers.database import DBManager

        if DBManager.activated_support is not None:
            return func(*args, **kwargs)
        else:
            print("Activate a user from the support department. Type <Help activate> to get more details")

    return wrapper

def requires_permissions(action=None):
    def decorator(class_methode):
        def wrapper(cls, *args, **kwargs):
            from controllers.permission import PermissionManager
            if PermissionManager.check_permissions(obj=cls.model, action=action, id_instance=kwargs.get('id',None)):
                return class_methode(cls, *args, **kwargs)
        return wrapper
    return decorator

