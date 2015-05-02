# <pep8-80 compliant>

# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.props import *

from . import cpuv_common

__author__ = "Nutti <nutti.metro@gmail.com>"
__status__ = "production"
__version__ = "3.0"
__date__ = "X XXXX 2015"


# copy UV map (sub menu operator)
class CPUVUVMapCopyUVOperation(bpy.types.Operator):
    bl_idname = "uv.cpuv_uvmap_copy_uv_op"
    bl_label = "Copy UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()

    def execute(self, context):
        props = bpy.context.scene.cpuv_props
        
        self.report(
            {'INFO'},
            "Copy UV coordinate. (UV map:" + self.uv_map + ")")
        
        # save current mode
        mode_orig = bpy.context.object.mode

        try:
            # prepare for coping
            props.src_obj = cpuv_common.prep_copy(self)
            
            # copy
            props.src_faces = cpuv_common.get_selected_faces(
                props.src_obj)
            props.src_uv_map = cpuv_common.copy_opt(
                self, self.uv_map, props.src_obj, props.src_faces)
            
            # finish coping
            cpuv_common.fini_copy()
        
        except cpuv_common.CPUVError as e:
            e.report(self)
            bpy.ops.object.mode_set(mode=mode_orig)
            return {'CANCELLED'}
        
        # revert to original mode
        bpy.ops.object.mode_set(mode=mode_orig)
        
        return {'FINISHED'}


# copy UV map
class CPUVUVMapCopyUV(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.cpuv_uvmap_copy_uv"
    bl_label = "Copy UV Map"
    bl_description = "Copy UV map data"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        
        layout = self.layout
        
        # create sub menu
        uv_maps = bpy.context.active_object.data.uv_textures.keys()
        for m in uv_maps:
            layout.operator(
                CPUVUVMapCopyUVOperation.bl_idname,
                text=m).uv_map = m
            

# paste UV map (sub menu operator)
class CPUVUVMapPasteUVOperation(bpy.types.Operator):
    bl_idname = "uv.cpuv_uvmap_paste_uv_op"
    bl_label = "Paste UV Map (Sub Menu Operator)"
    uv_map = bpy.props.StringProperty()
    
    flip_copied_uv = BoolProperty(
        name = "Flip Copied UV",
        description = "Flip Copied UV...",
        default = False)

    rotate_copied_uv = IntProperty(
        default = 0,
        name = "Rotate Copied UV",
        min = 0,
        max = 30)

    def execute(self, context):
        props = bpy.context.scene.cpuv_props
        
        self.report(
            {'INFO'}, "Paste UV coordinate. (UV map:" + self.uv_map + ")")
        
        # save current mode
        mode_orig = bpy.context.object.mode

        try:
            # prepare for pasting
            dest_obj = cpuv_common.prep_paste(
                self, props.src_obj, props.src_faces)
            
            # paste
            dest_faces = cpuv_common.get_selected_faces(dest_obj)
            cpuv_common.paste_opt(
                self, self.uv_map, props.src_obj, props.src_faces,
                props.src_uv_map, dest_obj, dest_faces)
            
            # finish pasting
            cpuv_common.fini_paste()
        
        except cpuv_common.CPUVError as e:
            e.report(self)
            bpy.ops.object.mode_set(mode=mode_orig)
            return {'CANCELLED'}
        
        # revert to original mode
        bpy.ops.object.mode_set(mode=mode_orig)
        
        return {'FINISHED'}


# paste UV map
class CPUVUVMapPasteUV(bpy.types.Menu):
    """Copying UV map coordinate on selected object."""
    
    bl_idname = "uv.cpuv_uvmap_paste_uv"
    bl_label = "Paste UV Map"
    bl_description = "Paste UV map data"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        
        layout = self.layout
        
        # create sub menu
        uv_maps = bpy.context.active_object.data.uv_textures.keys()
        for m in uv_maps:
            layout.operator(
                CPUVUVMapPasteUVOperation.bl_idname,
                text=m).uv_map = m
