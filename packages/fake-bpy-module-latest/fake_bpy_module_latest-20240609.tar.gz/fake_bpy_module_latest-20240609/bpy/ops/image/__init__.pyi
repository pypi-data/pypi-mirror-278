import typing
import collections.abc
import bpy.types

GenericType1 = typing.TypeVar("GenericType1")
GenericType2 = typing.TypeVar("GenericType2")

def add_render_slot(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Add a new render slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def change_frame(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    frame: typing.Any | None = 0,
):
    """Interactively change the current frame number

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param frame: Frame
    :type frame: typing.Any | None
    """

    ...

def clear_render_border(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear the boundaries of the render region and disable render region

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def clear_render_slot(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Clear the currently selected render slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def clipboard_copy(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Copy the image to the clipboard

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def clipboard_paste(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Paste new image from the clipboard

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def convert_to_mesh_plane(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    interpolation: str | None = "Linear",
    extension: str | None = "CLIP",
    alpha_mode: str | None = "STRAIGHT",
    use_auto_refresh: bool | typing.Any | None = True,
    relative: bool | typing.Any | None = True,
    shader: str | None = "PRINCIPLED",
    emit_strength: typing.Any | None = 1.0,
    use_transparency: bool | typing.Any | None = True,
    blend_method: str | None = "BLEND",
    shadow_method: str | None = "CLIP",
    use_backface_culling: bool | typing.Any | None = False,
    show_transparent_back: bool | typing.Any | None = True,
    overwrite_material: bool | typing.Any | None = True,
    name_from: str | None = "OBJECT",
    delete_ref: bool | typing.Any | None = True,
):
    """Convert selected reference images to textured mesh plane

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param interpolation: Interpolation, Texture interpolation

    Linear
    Linear -- Linear interpolation.

    Closest
    Closest -- No interpolation (sample closest texel).

    Cubic
    Cubic -- Cubic interpolation.

    Smart
    Smart -- Bicubic when magnifying, else bilinear (OSL only).
        :type interpolation: str | None
        :param extension: Extension, How the image is extrapolated past its original bounds

    CLIP
    Clip -- Clip to image size and set exterior pixels as transparent.

    EXTEND
    Extend -- Extend by repeating edge pixels of the image.

    REPEAT
    Repeat -- Cause the image to repeat horizontally and vertically.
        :type extension: str | None
        :param alpha_mode: Alpha Mode, Representation of alpha in the image file, to convert to and from when saving and loading the image

    STRAIGHT
    Straight -- Store RGB and alpha channels separately with alpha acting as a mask, also known as unassociated alpha. Commonly used by image editing applications and file formats like PNG.

    PREMUL
    Premultiplied -- Store RGB channels with alpha multiplied in, also known as associated alpha. The natural format for renders and used by file formats like OpenEXR.

    CHANNEL_PACKED
    Channel Packed -- Different images are packed in the RGB and alpha channels, and they should not affect each other. Channel packing is commonly used by game engines to save memory.

    NONE
    None -- Ignore alpha channel from the file and make image fully opaque.
        :type alpha_mode: str | None
        :param use_auto_refresh: Auto Refresh, Always refresh image on frame changes
        :type use_auto_refresh: bool | typing.Any | None
        :param relative: Relative Paths, Use relative file paths
        :type relative: bool | typing.Any | None
        :param shader: Shader, Node shader to use

    PRINCIPLED
    Principled -- Principled shader.

    SHADELESS
    Shadeless -- Only visible to camera and reflections.

    EMISSION
    Emission -- Emission shader.
        :type shader: str | None
        :param emit_strength: Emission Strength, Strength of emission
        :type emit_strength: typing.Any | None
        :param use_transparency: Use Alpha, Use alpha channel for transparency
        :type use_transparency: bool | typing.Any | None
        :param blend_method: Blend Mode, Blend Mode for Transparent Faces

    BLEND
    Blend -- Render polygon transparent, depending on alpha channel of the texture.

    CLIP
    Clip -- Use the alpha threshold to clip the visibility (binary visibility).

    HASHED
    Hashed -- Use noise to dither the binary visibility (works well with multi-samples).

    OPAQUE
    Opaque -- Render surface without transparency.
        :type blend_method: str | None
        :param shadow_method: Shadow Mode, Shadow mapping method

    CLIP
    Clip -- Use the alpha threshold to clip the visibility (binary visibility).

    HASHED
    Hashed -- Use noise to dither the binary visibility (works well with multi-samples).

    OPAQUE
    Opaque -- Material will cast shadows without transparency.

    NONE
    None -- Material will cast no shadow.
        :type shadow_method: str | None
        :param use_backface_culling: Backface Culling, Use backface culling to hide the back side of faces
        :type use_backface_culling: bool | typing.Any | None
        :param show_transparent_back: Show Backface, Render multiple transparent layers (may introduce transparency sorting problems)
        :type show_transparent_back: bool | typing.Any | None
        :param overwrite_material: Overwrite Material, Overwrite existing material with the same name
        :type overwrite_material: bool | typing.Any | None
        :param name_from: Name After, Name for new mesh object and material

    OBJECT
    Source Object -- Name after object source with a suffix.

    IMAGE
    Source Image -- name from laoded image.
        :type name_from: str | None
        :param delete_ref: Delete Reference Object, Delete empty image object once mesh plane is created
        :type delete_ref: bool | typing.Any | None
    """

    ...

def curves_point_set(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    point: str | None = "BLACK_POINT",
    size: typing.Any | None = 1,
):
    """Set black point or white point for curves

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param point: Point, Set black point or white point for curves
    :type point: str | None
    :param size: Sample Size
    :type size: typing.Any | None
    """

    ...

def cycle_render_slot(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    reverse: bool | typing.Any | None = False,
):
    """Cycle through all non-void render slots

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param reverse: Cycle in Reverse
    :type reverse: bool | typing.Any | None
    """

    ...

def external_edit(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str | typing.Any = "",
):
    """Edit image in an external application

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param filepath: filepath
    :type filepath: str | typing.Any
    """

    ...

def file_browse(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str | typing.Any = "",
    hide_props_region: bool | typing.Any | None = True,
    check_existing: bool | typing.Any | None = False,
    filter_blender: bool | typing.Any | None = False,
    filter_backup: bool | typing.Any | None = False,
    filter_image: bool | typing.Any | None = True,
    filter_movie: bool | typing.Any | None = True,
    filter_python: bool | typing.Any | None = False,
    filter_font: bool | typing.Any | None = False,
    filter_sound: bool | typing.Any | None = False,
    filter_text: bool | typing.Any | None = False,
    filter_archive: bool | typing.Any | None = False,
    filter_btx: bool | typing.Any | None = False,
    filter_collada: bool | typing.Any | None = False,
    filter_alembic: bool | typing.Any | None = False,
    filter_usd: bool | typing.Any | None = False,
    filter_obj: bool | typing.Any | None = False,
    filter_volume: bool | typing.Any | None = False,
    filter_folder: bool | typing.Any | None = True,
    filter_blenlib: bool | typing.Any | None = False,
    filemode: typing.Any | None = 9,
    relative_path: bool | typing.Any | None = True,
    show_multiview: bool | typing.Any | None = False,
    use_multiview: bool | typing.Any | None = False,
    display_type: str | None = "DEFAULT",
    sort_method: str | None = "",
):
    """Open an image file browser, hold Shift to open the file, Alt to browse containing directory

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str | typing.Any
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | typing.Any | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | typing.Any | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | typing.Any | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | typing.Any | None
        :param filter_image: Filter image files
        :type filter_image: bool | typing.Any | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | typing.Any | None
        :param filter_python: Filter Python files
        :type filter_python: bool | typing.Any | None
        :param filter_font: Filter font files
        :type filter_font: bool | typing.Any | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | typing.Any | None
        :param filter_text: Filter text files
        :type filter_text: bool | typing.Any | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | typing.Any | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | typing.Any | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | typing.Any | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | typing.Any | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | typing.Any | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | typing.Any | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | typing.Any | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | typing.Any | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | typing.Any | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | typing.Any | None
        :param show_multiview: Enable Multi-View
        :type show_multiview: bool | typing.Any | None
        :param use_multiview: Use Multi-View
        :type use_multiview: bool | typing.Any | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: str | None
        :param sort_method: File sorting mode
        :type sort_method: str | None
    """

    ...

def flip(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    use_flip_x: bool | typing.Any | None = False,
    use_flip_y: bool | typing.Any | None = False,
):
    """Flip the image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param use_flip_x: Horizontal, Flip the image horizontally
    :type use_flip_x: bool | typing.Any | None
    :param use_flip_y: Vertical, Flip the image vertically
    :type use_flip_y: bool | typing.Any | None
    """

    ...

def import_as_mesh_planes(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    interpolation: str | None = "Linear",
    extension: str | None = "CLIP",
    alpha_mode: str | None = "STRAIGHT",
    use_auto_refresh: bool | typing.Any | None = True,
    relative: bool | typing.Any | None = True,
    shader: str | None = "PRINCIPLED",
    emit_strength: typing.Any | None = 1.0,
    use_transparency: bool | typing.Any | None = True,
    blend_method: str | None = "BLEND",
    shadow_method: str | None = "CLIP",
    use_backface_culling: bool | typing.Any | None = False,
    show_transparent_back: bool | typing.Any | None = True,
    overwrite_material: bool | typing.Any | None = True,
    filepath: str | typing.Any = "",
    align: str | None = "WORLD",
    location: typing.Any | None = (0.0, 0.0, 0.0),
    rotation: typing.Any | None = (0.0, 0.0, 0.0),
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    directory: str | typing.Any = "",
    filter_image: bool | typing.Any | None = True,
    filter_movie: bool | typing.Any | None = True,
    filter_folder: bool | typing.Any | None = True,
    force_reload: bool | typing.Any | None = False,
    image_sequence: bool | typing.Any | None = False,
    offset: bool | typing.Any | None = True,
    offset_axis: str | None = "+X",
    offset_amount: typing.Any | None = 0.1,
    align_axis: str | None = "CAM_AX",
    prev_align_axis: str | None = "NONE",
    align_track: bool | typing.Any | None = False,
    size_mode: str | None = "ABSOLUTE",
    fill_mode: str | None = "FILL",
    height: typing.Any | None = 1.0,
    factor: typing.Any | None = 600.0,
):
    """Create mesh plane(s) from image files with the appropriate aspect ratio

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param interpolation: Interpolation, Texture interpolation

    Linear
    Linear -- Linear interpolation.

    Closest
    Closest -- No interpolation (sample closest texel).

    Cubic
    Cubic -- Cubic interpolation.

    Smart
    Smart -- Bicubic when magnifying, else bilinear (OSL only).
        :type interpolation: str | None
        :param extension: Extension, How the image is extrapolated past its original bounds

    CLIP
    Clip -- Clip to image size and set exterior pixels as transparent.

    EXTEND
    Extend -- Extend by repeating edge pixels of the image.

    REPEAT
    Repeat -- Cause the image to repeat horizontally and vertically.
        :type extension: str | None
        :param alpha_mode: Alpha Mode, Representation of alpha in the image file, to convert to and from when saving and loading the image

    STRAIGHT
    Straight -- Store RGB and alpha channels separately with alpha acting as a mask, also known as unassociated alpha. Commonly used by image editing applications and file formats like PNG.

    PREMUL
    Premultiplied -- Store RGB channels with alpha multiplied in, also known as associated alpha. The natural format for renders and used by file formats like OpenEXR.

    CHANNEL_PACKED
    Channel Packed -- Different images are packed in the RGB and alpha channels, and they should not affect each other. Channel packing is commonly used by game engines to save memory.

    NONE
    None -- Ignore alpha channel from the file and make image fully opaque.
        :type alpha_mode: str | None
        :param use_auto_refresh: Auto Refresh, Always refresh image on frame changes
        :type use_auto_refresh: bool | typing.Any | None
        :param relative: Relative Paths, Use relative file paths
        :type relative: bool | typing.Any | None
        :param shader: Shader, Node shader to use

    PRINCIPLED
    Principled -- Principled shader.

    SHADELESS
    Shadeless -- Only visible to camera and reflections.

    EMISSION
    Emission -- Emission shader.
        :type shader: str | None
        :param emit_strength: Emission Strength, Strength of emission
        :type emit_strength: typing.Any | None
        :param use_transparency: Use Alpha, Use alpha channel for transparency
        :type use_transparency: bool | typing.Any | None
        :param blend_method: Blend Mode, Blend Mode for Transparent Faces

    BLEND
    Blend -- Render polygon transparent, depending on alpha channel of the texture.

    CLIP
    Clip -- Use the alpha threshold to clip the visibility (binary visibility).

    HASHED
    Hashed -- Use noise to dither the binary visibility (works well with multi-samples).

    OPAQUE
    Opaque -- Render surface without transparency.
        :type blend_method: str | None
        :param shadow_method: Shadow Mode, Shadow mapping method

    CLIP
    Clip -- Use the alpha threshold to clip the visibility (binary visibility).

    HASHED
    Hashed -- Use noise to dither the binary visibility (works well with multi-samples).

    OPAQUE
    Opaque -- Material will cast shadows without transparency.

    NONE
    None -- Material will cast no shadow.
        :type shadow_method: str | None
        :param use_backface_culling: Backface Culling, Use backface culling to hide the back side of faces
        :type use_backface_culling: bool | typing.Any | None
        :param show_transparent_back: Show Backface, Render multiple transparent layers (may introduce transparency sorting problems)
        :type show_transparent_back: bool | typing.Any | None
        :param overwrite_material: Overwrite Material, Overwrite existing material with the same name
        :type overwrite_material: bool | typing.Any | None
        :param filepath: File Path, Filepath used for importing the file
        :type filepath: str | typing.Any
        :param align: Align

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :type align: str | None
        :param location: Location
        :type location: typing.Any | None
        :param rotation: Rotation
        :type rotation: typing.Any | None
        :param files: files
        :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
        :param directory: directory
        :type directory: str | typing.Any
        :param filter_image: filter_image
        :type filter_image: bool | typing.Any | None
        :param filter_movie: filter_movie
        :type filter_movie: bool | typing.Any | None
        :param filter_folder: filter_folder
        :type filter_folder: bool | typing.Any | None
        :param force_reload: Force Reload, Force reload the image if it is already opened elsewhere in Blender
        :type force_reload: bool | typing.Any | None
        :param image_sequence: Detect Image Sequences, Import sequentially numbered images as an animated image sequence instead of separate planes
        :type image_sequence: bool | typing.Any | None
        :param offset: Offset Planes, Offset planes from each other. If disabled, multiple planes will be created at the same location
        :type offset: bool | typing.Any | None
        :param offset_axis: Offset Direction, How planes are oriented relative to each others' local axis

    +X
    +X -- Side by Side to the Left.

    +Y
    +Y -- Side by Side, Downward.

    +Z
    +Z -- Stacked Above.

    -X
    -X -- Side by Side to the Right.

    -Y
    -Y -- Side by Side, Upward.

    -Z
    -Z -- Stacked Below.
        :type offset_axis: str | None
        :param offset_amount: Offset Distance, Set distance between each plane
        :type offset_amount: typing.Any | None
        :param align_axis: Align, How to align the planes

    +X
    +X -- Facing positive X.

    +Y
    +Y -- Facing positive Y.

    +Z
    +Z -- Facing positive Z.

    -X
    -X -- Facing negative X.

    -Y
    -Y -- Facing negative Y.

    -Z
    -Z -- Facing negative Z.

    CAM
    Face Camera -- Facing camera.

    CAM_AX
    Camera's Main Axis -- Facing the camera's dominant axis.
        :type align_axis: str | None
        :param prev_align_axis: prev_align_axis

    +X
    +X -- Facing positive X.

    +Y
    +Y -- Facing positive Y.

    +Z
    +Z -- Facing positive Z.

    -X
    -X -- Facing negative X.

    -Y
    -Y -- Facing negative Y.

    -Z
    -Z -- Facing negative Z.

    CAM
    Face Camera -- Facing camera.

    CAM_AX
    Camera's Main Axis -- Facing the camera's dominant axis.

    NONE
    Undocumented.
        :type prev_align_axis: str | None
        :param align_track: Track Camera, Add a constraint to make the planes track the camera
        :type align_track: bool | typing.Any | None
        :param size_mode: Size Mode, Method for computing the plane size

    ABSOLUTE
    Absolute -- Use absolute size.

    CAMERA
    Scale to Camera Frame -- Scale to fit or fill the camera frame.

    DPI
    Pixels per Inch -- Scale based on pixels per inch.

    DPBU
    Pixels per Blender Unit -- Scale based on pixels per Blender Unit.
        :type size_mode: str | None
        :param fill_mode: Scale, Method to scale the plane with the camera frame

    FILL
    Fill -- Fill camera frame, spilling outside the frame.

    FIT
    Fit -- Fit entire image within the camera frame.
        :type fill_mode: str | None
        :param height: Height, Height of the created plane
        :type height: typing.Any | None
        :param factor: Definition, Number of pixels per inch or Blender Unit
        :type factor: typing.Any | None
    """

    ...

def invert(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    invert_r: bool | typing.Any | None = False,
    invert_g: bool | typing.Any | None = False,
    invert_b: bool | typing.Any | None = False,
    invert_a: bool | typing.Any | None = False,
):
    """Invert image's channels

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param invert_r: Red, Invert red channel
    :type invert_r: bool | typing.Any | None
    :param invert_g: Green, Invert green channel
    :type invert_g: bool | typing.Any | None
    :param invert_b: Blue, Invert blue channel
    :type invert_b: bool | typing.Any | None
    :param invert_a: Alpha, Invert alpha channel
    :type invert_a: bool | typing.Any | None
    """

    ...

def match_movie_length(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Set image's user's length to the one of this video

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def new(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    name: str | typing.Any = "Untitled",
    width: typing.Any | None = 1024,
    height: typing.Any | None = 1024,
    color: typing.Any | None = (0.0, 0.0, 0.0, 1.0),
    alpha: bool | typing.Any | None = True,
    generated_type: str | None = "BLANK",
    float: bool | typing.Any | None = False,
    use_stereo_3d: bool | typing.Any | None = False,
    tiled: bool | typing.Any | None = False,
):
    """Create a new image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param name: Name, Image data-block name
    :type name: str | typing.Any
    :param width: Width, Image width
    :type width: typing.Any | None
    :param height: Height, Image height
    :type height: typing.Any | None
    :param color: Color, Default fill color
    :type color: typing.Any | None
    :param alpha: Alpha, Create an image with an alpha channel
    :type alpha: bool | typing.Any | None
    :param generated_type: Generated Type, Fill the image with a grid for UV map testing
    :type generated_type: str | None
    :param float: 32-bit Float, Create image with 32-bit floating-point bit depth
    :type float: bool | typing.Any | None
    :param use_stereo_3d: Stereo 3D, Create an image with left and right views
    :type use_stereo_3d: bool | typing.Any | None
    :param tiled: Tiled, Create a tiled image
    :type tiled: bool | typing.Any | None
    """

    ...

def open(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    allow_path_tokens: bool | typing.Any | None = True,
    filepath: str | typing.Any = "",
    directory: str | typing.Any = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    hide_props_region: bool | typing.Any | None = True,
    check_existing: bool | typing.Any | None = False,
    filter_blender: bool | typing.Any | None = False,
    filter_backup: bool | typing.Any | None = False,
    filter_image: bool | typing.Any | None = True,
    filter_movie: bool | typing.Any | None = True,
    filter_python: bool | typing.Any | None = False,
    filter_font: bool | typing.Any | None = False,
    filter_sound: bool | typing.Any | None = False,
    filter_text: bool | typing.Any | None = False,
    filter_archive: bool | typing.Any | None = False,
    filter_btx: bool | typing.Any | None = False,
    filter_collada: bool | typing.Any | None = False,
    filter_alembic: bool | typing.Any | None = False,
    filter_usd: bool | typing.Any | None = False,
    filter_obj: bool | typing.Any | None = False,
    filter_volume: bool | typing.Any | None = False,
    filter_folder: bool | typing.Any | None = True,
    filter_blenlib: bool | typing.Any | None = False,
    filemode: typing.Any | None = 9,
    relative_path: bool | typing.Any | None = True,
    show_multiview: bool | typing.Any | None = False,
    use_multiview: bool | typing.Any | None = False,
    display_type: str | None = "DEFAULT",
    sort_method: str | None = "",
    use_sequence_detection: bool | typing.Any | None = True,
    use_udim_detecting: bool | typing.Any | None = True,
):
    """Open image

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param allow_path_tokens: Allow the path to contain substitution tokens
        :type allow_path_tokens: bool | typing.Any | None
        :param filepath: File Path, Path to file
        :type filepath: str | typing.Any
        :param directory: Directory, Directory of the file
        :type directory: str | typing.Any
        :param files: Files
        :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | typing.Any | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | typing.Any | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | typing.Any | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | typing.Any | None
        :param filter_image: Filter image files
        :type filter_image: bool | typing.Any | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | typing.Any | None
        :param filter_python: Filter Python files
        :type filter_python: bool | typing.Any | None
        :param filter_font: Filter font files
        :type filter_font: bool | typing.Any | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | typing.Any | None
        :param filter_text: Filter text files
        :type filter_text: bool | typing.Any | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | typing.Any | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | typing.Any | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | typing.Any | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | typing.Any | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | typing.Any | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | typing.Any | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | typing.Any | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | typing.Any | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | typing.Any | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | typing.Any | None
        :param show_multiview: Enable Multi-View
        :type show_multiview: bool | typing.Any | None
        :param use_multiview: Use Multi-View
        :type use_multiview: bool | typing.Any | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: str | None
        :param sort_method: File sorting mode
        :type sort_method: str | None
        :param use_sequence_detection: Detect Sequences, Automatically detect animated sequences in selected images (based on file names)
        :type use_sequence_detection: bool | typing.Any | None
        :param use_udim_detecting: Detect UDIMs, Detect selected UDIM files and load all matching tiles
        :type use_udim_detecting: bool | typing.Any | None
    """

    ...

def open_images(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    directory: str | typing.Any = "",
    files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
    | None = None,
    relative_path: bool | typing.Any | None = True,
    use_sequence_detection: bool | typing.Any | None = True,
    use_udim_detection: bool | typing.Any | None = True,
):
    """Undocumented, consider contributing.

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param directory: directory
    :type directory: str | typing.Any
    :param files: files
    :type files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement] | None
    :param relative_path: Use relative path
    :type relative_path: bool | typing.Any | None
    :param use_sequence_detection: Use sequence detection
    :type use_sequence_detection: bool | typing.Any | None
    :param use_udim_detection: Use UDIM detection
    :type use_udim_detection: bool | typing.Any | None
    """

    ...

def pack(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Pack an image as embedded data into the .blend file

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def project_apply(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Project edited image back onto the object

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def project_edit(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Edit a snapshot of the 3D Viewport in an external image editor

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def read_viewlayers(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Read all the current scene's view layers from cache, as needed

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def reload(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Reload current image from disk

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def remove_render_slot(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Remove the current render slot

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def render_border(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    xmin: typing.Any | None = 0,
    xmax: typing.Any | None = 0,
    ymin: typing.Any | None = 0,
    ymax: typing.Any | None = 0,
    wait_for_input: bool | typing.Any | None = True,
):
    """Set the boundaries of the render region and enable render region

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param xmin: X Min
    :type xmin: typing.Any | None
    :param xmax: X Max
    :type xmax: typing.Any | None
    :param ymin: Y Min
    :type ymin: typing.Any | None
    :param ymax: Y Max
    :type ymax: typing.Any | None
    :param wait_for_input: Wait for Input
    :type wait_for_input: bool | typing.Any | None
    """

    ...

def replace(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    filepath: str | typing.Any = "",
    hide_props_region: bool | typing.Any | None = True,
    check_existing: bool | typing.Any | None = False,
    filter_blender: bool | typing.Any | None = False,
    filter_backup: bool | typing.Any | None = False,
    filter_image: bool | typing.Any | None = True,
    filter_movie: bool | typing.Any | None = True,
    filter_python: bool | typing.Any | None = False,
    filter_font: bool | typing.Any | None = False,
    filter_sound: bool | typing.Any | None = False,
    filter_text: bool | typing.Any | None = False,
    filter_archive: bool | typing.Any | None = False,
    filter_btx: bool | typing.Any | None = False,
    filter_collada: bool | typing.Any | None = False,
    filter_alembic: bool | typing.Any | None = False,
    filter_usd: bool | typing.Any | None = False,
    filter_obj: bool | typing.Any | None = False,
    filter_volume: bool | typing.Any | None = False,
    filter_folder: bool | typing.Any | None = True,
    filter_blenlib: bool | typing.Any | None = False,
    filemode: typing.Any | None = 9,
    relative_path: bool | typing.Any | None = True,
    show_multiview: bool | typing.Any | None = False,
    use_multiview: bool | typing.Any | None = False,
    display_type: str | None = "DEFAULT",
    sort_method: str | None = "",
):
    """Replace current image by another one from disk

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param filepath: File Path, Path to file
        :type filepath: str | typing.Any
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings
        :type hide_props_region: bool | typing.Any | None
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | typing.Any | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | typing.Any | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | typing.Any | None
        :param filter_image: Filter image files
        :type filter_image: bool | typing.Any | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | typing.Any | None
        :param filter_python: Filter Python files
        :type filter_python: bool | typing.Any | None
        :param filter_font: Filter font files
        :type filter_font: bool | typing.Any | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | typing.Any | None
        :param filter_text: Filter text files
        :type filter_text: bool | typing.Any | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | typing.Any | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | typing.Any | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | typing.Any | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | typing.Any | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | typing.Any | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | typing.Any | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | typing.Any | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | typing.Any | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | typing.Any | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | typing.Any | None
        :param show_multiview: Enable Multi-View
        :type show_multiview: bool | typing.Any | None
        :param use_multiview: Use Multi-View
        :type use_multiview: bool | typing.Any | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: str | None
        :param sort_method: File sorting mode
        :type sort_method: str | None
    """

    ...

def resize(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    size: typing.Any | None = (0, 0),
):
    """Resize the image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param size: Size
    :type size: typing.Any | None
    """

    ...

def rotate_orthogonal(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    degrees: str | None = "90",
):
    """Rotate the image

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param degrees: Degrees, Amount of rotation in degrees (90, 180, 270)

    90
    90 Degrees -- Rotate 90 degrees clockwise.

    180
    180 Degrees -- Rotate 180 degrees clockwise.

    270
    270 Degrees -- Rotate 270 degrees clockwise.
        :type degrees: str | None
    """

    ...

def sample(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    size: typing.Any | None = 1,
):
    """Use mouse to sample a color in current image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param size: Sample Size
    :type size: typing.Any | None
    """

    ...

def sample_line(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    xstart: typing.Any | None = 0,
    xend: typing.Any | None = 0,
    ystart: typing.Any | None = 0,
    yend: typing.Any | None = 0,
    flip: bool | typing.Any | None = False,
    cursor: typing.Any | None = 5,
):
    """Sample a line and show it in Scope panels

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param xstart: X Start
    :type xstart: typing.Any | None
    :param xend: X End
    :type xend: typing.Any | None
    :param ystart: Y Start
    :type ystart: typing.Any | None
    :param yend: Y End
    :type yend: typing.Any | None
    :param flip: Flip
    :type flip: bool | typing.Any | None
    :param cursor: Cursor, Mouse cursor style to use during the modal operator
    :type cursor: typing.Any | None
    """

    ...

def save(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Save the image with current name and settings

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def save_all_modified(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Save all modified images

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def save_as(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    save_as_render: bool | typing.Any | None = False,
    copy: bool | typing.Any | None = False,
    allow_path_tokens: bool | typing.Any | None = True,
    filepath: str | typing.Any = "",
    check_existing: bool | typing.Any | None = True,
    filter_blender: bool | typing.Any | None = False,
    filter_backup: bool | typing.Any | None = False,
    filter_image: bool | typing.Any | None = True,
    filter_movie: bool | typing.Any | None = True,
    filter_python: bool | typing.Any | None = False,
    filter_font: bool | typing.Any | None = False,
    filter_sound: bool | typing.Any | None = False,
    filter_text: bool | typing.Any | None = False,
    filter_archive: bool | typing.Any | None = False,
    filter_btx: bool | typing.Any | None = False,
    filter_collada: bool | typing.Any | None = False,
    filter_alembic: bool | typing.Any | None = False,
    filter_usd: bool | typing.Any | None = False,
    filter_obj: bool | typing.Any | None = False,
    filter_volume: bool | typing.Any | None = False,
    filter_folder: bool | typing.Any | None = True,
    filter_blenlib: bool | typing.Any | None = False,
    filemode: typing.Any | None = 9,
    relative_path: bool | typing.Any | None = True,
    show_multiview: bool | typing.Any | None = False,
    use_multiview: bool | typing.Any | None = False,
    display_type: str | None = "DEFAULT",
    sort_method: str | None = "",
):
    """Save the image with another name and/or settings

        :type override_context: bpy.types.Context | dict[str, typing.Any] | None
        :type execution_context: int | str | None
        :type undo: bool | None
        :param save_as_render: Save As Render, Save image with render color management.For display image formats like PNG, apply view and display transform.For intermediate image formats like OpenEXR, use the default render output color space
        :type save_as_render: bool | typing.Any | None
        :param copy: Copy, Create a new image file without modifying the current image in Blender
        :type copy: bool | typing.Any | None
        :param allow_path_tokens: Allow the path to contain substitution tokens
        :type allow_path_tokens: bool | typing.Any | None
        :param filepath: File Path, Path to file
        :type filepath: str | typing.Any
        :param check_existing: Check Existing, Check and warn on overwriting existing files
        :type check_existing: bool | typing.Any | None
        :param filter_blender: Filter .blend files
        :type filter_blender: bool | typing.Any | None
        :param filter_backup: Filter .blend files
        :type filter_backup: bool | typing.Any | None
        :param filter_image: Filter image files
        :type filter_image: bool | typing.Any | None
        :param filter_movie: Filter movie files
        :type filter_movie: bool | typing.Any | None
        :param filter_python: Filter Python files
        :type filter_python: bool | typing.Any | None
        :param filter_font: Filter font files
        :type filter_font: bool | typing.Any | None
        :param filter_sound: Filter sound files
        :type filter_sound: bool | typing.Any | None
        :param filter_text: Filter text files
        :type filter_text: bool | typing.Any | None
        :param filter_archive: Filter archive files
        :type filter_archive: bool | typing.Any | None
        :param filter_btx: Filter btx files
        :type filter_btx: bool | typing.Any | None
        :param filter_collada: Filter COLLADA files
        :type filter_collada: bool | typing.Any | None
        :param filter_alembic: Filter Alembic files
        :type filter_alembic: bool | typing.Any | None
        :param filter_usd: Filter USD files
        :type filter_usd: bool | typing.Any | None
        :param filter_obj: Filter OBJ files
        :type filter_obj: bool | typing.Any | None
        :param filter_volume: Filter OpenVDB volume files
        :type filter_volume: bool | typing.Any | None
        :param filter_folder: Filter folders
        :type filter_folder: bool | typing.Any | None
        :param filter_blenlib: Filter Blender IDs
        :type filter_blenlib: bool | typing.Any | None
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file
        :type filemode: typing.Any | None
        :param relative_path: Relative Path, Select the file relative to the blend file
        :type relative_path: bool | typing.Any | None
        :param show_multiview: Enable Multi-View
        :type show_multiview: bool | typing.Any | None
        :param use_multiview: Use Multi-View
        :type use_multiview: bool | typing.Any | None
        :param display_type: Display Type

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :type display_type: str | None
        :param sort_method: File sorting mode
        :type sort_method: str | None
    """

    ...

def save_sequence(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Save a sequence of images

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def tile_add(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    number: typing.Any | None = 1002,
    count: typing.Any | None = 1,
    label: str | typing.Any = "",
    fill: bool | typing.Any | None = True,
    color: typing.Any | None = (0.0, 0.0, 0.0, 1.0),
    generated_type: str | None = "BLANK",
    width: typing.Any | None = 1024,
    height: typing.Any | None = 1024,
    float: bool | typing.Any | None = False,
    alpha: bool | typing.Any | None = True,
):
    """Adds a tile to the image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param number: Number, UDIM number of the tile
    :type number: typing.Any | None
    :param count: Count, How many tiles to add
    :type count: typing.Any | None
    :param label: Label, Optional tile label
    :type label: str | typing.Any
    :param fill: Fill, Fill new tile with a generated image
    :type fill: bool | typing.Any | None
    :param color: Color, Default fill color
    :type color: typing.Any | None
    :param generated_type: Generated Type, Fill the image with a grid for UV map testing
    :type generated_type: str | None
    :param width: Width, Image width
    :type width: typing.Any | None
    :param height: Height, Image height
    :type height: typing.Any | None
    :param float: 32-bit Float, Create image with 32-bit floating-point bit depth
    :type float: bool | typing.Any | None
    :param alpha: Alpha, Create an image with an alpha channel
    :type alpha: bool | typing.Any | None
    """

    ...

def tile_fill(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    color: typing.Any | None = (0.0, 0.0, 0.0, 1.0),
    generated_type: str | None = "BLANK",
    width: typing.Any | None = 1024,
    height: typing.Any | None = 1024,
    float: bool | typing.Any | None = False,
    alpha: bool | typing.Any | None = True,
):
    """Fill the current tile with a generated image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param color: Color, Default fill color
    :type color: typing.Any | None
    :param generated_type: Generated Type, Fill the image with a grid for UV map testing
    :type generated_type: str | None
    :param width: Width, Image width
    :type width: typing.Any | None
    :param height: Height, Image height
    :type height: typing.Any | None
    :param float: 32-bit Float, Create image with 32-bit floating-point bit depth
    :type float: bool | typing.Any | None
    :param alpha: Alpha, Create an image with an alpha channel
    :type alpha: bool | typing.Any | None
    """

    ...

def tile_remove(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Removes a tile from the image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def unpack(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    method: str | None = "USE_LOCAL",
    id: str | typing.Any = "",
):
    """Save an image packed in the .blend file to disk

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param method: Method, How to unpack
    :type method: str | None
    :param id: Image Name, Image data-block name to unpack
    :type id: str | typing.Any
    """

    ...

def view_all(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    fit_view: bool | typing.Any | None = False,
):
    """View the entire image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param fit_view: Fit View, Fit frame to the viewport
    :type fit_view: bool | typing.Any | None
    """

    ...

def view_center_cursor(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Center the view so that the cursor is in the middle of the view

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def view_cursor_center(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    fit_view: bool | typing.Any | None = False,
):
    """Set 2D Cursor To Center View location

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param fit_view: Fit View, Fit frame to the viewport
    :type fit_view: bool | typing.Any | None
    """

    ...

def view_ndof(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """Use a 3D mouse device to pan/zoom the view

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def view_pan(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    offset: typing.Any | None = (0.0, 0.0),
):
    """Pan the view

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param offset: Offset, Offset in floating-point units, 1.0 is the width and height of the image
    :type offset: typing.Any | None
    """

    ...

def view_selected(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
):
    """View all selected UVs

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    """

    ...

def view_zoom(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    factor: typing.Any | None = 0.0,
    use_cursor_init: bool | typing.Any | None = True,
):
    """Zoom in/out the image

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param factor: Factor, Zoom factor, values higher than 1.0 zoom in, lower values zoom out
    :type factor: typing.Any | None
    :param use_cursor_init: Use Mouse Position, Allow the initial mouse position to be used
    :type use_cursor_init: bool | typing.Any | None
    """

    ...

def view_zoom_border(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    xmin: typing.Any | None = 0,
    xmax: typing.Any | None = 0,
    ymin: typing.Any | None = 0,
    ymax: typing.Any | None = 0,
    wait_for_input: bool | typing.Any | None = True,
    zoom_out: bool | typing.Any | None = False,
):
    """Zoom in the view to the nearest item contained in the border

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param xmin: X Min
    :type xmin: typing.Any | None
    :param xmax: X Max
    :type xmax: typing.Any | None
    :param ymin: Y Min
    :type ymin: typing.Any | None
    :param ymax: Y Max
    :type ymax: typing.Any | None
    :param wait_for_input: Wait for Input
    :type wait_for_input: bool | typing.Any | None
    :param zoom_out: Zoom Out
    :type zoom_out: bool | typing.Any | None
    """

    ...

def view_zoom_in(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    location: typing.Any | None = (0.0, 0.0),
):
    """Zoom in the image (centered around 2D cursor)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param location: Location, Cursor location in screen coordinates
    :type location: typing.Any | None
    """

    ...

def view_zoom_out(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    location: typing.Any | None = (0.0, 0.0),
):
    """Zoom out the image (centered around 2D cursor)

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param location: Location, Cursor location in screen coordinates
    :type location: typing.Any | None
    """

    ...

def view_zoom_ratio(
    override_context: bpy.types.Context | dict[str, typing.Any] | None = None,
    execution_context: int | str | None = None,
    undo: bool | None = None,
    *,
    ratio: typing.Any | None = 0.0,
):
    """Set zoom ratio of the view

    :type override_context: bpy.types.Context | dict[str, typing.Any] | None
    :type execution_context: int | str | None
    :type undo: bool | None
    :param ratio: Ratio, Zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out
    :type ratio: typing.Any | None
    """

    ...
