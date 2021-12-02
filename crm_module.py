#!/usr/bin/env python3

from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication
import sys
import sqlite3



class CRMView(Frame):
    def __init__(self, screen): # model
        super(CRMView, self).__init__(screen,
                                          screen.height * 2 // 3,
                                          screen.width * 2 // 3,
                                          hover_focus=True,
                                          can_scroll=False,
                                          title="Contact Details",
                                          reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        # self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([1, 1, 1, 1])
        self.add_layout(layout)
        layout.add_widget(Button("Add user", self._add), 0)
        layout.add_widget(Button("List Customers", self._listall), 1)
        layout.add_widget(Button("Edit Customer", self._edit ), 2)
        layout.add_widget(Button("Delete Customer", self._delete), 3)
        self.fix()

    def _add(self):
        return None

    def _listall(self):
        return None


    def _edit(self):
        return None

    def _delete(self):
        return None






# contacts = ContactModel()

def demo(screen, scene):
    scenes = [
        # Scene([ListView(screen, contacts)], -1, name="Main"),
        Scene([CRMView(screen)], -1, name="CRM Module") #contacts
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)

last_scene = None

while True:
    try:
        Screen.wrapper(demo, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene




