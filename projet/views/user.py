"""
Module for handling User views.
"""

from prettytable import PrettyTable, NONE,ALL
import pyinputplus as pyip
import hashlib

from models.user import User
from views.base import BaseView

class UserView(BaseView):
    """
    UserView class for handling user creation, updating, and display.
    """
    model = User
    fields = ["id", "Fullname", "email", "department_name"]

    @classmethod
    def create_update(cls,user=None):
        try:
            create = user is None
            action_label = "Creating" if create else "Updating"

            print(f" ----------------------- {action_label} user -----------------------")
            user = user or User()

            fullname_prompt = f" Fullname ({user.fullname}): " if not create else " Fullname : "
            email_prompt = f" Email : " if create else f" Email ({user.email}): "
            department_prompt = f" Department M,C,S : " if create else f" Department M,C,S ({user.department}): "

            fullname = pyip.inputStr(prompt=fullname_prompt, default=user.fullname, limit=30, blank=not create)
            email = pyip.inputEmail(prompt=email_prompt, default=user.email, limit=30, blank=not create)
            department = pyip.inputChoice(['M', 'S', 'C'], prompt=department_prompt, default=user.department, blank=not create)

            password = pyip.inputPassword(prompt=" Password : ", limit=20, blank=not create)
            password_confirm = pyip.inputPassword(prompt=" Confirm password : ", limit=20, blank=not create)

            if password != password_confirm:
                raise Exception(" Password and Confirm Password do not match.")

            user.fullname = fullname or user.fullname
            user.email = email or user.email
            user.department = department or user.department
            user.password = hashlib.sha256(password.encode()).hexdigest() if password else user.password
        except Exception as e:
            print(e)
        return user
    
    @classmethod
    def authenticate(cls, email):      
        print(f" -----User ({email}) authentication -----")
        password = pyip.inputPassword(prompt=" Password: ", limit=20)
        return password  

    @classmethod
    def expand(cls, users, title_msg):

        tab = PrettyTable()
        tab.field_names = ["#", "Details"]
        tab.align["Details"] = "l"
        contract_tab = PrettyTable()
        contract_tab.min_table_width = 95
        contract_tab.field_names = ["", "Count", "Total Amount", "Total Due"]
        contract_tab.align["Count"] = "c"
        contract_tab.align["Count", "Total Amount", "Total Due"] = "r"
        contract_tab.align[""] = "l"
        
        event_tab = PrettyTable()
        event_tab.min_table_width = 95
        event_tab.field_names = ["", "All", "Passed", "Ongoing", "Planned"]
        event_tab.align["All", "Passed", "Ongoing", "Planned"] = "r"
        event_tab.align[""] = "l"
        
        for index, user in enumerate(users):
            formatted_string = f"ID: {user.id}\n"
            formatted_string += f"Fullname: {user.fullname} - {user.department_name}\n"
            formatted_string += f"Email: {user.email}\n"

            if user.department == "C":
                formatted_string += f"Assigned Customers: {user.customers_count()}\n"
                contract_tab.clear_rows()
                contract_tab.add_row(["All contracts",
                                      user.contracts_count(),
                                      f"{user.contracts_total_amount():,.2f}",
                                      f"{user.contracts_due_amount():,.2f}"
                                      ])
                contract_tab.add_row(["Signed contracts",
                                      user.contracts_count([True]),
                                      f"{user.contracts_total_amount([True]):,.2f}",
                                      f"{user.contracts_due_amount([True]):,.2f}"
                                      ])
                contract_tab.add_row(["Not signed contracts",
                                      user.contracts_count([False]),
                                      f"{user.contracts_total_amount([False]):,.2f}",
                                      f"{user.contracts_due_amount([False]):,.2f}"])
                
                formatted_string += contract_tab.get_string(title="Contracts")+"\n"
                
                event_tab.clear_rows()
                event_tab.add_row(["Count",
                                   user.events_count(),
                                   user.events_count(['Passed']),
                                   user.events_count(['Ongoing']),
                                   user.events_count(['Planned'])
                                   ])
                formatted_string +=event_tab.get_string(title="Events")+"\n"

            elif user.department == "S":
                event_tab.clear_rows()
                event_tab.add_row(["Count",
                                   user.supported_events_count(),
                                   user.supported_events_count(['Passed']),
                                   user.supported_events_count(['Ongoing']),
                                   user.supported_events_count(['Planned'])
                                   ])
                formatted_string += event_tab.get_string(title="Supported Events")+"\n"

            tab.add_row([index + 1, formatted_string])

        print(tab.get_string(title=title_msg))
