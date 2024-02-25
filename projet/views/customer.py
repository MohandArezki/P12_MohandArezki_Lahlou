"""
Module for handling Customer views.
"""

from prettytable import PrettyTable, ALL, NONE
import pyinputplus as pyip

from utils import check_phone
from models.customer import Customer
from views.base import BaseView 
from controllers.database import DBManager

class CustomerView(BaseView):
    """
    Class for creating and displaying Customer views.
    """
    model = Customer
    fields = ["id", "name", "email", "phone", "company", "Contact", "created_date", "updated_date"]

    @classmethod
    def create_update(cls, customer=None):     
        create = customer is None
        action_label = "Creating" if create else "Updating"

        print(f"----------------------- {action_label} customer -----------------------")
        customer = customer or Customer()

        name_prompt = " Name : " if  create else f" Name ({customer.name}): "
        email_prompt = f" Email : " if create else f" Email ({customer.email}): "
        phone_prompt = f" Phone number :" if create else f" Phone number ({customer.phone}): "
        company_prompt = f" Company : " if create else f" Company ({customer.company}): "

        name = pyip.inputStr(prompt=name_prompt, default=customer.name, limit=30, blank=not create)
        email = pyip.inputEmail(prompt=email_prompt, default=customer.email, limit=30, blank=not create)
        phone = pyip.inputCustom(check_phone, prompt=phone_prompt, blank=True)
        company = pyip.inputStr(prompt=company_prompt, default=customer.company, limit=30, blank=not create)

        customer.name = name or customer.name
        customer.email = email or customer.email
        customer.phone = phone or customer.phone
        customer.company = company or customer.company
        
        if create :
            customer.contact = DBManager.activated_commercial
        elif DBManager.activated_commercial and DBManager.activated_commercial.id != customer.contact_id:
            if pyip.inputYesNo(f"Assign {DBManager.activated_commercial} as a new contact? (Y/N): ", default="N") == 'yes':
                customer.contact = DBManager.activated_commercial
        
        return customer

    @classmethod
    def expand(cls, customers, title_msg):
        """
        Display expanded information about customers.

        Args:
            customers (list): List of customers to display.
            title_msg (str): Title message for the table.
        """
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
        for index, customer in enumerate(customers):

            formatted_string = f"ID: {customer.id}\n"
            formatted_string += f"Name: {customer.name}\n"
            formatted_string += f"Email: {customer.email}\n"
            formatted_string += f"Phone: {customer.phone}\n"
            formatted_string += f"Company: {customer.company}\n"
            formatted_string += f"Created on: {customer.created_date.strftime('%Y-%m-%d %H:%M:%S') if customer.created_date else '-------- --:--:--'}\n"
            formatted_string += f"Updated on: {customer.updated_date.strftime('%Y-%m-%d %H:%M:%S') if customer.updated_date else '-------- --:--:--'}\n"
            formatted_string += f"Managed by: {customer.contact}\n"
            contract_tab.clear_rows()
            contract_tab.add_row(["All contracts",
                                      customer.contracts_count(),
                                      f"{customer.contracts_total_amount():,.2f}",
                                      f"{customer.contracts_due_amount():,.2f}"
                                      ])
            contract_tab.add_row(["Signed contracts",
                                      customer.contracts_count([True]),
                                      f"{customer.contracts_total_amount([True]):,.2f}",
                                      f"{customer.contracts_due_amount([True]):,.2f}"
                                      ])
            contract_tab.add_row(["Not signed contracts",
                                      customer.contracts_count([False]),
                                      f"{customer.contracts_total_amount([False]):,.2f}",
                                      f"{customer.contracts_due_amount([False]):,.2f}"])
                
            formatted_string += "\n"+contract_tab.get_string(title="Contracts")
                
            event_tab.clear_rows()
            event_tab.add_row(["Count",
                                   customer.events_count(),
                                   customer.events_count(['Passed']),
                                   customer.events_count(['Ongoing']),
                                   customer.events_count(['Planned'])
                                   ])
            formatted_string += "\n"+event_tab.get_string(title="Events")
                        
            tab.add_row([index + 1, formatted_string])
    
        print(tab.get_string(title=title_msg))
