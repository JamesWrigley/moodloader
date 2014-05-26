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
        mods_hbox = QtGui.QHBoxLayout()

        maps_vbox = QtGui.QVBoxLayout()
        cam_mods_vbox = QtGui.QVBoxLayout()
        global_mods_vbox = QtGui.QVBoxLayout()

        game_options_vbox = QtGui.QVBoxLayout()
        game_options_hbox = QtGui.QHBoxLayout()


        ### Stylesheet for the mods QGroupBox's ###
        mods_stylesheet = "QGroupBox {border: 2px solid gray; font-family: Inconsolata; font-size: 21px; margin-top: .5em;} QGroupBox::title {subcontrol-origin: margin; subcontrol-position: top center; padding:0 10px;}"


        ### Make status bar ###
        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.showMessage("Ready")


        ### Generic button tooltips ###
        install_mod_tooltip = "Install a mod permanently"
        run_mod_tooltip = "Run a mod in a WZ session (will not install it)"


        ### Make all the widgets ###

        # Header image is randomly chosen, 'choice()' is from the random module
        header_image = QtGui.QPixmap("addons-header-bg"+ choice(str(123)) + ".gif")
        header_image_label = QtGui.QLabel()
        header_image_label.setPixmap(header_image)

        # Map widgets
        self.install_map_button = QtGui.QPushButton("Install Map")
        self.install_map_button.setToolTip(install_mod_tooltip)
        self.run_map_button = QtGui.QPushButton("Run Map")
        self.run_map_button.setToolTip(run_mod_tooltip)
        maps_gbox = QtGui.QGroupBox("Maps")
        maps_gbox.setStyleSheet(mods_stylesheet)
        maps_gbox.setLayout(maps_vbox)

        # Campaign mod widgets
        self.install_cam_mod_button = QtGui.QPushButton("Install Campaign Mod")
        self.install_cam_mod_button.setToolTip(install_mod_tooltip)
        run_cam_mod_button = QtGui.QPushButton("Run Campaign Mod")
        run_cam_mod_button.setToolTip(run_mod_tooltip)
        cam_mod_gbox = QtGui.QGroupBox("Campaign Mods")
        cam_mod_gbox.setStyleSheet(mods_stylesheet)
        cam_mod_gbox.setLayout(cam_mods_vbox)

        # Global mod widgets
        self.install_global_mod_button = QtGui.QPushButton("Install Global Mod")
        self.install_global_mod_button.setToolTip(install_mod_tooltip)
        run_global_mod_button = QtGui.QPushButton("Run Global Mod")
        run_global_mod_button.setToolTip(run_mod_tooltip)
        global_mod_gbox = QtGui.QGroupBox("Global Mods")
        global_mod_gbox.setStyleSheet(mods_stylesheet)
        global_mod_gbox.setLayout(global_mods_vbox)


        ### QListViews to display existing mods ###
        self.map_mods_listview = QtGui.QListView()
        self.map_data_model = QtGui.QStandardItemModel(self.map_mods_listview)
        self.map_mods_listview.setModel(self.map_data_model)
        self.map_mods_listview.setTextElideMode(2)

        self.cam_mods_listview = QtGui.QListView()
        self.cam_data_model = QtGui.QStandardItemModel(self.cam_mods_listview)
        self.cam_mods_listview.setModel(self.cam_data_model)
        self.cam_mods_listview.setTextElideMode(2)

        self.global_mods_listview = QtGui.QListView()
        self.global_data_model = QtGui.QStandardItemModel(self.global_mods_listview)
        self.global_mods_listview.setModel(self.global_data_model)
        self.global_mods_listview.setTextElideMode(2)

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
        game_options_gbox.setStyleSheet(mods_stylesheet)
        game_options_gbox.setLayout(game_options_hbox)


        ### Pack everything ###

        # Pack mod buttons into their vbox's
        maps_vbox.insertSpacing(0, 10)
        maps_vbox.addWidget(self.install_map_button)
        maps_vbox.addWidget(self.run_map_button)
        maps_vbox.addWidget(self.map_mods_listview)

        cam_mods_vbox.insertSpacing(0, 10)
        cam_mods_vbox.addWidget(self.install_cam_mod_button)
        cam_mods_vbox.addWidget(run_cam_mod_button)
        cam_mods_vbox.addWidget(self.cam_mods_listview)
        
        global_mods_vbox.insertSpacing(0, 10)
        global_mods_vbox.addWidget(self.install_global_mod_button)
        global_mods_vbox.addWidget(run_global_mod_button)
        global_mods_vbox.addWidget(self.global_mods_listview)

        # Pack game options radio buttons, note the deplorable 'addStretch()'s
        game_options_hbox.addWidget(fullscreen_rb)
        game_options_hbox.addWidget(windowed_rb)
        game_options_hbox.addStretch()

        game_options_hbox.addWidget(shadows_on_rb)
        game_options_hbox.addWidget(shadows_off_rb)
        game_options_hbox.addStretch()

        game_options_hbox.addWidget(shaders_on_rb)
        game_options_hbox.addWidget(shaders_off_rb)

        # Pack group boxes into the main 'mods_hbox'
        mods_hbox.addWidget(maps_gbox)
        mods_hbox.addWidget(cam_mod_gbox)
        mods_hbox.addWidget(global_mod_gbox)

        # Pack everything into 'main_vbox'
        main_vbox.addWidget(header_image_label)
        main_vbox.addLayout(mods_hbox)
        main_vbox.addStretch()
        main_vbox.addWidget(game_options_gbox)
        main_vbox.addWidget(self.statusbar)


        self.setLayout(main_vbox)
        self.setWindowTitle("Warzone 2100 Mood Loader")
        self.resize(800, 600)
        self.center()
        self.show()
