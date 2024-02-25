from controllers.database import DBManager
from controllers.user import UserManager
from controllers.customer import CustomerManager
from controllers.contract import ContractManager
from controllers.event import EventManager


class DeactivateCommand:
    """Class representing a command to deactivate objects."""
    description = "Deactivate activated entity"
    usage = "deactivate"
    help_text = "This command allows you to deactivate the current entity."

 
    @staticmethod
    def execute(console, arg):
        """
        Execute the deactivate command.

        Args:
            console (Console): The console object.
            arg (str): The command arguments.

        Raises:
            Exception: If an error occurs during execution.
        """
        manager_mapping = {
            "event": EventManager.deactivate,
            "contract": ContractManager.deactivate,
            "customer": CustomerManager.deactivate,
            "user": UserManager.deactivate,
        }
        object = DBManager.get_current_object()
    
        try:            
            manager_function = manager_mapping.get(object)
            if manager_function:
                manager_function()
            else:
                raise Exception(f"Invalid object specified: {object}. Type <help deactivate> for more details ")
        except Exception as e:
            print(e)
    