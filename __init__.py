import bpy
from bpy.props import *

bl_info = {
    "name": "rigid bodys gen",
    "author": "12funkeys",
    "version": (0, 87),
    "blender": (2, 74, 0),
    "location": "pose > selected bones",
    "description": "Set rigid body and constraint easily",
    "warning": "",
    "support": "TESTING",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"
}

translation_dict = {
    "en_US" : {
        ("*", "Make Rigid Body Tools") : "Make Rigid Body Tools", 
        ("*", "Rigid Body Gen") : "Rigid Body Gen", 
        ("*", "Make Rigid Bodys") : "Make Rigid Bodys", 
        ("*", "Add Passive(on bones)") : "Add Passive(on bones)", 
        ("*", "make rigibodys move on bones") : "make rigibodys move on bones", 
        ("*", "Add Active") : "Add Active",
        ("*", "Add Joints") : "Add Joints",
        ("*", "Add Active & Joints") : "Add Active & Joints"
    },
    "ja_JP" : {
        ("*", "Make Rigid Body Tools") : "選択ボーン", 
        ("*", "Rigid Body Gen") : "剛体ツール", 
        ("*", "Make Rigid Bodys") : "選択ボーン", 
        ("*", "Add Passive(on bones)") : "基礎剛体の作成‐ボーン追従", 
        ("*", "make rigibodys move on bones") : "ボーンに追従する剛体を作成します", 
        ("*", "Add Active") : "基礎剛体の作成‐物理演算",
        ("*", "Add Joints") : "基礎Jointの作成",
        ("*", "Add Active & Joints") : "基礎剛体／連結Jointの作成"
    }
}

shapes = [
        ('MESH', 'Mesh', 'Mesh'),
        ('CONVEX_HULL', 'Convex Hull', 'Convex Hull'),
        ('CONE', 'Cone', 'Cone'),
        ('CYLINDER', 'Cylinder', 'Cylinder'),
        ('CAPSULE', 'Capsule', 'Capsule'),
        ('SPHERE', 'Sphere', 'Sphere'),
        ('BOX', 'Box', 'Box')]

types = [('MOTOR', 'Motor', 'Motor'),
            ('GENERIC_SPRING', 'Generic Spring', 'Generic Spring'),
            ('GENERIC', 'Generic', 'Generic')]

### add Tool Panel
class MenuRigidBodyTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Rigid Body Gen"
    bl_context = "posemode"
    bl_label = "Make Rigid Body Tools"


    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator(CreateRigidBodysOnBones.bl_idname, text=bpy.app.translations.pgettext("Add Passive(on bones)"), icon='BONE_DATA')
        col.operator(CreateRigidBodysPhysics.bl_idname, text=bpy.app.translations.pgettext("Add Active"), icon='PHYSICS')
        col.operator(CreateRigidBodysJoints.bl_idname, text=bpy.app.translations.pgettext("Add Joints"), icon='CONSTRAINT_DATA')
        col.operator(CreateRigidBodysPhysicsJoints.bl_idname, text=bpy.app.translations.pgettext("Add Active & Joints"), icon='MOD_PHYSICS')


### add MainMenu
class MenuRigidBodys(bpy.types.Menu):
    bl_idname = "menu.create_rigidbodys"
    bl_label = "Make Rigid Bodys"
    bl_description = "make rigibodys & constraint"

    def draw(self, context):
        layout = self.layout
        layout.operator(CreateRigidBodysOnBones.bl_idname, icon='BONE_DATA')
        layout.operator(CreateRigidBodysPhysics.bl_idname, icon='PHYSICS')
        layout.operator(CreateRigidBodysJoints.bl_idname, icon='CONSTRAINT_DATA')
        layout.operator(CreateRigidBodysPhysicsJoints.bl_idname, icon='MOD_PHYSICS')


