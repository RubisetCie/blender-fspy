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

import bpy
import mathutils
import bpy_extras.io_utils
import tempfile
import pathlib
import typing
from . import fspy
from . import fspy_properties

class FSPYBLD_OT_import_fspy(bpy.types.Operator, bpy_extras.io_utils.ImportHelper):
    """Imports the background image and camera parameters from an fSpy project file"""
    bl_idname = "fspybld.import_fspy"
    bl_label = "Import fSpy project file"
    bl_options = {'PRESET', 'UNDO'}

    filename_ext=".fspy"
    filter_glob: bpy.props.StringProperty(
        default="*.fspy",
        options={'HIDDEN'},
        maxlen=255
    ) # type: ignore

    update_existing_camera: bpy.props.BoolProperty(
        name="Update Existing Import",
        description="If a camera and background image matching the project file name already exist, update them instead of creating new objects",
        default=True
    ) # type: ignore

    import_background_image: bpy.props.BoolProperty(
        name="Import Background Image",
        description="Set the image from the fSpy project file as the camera background image",
        default=True
    ) # type: ignore

    def get_file_path(self) -> str:
        return self.filepath # type: ignore

    def execute(self, context):
        # Try loading fSpy project first
        try:
            project = fspy.Project(self.get_file_path())
        except fspy.ParseError as e:
            self.report({'ERROR'}, f'Can not load fSpy project file: {e}')
            return {'CANCELLED'}

        # Perform importing
        camera = find_or_create_camera(project, self.update_existing_camera)
        setup_camera(project, camera)
        set_render_resolution(project)
        setup_3d_area(project, camera, self.update_existing_camera, self.import_background_image)
        set_reference_distance_unit(project, camera)

        # Show finish message
        self.report({'INFO'}, f'Finished setting up camera "{project.file_name}"')
        return {'FINISHED'}


class ImporterError(Exception):
    pass


def add_into_scene(instance: bpy.types.Object) -> None:
    """
    Add given Blender object into active scene.
    """
    view_layer = bpy.context.view_layer
    collection = view_layer.active_layer_collection.collection # type: ignore
    collection.objects.link(instance)


def select_object(instance: bpy.types.Object) -> None:
    """
    Set given object as active object and the only selected object.
    """
    # Deselect all first
    bpy.ops.object.select_all(action = 'DESELECT')
    # Select self and set self as active object
    instance.select_set(True)
    bpy.context.view_layer.objects.active = instance


def find_or_create_camera(project: fspy.Project, update_existing_camera: bool) -> bpy.types.Object:
    """
    Finds or creates a suitable camera in Blender.
    """
    # Find existing camera
    camera_name = project.file_name
    camera_object: bpy.types.Object | None = bpy.data.objects.get(camera_name, None)

    # If there is no existing camera, create new.
    if camera_object is None: pass
    # If user do not need update current camera, create new.
    elif not update_existing_camera: camera_object = None
    # If existing camera object is not camera, create new.
    elif camera_object.type != 'CAMERA': camera_object = None
    # Okey, use existing one.
    else: pass

    # Create new camera if necessary
    if camera_object is None:
        # Set the camera name to match the name of the project file
        camera_data = bpy.data.cameras.new(camera_name)
        camera_object = bpy.data.objects.new(camera_name, camera_data)
        # Add into active scene
        add_into_scene(camera_object)

    # Select fetched camera
    select_object(camera_object)

    # Return fetched camera
    return camera_object


def setup_camera(project: fspy.Project, camera: bpy.types.Object) -> None:
    """
    Set camera parameters
    """
    camera_parameters = project.camera_parameters
    camera_data = typing.cast(bpy.types.Camera, camera.data)

    # Set field of view
    camera_data.type = 'PERSP'
    camera_data.lens_unit = 'FOV'
    camera_data.angle = camera_parameters.fov_horiz

    # Set camera transform
    camera.matrix_world = mathutils.Matrix(camera_parameters.camera_transfrom)

    # Set camera shift (aka principal point)
    x_shift_scale = 1
    y_shift_scale = 1
    if camera_parameters.image_height > camera_parameters.image_width:
        x_shift_scale = camera_parameters.image_width / camera_parameters.image_height
    else:
        y_shift_scale = camera_parameters.image_height / camera_parameters.image_width

    pp = camera_parameters.principal_point
    pp_rel: tuple[float, float] = (0, 0)
    image_aspect: float = camera_parameters.image_width / camera_parameters.image_height
    if image_aspect <= 1:
        pp_rel = (0.5 * (pp[0] / image_aspect + 1), 0.5 * (-pp[1] + 1))
    else:
        pp_rel = (0.5 * (pp[0] + 1), 0.5 * (-pp[1] * image_aspect + 1))
    camera_data.shift_x = x_shift_scale * (0.5 - pp_rel[0])
    camera_data.shift_y = y_shift_scale * (-0.5 + pp_rel[1])

    camera_properties = fspy_properties.FspyProperties()
    camera_properties.fspy_imported = True
    camera_properties.image_resolution = (
        camera_parameters.image_width,
        camera_parameters.image_height
    )
    fspy_properties.set_fspy_properties(camera_data, camera_properties)


