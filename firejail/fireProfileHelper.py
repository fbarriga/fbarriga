#!/usr/bin/env python

import collections
import pygtk
pygtk.require('2.0')

import gtk

INPUT_FILE="bar"

class FireProfileHelper:

    # close the window and quit
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def readOutput(self, filename):
        f = open( filename, "r" )
        files = {}
        for line in f:
            parts = line.split( '"' )
            action = parts[0].split('(')[0]
            file = parts[1]
            if parts[2].find("ENOENT") > -1:
                self.files_not_found[ file ] = True
            
            if file not in files:
                files[ file ] = []
            
            if action not in files[file]:
                files[ file ].append( action )

        self.files = collections.OrderedDict(sorted(files.items()))

    def createTree(self):
        for file in self.files:
            path = ""
            parts = file.split('/')[1:]
            for part in parts:
                if len( part ) == 0:
                    continue
                old_tmp = path
                path += "/" + part
                if path not in self.data_tree:
                    if len (path.split('/') ) == 2:
                        parent = None
                    else:
                        parent = self.data_tree[ old_tmp ]

                    actions = ""
                    if path in self.files:
                        actions = str.join( "|", self.files[ path ] )
                    markup_path = part
                    if path in self.files_not_found:
                        markup_path = '<span foreground="red">' + part + '</span>'
                    self.data_tree[ path ] = self.treestore.append( parent, [ markup_path, False, actions ])

    def createUITree(self):
        # Create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Create FireJail Profile")
        self.window.set_size_request(600, 600)
        self.window.connect("delete_event", self.delete_event)

        # create a TreeStore with one string column to use as the model
        self.treestore = gtk.TreeStore( str, bool, str )

        # create the TreeView using treestore
        self.treeview = gtk.TreeView(self.treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('Path')

        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'markup', 0)

        # make it searchable
        self.treeview.set_search_column(0)

        renderer_toggle = gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)

        column_toggle = gtk.TreeViewColumn("Enable", renderer_toggle, active=1)
        self.treeview.append_column(column_toggle)

        renderer_text2 = gtk.CellRendererText()
        column_text2 = gtk.TreeViewColumn("Actions", renderer_text2, markup=2)

        self.treeview.append_column(column_text2)

        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.add(self.treeview)

        self.window.add(scrolled_window)
        self.window.show_all()

    def on_cell_toggled(self, widget, path):
        self.treestore[path][1] = not self.treestore[path][1]

    def __init__(self, master=None):
        self.files = {}
        self.files_not_found = {}
        self.readOutput( INPUT_FILE )
        self.createUITree()
        self.data_tree = {}
        self.createTree()


def main():
    gtk.main()

if __name__ == "__main__":
    tvexample = FireProfileHelper()
    main()

