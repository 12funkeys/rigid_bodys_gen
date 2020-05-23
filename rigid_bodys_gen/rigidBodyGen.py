import bpy
from bpy.props import *

bl_info = {
    "name": "rigid bodys gen",
    "author": "12funkeys",
    "version": (2, 0, 0),
    "blender": (2, 82, 0),
    "location": "pose > selected bones",
    "description": "Set rigid body and constraint easily",
    "warning": "",
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Rigging"
}

translation_dict = {
    "en_US" : {
        ("*", "Make Rigid Body Tools") : "Make Rigid Body Tools",
        #("*", "Rigid Body Gen") : "Rigid Body Gen",
        ("*", "Make Rigid Bodys") : "Make Rigid Bodys",
        ("*", "Add Passive(on bones)") : "Add Passive(on bones)",
        ("*", "make rigibodys move on bones") : "make rigibodys move on bones",
        ("*", "Add Active") : "Add Active",
        ("*", "Add Joints") : "Add Joints",
        ("*", "Add Active & Joints") : "Add Active & Joints"
    },
    "ja_JP" : {
        ("*", "Make Rigid Body Tools") : "選択ボーン",
        #("*", "Rigid Body Gen") : "剛体ツール",
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
class RBG_PT_MenuRigidBodyTools(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rigid Body Gen"
    bl_context = "posemode"
    bl_label = "Make Rigid Body Tools"


    @classmethod
    def poll(cls, context):
        return (context.object is not None)

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        col.operator(RBG_OT_CreateRigidBodysOnBones.bl_idname, text=bpy.app.translations.pgettext("Add Passive(on bones)"), icon='BONE_DATA')
        col.operator(RBG_OT_CreateRigidBodysPhysics.bl_idname, text=bpy.app.translations.pgettext("Add Active"), icon='PHYSICS')
        col.operator(RBG_OT_CreateRigidBodysJoints.bl_idname, text=bpy.app.translations.pgettext("Add Joints"), icon='RIGID_BODY_CONSTRAINT')
        col.operator(RBG_OT_CreateRigidBodysPhysicsJoints.bl_idname, text=bpy.app.translations.pgettext("Add Active & Joints"), icon='RIGID_BODY')


### add MainMenu
class RBG_MT_MenuRigidBodys(bpy.types.Menu):
    # bl_idname = "menu_MT_create_rigidbodys"
    bl_label = "Make Rigid Bodys"
    bl_description = "make rigibodys & constraint"

    def draw(self, context):
        layout = self.layout
        layout.operator(RBG_OT_CreateRigidBodysOnBones.bl_idname, icon='BONE_DATA')
        layout.operator(RBG_OT_CreateRigidBodysPhysics.bl_idname, icon='PHYSICS')
        layout.operator(RBG_OT_CreateRigidBodysJoints.bl_idname, icon='RIGID_BODY_CONSTRAINT')
        layout.operator(RBG_OT_CreateRigidBodysPhysicsJoints.bl_idname, icon='RIGID_BODY')

    # add menu
    def menu_fn(self, context):
        self.layout.separator()
        self.layout.menu(self.bl_idname, icon='MESH_ICOSPHERE')


    @classmethod
    def register(cls):
        bpy.app.translations.register(__name__, translation_dict)
        bpy.types.VIEW3D_MT_pose.append(cls.menu_fn)

    @classmethod
    def unregister(cls):
        bpy.types.VIEW3D_MT_pose.remove(cls.menu_fn)
        bpy.app.translations.unregister(__name__)

### user prop
def user_props():
    scene = bpy.types.Scene

    scene.rbg_rb_shape = EnumProperty(
        name='Shape',
        description='Choose Rigid Body Shape',
        items=shapes,
        default='CAPSULE')

    scene.rbg_rc_dim = FloatVectorProperty(
        name = "Dimensions",
        description = "rigid body Dimensions XYZ",
        default = (1, 1, 1),
        subtype = 'XYZ',
        unit = 'NONE',
        min = 0,
        max = 5)

    scene.rbg_rc_mass = FloatProperty(
        name = "Mass",
        description = "rigid body mass",
        default = 1.0,
        subtype = 'NONE',
        min = 0.001,)

    scene.rbg_rc_friction = FloatProperty(
        name = "Friction",
        description = "rigid body friction",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    scene.rbg_rc_bounciness = FloatProperty(
        name = "Bounciness",
        description = "rigid body bounciness",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    scene.rbg_rc_translation = FloatProperty(
        name = "Translation",
        description = "rigid body translation",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    scene.rbg_rc_rotation = FloatProperty(
        name = "Rotation",
        description = "rigid body rotation",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)


    scene.rbg_jo_type = EnumProperty(
        name='Type',
        description='Choose Contstraint Type',
        items=types,
        default='GENERIC_SPRING')

    scene.rbg_jo_dim = FloatVectorProperty(
        name = "joint Dimensions",
        description = "joint Dimensions XYZ",
        default = (1, 1, 1),
        subtype = 'XYZ',
        unit = 'NONE',
        min = 0,
        max = 5)

    scene.rbg_jo_limit_lin_x = BoolProperty(
        name='X Axis',
        description='limit x',
        default=True,
        options={'ANIMATABLE'})

    scene.rbg_jo_limit_lin_y = BoolProperty(
        name='Y Axis',
        description='limit y',
        default=True)

    scene.rbg_jo_limit_lin_z = BoolProperty(
        name='Z Axis',
        description='limit z',
        default=True)

    scene.rbg_jo_limit_lin_x_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_x_lower",
        default = 0,
        subtype = 'NONE')

    scene.rbg_jo_limit_lin_y_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_y_lower",
        default = 0,
        subtype = 'NONE')

    scene.rbg_jo_limit_lin_z_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_lin_z_lower",
        default = 0,
        subtype = 'NONE')

    scene.rbg_jo_limit_lin_x_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_x_upper",
        default = 0,
        subtype = 'NONE')

    scene.rbg_jo_limit_lin_y_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_y_upper",
        default = 0,
        subtype = 'NONE')

    scene.rbg_jo_limit_lin_z_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_lin_z_upper",
        default = 0,
        subtype = 'NONE')

    scene.rbg_jo_limit_ang_x = BoolProperty(
        name='X Angle',
        description='Angle limit x',
        default=True,
        options={'ANIMATABLE'})

    scene.rbg_jo_limit_ang_y = BoolProperty(
        name='Y Angle',
        description='Angle limit y',
        default=True)

    scene.rbg_jo_limit_ang_z = BoolProperty(
        name='Z Angle',
        description='Angle limit z',
        default=True)

    scene.rbg_jo_limit_ang_x_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_x_lower",
        default = -0.785398,
        subtype = 'ANGLE')

    scene.rbg_jo_limit_ang_y_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_y_lower",
        default = -0.785398,
        subtype = 'ANGLE')

    scene.rbg_jo_limit_ang_z_lower = FloatProperty(
        name = "Lower",
        description = "joint limit_ang_z_lower",
        default = -0.785398,
        subtype = 'ANGLE')

    scene.rbg_jo_limit_ang_x_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_x_upper",
        default = 0.785398,
        subtype = 'ANGLE')

    scene.rbg_jo_limit_ang_y_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_y_upper",
        default = 0.785398,
        subtype = 'ANGLE')

    scene.rbg_jo_limit_ang_z_upper = FloatProperty(
        name = "Upper",
        description = "joint limit_ang_z_upper",
        default = 0.785398,
        subtype = 'ANGLE')


    scene.rbg_jo_use_spring_x = BoolProperty(
        name='X',
        description='use spring x',
        default=False)

    scene.rbg_jo_use_spring_y = BoolProperty(
        name='Y',
        description='use spring y',
        default=False)

    scene.rbg_jo_use_spring_z = BoolProperty(
        name='Z',
        description='use spring z',
        default=False)

    scene.rbg_jo_spring_stiffness_x = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the X Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0)

    scene.rbg_jo_spring_stiffness_y = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the Y Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0)

    scene.rbg_jo_spring_stiffness_z = FloatProperty(
        name = "Stiffness",
        description = "Stiffness on the Z Axis",
        default = 10.000,
        subtype = 'NONE',
        min = 0)

    scene.rbg_jo_spring_damping_x = FloatProperty(
        name = "Damping X",
        description = "Damping on the X Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    scene.rbg_jo_spring_damping_y = FloatProperty(
        name = "Damping Y",
        description = "Damping on the Y Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)

    scene.rbg_jo_spring_damping_z = FloatProperty(
        name = "Damping Z",
        description = "Damping on the Z Axis",
        default = 0.5,
        subtype = 'NONE',
        min = 0,
        max = 1)


    scene.rbg_jo_constraint_object = BoolProperty(
        name='Auto Constraint Object',
        description='Constraint Object',
        default=True)

    scene.rbg_rc_rootbody_passive = BoolProperty(
        name='Passive',
        description='Rigid Body Type Passive',
        default=True)

    scene.rbg_rc_add_pole_rootbody = BoolProperty(
        name='Add Pole Object',
        description='Add Pole Object',
        default=True)

    scene.rbg_rc_rootbody_animated = BoolProperty(
        name='animated',
        description='Root Rigid Body sets animated',
        default=True)

    scene.rbg_rc_parent_armature = BoolProperty(
        name='Parent to armature',
        description='Parent to armature',
        default=True)

def del_props():
    scene = bpy.types.Scene
    del scene.rbg_rb_shape


### Create Rigid Bodys On Bones
class RBG_OT_CreateRigidBodysOnBones(bpy.types.Operator):

    bl_idname = "rigidbody.on_bones"
    bl_label = "Add Passive(on bones)"
    bl_description = "make rigibodys move on bones"
    bl_options = {'REGISTER', 'UNDO'}

    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30

    ###instance UProp.rigidbody
    # rbg_rb_shape = UProp.rb_shape
    # rbg_rc_dim = UProp.rc_dim
    # rbg_rc_mass = UProp.rc_mass
    # rbg_rc_friction = UProp.rc_friction
    # rbg_rc_bounciness = UProp.rc_bounciness
    # rbg_rc_translation = UProp.rc_translation
    # rbg_rc_rotation = UProp.rc_rotation
    # rbg_rc_rootbody_passive = UProp.rc_rootbody_passive
    # rbg_rc_rootbody_animated = UProp.rc_rootbody_animated
    # rbg_rc_parent_armature = UProp.rc_parent_armature


    # def __init__(self):
    #
    #     context.scene.rbg_rc_dim = (1, 1, 1)

    def draw(self, context):

        scene = context.scene

        layout = self.layout
        box = layout.box()
        box.prop(scene, 'rbg_rb_shape')
        box.prop(scene, 'rbg_rc_dim')
        box.prop(scene, 'rbg_rc_mass')
        box.prop(scene, 'rbg_rc_friction')
        box.prop(scene, 'rbg_rc_bounciness')
        box.label(text="Damping:")
        box.prop(scene, 'rbg_rc_translation')
        box.prop(scene, 'rbg_rc_rotation')
        box.prop(scene, 'rbg_rc_rootbody_passive')
        box.prop(scene, 'rbg_rc_rootbody_animated')
        box.prop(scene, 'rbg_rc_parent_armature')

    ###
    def execute(self, context):

        scene = context.scene

        ###selected Armature
        ob = bpy.context.active_object

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

        if len(bpy.context.selected_pose_bones) == 0:
            return {'FINISHED'}

        for selected_bones in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bones.vector[0]))

            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(size=1.0, calc_uvs=False, enter_editmode=False, align='WORLD', location=selected_bones.center, rotation=(0.0, 0.0, 0.0))
            rc = bpy.context.active_object
            rc.name = "rbg." + selected_bones.name
            viewport_display(self, rc)
            rc.show_in_front = True
            rc.hide_render = True

            ###Damped Track
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
                selected_bones.length * self.init_rc_dimX * scene.rbg_rc_dim[0],
                selected_bones.length * self.init_rc_dimY * scene.rbg_rc_dim[1],
                selected_bones.length * self.init_rc_dimZ * scene.rbg_rc_dim[2]]

            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            if scene.rbg_rc_rootbody_passive == True:
                bpy.context.object.rigid_body.type = "PASSIVE"
            else:
                bpy.context.object.rigid_body.type = "ACTIVE"

            bpy.context.object.rigid_body.collision_shape = scene.rbg_rb_shape
            bpy.context.object.rigid_body.kinematic = scene.rbg_rc_rootbody_animated
            bpy.context.object.rigid_body.mass = scene.rbg_rc_mass
            bpy.context.object.rigid_body.friction = scene.rbg_rc_friction
            bpy.context.object.rigid_body.restitution = scene.rbg_rc_bounciness
            bpy.context.object.rigid_body.linear_damping = scene.rbg_rc_translation
            bpy.context.object.rigid_body.angular_damping = scene.rbg_rc_rotation


            ### Child OF
            CoC = rc.constraints.new("CHILD_OF")
            CoC.name = 'Child_Of_' + selected_bones.name
            CoC.target = ob
            CoC.subtarget = selected_bones.name

            #without ops way to childof_set_inverse
            sub_target = bpy.data.objects[ob.name].pose.bones[selected_bones.name]
            #self.report({'INFO'}, str(sub_target))
            CoC.inverse_matrix = sub_target.matrix.inverted()
            rc.update_tag(refresh={'OBJECT'})
            bpy.context.scene.update_tag()

            #parent to armature
            if scene.rbg_rc_parent_armature == True:
                rc.parent = ob

        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='DESELECT')

        self.report({'INFO'}, "OK")
        return {'FINISHED'}

#
class RBG_OT_CreateRigidBodysPhysics(bpy.types.Operator):

    bl_idname = "rigidbody.physics"
    bl_label = "Add Active"
    bl_description = "make physics engine on rigibodys"
    bl_options = {'REGISTER', 'UNDO'}

    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30

    ###instance UProp.rigidbody
    # rbg_rb_shape = UProp.rb_shape
    # rbg_rc_dim = UProp.rc_dim
    # rbg_rc_mass = UProp.rc_mass
    # rbg_rc_friction = UProp.rc_friction
    # rbg_rc_bounciness = UProp.rc_bounciness
    # rbg_rc_translation = UProp.rc_translation
    # rbg_rc_rotation = UProp.rc_rotation
    # #rbg_rc_rootbody_passive = UProp.rc_rootbody_passive
    # rbg_rc_rootbody_animated = UProp.rc_rootbody_animated
    # rbg_rc_parent_armature = UProp.rc_parent_armature

    # def __init__(self):
    #
    #     context.scene.rbg_rc_dim = (1, 1, 1)

    def draw(self, context):

        scene = context.scene
        layout = self.layout
        box = layout.box()
        box.prop(scene, 'rbg_rb_shape')
        box.prop(scene, 'rbg_rc_dim')
        box.prop(scene, 'rbg_rc_mass')
        box.prop(scene, 'rbg_rc_friction')
        box.prop(scene, 'rbg_rc_bounciness')
        box.prop(scene, 'rbg_rc_translation')
        box.prop(scene, 'rbg_rc_rotation')
        box.prop(scene, 'rbg_rc_rootbody_animated')
        box.prop(scene, 'rbg_rc_parent_armature')

    ###
    def execute(self, context):

        scene = context.scene
        ###selected Armature
        ob = bpy.context.active_object
        #self.report({'INFO'}, ob.data)

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

        for selected_bones in bpy.context.selected_pose_bones:

            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(size=1.0, calc_uvs=False, enter_editmode=False, align='WORLD', location=selected_bones.center, rotation=(0.0, 0.0, 0.0))
            rc = bpy.context.active_object
            rc.name = "rbg." + selected_bones.name
            viewport_display(self, rc)
            rc.show_in_front = True
            bpy.data.objects[rc.name].hide_render = True

            ###Damped Track
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
                selected_bones.length * self.init_rc_dimX * scene.rbg_rc_dim[0],
                selected_bones.length * self.init_rc_dimY * scene.rbg_rc_dim[1],
                selected_bones.length * self.init_rc_dimZ * scene.rbg_rc_dim[2]]

            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            bpy.context.object.rigid_body.type = "ACTIVE"
            bpy.context.object.rigid_body.collision_shape = scene.rbg_rb_shape
            bpy.context.object.rigid_body.kinematic = scene.rbg_rc_rootbody_animated
            bpy.context.object.rigid_body.mass = scene.rbg_rc_mass
            bpy.context.object.rigid_body.friction = scene.rbg_rc_friction
            bpy.context.object.rigid_body.restitution = scene.rbg_rc_bounciness
            bpy.context.object.rigid_body.linear_damping = scene.rbg_rc_translation
            bpy.context.object.rigid_body.angular_damping = scene.rbg_rc_rotation

            ### Child OF
            bpy.context.view_layer.objects.active = ob
            bpy.ops.pose.armature_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bones.name]
            ab = bpy.context.active_pose_bone


            CoC = ab.constraints.new("CHILD_OF")
            CoC.name = 'Child_Of_' + rc.name
            CoC.target = rc

            #without ops way to childof_set_inverse
            CoC_target = rc
            #self.report({'INFO'}, str(rc))
            CoC.inverse_matrix = CoC_target.matrix_world.inverted()
            rc.update_tag(refresh={'OBJECT'})
            bpy.context.scene.update_tag()

            ###parent none
            bpy.ops.object.editmode_toggle()
            bpy.context.active_bone.parent = None
            bpy.ops.object.posemode_toggle()

            #parent to armature
            if scene.rbg_rc_parent_armature == True:
                rc.parent = ob

        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='DESELECT')

        self.report({'INFO'}, "OK")
        return {'FINISHED'}

#
class RBG_OT_CreateRigidBodysJoints(bpy.types.Operator):

    bl_idname = "rigidbody.joints"
    bl_label = "Add Joints"
    bl_description = "add Add Joints on bones"
    bl_options = {'REGISTER', 'UNDO'}

    init_rbg_jo_dimX = 0.33
    init_rbg_jo_dimY = 0.33
    init_rbg_jo_dimZ = 0.33

    ###instance UProp.joint
    # rbg_jo_type = UProp.jo_type
    # rbg_jo_dim = UProp.jo_dim
    # rbg_jo_limit_lin_x = UProp.jo_limit_lin_x
    # rbg_jo_limit_lin_y = UProp.jo_limit_lin_y
    # rbg_jo_limit_lin_z = UProp.jo_limit_lin_z
    # rbg_jo_limit_lin_x_lower = UProp.jo_limit_lin_x_lower
    # rbg_jo_limit_lin_y_lower = UProp.jo_limit_lin_y_lower
    # rbg_jo_limit_lin_z_lower = UProp.jo_limit_lin_z_lower
    # rbg_jo_limit_lin_x_upper = UProp.jo_limit_lin_x_upper
    # rbg_jo_limit_lin_y_upper = UProp.jo_limit_lin_y_upper
    # rbg_jo_limit_lin_z_upper = UProp.jo_limit_lin_z_upper
    # rbg_jo_limit_ang_x = UProp.jo_limit_ang_x
    # rbg_jo_limit_ang_y = UProp.jo_limit_ang_y
    # rbg_jo_limit_ang_z = UProp.jo_limit_ang_z
    # rbg_jo_limit_ang_x_lower = UProp.jo_limit_ang_x_lower
    # rbg_jo_limit_ang_y_lower = UProp.jo_limit_ang_y_lower
    # rbg_jo_limit_ang_z_lower = UProp.jo_limit_ang_z_lower
    # rbg_jo_limit_ang_x_upper = UProp.jo_limit_ang_x_upper
    # rbg_jo_limit_ang_y_upper = UProp.jo_limit_ang_y_upper
    # rbg_jo_limit_ang_z_upper = UProp.jo_limit_ang_z_upper
    # rbg_jo_use_spring_x = UProp.jo_use_spring_x
    # rbg_jo_use_spring_y = UProp.jo_use_spring_y
    # rbg_jo_use_spring_z = UProp.jo_use_spring_z
    # rbg_jo_spring_stiffness_x = UProp.jo_spring_stiffness_x
    # rbg_jo_spring_stiffness_y = UProp.jo_spring_stiffness_y
    # rbg_jo_spring_stiffness_z = UProp.jo_spring_stiffness_z
    # rbg_jo_spring_damping_x = UProp.jo_spring_damping_x
    # rbg_jo_spring_damping_y = UProp.jo_spring_damping_y
    # rbg_jo_spring_damping_z = UProp.jo_spring_damping_z
    # rbg_rc_parent_armature = UProp.rc_parent_armature

    # def __init__(self):
    #
    #     context.scene.rbg_jo_dim = (1, 1, 1)

    def draw(self, context):

        scene = context.scene
        layout = self.layout
        box = layout.box()
        box.prop(scene, 'rbg_jo_type')
        box.prop(scene, 'rbg_jo_dim')


        col = box.column(align=True)
        col.label(text="Limits:")

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_lin_x', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_lin_x_lower')
        sub.prop(scene, 'rbg_jo_limit_lin_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_lin_y', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_lin_y_lower')
        sub.prop(scene, 'rbg_jo_limit_lin_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_lin_z', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_lin_z_lower')
        sub.prop(scene, 'rbg_jo_limit_lin_z_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_ang_x', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_ang_x_lower')
        sub.prop(scene, 'rbg_jo_limit_ang_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_ang_y', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_ang_y_lower')
        sub.prop(scene, 'rbg_jo_limit_ang_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_ang_z', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_ang_z_lower')
        sub.prop(scene, 'rbg_jo_limit_ang_z_upper')


        col.label(text="Springs:")

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_use_spring_x', toggle=True)
        sub.prop(scene, 'rbg_jo_spring_stiffness_x')
        sub.prop(scene, 'rbg_jo_spring_damping_x')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_use_spring_y', toggle=True)
        sub.prop(scene, 'rbg_jo_spring_stiffness_y')
        sub.prop(scene, 'rbg_jo_spring_damping_y')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_use_spring_z', toggle=True)
        sub.prop(scene, 'rbg_jo_spring_stiffness_z')
        sub.prop(scene, 'rbg_jo_spring_damping_z')

        col.prop(scene, 'rbg_rc_parent_armature')


    ###
    def execute(self, context):

        scene = context.scene
        add_RigidBody_World()

        ###selected Armature
        ob = bpy.context.active_object

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

        for selected_bones in bpy.context.selected_pose_bones:
            #self.report({'INFO'}, str(selected_bones.vector[0]))

            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(size=1.0, calc_uvs=False, enter_editmode=False, align='WORLD', location=selected_bones.head, rotation=(0.0, 0.0, 0.0))
            rc = bpy.context.active_object
            rc.name = "joint." + selected_bones.name
            viewport_display(self, rc)
            rc.show_in_front = True
            bpy.data.objects[rc.name].hide_render = True

            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bones.length * self.init_rbg_jo_dimX * scene.rbg_jo_dim[0],
                selected_bones.length * self.init_rbg_jo_dimY * scene.rbg_jo_dim[1],
                selected_bones.length * self.init_rbg_jo_dimZ * scene.rbg_jo_dim[2]]

            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.constraint_add()
            bpy.context.object.rigid_body_constraint.type = scene.rbg_jo_type
            bpy.context.object.rigid_body_constraint.use_breaking = False
            bpy.context.object.rigid_body_constraint.use_override_solver_iterations = True
            bpy.context.object.rigid_body_constraint.breaking_threshold = 10
            bpy.context.object.rigid_body_constraint.solver_iterations = 10

            bpy.context.object.rigid_body_constraint.use_limit_lin_x = scene.rbg_jo_limit_lin_x
            bpy.context.object.rigid_body_constraint.use_limit_lin_y = scene.rbg_jo_limit_lin_y
            bpy.context.object.rigid_body_constraint.use_limit_lin_z = scene.rbg_jo_limit_lin_z
            bpy.context.object.rigid_body_constraint.limit_lin_x_lower = scene.rbg_jo_limit_lin_x_lower
            bpy.context.object.rigid_body_constraint.limit_lin_y_lower = scene.rbg_jo_limit_lin_y_lower
            bpy.context.object.rigid_body_constraint.limit_lin_z_lower = scene.rbg_jo_limit_lin_z_lower
            bpy.context.object.rigid_body_constraint.limit_lin_x_upper = scene.rbg_jo_limit_lin_x_upper
            bpy.context.object.rigid_body_constraint.limit_lin_y_upper = scene.rbg_jo_limit_lin_y_upper
            bpy.context.object.rigid_body_constraint.limit_lin_z_upper = scene.rbg_jo_limit_lin_z_upper

            bpy.context.object.rigid_body_constraint.use_limit_ang_x = scene.rbg_jo_limit_ang_x
            bpy.context.object.rigid_body_constraint.use_limit_ang_y = scene.rbg_jo_limit_ang_y
            bpy.context.object.rigid_body_constraint.use_limit_ang_z = scene.rbg_jo_limit_ang_z
            bpy.context.object.rigid_body_constraint.limit_ang_x_lower = scene.rbg_jo_limit_ang_x_lower
            bpy.context.object.rigid_body_constraint.limit_ang_y_lower = scene.rbg_jo_limit_ang_y_lower
            bpy.context.object.rigid_body_constraint.limit_ang_z_lower = scene.rbg_jo_limit_ang_z_lower
            bpy.context.object.rigid_body_constraint.limit_ang_x_upper = scene.rbg_jo_limit_ang_x_upper
            bpy.context.object.rigid_body_constraint.limit_ang_y_upper = scene.rbg_jo_limit_ang_y_upper
            bpy.context.object.rigid_body_constraint.limit_ang_z_upper = scene.rbg_jo_limit_ang_z_upper

            bpy.context.object.rigid_body_constraint.use_spring_x = scene.rbg_jo_use_spring_x
            bpy.context.object.rigid_body_constraint.use_spring_y = scene.rbg_jo_use_spring_y
            bpy.context.object.rigid_body_constraint.use_spring_z = scene.rbg_jo_use_spring_z
            bpy.context.object.rigid_body_constraint.spring_stiffness_x = scene.rbg_jo_spring_stiffness_x
            bpy.context.object.rigid_body_constraint.spring_stiffness_y = scene.rbg_jo_spring_stiffness_y
            bpy.context.object.rigid_body_constraint.spring_stiffness_z = scene.rbg_jo_spring_stiffness_z
            bpy.context.object.rigid_body_constraint.spring_damping_x = scene.rbg_jo_spring_damping_x
            bpy.context.object.rigid_body_constraint.spring_damping_y = scene.rbg_jo_spring_damping_y
            bpy.context.object.rigid_body_constraint.spring_damping_z = scene.rbg_jo_spring_damping_z

            #parent to armature
            if scene.rbg_rc_parent_armature == True:
                rc.parent = ob

        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='DESELECT')

        self.report({'INFO'}, "OK")
        return {'FINISHED'}

class RBG_OT_CreateRigidBodysPhysicsJoints(bpy.types.Operator):

    bl_idname = "rigidbody.physics_joints"
    bl_label = "Add Active & Joints"
    bl_description = "Add Active & Joints"
    bl_options = {'REGISTER', 'UNDO'}


    init_rc_dimX = 0.28
    init_rc_dimY = 0.28
    init_rc_dimZ = 1.30

    #pole_dict = {}

    ###instance UProp.rigidbody
    # rbg_rb_shape = UProp.rb_shape
    # rbg_rc_dim = UProp.rc_dim
    # rbg_rc_mass = UProp.rc_mass
    # rbg_rc_friction = UProp.rc_friction
    # rbg_rc_bounciness = UProp.rc_bounciness
    # rbg_rc_translation = UProp.rc_translation
    # rbg_rc_rotation = UProp.rc_rotation
    # rbg_rc_add_pole_rootbody = UProp.rc_add_pole_rootbody
    # rbg_rc_parent_armature = UProp.rc_parent_armature

    init_rbg_jo_dimX = 0.33
    init_rbg_jo_dimY = 0.33
    init_rbg_jo_dimZ = 0.33

    ###instance UProp.joint
    # rbg_jo_type = UProp.jo_type
    # rbg_jo_dim = UProp.jo_dim
    # rbg_jo_limit_lin_x = UProp.jo_limit_lin_x
    # rbg_jo_limit_lin_y = UProp.jo_limit_lin_y
    # rbg_jo_limit_lin_z = UProp.jo_limit_lin_z
    # rbg_jo_limit_lin_x_lower = UProp.jo_limit_lin_x_lower
    # rbg_jo_limit_lin_y_lower = UProp.jo_limit_lin_y_lower
    # rbg_jo_limit_lin_z_lower = UProp.jo_limit_lin_z_lower
    # rbg_jo_limit_lin_x_upper = UProp.jo_limit_lin_x_upper
    # rbg_jo_limit_lin_y_upper = UProp.jo_limit_lin_y_upper
    # rbg_jo_limit_lin_z_upper = UProp.jo_limit_lin_z_upper
    # rbg_jo_limit_ang_x = UProp.jo_limit_ang_x
    # rbg_jo_limit_ang_y = UProp.jo_limit_ang_y
    # rbg_jo_limit_ang_z = UProp.jo_limit_ang_z
    # rbg_jo_limit_ang_x_lower = UProp.jo_limit_ang_x_lower
    # rbg_jo_limit_ang_y_lower = UProp.jo_limit_ang_y_lower
    # rbg_jo_limit_ang_z_lower = UProp.jo_limit_ang_z_lower
    # rbg_jo_limit_ang_x_upper = UProp.jo_limit_ang_x_upper
    # rbg_jo_limit_ang_y_upper = UProp.jo_limit_ang_y_upper
    # rbg_jo_limit_ang_z_upper = UProp.jo_limit_ang_z_upper
    # rbg_jo_use_spring_x = UProp.jo_use_spring_x
    # rbg_jo_use_spring_y = UProp.jo_use_spring_y
    # rbg_jo_use_spring_z = UProp.jo_use_spring_z
    # rbg_jo_spring_stiffness_x = UProp.jo_spring_stiffness_x
    # rbg_jo_spring_stiffness_y = UProp.jo_spring_stiffness_y
    # rbg_jo_spring_stiffness_z = UProp.jo_spring_stiffness_z
    # rbg_jo_spring_damping_x = UProp.jo_spring_damping_x
    # rbg_jo_spring_damping_y = UProp.jo_spring_damping_y
    # rbg_jo_spring_damping_z = UProp.jo_spring_damping_z
    # rbg_jo_constraint_object = UProp.jo_constraint_object


    # def __init__(self):
    #
    #     context.scene.rbg_rc_dim = (1, 1, 1)
    #     context.scene.rbg_jo_dim = (1, 1, 1)

    def draw(self, context):

        scene = context.scene
        ###Rigid Body Object
        layout = self.layout

        box = layout.box()
        box.prop(scene, 'rbg_rb_shape')
        box.prop(scene, 'rbg_rc_dim')
        box.prop(scene, 'rbg_rc_mass')
        box.prop(scene, 'rbg_rc_friction')
        box.prop(scene, 'rbg_rc_bounciness')
        box.prop(scene, 'rbg_rc_translation')
        box.prop(scene, 'rbg_rc_rotation')


        #Joint Object
        layout = self.layout
        box = layout.box()
        box.prop(scene, 'rbg_jo_type')
        box.prop(scene, 'rbg_jo_constraint_object')
        box.prop(scene, 'rbg_rc_add_pole_rootbody')
        box.prop(scene, 'rbg_rc_parent_armature')
        box.prop(scene, 'rbg_jo_dim')

        col = box.column(align=True)
        col.label(text="Limits:")

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_lin_x', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_lin_x_lower')
        sub.prop(scene, 'rbg_jo_limit_lin_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_lin_y', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_lin_y_lower')
        sub.prop(scene, 'rbg_jo_limit_lin_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_lin_z', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_lin_z_lower')
        sub.prop(scene, 'rbg_jo_limit_lin_z_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_ang_x', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_ang_x_lower')
        sub.prop(scene, 'rbg_jo_limit_ang_x_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_ang_y', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_ang_y_lower')
        sub.prop(scene, 'rbg_jo_limit_ang_y_upper')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_limit_ang_z', toggle=True)
        sub.prop(scene, 'rbg_jo_limit_ang_z_lower')
        sub.prop(scene, 'rbg_jo_limit_ang_z_upper')

        col.label(text="Springs:")

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_use_spring_x', toggle=True)
        sub.prop(scene, 'rbg_jo_spring_stiffness_x')
        sub.prop(scene, 'rbg_jo_spring_damping_x')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_use_spring_y', toggle=True)
        sub.prop(scene, 'rbg_jo_spring_stiffness_y')
        sub.prop(scene, 'rbg_jo_spring_damping_y')

        row = col.row(align=True)
        sub = row.row(align=True)
        sub.prop(scene, 'rbg_jo_use_spring_z', toggle=True)
        sub.prop(scene, 'rbg_jo_spring_stiffness_z')
        sub.prop(scene, 'rbg_jo_spring_damping_z')

    #
    def execute(self, context):

        scene = context.scene
        add_RigidBody_World()

        ###selected Armature
        ob = bpy.context.active_object
        self.report({'INFO'}, "ob:" + str(ob))

        ### Apply Object transform
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        bpy.ops.object.posemode_toggle()

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
            bpy.ops.mesh.primitive_cube_add(size=1.0, calc_uvs=False, enter_editmode=False, align='WORLD', location=selected_bones.head, rotation=(0.0, 0.0, 0.0))
            jc = bpy.context.active_object
            jc.name = "joint." + ob.name + "." + selected_bones.name
            viewport_display(self, jc)
            jc.show_in_front = True
            bpy.data.objects[jc.name].hide_render = True

            ### Rigid Body Dimensions
            bpy.context.object.dimensions = [
                selected_bones.length * self.init_rbg_jo_dimX * scene.rbg_jo_dim[0],
                selected_bones.length * self.init_rbg_jo_dimY * scene.rbg_jo_dim[1],
                selected_bones.length * self.init_rbg_jo_dimZ * scene.rbg_jo_dim[2]]

            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.constraint_add()
            jc.rigid_body_constraint.type = scene.rbg_jo_type
            jc.rigid_body_constraint.use_breaking = False
            jc.rigid_body_constraint.use_override_solver_iterations = True
            jc.rigid_body_constraint.breaking_threshold = 10
            jc.rigid_body_constraint.solver_iterations = 10

            jc.rigid_body_constraint.use_limit_lin_x = scene.rbg_jo_limit_lin_x
            jc.rigid_body_constraint.use_limit_lin_y = scene.rbg_jo_limit_lin_y
            jc.rigid_body_constraint.use_limit_lin_z = scene.rbg_jo_limit_lin_z
            jc.rigid_body_constraint.limit_lin_x_lower = scene.rbg_jo_limit_lin_x_lower
            jc.rigid_body_constraint.limit_lin_y_lower = scene.rbg_jo_limit_lin_y_lower
            jc.rigid_body_constraint.limit_lin_z_lower = scene.rbg_jo_limit_lin_z_lower
            jc.rigid_body_constraint.limit_lin_x_upper = scene.rbg_jo_limit_lin_x_upper
            jc.rigid_body_constraint.limit_lin_y_upper = scene.rbg_jo_limit_lin_y_upper
            jc.rigid_body_constraint.limit_lin_z_upper = scene.rbg_jo_limit_lin_z_upper

            jc.rigid_body_constraint.use_limit_ang_x = scene.rbg_jo_limit_ang_x
            jc.rigid_body_constraint.use_limit_ang_y = scene.rbg_jo_limit_ang_y
            jc.rigid_body_constraint.use_limit_ang_z = scene.rbg_jo_limit_ang_z
            jc.rigid_body_constraint.limit_ang_x_lower = scene.rbg_jo_limit_ang_x_lower
            jc.rigid_body_constraint.limit_ang_y_lower = scene.rbg_jo_limit_ang_y_lower
            jc.rigid_body_constraint.limit_ang_z_lower = scene.rbg_jo_limit_ang_z_lower
            jc.rigid_body_constraint.limit_ang_x_upper = scene.rbg_jo_limit_ang_x_upper
            jc.rigid_body_constraint.limit_ang_y_upper = scene.rbg_jo_limit_ang_y_upper
            jc.rigid_body_constraint.limit_ang_z_upper = scene.rbg_jo_limit_ang_z_upper

            jc.rigid_body_constraint.use_spring_x = scene.rbg_jo_use_spring_x
            jc.rigid_body_constraint.use_spring_y = scene.rbg_jo_use_spring_y
            jc.rigid_body_constraint.use_spring_z = scene.rbg_jo_use_spring_z
            jc.rigid_body_constraint.spring_stiffness_x = scene.rbg_jo_spring_stiffness_x
            jc.rigid_body_constraint.spring_stiffness_y = scene.rbg_jo_spring_stiffness_y
            jc.rigid_body_constraint.spring_stiffness_z = scene.rbg_jo_spring_stiffness_z
            jc.rigid_body_constraint.spring_damping_x = scene.rbg_jo_spring_damping_x
            jc.rigid_body_constraint.spring_damping_y = scene.rbg_jo_spring_damping_y
            jc.rigid_body_constraint.spring_damping_z = scene.rbg_jo_spring_damping_z

            self.report({'INFO'}, "selected_bones.parent:" + str(selected_bones.parent))
            if selected_bones.parent is not None and selected_bones.parent not in spb and selected_bones.parent not in pole_dict and scene.rbg_rc_add_pole_rootbody == True:

                    ###Create Rigidbody Cube
                    bpy.ops.mesh.primitive_cube_add(size=1.0, calc_uvs=False, enter_editmode=False, align='WORLD', location=selected_bones.parent.center, rotation=(0.0, 0.0, 0.0))
                    rc2 = bpy.context.active_object
                    rc2.name = "rbg.pole." + ob.name + "." + selected_bones.parent.name
                    viewport_display(self, rc2)
                    rc2.show_in_front = True
                    rc2.hide_render = True

                    ### Rigid Body Dimensions
                    bpy.context.object.dimensions = [
                        selected_bones.parent.length * self.init_rbg_jo_dimX,
                        selected_bones.parent.length * self.init_rbg_jo_dimY,
                        selected_bones.parent.length * self.init_rbg_jo_dimZ]

                    ### Scale Apply
                    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

                    ### Set Rigid Body
                    bpy.ops.rigidbody.object_add()

                    rc2.rigid_body.type = "PASSIVE"
                    rc2.rigid_body.collision_shape = "BOX"
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
                    rc2.update_tag(refresh={'OBJECT'})
                    bpy.context.scene.update_tag()

                    #parent to armature
                    if scene.rbg_rc_parent_armature == True:
                        rc2.parent = ob


            ###constraint.object1

            if selected_bones.parent is not None and selected_bones.parent not in spb and scene.rbg_rc_add_pole_rootbody == True:

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
            if scene.rbg_rc_parent_armature == True:
                jc.parent = ob


            ###Rigid Body Session
            ###Create Rigidbody Cube
            bpy.ops.mesh.primitive_cube_add(size=1.0, calc_uvs=False, enter_editmode=False, align='WORLD', location=selected_bones.center, rotation=(0.0, 0.0, 0.0))
            rc = bpy.context.active_object
            rc.name = parent_bones_ob
            viewport_display(self, rc)
            rc.show_in_front = True
            bpy.data.objects[rc.name].hide_render = True

            ###constraint.object2
            if parent_bones_ob != "":
                jc.rigid_body_constraint.object2 = bpy.data.objects[parent_bones_ob]

            if len(selected_bones.children_recursive) == 0:
                parent_bones_ob = ""

            ###Damped Track
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
                selected_bones.length * self.init_rc_dimX * scene.rbg_rc_dim[0],
                selected_bones.length * self.init_rc_dimY * scene.rbg_rc_dim[1],
                selected_bones.length * self.init_rc_dimZ * scene.rbg_rc_dim[2]]

            ### Scale Apply
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

            ### Set Rigid Body
            bpy.ops.rigidbody.object_add()

            bpy.context.object.rigid_body.type = "ACTIVE"
            bpy.context.object.rigid_body.collision_shape = scene.rbg_rb_shape
            bpy.context.object.rigid_body.mass = scene.rbg_rc_mass
            bpy.context.object.rigid_body.friction = scene.rbg_rc_friction
            bpy.context.object.rigid_body.restitution = scene.rbg_rc_bounciness
            bpy.context.object.rigid_body.linear_damping = scene.rbg_rc_translation
            bpy.context.object.rigid_body.angular_damping = scene.rbg_rc_rotation

            ### Child OF
            bpy.context.view_layer.objects.active = ob
            bpy.ops.pose.armature_apply()
            #bpy.ops.pose.visual_transform_apply()
            bpy.ops.pose.select_all(action='DESELECT')
            bpy.context.object.data.bones.active = bpy.context.object.data.bones[selected_bones.name]
            ab = bpy.context.active_pose_bone
            #self.report({'INFO'}, str(rc.name))
            CoC = ab.constraints.new("CHILD_OF")
            CoC.name = 'Child_Of_' + rc.name
            CoC.target = rc

            #without ops way to childof_set_inverse
            CoC_target = rc
            #self.report({'INFO'}, str(rc))
            CoC.inverse_matrix = CoC_target.matrix_world.inverted()
            rc.update_tag(refresh={'OBJECT'})
            bpy.context.scene.update_tag()

            #parent to armature
            if scene.rbg_rc_parent_armature == True:
                rc.parent = ob

            ###parent none
            bpy.ops.object.editmode_toggle()
            bpy.context.active_bone.parent = None
            bpy.ops.object.posemode_toggle()

        ###clear object select
        bpy.context.view_layer.objects.active = ob
        bpy.ops.object.posemode_toggle()
        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.posemode_toggle()
        bpy.ops.pose.select_all(action='DESELECT')

        wm.progress_end()

        self.report({'INFO'}, "OK")
        return {'FINISHED'}



def viewport_display(self, rb):
        rb.display_type = 'WIRE'
        rb.show_in_front = True
        rb.display.show_shadows = False
        rb.hide_render = True


def add_RigidBody_World():
        scene = bpy.context.scene
        if scene.rigidbody_world is None:
            bpy.ops.rigidbody.world_add()


classes = [
    RBG_PT_MenuRigidBodyTools,
    RBG_MT_MenuRigidBodys,
    RBG_OT_CreateRigidBodysOnBones,
    RBG_OT_CreateRigidBodysPhysics,
    RBG_OT_CreateRigidBodysJoints,
    RBG_OT_CreateRigidBodysPhysicsJoints
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
