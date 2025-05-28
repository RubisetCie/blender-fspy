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
from . import fspy_properties


class FSPYBLD_PT_fspy_properties(bpy.types.Panel):
    bl_label = "fSpy"
    bl_idname = "FSPYBLD_PT_fspy_properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    @classmethod
    def poll(cls, context):
        camera = context.camera
        if camera is None:
            return False

        camera_properties = fspy_properties.get_fspy_properties(camera)
        if not camera_properties.fspy_imported:
            return False

        return True

    def draw(self, context):
        layout = self.layout

        # Show operators
        layout.operator(FSPYBLD_OT_set_render_resolution.bl_idname)

        # Show parameters
        layout = layout.row()
        layout.enabled = False
        layout.use_property_split = True
        camera = typing.cast(bpy.types.Camera, context.camera)
        camera_properties = fspy_properties.get_fspy_properties(camera)
        layout.prop(camera_properties, 'image_resolution')


class FSPYBLD_OT_set_render_resolution(bpy.types.Operator):
    # TODO: bad description
    """
    Set the resolution of the render to the resolution of the
    reference image that was used for this camera.
    """
    bl_idname = "fspybld.set_render_resolution"
    bl_label = "Set Render Resolution"

    @classmethod
    def poll(cls, context):
        camera = context.camera
        if camera is None:
            return False

        camera_properties = fspy_properties.get_fspy_properties(camera)
        if not camera_properties.fspy_imported:
            return False

        return True

    def execute(self, context):
        # TODO: fix bad code
        camera = typing.cast(bpy.types.Camera, context.camera)
        camera_properties = fspy_properties.get_fspy_properties(camera)
        render_settings = bpy.context.scene.render

        (w, h) = camera_properties.image_resolution
        render_settings.resolution_x = w
        render_settings.resolution_y = h
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FSPYBLD_OT_set_render_resolution)
    bpy.utils.register_class(FSPYBLD_PT_fspy_properties)


def unregister():
    bpy.utils.unregister_class(FSPYBLD_PT_fspy_properties)
    bpy.utils.unregister_class(FSPYBLD_OT_set_render_resolution)
