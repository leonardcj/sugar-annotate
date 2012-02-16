#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# activity.py by:
#    Agustin Zubiaga <aguz@sugarlabs.com>

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
import pango

WHITE = gtk.gdk.Color('#FFFFFF')


class NotesArea(gtk.EventBox):

    def __init__(self):
        gtk.EventBox.__init__(self)

        self.mainbox = gtk.VBox()
        self.notes = []

        self.add(self.mainbox)
        self.groups = []
        self.notes = []

        self.modify_bg(gtk.STATE_NORMAL, WHITE)

        self._add_box()

        self.show_all()

    def add_note(self):
        note = Note()

        if not self.groups[-1].space:
            self._add_box()

        last_box = self.groups[-1]
        last_box.pack_start(note, False, True, 20)
        last_box.space -= 1

        self.notes.append(note)

        self.show_all()

        return note

    def _add_box(self):
        box = gtk.HBox()
        box.space = 3

        self.mainbox.pack_start(box, False, True, 20)
        self.groups.append(box)

    def set_note_text(self, note=-1, text=''):
        self.notes[note].set_text(text)


class Note(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.set_size_request(200, 200)
        self.add_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.VISIBILITY_NOTIFY_MASK)

        self.text = ''

        pango_context = self.get_pango_context()
        self.layout = pango.Layout(pango_context)
        self.layout.set_alignment(pango.ALIGN_CENTER)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.ENTER_NOTIFY_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK)

        self.connect('expose-event', self._expose_cb)
        self.connect('button-press-event', self.__button_press_cb)

        self.show_all()

    def _expose_cb(self, widget, event):
        context = self.window.cairo_create()
        gc = self.window.new_gc()

        x, y, w, h = self.get_allocation()

        # Black Frame:
        context.rectangle(0, 0, w, h)
        context.set_source_rgb(0, 0, 0)
        context.fill()

        # Background rectangle:
        context.rectangle(0, 0, w - 1.5, w - 1.5)
        context.set_source_rgb(56862, 59938, 0)
        context.fill()

        # Write Text:
        self.layout.set_markup(self.text)

        self.window.draw_layout(gc, 0, 0, self.layout)

    def set_text(self, text):
        self.text = text
        self.queue_draw()

    def __button_press_cb(self, widget, event):
        window = gtk.Window()
        entry = gtk.Entry()
        entry.connect('changed', lambda w: self.set_text(w.get_text()))

        window.add(entry)
        window.show_all()