### user prop
class UProp:

        rb_shape = EnumProperty(
            name='Shape',
            description='Choose Rigid Body Shape',
            items=shapes,
            #items=bpy.types.RigidBodyObject.collision_shape,
            default='CAPSULE')
            #update=update_shape)

        rc_dim = FloatVectorProperty(
            name = "Dimensions",
            description = "rigid body Dimensions XYZ",
            default = (1, 1, 1),
            subtype = 'XYZ',
            unit = 'NONE',
            min = 0,
            max = 5)

        rc_mass = FloatProperty(
            name = "Mass",
            description = "rigid body mass",
            default = 1.0,
            subtype = 'NONE',
            min = 0.001,)

        rc_friction = FloatProperty(
            name = "Friction",
            description = "rigid body friction",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        rc_bounciness = FloatProperty(
            name = "Bounciness",
            description = "rigid body bounciness",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        rc_translation = FloatProperty(
            name = "Translation",
            description = "rigid body translation",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        rc_rotation = FloatProperty(
            name = "Rotation",
            description = "rigid body rotation",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)


        jo_type = EnumProperty(
            name='Type',
            description='Choose Contstraint Type',
            items=types,
            default='GENERIC_SPRING')

        jo_dim = FloatVectorProperty(
            name = "joint Dimensions",
            description = "joint Dimensions XYZ",
            default = (1, 1, 1),
            subtype = 'XYZ',
            unit = 'NONE',
            min = 0,
            max = 5)

        jo_limit_lin_x = BoolProperty(
            name='X Axis',
            description='limit x',
            default=True,
            options={'ANIMATABLE'})

        jo_limit_lin_y = BoolProperty(
            name='Y Axis',
            description='limit y',
            default=True)

        jo_limit_lin_z = BoolProperty(
            name='Z Axis',
            description='limit z',
            default=True)

        jo_limit_lin_x_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_lin_x_lower",
            default = 0,
            subtype = 'NONE')

        jo_limit_lin_y_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_lin_y_lower",
            default = 0,
            subtype = 'NONE')

        jo_limit_lin_z_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_lin_z_lower",
            default = 0,
            subtype = 'NONE')

        jo_limit_lin_x_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_lin_x_upper",
            default = 0,
            subtype = 'NONE')

        jo_limit_lin_y_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_lin_y_upper",
            default = 0,
            subtype = 'NONE')

        jo_limit_lin_z_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_lin_z_upper",
            default = 0,
            subtype = 'NONE')

        jo_limit_ang_x = BoolProperty(
            name='X Angle',
            description='Angle limit x',
            default=True,
            options={'ANIMATABLE'})

        jo_limit_ang_y = BoolProperty(
            name='Y Angle',
            description='Angle limit y',
            default=True)

        jo_limit_ang_z = BoolProperty(
            name='Z Angle',
            description='Angle limit z',
            default=True)

        jo_limit_ang_x_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_ang_x_lower",
            default = -0.785398,
            subtype = 'ANGLE')

        jo_limit_ang_y_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_ang_y_lower",
            default = -0.785398,
            subtype = 'ANGLE')

        jo_limit_ang_z_lower = FloatProperty(
            name = "Lower",
            description = "joint limit_ang_z_lower",
            default = -0.785398,
            subtype = 'ANGLE')

        jo_limit_ang_x_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_ang_x_upper",
            default = 0.785398,
            subtype = 'ANGLE')

        jo_limit_ang_y_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_ang_y_upper",
            default = 0.785398,
            subtype = 'ANGLE')

        jo_limit_ang_z_upper = FloatProperty(
            name = "Upper",
            description = "joint limit_ang_z_upper",
            default = 0.785398,
            subtype = 'ANGLE')


        jo_use_spring_x = BoolProperty(
            name='X',
            description='use spring x',
            default=False)

        jo_use_spring_y = BoolProperty(
            name='Y',
            description='use spring y',
            default=False)

        jo_use_spring_z = BoolProperty(
            name='Z',
            description='use spring z',
            default=False)

        jo_spring_stiffness_x = FloatProperty(
            name = "Stiffness",
            description = "Stiffness on the X Axis",
            default = 10.000,
            subtype = 'NONE',
            min = 0)

        jo_spring_stiffness_y = FloatProperty(
            name = "Stiffness",
            description = "Stiffness on the Y Axis",
            default = 10.000,
            subtype = 'NONE',
            min = 0)
            
        jo_spring_stiffness_z = FloatProperty(
            name = "Stiffness",
            description = "Stiffness on the Z Axis",
            default = 10.000,
            subtype = 'NONE',
            min = 0)

        jo_spring_damping_x = FloatProperty(
            name = "Damping X",
            description = "Damping on the X Axis",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        jo_spring_damping_y = FloatProperty(
            name = "Damping Y",
            description = "Damping on the Y Axis",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)

        jo_spring_damping_z = FloatProperty(
            name = "Damping Z",
            description = "Damping on the Z Axis",
            default = 0.5,
            subtype = 'NONE',
            min = 0,
            max = 1)
            
        
        jo_constraint_object = BoolProperty(
            name='Auto Constraint Object',
            description='Constraint Object',
            default=True)

        rc_rootbody_passive = BoolProperty(
            name='Passive',
            description='Rigid Body Type Passive',
            default=True)

        rc_add_pole_rootbody = BoolProperty(
            name='Add Pole Object',
            description='Add Pole Object',
            default=True)

        rc_rootbody_animated = BoolProperty(
            name='animated',
            description='Root Rigid Body sets animated',
            default=True)

        rc_parent_armature = BoolProperty(
            name='Parent to armature',
            description='Parent to armature',
            default=True)


### Create Rigid Bodys On Bones
class CreateRigidBodysOnBones(bpy.types.Operator):

    bl_idname = "rigidbody.on_bones"
    bl_label = "Add Passive(on bones)"
    bl_description = "make rigibodys move on bones"
    bl_options = {'REGISTER', 'UNDO'}
    
    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30    

    ###instance UProp.rigidbody
    p_rb_shape = UProp.rb_shape
    p_rb_dim = UProp.rc_dim
    p_rb_mass = UProp.rc_mass
    p_rb_friction = UProp.rc_friction
    p_rb_bounciness = UProp.rc_bounciness
    p_rb_translation = UProp.rc_translation
    p_rb_rotation = UProp.rc_rotation
    p_rb_rootbody_passive = UProp.rc_rootbody_passive
    p_rb_rootbody_animated = UProp.rc_rootbody_animated
    p_rb_parent_armature = UProp.rc_parent_armature


    def __init__(self):
        
        self.p_rb_dim = (1, 1, 1)

    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}
                        

        layout = self.layout

        # Branch specs
        #layout.label('Tree Definition')

        #layout.prop(self,'chooseSet')
        box = layout.box()
        box.prop(self, 'p_rb_shape')
        box.prop(self, 'p_rb_dim')
        box.prop(self, 'p_rb_mass')
        box.prop(self, 'p_rb_friction')
        box.prop(self, 'p_rb_bounciness')
        box.label(text="Damping:")
        box.prop(self, 'p_rb_translation')
        box.prop(self, 'p_rb_rotation')
        box.prop(self, 'p_rb_rootbody_passive')
        box.prop(self, 'p_rb_rootbody_animated')
        box.prop(self, 'p_rb_parent_armature')

    ### 
    def execute(self, context):
        
        #bpy.ops.screen.frame_jump(end=False)
        #bpy.ops.ptcache.free_bake_all()

        #bpy.context.RigidBodyWorld.point_cache.frame_start = 1
        
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        #self.report({'INFO'}, ob.data)

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

        #new material
        mat = add_mat(self, context)
        #bpy.ops.material.new()
        #nm = bpy.data.materials[-1]
        #nm.name = "rigid_mat"
        #nm.use_shadeless = True
        #nm.use_transparency = True
        #nm.alpha = 0
        #nm.use_shadows = False
        #nm.use_raytrace = False

        if len(bpy.context.selected_pose_bones) == 0:
            return {'FINISHED'}

        for selected_bones in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bones.vector[0]))            
            
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bones.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            rc.name = "rbg." + selected_bones.name
            rc.show_x_ray = True
            rc.show_transparent = True
            rc.data.materials.append(mat)
            rc.hide_render = True

            ###Material set
            bpy.ops.object.constraint_add(type='DAMPED_TRACK')
            dt = bpy.context.object.constraints["Damped Track"]
            dt.target = ob
            dt.subtarget = selected_bones.name
            dt.head_tail = 1
            dt.track_axis = 'TRACK_Z'
            
            ### Apply Tranceform
            bpy.ops.object.visual_transform_apply()
            rc.constraints.remove(dt)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bones.length * self.init_rc_dimX * self.p_rb_dim[0], 
                selected_bones.length * self.init_rc_dimY * self.p_rb_dim[1], 
                selected_bones.length * self.init_rc_dimZ * self.p_rb_dim[2]]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            if self.p_rb_rootbody_passive == True:
                bpy.context.object.rigid_body.type = "PASSIVE"
            else:
                bpy.context.object.rigid_body.type = "ACTIVE"

            bpy.context.object.rigid_body.collision_shape = self.p_rb_shape
            bpy.context.object.rigid_body.kinematic = self.p_rb_rootbody_animated
            bpy.context.object.rigid_body.mass = self.p_rb_mass
            bpy.context.object.rigid_body.friction = self.p_rb_friction
            bpy.context.object.rigid_body.restitution = self.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = self.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = self.p_rb_rotation


            ### Child OF
            CoC = rc.constraints.new("CHILD_OF")
            CoC.name = 'Child_Of_' + selected_bones.name
            CoC.target = ob
            CoC.subtarget = selected_bones.name
            
            #without ops way to childof_set_inverse
            sub_target = bpy.data.objects[ob.name].pose.bones[selected_bones.name]
            #self.report({'INFO'}, str(sub_target))
            CoC.inverse_matrix = sub_target.matrix.inverted()   
            rc.update_tag({'OBJECT'})
            bpy.context.scene.update()

            #parent to armature
            if self.p_rb_parent_armature == True:
                rc.parent = ob

        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='DESELECT')  
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}

