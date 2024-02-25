"""
Module for handling Contract views.
"""

from prettytable import PrettyTable, ALL,NONE
import pyinputplus as pyip

from models.contract import Contract
from views.base import BaseView 
from controllers.database import DBManager

class ContractView(BaseView):
    """
    Class for creating and displaying Contract views.
    """
    model = Contract
    fields = ["id", "contract_date", "state", "customer","contact", "total_amount", "due_amount"]

    @classmethod
    def create_update(cls, contract=None):
        create = contract is None
        action_label = "Creating" if create else "Updating"

        print(f"----------------------- {action_label} contract -----------------------")
        contract = contract or Contract()

        contract_date_prompt = " Date (yyyy-mm-dd) : " if  create else f" Date (yyyy-mm-dd) ({contract.contract_date}): "
        total_amount_prompt = f" Total amount: " if create else f" Total amount ({contract.total_amount}): "
        due_amount_prompt = f" Due amount: " if create else f" Phone number ({contract.due_amount}): "
        signed_prompt = f" Contract signed ? (Y/N): " if create else f" Contract signed ? (Y/N) ({'Y' if contract.signed else 'N'}): "

        contract_date = pyip.inputDate(prompt=contract_date_prompt, default=contract.contract_date, formats=['%Y-%m-%d'],blank=not create)
        total_amount = pyip.inputFloat(prompt=total_amount_prompt, min=0, default=contract.total_amount,blank=not create)
        due_amount = pyip.inputFloat(prompt=due_amount_prompt, min=0, default=contract.due_amount,blank=not create)
        signed = (pyip.inputYesNo(prompt=signed_prompt, default="N" if contract.signed else "Y") == "yes")

        contract.contract_date = contract_date or contract.contract_date
        contract.total_amount = total_amount or contract.total_amount
        contract.due_amount = due_amount or contract.due_amount
        contract.signed = signed
     
        if create :
            contract.customer = DBManager.activated_customer
        elif DBManager.activated_customer and DBManager.activated_customer.id != contract.customer_id:
            if pyip.inputYesNo(f"Assign {DBManager.activated_customer} as a new customer? (Y/N): ", default="N"):
                contract.customer = DBManager.activated_customer

        return contract

    @classmethod
    def expand(cls, contracts, title_msg):
        """
        Display expanded information about contracts.

        Args:
            contracts (list): List of contracts to display.
            title_msg (str): Title message for the table.
        """
        tab = PrettyTable()
        tab.field_names = ["#", "Details"]
        tab.align["Details"] = "l"
        
        event_tab = PrettyTable()
        event_tab.min_table_width = 95
        event_tab.field_names = ["", "All", "Passed", "Ongoing", "Planned"]
        event_tab.align["All", "Passed", "Ongoing", "Planned"] = "r"
        event_tab.align[""] = "l"
        for index, contract in enumerate(contracts):
            
            formatted_string = f"ID: {contract.id}\n"
            formatted_string += f"Date: {contract.contract_date.strftime('%Y-%m-%d') if contract.contract_date else '--------'}\n"
            formatted_string +=f"Total amount: {contract.total_amount:,.2f}\n"
            formatted_string +=f"Due amount  : {contract.due_amount:,.2f}\n"
            formatted_string +=f"State : {contract.state}\n"
            formatted_string +=f"Customer:{contract.customer}\n{contract.customer.company}\n"
            formatted_string +=f"Commercial contact: {contract.customer.contact}\n"

            event_tab.clear_rows()
            event_tab.add_row(["Count",
                                    contract.events_count(),
                                    contract.events_count(['Passed']),
                                    contract.events_count(['Ongoing']),
                                    contract.events_count(['Planned'])
                                    ])
            formatted_string += event_tab.get_string(title="Events")
                            
            tab.add_row([index + 1, formatted_string])


        print(tab.get_string(title=title_msg))
