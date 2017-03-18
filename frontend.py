#!/usr/bin/env python3

# Copyright 2017 Thomas Jeffery

# This file is part of Amoeba-gtk.

# Amoeba-gtk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Amoeba-gtk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Amoeba-gtk.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

import client

from config import Config
from editor_view import EditorView

class Window(Gtk.Window):
    def __init__(self, config):
        Gtk.Window.__init__(self, title="Amoeba-gtk")
        self.set_default_size(800, 600)
        self.connect("delete-event", Gtk.main_quit)
        self.set_events(Gdk.EventMask.KEY_PRESS_MASK)
        self.connect("key-press-event", self.on_key_press)

        self.editor = EditorView(text="Amoeba 0.0.1", config=config["editor"])
        self.add(self.editor)

        self.show_all()

        # Connect to backend
        self.client = client.Client("tcp://localhost:5555")
        self.client.request({"config": config})
        print("%s" % self.client.get_reply())

    def on_key_press(self, window, event):
        keycode = event.get_scancode()
        keyval = event.get_keyval().keyval
        #print('    "' + chr(Gdk.keyval_to_unicode(keyval)) + '": ', keycode)

        if keyval == Gdk.KEY_Escape:
            self.quit()
        elif keyval == Gdk.KEY_space:
            self.client.request({
                "buffer.insert": (" ", self.editor.config["cursor"]["position"])
            })
            self.editor.config["cursor"]["position"] += 1
            self.client.get_reply()

        # Show the buffer
        self.editor.set_text(self.get_buffer())

    def quit(self):
        try:
            self.client.request({"quit": True})
            print("Recieved reply: %s" % self.client.get_reply())
        except KeyboardInterrupt:
            print("Keyboard interrupt: Shutting down...")
        finally:
            Gtk.main_quit()

    def get_buffer(self):
        self.client.request({"buffer.print": True})
        return self.client.get_reply().decode("UTF-8")


if __name__ == "__main__":
    win = Window(Config("config.json"))
    Gtk.main()
