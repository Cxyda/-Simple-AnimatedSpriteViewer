#!/usr/bin/python
# -*- encoding: utf-8 -*-
__author__ = "Daniel Steegmüller"

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class SideBar(Gtk.Grid):
    """
    The SideBar class creates all the widgets and handles the SideBar inputs
    """
    def __init__(self, callback):
        Gtk.Grid.__init__(self)

        self.fps = 12
        self.x_image_count = 6
        self.y_image_count = 1
        self.image_count = 6
        self.callback = callback

        x_adjustment = Gtk.Adjustment(self.x_image_count, 1, 100, 1, 10, 0)
        y_adjustment = Gtk.Adjustment(self.y_image_count, 1, 100, 1, 10, 0)
        fps_adjustment = Gtk.Adjustment(self.fps, 1, 48, 1, 10, 0)
        img_count_adjustment = Gtk.Adjustment(self.image_count, 1, 100, 1, 10, 0)

        # creating widgets
        img_count_lbl = Gtk.Label(" Image count : ")
        self.__img_count_widget = Gtk.SpinButton()
        self.__img_count_widget.set_adjustment(img_count_adjustment)
        image_cnt_tooltip = "The overall amount of images on the sprite sheet"
        img_count_lbl.set_tooltip_text(image_cnt_tooltip)
        self.__img_count_widget.set_tooltip_text(image_cnt_tooltip)

        x_count_lbl = Gtk.Label("Count X : ")
        self.__x_count_widget = Gtk.SpinButton()
        self.__x_count_widget.set_adjustment(x_adjustment)
        x_cnt_tooltip = "The amount of images on the sprite sheet in x-direction"
        x_count_lbl.set_tooltip_text(x_cnt_tooltip)
        self.__x_count_widget.set_tooltip_text(x_cnt_tooltip)

        y_count_lbl = Gtk.Label("Count Y : ")
        self.__y_count_widget = Gtk.SpinButton()
        self.__y_count_widget.set_adjustment(y_adjustment)
        y_cnt_tooltip = "The amount of images on the sprite sheet in y-direction"
        y_count_lbl.set_tooltip_text(y_cnt_tooltip)
        self.__y_count_widget.set_tooltip_text(y_cnt_tooltip)

        fps_count_lbl = Gtk.Label(" FPS : ")
        self.__fps_widget = Gtk.SpinButton()
        self.__fps_widget.set_adjustment(fps_adjustment)
        fps_tooltip = "The FramesPerSecond to be played"
        fps_count_lbl.set_tooltip_text(fps_tooltip)
        self.__fps_widget.set_tooltip_text(fps_tooltip)

        # attaching widgets
        self.attach(img_count_lbl, 0, 2, 2, 1)
        self.attach_next_to(self.__img_count_widget, img_count_lbl, Gtk.PositionType.RIGHT, 1, 1)

        self.attach_next_to(x_count_lbl, img_count_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.__x_count_widget, self.__img_count_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(y_count_lbl, x_count_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.__y_count_widget, self.__x_count_widget, Gtk.PositionType.BOTTOM, 1, 1)

        self.attach_next_to(fps_count_lbl, y_count_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.attach_next_to(self.__fps_widget, self.__y_count_widget, Gtk.PositionType.BOTTOM, 1, 1)

        # set default parameters
        x_adjustment.set_value(self.x_image_count)
        y_adjustment.set_value(self.y_image_count)
        fps_adjustment.set_value(self.fps)
        img_count_adjustment.set_value(self.image_count)

        # Connect all widgets
        self.__x_count_widget.connect("value-changed", self.__on_value_changed__)
        self.__y_count_widget.connect("value-changed", self.__on_value_changed__)
        self.__fps_widget.connect("value-changed", self.__on_value_changed__)
        self.__img_count_widget.connect("value-changed", self.__on_value_changed__)

    def __on_value_changed__(self, widget):
        self.fps = self.__fps_widget.get_value()
        self.x_image_count = self.__x_count_widget.get_value()
        self.y_image_count = self.__y_count_widget.get_value()
        self.image_count = self.__img_count_widget.get_value()
        self.callback()
