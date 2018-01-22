#This should be copied into the blender python console
from mathutils import Vector
import numpy as np
import os
class flyingCam:
    def __init__(self, normal, fovh=50,fovv=40):
        normal_vec = Vector(normal)
        mag = normal_vec.magnitude
        self.normal=normal_vec / mag
        self.FOV=fovh
        self.filepath = ''
        bpy.data.cameras["Camera"].lens_unit = 'FOV'
        bpy.data.cameras["Camera"].angle = fovh / 180.0 * pi
        bpy.data.scenes["Scene"].render.resolution_x = 2000
        bpy.data.scenes["Scene"].render.resolution_y = 2000 * tan((fovv * pi / 180.0)/2.0) / tan((fovh * pi/ 180.0)/2.0)
    def print_heading(self):
        print(cam.location)
    def aim(self):
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        heading = cam.location - cursor_loc
        rot_quat = heading.to_track_quat('Z', 'X')
        cam.rotation_euler = rot_quat.to_euler()
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
    def pic(self, filepath=''):
        #Taken from https://blender.
        #stackexchange.com/questions/30643/how-to-toggle-to-camera-view-via-python
        if filepath == '':
            filepath = self.filepath
        self.filepath = filepath
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        i = 0
        full_file_path = filepath + str(i) + '.png'
        while os.path.isfile(full_file_path):
            i+=1
            full_file_path = filepath + str(i) + '.png'
        D.scenes["Scene"].render.filepath = filepath + str(i) + '.png'
        bpy.ops.render.render(write_still=True)
        area.spaces[0].region_3d.view_perspective = 'PERSP'
    def picgl(self, filepath=''):
        #Taken from https://blender.
        #stackexchange.com/questions/30643/how-to-toggle-to-camera-view-via-python
        if filepath == '':
            filepath = self.filepath
        self.filepath = filepath
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
    def rot(self):
        active_obj = bpy.context.scene.objects.active
        active_obj_matrix = active_obj.matrix_world
        z_axis = (active_obj_matrix[0][2], active_obj_matrix[1][2], active_obj_matrix[2][2])
        #taken from: https://stackoverflow.com/questions/4930404/how-do-get-more-control-over-loop-increments-in-python
        min_angle = 180.0
        best_step = -1
        for i in range(20):
            bpy.ops.transform.rotate(value= 2 * pi / 20.0, axis=z_axis)
            active_obj_matrix = active_obj.matrix_world
            y_axis = (active_obj_matrix[0][1], active_obj_matrix[1][1], active_obj_matrix[2][1])
            print(y_axis)
            angle = self.angle(y_axis, self.normal.to_tuple())
            print(angle)
            if angle < min_angle:
                min_angle = angle
                which_step = i
                print('new min found')
        bpy.ops.transform.rotate(value= (19-which_step)*((-1.0)*(2 * pi / 20.0)), axis=z_axis)#unrotating it to the last best one
        
    def angle(self,v1, v2):
        #Taken from: https://stackoverflow.com/questions/39497496/angle-between-two-vectors-3d-python
        # v1 is your firsr vector
        # v2 is your second vector
            angle = np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
            if angle < pi:
                return angle
            else:
                return 2 * pi - angle
            
c = flyingCam((0,-1,0),60,40)
c.rot()
