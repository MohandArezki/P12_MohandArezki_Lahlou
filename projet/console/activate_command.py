from controllers.database import DBManager
from controllers.user import UserManager
from controllers.customer import CustomerManager
from controllers.contract import ContractManager
from controllers.event import EventManager


class ActivateCommand:
    """Command to activate an object."""
    description = "activate an entity"
    usage = "activate -id <identifier>"
    help_text = "This command allows you to activate an entity by specifying its identifier."

    @staticmethod
    def execute(console, arg):
        """
        Execute the activate command.

        Args:
            console: The console instance.
            arg (str): The command arguments.

        Returns:
            None
        """
        manager_mapping = {
            "event": EventManager.activate,
            "contract": ContractManager.activate,
            "customer": CustomerManager.activate,
            "user": UserManager.activate,
        }

        object, id = console.extract_arguments(arg, "object", "id")
        object = object or DBManager.get_current_object()
    
        try:
            manager_function = manager_mapping.get(object)
            if manager_function:
                manager_function(id=id)
            else:
                raise Exception(f"Invalid object specified: {object}. Type <help activate> for more details ")
        except Exception as e:
            print(e)
    