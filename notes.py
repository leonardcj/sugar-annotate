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
import gobject
import pango

#from gettext import gettext as _

WHITE = gtk.gdk.Color('#FFFFFF')
BLACK = gtk.gdk.Color('#000000')

NOTE_WIDTH = 200
NOTE_HEIGHT = 200
LEFT_MARGIN = 15
RIGHT_MARGIN = 15
LAYOUT_WIDTH = NOTE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
BOX_SPACE = 20

ESC_KEY = 65307


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
        note.connect('editing', self.__editing_note_cb)

        if not self.groups[-1].space:
            self._add_box()

        last_box = self.groups[-1]
        last_box.pack_start(note.fixed, False, True, BOX_SPACE)
        last_box.space -= 1

        if last_box.space == 2:
            last_box.show_all()

        self.notes.append(note)

        note.fixed.show_all()
        note.textview.frame.hide()

        return note

    def _add_box(self):
        box = gtk.HBox()
        box.space = 3

        self.mainbox.pack_start(box, False, True, BOX_SPACE)
        self.groups.append(box)

    def set_note_text(self, note=-1, text=''):
        self.notes[note].set_text(text)

    def __editing_note_cb(self, note):
        for i in self.notes:
            if i != note:
                i.hide_textview()

    def __note_removed_cb(self, note):
        del self.notes[self.notes.index(note)]
        self._relocate_notes()

    def _relocate_notes(self):
        data = [i.text for i in self.notes]

        for i in self.groups:
            i.destroy()

        for i in data:
            note = self.add_note()
            note.set_text(i)


class Note(gtk.DrawingArea):

    __gsignals__ = {'editing': (gobject.SIGNAL_RUN_FIRST, None, []),
                    'removed': (gobject.SIGNAL_RUN_FIRST, None, [])}

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.set_size_request(NOTE_WIDTH, NOTE_HEIGHT)

        self.text = ''

        pango_context = self.get_pango_context()
        self.layout = pango.Layout(pango_context)
        self.layout.set_width(LAYOUT_WIDTH * pango.SCALE)
        self.layout.set_wrap(pango.WRAP_WORD)

        self.add_events(gtk.gdk.EXPOSURE_MASK |
                        gtk.gdk.VISIBILITY_NOTIFY_MASK |
                        gtk.gdk.BUTTON_PRESS_MASK |
                        gtk.gdk.BUTTON_RELEASE_MASK |
                        gtk.gdk.POINTER_MOTION_MASK |
                        gtk.gdk.ENTER_NOTIFY_MASK |
                        gtk.gdk.LEAVE_NOTIFY_MASK)

        self.connect('expose-event', self._expose_cb)
        self.connect('button-press-event', self.__edit_cb)
        self.connect('button-press-event', self.__popup_menu_cb)

        self.fixed = gtk.Fixed()

        self.fixed.put(self, 0, 0)

        self.textview = gtk.TextView()
        self.textview.set_left_margin(LEFT_MARGIN)
        self.textview.set_right_margin(RIGHT_MARGIN)

        self.textview.set_wrap_mode(gtk.WRAP_WORD)

        self.textview.set_property('width-request', NOTE_WIDTH)
        self.textview.set_property('height-request', NOTE_HEIGHT)

        self.textview.connect('key-press-event', self.__hide_textview_cb)

        self.textview.frame = gtk.Frame()
        self.textview.frame.modify_bg(gtk.STATE_NORMAL,
                                      BLACK)
        self.textview.frame.add(self.textview)

        self.fixed.put(self.textview.frame, 0, 0)

    def _expose_cb(self, widget, event):
        context = self.window.cairo_create()
        gc = self.window.new_gc()

        x, y, w, h = self.get_allocation()

        # Black Frame:
        context.rectangle(0, 0, w, h)
        context.set_source_rgb(0, 0, 0)
        context.fill()

        # Background rectangle:
        context.rectangle(0, 0, w - 1.5, h - 1.5)
        context.set_source_rgb(56862, 59938, 0)
        context.fill()

        # Write Text:

        self.layout.set_markup(self.text)

        self.window.draw_layout(gc, LEFT_MARGIN, 0, self.layout)

    def set_text(self, text):
        self.text = text
        self.queue_draw()

    def hide_textview(self):
        self._set_text(self.textview)

        self.textview.frame.hide()
        self.show()

    def __hide_textview_cb(self, widget, event):
        if event.keyval == ESC_KEY:
            self.hide_textview()

    def _set_text(self, widget):
        buffer = widget.get_buffer()
        start, end = buffer.get_bounds()
        text = buffer.get_text(start, end)

        self.set_text(text)

    def __edit_cb(self, widget, event):
        if event.button == 1:
            self.hide()
            buf = self.textview.get_buffer()
            buf.set_text(self.text)
            self.textview.frame.show_all()

            self.emit('editing')

    def __popup_menu_cb(self, widget, event):
        if event.button == 3:
            popup_menu = gtk.Menu()

            remove_note = gtk.ImageMenuItem(gtk.STOCK_REMOVE)
            remove_note.set_use_stock(True)
            remove_note.connect('activate', self._remove_note)
            popup_menu.append(remove_note)

            popup_menu.popup(None, None, None, event.button, event.time, None)
            popup_menu.show_all()

    def _remove_note(self, widget):
        self.fixed.destroy()
        self.emit('removed')
