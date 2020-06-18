import bpy
import bmesh
import numpy as np
from bpy.props import *



def user_props():
    scene = bpy.types.Scene
    
    scene.addbone_marge_on = BoolProperty(
        name='Marge Bone',
        description='Marge Bone',
        default=True,
        )
    
    scene.addbone_switch_dir = BoolProperty(
        name='Bone Direction Flip',
        description='Bone Direction Flip',
        default=False,
        )
        
    scene.addbone_marge_count = IntProperty(
        name='MargeCount',
        description='Marge Bone Counts',
#        array_length=10,
        default=1,
        min=1,
        max=10,
        )

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
        
        scene = context.scene

        layout = self.layout
        box = layout.box()
        box.prop(scene, 'addbone_switch_dir')
        box.prop(scene, 'addbone_marge_on')
        box.prop(scene, 'addbone_marge_count')

def del_props():
    scene = bpy.types.Scene
    del scene.addbone_marge_on
    del scene.addbone_marge_count

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
        
        scene = context.scene
        object = bpy.context.object
        mesh = object.data
        bm = bmesh.from_edit_mesh(mesh)
        
        amt = createArmature('armature')
        
        bpy.ops.object.mode_set(mode='EDIT')

#        eo = bpy.context.edit_object
        mw = object.matrix_world
        self.report({'INFO'}, str(mw))
        
        elist = [e for e in bm.edges if e.select]
#        bonelist = np.array([0,0,0])
#        bonelist = np.array([[0] * 3] * 1)
        bonelist = np.array([[0,0,0]])
        
        for e in elist:
#            if (e.select == True):
#                print(e)
#                self.report({'INFO'}, str(e))
#                self.report({'INFO'}, str(e.verts[0].co))
                
                #createBones(amt, e.verts, mw)
                
                bone = amt.edit_bones.new('Bone.' + str(e.index))
                bone.head = mw @ e.verts[0].co
                bone.tail = mw @ e.verts[1].co
                
#                self.report({'INFO'}, str(bone.name))
#                self.report({'INFO'}, str(e.verts[1].index))

                #https://teratail.com/questions/91895
#                p = int(e.verts[1].index)                
#                r = np.where(bonelist[:,1] == p)
#                self.report({'INFO'}, str(r))
#                bonelist.append([bone.name ,e.verts[0].index ,e.verts[1].index])
                bonelist = np.append(bonelist, [[bone.name ,e.verts[0].index ,e.verts[1].index]], axis = 0) 
                
#        bpy.ops.object.mode_set(mode='OBJECT')
        self.report({'INFO'}, str(bonelist))
        
        editbones = amt.edit_bones
        
        for b in editbones:
            for b2 in editbones:
                if b != b2:
                    if b.tail == b2.tail:
                        b2.select = True
                        bpy.ops.armature.switch_direction()
                        b2.select = False
        
        if scene.addbone_switch_dir:
            bpy.ops.armature.select_all(action='SELECT')
            bpy.ops.armature.switch_direction()
            bpy.ops.armature.select_all(action='DESELECT')                

        for b in editbones:
            for b2 in editbones:
                if b != b2:                        
                    if b.head == b2.tail:
                        b.parent = b2
                        b.use_connect = True

        if scene.addbone_marge_on:
            MargeCount = scene.addbone_marge_count
            bpy.ops.armature.select_all(action='SELECT')
            elist = [e for e in context.selected_editable_bones if e.select]

            rootbones = []     
                    
            for v in elist:
                if v.parent:
                    if v.parent.select == False:
                        rootbones += [v]
                else:
                    rootbones += [v]
                    
            bpy.ops.armature.select_all(action='DESELECT')

            i = 0

            for bone in rootbones:
                while bone in elist:
                    print("bone.name:" + bone.name) 
                    
                    i = i + 1
                         
                    if bone.children:
                        bone.select = True
                        print("children.name:" + bone.children[0].name) 
                        bone = bone.children[0]

                        if i == MargeCount:
                            bpy.ops.armature.merge(type='WITHIN_CHAIN')
                            bpy.ops.armature.select_all(action='DESELECT')
                            i = 0
                        
                    else:
                        bone.select = True
                        bpy.ops.armature.merge(type='WITHIN_CHAIN')
                        i = 0
                        break


        
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
    user_props()

# クラスの登録解除
def unregister():
    del_props()
    for cls in classes:
         bpy.utils.unregister_class(cls)


# main
if __name__ == "__main__":
     register()