def set_render_resolution(project: fspy.Project) -> None:
    """
    Sets the render resolution to match the project image
    """
    render_settings = bpy.context.scene.render
    render_settings.resolution_x = project.camera_parameters.image_width
    render_settings.resolution_y = project.camera_parameters.image_height


def find_or_create_image(
        project: fspy.Project, bg_images: bpy.types.CameraBackgroundImages,
        update_existing_camera: bool) -> bpy.types.CameraBackgroundImage:
    """
    Find or create new image slot for camera background images.
    """
    # Find existing image in background image collection.
    image_name = project.file_name
    existing_bg_image: bpy.types.CameraBackgroundImage | None = None

    # Only perform finding if "update existing camera" requested
    if update_existing_camera:
        for bg_image in bg_images:
            inner = bg_image.image
            if inner is None:
                continue
            if inner.name == image_name:
                # We found image we expected.
                # Clear its associated image so that we can have a new image with same name.
                bg_image.image = None
                bpy.data.images.remove(inner)
                # And set it for return value.
                existing_bg_image = bg_image
                break

    # Create new image slot if necessary.
    if existing_bg_image is None:
        existing_bg_image = bg_images.new()

    return existing_bg_image


def load_fspy_image_data(project: fspy.Project) -> bpy.types.Image:
    """
    Load fSpy project file stored image data into Blender safely.
    """
    # Create a temporary folder for loading.
    with tempfile.TemporaryDirectory() as temp_folder:
        # Write project image data to a temp file
        temp_file = pathlib.Path(temp_folder) / 'fspy-temp-image'
        with temp_file.open('wb') as temp_file_writer:
            temp_file_writer.write(project.image_data)

        # Load background image data from temp file
        image = bpy.data.images.load(str(temp_file))
        image.name = project.file_name
        # And immediately pack it into Blender file
        # because original file will be deleted when leaving this `with`.
        image.pack()

    return image


def setup_3d_area(project: fspy.Project, camera: bpy.types.Object,
                  update_existing_camera: bool,
                  import_background_image: bool) -> None:
    # Find the first 3D view area and set its background image
    def find_first_3d_view_area() -> bpy.types.SpaceView3D | None:
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                return typing.cast(bpy.types.SpaceView3D | None, area.spaces.active)
        return None

    space_data = find_first_3d_view_area()
    if space_data is None: return
    camera_data = typing.cast(bpy.types.Camera, camera.data)

    # Show background images
    camera_data.show_background_images = True

    # Make the calibrated camera the active camera
    space_data.camera = camera
    space_data.region_3d.view_perspective = 'CAMERA'

    # Set camera background image
    if import_background_image:
        # Get background image slots
        bg_images = camera_data.background_images

        # Setting background image has been requested.
        # First, hide all existing bg images
        for bg_image in bg_images:
            bg_image.show_background_image = False

        # Try to find an existing bg image slot matching the project name
        # or create new one if necessary
        bg_image = find_or_create_image(project, bg_images, update_existing_camera)

        # Make sure the background image slot is visible
        bg_image.show_background_image = True

        # Load project image into background
        bg_image.image = load_fspy_image_data(project)


def set_reference_distance_unit(project: fspy.Project,
                                camera: bpy.types.Object) -> None:
    scene = bpy.context.scene
    unit_settings = scene.unit_settings

    is_imperial = False
    blender_unit = None
    scale_length = None
    match project.reference_distance_unit:
        case fspy.ReferenceDistanceUnit.MILLIMETERS:
            blender_unit = 'MILLIMETERS'
            scale_length = 0.001
        case fspy.ReferenceDistanceUnit.CENTIMETERS:
            blender_unit = 'CENTIMETERS'
            scale_length = 0.01
        case fspy.ReferenceDistanceUnit.METERS:
            blender_unit = 'METERS'
            scale_length = 1.0
        case fspy.ReferenceDistanceUnit.KILOMETERS:
            blender_unit = 'KILOMETERS'
            scale_length = 1000.0
        case fspy.ReferenceDistanceUnit.INCHES:
            blender_unit = 'INCHES'
            scale_length = 1.0 / 12.0
            is_imperial = True
        case fspy.ReferenceDistanceUnit.FEET:
            blender_unit = 'FEET'
            scale_length = 1.0
            is_imperial = True
        case fspy.ReferenceDistanceUnit.MILES:
            blender_unit = 'MILES'
            scale_length = 5280.0
            is_imperial = True

    if blender_unit is not None:
        camera_distance_scale = 1.0
        if is_imperial:
            camera_distance_scale = 1.0 / 3.2808399
            unit_settings.system = 'IMPERIAL'
        else:
            unit_settings.system = 'METRIC'
        unit_settings.length_unit = blender_unit
        unit_settings.scale_length = scale_length
        camera.location *= camera_distance_scale
    else:
        unit_settings.system = 'NONE'
        unit_settings.scale_length = 1.0

def register():
    bpy.utils.register_class(FSPYBLD_OT_import_fspy)

def unregister():
    bpy.utils.unregister_class(FSPYBLD_OT_import_fspy)
