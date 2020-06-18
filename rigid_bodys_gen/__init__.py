bl_info = {
    "name": "rigid bodys tools",
    "author": "12funkeys",
    "version": (2, 0),
    "blender": (2, 80, 0),
    "location": "pose > selected bones",
    "description": "Set rigid body and constraint easily",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"
}

if "bpy" in locals():
    import imp
    imp.reload(rigidBodyGen)
    imp.reload(AddBones)
else:
    from . import rigidBodyGen
    from . import AddBones

import bpy



# クラスの登録
def register():
    rigidBodyGen.register()
    AddBones.register()

# クラスの登録解除
def unregister():
    rigidBodyGen.unregister()
    AddBones.unregister()


# main
if __name__ == "__main__":
    register()
