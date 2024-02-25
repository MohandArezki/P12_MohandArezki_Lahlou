import os
import cmd
import console
from controllers.database import DBManager


class Console(cmd.Cmd):
    """Interactive console for CRM application."""

    def __init__(self):
        """Initialize the console."""
        super().__init__()
        self.commands = {
            'exit': console.ExitCommand(),
            'help': console.HelpCommand(),
            'login': console.LoginCommand(),
            'logout': console.LogoutCommand(),
            'create': console.CreateCommand(),
            'update': console.UpdateCommand(),
            'delete': console.DeleteCommand(),
            'activate': console.ActivateCommand(),
            'deactivate': console.DeactivateCommand(),
            'display': console.DisplayCommand(),
        }  

        self.do_login("-email admin@epic.com")
        self.do_activate("-object user -id 5")
        self.do_create("-object customer")
        
        self.postcmd("")

    def do_login(self, arg):
        """Login command handler."""
        self.commands['login'].execute(self, arg)

    def do_logout(self, arg):
        """Logout command handler."""
        self.commands['logout'].execute(self, arg)

    def do_exit(self, arg):
        """Exit command handler."""
        self.commands['exit'].execute(self, arg)
        return True

    def do_help(self, arg):
        self.commands['help'].execute(self, arg)

    def do_create(self, arg):
        """Create command handler."""
        self.commands['create'].execute(self, arg)

    def do_update(self, arg):
        """Update command handler."""
        self.commands['update'].execute(self, arg)

    def do_display(self, arg):
        """display command handler."""
        self.commands['display'].execute(self, arg)

    def do_activate(self, arg):
        """activate command handler."""
        self.commands['activate'].execute(self, arg)

    def do_deactivate(self, arg):
        """Deactivate command handler."""
        self.commands['deactivate'].execute(self, arg)
  
    def do_delete(self, arg):
        """delete command handler."""
        self.commands['delete'].execute(self, arg)
    def do_clear(self, arg):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def postcmd(self, stop=False, line=""):
        """Called after a command has been executed."""
        self.prompt = "_" * 100 + "\n" + " Welcome - EPIC-CRM ".center(100, "_")+"\n{} [-] Type command >> ".format(DBManager.info_activate())
        return stop

    def precmd(self, line: str) -> str:
        """Run before each command is executed."""
        return line.lower()

    def default(self, command):
        """Handle a default command when the entered command is not recognized."""
        print(f"Command not found: {command}. Type 'help'clear for available command expands.")

    def extract_arguments(self, arg, *arguments):
        """Extract arguments from the command."""
        args = arg.split()
        extracted_arguments = {arg: None for arg in arguments}

        current_arg = None
        for item in args:
            if item.startswith('-') and item.lstrip('-') in arguments:
                current_arg = item.lstrip('-')
            elif current_arg is not None:
                extracted_arguments[current_arg] = (extracted_arguments[current_arg] or '') + ' ' + item

        extracted_values = [extracted_arguments[arg].strip() if extracted_arguments[arg] is not None else None for arg in arguments]
        return extracted_values