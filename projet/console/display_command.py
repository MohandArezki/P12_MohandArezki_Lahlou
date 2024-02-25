from controllers.database import DBManager
from controllers.user import UserManager
from controllers.customer import CustomerManager
from controllers.contract import ContractManager
from controllers.event import EventManager


class DisplayCommand:
    """Command to view objects."""
    description = "Display information"
    usage = "display -object <entity> [-filter <filter_option>] [-mode <display_mode>]"
    help_text = (
    "Display information about a specified entity.\n"
    "Parameters:\n"
    "-object           Specify the entity type to display information about.\n"
    "                   Possible values: user, customer, contract, event.\n\n"
    "Optional Parameters:\n"
    "-filter           Filter the displayed information based on specific criteria.\n"
    "Depending on the activated entity, available options vary:\n"
    "- For 'user': all, is_commercial, is_support, is_manager, default_value= activated entity.\n"
    "- For 'customer': all, with_contracts, without_contract, default_value= activated entity.\n"
    "- For 'contract': all, signed, not_signed, fully_paid, not_fully_paid, default_value= activated entity.\n"
    "- For 'event': all, passed, ongoing, planned, no_support, with_support, default_value= activated entity.\n"
    "-mode             Choose the display mode for the information.\n"
    "Possible values: list (default_value), expand.\n\n"
    "Examples:\n"
    "display -object user -filter all -mode expand\n"
    "display -object contract\n"
    "display -object event -filter ongoing\n"
)
    @staticmethod
    def execute(console, arg):
        manager_mapping = {
            "event": EventManager.display,
            "contract": ContractManager.display,
            "customer": CustomerManager.display,
            "user": UserManager.display
        }

        object, filter, mode= console.extract_arguments(arg, "object","filter","mode")
        object = object or DBManager.get_current_object()
        mode = mode or "list"
        
        try:
            if mode not in ["list", "expand"]:
                raise ValueError("Invalid mode specified.")
            
            manager_function = manager_mapping.get(object)
            
            if manager_function:
                manager_function(filter=filter, mode=mode)
            else:
                raise ValueError("Invalid object specified. Type <help display> for more details.")
        except ValueError as ve:
            print(str(ve))
        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")