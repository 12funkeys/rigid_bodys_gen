import bpy
import bmesh

# show UI
### add Tool Panel
class RBG_PT_MenuAddBonesTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigid Body Gen"
    # bl_context = "mesh_edit"
    bl_label = "Add Bones Tools"


    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH'}

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator(RBG_OT_AddBonesOnEdges.bl_idname, text="Adding Bones On Edges", icon='BONE_DATA')


# add bones
class RBG_OT_AddBonesOnEdges(bpy.types.Operator):

    bl_idname = "bone_gen.add_bones_onedges"
    bl_label = "Adding Bones On Edges"
    bl_description = "Adding Bones On Selected Edges"
    bl_options = {'REGISTER', 'UNDO'}

    # def __init__(self):

    # def draw(self, context):

    ###
    def execute(self, context):
        
        object = bpy.context.object
        mesh = object.data
        bm = bmesh.from_edit_mesh(mesh)
        
        amt = createArmature('armature')
        
        bpy.ops.object.mode_set(mode='EDIT')

#        eo = bpy.context.edit_object
        mw = object.matrix_world
        self.report({'INFO'}, str(mw))
        
        for e in bm.edges:
            if (e.select == True):
#                print(e)
#                self.report({'INFO'}, str(e))
#                self.report({'INFO'}, str(e.verts[0].co))
                
                createBones(amt, e.verts, mw)
                
        bpy.ops.object.mode_set(mode='OBJECT')
        
#        for ed in bpy.context.active_object.data.edges:
#            
#            if (ed.select == True):
#                print("edge index:{0: 2} v0:{0} v1:{1}".format(ed.index, ed.vertices[0], ed.vertices[1]))
        return {'FINISHED'}


def createArmature(name):
    # アーマチュアとオブジェクトを作成
    amt = bpy.data.armatures.new(name+'Amt')
    ob = bpy.data.objects.new(name, amt)
#    ob.location = origin
#    ob.show_name = True
 
    # シーンにオブジェクトをリンクしアクティブ化
    scn = bpy.context.collection
    scn.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
#    ob.select_set(state=True)
 
    return amt

def createBones(amt, verts, mw):

    bone = amt.edit_bones.new('Bone')
    bone.head = mw @ verts[0].co
    bone.tail = mw @ verts[1].co
    
    return


classes = [
     RBG_PT_MenuAddBonesTools,
     RBG_OT_AddBonesOnEdges
]

# クラスの登録
def register():
     for cls in classes:
         bpy.utils.register_class(cls)

# クラスの登録解除
def unregister():
     for cls in classes:
         bpy.utils.unregister_class(cls)


# main
if __name__ == "__main__":
     register()