#
class CreateRigidBodysPhysics(bpy.types.Operator):

    bl_idname = "rigidbody.physics"
    bl_label = "Add Active"
    bl_description = "make physics engine on rigibodys"
    bl_options = {'REGISTER', 'UNDO'}

    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30    

    ###instance UProp.rigidbody
    p_rb_shape = UProp.rb_shape
    p_rb_dim = UProp.rc_dim
    p_rb_mass = UProp.rc_mass
    p_rb_friction = UProp.rc_friction
    p_rb_bounciness = UProp.rc_bounciness
    p_rb_translation = UProp.rc_translation
    p_rb_rotation = UProp.rc_rotation
    #p_rb_rootbody_passive = UProp.rc_rootbody_passive
    p_rb_rootbody_animated = UProp.rc_rootbody_animated
    p_rb_parent_armature = UProp.rc_parent_armature

    def __init__(self):
        
        self.p_rb_dim = (1, 1, 1)

    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        layout = self.layout

        # Branch specs
        #layout.label('Tree Definition')

        #layout.prop(self,'chooseSet')
        box = layout.box()
        box.prop(self, 'p_rb_shape')
        box.prop(self, 'p_rb_dim')
        box.prop(self, 'p_rb_mass')
        box.prop(self, 'p_rb_friction')
        box.prop(self, 'p_rb_bounciness')
        box.prop(self, 'p_rb_translation')
        box.prop(self, 'p_rb_rotation')
        #box.prop(self, 'p_rb_rootbody_passive')
        box.prop(self, 'p_rb_rootbody_animated')
        box.prop(self, 'p_rb_parent_armature')

    ### 
    def execute(self, context):
        
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        #self.report({'INFO'}, ob.data)

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

        #new material
        mat = add_mat(self, context)

        for selected_bones in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bones.vector[0]))            
            
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bones.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            bpy.context.object.name = "rbg." + selected_bones.name
            rc.show_x_ray = True
            rc.show_transparent = True
            rc.data.materials.append(mat)
            bpy.data.objects[rc.name].hide_render = True

            ###Material set
            bpy.ops.object.constraint_add(type='DAMPED_TRACK')
            dt = bpy.context.object.constraints["Damped Track"]
            dt.target = ob
            dt.subtarget = selected_bones.name
            dt.head_tail = 1
            dt.track_axis = 'TRACK_Z'
            
            ### Apply Tranceform
            bpy.ops.object.visual_transform_apply()
            rc.constraints.remove(dt)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bones.length * self.init_rc_dimX * self.p_rb_dim[0], 
                selected_bones.length * self.init_rc_dimY * self.p_rb_dim[1], 
                selected_bones.length * self.init_rc_dimZ * self.p_rb_dim[2]]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            #if self.p_rb_rootbody_passive == True:
            #    bpy.context.object.rigid_body.type = "PASSIVE"
            #else:
            bpy.context.object.rigid_body.type = "ACTIVE"

            bpy.context.object.rigid_body.collision_shape = self.p_rb_shape
            bpy.context.object.rigid_body.kinematic = self.p_rb_rootbody_animated
            bpy.context.object.rigid_body.mass = self.p_rb_mass
            bpy.context.object.rigid_body.friction = self.p_rb_friction
            bpy.context.object.rigid_body.restitution = self.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = self.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = self.p_rb_rotation

            ### Child OF
            bpy.context.scene.objects.active = ob
            bpy.ops.pose.armature_apply()
            #bpy.ops.pose.visual_transform_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bones.name]
            ab = bpy.context.active_pose_bone


            #self.report({'INFO'}, str(rc.name))
            #CoC = bpy.ops.pose.constraint_add(type='CHILD_OF')
            CoC = ab.constraints.new("CHILD_OF")
            #self.report({'INFO'}, "info:" + str(CoC))
            CoC.name = 'Child_Of_' + rc.name
            CoC.target = rc
            
            #bpy.ops.constraint.childof_set_inverse(constraint=CoC.name, owner=ab)
            
            #without ops way to childof_set_inverse
            CoC_target = rc
            #self.report({'INFO'}, str(rc))
            CoC.inverse_matrix = CoC_target.matrix_world.inverted()   
            rc.update_tag({'OBJECT'})
            bpy.context.scene.update()

            ###parent none
            bpy.ops.object.editmode_toggle()
            bpy.context.active_bone.parent = None
            #bpy.context.active_bone.use_connect = False
            #bpy.context.active_bone.use_inherit_rotation = False
            bpy.ops.object.posemode_toggle()

            #parent to armature
            if self.p_rb_parent_armature == True:
                rc.parent = ob
            
        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle() 
        bpy.ops.pose.select_all(action='DESELECT')
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}
    
