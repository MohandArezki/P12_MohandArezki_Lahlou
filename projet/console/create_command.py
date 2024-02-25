from controllers.database import DBManager
from controllers.user import UserManager
from controllers.customer import CustomerManager
from controllers.contract import ContractManager
from controllers.event import EventManager

class CreateCommand:
    """Class representing a command to create objects."""
    description = "Create a new entity"
    usage = "create -object <entity>"
    help_text = (
        "Create a new entity.\n"
        "Parameters:\n"
        "-object           Specify the type of entity to create.\n"
        "                   Possible values: user, customer, contract, event.\n\n"
        "Examples:\n"
        "create -object user\n"
        "create -object event\n"
    )

    @staticmethod
    def execute(console, arg):
        """
        Execute the create command.

        Args:
            console (Console): The console object.
            arg (str): The command arguments.

        Raises:
            ParameterErrorException: If an error occurs due to invalid parameters.
            Exception: If an unexpected error occurs during execution.
        """
        manager_mapping = {
            "event": EventManager.create,
            "contract": ContractManager.create,
            "customer": CustomerManager.create,
            "user": UserManager.create,
            "database": DBManager.create
        }
        object_arg, = console.extract_arguments(arg, "object")
        object_arg = object_arg or DBManager.get_current_object()
        try:
            manager_function = manager_mapping.get(object_arg)
            if manager_function:
                manager_function()
            else:
                raise Exception(f"Invalid object specified: {object_arg}. Type <help create> for more details ")
        except Exception as e:
            print(e)
