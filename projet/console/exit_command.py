from controllers.database import DBManager


class ExitCommand:
    """Class representing a command to exit the application."""
    description = "Exit the application"
    usage = "exit"
    help_text = "This command allows you to exit the application."


    @staticmethod
    def execute(console, arg):
        """
        Execute the exit command by closing the session.

        Args:
            console (Console): The console object.
            arg (str): The command arguments.
        """
        print("Closing session ...")
        DBManager.session().close()
