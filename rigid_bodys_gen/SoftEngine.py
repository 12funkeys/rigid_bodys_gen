import bpy
from bpy.props import *
import bmesh
import numpy as np
import sys
from time import sleep

bl_info = {
    "name": "soft engine",
    "author": "12funkeys",
    "version": (0, 1),
    "blender": (2, 80, 0),
    "location": "Object > Edit mode",
    "description": "Set rigid body and constraint easily",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"
}

shapes = [
        ('MESH', 'Mesh', 'Mesh'),
        ('CONVEX_HULL', 'Convex Hull', 'Convex Hull'),
        ('CONE', 'Cone', 'Cone'),
        ('CYLINDER', 'Cylinder', 'Cylinder'),
        ('CAPSULE', 'Capsule', 'Capsule'),
        ('SPHERE', 'Sphere', 'Sphere'),
        ('BOX', 'Box', 'Box')]

types = [
        ('GENERIC_SPRING', 'Generic Spring', 'Generic Spring'),
        ('GENERIC', 'Generic', 'Generic')]

### user prop
def user_props():
        scene = bpy.types.Scene
        scene.rb_shape = EnumProperty(
            name='Shape',
            description='Choose Rigid Body Shape',
            items=shapes,
            default='CAPSULE')

        scene.rc_dim = FloatVectorProperty(
            name = "Dimensions",
            description = "rigid body Dimensions XYZ",
            default = (1, 1, 1),
            subtype = 'XYZ',
            unit = 'NONE',
            min = 0,
            max = 5)

        scene.rc_rudius = FloatProperty(
            name = "Rudius",
            description = "rigid body rudius",
            default = 0.1,
            subtype = 'NONE',
            min = 0.001,)

        scene.rc_mass = FloatProperty(
            name = "Mass",
            description = "rigid body mass",
            default = 1.0,
            subtype = 'NONE',
            min = 0.001,)

        scene.rc_friction = FloatProperty(
            name = "Friction",
            description = "rigid body friction",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        scene.rc_bounciness = FloatProperty(
            name = "Bounciness",
            description = "rigid body bounciness",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        scene.rc_translation = FloatProperty(
            name = "Translation",
            description = "rigid body translation",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        scene.rc_rotation = FloatProperty(
            name = "Rotation",
            description = "rigid body rotation",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)


        scene.jo_type = EnumProperty(
            name='Type',
            description='Choose Contstraint Type',
            items=types,
            default='GENERIC')

        scene.jo_limit_lin_x = BoolProperty(
            name='X Axis',
            description='limit x',
            default=True,
            options={'ANIMATABLE'})

        scene.jo_limit_lin_y = BoolProperty(
            name='Y Axis',
            description='limit y',
            default=True)

        scene.jo_limit_lin_z = BoolProperty(
            name='Z Axis',
            description='limit z',
            default=True)

        scene.jo_limit_lin_x_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_lin_x_lower",
            default = 0,
            subtype = 'NONE')

        scene.jo_limit_lin_y_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_lin_y_lower",
            default = 0,
            subtype = 'NONE')

        scene.jo_limit_lin_z_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_lin_z_lower",
            default = 0,
            subtype = 'NONE')

        scene.jo_limit_lin_x_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_lin_x_upper",
            default = 0,
            subtype = 'NONE')

        scene.jo_limit_lin_y_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_lin_y_upper",
            default = 0,
            subtype = 'NONE')

        scene.jo_limit_lin_z_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_lin_z_upper",
            default = 0,
            subtype = 'NONE')

        scene.jo_limit_ang_x = BoolProperty(
            name='X Angle',
            description='Angle limit x',
            default=True,
            options={'ANIMATABLE'})

        scene.jo_limit_ang_y = BoolProperty(
            name='Y Angle',
            description='Angle limit y',
            default=True)

        scene.jo_limit_ang_z = BoolProperty(
            name='Z Angle',
            description='Angle limit z',
            default=True)

        scene.jo_limit_ang_x_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_ang_x_lower",
            default = -0.785398,
            subtype = 'ANGLE')

        scene.jo_limit_ang_y_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_ang_y_lower",
            default = -0.785398,
            subtype = 'ANGLE')

        scene.jo_limit_ang_z_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_ang_z_lower",
            default = -0.785398,
            subtype = 'ANGLE')

        scene.jo_limit_ang_x_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_ang_x_upper",
            default = 0.785398,
            subtype = 'ANGLE')

        scene.jo_limit_ang_y_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_ang_y_upper",
            default = 0.785398,
            subtype = 'ANGLE')

        scene.jo_limit_ang_z_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_ang_z_upper",
            default = 0.785398,
            subtype = 'ANGLE')


        scene.jo_use_spring_x = BoolProperty(
            name='X',
            description='use spring x',
            default=False)

        scene.jo_use_spring_y = BoolProperty(
            name='Y',
            description='use spring y',
            default=False)

        scene.jo_use_spring_z = BoolProperty(
            name='Z',
            description='use spring z',
            default=False)

        scene.jo_spring_stiffness_x = FloatProperty(
            name = "Stiffness",
            description = "Stiffness on the X Axis",
            default = 10.000,
            subtype = 'NONE',
            min = 0)

        scene.jo_spring_stiffness_y = FloatProperty(
            name = "Stiffness",
            description = "Stiffness on the Y Axis",
            default = 10.000,
            subtype = 'NONE',
            min = 0)

        scene.jo_spring_stiffness_z = FloatProperty(
            name = "Stiffness",
            description = "Stiffness on the Z Axis",
            default = 10.000,
            subtype = 'NONE',
            min = 0)

        scene.jo_spring_damping_x = FloatProperty(
            name = "Damping X",
            description = "Damping on the X Axis",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        scene.jo_spring_damping_y = FloatProperty(
            name = "Damping Y",
            description = "Damping on the Y Axis",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        scene.jo_spring_damping_z = FloatProperty(
            name = "Damping Z",
            description = "Damping on the Z Axis",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)


        scene.jo_constraint_object = BoolProperty(
            name='Auto Constraint Object',
            description='Constraint Object',
            default=True)

        scene.rc_rootbody_passive = BoolProperty(
            name='Passive',
            description='Rigid Body Type Passive',
            default=True)


def del_props():
    scene = bpy.types.Scene
    del scene.rb_shape



# show UI
### add Tool Panel
class RBG_PT_MenuAddBonesTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigid Body Gen"
    # bl_context = "mesh_edit"
    bl_label = "Soft Engine"



    @classmethod
    def poll(cls, context):
        return context.mode in {'EDIT_MESH'}

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        col = layout.column(align=True)
        col.operator(RBG_OT_AddBonesOnEdges.bl_idname, text="Adding Bones On Edges", icon='BONE_DATA')

        ###Rigid Body Object
        layout = self.layout

        box = layout.box()
        box.prop(scene, 'rb_shape')
#        box.prop(scene, 'rc_dim')
        box.prop(scene, 'rc_rudius')
        box.prop(scene, 'rc_mass')
        box.prop(scene, 'rc_friction')
        box.prop(scene, 'rc_bounciness')
        box.prop(scene, 'rc_translation')
        box.prop(scene, 'rc_rotation')


        #Joint Object
        layout = self.layout
        box = layout.box()
        box.prop(scene, 'jo_type')

        col = box.column(align=True)
        col.label(text="Limits:")

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_limit_lin_x', toggle=True)
        sub.prop(scene, 'jo_limit_lin_x_lower')
        sub.prop(scene, 'jo_limit_lin_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_limit_lin_y', toggle=True)
        sub.prop(scene, 'jo_limit_lin_y_lower')
        sub.prop(scene, 'jo_limit_lin_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_limit_lin_z', toggle=True)
        sub.prop(scene, 'jo_limit_lin_z_lower')
        sub.prop(scene, 'jo_limit_lin_z_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_limit_ang_x', toggle=True)
        sub.prop(scene, 'jo_limit_ang_x_lower')
        sub.prop(scene, 'jo_limit_ang_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_limit_ang_y', toggle=True)
        sub.prop(scene, 'jo_limit_ang_y_lower')
        sub.prop(scene, 'jo_limit_ang_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_limit_ang_z', toggle=True)
        sub.prop(scene, 'jo_limit_ang_z_lower')
        sub.prop(scene, 'jo_limit_ang_z_upper')

        col.label(text="Springs:")

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_use_spring_x', toggle=True)
        sub.prop(scene, 'jo_spring_stiffness_x')
        sub.prop(scene, 'jo_spring_damping_x')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_use_spring_y', toggle=True)
        sub.prop(scene, 'jo_spring_stiffness_y')
        sub.prop(scene, 'jo_spring_damping_y')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'jo_use_spring_z', toggle=True)
        sub.prop(scene, 'jo_spring_stiffness_z')
        sub.prop(scene, 'jo_spring_damping_z')


# add bones
class RBG_OT_AddBonesOnEdges(bpy.types.Operator):

    bl_idname = "bone_gen.add_bones_onedges"
    bl_label = "Execute Soft Engine"
    bl_description = "Execute Soft Engine"
    bl_options = {'REGISTER', 'UNDO'}

    # def __init__(self):

    # def draw(self, context):

    ###
    def execute(self, context):
        
        scene = context.scene
        object = bpy.context.object
        mesh = object.data
        
        bm = bmesh.from_edit_mesh(mesh)
        
        obamt = createArmature('armature', object.location)
#        self.report({'INFO'}, str(obamt))
        
        
        bpy.ops.object.mode_set(mode='EDIT')
        
        eo = bpy.context.edit_object
        mw = eo.matrix_world

        vlist = [e for e in bm.verts if e.select]
        vindex = [e.index for e in bm.verts if e.select]
        elist = [e for e in bm.edges if e.select]
        elistv = np.ravel([(e.verts[0].index, e.verts[1].index) for e in elist])
        elisttolist = elistv.tolist()
        singleVerts = [i for i in list(set(elisttolist)) if elisttolist.count(i) == 1]
#        self.report({'INFO'}, str(singleVerts))
           
       #create Rigidbody object
       
        sys.stdout.write("Soft Engine Working..."+"\n")
        sys.stdout.flush()
        
        idx = 0
        for v in vlist:
            idx += 1
            wvco = mw @ v.co
            bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, radius=scene.rc_rudius, calc_uvs=False, enter_editmode=False, align='WORLD', location=wvco, rotation=(0.0, 0.0, 0.0))
