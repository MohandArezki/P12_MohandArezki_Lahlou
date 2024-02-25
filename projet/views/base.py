from prettytable import PrettyTable, ALL
from sqlalchemy import Integer, Float, Boolean, DateTime, Date

class BaseView:
    """Base class for creating views of database models."""

    def __init__(self, model, fields):
        """
        Initialize BaseView.

        Args:
            model: The database model associated with the view.
            fields: List of fields to be displayed in the view.
        """
        model = model
        fields = fields
    
    @classmethod
    def list(cls, records, title_msg):
        """
        Display a list view of records.

        Args:
            records: List of database records to be displayed.
            title_msg: Title message for the view.

        Raises:
            Exception: If an error occurs during the view creation.
        """
        try:
            tab = PrettyTable()    
            tab.hrules = ALL
            field_names=["#"]
            tab.add_column("#", [i for i in range(1, len(records) + 1)], align="c")
            for field in cls.fields:
                column_header=None
                try:
                    field_type = cls.model.__table__.columns[field].type
                    column_header = cls.model.__table__.columns[field].info.get("label", field.replace("_", " ").capitalize())
                    if isinstance(field_type, (Integer, Boolean)):
                        tab.add_column(column_header, [f"{getattr(record, field)}" for record in records], align="c")
                    elif isinstance(field_type, Float):
                        tab.add_column(column_header, [f"{getattr(record, field):,.2f}" for record in records], align="r")
                    elif isinstance(field_type, DateTime):
                        tab.add_column(column_header, [getattr(record, field).strftime("%Y-%m-%d %H:%M") if getattr(record, field) else "" for record in records], align="c")
                    elif isinstance(field_type, Date):
                        tab.add_column(column_header, [getattr(record, field).strftime("%Y-%m-%d") if getattr(record, field) else "" for record in records], align="c")
                    else:
                        tab.add_column(column_header, [f"{getattr(record, field)}" for record in records], align="l")
                except:
                    tab.add_column(column_header, [f"{getattr(record, field.lower())}" for record in records], align="l")
                field_names.append(column_header if column_header else field.replace("_", " ").capitalize())
            
            tab.field_names=field_names            
            print(tab.get_string(title=title_msg))
        except Exception as e:
            print(f"Error creating view: {e}")

