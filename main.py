bl_info = {
    "name": "Auto Save and Restore",
    "blender": (3, 0, 0),
    "category": "Object",
    "description": "Save and restore changes in Blender",
}

import bpy
import os
import json

# Définir le chemin global pour le fichier de sauvegarde
temp_dir = bpy.app.tempdir
global_filepath = os.path.join(temp_dir, "scene_state.json")

class SaveSceneStateOperator(bpy.types.Operator):
    bl_idname = "wm.save_scene_state"
    bl_label = "Save Scene State"

    def execute(self, context):
        scene = context.scene
        data = {
            "objects": []
        }

        for obj in scene.objects:
            obj_data = {
                "name": obj.name,
                "location": list(obj.location),
                "rotation_euler": list(obj.rotation_euler),
                "scale": list(obj.scale)
            }
            data["objects"].append(obj_data)

        with open(global_filepath, 'w') as f:
            json.dump(data, f, indent=4)

        self.report({'INFO'}, f"Scene state saved to {global_filepath}")
        return {'FINISHED'}


class LoadSceneStateOperator(bpy.types.Operator):
    bl_idname = "wm.load_scene_state"
    bl_label = "Load Scene State"

    def execute(self, context):
        if not os.path.exists(global_filepath):
            self.report({'ERROR'}, f"No saved state found at {global_filepath}")
            return {'CANCELLED'}

        with open(global_filepath, 'r') as f:
            data = json.load(f)

        for obj_data in data["objects"]:
            if obj_data["name"] in bpy.data.objects:
                obj = bpy.data.objects[obj_data["name"]]
                obj.location = obj_data["location"]
                obj.rotation_euler = obj_data["rotation_euler"]
                obj.scale = obj_data["scale"]
                obj.keyframe_insert(data_path="location")
                obj.keyframe_insert(data_path="rotation_euler")
                obj.keyframe_insert(data_path="scale")

        self.report({'INFO'}, "Scene state loaded")
        return {'FINISHED'}


class SCENE_PT_auto_save_restore(bpy.types.Panel):
    bl_label = "Auto Save and Restore"
    bl_idname = "SCENE_PT_auto_save_restore"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.operator("wm.save_scene_state")
        row = layout.row()
        row.operator("wm.load_scene_state")


def register():
    bpy.utils.register_class(SaveSceneStateOperator)
    bpy.utils.register_class(LoadSceneStateOperator)
    bpy.utils.register_class(SCENE_PT_auto_save_restore)


def unregister():
    bpy.utils.unregister_class(SaveSceneStateOperator)
    bpy.utils.unregister_class(LoadSceneStateOperator)
    bpy.utils.unregister_class(SCENE_PT_auto_save_restore)


if __name__ == "__main__":
    register()
