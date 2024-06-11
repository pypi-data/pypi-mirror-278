import math

class Capture:

    # Parameters
    is_button_pressed = False
    drone_x = 0.0
    drone_y = 0.0
    drone_z = 0.0
    drone_angle = 0.0
    move_x = 0.0
    move_y = 0.0
    move_z = 0.0
    rotate = 0.0
    is_captured = False
    object_position = [-25, 17, -50]
    object_rotate = 360.0
    object_scale = 0.01
    object_value_x_index = 10
    object_value_y_index = 11
    object_value_z_index = 12
    object_rotate_index = 0
    drone_value_x_index = 6
    drone_value_y_index = 7
    drone_value_z_index = 9
    drone_rotate_index = 8
    radius_limit = 100

    def __init__(self, object_position, object_rotate, object_scale, object_index_x, object_index_y, object_index_z, object_rotate_index, drone_x, drone_y, drone_z, drone_angle, radius_limit):
        self.is_button_pressed = False
        self.drone_x = 0.0
        self.drone_y = 0.0
        self.drone_z = 0.0
        self.drone_angle = 0.0
        self.move_x = 0.0
        self.move_y = 0.0
        self.move_z = 0.0
        self.rotate = 0.0
        self.is_captured = False
        self.object_position = object_position
        self.object_rotate = object_rotate
        self.object_scale = object_scale
        self.object_value_x_index = object_index_x
        self.object_value_y_index = object_index_y
        self.object_value_z_index = object_index_z
        self.object_rotate_index = object_rotate_index
        self.drone_value_x_index = drone_x
        self.drone_value_y_index = drone_y
        self.drone_value_z_index = drone_z
        self.drone_rotate_index = drone_angle
        self.radius_limit = radius_limit

    def run(self, send_array):
        if self.is_button_pressed:
            radius = math.sqrt(math.pow((self.move_x - send_array[self.drone_value_x_index] * self.object_scale), 2) + math.pow((self.move_y - send_array[self.drone_value_y_index] * self.object_scale), 2) + math.pow((self.move_z - send_array[self.drone_value_z_index] * self.object_scale), 2))
            if radius < self.radius_limit:
                if self.is_captured:
                    self.move_x = (send_array[self.drone_value_x_index] - self.drone_x) * self.object_scale
                    self.move_y = (send_array[self.drone_value_y_index] - self.drone_y) * self.object_scale
                    self.move_z = (send_array[self.drone_value_z_index] - self.drone_z) * self.object_scale
                    self.rotate = send_array[self.drone_rotate_index] - self.drone_angle
                    send_array[self.object_value_x_index] = self.object_position[0] + self.move_x
                    send_array[self.object_value_y_index] = self.object_position[1] + self.move_y
                    send_array[self.object_value_z_index] = self.object_position[2] + self.move_z
                    send_array[self.object_rotate_index] = self.object_rotate + self.rotate
                else:
                    self.drone_x = send_array[self.drone_value_x_index]
                    self.drone_y = send_array[self.drone_value_y_index]
                    self.drone_z = send_array[self.drone_value_z_index]
                    self.drone_angle = send_array[self.drone_rotate_index]
                    self.is_captured = True
        else:
            self.object_rotate = send_array[self.object_rotate_index]
            self.object_position = [send_array[self.object_value_x_index], send_array[self.object_value_y_index], send_array[self.object_value_z_index]]
            self.is_captured = False
        return send_array