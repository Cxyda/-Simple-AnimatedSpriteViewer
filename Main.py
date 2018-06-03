#!/usr/bin/python
# -*- encoding: utf-8 -*-
__author__ = "Daniel Steegmüller"

import MainWindow
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

if __name__ == '__main__':
    win = MainWindow.MainWindow()
    win.connect('delete-event', Gtk.main_quit)
    win.show_all()
    Gtk.main()
