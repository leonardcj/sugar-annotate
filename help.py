#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# help.py by:
#    Ignacio Rodríguez <ignacio@sugarlabs.org>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
import gtk
import os
import gobject
from gettext import gettext as _
close = gtk.ToolButton()


class helpbox(gtk.VBox):
    def __init__(self):
        super(helpbox, self).__init__()
        self.toolbar = gtk.Toolbar()
        close.set_icon_name('gtk-cancel')
        self.titlelabel = gtk.Label(_('Help of Annotate'))
        self.toolitem = gtk.ToolItem()
        self.toolitem.add(self.titlelabel)
        self.toolbar.set_size_request(100, 55)
        self.separator = gtk.SeparatorToolItem()
        self.separator.props.draw = False
        self.separator.set_expand(True)
        self.activityitem = gtk.ToolItem()
        self.activityicon = gtk.Image()
        self.activityitem.add(self.activityicon)
        self.activityicon.set_from_file('activity/annotate.svg')
        self.toolbar.insert(self.activityitem, -1)
        self.toolbar.insert(self.toolitem, -1)
        self.toolbar.insert(self.separator, -1)
        self.toolbar.insert(close, -1)
        self.frame_path = \
        os.path.expanduser('~/Activities/Annotate.activity/help/')
        self.connect('show', self.first)
        self.framesdir = os.listdir(self.frame_path)
        self.frames = []
        self.width = int(gtk.gdk.screen_width() / 1.255 - 55)
        self.height = int(gtk.gdk.screen_height() / 1.255 - 55)
        for x in self.framesdir:
            self.frames.append(self.frame_path + x)
            self.frames = sorted(self.frames)
        self.frame = gtk.Image()
        self.currentframe = 1
        self.frame.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size
            (self.frames[self.currentframe], self.width, self.height))
        self.pack_start(self.toolbar, False, False, 0)
        self.pack_start(self.frame, True, True, 0)
        self.show_all()
        self.update()

    def update(self):
        self.currentframe += 1
        try:
            self.frame.set_from_pixbuf(gtk.gdk.pixbuf_new_from_file_at_size
            (self.frames[self.currentframe], self.width, self.height))
        except IndexError:
            self.currentframe = 1
        self.frame.show()
        if self.currentframe >= 11 and self.currentframe <= 20:
            gobject.timeout_add(1000, self.update)
        else:
            gobject.timeout_add(500, self.update)

    def first(self, widget):
        self.currentframe = 1


class helpwindow(gtk.Window):
    def __init__(self):
        super(helpwindow, self).__init__()
        self.help = helpbox()
        self.add(self.help)
        self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.set_title(_('Help of Annotate'))
        self.set_decorated(False)
        self.set_resizable(False)
        close.connect('clicked', lambda x: self.hide())
        self.show_all()
