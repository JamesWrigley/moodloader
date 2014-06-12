#! /usr/bin/python3

# ########################## Copyrights and License ##############################
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
import subprocess
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
        self.wz_binary = shutil.which("warzone2100")


        super(MoodLoader, self).__init__()
        self.initUI()

        ### Set up connections ###
        self.install_map_button.clicked.connect(lambda: self.install_addon("/maps/"))
        self.install_cam_mod_button.clicked.connect(lambda: self.install_addon("/mods/campaign/"))
        self.install_global_mod_button.clicked.connect(lambda: self.install_addon("/mods/global/"))

        ### Set up the QListView's
        self.populate_listviews()
        for listview in [self.maps_listview, self.cam_mods_listview, self.global_mods_listview]:
            listview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        # Connect each QListView to send its addon type to 'self.listview()'
        self.maps_listview.connect(self.maps_listview, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                       lambda: self.listview_menu("/maps/"))
        self.cam_mods_listview.connect(self.cam_mods_listview, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                       lambda: self.listview_menu("/mods/campaign/"))
        self.global_mods_listview.connect(self.global_mods_listview, QtCore.SIGNAL("customContextMenuRequested(QPoint)"),
                                          lambda: self.listview_menu("/mods/global/"))


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
            self.statusbar.showMessage("No config folder found.")
            return("")


    def install_addon(self, addon_type):
        """
        Install a map to the /.warzone2100-xx/maps folder.
        Note that even though the name of the argument is 'addon_type', it's actually
        the folder name the map is to be installed into (i.e. '/maps/' for a map).
        """
        addon_path = QtGui.QFileDialog.getOpenFileName(self, "Select Addon", self.open_dialog_dir, "WZ Addons (*.wz);; All files (*.*)")
        addon_install_path  = self.config_dir + addon_type
        addon_name = os.path.basename(addon_path)

        # Check that all cases are covered before installing
        if not addon_path:
            return
        elif not os.path.isdir(addon_install_path):
            os.mkdir(addon_install_path)
        elif os.path.isfile(addon_install_path + addon_name):
            self.statusbar.showMessage("Addon already installed.")
            return

        shutil.copy(addon_path, addon_install_path)
        self.populate_listviews()
        self.statusbar.showMessage("Addon installed.")
        self.open_dialog_dir = os.path.dirname(addon_path) # Note that we reset 'self.open_dialog_dir' to the last used folder


    def delete_addon(self, addon_type):
        """
        As abundantly clear from the name, this method deletes the currently
        selected addon.
        """
        addon_folder = self.config_dir + addon_type

        if addon_type == "/maps/":
            addon_name = self.maps_listview.currentIndex().data(role=3)
        elif addon_type == "/mods/campaign/":
            addon_name = self.cam_mods_listview.currentIndex().data(role=3)
        elif addon_type == "/mods/global/":
            addon_name = self.global_mods_listview.currentIndex().data(role=3)

        # Get confirmation from the user before deleting
        confirmation_dialog = QtGui.QMessageBox.question(self, "Confirm Action",
                                                         "Are you sure you want to delete this addon?",
                                                         QtGui.QMessageBox.No,
                                                         QtGui.QMessageBox.Yes)
        if confirmation_dialog == QtGui.QMessageBox.Yes:
            os.remove(addon_folder + addon_name)
            self.populate_listviews()
            self.statusbar.showMessage("Addon successfully deleted.")


    def condense_addon(self, addon_name):
        """
        A little helper function to pretty-ify output for the QListView's.
        """
        # The hash length is always 64 chars, so by this we check if one is in the name
        if len(addon_name) > 64:
            addon_name = re.findall(".*-", addon_name)[0]
            return(addon_name[:-1]) # Removes the trailing dash before returning
        else:
            return(addon_name.replace(".wz", ""))


    def populate_listviews(self):
        """
        Gets a list of map, campaign, and global mods, and populates their
        respective QListView's with them.
        """
        # We need this to elide the text
        addon_size = QtCore.QSize(50, 15)
        # And this to sort the mods properly (mainly maps)
        natural_sort = lambda addon: (float(re.split("([0-9]+)", addon)[1]))
                
        # Clear all existing items
        for model in [self.map_data_model, self.cam_data_model, self.global_data_model]:
            model.clear()

        if os.path.isdir(self.config_dir + "/maps/"):
            maps = [addon for addon in os.listdir(self.config_dir + "/maps/")
                        if os.path.isfile(self.config_dir + "/maps/" + addon) and addon.__contains__(".wz")]
            maps.sort(key=natural_sort)

            for addon in maps:
                addon_item = QtGui.QStandardItem(self.condense_addon(addon))
                addon_item.setSizeHint(addon_size)
                addon_item.setToolTip(addon)
                addon_item.setEditable(False)
                self.map_data_model.appendRow(addon_item)

        if os.path.isdir(self.config_dir + "/mods/campaign/"):
            cam_mods = [addon for addon in os.listdir(self.config_dir + "/mods/campaign/")
                        if os.path.isfile(self.config_dir + "/mods/campaign/" + addon) and addon.__contains__(".wz")]

            for addon in cam_mods:
                addon_item = QtGui.QStandardItem(self.condense_addon(addon))
                addon_item.setSizeHint(addon_size)
                addon_item.setToolTip(addon)
                addon_item.setEditable(False)
                self.cam_data_model.appendRow(addon_item)

        if os.path.isdir(self.config_dir + "/mods/global/"):
            global_mods = [addon for addon in os.listdir(self.config_dir + "/mods/global/")
                           if os.path.isfile(self.config_dir + "/mods/global/" + addon) and addon.__contains__(".wz")]

            for addon in global_mods:
                addon_item = QtGui.QStandardItem(self.condense_addon(addon))
                addon_item.setSizeHint(addon_size)
                addon_item.setToolTip(addon)
                addon_item.setEditable(False)
                self.global_data_model.appendRow(addon_item)


    def run_addon(self, wz_flag):
        """
        As the self-explanatory name implies, this runs the selected mod.
        Note that we use 'subprocess.Popen' so as not to block the GUI.
        """

        # Retrieve the tooltip (which is the filename) from the active item
        if wz_flag == " --mod_ca=":
            addon = self.cam_mods_listview.currentIndex().data(role=3)
        elif wz_flag == " --mod=":
            addon = self.global_mods_listview.currentIndex().data(role=3)

        subprocess.Popen(self.wz_binary + wz_flag + addon, shell=True)

    def listview_menu(self, addon_type):
        """
        Called when a QListView item is right-clicked on, lets the user delete
        the selected addon.
        """
        # Create the menu
        menu = QtGui.QMenu("Options", self)

        # Create actions
        delete_addon_action = QtGui.QAction("Delete Addon", self)
        delete_addon_action.triggered.connect(lambda: self.delete_addon(addon_type))
        menu.addAction(delete_addon_action)

        if addon_type != "/maps/":
            run_addon_action = QtGui.QAction("Run Addon", self)
            run_addon_action.triggered.connect(lambda: self.run_addon(wz_flag))
            menu.addAction(run_addon_action)

            if addon_type == "/mods/campaign/":
                wz_flag = " --mod_ca="
            elif addon_type == "/mods/global/":
                wz_flag = " --mod="

        # Display menu the cursor position
        menu.exec_(QtGui.QCursor.pos())


def main():
    app = QtGui.QApplication(sys.argv)
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