#            bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)

            
            #view setting
            rc = bpy.context.active_object
            rc.name = "rc." + str(v.index)
            rc.show_in_front = True
            rc.display_type = 'WIRE'
            rc.show_in_front = True
            rc.display.show_shadows = False
            rc.hide_render = True
            rc.hide_render = True
            
            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()
            if v.index in singleVerts:
                rc.rigid_body.type = "PASSIVE"
                rc.rigid_body.kinematic = True
            else:
                rc.rigid_body.type = "ACTIVE"
                rc.rigid_body.kinematic = False
                
            rc.rigid_body.collision_shape = "SPHERE"
            rc.rigid_body.mass = scene.rc_mass
            rc.rigid_body.friction = scene.rc_friction
            rc.rigid_body.restitution = scene.rc_bounciness
            rc.rigid_body.linear_damping = scene.rc_translation
            rc.rigid_body.angular_damping = scene.rc_rotation
            
            msg = "PROSESS 1/4: %i of %i" % (idx, len(vlist)-1)
            sys.stdout.write(msg + chr(8) * len(msg))
            sys.stdout.flush()
            sleep(0.02)
        
        sys.stdout.write("PROSESS 1/4 DONE" + " "*len(msg)+"\n")
        sys.stdout.flush()

        #create bones
        object.select_set(state=True)
        bpy.context.view_layer.objects.active = obamt[0]
        bpy.ops.object.parent_set(type='ARMATURE')
        bpy.ops.object.mode_set(mode='EDIT')
        for v in vlist:
