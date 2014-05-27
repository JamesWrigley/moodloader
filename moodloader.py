#! /usr/bin/python3

# ########################## Copyrights and license ##############################
#                                                                                #
# This file is part of MoodLoader. http://github.com/JamesWrigley/MoodLoader/    #
#                                                                                #
# MoodLoader is free software: you can redistribute it and/or modify it under    #
# the terms of the GNU General Public License as published by the Free Software  #
# Foundation, either version 3 of the License, or (at your option) any later     #
# version.                                                                       #
#                                                                                #
# MoodLoader is distributed in the hope that it will be useful, but WITHOUT ANY  #
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS      #
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. #
#                                                                                #
# You should have received a copy of the GNU General Public License along with   #
# MoodLoader. If not, see <http://www.gnu.org/licenses/>.                        #
#                                                                                #
# ################################################################################

import re
import os
import sys
import shutil
from PyQt4 import QtGui, QtCore
from moodloader_ui import MoodLoader

class MainWindow(MoodLoader):
    """
    Subclass the GUI for the main window. We implement '__init__()' here, and
    also set up connections for the widgets.
    """

    def __init__(self):
        ### Create some system variables ###
        self.config_dir = self.get_config_path()
        self.open_dialog_dir = os.path.expanduser("~")


        super(MoodLoader, self).__init__()
        self.initUI()

        ### Set up connections ###
        self.install_map_button.clicked.connect(lambda: self.install_mod("/maps/"))
        self.install_cam_mod_button.clicked.connect(lambda: self.install_mod("/campaign/"))
        self.install_global_mod_button.clicked.connect(lambda: self.install_mod("/global/"))

        ### Set up the QListView's
        self.populate_listviews()
        for listview in [self.map_mods_listview, self.cam_mods_listview, self.global_mods_listview]:
            listview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # Connect each QListView to send its mod type to 'self.listview()'
        self.map_mods_listview.connect(self.map_mods_listview, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                       lambda: self.listview_menu("map"))
        self.cam_mods_listview.connect(self.cam_mods_listview, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                       lambda: self.listview_menu("cam"))
        self.global_mods_listview.connect(self.global_mods_listview, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                          lambda: self.listview_menu("global"))


    def get_config_path(self):
        """
        Get the path of the config folder of the latest version of WZ on the
        users computer.
        """
        matching_dir_versions = [float(re.findall(r'\d+\.\d+', directory)[0])
                                 for directory in os.listdir(os.path.expanduser("~"))
                                 if re.match(".warzone2100-\d+\.\d+", directory)]

        if len(matching_dir_versions) >= 1:
            return(os.path.expanduser("~") + "/.warzone2100-" + str(max(matching_dir_versions)))
        else:
            self.statusbar.showMessage("No config folder found!")
            return("")


    def install_mod(self, mod_type):
        """
        Install a map to the /.warzone2100-xx/maps folder.
        Note that even the name of the argument is 'mod_type', it's actually
        the folder name the map is to be installed into (i.e. '/maps/' for a map mod).
        """
        mod_path = QtGui.QFileDialog.getOpenFileName(self, "Select Mod", self.open_dialog_dir, "WZ Mods (*.wz);; All files (*.*)")
        mod_install_path  = self.config_dir + mod_type
        mod_name = os.path.basename(mod_path)

        # Check that all cases are covered before installing
        if not mod_path:
            return
        elif not os.path.isdir(mod_install_path):
            os.mkdir(mod_install_path)
        elif os.path.isfile(mod_install_path + mod_name):
            self.statusbar.showMessage("Mod already installed!")
            return

        shutil.copy(mod_path, mod_install_path)
        self.populate_listviews()
        self.statusbar.showMessage("Map installed!")
        self.open_dialog_dir = os.path.dirname(mod_path) # Note that we reset 'self.open_dialog_dir' to the last used folder


    def delete_mod(self, mod_type):
        """
        As abundantly clear from the name, this method deletes the currently
        selected mod.
        """
        if mod_type == "map":
            mod_name = self.map_mods_listview.currentIndex().data()
            mod_folder = self.config_dir + "/maps/"
        elif mod_type == "cam":
            mod_name = self.cam_mods_listview.currentIndex().data()
            mod_folder = self.config_dir + "/campaign/"
        elif mod_type == "global":
            mod_name = self.global_mods_listview.currentIndex().data()
            mod_folder = self.config_dir + "/global/"

        # Get the full file name from the partial 'mod_name'
        mod_name = next((mod for mod in os.listdir(mod_folder) if mod.__contains__(mod_name)))
        os.remove(mod_folder + mod_name)
        self.populate_listviews()
        self.statusbar.showMessage("Mod successfully deleted!")


    def condense_mod(self, mod_name):
        """
        A little helper function to pretty-ify output for the QListView's.
        """
        # The hash length is always 64 chars, so by this we check if one is in the name
        if len(mod_name) > 64:
            mod_name = re.findall(".*-", mod_name)[0]
            return(mod_name[:-1]) # Removes the trailing dash before returning
        else:
            return(mod_name.replace(".wz", ""))


    def populate_listviews(self):
        """
        Gets a list of map, campaign, and global mods, and populates their
        respective QListView's with them.
        """
        # We need this to elide the text
        mod_size = QtCore.QSize(50, 15)

        # Clear all existing items
        for model in [self.map_data_model, self.cam_data_model, self.global_data_model]:
            model.clear()

        if os.path.isdir(self.config_dir + "/maps/"):
            map_mods = [mod for mod in os.listdir(self.config_dir + "/maps/")
                        if os.path.isfile(self.config_dir + "/maps/" + mod) and mod.__contains__(".wz")]
            for mod in map_mods:
                mod_item = QtGui.QStandardItem(self.condense_mod(mod))
                mod_item.setSizeHint(mod_size)
                mod_item.setToolTip(mod)
                mod_item.setEditable(False)
                self.map_data_model.appendRow(mod_item)

        if os.path.isdir(self.config_dir + "/campaign/"):
            cam_mods = [mod for mod in os.listdir(self.config_dir + "/campaign/")
                        if os.path.isfile(self.config_dir + "/campaign/" + mod) and mod.__contains__(".wz")]
            for mod in cam_mods:
                mod_item = QtGui.QStandardItem(self.condense_mod(mod))
                mod_item.setSizeHint(mod_size)
                mod_item.setToolTip(mod)
                mod_item.setEditable(False)
                self.cam_data_model.appendRow(mod_item)

        if os.path.isdir(self.config_dir + "/global/"):
            global_mods = [mod for mod in os.listdir(self.config_dir + "/global/")
                           if os.path.isfile(self.config_dir + "/global/" + mod) and mod.__contains__(".wz")]
            for mod in global_mods:
                mod_item = QtGui.QStandardItem(self.condense_mod(mod))
                mod_item.setSizeHint(mod_size)
                mod_item.setToolTip(mod)
                mod_item.setEditable(False)
                self.global_data_model.appendRow(mod_item)


    def listview_menu(self, mod_type):
        """
        Called when a QListView item is right-clicked on, lets the user delete
        the selected mod.
        """
        # Create the delete action
        delete_mod_action = QtGui.QAction("Delete Mod", self)
        delete_mod_action.triggered.connect(lambda: self.delete_mod(mod_type))

        # Create the menu, and display it at the cursor position
        menu = QtGui.QMenu("Options", self)
        menu.addAction(delete_mod_action)

        menu.exec_(QtGui.QCursor.pos())


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