#
class CreateRigidBodysJoints(bpy.types.Operator):

    bl_idname = "rigidbody.joints"
    bl_label = "Add Joints"
    bl_description = "add Add Joints on bones"
    bl_options = {'REGISTER', 'UNDO'}

    init_joint_dimX = 0.33
    init_joint_dimY = 0.33
    init_joint_dimZ = 0.33    

    ###instance UProp.joint
    joint_type = UProp.jo_type
    joint_dim = UProp.jo_dim
    joint_Axis_limit_x = UProp.jo_limit_lin_x
    joint_Axis_limit_y = UProp.jo_limit_lin_y
    joint_Axis_limit_z = UProp.jo_limit_lin_z
    joint_Axis_limit_x_lower = UProp.jo_limit_lin_x_lower
    joint_Axis_limit_y_lower = UProp.jo_limit_lin_y_lower
    joint_Axis_limit_z_lower = UProp.jo_limit_lin_z_lower
    joint_Axis_limit_x_upper = UProp.jo_limit_lin_x_upper
    joint_Axis_limit_y_upper = UProp.jo_limit_lin_y_upper
    joint_Axis_limit_z_upper = UProp.jo_limit_lin_z_upper
    joint_Angle_limit_x = UProp.jo_limit_ang_x
    joint_Angle_limit_y = UProp.jo_limit_ang_y
    joint_Angle_limit_z = UProp.jo_limit_ang_z
    joint_Angle_limit_x_lower = UProp.jo_limit_ang_x_lower
    joint_Angle_limit_y_lower = UProp.jo_limit_ang_y_lower
    joint_Angle_limit_z_lower = UProp.jo_limit_ang_z_lower
    joint_Angle_limit_x_upper = UProp.jo_limit_ang_x_upper
    joint_Angle_limit_y_upper = UProp.jo_limit_ang_y_upper
    joint_Angle_limit_z_upper = UProp.jo_limit_ang_z_upper
    joint_use_spring_x = UProp.jo_use_spring_x
    joint_use_spring_y = UProp.jo_use_spring_y
    joint_use_spring_z = UProp.jo_use_spring_z
    joint_spring_stiffness_x = UProp.jo_spring_stiffness_x
    joint_spring_stiffness_y = UProp.jo_spring_stiffness_y
    joint_spring_stiffness_z = UProp.jo_spring_stiffness_z
    joint_spring_damping_x = UProp.jo_spring_damping_x
    joint_spring_damping_y = UProp.jo_spring_damping_y
    joint_spring_damping_z = UProp.jo_spring_damping_z
    p_rb_parent_armature = UProp.rc_parent_armature

    def __init__(self):

        self.joint_dim = (1, 1, 1)

    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        layout = self.layout

        # Branch specs
        #layout.label('Tree Definition')

        #layout.prop(self,'chooseSet')
        box = layout.box()
        box.prop(self, 'joint_type')
        box.prop(self, 'joint_dim')


        col = box.column(align=True)
        col.label("Limits:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_x', toggle=True)
        sub.prop(self, 'joint_Axis_limit_x_lower')
        sub.prop(self, 'joint_Axis_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_y', toggle=True)
        sub.prop(self, 'joint_Axis_limit_y_lower')
        sub.prop(self, 'joint_Axis_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_z', toggle=True)
        sub.prop(self, 'joint_Axis_limit_z_lower')  
        sub.prop(self, 'joint_Axis_limit_z_upper')

        #col = layout.column(align=True)

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_x', toggle=True)
        sub.prop(self, 'joint_Angle_limit_x_lower')
        sub.prop(self, 'joint_Angle_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_y', toggle=True)
        sub.prop(self, 'joint_Angle_limit_y_lower')
        sub.prop(self, 'joint_Angle_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_z', toggle=True)
        sub.prop(self, 'joint_Angle_limit_z_lower')  
        sub.prop(self, 'joint_Angle_limit_z_upper')


        #col = layout.column(align=True)
        col.label("Springs:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_x', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_x')
        sub.prop(self, 'joint_spring_damping_x')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_y', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_y')
        sub.prop(self, 'joint_spring_damping_y')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_z', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_z')  
        sub.prop(self, 'joint_spring_damping_z')
        
        col.prop(self, 'p_rb_parent_armature')


    ### 
    def execute(self, context):
 
        add_RigidBody_World()        
        
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        #self.report({'INFO'}, ob.data)

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

        #new material
        mat = add_mat(self, context)

        for selected_bones in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bones.vector[0]))            
            
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bones.head, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            bpy.context.object.name = "joint." + selected_bones.name
            rc.show_x_ray = True
            rc.show_transparent = True
            rc.show_wire = True
            rc.data.materials.append(mat)
            bpy.data.objects[rc.name].hide_render = True
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bones.length * self.init_joint_dimX * self.joint_dim[0], 
                selected_bones.length * self.init_joint_dimY * self.joint_dim[1], 
                selected_bones.length * self.init_joint_dimZ * self.joint_dim[2]]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.constraint_add()
            bpy.context.object.rigid_body_constraint.type = self.joint_type
            bpy.context.object.rigid_body_constraint.use_breaking = False
            bpy.context.object.rigid_body_constraint.use_override_solver_iterations = True
            bpy.context.object.rigid_body_constraint.breaking_threshold = 10
            bpy.context.object.rigid_body_constraint.solver_iterations = 10

            bpy.context.object.rigid_body_constraint.use_limit_lin_x = self.joint_Axis_limit_x
            bpy.context.object.rigid_body_constraint.use_limit_lin_y = self.joint_Axis_limit_y
            bpy.context.object.rigid_body_constraint.use_limit_lin_z = self.joint_Axis_limit_z
            bpy.context.object.rigid_body_constraint.limit_lin_x_lower = self.joint_Axis_limit_x_lower
            bpy.context.object.rigid_body_constraint.limit_lin_y_lower = self.joint_Axis_limit_y_lower
            bpy.context.object.rigid_body_constraint.limit_lin_z_lower = self.joint_Axis_limit_z_lower
            bpy.context.object.rigid_body_constraint.limit_lin_x_upper = self.joint_Axis_limit_x_upper
            bpy.context.object.rigid_body_constraint.limit_lin_y_upper = self.joint_Axis_limit_y_upper
            bpy.context.object.rigid_body_constraint.limit_lin_z_upper = self.joint_Axis_limit_z_upper

            bpy.context.object.rigid_body_constraint.use_limit_ang_x = self.joint_Angle_limit_x
            bpy.context.object.rigid_body_constraint.use_limit_ang_y = self.joint_Angle_limit_y
            bpy.context.object.rigid_body_constraint.use_limit_ang_z = self.joint_Angle_limit_z
            bpy.context.object.rigid_body_constraint.limit_ang_x_lower = self.joint_Angle_limit_x_lower
            bpy.context.object.rigid_body_constraint.limit_ang_y_lower = self.joint_Angle_limit_y_lower
            bpy.context.object.rigid_body_constraint.limit_ang_z_lower = self.joint_Angle_limit_z_lower
            bpy.context.object.rigid_body_constraint.limit_ang_x_upper = self.joint_Angle_limit_x_upper
            bpy.context.object.rigid_body_constraint.limit_ang_y_upper = self.joint_Angle_limit_y_upper
            bpy.context.object.rigid_body_constraint.limit_ang_z_upper = self.joint_Angle_limit_z_upper

            bpy.context.object.rigid_body_constraint.use_spring_x = self.joint_use_spring_x
            bpy.context.object.rigid_body_constraint.use_spring_y = self.joint_use_spring_y
            bpy.context.object.rigid_body_constraint.use_spring_z = self.joint_use_spring_z
            bpy.context.object.rigid_body_constraint.spring_stiffness_x = self.joint_spring_stiffness_x
            bpy.context.object.rigid_body_constraint.spring_stiffness_y = self.joint_spring_stiffness_y
            bpy.context.object.rigid_body_constraint.spring_stiffness_z = self.joint_spring_stiffness_z
            bpy.context.object.rigid_body_constraint.spring_damping_x = self.joint_spring_damping_x
            bpy.context.object.rigid_body_constraint.spring_damping_y = self.joint_spring_damping_y
            bpy.context.object.rigid_body_constraint.spring_damping_z = self.joint_spring_damping_z

            ###constraint.object
            #bpy.context.object.rigid_body_constraint.object1 = bpy.data.objects["rigidbody.Bone"]
            #bpy.context.object.rigid_body_constraint.object2 = bpy.data.objects["rigidbody.Bone.001"]



            #parent to armature
            if self.p_rb_parent_armature == True:
                rc.parent = ob

        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='DESELECT')
 
        
        self.report({'INFO'}, "OK")
        return {'FINISHED'}

