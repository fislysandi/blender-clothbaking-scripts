import bpy

# Get the mesh object and set it as the active object
mesh_object = bpy.context.view_layer.objects.active

# Get all the empties with the name "Instance_ClothSym_Bake" in the scene
empties = [obj for obj in bpy.context.scene.objects if obj.name.startswith('Instance_ClothSym_Bake')]

# Iterate over each empty and vertexxx
for i, empty in enumerate(empties):
    vertex_idx = i % len(mesh_object.data.vertices)
    vertex = mesh_object.data.vertices[vertex_idx]

    # Parent the empty to the vertex
    bpy.ops.object.select_all(action='DESELECT')
    empty.select_set(True)
    bpy.context.view_layer.objects.active = mesh_object
    bpy.ops.object.parent_set(type='VERTEX')

    # Switch back to object mode
    bpy.ops.object.mode_set(mode='OBJECT')