#            self.report({'INFO'}, str(v))
              
            bone = obamt[1].edit_bones.new('softbone.' + str(v.index))
            bone.head = v.co
            bone.tail = bone.head + 0.1 * v.normal
#            obamt[0].update_tag(refresh={'OBJECT'})


        #new CHILD_OF
        bpy.ops.object.posemode_toggle()
        idx = 0
        for v in vlist:
            idx += 1
                       
            co = obamt[0].pose.bones['softbone.' + str(v.index)].constraints.new("CHILD_OF")
            tgt = bpy.data.objects['rc.' + str(v.index)]
            co.target = tgt
#            bpy.ops.constraint.childof_set_inverse(constraint=co.name, owner='BONE')
            co.inverse_matrix = mw @ tgt.matrix_world.inverted()   
            obamt[0].update_tag(refresh={'OBJECT'})
#            bpy.context.scene.update()

            msg = "PROSESS 2/4: %i of %i" % (idx, len(vlist)-1)
            sys.stdout.write(msg + chr(8) * len(msg))
            sys.stdout.flush()
            sleep(0.02)
        
        sys.stdout.write("PROSESS 2/4 DONE" + " "*len(msg)+"\n")
        sys.stdout.flush()

        bpy.ops.object.mode_set(mode='OBJECT')
        
        idx = 0
        for e in elist:
            idx += 1
