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


class NotesArea(gtk.EventBox):

    def __init__(self):
        gtk.EventBox.__init__(self)

        self.fixed = gtk.Fixed()
        self.notes = []

        self.add(self.fixed)
        self.group = 1
        self.count = 1

        self.show_all()

    def add_note(self):
        note = Note()

        if not self.notes:

            self.fixed.put(note, 40, 40)
            self.notes.append([(40, 40), note])

        elif self.notes:
            last_note_x, last_note_y = self.notes[-1][0]

            if self.group == 1:
                pos = (last_note_x + 240, 40)

            elif self.group > 1:
                pos = (40, 140 * self.group)

            self.fixed.put(note, pos[0], pos[1])
            self.notes.append([pos, note])

        print self.count, self.group

        if self.count != 3:
            self.count += 1

        elif self.count == 3:
            self.group += 1
            self.count = 0

    def set_note_text(self, note=-1, text=""):
        self.notes[note][1].set_text(text)


class Note(gtk.DrawingArea):

    def __init__(self):

        gtk.DrawingArea.__init__(self)

        self.set_size_request(200, 200)
        self.add_events(gtk.gdk.EXPOSURE_MASK | gtk.gdk.VISIBILITY_NOTIFY_MASK)

        self.text = ""

        pango_context = self.get_pango_context()
        self.layout = pango.Layout(pango_context)
        self.layout.set_alignment(pango.ALIGN_CENTER)

        self.connect("expose-event", self._expose_cb)

        self.show_all()

    def _expose_cb(self, widget, event):
        context = self.window.cairo_create()
        gc = self.window.new_gc()

        x, y, w, h = self.get_allocation()

        # Black Frame
        context.rectangle(0, 0, w, h)
        context.set_source_rgb(0, 0, 0)
        context.fill()

        # White Background:
        context.rectangle(0, 0, w - 2, w - 2)
        context.set_source_rgb(0, 255, 0)
        context.fill()

        # Write Text
        self.layout.set_markup(self.text)
        layout_width = self._get_layout_width()

        new_x = x + w / 2 - layout_width / 2

        self.window.draw_layout(gc, new_x, 0, self.layout)

    def _get_layout_width(self, text=None):
        if not text:
            text = self.text
        str_long = len(text)
        pixel_size = self.layout.get_pixel_size()[1]

        layout_size = str_long * pixel_size

        return layout_size

    def set_text(self, text):
        layout_width = self._get_layout_width(text)
        x, y, w, h = self.get_allocation()

        if w > layout_width:
            self.text = text

        else:
            print "The text is longer than the Note (%s px / %s px)" % (
                                                            layout_width, w)

if __name__ == "__main__":
    w = gtk.Window()
    n = NotesArea()
    w.add(n)
    n.add_note()
    n.add_note()
    w.resize(800, 600)
    w.show_all()
    n.set_note_text(0, "Agu")
    n.set_note_text(1, "Aguz")
    gtk.main()
