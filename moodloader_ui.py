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


from random import choice
from PyQt4 import QtGui

class MoodLoader(QtGui.QWidget):
    """
    This class contains the GUI for MoodLoader, it's meant to be imported
    and subclassed from a starter file. Note that the starter file must
    implement an '__init__()' method.
    """
    def center(self):
        """
        A little function to center the program window
        """
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def initUI(self):
        ### Make all the layouts ###
        main_vbox = QtGui.QVBoxLayout()
        addons_hbox = QtGui.QHBoxLayout()

        maps_vbox = QtGui.QVBoxLayout()
        cam_mods_vbox = QtGui.QVBoxLayout()
        global_mods_vbox = QtGui.QVBoxLayout()
        multiplayer_mods_vbox = QtGui.QVBoxLayout()

        game_options_vbox = QtGui.QVBoxLayout()
        game_options_hbox = QtGui.QHBoxLayout()


        ### Stylesheet for the addons QGroupBox's ###
        addons_stylesheet = "QGroupBox {border: 2px solid gray; font-family: Inconsolata; font-size: 21px; margin-top: .5em;} QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; padding:0 10px;}"


        ### Make status bar ###
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.showMessage("Ready")


        ### Make all the widgets ###

        # Header image is randomly chosen, 'choice()' is from the random module
        header_image = QtGui.QPixmap("addons-header-bg"+ choice(str(123)) + ".gif")
        header_image_label = QtGui.QLabel()
        header_image_label.setPixmap(header_image)

        # Map widgets
        self.install_map_button = QtGui.QPushButton("Install Map")
        maps_gbox = QtGui.QGroupBox("Maps")
        maps_gbox.setStyleSheet(addons_stylesheet)
        maps_gbox.setLayout(maps_vbox)

        # Campaign mod widgets
        self.install_cam_mod_button = QtGui.QPushButton("Install Campaign Mod")
        cam_mods_gbox = QtGui.QGroupBox("Campaign Mods")
        cam_mods_gbox.setStyleSheet(addons_stylesheet)
        cam_mods_gbox.setLayout(cam_mods_vbox)

        # Global mod widgets
        self.install_global_mod_button = QtGui.QPushButton("Install Global Mod")
        global_mods_gbox = QtGui.QGroupBox("Global Mods")
        global_mods_gbox.setStyleSheet(addons_stylesheet)
        global_mods_gbox.setLayout(global_mods_vbox)

        # Multiplayer mod widgets
        self.install_multiplayer_mod_button = QtGui.QPushButton("Install Multiplayer Mod")
        multiplayer_mods_gbox = QtGui.QGroupBox("Multiplayer Mods")
        multiplayer_mods_gbox.setStyleSheet(addons_stylesheet)
        multiplayer_mods_gbox.setLayout(multiplayer_mods_vbox)


        ### QListViews to display existing addons ###
        self.maps_listview = QtGui.QListView()
        self.map_data_model = QtGui.QStandardItemModel(self.maps_listview)
        self.maps_listview.setModel(self.map_data_model)
        self.maps_listview.setTextElideMode(2)
        self.maps_listview.setSelectionMode(3)

        self.cam_mods_listview = QtGui.QListView()
        self.cam_data_model = QtGui.QStandardItemModel(self.cam_mods_listview)
        self.cam_mods_listview.setModel(self.cam_data_model)
        self.cam_mods_listview.setTextElideMode(2)
        self.cam_mods_listview.setSelectionMode(3)

        self.global_mods_listview = QtGui.QListView()
        self.global_data_model = QtGui.QStandardItemModel(self.global_mods_listview)
        self.global_mods_listview.setModel(self.global_data_model)
        self.global_mods_listview.setTextElideMode(2)
        self.global_mods_listview.setSelectionMode(3)

        self.multiplayer_mods_listview = QtGui.QListView()
        self.multiplayer_data_model = QtGui.QStandardItemModel(self.multiplayer_mods_listview)
        self.multiplayer_mods_listview.setModel(self.multiplayer_data_model)
        self.multiplayer_mods_listview.setTextElideMode(2)
        self.multiplayer_mods_listview.setSelectionMode(3)

        # Game options widgets
        fullscreen_rb = QtGui.QRadioButton("Fullscreen")
        windowed_rb = QtGui.QRadioButton("Windowed")
        shadows_on_rb = QtGui.QRadioButton("Shadows On")
        shadows_off_rb = QtGui.QRadioButton("Shadows Off")
        shaders_on_rb = QtGui.QRadioButton("Shaders On")
        shaders_off_rb = QtGui.QRadioButton("Shaders Off")

        windowing_button_group = QtGui.QButtonGroup(game_options_hbox)
        shadows_button_group = QtGui.QButtonGroup(game_options_hbox)
        shaders_button_group = QtGui.QButtonGroup(game_options_hbox)

        windowing_button_group.addButton(fullscreen_rb)
        windowing_button_group.addButton(windowed_rb)
        shadows_button_group.addButton(shadows_on_rb)
        shadows_button_group.addButton(shadows_off_rb)
        shaders_button_group.addButton(shaders_on_rb)
        shaders_button_group.addButton(shaders_off_rb)

        game_options_gbox = QtGui.QGroupBox("Game Options")
        game_options_gbox.setStyleSheet(addons_stylesheet)
        game_options_gbox.setLayout(game_options_hbox)


        ### Pack everything ###

        # Pack mod buttons into their vbox's
        maps_vbox.insertSpacing(0, 10)
        maps_vbox.addWidget(self.install_map_button)
        maps_vbox.addWidget(self.maps_listview)

        cam_mods_vbox.insertSpacing(0, 10)
        cam_mods_vbox.addWidget(self.install_cam_mod_button)
        cam_mods_vbox.addWidget(self.cam_mods_listview)
        
        global_mods_vbox.insertSpacing(0, 10)
        global_mods_vbox.addWidget(self.install_global_mod_button)
        global_mods_vbox.addWidget(self.global_mods_listview)

        multiplayer_mods_vbox.insertSpacing(0, 10)
        multiplayer_mods_vbox.addWidget(self.install_multiplayer_mod_button)
        multiplayer_mods_vbox.addWidget(self.multiplayer_mods_listview)

        # Pack game options radio buttons
        game_options_hbox.addWidget(fullscreen_rb)
        game_options_hbox.addWidget(windowed_rb)
        game_options_hbox.addStretch()

        game_options_hbox.addWidget(shadows_on_rb)
        game_options_hbox.addWidget(shadows_off_rb)
        game_options_hbox.addStretch()

        game_options_hbox.addWidget(shaders_on_rb)
        game_options_hbox.addWidget(shaders_off_rb)

        # Pack group boxes into the main 'addons_hbox'
        addons_hbox.addWidget(maps_gbox)
        addons_hbox.addWidget(cam_mods_gbox)
        addons_hbox.addWidget(global_mods_gbox)
        addons_hbox.addWidget(multiplayer_mods_gbox)

        # Pack everything into 'main_vbox'
        main_vbox.addWidget(header_image_label)
        main_vbox.addLayout(addons_hbox)
        main_vbox.addStretch()
        main_vbox.addWidget(game_options_gbox)
        main_vbox.addWidget(self.statusbar)


        self.setLayout(main_vbox)
        self.setWindowTitle("Warzone 2100 Mood Loader")
        self.resize(800, 600)
        self.center()
        self.show()
