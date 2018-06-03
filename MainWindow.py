#!/usr/bin/python
# -*- encoding: utf-8 -*-
__author__ = "Daniel Steegmüller"

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import SideBar as Sb
import WindowSettings as Ws
import SpriteBuffer
import threading
import os


class MainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title=Ws.WindowSettings.title,
                            default_width=Ws.WindowSettings.width, default_height=Ws.WindowSettings.height)
        self.stage_grid = None
        self.canvas = None
        self.animation_frame = None
        self.sidebar = None
        self.animation_timer = None
        self.sprite_buffer = None
        self.quit = False
        self.create_window_layout()

    # Creates the animation frame
    def create_animation_frame(self):
        self.animation_frame = Gtk.Frame(label="Animation")
        self.stage_grid.attach(self.animation_frame, 0, 0, 5, 1)
        self.animation_frame.set_hexpand(True)
        self.animation_frame.set_vexpand(True)
        self.animation_frame.set_border_width(5)

        self.canvas = Gtk.Image()
        self.animation_frame.add(self.canvas)

    # Called when some value changed from any widget
    def on_changed(self):
        self.sprite_buffer.set_properties(self.sidebar.x_image_count,
                                          self.sidebar.y_image_count,
                                          self.sidebar.image_count)

    # Create the Window with animation frame and sidebar
    def create_window_layout(self):
        action_group = Gtk.ActionGroup("my_actions")

        self.add_file_menu_actions(action_group)
        uimanager = self.create_ui_manager()
        uimanager.insert_action_group(action_group)
        menubar = uimanager.get_widget("/MenuBar")
        window_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        window_box.pack_start(menubar, False, False, 0)

        self.stage_grid = Gtk.Grid()
        self.sidebar = Sb.SideBar(self.on_changed)
        self.create_animation_frame()
        window_box.add(self.stage_grid)

        menu_frame = Gtk.Frame(label="Settings")
        menu_frame.set_border_width(5)

        menu_frame.add(self.sidebar)
        self.stage_grid.attach_next_to(menu_frame, self.animation_frame, Gtk.PositionType.RIGHT, 1, 1)

        self.add(window_box)

    # Create the UI Manager
    def create_ui_manager(self):
        uimanager = Gtk.UIManager()
        uimanager.add_ui_from_string(Ws.WindowSettings.MENU_INFO)

        accelgroup = uimanager.get_accel_group()
        self.add_accel_group(accelgroup)
        return uimanager

    # Adds all Menu actions
    def add_file_menu_actions(self, action_group):
        action_filemenu = Gtk.Action("FileMenu", "File", None, None)
        action_group.add_action(action_filemenu)

        action_filenopen = Gtk.Action("FileOpen", None, None, Gtk.STOCK_OPEN)
        action_filenopen.connect("activate", self.on_menu_file_open)
        action_group.add_action(action_filenopen)

        action_filequit = Gtk.Action("FileQuit", None, None, Gtk.STOCK_QUIT)
        action_filequit.connect("activate", self.on_menu_file_quit)
        action_group.add_action(action_filequit)

    # Shows the OpenFileDialog
    def on_menu_file_open(self, widget):
        dialog = Gtk.FileChooserDialog("Open Image", self, Gtk.FileChooserAction.OPEN)
        path = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(path, "SpriteAnimations")
        if os.path.exists(path):
            dialog.set_current_folder(path)

        dialog.add_button(Gtk.STOCK_CANCEL, 0)
        dialog.add_button(Gtk.STOCK_OK, 1)
        dialog.set_default_response(1)

        filefilter = Gtk.FileFilter()
        filefilter.add_pixbuf_formats()
        dialog.set_filter(filefilter)

        if dialog.run() == 1 and dialog.get_filename() is not None:
            self.setup_sprite_animation(dialog.get_filename())

        dialog.destroy()

    def on_menu_file_quit(self, widget):
        self.quit = True

    # Sets up the sprite animation and canvas
    def setup_sprite_animation(self, file):
        self.sprite_buffer = SpriteBuffer.SpriteBuffer(file)
        self.on_changed()

        self.canvas.set_from_pixbuf(self.sprite_buffer.get_next_image())

        self.start_thread_timer()

    # Initialize Timer
    def start_thread_timer(self):
        if not self.quit:
            fps = (1.0 / self.sidebar.fps)
            self.animation_timer = threading.Timer(fps, self.start_thread_timer).start()
            self.canvas.set_from_pixbuf(self.sprite_buffer.get_next_image())
        else:
            Gtk.main_quit()
