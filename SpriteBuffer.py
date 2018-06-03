#!/usr/bin/python
# -*- encoding: utf-8 -*-
__author__ = "Daniel Steegmüller"

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import GdkPixbuf


class SpriteBuffer(object):
    """
    This class handles the cropping of single frames out of sprite animations.
    Detailed documentation of the GdkPixbuf.Pixbuf class can be found here
            https://lazka.github.io/pgi-docs/GdkPixbuf-2.0/classes/Pixbuf.html#GdkPixbuf.Pixbuf
    """

    def __init__(self, file_name):
        self.__src_offset_x = 0
        self.__src_offset_y = 0
        self.__current_image_in_x = 0
        self.__current_image_in_y = 0

        self.file_name = file_name
        self.original_pixbuf = GdkPixbuf.Pixbuf.new_from_file(self.file_name)
        self.original_width = self.original_pixbuf.get_width()
        self.original_height = self.original_pixbuf.get_height()

        self.x_image_count = 1
        self.y_image_count = 1
        self.image_count = 1
        self.cropped_pixbuf = None
        self.rect_width = self.original_width / self.x_image_count
        self.rect_height = self.original_height / self.y_image_count
        self.current_image = 0

    def set_properties(self, x_count, y_count, image_count):
        """
        Sets the parameters for the rectangle to be copied
        :param x_count: The amount of images in x direction
        :param y_count: The amount of images in y direction
        :param image_count: The overall image count of the animation
        """
        self.x_image_count = x_count
        self.y_image_count = y_count
        self.image_count = image_count
        self.rect_width = self.original_width / self.x_image_count
        self.rect_height = self.original_height / self.y_image_count
        self.cropped_pixbuf = GdkPixbuf.Pixbuf.new(colorspace=self.original_pixbuf.get_colorspace(),
                                                   has_alpha=self.original_pixbuf.get_has_alpha(),
                                                   bits_per_sample=self.original_pixbuf.get_bits_per_sample(),
                                                   width=self.rect_width,
                                                   height=self.rect_height)

    def get_next_image(self):
        """
        copies a rectangle of pixels from the sprite sheet to the canvas
        :return: Returns a single frame of the spritesheet animation
        """
        if self.current_image >= self.image_count:
            self.current_image = 0
            self.__current_image_in_x = 0
            self.__current_image_in_y = 0

        self.__src_offset_x = self.__current_image_in_x * self.rect_width
        self.__src_offset_y = self.__current_image_in_y * self.rect_height

        if (self.__src_offset_x + self.rect_width) > self.original_width:
            self.__src_offset_x = 0
        if (self.__src_offset_y + self.rect_height) > self.original_height:
            self.__src_offset_y = 0

        self.original_pixbuf.copy_area(self.__src_offset_x, self.__src_offset_y,
                                       self.rect_width, self.rect_height,
                                       self.cropped_pixbuf, 0, 0)
        self.current_image += 1
        self.__current_image_in_x += 1

        if self.__current_image_in_x >= self.x_image_count:
            self.__current_image_in_x = 0
            self.__current_image_in_y += 1

        if self.__current_image_in_y >= self.y_image_count:
            self.__current_image_in_y = 0

        return self.cropped_pixbuf