#            print(e)
#            self.report({'INFO'}, str(e))
#            self.report({'INFO'}, str(e.verts[0].co))
                        
            mid = (e.verts[0].co + e.verts[1].co) / 2
            wmid = mw @ mid
#            self.report({'INFO'}, str(mid))
            
#        self.report({'INFO'}, str(mw))
#        self.report({'INFO'}, str(object.location))
    
#                bpy.ops.mesh.primitive_cube_add(size=0.1, calc_uvs=True, enter_editmode=False, align='WORLD', location=wmid, rotation=(0.0, 0.0, 0.0))
            jc = bpy.ops.object.empty_add(type='PLAIN_AXES', radius=0.1, align='WORLD', location=wmid)
            ### Set Rigid Body Joint
            jc = bpy.context.active_object
            bpy.ops.rigidbody.constraint_add()
            jc.rigid_body_constraint.type = scene.jo_type
            jc.rigid_body_constraint.use_breaking = False
            jc.rigid_body_constraint.disable_collisions = False
            jc.rigid_body_constraint.use_override_solver_iterations = True
            jc.rigid_body_constraint.breaking_threshold = 10
            jc.rigid_body_constraint.solver_iterations = 10
            jc.rigid_body_constraint.object1 = bpy.data.objects['rc.' + str(e.verts[0].index)]
            jc.rigid_body_constraint.object2 = bpy.data.objects['rc.' + str(e.verts[1].index)]
  
            jc.rigid_body_constraint.use_limit_lin_x = scene.jo_limit_lin_x
            jc.rigid_body_constraint.use_limit_lin_y = scene.jo_limit_lin_y
            jc.rigid_body_constraint.use_limit_lin_z = scene.jo_limit_lin_z
            jc.rigid_body_constraint.limit_lin_x_lower = scene.jo_limit_lin_x_lower
            jc.rigid_body_constraint.limit_lin_y_lower = scene.jo_limit_lin_y_lower
            jc.rigid_body_constraint.limit_lin_z_lower = scene.jo_limit_lin_z_lower
            jc.rigid_body_constraint.limit_lin_x_upper = scene.jo_limit_lin_x_upper
            jc.rigid_body_constraint.limit_lin_y_upper = scene.jo_limit_lin_y_upper
            jc.rigid_body_constraint.limit_lin_z_upper = scene.jo_limit_lin_z_upper

            jc.rigid_body_constraint.use_limit_ang_x = scene.jo_limit_ang_x
            jc.rigid_body_constraint.use_limit_ang_y = scene.jo_limit_ang_y
            jc.rigid_body_constraint.use_limit_ang_z = scene.jo_limit_ang_z
            jc.rigid_body_constraint.limit_ang_x_lower = scene.jo_limit_ang_x_lower
            jc.rigid_body_constraint.limit_ang_y_lower = scene.jo_limit_ang_y_lower
            jc.rigid_body_constraint.limit_ang_z_lower = scene.jo_limit_ang_z_lower
            jc.rigid_body_constraint.limit_ang_x_upper = scene.jo_limit_ang_x_upper
            jc.rigid_body_constraint.limit_ang_y_upper = scene.jo_limit_ang_y_upper
            jc.rigid_body_constraint.limit_ang_z_upper = scene.jo_limit_ang_z_upper

            jc.rigid_body_constraint.use_spring_x = scene.jo_use_spring_x
            jc.rigid_body_constraint.use_spring_y = scene.jo_use_spring_y
            jc.rigid_body_constraint.use_spring_z = scene.jo_use_spring_z
            jc.rigid_body_constraint.spring_stiffness_x = scene.jo_spring_stiffness_x
            jc.rigid_body_constraint.spring_stiffness_y = scene.jo_spring_stiffness_y
            jc.rigid_body_constraint.spring_stiffness_z = scene.jo_spring_stiffness_z
            jc.rigid_body_constraint.spring_damping_x = scene.jo_spring_damping_x
            jc.rigid_body_constraint.spring_damping_y = scene.jo_spring_damping_y
            jc.rigid_body_constraint.spring_damping_z = scene.jo_spring_damping_z
  
    
            msg = "PROSESS 3/4: %i of %i" % (idx, len(elist)-1)
            sys.stdout.write(msg + chr(8) * len(msg))
            sys.stdout.flush()
            sleep(0.02)
        
        sys.stdout.write("PROSESS 3/4 DONE" + " "*len(msg)+"\n")
        sys.stdout.flush()
    
        idx = 0
        for v in vindex:
            idx += 1
            
            #make vertex group
            bpy.context.view_layer.objects.active = object
            bpy.ops.object.mode_set(mode='OBJECT')
            vg = object.vertex_groups.new(name='softbone.' + str(v))
            vg.add([int(v)], 1.0, "ADD")

            msg = "PROSESS 4/4: %i of %i" % (idx, len(vindex)-1)
            sys.stdout.write(msg + chr(8) * len(msg))
            sys.stdout.flush()
            sleep(0.02)
        
        sys.stdout.write("PROSESS 4/4 DONE" + " "*len(msg)+"\n")
        sys.stdout.write("COMPLETED!" + " "*len(msg)+"\n")
        sys.stdout.flush()

#                createBones(amt, e.verts)
#                
#        bpy.ops.object.mode_set(mode='OBJECT')
        
#        for ed in bpy.context.active_object.data.edges:
#            
#            if (ed.select == True):
#                print("edge index:{0: 2} v0:{0} v1:{1}".format(ed.index, ed.vertices[0], ed.vertices[1]))
        return {'FINISHED'}


def createArmature(name, loc):
    # アーマチュアとオブジェクトを作成
    amt = bpy.data.armatures.new(name+'Amt')
    ob = bpy.data.objects.new(name, amt)
    ob.location = loc
#    ob.show_name = True
 
    # シーンにオブジェクトをリンクしアクティブ化
    scn = bpy.context.collection
    scn.objects.link(ob)
    bpy.context.view_layer.objects.active = ob
#    ob.select_set(state=True)
 
    return [ob,amt]

def createBones(amt, verts):
 
    bone = amt.edit_bones.new('Bone')
    bone.head = verts[0].co
    bone.tail = verts[1].co
    
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
