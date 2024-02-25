from controllers.user import UserManager


class LoginCommand:
    """Class representing a command to log in a user."""
    description = "Log in to the application"
    usage = "login -email <email>"
    help_text = "This command allows you to log in to the application by providing an email address."

    @staticmethod
    def execute(console, arg):
        """
        Execute the login command by attempting to log in the user.

        Args:
            console (Console): The console object.
            arg (str): The command arguments.
        """
        try:
            email, = console.extract_arguments(arg, "email")

            if email:
                UserManager.login(email)
            else:
                raise Exception(f"Invalid parameter. Type <help login> for more details ")
        except Exception as e:
            print(e)
    