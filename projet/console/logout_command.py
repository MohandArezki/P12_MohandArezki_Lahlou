from controllers.user import UserManager

class LogoutCommand:
    """Class representing a command to log out a user."""
    description = "Log out of the application"
    usage = "logout"
    help_text = "This command allows you to log out of the application."

    @staticmethod
    def execute(console, arg):
        """
        Execute the logout command by logging out the user.

        Args:
            console (Console): The console object.
            arg (str): The command arguments.
        """
        if not arg:
            UserManager.logout()
        else:
            console.print_argument_not_found()
