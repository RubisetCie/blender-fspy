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

import json
import struct
import enum
import pathlib
import typing


TransformMatrixRow = tuple[float, float, float, float]
TransformMatrix = tuple[TransformMatrixRow, TransformMatrixRow, TransformMatrixRow, TransformMatrixRow]


class ParseError(Exception):
    pass


class ReferenceDistanceUnit(enum.StrEnum):
    MILLIMETERS = 'Millimeters'
    CENTIMETERS = 'Centimeters'
    METERS = 'Meters'
    KILOMETERS = 'Kilometers'
    INCHES = 'Inches'
    FEET = 'Feet'
    MILES = 'Miles'


class CameraParameters:
    principal_point: tuple[float, float]
    fov_horiz: float
    camera_transfrom: TransformMatrix
    image_width: int
    image_height: int

    def __init__(self, json_camera_parameters: dict[str, typing.Any]) -> None:
        json_principal_point: dict[str, float] = json_camera_parameters['principalPoint']
        self.principal_point = (json_principal_point['x'], json_principal_point['y'])
        self.fov_horiz = json_camera_parameters['horizontalFieldOfView']
        json_camera_transform: dict[str, list[list[float]]] = json_camera_parameters['cameraTransform']
        self.camera_transfrom = tuple(map(lambda v: tuple(v), json_camera_transform['rows'])) # type: ignore
        self.image_width = json_camera_parameters['imageWidth']
        self.image_height = json_camera_parameters['imageHeight']


class Project:
    MAGIC_WORD: typing.ClassVar[bytes] = b'fspy'
    FILE_VER: typing.ClassVar[int] = 1
    FILE_VER_PACKER: typing.ClassVar[struct.Struct] = struct.Struct('<I')
    PART_SIZE_PACKER: typing.ClassVar[struct.Struct] = struct.Struct('<II')

    file_name: str
    image_data: bytes
    camera_parameters: CameraParameters
    reference_distance_unit: ReferenceDistanceUnit

    def __init__(self, project_file_path: str) -> None:
        # Setup file name and open file.
        self.file_name = pathlib.Path(project_file_path).name
        with open(project_file_path, 'rb') as project_file:
            # Check magic word at file header.
            gotten_magic_word = project_file.read(len(Project.MAGIC_WORD))
            if gotten_magic_word != Project.MAGIC_WORD:
                raise ParseError('Trying to import a file that is not an fSpy project')

            # Check file version
            gotten_file_ver: int
            (gotten_file_ver, ) = Project.FILE_VER_PACKER.unpack(
                project_file.read(Project.FILE_VER_PACKER.size))
            if gotten_file_ver != Project.FILE_VER:
                raise ParseError(f'Unsupported fSpy project file version {gotten_file_ver}')
            
            # Extract size info
            state_string_size: int
            image_buffer_size: int
            (state_string_size, image_buffer_size) = Project.PART_SIZE_PACKER.unpack(
                 project_file.read(Project.PART_SIZE_PACKER.size))
            if image_buffer_size == 0:
                raise ParseError('Trying to import an fSpy project with no image data')
            
            # Read 2 parts respectively
            state_string: dict[str, typing.Any] = json.loads(project_file.read(state_string_size))
            image_buffer = project_file.read(image_buffer_size)
            if len(image_buffer) != image_buffer_size:
                raise ParseError('Fail to read image data within given fSpy project')

            # Parse read state string
            # Fetch camera parameters
            json_camera_parameters: dict[str, typing.Any] | None = state_string['cameraParameters']
            if json_camera_parameters is None:
                raise ParseError('Trying to import an fSpy project without camera parameters')
            self.camera_parameters = CameraParameters(json_camera_parameters)
            # Fetch reference distance unit
            json_calibration_settings_base: dict[str, typing.Any] = state_string['calibrationSettingsBase']
            json_reference_distance_unit: str = json_calibration_settings_base['referenceDistanceUnit']
            self.reference_distance_unit = ReferenceDistanceUnit(json_reference_distance_unit)

            # Assign image data
            self.image_data = image_buffer
