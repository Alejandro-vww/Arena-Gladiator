class Coordinates:
    def __init__(self, window):
        self.window = window

    def scale_x_1080p(self, value):
        return int(value/1920 * self.window.width)

    def scale_y_1080p(self, value):
        return int(value/1080 * self.window.height)

    # throws StopIteration when iteration ends and you request one more
    def x_coord_generator(self, start, end, divisions, center=None):
        center = int((end + start) / 2) if not center else center
        l_pointer, r_pointer = center, center
        jump = int((end - start)/divisions)
        yield center
        for _ in range(divisions-1):
            l_pointer -= jump
            r_pointer += jump
            if l_pointer >= start:
                yield l_pointer
            if r_pointer <= end:
                yield r_pointer

            if l_pointer <= start and r_pointer >= end:
                break

    @property
    def left_hand(self):
        return self.scale_x_1080p(190)

    @property
    def right_hand(self):
        return self.scale_x_1080p(1860)

    @property
    def height_hand(self):
        return self.scale_y_1080p(1070)

    @property
    def commander(self):
        return self.scale_x_1080p(1540), self.scale_y_1080p(1070)

    @property
    def start_button(self):
        return self.scale_x_1080p(1735), self.scale_y_1080p(1005)

    @property
    def cancel_button(self):
        return self.scale_x_1080p(1780), self.scale_y_1080p(886)

    @property
    def mulligan_button(self):
        return self.scale_x_1080p(781), self.scale_y_1080p(876)

    @property
    def config_button(self):
        return int(1890/1920 * self.window.unchecked_width), int(30/1075 * self.window.unchecked_height)

    @property
    def concede_button(self):
        return int(961/1920 * self.window.unchecked_width), int(638/1080 * self.window.unchecked_height)

    @property
    def villain(self):
        return self.scale_x_1080p(965), self.scale_y_1080p(120)

    @property
    def left_card_option(self):
        return self.scale_x_1080p(670), self.scale_y_1080p(450)

    @property
    def right_card_option(self):
        return self.scale_x_1080p(1260), self.scale_y_1080p(450)

    @property
    def left_option(self):
        return self.scale_x_1080p(780), self.scale_y_1080p(875)

    @property
    def right_option(self):
        return self.scale_x_1080p(1135), self.scale_y_1080p(875)

    def five_color_option(self, color):
        if color == 'white':
            return self.scale_x_1080p(970), self.scale_y_1080p(258)
        elif color == 'blue':
            return self.scale_x_1080p(970), self.scale_y_1080p(367)
        elif color == 'black':
            return self.scale_x_1080p(970), self.scale_y_1080p(480)
        elif color == 'red':
            return self.scale_x_1080p(970), self.scale_y_1080p(587)
        elif color == 'green':
            return self.scale_x_1080p(970), self.scale_y_1080p(690)
        print('wrong color')
        return self.scale_x_1080p(970), self.scale_y_1080p(587)









