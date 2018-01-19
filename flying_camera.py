#This should be copied into the blender python console
from mathutils import Vector
import os
class flyingCam:
    def __init__(self, normal, fovh=50,fovv=40):
        normal_vec = Vector(normal)
        mag = normal_vec.magnitude
        self.normal=normal_vec / mag
        self.FOV=fovh
        bpy.data.cameras["Camera"].lens_unit = 'FOV'
        bpy.data.cameras["Camera"].angle = fovh / 180.0 * pi
        bpy.data.scenes["Scene"].render.resolution_x = 2000
        bpy.data.scenes["Scene"].render.resolution_y = 2000 * fovv / fovh
    def print_heading(self):
        print(cam.location)
    def aim(self):
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        heading = cam.location - cursor_loc
        rot_quat = heading.to_track_quat('Z', 'X')
        cam.rotation_euler = rot_quat.to_euler()
        print(cam.rotation_euler)
    def to_cursor(self):
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        heading = cam.location - cursor_loc
        cam.location -= heading/2.0
        rot_quat = heading.to_track_quat('Z', 'X')
        cam.rotation_euler = rot_quat.to_euler()
    def forward(self, distance=1):
        cam = D.objects["Camera"]
        #Taken from: https://blender.stackexchange.com/questions/13738/
        #how-to-calculate-camera-direction-and-up-vector
        up = cam.matrix_world.to_quaternion() * Vector((0.0, 1.0, 0.0))
        cam_direction = cam.matrix_world.to_quaternion() * Vector((0.0, 0.0, -1.0))
        cam.location += cam_direction * distance
        e_rot = cam.rotation_euler
        heading_vec = Vector((e_rot.x,e_rot.y,e_rot.z))
    def pic(self, filepath):
        #Taken from https://blender.
        #stackexchange.com/questions/30643/how-to-toggle-to-camera-view-via-python
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        i = 0
        full_file_path = filepath + str(i) + '.png'
        while os.path.isfile(full_file_path):
            i+=1
            full_file_path = filepath + str(i) + '.png'
        D.scenes["Scene"].render.filepath = filepath + str(i) + '.png'
        bpy.ops.render.opengl(write_still=True)
        area.spaces[0].region_3d.view_perspective = 'PERSP'
    def place(self,offset):
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        cam.location = cursor_loc + self.normal * offset
        
a = flyingCam((0,0,1),20)
a.place(10)
