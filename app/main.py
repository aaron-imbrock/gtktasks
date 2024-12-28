#!/usr/bin/env python3
import gi
import signal
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gdk

class TodoWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Tasks")
        self.set_border_width(10)
        self.set_default_size(300, 400)
        
        # Load CSS
        css_provider = Gtk.CssProvider()
        css = b"""
            entry { min-height: 30px; }
            button { 
                background: #4a90e2;
                color: white;
                min-height: 30px;
                border-radius: 4px;
            }
            listbox { background: white; }
            .task-row { 
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
        """
        css_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)
        
        # Entry with placeholder
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text("Enter a new task...")
        vbox.pack_start(self.entry, False, True, 0)
        
        # Add button
        button = Gtk.Button(label="Add Todo")
        button.connect("clicked", self.add_todo)
        vbox.pack_start(button, False, False, 0)
        
        # Scrolled window for listbox
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        vbox.pack_start(scrolled, True, True, 0)
        
        self.listbox = Gtk.ListBox()
        scrolled.add(self.listbox)
        
        self.connect("delete-event", Gtk.main_quit)

    def add_todo(self, widget):
        text = self.entry.get_text()
        if text:
            list_item = Gtk.ListBoxRow()
            list_item.get_style_context().add_class("task-row")
            label = Gtk.Label(label=text, xalign=0)
            list_item.add(label)
            self.listbox.add(list_item)
            self.listbox.show_all()
            self.entry.set_text("")

def signal_handler(signum, frame):
    Gtk.main_quit()

def start():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    GLib.unix_signal_add(GLib.PRIORITY_DEFAULT, signal.SIGINT, 
                        lambda: Gtk.main_quit() or True)
    
    window = TodoWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()

if __name__ == '__main__':
    start()
