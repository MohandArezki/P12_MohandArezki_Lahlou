from datetime import datetime
from sqlalchemy import or_
from models.user import User
from models.event import Event
from models.contract import Contract
from models.customer import Customer

class FilterManager:
    """
    Class for managing filters on different objects.
    """
    default_filters_objects = [
        {
            "object": "Event",
            "filters": [
                {
                    "condition": "DBManager.activated_event is not None",
                    "filter": {
                        "message": "f'And(Event = {DBManager.activated_event}) '",
                        "expr_filter": "(Event.id == DBManager.activated_event.id,)",
                    },
                },
                {
                    "condition": "DBManager.activated_contract is not None",
                    "filter": {
                        "message": "f'And(Contract = {DBManager.activated_contract}) '",
                        "expr_filter": "(Event.contract_id == DBManager.activated_contract.id,)",
                    },
                },
                {
                    "condition": "DBManager.activated_customer is not None",
                    "filter": {
                        "message": "f'And(Customer = {DBManager.activated_customer}) '",
                        "expr_filter": "(Event.contract.has(Contract.customer_id == DBManager.activated_customer.id),)",
                    },
                },
                {
                    "condition": "DBManager.activated_commercial is not None",
                    "filter": {
                        "message": "f'And (Commercial = {DBManager.activated_commercial}) '",
                        "expr_filter": "(Event.contract.has(Contract.customer.has(Customer.contact_id == DBManager.activated_commercial.id)),)",
                    },
                },
                 {
                    "condition": "DBManager.activated_support is not None",
                    "filter": {
                        "message": "f'And (Support = {DBManager.activated_support}) '",
                        "expr_filter": "(Event.support_id == DBManager.activated_support.id,)",
                    },
                },
            ],
        },
        {
            "object": "Contract",
            "filters": [
                {
                    "condition": "DBManager.activated_contract is not None",
                    "filter": {
                        "message": "f'And(Contract = {DBManager.activated_contract}) '",
                        "expr_filter": "(Contract.id == DBManager.activated_contract.id,)",
                    },
                },
                {
                    "condition": "DBManager.activated_customer is not None",
                    "filter": {
                        "message": "f'And(Customer = {DBManager.activated_customer}) '",
                        "expr_filter": "(Contract.customer_id == DBManager.activated_customer.id,)",
                    },
                },  
                 {
                    "condition": "DBManager.activated_commercial is not None",
                    "filter": {
                        "message": "f'And(Commercial = {DBManager.activated_commercial}) '",
                        "expr_filter": "(Contract.customer.has(Customer.contact_id == DBManager.activated_commercial.id),)",
                    },
                },
            ],
        },
        {
            "object": "Customer",
            "filters": [
                {
                    "condition": "DBManager.activated_customer is not None",
                    "filter": {
                        "message": "f'And(Customer = {DBManager.activated_customer}) '",
                        "expr_filter": " (Customer.id == DBManager.activated_customer.id,)",
                    },
                },
                {
                    "condition": "DBManager.activated_commercial is not None",
                    "filter": {
                        "message": "f'And(Commercial = {DBManager.activated_commercial}) '",
                        "expr_filter": "(Customer.contact_id == DBManager.activated_commercial.id,)",
                    },
                },                   
            ],
        },
        {
            "object": "User",
            "filters": [
                {
                    "condition": "DBManager.activated_commercial is not None",
                    "filter": {
                        "message": "f'Commercial = {DBManager.activated_commercial} '",
                        "expr_filter": "(User.id == DBManager.activated_commercial.id,)",
                    }                    
                },
                {   "condition": "DBManager.activated_support is not None",
                    "filter": {
                        "message": "f'Support = {DBManager.activated_support} '",
                        "expr_filter": "(User.id == DBManager.activated_support.id,)",
                    },
                }    
            ],
        },
    ]
    filters_objects = [
        {
            "object": "Event",
            "filters": [
                {"argument":"all", "expr_filter": "()"},
                {"argument": "passed", "expr_filter": "(datetime.now() > Event.date_end,)"},
                {"argument": "ongoing", "expr_filter": "(datetime.now() >= Event.date_start, datetime.now() <= Event.date_end,)"},
                {"argument": "planned", "expr_filter": "(Event.date_start > datetime.now(),)"},
                {"argument": "without_support", "expr_filter": "(Event.support_id.is_(None),)"},
                {"argument": "with_support", "expr_filter": "(Event.support_id.isnot(None),)"},
            ],
        },
        {
            "object": "Contract",
            "filters": [
                {"argument":"all", "expr_filter": "()"},
                {"argument": "signed", "expr_filter": "(Contract.signed == True,)"},
                {"argument": "not_signed", "expr_filter": "(Contract.signed == False,)"},
                {"argument": "fully_paid", "expr_filter": "(Contract.due_amount <=0,)"},
                {"argument": "not_fully_paid", "expr_filter": "(Contract.due_amount >0,)"},
            ],
        },
        {
            "object": "User",
            "filters": [
                {"argument":"all", "expr_filter": "()"},
                {"argument": "commercial", "expr_filter": "(User.department == 'C',)"},
                {"argument": "support", "expr_filter": "(User.department == 'S',)"},
                {"argument": "manager", "expr_filter": "(User.department == 'M',)"},
            ],
        },
        {
            "object": "Customer",
            "filters": [
                {"argument":"all", "expr_filter": "()"},
                {"argument":"with_contracts", "expr_filter": "(User.contracts != [],)"},
                {"argument":"without_contract", "expr_filter": "(User.contracts == [],)"},
            ],
        },
    ]    
   
    @classmethod
    def set_default_filter(cls, object):
        """
        Set default filters for the given object.

        Args:
            cls: Class reference.
            object: The object for which filters need to be set.

        Returns:
            Tuple: A tuple containing a message and expression filter based on default conditions.
        """
        from controllers.base import DBManager


        msg = ""
        expr_filter = ()
               
        for default_filters_object in cls.default_filters_objects:
            if default_filters_object['object'] == object.__name__:
                for condition_filter in default_filters_object['filters']:
                    if condition_filter['filter']!="all":
                        if eval(condition_filter['condition']):
                            msg += eval(condition_filter['filter']['message'])
                            expr_filter += eval(condition_filter['filter']['expr_filter'])
                            
        return msg, expr_filter
    
    @classmethod
    def available_object_filters(cls, object_name):
        return [filter_item["argument"] for filters_object in cls.filters_objects
                            if filters_object["object"] == object_name
                            for filter_item in filters_object["filters"]]

    @classmethod
    def parse_filter_arguments(cls, object, filter_arg):
        """
        Parse filter arguments for the given object.

        Args:
            object: The object for which filters need to be parsed.
            filter_arg: Filter arguments as a string.

        Returns:
            Tuple: A tuple containing a message and expression filter based on parsed conditions.
        """
        from controllers.base import DBManager

        expr_filter = ()
        msg = ""
        msg, expr_filter = cls.set_default_filter(object)
        if not filter_arg:
            return msg, expr_filter
        
        filter_args = filter_arg.split(" ")
        valid_filters = cls.available_object_filters(object.__name__)
        if "all" in filter_args:
            expr_filter = ()
            msg = ""
                
        for arg in filter_args:
            if arg in valid_filters:
                for filters_object in cls.filters_objects:
                    if filters_object['object'] == object.__name__:
                        for filter in filters_object['filters']:                                                       
                            if arg == filter['argument']:
                                expr_filter += eval(filter['expr_filter'])
                                msg = msg + arg + " "
                                break
            else:
                raise ValueError(f"Invalid filter argument ({arg}) for {object.__name__}. Available filters {valid_filters}")
        return msg, expr_filter
