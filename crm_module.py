#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, Label
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import random

from models import ContactModel
import uuid




class CRMView(Frame):
    def __init__(self, screen, model):
        super(CRMView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="CRM Module",
                                          reduce_cpu=True)

        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Label("\n Welcome to the CRM module! \n Please choose one of the following.",
                                height=5,
                                align="^"))
        layout.add_widget(Divider(height=1))

        layout1 = Layout([1,1], fill_frame=True)
        self.add_layout(layout1)
        layout1.add_widget(Button("Add user", self._add), 0)
        layout1.add_widget(Divider())

        layout1.add_widget(Button("List Customers", self._listall), 1)

        layout3 = Layout([1])
        self.add_layout(layout3)
        layout3.add_widget(Button("Edit Customer", self._edit ), 0)

        layout4 = Layout([1])
        self.add_layout(layout4)
        layout4.add_widget(Button("Delete Customer", self._delete), 0)

        layout4.add_widget(Divider(height=1))

        layout5 = Layout([1])
        self.add_layout(layout5)
        layout5.add_widget(Button("Quit", self._quit), 0)


        self.fix()

    def _add(self):
        self._model.current_id = None
        raise NextScene("Customer Details")

    def _listall(self):
        raise NextScene("Customer List")


    def _edit(self):
        return None

    def _delete(self):
        return None

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class CustomerView(Frame):
    def __init__(self, screen, model):
        super(CustomerView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Customer Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        self.__unique_id = uuid.uuid1()

        # Create the form for displaying the list of contacts.
        layout = Layout([50], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(Label(label=f"Unique ID: {self.__unique_id}", name="id"))
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Subscription Status:", "status"))
        layout.add_widget(Text("Email address:", "email"))

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Save", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(CustomerView, self).reset()
        self.data = self._model.get_current_contact()

    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("CRM Module")

    @staticmethod
    def _cancel():
        raise NextScene("CRM Module")





class ListView(Frame):
    def __init__(self, screen, model):
        super(ListView, self).__init__(screen,
                                       screen.height * 2 // 3,
                                       screen.width * 2 // 3,
                                       on_load=self._reload_list,
                                       hover_focus=True,
                                       can_scroll=False,
                                       title="Customer List")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            options=model.get_summary(),
            name="customers",
            add_scroll_bar=True)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Go back", self._go_back), 0)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()

    def _reload_list(self, new_value=None):
        self._list_view.options = self._model.get_summary()
        self._list_view.value = new_value

    def _go_back(self):
        raise NextScene("CRM Module")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")




customers = ContactModel()

def demo(screen, scene):
    scenes = [
        Scene([CRMView(screen, customers)], -1, name="CRM Module"),
        Scene([CustomerView(screen, customers)], -1, name="Customer Details"),
        Scene([ListView(screen, customers)], -1, name="Customer List")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

last_scene = None

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene



