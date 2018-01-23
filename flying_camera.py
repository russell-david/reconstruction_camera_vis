#This should be copied into the blender python console
from mathutils import Vector
import numpy as np
import os
class flyingCam:
    def __init__(self, normal, fovh=50,fovv=40):
        """this is the only non-default constructor. It takes in the world-up tuple, the horizontal fov and the vertical fov"""
        normal_vec = Vector(normal)
        mag = normal_vec.magnitude
        self.normal=normal_vec / mag
        self.FOV=fovh
        self.filepath = '/home/david/Documents/blender_outputs/stabilized_render'
        bpy.data.cameras["Camera"].lens_unit = 'FOV'
        bpy.data.cameras["Camera"].angle = fovh / 180.0 * pi
        bpy.data.scenes["Scene"].render.resolution_x = 2000
        bpy.data.scenes["Scene"].render.resolution_y = 2000 * tan((fovv * pi / 180.0)/2.0) / tan((fovh * pi/ 180.0)/2.0)
        print('This is a simple class for placing cameras in a virtual blender environment')
        print('you can initialize an object as obj_name = flyingCam(world up tuple, hovizontal FOV, vertical FOV)')
        print('The most useful methods are:')
        print('.place(height) which places the camera a specified distance above the clicked point')
        print('.aim() which aims at the clicked point')
        print('.pic(filepath) which takes a picture and saves it to the specified location. The filepath need only be entered once')
        print('.picgl(filepath) which produces a faster but lower-quality render')
        print('Before beggining, please make sure the camera is selected as the active object.')
        print('Also, you will generally want to set Viewpoint shading to material and make the material "emit"')
    def aim(self):
        """This points the camera toward the cursor"""
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        heading = cam.location - cursor_loc
        rot_quat = heading.to_track_quat('Z', 'X')
        cam.rotation_euler = rot_quat.to_euler()
    def to_cursor(self):
        """This moves the camera halfway to the cursor"""
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        heading = cam.location - cursor_loc
        cam.location -= heading/2.0
        rot_quat = heading.to_track_quat('Z', 'X')
        cam.rotation_euler = rot_quat.to_euler()
    def forward(self, distance=1):
        """Similar to the above, but moves a specified distance"""
        cam = D.objects["Camera"]
        #Taken from: https://blender.stackexchange.com/questions/13738/
        #how-to-calculate-camera-direction-and-up-vector
        up = cam.matrix_world.to_quaternion() * Vector((0.0, 1.0, 0.0))
        cam_direction = cam.matrix_world.to_quaternion() * Vector((0.0, 0.0, -1.0))
        cam.location += cam_direction * distance
        e_rot = cam.rotation_euler
        heading_vec = Vector((e_rot.x,e_rot.y,e_rot.z))
    def pic(self, filepath='/home/david/Documents/blender_outputs/stabilized_render'):
        """Takes a picture using the full render. The filepath is only needed on the first capture"""
        #Taken from https://blender.
        #stackexchange.com/questions/30643/how-to-toggle-to-camera-view-via-python
        if filepath == '/home/david/Documents/blender_outputs/stabilized_render':
            filepath = self.filepath
        self.filepath = filepath
        area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
        area.spaces[0].region_3d.view_perspective = 'CAMERA'
        i = 0
        full_file_path = filepath + str(i) + '.png'
        while os.path.isfile(full_file_path):
            i+=1
            full_file_path = filepath + str(i) + '.png'
        self.aim()
        self.rot()
        D.scenes["Scene"].render.filepath = filepath + str(i) + '.png'
        bpy.ops.render.render(write_still=True)
        area.spaces[0].region_3d.view_perspective = 'PERSP'
    def picgl(self, filepath=''):
        """Takes a picture more quickly"""
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
        self.aim()
        self.rot()
        D.scenes["Scene"].render.filepath = filepath + str(i) + '.png'
        bpy.ops.render.opengl(write_still=True)
        area.spaces[0].region_3d.view_perspective = 'PERSP'
    def place(self,offset):
        """Places the camera a specified distance above the clicked point"""
        cam = D.objects["Camera"]
        cursor_loc = bpy.context.scene.cursor_location
        cam.location = cursor_loc + self.normal * offset
    def rot(self):
        """Rotates the camera so it's up axis is as close as possible to the world up"""
        num_rotations = 200
        active_obj = bpy.context.scene.objects.active
        active_obj_matrix = active_obj.matrix_world
        z_axis = (active_obj_matrix[0][2], active_obj_matrix[1][2], active_obj_matrix[2][2])
        #taken from: https://stackoverflow.com/questions/4930404/how-do-get-more-control-over-loop-increments-in-python
        min_angle = 180.0
        best_step = -1
        for i in range(num_rotations):
            bpy.ops.transform.rotate(value= 2 * pi / float(num_rotations), axis=z_axis)
            active_obj_matrix = active_obj.matrix_world
            y_axis = (active_obj_matrix[0][1], active_obj_matrix[1][1], active_obj_matrix[2][1])
            angle = self.angle(y_axis, self.normal.to_tuple())
            if angle < min_angle:
                min_angle = angle
                which_step = i
        bpy.ops.transform.rotate(value= ((num_rotations - 1)-which_step)*((-1.0)*(2 * pi / float(num_rotations))), axis=z_axis)#unrotating it to the last best one
    def angle(self,v1, v2):
        """computes the < 180 angle between two vectors"""
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
