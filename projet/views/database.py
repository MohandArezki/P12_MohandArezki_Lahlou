import pyinputplus as pyip


class DBView:
    """
    Class for handling database view.
    """
    @classmethod
    def credentials(cls):
        """
        Get superadmin credentials.

        Returns:
            tuple: Username and password.
        """
        print("------------- Superadmin credentials ----------")
        username = pyip.inputStr(prompt=" Username : ")
        password = pyip.inputPassword(prompt=" Password : ")
        return username, password
