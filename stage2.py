import bpy

# Get the mesh object and set it as the active object
mesh_object = bpy.context.view_layer.objects.active

# Get all the empties with the name "Instance_ClothSym_Bake" in the scene
empties = [obj for obj in bpy.context.scene.objects if obj.name.startswith('Instance_ClothSym_Bake')]

# Get the armature with the name "Instance_Bone" in the scene
armature = [obj for obj in bpy.context.scene.objects if obj.type == 'ARMATURE' and obj.name.startswith('Instance_Bone')][0]

# Switch to Pose mode
armature.select_set(True)
bpy.context.view_layer.objects.active = armature
bpy.ops.object.mode_set(mode='POSE')

# Get the list of pose bones in the armature
pose_bones = armature.pose.bones

# Iterate over each bone in the list and add a "Copy Transforms" constraint to the bone if it doesn't have one already
num_assigned = 0  # Counter for the number of bones assigned a constraint
for bone in pose_bones:

    # Check if the bone already has a "Copy Transforms" constraint
    if not any(constraint for constraint in bone.constraints if constraint.type == 'COPY_TRANSFORMS'):
        # Get the next empty in the list and add the "Copy Transforms" constraint to the bone with the empty as the target
        if empties:
            empty = empties.pop(0)
            bone_constraint = bone.constraints.new('COPY_TRANSFORMS')
            bone_constraint.target = empty
            num_assigned += 1

    # Check if all bones have been assigned a constraint and exit the loop if they have
    if num_assigned >= len(pose_bones):
        break

# Switch back to object mode and deselect the Armature object
bpy.ops.object.mode_set(mode='OBJECT')
armature.select_set(False)
