#This should be copied into the blender python console
from mathutils import Vector
import os
class flyingCam:
    def __init__(self, normal, fov=20):
        self.normal=Vector(normal)
        self.FOV=fov
    def print_heading(self):
        print(cam.location)
    def to_cursor(self):
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        heading = cam.location - cursor_loc
        rot_quat = heading.to_track_quat('Z', 'X')
        cam.rotation_euler = rot_quat.to_euler()
        print(cam.rotation_euler)
    def move_to_cursor(self):
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        heading = cam.location - cursor_loc
        cam.location -= heading/2.0
        rot_quat = heading.to_track_quat('Z', 'X')
        cam.rotation_euler = rot_quat.to_euler()
    def move_forward(self, distance=1):
        cam = D.objects["Camera"]
        #Taken from: https://blender.stackexchange.com/questions/13738/
        #how-to-calculate-camera-direction-and-up-vector
        up = cam.matrix_world.to_quaternion() * Vector((0.0, 1.0, 0.0))
        cam_direction = cam.matrix_world.to_quaternion() * Vector((0.0, 0.0, -1.0))
        cam.location += cam_direction * distance
        e_rot = cam.rotation_euler
        heading_vec = Vector((e_rot.x,e_rot.y,e_rot.z))
    def take_pic(self, filepath):
        #Taken from https://blender.
        #stackexchange.com/questions/30643/how-to-toggle-to-camera-view-via-python
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        i = 0
        full_file_path = filepath + str(i) + '.png'
        print(full_file_path)
        while os.path.isfile(full_file_path):
            i+=1
            full_file_path = filepath + str(i) + '.png'
        D.scenes["Scene"].render.filepath = filepath + str(i) + '.png'
        bpy.ops.render.opengl(write_still=True)
        area.spaces[0].region_3d.view_perspective = 'PERSP'
    def place_cam(self,offset_tuple):
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        cam.location = cursor_loc + Vector(offset_tuple)
        
a = flyingCam((0,1,0),20)
a.take_pic("/home/david/Documents/blender_outputs/test")

