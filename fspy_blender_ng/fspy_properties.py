# fSpy Blender Importer
# Copyright (C) 2018-2025 Per Gantelius, Elie Michel, yyc12345
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

import bpy
import typing

FSPY_PROPERTIES_NAME: str = 'fspy'


class FSPYBLD_PG_fspy_properties(bpy.types.PropertyGroup):
    fspy_imported: bpy.props.BoolProperty(
        name="fSpy Imported",
        description=
        "True if this camera is fSpy imported and following fields have maening values.",
        default=False,
    )  # type: ignore

    image_resolution: bpy.props.IntVectorProperty(
        name="Image Resolution",
        description=
        "The resolution in pixels of the reference image that was used in fSpy",
        size=2,
        default=(0, 0),
        min=0,
    )  # type: ignore


def get_fspy_properties(camera: bpy.types.Camera) -> FSPYBLD_PG_fspy_properties:
    return typing.cast(FSPYBLD_PG_fspy_properties,
                       getattr(camera, FSPY_PROPERTIES_NAME))


def register():
    bpy.utils.register_class(FSPYBLD_PG_fspy_properties)
    setattr(bpy.types.Camera, FSPY_PROPERTIES_NAME,
            bpy.props.PointerProperty(type=FSPYBLD_PG_fspy_properties))


def unregister():
    delattr(bpy.types.Camera, FSPY_PROPERTIES_NAME)
    bpy.utils.unregister_class(FSPYBLD_PG_fspy_properties)
