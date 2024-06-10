import math

class Data:

    # Индексы
    move_value_x_index = 9
    move_value_y_index = 6
    move_value_z_index = 7
    rotate_value_index = 8
    sound_play_index = 5
    blades_rotate_index = 4
    rotate_front_index = 2
    rotate_side_index = 3
    battery_division_indexes = [1, 11, 12, 13, 14, 15, 16]

    # Перемещение
    move_value_x = 0.0
    move_value_y = 0.0
    move_value_z = 0.0

    # Повороты
    rotate_value = 0.0
    rotate_side = 0.0
    rotate_front = 0.0
    blades_rotate_value = 0.0

    # Заряд батареи
    battery = 1.0
    battery_consumption = 0.000001

    # Включена ли музыка
    is_sound_play = False

    # Имитация ветра
    wind_vector = [2, 1, 0]
    wind_power = 5

    # Масштабы
    move_scale = 10
    rotate_scale = 0.0001

    def __init__(self, x, y, z, rotate, rotate_front, rotate_side, blades, sound, battery, move_scale, rotate_scale, battery_consumption, wind_power, wind_vector_x, wind_vecrot_y, wind_vecrot_z):
        # Перемещение
        self.move_value_x = 0.0
        self.move_value_y = 0.0
        self.move_value_z = 0.0
        # Повороты
        self.rotate_value = 0.0
        self.rotate_side = 0.0
        self.rotate_front = 0.0
        self.blades_rotate_value = 0.0
        # Батарея
        self.battery = 1.0
        self.battery_consumption = battery_consumption
        # Включена ли музыка
        self.is_sound_play = False
        # Имитация ветра
        self.wind_vector = [wind_vector_x, wind_vecrot_y, wind_vecrot_z]
        self.wind_power = wind_power
        # Индексы
        self.move_value_x_index = x
        self.move_value_y_index = y
        self.move_value_z_index = z
        self.rotate_value_index = rotate
        self.sound_play_index = sound
        self.blades_rotate_index = blades
        self.rotate_front_index = rotate_front
        self.rotate_side_index = rotate_side
        self.battery_division_indexes = battery
        self.move_scale = move_scale
        self.rotate_scale = rotate_scale

    def move_vertical(self, send_array, stick_value):
        if self.move_value_z > 0.01:
            self.battery -= self.battery_consumption
            send_array = self.rotate_when_vertical(send_array=send_array, stick_value=stick_value)
            self.move_value_y -= self.move_scale * math.sin(Data.rotate_value * math.pi / 180) * Data.battery * stick_value
            self.move_value_x -= self.move_scale * math.cos(-Data.rotate_value * math.pi / 180) * Data.battery * stick_value
            send_array[self.move_value_x_index] = Data.move_value_x
            send_array[self.move_value_y_index] = Data.move_value_y
        return send_array

    def move_horizontal(self, send_array, stick_value):
        if self.move_value_z > 0.01:
            self.battery -= self.battery_consumption
            send_array = self.rotate_when_horizontal(send_array=send_array, stick_value=stick_value)
            self.move_value_y += self.move_scale * math.cos(Data.rotate_value * math.pi / 180) * Data.battery * stick_value
            self.move_value_x += self.move_scale * math.sin(-Data.rotate_value * math.pi / 180) * Data.battery * stick_value
            send_array[self.move_value_x_index] = Data.move_value_x
            send_array[self.move_value_y_index] = Data.move_value_y
        return send_array

    def rotate_right(self, send_array, stick_value):
        if self.move_value_z > 0.01:
            self.battery -= self.battery_consumption
            self.rotate_value -= self.rotate_scale * stick_value
            send_array[self.rotate_value_index] = self.rotate_value
        return send_array

    def rotate_left(self, send_array, stick_value):
        if self.move_value_z > 0.01:
            self.battery -= self.battery_consumption
            self.rotate_value -= self.rotate_scale * stick_value
            send_array[self.rotate_value_index] = self.rotate_value
        return send_array


    def up_move(self, send_array, stick_value):
        self.battery -= self.battery_consumption
        send_array = self.turn_on_sound(send_array=send_array)
        self.move_value_z += self.move_scale * self.battery * stick_value
        send_array[self.move_value_z_index] = Data.move_value_z
        return send_array


    def turn_on_sound(self, send_array):
        if not self.is_sound_play:
            send_array[self.sound_play_index] = 1
            self.is_sound_play = True
        return send_array


    def turn_off_sound(self, send_array):
        if self.is_sound_play:
            send_array[self.sound_play_index] = 0
        return send_array


    def down_move(self, send_array, stick_value):
        if self.move_value_z > 0:
            self.move_value_z += self.move_scale * stick_value
            send_array[self.move_value_z_index] = self.move_value_z
        else:
            send_array = self.turn_off_sound(send_array=send_array)
            self.is_sound_play = False
        return send_array


    def rotate_blades(self, send_array):
        self.blades_rotate_value += 25
        send_array[self.blades_rotate_index] = self.blades_rotate_value
        return send_array


    def rotate_when_vertical(self, send_array, stick_value):
        if -15 < self.rotate_front < 15:
            self.rotate_front -= self.rotate_scale * stick_value
        send_array[self.rotate_front_index] = self.rotate_front
        return send_array


    def rotate_when_horizontal(self, send_array, stick_value):
        if -15 < self.rotate_side < 15:
            self.rotate_side -= self.rotate_scale * stick_value
        send_array[self.rotate_side_index] = self.rotate_side
        return send_array


    def stabilisation(self, send_array):
        self.rotate_side = 0.0
        self.rotate_front = 0.0
        send_array[self.rotate_side_index] = Data.rotate_side
        send_array[self.rotate_front_index] = Data.rotate_front
        return send_array


    def charge(self, send_array):
        if self.battery > 0:
            self.battery -= self.battery_consumption
        part_number = len(self.battery_division_indexes) - 1
        for division_index in self.battery_division_indexes:
            intermediate_value = part_number / len(self.battery_division_indexes)
            if self.battery > intermediate_value:
                send_array[division_index] = 1
            else:
                send_array[division_index] = 0
            part_number -= 1
        return send_array


    def move_by_wind(self, send_array):
        if self.move_value_z > 0:
            self.move_value_x += self.wind_vector[0] * self.wind_power * self.move_scale
            self.move_value_y += self.wind_vector[1] * self.wind_power * self.move_scale
            self.move_value_z += self.wind_vector[2] * self.wind_power * self.move_scale
            send_array[self.move_value_x_index] = self.move_value_x
            send_array[self.move_value_y_index] = self.move_value_y
            send_array[self.move_value_z_index] = self.move_value_z
        return send_array


    def run(self, send_array, left_stick_vertical, left_stick_horizontal, right_stick_vertical, right_stick_horizontal, battery_limit):
        # если заряд батареи больше порогового значения, то выполняются все действия
        if self.battery > battery_limit:
            # Взлет
            if left_stick_vertical > 0.1:
                send_array = self.up_move(send_array=send_array, stick_value=left_stick_vertical)
            # Посадка
            if left_stick_vertical < -0.1:
                send_array = self.down_move(send_array=send_array, stick_value=left_stick_vertical)
            # Поворот по часовой
            if left_stick_horizontal > 0.1:
                send_array = self.rotate_right(send_array=send_array, stick_value=left_stick_horizontal)
            # Поворот против часовой
            if left_stick_horizontal < -0.1:
                send_array = self.rotate_left(send_array=send_array, stick_value=left_stick_horizontal)
            # Перемещение вперед и назад
            if right_stick_vertical < -0.1 or right_stick_vertical > 0.1:
                send_array = self.move_vertical(send_array=send_array, stick_value=right_stick_vertical)
            # Перемещение вправо и влево
            if right_stick_horizontal < -0.1 or right_stick_horizontal > 0.1:
                send_array = self.move_horizontal(send_array=send_array, stick_value=right_stick_horizontal)
            # Стабилизация
            if -0.1 < right_stick_vertical < 0.1 and -0.1 < right_stick_horizontal < 0.1 and (
                    self.rotate_front != 0 or self.rotate_side != 0):
                send_array = self.stabilisation(send_array=send_array)
            # Вращение лопастей
            if self.move_value_z > 0.01:
                send_array = self.rotate_blades(send_array=send_array)
        else:
            # если заряд батареи меньше порогового значения, то уходим на пасадку
            send_array = self.down_move(send_array=send_array, stick_value=-1)
        # Заряд батареи
        send_array = self.charge(send_array=send_array)
        # Имитация ветра
        send_array = self.move_by_wind(send_array=send_array)
        return send_array
