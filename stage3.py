import bpy

# Get selected objects
selected_objects = bpy.context.selected_objects

# Check if armature and mesh are selected
if len(selected_objects) != 2:
    print("Please select an armature and a mesh.")
else:
    armature = None
    mesh = None
    for obj in selected_objects:
        if obj.type == 'ARMATURE':
            armature = obj
        elif obj.type == 'MESH':
            mesh = obj

    # Check if armature and mesh are selected
    if not armature or not mesh:
        print("Please select an armature and a mesh.")
    else:
        # Parent mesh to armature with empty groups
        bpy.ops.object.select_all(action='DESELECT')
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        mesh.select_set(True)
        bpy.ops.object.parent_set(type='ARMATURE')

        # Create a dictionary to store bone name to vertex group mapping
        bone_groups = {}

        # Loop through each vertex in the mesh
        for vert in mesh.data.vertices:
            # Get the position of the vertex in world space
            vert_world_pos = mesh.matrix_world @ vert.co

            # Find the closest bone to the vertex
            closest_bone = None
            closest_distance = float('inf')
            for bone in armature.pose.bones:
                bone_world_pos = armature.matrix_world @ bone.head
                distance = (bone_world_pos - vert_world_pos).length
                if distance < closest_distance:
                    closest_bone = bone
                    closest_distance = distance

            # Get the name of the closest bone
            bone_name = closest_bone.name

            # Add the vertex to the bone group
            if bone_name in bone_groups:
                bone_groups[bone_name].append(vert.index)
            else:
                bone_groups[bone_name] = [vert.index]

        # Assign the vertex groups to the armature bones
        for bone in armature.pose.bones:
            bone_name = bone.name
            if bone_name in bone_groups:
                vert_indices = bone_groups[bone_name]
                vertex_group = mesh.vertex_groups.new(name=bone_name)
                for vert_index in vert_indices:
                    vertex_group.add([vert_index], 1.0, 'REPLACE')

        # Apply armature modifiers and set smooth shading
        for mod in mesh.modifiers:
            if mod.type == 'ARMATURE':
                mod.show_viewport = True
                mod.use_deform_preserve_volume = True
        mesh.data.use_auto_smooth = True

        # Select and activate the mesh
        bpy.ops.object.select_all(action='DESELECT')
        armature.select_set(False)
        mesh.select_set(True)
        bpy.context.view_layer.objects.active = mesh
