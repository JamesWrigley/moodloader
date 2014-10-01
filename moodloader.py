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
import zipfile
import subprocess
from PyQt4 import QtGui, QtCore
from moodloader_ui import MoodLoader, PropertiesDialog

class MainWindow(MoodLoader):
    """
    Subclass the GUI for the main window. We implement '__init__()' here, and
    also set up connections for the widgets.
    """

    def __init__(self):
        super(MoodLoader, self).__init__()
        self.initUI()

        ### Create some system variables ###
        self.config_dir = self.get_config_path()
        self.open_dialog_dir = os.path.expanduser("~")
        self.wz_binary = self.get_binary_path(False)

        ### Set up connections ###
        self.install_map_button.clicked.connect(lambda: self.install_addon("/maps/"))
        self.install_cam_mod_button.clicked.connect(lambda: self.install_addon("/mods/campaign/"))
        self.install_global_mod_button.clicked.connect(lambda: self.install_addon("/mods/global/"))
        self.install_multiplayer_mod_button.clicked.connect(lambda: self.install_addon("/mods/multiplay/"))

        ### Set up the QListView's
        self.populate_listviews()
        for listview in [self.maps_listview, self.cam_mods_listview, self.global_mods_listview, self.multiplayer_mods_listview]:
            listview.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        ### Connect each QListView to send its addon type to 'self.listview()'

        # Some helper lambda's
        check_if_maps_item = lambda point: self.maps_listview.indexAt(point).isValid()
        check_if_global_item = lambda point: self.global_mods_listview.indexAt(point).isValid()
        check_if_cam_item = lambda point: self.cam_mods_listview.indexAt(point).isValid()
        check_if_multiplay_item = lambda point: self.multiplayer_mods_listview.indexAt(point).isValid()

        self.maps_listview.customContextMenuRequested.connect(lambda point:
                                                              self.listview_menu("/maps/")
                                                              if check_if_maps_item(point) else None)
        self.cam_mods_listview.customContextMenuRequested.connect(lambda point:
                                                                  self.listview_menu("/mods/campaign/")
                                                                  if check_if_cam_item(point) else None)
        self.global_mods_listview.customContextMenuRequested.connect(lambda point:
                                                                     self.listview_menu("/mods/global/")
                                                                     if check_if_global_item(point) else None)
        self.multiplayer_mods_listview.customContextMenuRequested.connect(lambda point:
                                                                          self.listview_menu("/mods/multiplay/")
                                                                          if check_if_multiplay_item(point) else None)


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


    def get_binary_path(self, assign):
        """
        Get the path of the WZ binary. The 'assign' boolean specifies whether we
        assign 'binary_path' to an existing 'self.wz_binary' variable or just return it.
        The 'assign' field should always be True when called after the program starts
        since the 'self.wz_binary' field is already existent.
        If a config file exists, we read from that, else we write the 'binary_path' to
        a new one if the user chooses a binary.
        """
        config_file = os.path.expanduser("~") + "/.moodloader"

        if os.path.isfile(config_file) and os.path.getsize(config_file) > 0:
            config_file = open(config_file)
            binary_path = config_file.readline()
            config_file.close()
        else:
            binary_path = shutil.which("warzone2100")

            # If 'shutil.which()' can't find the binary, then we prompt the user for it
            if binary_path == None:
                confirmation_dialog = QtGui.QMessageBox.question(self, "Missing Path",
                                                                 "Moodloader cannot find the path of Warzone, would you like to set it manually? If you don't you will not be able to run addons from Moodloader.",
                                                                 QtGui.QMessageBox.No,
                                                                 QtGui.QMessageBox.Yes)
                if confirmation_dialog == QtGui.QMessageBox.Yes:
                    binary_path = QtGui.QFileDialog.getOpenFileName(self, "Select Binary",
                                                                    os.path.expanduser("~"))
                    # Write the users settings to 'config_file'
                    config_file = open(config_file, "w")
                    config_file.write(binary_path)
                    config_file.close()

        if assign:
            self.wz_binary = binary_path
        elif not assign:
            return(binary_path)


    def install_addon(self, addon_type):
        """
        Install an addon to the appropriate folder.
        Note that even though the name of the argument is 'addon_type', it's actually
        the folder name the map is to be installed into (i.e. '/maps/' for a map).
        """
        addon_path = QtGui.QFileDialog.getOpenFileName(self, "Select Addon", self.open_dialog_dir, "WZ Addons (*.wz);; All files (*.*)")
        addon_install_path  = self.config_dir + addon_type
        addon_name = os.path.basename(addon_path)

        # Check that all prerequisites are covered before installing
        if not addon_path:
            return
        elif not os.path.isdir(addon_install_path):
            # Show a warning dialog if Moodloader is underpriveleged
            try:
                os.makedirs(addon_install_path)
            except PermissionError as error:
                QtGui.QMessageBox.warning(self, "Error", str(error))
                return
        elif os.path.isfile(addon_install_path + addon_name):
            self.statusbar.showMessage("Addon already installed.")
            return

        shutil.copy(addon_path, addon_install_path)
        self.populate_listviews()
        self.statusbar.showMessage("Addon installed.")
        self.open_dialog_dir = os.path.dirname(addon_path) # Note that we reset 'self.open_dialog_dir' to the last used folder


    def delete_addons(self, addon_type):
        """
        As abundantly clear from the name, this method deletes all the currently
        selected addons.
        """
        # 'get_file_name' gets the actual map name from the tooltip passed to it,
        # it's meant to work on the tooltips of map-mods, which are HTML formatted
        get_file_name = lambda addon: re.search("[0-9](\S+?).wz", addon).group()
        addon_folder = self.config_dir + addon_type
        selected_addons = []

        # Populate 'selected_addons' with the users selection
        if addon_type == "/maps/":
            selected_addons = [get_file_name(addon.data(role=3)) for addon in self.maps_listview.selectedIndexes()]
        elif addon_type == "/mods/campaign/":
            selected_addons = [addon.data(role=3) for addon in self.cam_mods_listview.selectedIndexes()]
        elif addon_type == "/mods/global/":
            selected_addons = [addon.data(role=3) for addon in self.global_mods_listview.selectedIndexes()]
        elif addon_type == "/mods/multiplay/":
            selected_addons = [addon.data(role=3) for addon in self.multiplayer_mods_listview.selectedIndexes()]

        # Make accurate messages to display, and get confirmation from the user before deleting
        if len(selected_addons) == 1:
            dialog_string = "Are you sure you want to delete this addon?"
            statusbar_message = "Addon successfully deleted."
        else:
            dialog_string = "Are you sure you want to delete these addons?"
            statusbar_message = "Addons successfully deleted."
        confirmation_dialog = QtGui.QMessageBox.question(self, "Confirm Delete",
                                                         dialog_string,
                                                         QtGui.QMessageBox.No,
                                                         QtGui.QMessageBox.Yes)
        if confirmation_dialog == QtGui.QMessageBox.Yes:
            for addon in selected_addons: os.remove(addon_folder + addon)
            self.populate_listviews()
            self.statusbar.showMessage(statusbar_message)


    def run_addons(self, wz_flag):
        """
        As the name implies, this runs all selected addons.
        Note that we use 'subprocess.Popen' so as not to block the GUI.
        """
        args = [self.wz_binary]

        # Retrieve the tooltips (which are the filenames) from the selected items
        if wz_flag == "--mod_ca=":
            selected_addons = [mod.data(role=3) for mod in self.cam_mods_listview.selectedIndexes()]
            for mod in selected_addons: args.append("--mod_ca={0}".format(mod))
        elif wz_flag == "--mod=":
            selected_addons = [mod.data(role=3) for mod in self.global_mods_listview.selectedIndexes()]
            for mod in selected_addons: args.append("--mod={0}".format(mod))
        elif wz_flag == "--mod_mp=":
            selected_addons = [mod.data(role=3) for mod in self.multiplayer_mods_listview.selectedIndexes()]
            for mod in selected_addons: args.append("--mod_mp={0}".format(mod))

        subprocess.Popen(args)


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


    def check_addon(self, addon_path):
        """
        Checks the addon for validity. If the addon is a map mod we return 1,
        and if its file layout is mutilated we return 2, else we return 0.
        """
        forbidden_files = ['Thumbs.db', 'Desktop.ini', '.DS_Store']
        forbidden_extensions = ['.bak', '.tmp', '.wz', '.zip', '.js', '.png']
        required_extensions = ['.gam', '.bjo', '.map', '.ttp', '.lev']

        with zipfile.ZipFile(addon_path) as addon:
            addon_files = addon.namelist()
            addon_file_extensions = [os.path.splitext(path)[1] for path in addon_files]

        # Make sure all cases are covered
        if any("\\" in file for file in addon_files):
            return(2)
        elif not (all(ext in addon_file_extensions for ext in required_extensions) and not \
             any(ext in addon_file_extensions for ext in forbidden_extensions) and not \
             any(illegal in addon_files for illegal in forbidden_files)):
            return(1)
        else:
            return(0)


    def populate_listviews(self):
        """
        Gets a list of all installed addons and populates their respective
        QListView's with them.
        """
        addon_size = QtCore.QSize(50, 15) # We need this to elide the text
        natural_sort = lambda addon: (float(re.split("([0-9]+)", addon)[1])) # A key to sort the maps properly
        maps_dir = self.config_dir + "/maps/"
        cam_mods_dir = self.config_dir + "/mods/campaign/"
        global_mods_dir = self.config_dir + "/mods/global/"
        multiplayer_mods_dir = self.config_dir + "/mods/multiplay/"
                
        # Clear all existing items
        for model in [self.map_data_model, self.cam_data_model, self.global_data_model, self.multiplayer_data_model]:
            model.clear()

        for directory in [maps_dir, cam_mods_dir, global_mods_dir, multiplayer_mods_dir]:
            if os.path.isdir(directory):
                if directory == maps_dir:
                    data_model = self.map_data_model
                elif directory == cam_mods_dir:
                    data_model = self.cam_data_model
                elif directory == global_mods_dir:
                    data_model = self.global_data_model
                else:
                    data_model = self.multiplayer_data_model

                addon_list = [addon for addon in os.listdir(directory)
                              if os.path.isfile(directory + addon) and addon.__contains__(".wz")]
                if directory == maps_dir: addon_list.sort(key=natural_sort) # We only sort maps

                # Create the items to append to each QListView
                for addon in addon_list:
                    addon_item = QtGui.QStandardItem(self.condense_addon(addon))
                    addon_item.setSizeHint(addon_size)
                    addon_item.setToolTip(addon)
                    addon_item.setEditable(False)
                    # Mark all map-mods
                    if directory == maps_dir:
                        if self.check_addon(directory + addon) == 1:
                            addon_item.setForeground(QtCore.Qt.red)
                            addon_item.setToolTip("<p align=center style=white-space:pre>{0} <br>This is a map-mod.</p>".format(addon))
                        elif self.check_addon(directory + addon) == 2:
                            addon_item.setForeground(QtCore.Qt.darkMagenta)
                            addon_item.setToolTip("<p align=center style=white-space:pre>{0} <br>This map has corrupted paths.</p>".format(addon))

                    data_model.appendRow(addon_item)


    def listview_menu(self, addon_type):
        """
        Called when a QListView item is right-clicked on, shows the user
        available operations to perform on the addon.
        """
        # Set up some variables for later. 'wz_flag' is a 'run_addons() argument,
        # and 'addon_path' is the absolute path of the currently active addon.
        if addon_type == "/maps/":
            addon_path = self.config_dir + addon_type + re.search("[0-9](\S+?).wz",
                                                                  self.maps_listview.currentIndex().data(role=3)).group()
        elif addon_type == "/mods/campaign/":
            wz_flag = "--mod_ca="
            addon_path = self.config_dir + addon_type + self.cam_mods_listview.currentIndex().data(role=3)
        elif addon_type == "/mods/global/":
            wz_flag = "--mod="
            addon_path = self.config_dir + addon_type + self.global_mods_listview.currentIndex().data(role=3)
        elif addon_type == "/mods/multiplay/":
            wz_flag = "--mod_mp="
            addon_path = self.config_dir + addon_type + self.multiplayer_mods_listview.currentIndex().data(role=3)


        # Create the menu
        menu = QtGui.QMenu("Options", self)

        # Create actions
        delete_addons_action = QtGui.QAction("Delete addon(s)", self)
        delete_addons_action.triggered.connect(lambda: self.delete_addons(addon_type))
        menu.addAction(delete_addons_action)

        # We only add the run options for mods, not maps
        if addon_type != "/maps/":
            # We only go into the first branch if 'self.wz_binary' is empty
            if self.wz_binary == None:
                get_binary_path_action = QtGui.QAction("Choose Binary", self)
                get_binary_path_action.triggered.connect(lambda: self.get_binary_path(True))
                menu.addAction(get_binary_path_action)
            else:
                run_addons_action = QtGui.QAction("Run selected addons", self)
                run_addons_action.triggered.connect(lambda: self.run_addons(wz_flag))
                menu.addAction(run_addons_action)

        # Create action for the properties dialog, this only works with maps ATM
        if addon_type == "/maps/" and self.check_addon(addon_path) != 2:
            properties_dialog_action = QtGui.QAction("Properties", self)
            properties_dialog_action.triggered.connect(lambda: PropertiesDialog(addon_path))
            menu.addAction(properties_dialog_action)

        # Display menu at the cursor position
        menu.exec_(QtGui.QCursor.pos())


def main():
    app = QtGui.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon("icon.png"))
    window = MainWindow()

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