class CreateRigidBodysPhysicsJoints(bpy.types.Operator):

    bl_idname = "rigidbody.physics_joints"
    bl_label = "Add Active & Joints"
    bl_description = "Add Active & Joints"
    bl_options = {'REGISTER', 'UNDO'}


    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30    

    #pole_dict = {}

    ###instance UProp.rigidbody
    p_rb_shape = UProp.rb_shape
    p_rb_dim = UProp.rc_dim
    p_rb_mass = UProp.rc_mass
    p_rb_friction = UProp.rc_friction
    p_rb_bounciness = UProp.rc_bounciness
    p_rb_translation = UProp.rc_translation
    p_rb_rotation = UProp.rc_rotation
    p_rb_add_pole_rootbody = UProp.rc_add_pole_rootbody
    p_rb_parent_armature = UProp.rc_parent_armature

    init_joint_dimX = 0.33
    init_joint_dimY = 0.33
    init_joint_dimZ = 0.33    

    ###instance UProp.joint
    joint_type = UProp.jo_type
    joint_dim = UProp.jo_dim
    joint_Axis_limit_x = UProp.jo_limit_lin_x
    joint_Axis_limit_y = UProp.jo_limit_lin_y
    joint_Axis_limit_z = UProp.jo_limit_lin_z
    joint_Axis_limit_x_lower = UProp.jo_limit_lin_x_lower
    joint_Axis_limit_y_lower = UProp.jo_limit_lin_y_lower
    joint_Axis_limit_z_lower = UProp.jo_limit_lin_z_lower
    joint_Axis_limit_x_upper = UProp.jo_limit_lin_x_upper
    joint_Axis_limit_y_upper = UProp.jo_limit_lin_y_upper
    joint_Axis_limit_z_upper = UProp.jo_limit_lin_z_upper
    joint_Angle_limit_x = UProp.jo_limit_ang_x
    joint_Angle_limit_y = UProp.jo_limit_ang_y
    joint_Angle_limit_z = UProp.jo_limit_ang_z
    joint_Angle_limit_x_lower = UProp.jo_limit_ang_x_lower
    joint_Angle_limit_y_lower = UProp.jo_limit_ang_y_lower
    joint_Angle_limit_z_lower = UProp.jo_limit_ang_z_lower
    joint_Angle_limit_x_upper = UProp.jo_limit_ang_x_upper
    joint_Angle_limit_y_upper = UProp.jo_limit_ang_y_upper
    joint_Angle_limit_z_upper = UProp.jo_limit_ang_z_upper
    joint_use_spring_x = UProp.jo_use_spring_x
    joint_use_spring_y = UProp.jo_use_spring_y
    joint_use_spring_z = UProp.jo_use_spring_z
    joint_spring_stiffness_x = UProp.jo_spring_stiffness_x
    joint_spring_stiffness_y = UProp.jo_spring_stiffness_y
    joint_spring_stiffness_z = UProp.jo_spring_stiffness_z
    joint_spring_damping_x = UProp.jo_spring_damping_x
    joint_spring_damping_y = UProp.jo_spring_damping_y
    joint_spring_damping_z = UProp.jo_spring_damping_z
    joint_constraint_object = UProp.jo_constraint_object


    def __init__(self):
        
        self.p_rb_dim = (1, 1, 1)
        self.joint_dim = (1, 1, 1)

    def draw(self, context):

        #if len(bpy.context.selected_pose_bones) == 0:
        #    layout = self.layout
        #    layout.label("You shuld select bone first", icon="ERROR")
        #    return {'FINISHED'}

        ###Rigid Body Object
        layout = self.layout

        box = layout.box()
        box.prop(self, 'p_rb_shape')
        box.prop(self, 'p_rb_dim')
        box.prop(self, 'p_rb_mass')
        box.prop(self, 'p_rb_friction')
        box.prop(self, 'p_rb_bounciness')
        box.prop(self, 'p_rb_translation')
        box.prop(self, 'p_rb_rotation')


        #Joint Object
        layout = self.layout

        box = layout.box()
        box.prop(self, 'joint_type')
        box.prop(self, 'joint_constraint_object')
        box.prop(self, 'p_rb_add_pole_rootbody')
        box.prop(self, 'p_rb_parent_armature')
        box.prop(self, 'joint_dim')

        col = box.column(align=True)
        col.label("Limits:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_x', toggle=True)
        sub.prop(self, 'joint_Axis_limit_x_lower')
        sub.prop(self, 'joint_Axis_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_y', toggle=True)
        sub.prop(self, 'joint_Axis_limit_y_lower')
        sub.prop(self, 'joint_Axis_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Axis_limit_z', toggle=True)
        sub.prop(self, 'joint_Axis_limit_z_lower')  
        sub.prop(self, 'joint_Axis_limit_z_upper')

        #col = layout.column(align=True)

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_x', toggle=True)
        sub.prop(self, 'joint_Angle_limit_x_lower')
        sub.prop(self, 'joint_Angle_limit_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_y', toggle=True)
        sub.prop(self, 'joint_Angle_limit_y_lower')
        sub.prop(self, 'joint_Angle_limit_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_Angle_limit_z', toggle=True)
        sub.prop(self, 'joint_Angle_limit_z_lower')  
        sub.prop(self, 'joint_Angle_limit_z_upper')


        #col = layout.column(align=True)
        col.label("Springs:")

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_x', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_x')
        sub.prop(self, 'joint_spring_damping_x')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_y', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_y')
        sub.prop(self, 'joint_spring_damping_y')

        row = col.row(align=True)
        sub = row.row(align=True)
        #sub.alignment = 'EXPAND'
        sub.prop(self, 'joint_use_spring_z', toggle=True)
        sub.prop(self, 'joint_spring_stiffness_z')  
        sub.prop(self, 'joint_spring_damping_z')

    # 
    def execute(self, context):

        add_RigidBody_World()        
        
        ###selected Armature
        ob = bpy.context.active_object
        acrive_layer = bpy.context.scene.active_layer
        self.report({'INFO'}, "ob:" + str(ob))

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

        #new material
        mat = add_mat(self, context)
        parent_bones_ob = ""
        
        pole_dict = {}
        
        wm = bpy.context.window_manager 

        spb = bpy.context.selected_pose_bones
        tot = len(spb)
        wm.progress_begin(0, tot)
        i = 0

        self.report({'INFO'}, "pole_dict:" + str(pole_dict)) 

        for selected_bones in spb:
            #self.report({'INFO'}, str(selected_bones.vector[0]))            

            i += 1
            wm.progress_update(i)

            ###Joint Session
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bones.head, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            jc = bpy.context.active_object
            jc.name = "joint." + ob.name + "." + selected_bones.name
            jc.show_x_ray = True
            jc.show_transparent = True
            jc.show_wire = True
            jc.data.materials.append(mat)
            bpy.data.objects[jc.name].hide_render = True
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bones.length * self.init_joint_dimX * self.joint_dim[0], 
                selected_bones.length * self.init_joint_dimY * self.joint_dim[1], 
                selected_bones.length * self.init_joint_dimZ * self.joint_dim[2]]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.constraint_add()
            jc.rigid_body_constraint.type = self.joint_type
            jc.rigid_body_constraint.use_breaking = False
            jc.rigid_body_constraint.use_override_solver_iterations = True
            jc.rigid_body_constraint.breaking_threshold = 10
            jc.rigid_body_constraint.solver_iterations = 10

            jc.rigid_body_constraint.use_limit_lin_x = self.joint_Axis_limit_x
            jc.rigid_body_constraint.use_limit_lin_y = self.joint_Axis_limit_y
            jc.rigid_body_constraint.use_limit_lin_z = self.joint_Axis_limit_z
            jc.rigid_body_constraint.limit_lin_x_lower = self.joint_Axis_limit_x_lower
            jc.rigid_body_constraint.limit_lin_y_lower = self.joint_Axis_limit_y_lower
            jc.rigid_body_constraint.limit_lin_z_lower = self.joint_Axis_limit_z_lower
            jc.rigid_body_constraint.limit_lin_x_upper = self.joint_Axis_limit_x_upper
            jc.rigid_body_constraint.limit_lin_y_upper = self.joint_Axis_limit_y_upper
            jc.rigid_body_constraint.limit_lin_z_upper = self.joint_Axis_limit_z_upper

            jc.rigid_body_constraint.use_limit_ang_x = self.joint_Angle_limit_x
            jc.rigid_body_constraint.use_limit_ang_y = self.joint_Angle_limit_y
            jc.rigid_body_constraint.use_limit_ang_z = self.joint_Angle_limit_z
            jc.rigid_body_constraint.limit_ang_x_lower = self.joint_Angle_limit_x_lower
            jc.rigid_body_constraint.limit_ang_y_lower = self.joint_Angle_limit_y_lower
            jc.rigid_body_constraint.limit_ang_z_lower = self.joint_Angle_limit_z_lower
            jc.rigid_body_constraint.limit_ang_x_upper = self.joint_Angle_limit_x_upper
            jc.rigid_body_constraint.limit_ang_y_upper = self.joint_Angle_limit_y_upper
            jc.rigid_body_constraint.limit_ang_z_upper = self.joint_Angle_limit_z_upper

            jc.rigid_body_constraint.use_spring_x = self.joint_use_spring_x
            jc.rigid_body_constraint.use_spring_y = self.joint_use_spring_y
            jc.rigid_body_constraint.use_spring_z = self.joint_use_spring_z
            jc.rigid_body_constraint.spring_stiffness_x = self.joint_spring_stiffness_x
            jc.rigid_body_constraint.spring_stiffness_y = self.joint_spring_stiffness_y
            jc.rigid_body_constraint.spring_stiffness_z = self.joint_spring_stiffness_z
            jc.rigid_body_constraint.spring_damping_x = self.joint_spring_damping_x
            jc.rigid_body_constraint.spring_damping_y = self.joint_spring_damping_y
            jc.rigid_body_constraint.spring_damping_z = self.joint_spring_damping_z

            self.report({'INFO'}, "selected_bones.parent:" + str(selected_bones.parent))
            if selected_bones.parent is not None and selected_bones.parent not in spb and selected_bones.parent not in pole_dict and self.p_rb_add_pole_rootbody == True:

                    ###Create Rigidbody Cube
                    bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bones.parent.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
                    bpy.context.object.layers[acrive_layer] = True
                    bpy.context.object.layers[19] = False
                    rc2 = bpy.context.active_object
                    rc2.name = "rbg.pole." + ob.name + "." + selected_bones.parent.name
                    rc2.show_x_ray = True
                    rc2.show_transparent = True
                    rc2.data.materials.append(mat)
                    rc2.hide_render = True

                    ###Material set
                    #bpy.ops.object.constraint_add(type='DAMPED_TRACK')
                    #dt = bpy.context.object.constraints["Damped Track"]
                    #dt.target = ob
                    #dt.subtarget = selected_bones.name
                    #dt.head_tail = 1
                    #dt.track_axis = 'TRACK_Z'
                    
                    ### Apply Tranceform
                    #bpy.ops.object.visual_transform_apply()
                    #rc2.constraints.remove(dt)
                    
                    ### Rigid Body Dimensions
                    bpy.context.object.dimensions = [
                        selected_bones.parent.length * self.init_joint_dimX, 
                        selected_bones.parent.length * self.init_joint_dimY, 
                        selected_bones.parent.length * self.init_joint_dimZ]
                    
                    ### Scale Apply
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

                    ### Set Rigid Body
                    bpy.ops.rigidbody.object_add()

                    rc2.rigid_body.type = "PASSIVE"
                    rc2.rigid_body.collision_shape = "BOX"
                    #rc2.rigid_body.collision_shape = self.p_rb_shape
                    #rc2.rigid_body.mass = self.p_rb_mass
                    #rc2.rigid_body.friction = self.p_rb_friction
                    #rc2.rigid_body.restitution = self.p_rb_bounciness
                    #rc2.rigid_body.linear_damping = self.p_rb_translation
                    #rc2.rigid_body.angular_damping = self.p_rb_rotation
                    rc2.rigid_body.kinematic = True

                    ### Child OF
                    CoC2 = rc2.constraints.new("CHILD_OF")
                    CoC2.name = 'Child_Of_' + selected_bones.parent.name
                    CoC2.target = ob
                    CoC2.subtarget = selected_bones.parent.name
                    
                    #without ops way to childof_set_inverse
                    sub_target = bpy.data.objects[ob.name].pose.bones[selected_bones.parent.name]
                    #self.report({'INFO'}, str(sub_target))
                    CoC2.inverse_matrix = sub_target.matrix.inverted()   
                    rc2.update_tag({'OBJECT'})
                    bpy.context.scene.update()

                    #parent to armature
                    #bpy.context.scene.objects.active = ob
                    if self.p_rb_parent_armature == True:
                        rc2.parent = ob


            ###constraint.object1
            
            if selected_bones.parent is not None and selected_bones.parent not in spb and self.p_rb_add_pole_rootbody == True:
                    
                if selected_bones.parent not in pole_dict:
                    pole_dict[selected_bones.parent] = rc2 
                    self.report({'INFO'}, "pole_dict:" + str(pole_dict)) 
                    jc.rigid_body_constraint.object1 = rc2
                    parent_bones_ob = "rbg." + ob.name + "." + selected_bones.name
                else:
                    jc.rigid_body_constraint.object1 = pole_dict[selected_bones.parent]
                    parent_bones_ob = "rbg." + ob.name + "." + selected_bones.name


            else:
                if parent_bones_ob != "":
                    jc.rigid_body_constraint.object1 = bpy.data.objects[parent_bones_ob]

                parent_bones_ob = "rbg." + ob.name + "." + selected_bones.name



            #self.report({'INFO'}, "recursive:" + str(selected_bones.children_recursive)) 
            #self.report({'INFO'}, "parent_bones_ob:" + str(parent_bones_ob)) 


            #parent to armature
            if self.p_rb_parent_armature == True:
            #bpy.context.scene.objects.active = ob
                jc.parent = ob


            ###Rigid Body Session            
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(radius=1, view_align=False, enter_editmode=False, location=selected_bones.center, layers=(False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True))
            bpy.context.object.layers[acrive_layer] = True
            bpy.context.object.layers[19] = False
            rc = bpy.context.active_object
            bpy.context.object.name = parent_bones_ob
            rc.show_x_ray = True
            rc.show_transparent = True
            rc.data.materials.append(mat)
            bpy.data.objects[rc.name].hide_render = True

            ###constraint.object2
            #self.report({'INFO'}, "parent_bones_ob:" + str(parent_bones_ob))
            if parent_bones_ob != "":            
                jc.rigid_body_constraint.object2 = bpy.data.objects[parent_bones_ob]

            if len(selected_bones.children_recursive) == 0:
                parent_bones_ob = ""

            ###Material set
            bpy.ops.object.constraint_add(type='DAMPED_TRACK')
            dt = bpy.context.object.constraints["Damped Track"]
            dt.target = ob
            dt.subtarget = selected_bones.name
            dt.head_tail = 1
            dt.track_axis = 'TRACK_Z'
            
            ### Apply Tranceform
            bpy.ops.object.visual_transform_apply()
            rc.constraints.remove(dt)
            
            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bones.length * self.init_rc_dimX * self.p_rb_dim[0], 
                selected_bones.length * self.init_rc_dimY * self.p_rb_dim[1], 
                selected_bones.length * self.init_rc_dimZ * self.p_rb_dim[2]]
            
            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            bpy.context.object.rigid_body.type = "ACTIVE"
            bpy.context.object.rigid_body.collision_shape = self.p_rb_shape
            bpy.context.object.rigid_body.mass = self.p_rb_mass
            bpy.context.object.rigid_body.friction = self.p_rb_friction
            bpy.context.object.rigid_body.restitution = self.p_rb_bounciness
            bpy.context.object.rigid_body.linear_damping = self.p_rb_translation
            bpy.context.object.rigid_body.angular_damping = self.p_rb_rotation

            ### Child OF
            bpy.context.scene.objects.active = ob
            bpy.ops.pose.armature_apply()
            #bpy.ops.pose.visual_transform_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bones.name]
            ab = bpy.context.active_pose_bone
            #self.report({'INFO'}, str(rc.name))
            #CoC = bpy.ops.pose.constraint_add(type='CHILD_OF')
            CoC = ab.constraints.new("CHILD_OF")
            #self.report({'INFO'}, "info:" + str(CoC))
            CoC.name = 'Child_Of_' + rc.name
            CoC.target = rc
            
            #bpy.ops.constraint.childof_set_inverse(constraint=CoC.name, owner=ab)
            
            #without ops way to childof_set_inverse
            CoC_target = rc
            #self.report({'INFO'}, str(rc))
            CoC.inverse_matrix = CoC_target.matrix_world.inverted()   
            rc.update_tag({'OBJECT'})
            bpy.context.scene.update()

            #parent to armature
            if self.p_rb_parent_armature == True:
            #bpy.context.scene.objects.active = ob
            #bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
                rc.parent = ob

            ###parent none
            bpy.ops.object.editmode_toggle()
            bpy.context.active_bone.parent = None
            bpy.ops.object.posemode_toggle()

        ###clear object select
        bpy.context.scene.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='DESELECT')

        wm.progress_end()

        self.report({'INFO'}, "OK")
        return {'FINISHED'}

