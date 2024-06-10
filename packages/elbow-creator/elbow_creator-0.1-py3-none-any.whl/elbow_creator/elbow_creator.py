# elbow_creator.py
import bpy
import mathutils
import math

def create_elbow(radius, point1, point2):
    # Calculate the direction vector and the midpoint between the points
    vec1 = mathutils.Vector(point1)
    vec2 = mathutils.Vector(point2)
    direction = vec2 - vec1
    midpoint = (vec1 + vec2) / 2

    # Create a torus and select a quarter section
    bpy.ops.mesh.primitive_torus_add(
        major_radius=radius * 2, 
        minor_radius=radius, 
        major_segments=48, 
        minor_segments=12, 
        location=(0, 0, 0)
    )

    torus = bpy.context.object
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    bpy.ops.object.mode_set(mode='OBJECT')
    mesh = torus.data
    for v in mesh.vertices:
        if v.co.y < 0 or v.co.x < 0:
            v.select = True
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Move and rotate the elbow to match the points
    direction.normalize()
    rotation_matrix = direction.to_track_quat('Z', 'Y').to_matrix().to_4x4()
    translation_matrix = mathutils.Matrix.Translation(midpoint)
    transform_matrix = translation_matrix @ rotation_matrix
    torus.matrix_world = transform_matrix

