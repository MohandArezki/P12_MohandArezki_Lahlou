from models.contract import Contract
from controllers.base import BaseManager
from views.contract import ContractView
from decorators import requires_customer


class ContractManager(BaseManager):
    """
    Manager class for handling operations related to contracts.
    
    Inherits from BaseManager.

    Attributes:
        model: The Contract model.
        view: The ContractView class for handling views.
    """

    model = Contract
    view = ContractView

    @classmethod
    @requires_customer
    def create(cls):
        """
        Create a new contract.

        Requires the presence of a customer.

        Returns:
            None
        """
        return super().create()

    @classmethod    
    def update(cls, id=None):
        """
        Update an existing contract.

        Args:
            id (Optional): The ID of the contract to update.

        Requires the presence of a customer.

        Returns:
            None
        """
        return super().update(id=id)
