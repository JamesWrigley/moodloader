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

import os
import re
import zipfile

"""
All the functions we need to get various information from an addon to display
in its properties dialog.
"""

def get_addon_type(addon_path):
    if "/maps/" in addon_path:
        return("Map")
    elif "/global/" in addon_path:
        return("Global Mod")
    elif "/campaign/" in addon_path:
        return("Campaign Mod")
    else:
        return("Multiplayer Mod")


def get_map_stats(addon_path):
    """
    Get a bunch of statistics from the map in 'addon_path'. ATM, this is
    limited to the number of oils on the map.
    """
    addon = zipfile.ZipFile(addon_path)
    addon_files = addon.namelist()

    # Get the max number of players
    player_count = re.search("\d+", os.path.basename(addon_path)).group()

    # Get the number of oils in the map, both total and per-player
    feature_ini_path = next(path for path in addon_files if "feature.ini" in path)
    total_oils = str(addon.read(feature_ini_path)).count("OilResource")
    oil_count_label = str(round(total_oils / int(player_count), 2)) + \
                      " (total: %s)" % total_oils
    return(oil_count_label)
