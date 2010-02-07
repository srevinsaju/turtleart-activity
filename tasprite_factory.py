#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Copyright (c) 2009,10 Walter Bender

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

import pygtk
pygtk.require('2.0')
import gtk
import os
from gettext import gettext as _

class SVG:
    def __init__(self):
        self._x = 0
        self._y = 0
        self._min_x = 0
        self._min_y = 0
        self._max_x = 0
        self._max_y = 0
        self._width = 0
        self._height = 0
        self.docks = []
        self._scale = 1
        self._orientation = 0
        self._radius = 8
        self._stroke_width = 1
        self._innie = [False]
        self._outie = False
        self._innie_x1 = (9-self._stroke_width)/2
        self._innie_y1 = 3
        self._innie_x2 = (9-self._stroke_width)/2
        self._innie_y2 = (9-self._stroke_width)/2
        self._innie_spacer = 9
        self._slot = True
        self._cap = False
        self._tab = True
        self._bool = False
        self._slot_x = 10
        self._slot_y = 2
        self._porch = False
        self._porch_x = self._innie_x1+self._innie_x2+4*self._stroke_width
        self._porch_y = self._innie_y1+self._innie_y2+4*self._stroke_width
        self._expand_x = 0
        self._expand_y = 0
        self._else = False
        self._draw_innies = True
        self._hide = False
        self._show = False
        self._dot_radius = 8
        self._fill = "#00FF00"
        self._stroke = "#00A000"
        self._gradiant = False
        self.margins = [0, 0, 0, 0]

    def basic_block(self):
        (x, y) = self._calculate_x_y()
        self.margins[0] = int(x+2*self._stroke_width+0.5)
        self.margins[1] = int(y+self._stroke_width+0.5+self._slot_y)
        self.margins[2] = 0
        self.margins[3] = int(self._stroke_width+0.5+self._slot_y*2)
        svg = self._new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1)
        for i in range(len(self._innie)):
            if self._innie[i] is True:
                svg += self._do_innie()
            if i==0 and self._porch is True:
                svg += self._do_porch()
            elif len(self._innie)-1 > i:
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        svg += self._rline_to(0, self._expand_y)
        svg += self._corner(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        if self._tab:
            svg += self._do_tab()
        else:
            svg += self._do_tail()
        svg += self._corner(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self._line_to(x, self._radius+self._innie_y2+\
                                    self._stroke_width/2.0)
            svg += self._do_outie()
        self._calculate_w_h()
        svg += self._close_path()
        svg += self._style()
        if self._show is True:
            if self._outie is True:
                x = self._innie_x1 + 2*self._innie_x2 + 2*self._dot_radius
            else:
                x = 12
            svg += self._show_dot(x,self._height-12-self._innie_y2-self._slot_y)
        if self._hide is True:
            if True in self._innie:
                x = self._width - (self._innie_x1 + 2*self._innie_x2 +\
                                   2*self._dot_radius)
            else:
                x = self._width-12
            svg += self._hide_dot(x,self._height-12-self._innie_y2-self._slot_y)

        svg += self._footer()
        return self._header() + svg

    def basic_flow(self):
        (x, y) = self._calculate_x_y()
        svg = self._new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        svg += self._rline_to(self._expand_x, 0)
        xx = self._x
        svg += self._corner(1, 1)
        for i in range(len(self._innie)):
            if self._innie[i] is True:
                svg += self._do_innie()
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        if self._bool is True:
            svg += self._rline_to(0,self._radius/2.0)
            svg += self._do_boolean()
            svg += self._rline_to(0,self._radius/2.0)
        if self._else:
            svg += self._rline_to(self._radius*3+self._slot_x*2, 0)
        else:
            svg += self._rline_to(self._radius+self._slot_x, 0)
        hh = self._x
        svg += self._corner(1, 1)
        svg += self._rline_to(-self._radius,0)
        if self._else:
            svg += self._do_tab()
            svg += self._rline_to(-self._radius*2, 0)
        svg += self._do_tab()
        svg += self._rline_to(-self._radius, 0)
        svg += self._rline_to(0, self._expand_y)
        svg += self._corner(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        if self._tab:
            svg += self._do_tab()
        else:
            svg += self._do_tail()
        svg += self._corner(-1, -1)
        svg += self._rline_to(0, -self._expand_y)
        if True in self._innie:
            svg += self._line_to(x, self._radius+self._innie_y2+\
                                    self._stroke_width)
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        if self._hide is True:
            svg += self._hide_dot(hh,
                                  self._height-12-self._innie_y2-self._slot_y)
        if self._show is True:
            svg += self._show_dot(hh-24,
                                  self._height-12-self._innie_y2-self._slot_y)
        svg += self._footer()
        return self._header() + svg

    def portfolio(self):
        (x, y) = self._calculate_x_y()
        x += self._innie_x1+self._innie_x2
        svg = self._new_path(x, y)
        svg += self._corner(1, -1)
        svg += self._do_slot()
        xx = self._x
        svg += self._rline_to(self._expand_x, 0)
        svg += self._corner(1, 1)
        svg += self._rline_to(0, self._expand_y)
        for i in range(len(self._innie)):
            if self._innie[i] is True and i > 0 and self._draw_innies:
                svg += self._do_innie()
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
            else:
                svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        svg += self._corner(-1, 1)
        svg += self._line_to(xx, self._y)
        svg += self._do_tab()
        svg += self._corner(-1, -1)
        for i in range(len(self._innie)):
            if self._innie[len(self._innie)-i-1] is True:
                svg += self._rline_to(0, -2*self._innie_y2-self._innie_spacer)
                svg += self._do_reverse_innie()
            else:
                svg += self._rline_to(0, -2*self._innie_y2-self._innie_spacer)
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        svg += self._footer()
        return self._header() + svg

    def basic_box(self):
        self.set_outie(True)
        x = self._stroke_width/2.0+self._innie_x1+self._innie_x2
        svg = self._new_path(x, self._stroke_width/2.0)
        svg += self._rline_to(self._expand_x, 0)
        svg += self._rline_to(0, 2*self._radius+self._innie_y2+self._expand_y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._line_to(x, self._radius+self._innie_y2+\
                                self._stroke_width/2.0)
        svg += self._do_outie()
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        svg += self._footer()
        return self._header() + svg

    def boolean_and_or(self):
        svg = self._start_boolean(self._stroke_width/2.0,
                                  self._radius*5.5+self._stroke_width/2.0+\
                                  self._innie_y2+self._innie_spacer)
        svg += self._rline_to(0,-self._radius*3.5-self._innie_y2-\
                             self._innie_spacer-self._stroke_width)
        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius/2.0+self._expand_x, 0)
        xx = self._x
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius*1.5+self._innie_y2+\
                                self._innie_spacer)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean()
        return self._header() + svg

    def boolean_not(self):
        svg = self._start_boolean(self._stroke_width/2.0,
                                  self._radius*2.0+self._stroke_width/2.0)
        svg += self._rline_to(0,-self._stroke_width)
        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius/2.0+self._expand_x, 0)
        xx = self._x
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._do_boolean()
        svg += self._rline_to(0,self._radius/2.0)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean()
        return self._header() + svg

    def boolean_compare(self):
        yoffset = self._radius*2+2*self._innie_y2+\
                  self._innie_spacer+self._stroke_width/2.0
        if self._porch is True:
            yoffset += self._porch_y
        svg = self._start_boolean(self._stroke_width/2.0, yoffset)
        yoffset = -2*self._innie_y2-self._innie_spacer-self._stroke_width
        if self._porch is True:
            yoffset -= self._porch_y
        svg += self._rline_to(0, yoffset)
        svg += self._rarc_to(1, -1)
        svg += self._rline_to(self._radius/2.0+self._expand_x, 0)
        svg += self._rline_to(0,self._radius)
        xx = self._x
        svg += self._do_innie()
        if self._porch is True:
           svg += self._do_porch()
        else:
           svg += self._rline_to(0, 2*self._innie_y2+self._innie_spacer)
        svg += self._do_innie()
        svg += self._rline_to(0, self._radius)
        svg += self._line_to(xx, self._y)
        svg += self._rline_to(-self._expand_x, 0)
        svg += self._end_boolean()
        return self._header() + svg

    def turtle(self, colors):
        self._fill, self._stroke = colors[2], "none"
        svg = self._rect(21, 21, 19.5, 18)
        self._fill = colors[3]
        svg += self._rect(3, 3, 30, 24)
        svg += self._rect(3, 3, 24, 24)
        svg += self._rect(3, 3, 30, 30)
        svg += self._rect(3, 3, 24, 30)
        svg += self._rect(3, 3, 27, 27)
        svg += self._rect(3, 3, 21, 27)
        svg += self._rect(3, 3, 33, 27)
        svg += self._rect(3, 3, 27, 21)
        svg += self._rect(3, 3, 21, 21)
        svg += self._rect(3, 3, 33, 21)
        svg += self._rect(3, 3, 27, 33)
        svg += self._rect(3, 3, 21, 33)
        svg += self._rect(3, 3, 33, 33)
        svg += self._rect(3, 3, 30, 36)
        svg += self._rect(3, 3, 24, 36)
        svg += self._rect(3, 3, 30, 18)
        svg += self._rect(3, 3, 24, 18)
        svg += self._rect(3, 3, 36, 24)
        svg += self._rect(3, 3, 36, 30)
        svg += self._rect(3, 3, 36, 18)
        svg += self._rect(3, 3, 36, 36)
        self._fill, self._stroke = colors[0], colors[0]
        svg += self._turtle_body()
        self._fill, self._stroke = colors[1], colors[1]
        svg += self._turtle_shell()
        self._fill, self._stroke = "#000000", "#000000"
        svg += self._circle(1.25,32.5,8)
        svg += self._circle(1.25,27.5,8)
        svg += self._footer()
        self._width, self._height = 60, 60
        return self._header() + svg

    def palette(self, width, height):
        self._width, self._height = width, height
        self._fill, self._stroke = "#FFD000", "none"
        svg = self._rect(width, height, 0, 0)
        svg += self._hide_dot(width-12, height-12)
        svg += self._footer()
        return self._header() + svg

    def toolbar(self, width, height):
        self._width, self._height = width, height
        self._fill, self._stroke = "#282828", "none"
        svg = self._rect(width, height, 0, 0)
        svg += self._footer()
        return self._header() + svg

    #
    # Utility methods
    #
    def set_draw_innies(self, flag=True):
        self._draw_innies = flag

    def set_hide(self, flag=False):
        self._hide = flag

    def set_show(self, flag=False):
        self._show = flag

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def get_innie_width(self):
        return (self._innie_x1+self._innie_x2)*self._scale

    def get_slot_depth(self):
        return self._slot_y*self._scale

    def clear_docks(self):
        self.docks = []

    def set_scale(self, scale=1):
        self._scale = scale

    def set_orientation(self, orientation=0):
        self._orientation = orientation

    def expand(self, w=0, h=0):
        self._expand_x = w
        self._expand_y = h

    def set_stroke_width(self, stroke_width=1.5):
        self._stroke_width = stroke_width
        self._calc_porch_params()

    def set_colors(self, colors=["#00FF00","#00A000"]):
        self._fill = colors[0]
        self._stroke = colors[1]

    def set_fill_color(self, color="#00FF00"):
        self._fill = color

    def set_stroke_color(self, color="#00A000"):
        self._stroke = color

    def set_gradiant(self, flag=False):
        self._gradiant = flag

    def set_innie(self, innie_array=[False]):
        self._innie = innie_array

    def set_outie(self, flag=False):
        self._outie = flag

    def set_slot(self, flag=True):
        self._slot = flag
        if self._slot is True:
            self._cap = False

    def set_cap(self, flag=False):
        self._cap = flag
        if self._cap is True:
            self._slot = False

    def set_tab(self, flag=True):
        self._tab = flag

    def set_porch(self, flag=False):
        self._porch = flag

    def set_boolean(self, flag=False):
        self._bool = flag

    def set_else(self, flag=False):
        self._else = flag

    #
    # Exotic methods
    #

    def set_radius(self, radius=8):
        self._radius = radius

    def set_innie_params(self, x1=4, y1=3, x2=4, y2=4):
        self._innie_x1 = x1
        self._innie_y1 = y1
        self._innie_x2 = x2
        self._innie_y2 = y2
        self._calc_porch_params()

    def set_innie_spacer(self, innie_spacer = 0):
        self._innie_spacer = innie_spacer

    def set_slot_params(self, x=12, y=4):
        self._slot_x = x
        self._slot_y = y

    def _calc_porch_params(self):
        self._porch_x = self._innie_x1+self._innie_x2+4*self._stroke_width
        self._porch_y = self._innie_y1+self._innie_y2+4*self._stroke_width

    #
    # SVG helper methods
    #

    def _header(self):
        return "%s%s%s%s%s%s%s%s%.1f%s%s%.1f%s%s%s" % (
            "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"no\"?>\n",
            "<!-- Created with Python -->\n",
            "<svg\n",
            "   xmlns:svg=\"http://www.w3.org/2000/svg\"\n",
            "   xmlns=\"http://www.w3.org/2000/svg\"\n",
            "   xmlns:xlink=\"http://www.w3.org/1999/xlink\"\n",
            "   version=\"1.1\"\n",
            "   width=\"", self._width, "\"\n",
            "   height=\"", self._height, "\">\n",
            self._defs(),
            self._transform())

    def _defs(self):
        if self._gradiant is True:
            return "%s%s%s%s%s%s%s%s%s%s%s%s%.1f%s%s%.1f%s%s%.1f%s%s" % (
        "  <defs>\n    <linearGradient\n       id=\"linearGradient1234\">\n",
        "      <stop\n         style=\"stop-color:#ffffff;stop-opacity:1;\"\n",
        "         offset=\"0\" />\n",
        "      <stop\n         style=\"stop-color:", self._fill,
        ";stop-opacity:1;\"\n",
        "         offset=\"1\" />\n",
        "    </linearGradient>\n",
        "    <linearGradient\n       xlink:href=\"#linearGradient1234\"\n",
        "       id=\"linearGradient5678\"\n",
        "       x1=\"0\"\n",
        "       y1=\"", self._height/2.0, "\"\n",
        "       x2=\"", self._width, "\"\n",
        "       y2=\"", self._height/2.0, "\"\n",
        "       gradientUnits=\"userSpaceOnUse\" />\n  </defs>\n")
        else:
            return ""

    def _transform(self):
        if self._orientation != 0:
            orientation = "<g\ntransform = \"rotate(%.1f %.1f %.1f)\">\n" % (
                self._orientation, self._width/2.0, self._height/2.0)
        else:
            orientation = ""
        return "<g\ntransform=\"scale(%.1f, %.1f)\">\n%s" % (
                self._scale, self._scale, orientation )

    def _footer(self):
        if self._orientation != 0:
            return "   </g>\n</g>\n</svg>\n"
        else:
            return "   </g>\n</svg>\n"

    def _style(self):
        if self._gradiant is True:
            fill = "url(#linearGradient5678)"
        else:
            fill = self._fill
        return "%s%s;%s%s;%s%.1f;%s%s" % (
               "       style=\"fill:",fill,
               "fill-opacity:1;stroke:",self._stroke,
               "stroke-width:",self._stroke_width,
               "stroke-linecap:square;",
               "stroke-opacity:1;\" />\n")

    def _circle(self, r, cx, cy):
        return "%s%s%s%s%s%f%s%f%s%f%s" % ("<circle style=\"fill:",
             self._fill, ";stroke:", self._stroke, ";\" r=\"", r, "\" cx=\"",
             cx, "\" cy=\"", cy, "\" />\n")

    def _rect(self, w, h, x, y):
        return "%s%s%s%s%s%f%s%f%s%f%s%f%s" % ("<rect style=\"fill:",
               self._fill, ";stroke:", self._stroke, ";\" width=\"", w,
               "\" height=\"", h,"\" x=\"", x, "\" y=\"", y, "\" />\n")

    def _turtle_body(self):
        return "%s%s%s%s%s" % ("<path style=\"", self._fill, ";stroke:",
               self._stroke, "\" d=\"M 20,42 C 21,41 23,40 24,40 C 24,39 24,40 26,41 C 28,43 31,43 34,41 C 35,40 35,39 36,40 C 36,40 38,41 39,42 C 41,42 45,43 46,43 C 47,43 46,41 43,39 L 39,36 L 42,34 C 44,30 45,28 43,25 L 41,22 L 46,18 C 48,16 47.5,13.5 47,13 C 46.5,12.5 46,13 45,13 C 44,13 43.5,14 42.5,15 C 39.5,17 40,18 37,17 C 32,16 31.5,15 34.5,12 C 36.5,10 36,7 34,6 C 32,3 28,4 26,6 C 24,8 23,10 25,12 C 28,15 27,16 22,17 C 18,18 19,17 17,15 C 16,14 16,13 15,13 C 14,13 13,13 13,13 C 12,13 11,16 14,18 L 19,22 L 17,25 C 15,28 16,30 18,34 L 20,36 L 16,39 C 13,41 12,43 13,43 C 14,43 18,42 20,42 z M 30,18 C 32,18 36,19 38,20 C 40,22 39.5,25 39.5,28 C 39.5,30 40,32.5 38.5,35 C 37,36.5 36.5,37.5 35,38 C 33.5,38.5 31,39 30,39 C 28,39 26,39 25,38 C 23,37 22.5,37 21.5,35 C 20.5,33 20.5,30 20.5,28 C 20.5,25 20,22 22,20 C 24,19 27,18 30,18 z\" />\n")

    def _turtle_shell(self):
        return "%s%s%s%s%s" % ("<path style=\"", self._fill, ";stroke:",
               self._stroke, "\" d=\"M 33,10 C 33,11 31.5,12 30,12 C 28,12 27,11 27,10 C 27,9 28,8 30,8 C 31.5,8 33,9 33,10 z\" />\n")

    def _check_min_max(self):
        if self._x < self._min_x:
            self._min_x = self._x
        if self._y < self._min_y:
            self._min_y = self._y
        if self._x > self._max_x:
            self._max_x = self._x
        if self._y > self._max_y:
            self._max_y = self._y

    def _line_to(self, x, y):
        if self._x == x and self._y == y:
            return ""
        else:
            self._x = x
            self._y = y
            self._check_min_max()
            return "L %.1f %.1f " % (x, y) 

    def _rline_to(self, dx, dy):
        if dx == 0 and dy == 0:
            return ""
        else:
            return self._line_to(self._x+dx, self._y+dy)

    def _arc_to(self, x, y, r, a=90, l=0, s=1):
        if r == 0:
            return self._line_to(x, y)
        else:
            self._x = x
            self._y = y
            self._check_min_max()
            return "A %.1f %.1f %.1f %d %d %.1f %.1f " % (
                r, r, a, l, s, x, y)

    def _rarc_to(self, sign_x, sign_y, a=90, l=0, s=1):
        if self._radius == 0:
            return ""
        else:
            x = self._x + sign_x*self._radius
            y = self._y + sign_y*self._radius
            return self._arc_to(x, y, self._radius, a, l, s)

    def _corner(self, sign_x, sign_y, a=90, l=0, s=1):
        svg_str = ""
        if self._radius > 0:
            r2 = self._radius/2.0
            if sign_x*sign_y == 1:
                svg_str +=self._rline_to(sign_x*r2, 0)
            else:
                svg_str +=self._rline_to(0, sign_y*r2)
            x = self._x + sign_x*r2
            y = self._y + sign_y*r2
            svg_str += self._arc_to(x, y, r2, a, l, s)
            if sign_x*sign_y == 1:
                svg_str +=self._rline_to(0, sign_y*r2)
            else:
                svg_str +=self._rline_to(sign_x*r2, 0)
        return svg_str

    def _new_path(self, x, y):
        self._min_x = x
        self._min_y = y
        self._max_x = x
        self._max_y = y
        self._x = x
        self._y = y
        return "      <path d=\"m%.1f %.1f " % (x, y)

    def _close_path(self):
        return "z\"\n"

    def _hide_dot(self, x, y):
        _saved_fill, _saved_stroke = self._fill, self._stroke
        self._fill, self._stroke = "#FF0000", "#FF0000"
        svg = "</g>/n<g>/n"
        svg += self._circle(self._dot_radius, x, y)
        self._fill, self._stroke = "#FFFFFF", "#FFFFFF"
        svg += self._rect(10, 2, x-5, y-1)
        self._fill, self._stroke = _saved_fill, _saved_stroke
        return svg

    def _show_dot(self, x, y):
        _saved_fill, _saved_stroke = self._fill, self._stroke
        self._fill, self._stroke = "#00FE00", "#00FE00"
        svg = "</g>/n<g>/n"
        svg += self._circle(self._dot_radius, x, y)
        self._fill, self._stroke = "#FEFEFE", "#FEFEFE"
        svg += self._rect(10, 2, x-5, y-1)
        svg += self._rect(2, 10, x-1, y-5)
        self._fill, self._stroke = _saved_fill, _saved_stroke
        return svg

    def _do_slot(self):
        if self._slot is True:
            self.docks.append((int(self._x*self._scale),
                               int(self._y*self._scale)))
            return "%s%s%s" % (
                self._rline_to(0, self._slot_y),
                self._rline_to(self._slot_x, 0),
                self._rline_to(0, -self._slot_y))
        elif self._cap is True:
            return "%s%s" % (
                self._rline_to(self._slot_x/2.0, -self._slot_y*2.0),
                self._rline_to(self._slot_x/2.0, self._slot_y*2.0))
        else:
            return self._rline_to(self._slot_x, 0)

    def _do_tail(self):
        if self._outie is True:
            return self._rline_to(-self._slot_x, 0)
        else:
            return "%s%s" % (
                self._rline_to(-self._slot_x/2.0, self._slot_y*2.0),
                self._rline_to(-self._slot_x/2.0, -self._slot_y*2.0))

    def _do_tab(self):
        s = "%s%s%s%s%s" % (
            self._rline_to(-self._stroke_width, 0),
            self._rline_to(0, self._slot_y),
            self._rline_to(-self._slot_x+2*self._stroke_width, 0),
            self._rline_to(0, -self._slot_y),
            self._rline_to(-self._stroke_width, 0))
        self.docks.append((int(self._x*self._scale),
                           int((self._y+self._stroke_width)*self._scale)))
        return s

    def _do_innie(self):
        self.docks.append((int((self._x+self._stroke_width)*self._scale),
                           int((self._y+self._innie_y2)*self._scale)))
        if self.margins[2] == 0:
            self.margins[1] = int((self._y+self._innie_y2)*self._scale)
            self.margins[2] = int((self._x-self._innie_x1-self._innie_x2-\
                                  self._stroke_width*2)*self._scale)
        self.margins[3] = int((self._y+self._innie_y2)*self._scale)
        # print "x: %d (%d, %d)" % (self._x, self._innie_x1, self._innie_x2)
        return "%s%s%s%s%s%s%s" % (
            self._rline_to(-self._innie_x1, 0),
            self._rline_to(0, -self._innie_y1),
            self._rline_to(-self._innie_x2, 0),
            self._rline_to(0, self._innie_y2+2*self._innie_y1),
            self._rline_to(self._innie_x2, 0),
            self._rline_to(0, -self._innie_y1),          
            self._rline_to(self._innie_x1, 0))

    def _do_reverse_innie(self):
        self.docks.append((int((self._x+self._stroke_width)*self._scale),
                           int((self._y)*self._scale)))
        return "%s%s%s%s%s%s%s" % (
            self._rline_to(-self._innie_x1, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(-self._innie_x2, 0),
            self._rline_to(0, -self._innie_y2-2*self._innie_y1),
            self._rline_to(self._innie_x2, 0),
            self._rline_to(0, self._innie_y1),          
            self._rline_to(self._innie_x1, 0))

    def _do_outie(self):
        if self._outie is not True:
            return self._rline_to(0, -self._innie_y2)
        self.docks.append((int(self._x*self._scale), int(self._y*self._scale)))
        return "%s%s%s%s%s%s%s%s%s" % (
            self._rline_to(0, -self._stroke_width),
            self._rline_to(-self._innie_x1-2*self._stroke_width, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(-self._innie_x2+2*self._stroke_width, 0),
            self._rline_to(0,
                -self._innie_y2-2*self._innie_y1+2*self._stroke_width),
            self._rline_to(self._innie_x2-2*self._stroke_width, 0),
            self._rline_to(0, self._innie_y1),
            self._rline_to(self._innie_x1+2*self._stroke_width, 0),
            self._rline_to(0, -self._stroke_width))

    def _do_porch(self):
         return "%s%s%s" % (
            self._rline_to(0, self._porch_y),
            self._rline_to(self._porch_x-self._radius, 0),
            self._corner(1, 1))

    def _start_boolean(self, xoffset, yoffset):
        svg = self._new_path(xoffset, yoffset)
        self._radius -= self._stroke_width
        self.docks.append((int(self._x*self._scale), int(self._y*self._scale)))
        svg += self._rarc_to(1, -1)
        self._radius += self._stroke_width
        return svg + self._rline_to(self._stroke_width, 0)

    def _do_boolean(self):
        self.docks.append(
            (int((self._x-self._radius+self._stroke_width)*self._scale),
                           int((self._y+self._radius)*self._scale)))
        return self._rarc_to(-1, 1, 90, 0, 0) + self._rarc_to(1, 1, 90, 0, 0)

    def _end_boolean(self):
        svg = self._rline_to(-self._radius*1.5,0)
        svg += self._rline_to(0, -self._stroke_width)
        svg += self._rline_to(-self._stroke_width, 0)
        self._radius -= self._stroke_width
        svg += self._rarc_to(-1, -1)
        self._radius += self._stroke_width
        svg += self._close_path()
        self._calculate_w_h()
        svg += self._style()
        return svg + self._footer()

    def _calculate_w_h(self):
        self._width = (self._max_x-self._min_x+self._stroke_width)*\
                      self._scale
        # print "width is %d, x is %d, right is %d" % (self._width,
                                                     self.margins[2],
                                            int(self._width - self.margins[2]))
        if self.margins[2] == 0:
            self.margins[2] = int(self._stroke_width*2+0.5)
        else:
            self.margins[2] = int(self._width - self.margins[2])
        if self.margins[3] == 0:
            self.margins[3] = int(self._stroke_width*2+0.5)
        else:
            self.margins[3] = int(self._height - self.margins[3])
        self._height = (self._max_y-self._min_y+self._stroke_width)*\
                      self._scale

    def _calculate_x_y(self):
        x = self._stroke_width/2.0
        y = self._stroke_width/2.0+self._radius
        if self._outie is True:
            x += self._innie_x1+self._innie_x2
        if self._cap is True:
            y += self._slot_y*2.0
        return(x, y)

#
# Command-line tools for testing
#

def open_file(datapath, filename):
    return file(os.path.join(datapath, filename), "w")

def close_file(f):
    f.close()

def generator(datapath):

    """
    svgt = SVG()
    svgt.set_orientation(180)
    f = open_file(datapath, "turtle180.svg")
    svg_str = svgt.turtle()
    f.write(svg_str)
    close_file(f)
    """

    svg0 = SVG()
    f = open_file(datapath, "portfolio-test.svg")
    svg0.set_scale(1)
    svg0.expand(25,15)
    svg0.set_slot(True)
    svg0.set_innie([True, True, False, True])
    svg0.set_tab(True)
    svg0.set_gradiant(True)
    svg0.set_draw_innies(False)
    svg_str = svg0.portfolio()
    f.write(svg_str)
    close_file(f)

    """
    svg1 = SVG()
    f = open_file(datapath, "blob-test.svg")
    svg1.set_scale(2)
    svg1.expand(0,20)
    svg1.set_tab(True)
    svg1.set_slot(True)
    svg1.set_gradiant(True)
    svg1.set_hide(True)
    svg_str = svg1.basic_block()
    f.write(svg_str)
    close_file(f)

    svg2 = SVG()
    f = open_file(datapath, "box-test.svg")
    svg2.set_scale(1)
    svg2.expand(40,0)
    svg2.set_colors(["#FFA000","#A08000"])
    svg2.set_gradiant(True)
    svg_str = svg2.basic_box()
    f.write(svg_str)
    close_file(f)

    svg3 = SVG()
    f = open_file(datapath, "compare-text.svg")
    svg3.set_scale(1)
    svg3.set_colors(["#0000FF","#0000A0"])
    svg3.set_gradiant(True)
    # svg3.set_porch(True)
    svg_str = svg3.boolean_compare()
    f.write(svg_str)
    close_file(f)

    svg4 = SVG()
    f = open_file(datapath, "and-or-test.svg")
    svg4.set_scale(1)
    svg4.set_colors(["#00FFFF","#00A0A0"])
    svg4.set_gradiant(True)
    svg_str = svg4.boolean_and_or()
    f.write(svg_str)
    close_file(f)

    svg5 = SVG()
    f = open_file(datapath, "nor-test.svg")
    svg5.set_scale(1)
    svg5.set_colors(["#FF00FF","#A000A0"])
    svg5.set_gradiant(True)
    svg_str = svg5.boolean_not()
    f.write(svg_str)
    close_file(f)
    """

def main():
    return 0

if __name__ == "__main__":
    generator(os.path.abspath('.'))
    main()


#
# Load pixbuf from SVG string
#
def svg_str_to_pixbuf(svg_string):
    pl = gtk.gdk.PixbufLoader('svg')
    pl.write(svg_string)
    pl.close()
    pixbuf = pl.get_pixbuf()
    return pixbuf


#
# Read SVG string from a file
#
def svg_from_file(pathname):
    f = file(pathname, 'r')
    svg = f.read()
    f.close()
    return(svg)

