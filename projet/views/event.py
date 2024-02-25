"""
Module for handling Event views.
"""

from prettytable import PrettyTable
import pyinputplus as pyip

from models.event import Event
from views.base import BaseView
from controllers.database import DBManager

class EventView(BaseView):
    """
    Class for creating and displaying Event views.
    """
    model = Event
    fields = ["id", "name", "Support", "date_start", "date_end", "location", "attendees"]

    @classmethod
    def create_update(cls, event=None):
        create = event is None
        action_label = "Creating" if create else "Updating"

        print(f"----------------------- {action_label} Event -----------------------")
        event = event or Event()

        name_prompt = " Name: " if create else f" Name ({event.name}): "
        date_start_prompt = f" Start date (yyyy-mm-dd HH:MM): " if create else f" Start date (yyyy-mm-dd HH:MM) ({event.date_start.strftime('%Y-%m-%d %H:%M')}): "
        date_end_prompt = f" End date (yyyy-mm-dd HH:MM): " if create else f" End date (yyyy-mm-dd HH:MM) ({event.date_end.strftime('%Y-%m-%d %H:%M')}): "
        location_prompt = f" Location: " if create else f" Location ({event.location}): "
        attendees_prompt = f" Attendees: " if create else f" Attendees ({event.attendees}): "
        notes_prompt = f" Notes: " if create else f" Notes ({event.notes}): "

        name = pyip.inputStr(prompt=name_prompt, default=event.name, blank=not create)
        date_start = pyip.inputDatetime(prompt=date_start_prompt, default=event.date_start, formats=['%Y-%m-%d %H:%M'], blank=not create)
        date_end = pyip.inputDatetime(prompt=date_end_prompt, default=event.date_end, formats=['%Y-%m-%d %H:%M'], blank=not create)
        location = pyip.inputStr(prompt=location_prompt, default=event.location, limit=50, blank=not create)
        attendees = pyip.inputInt(prompt=attendees_prompt, default=event.attendees, blank=not create)
        notes = pyip.inputStr(prompt=notes_prompt, default=event.notes, limit=255, blank=not create)

        event.name = name or event.name
        event.date_start = date_start or event.date_start
        event.date_end = date_end or event.date_end
        event.location = location or event.location
        event.attendees = attendees or event.attendees
        event.notes = notes or event.notes
        if create:
            event.contract = DBManager.activated_contract
        elif DBManager.activated_contract and DBManager.activated_contract.id != event.contract_id:
            if pyip.inputYesNo(f"Assign {DBManager.activated_contract} as a new contract? (Y/N): ", default="N"):
                event.contract = DBManager.activated_contract

        if DBManager.activated_support is not None:
            if pyip.inputYesNo(f"Assign {DBManager.activated_support} as Support? (Y/N): ", default="N"):
                    event.support = DBManager.activated_support
            elif not create and pyip.inputYesNo("Revoke Support? (Y/N): ", default="N"):
                event.support = None

        return event

    @classmethod
    def expand(cls, events, title_msg):
        tab = PrettyTable()
        tab.field_names = ["#", "Details"]
        tab.align["Details"] = "l"
        tab._max_width = {"Details": 150}

        for index, event in enumerate(events):
            formatted_string = (
                f"ID: {event.full_repr}\n"
                f"Status: {event.status}\n"
                f"Support: {event.support}\n"
                f"From: {event.date_start.strftime('%Y-%m-%d %H:%M') if event.date_start else '-------- --:--'} "
                f"To: {event.date_end.strftime('%Y-%m-%d %H:%M') if event.date_end else '-------- --:--'}\n"
                f"Location: {event.location}\n"
                f"Attendees: {event.attendees}\n"
                f"Notes: {event.notes}\n"
                f"---------------------------Contract-----------------------------\n"
                f"ID: {event.contract}\n"
                f"Date: {event.contract.contract_date.strftime('%Y-%m-%d')}\n"
                f"Customer: {event.contract.customer}\n"
                f"Commercial Contact: {event.contract.customer.contact}\n"
            )
            tab.add_row([index + 1, formatted_string])

        print(tab.get_string(title=title_msg))
