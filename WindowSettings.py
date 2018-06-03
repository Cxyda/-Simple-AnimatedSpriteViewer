#!/usr/bin/python
# -*- encoding: utf-8 -*-
__author__ = "Daniel Steegmüller"


class WindowSettings(object):
    """
    All settings for the Main Window are located here.
    """
    width = 600
    height = 400
    title = "GTK Oos Animated Sprite Viewer"

    # Menu Style
    MENU_INFO = """
    <ui>
      <menubar name='MenuBar'>
        <menu action='FileMenu'>
          <menuitem action='FileOpen'/>
          <separator />
          <menuitem action='FileQuit' />
        </menu>   
      </menubar>
    </ui>
    """
