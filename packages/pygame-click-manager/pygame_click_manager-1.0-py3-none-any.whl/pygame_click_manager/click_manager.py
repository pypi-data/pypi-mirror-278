import pygame.mouse as mouse


class ClickManager:
    @classmethod
    def check_buttons_for_clicks(cls, starting_pos: tuple[int, int], size: tuple[int, int], command=None) -> bool:
        if cls.is_mouse_in_area(starting_pos, size) and mouse.get_pressed()[0]:
            if command:
                command()
            return True
        return False

    @classmethod
    def is_mouse_in_area(cls, starting_pos: tuple[int, int], size: tuple[int, int]) -> bool:
        start_x, start_y = starting_pos
        end_x, end_y = cls._get_end_pos(starting_pos, size)
        x, y = mouse.get_pos()
        return start_x <= x <= end_x and start_y <= y <= end_y

    @classmethod
    def is_object_inside_another(cls, start_pos_1: tuple[int, int], size_1: tuple[int, int],
                                 start_pos_2: tuple[int, int], size_2: tuple[int, int]) -> bool:
        """
        Check if the second object is inside the first object.
        :param start_pos_1: Starting position of the first object.
        :param size_1: Size of the first object.
        :param start_pos_2: Starting position of the second object.
        :param size_2: Size of the second object.
        :return: True if the second object is inside the first object, else False.
        """
        x1, y1 = start_pos_1
        x2, y2 = start_pos_2

        end_x1, end_y1 = cls._get_end_pos(start_pos_1, size_1)
        end_x2, end_y2 = cls._get_end_pos(start_pos_2, size_2)

        return (
            x1 <= x2 <= end_x1 and y1 <= y2 <= end_y1 and
            cls._is_object_touching_another(start_pos_1, size_1, start_pos_2, size_2)
        )

    @classmethod
    def is_object_colliding_with_another(cls, start_pos_1: tuple[int, int], size_1: tuple[int, int],
                                         start_pos_2: tuple[int, int], size_2: tuple[int, int]) -> bool:
        """
        Check if the second object collides with the first object.
        :param start_pos_1: Starting position of the first object.
        :param size_1: Size of the first object.
        :param start_pos_2: Starting position of the second object.
        :param size_2: Size of the second object.
        :return: True if the objects collide, else False.
        """
        end_x1, end_y1 = cls._get_end_pos(start_pos_1, size_1)
        end_x2, end_y2 = cls._get_end_pos(start_pos_2, size_2)

        x1, y1 = start_pos_1
        x2, y2 = start_pos_2

        return (
            y1 <= y2 <= end_y1 or y1 <= end_y2 <= end_y1 or
            y2 <= y1 <= end_y2 or y2 <= end_y1 <= end_y2
        ) and (
            x1 <= x2 <= end_x1 or x1 <= end_x2 <= end_x1 or
            x2 <= x1 <= end_x2 or x2 <= end_x1 <= end_x2
        )

    @classmethod
    def _is_object_touching_another(cls, start_pos_1: tuple[int, int], size_1: tuple[int, int],
                                    start_pos_2: tuple[int, int], size_2: tuple[int, int]) -> bool:
        """
        Check if the second object is touching the first object.
        :param start_pos_1: Starting position of the first object.
        :param size_1: Size of the first object.
        :param start_pos_2: Starting position of the second object.
        :param size_2: Size of the second object.
        :return: True if the second object is touching the first object, else False.
        """
        end_x1, end_y1 = cls._get_end_pos(start_pos_1, size_1)
        end_x2, end_y2 = cls._get_end_pos(start_pos_2, size_2)

        return (
            start_pos_1[0] <= start_pos_2[0] <= end_x1 and
            start_pos_1[1] <= start_pos_2[1] <= end_y1
        ) or (
            start_pos_2[0] <= start_pos_1[0] <= end_x2 and
            start_pos_2[1] <= start_pos_1[1] <= end_y2
        )

    @staticmethod
    def _get_end_pos(starting_pos: tuple[int, int], size: tuple[int, int]) -> tuple[int, int]:
        start_x, start_y = starting_pos
        width, height = size
        return start_x + width, start_y + height