# add menu
def menu_fn(self, context):
    self.layout.separator()
    self.layout.menu(MenuRigidBodys.bl_idname, icon='MESH_ICOSPHERE')


def add_mat(self, context):
        #new material
        if "rigid_mat" not in bpy.data.materials:
            mat = bpy.data.materials.new('rigid_mat')
            mat.name = "rigid_mat"
            mat.use_shadeless = True
            mat.use_transparency = True
            mat.alpha = 0
            mat.use_shadows = False
            mat.use_raytrace = False           
            return mat
        
        else:
            mat = bpy.data.materials["rigid_mat"]
            return mat

def add_RigidBody_World():
        scene = bpy.context.scene
        if scene.rigidbody_world is None:
            bpy.ops.rigidbody.world_add()

# addon enable
def register():
    bpy.utils.register_module(__name__)
    #bpy.utils.register_class(MenuRigidBodyTools)
    bpy.types.VIEW3D_MT_pose.append(menu_fn)
    bpy.app.translations.register(__name__, translation_dict)
    print("rigid_bodys_gen enabled")


# addon disable
def unregister():
    bpy.app.translations.unregister(__name__)
    bpy.types.VIEW3D_MT_pose.remove(menu_fn)
    #bpy.utils.unregister_class(MenuRigidBodyTools)
    bpy.utils.unregister_module(__name__)
    print("rigid_bodys_gen disable")


# main
if __name__ == "__main__":
    register()
