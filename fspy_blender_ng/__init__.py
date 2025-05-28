# fSpy Blender Importer
# Copyright (C) 2018-2025 Per Gantelius, yyc12345
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Load Blender core library.
import bpy

# Load or reload other modules.
if "bpy" in locals():
    import importlib
    if 'fspy' in locals():
        importlib.reload(fspy)  # type: ignore
    if 'fspy_importer' in locals():
        importlib.reload(fspy_importer)  # type: ignore
    if 'fspy_properties' in locals():
        importlib.reload(fspy_properties)  # type: ignore
    if 'fspy_panel' in locals():
        importlib.reload(fspy_panel)  # type: ignore

from . import fspy
from . import fspy_importer
from . import fspy_properties
from . import fspy_panel


def menu_func_import(self, context):
    self.layout.operator(fspy_importer.FSPYBLD_OT_import_fspy.bl_idname,
                         text="fSpy (.fspy)")


def register():
    fspy_properties.register()
    fspy_panel.register()
    fspy_importer.register()
    bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
    bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)
    fspy_importer.unregister()
    fspy_panel.unregister()
    fspy_properties.unregister()


if __name__ == "__main__":
    register()
