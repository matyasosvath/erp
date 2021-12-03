#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, Label
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys

from models import ContactModel, CustomerModel, Customer
import uuid


class ERPView(Frame):
    def __init__(self, screen):
        super(ERPView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="ERP Software",
                                          reduce_cpu=True)


        # Create the form for displaying the list of contacts.
        layout = Layout([100])
        self.add_layout(layout)
        layout.add_widget(Label("\n Welcome to the ERP Software \
                                \n Please choose one of the following module.",
                                height=5,
                                align="^"))
        layout.add_widget(Divider(height=1))

        layout1 = Layout([1,1,1])
        self.add_layout(layout1)
        layout1.add_widget(Button("CRM Module", self._go_to_crm), 0)
        layout1.add_widget(Button("HR Module", self._go_to_hr), 1)
        layout1.add_widget(Button("Sales Module", self._go_to_sales), 2)
        layout1.add_widget(Divider(height=1))


        layout4 = Layout([1])
        self.add_layout(layout4)
        layout4.add_widget(Button("Quit", self._quit), 0)

        self.fix()

    def _go_to_crm(self):
        raise NextScene("CRM Module")

    def _go_to_hr(self):
        raise NextScene("HR Module")

    def _go_to_sales(self):
        raise NextScene("Sales Module")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


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
        self.save()
        raise NextScene("Customer ID")

    def _delete(self):
        self.save()
        raise NextScene("Customer ID")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class AskCustomerIdView(Frame):
    def __init__(self,screen,model):
        super(AskCustomerIdView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Customer ID",
                                          reduce_cpu=True)

        # Save off the model that accesses the contacts database.
        self._model = model

        # self.__unique_id = uuid.uuid1()
        # self.__unique_id = generate_random_id(1,100)

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)

        layout.add_widget(Text("ID:", "id"))

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Edit", self._ok), 0)
        layout2.add_widget(Button("Delete", self._delete), 1)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(AskCustomerIdView, self).reset()
        if self._model.current_id is None:
            self._model.current_id = self.data

#TODO keresd meg az ID, ha nincs pop up hogy nincs

    def _ok(self):
        self.save()
        raise NextScene("Customer Details")

    def _delete(self):
        self.save()
        self._model.delete(self.data["id"])
        raise NextScene("CRM Module")

    @staticmethod
    def _cancel():
        raise NextScene("CRM Module")


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

        # self.__unique_id = uuid.uuid1()
        # self.__unique_id = generate_random_id(1,100)

        # Create the form for displaying the list of contacts.
        layout = Layout([50], fill_frame=True)
        self.add_layout(layout)

        # layout.add_widget(Label(label=f"Unique ID:", name="id"))
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
        if self._model.current_id is None:
            self._customer = Customer()
            self.data = {
                "name": self._customer.name,
                "email": self._customer.email,
                "status": self._customer.status}
        else:
            #TODO hibás
            self.data = self._model.customers[self._model.current_id]

    def _ok(self):
        self.save()
        if self._model.current_id is None:
            self._model.customers.append(Customer(**self.data))
            # self._model.customers.append(self.data)
        else:
            self._model.contacts[self._model.current_id] = self.data
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
            options= [(f"Name: {x.name}, ID: {x.id}, E-mail: {x.email} ", i) for i,x in enumerate(self._model.customers)],
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
        self._list_view.options =  [(f"Name: {x.name}, ID: {x.id}, E-mail: {x.email} ", i) for i,x in enumerate(self._model.customers)]
        self._list_view.value = new_value

    def _go_back(self):
        raise NextScene("CRM Module")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")




customers = CustomerModel()

def demo(screen, scene):
    scenes = [
        Scene([ERPView(screen)], -1, name="ERP Software"),
        Scene([CRMView(screen, customers)], -1, name="CRM Module"),
        Scene([CustomerView(screen, customers)], -1, name="Customer Details"),
        Scene([ListView(screen, customers)], -1, name="Customer List"),
        Scene([AskCustomerIdView(screen, customers)], -1, name="Customer ID")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

last_scene = None

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene




