import bpy

context = bpy.context

bpy.ops.object.mode_set(mode='EDIT')

#eo = bpy.context.edit_object
#mw = eo.matrix_world

MargeCount = 3

elist = [e for e in context.selected_editable_bones if e.select]

print("###start###")
#bpy.ops.armature.select_all(action='DESELECT')

#i = 0
#for v in elist:
#    print(v.name)
#    i = i + 1
#    print(i)
#    v.select = True
#    
#    if i == 3:
#        bpy.ops.armature.merge(type='WITHIN_CHAIN')
#        i = 0

rootbones = []     
        
for v in elist:
    if v.parent:
#        print("v.name:"+v.name)
#        print("parent.name:"+v.parent.name)
        if v.parent.select == False:
#            print("root.name:"+v.name)
            rootbones += [v]
    else:
#        print("root.name:" + v.name) 
        rootbones += [v]
        
#print("rootbones:" + str(rootbones))   
#print("children.name:" + str(rootbone.children[0].select))  

bpy.ops.armature.select_all(action='DESELECT')

i = 0
#bone = rootbones
#bone.select = True

#print("bone:" + str(bone))

for bone in rootbones:
    while bone in elist:
        print("bone.name:" + bone.name) 
        
        i = i + 1
        print("i:" + str(i)) 
             
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
                


#else:
#    print("return:" + bone.name) 