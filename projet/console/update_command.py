from controllers.database import DBManager
from controllers.user import UserManager
from controllers.customer import CustomerManager
from controllers.contract import ContractManager
from controllers.event import EventManager


class UpdateCommand:
    """Class representing a command to update objects."""
    description = "Update an existing entity"
    usage = "update -object <entity> -id <identifier>"
    help_text = (
    "Update an existing entity.\n"
    "Parameters:\n"
    "-object           Specify the type of entity to update.\n"
    "                   Possible values: user, customer, contract, event.\n"
    "<-id>             Specify the ID of the entity to update.\n\n"
    "Examples:\n"
    "update -object user -id 123\n"
    "update -object event -id 456\n"
)

   
    @staticmethod
    def execute(console, arg):
        """
        Execute the update command.

        Args:
            console: The console instance.
            arg (str): The command arguments.

        Returns:
            None
        """
        manager_mapping = {
            "event": EventManager.update,
            "contract": ContractManager.update,
            "customer": CustomerManager.update,
            "user": UserManager.update,
        }

        object, id, = console.extract_arguments(arg, "object", "id")
        object = object or DBManager.get_current_object()    
        active_instance = getattr(DBManager, f"activated_{object}", None)
        try:
            if not id:
                if active_instance and hasattr(active_instance, 'id'):
                    id = active_instance.id

            manager_function = manager_mapping.get(object)
            if manager_function:
                manager_function(id=id)
            else:
                raise ValueError(f"Invalid object specified: {object}. Type <help update> for more details.")

        except (ValueError, Exception) as e:
            print(f"An error occurred: {str(e)}")
