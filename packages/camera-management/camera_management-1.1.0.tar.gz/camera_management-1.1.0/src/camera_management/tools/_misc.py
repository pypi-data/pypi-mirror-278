def calculate_offset_from_midpoint(max_dimension: int, offset: int) -> int:
    """
    Given the dimension of a camera sensor this function calculates the coordinate for the starting point for a box with the width of 'offset'.
    :param max_dimension: Maximum size of the sensor in the wanted dimension (X or Y)
    :param offset: The size of the box you want to create
    """
    return int(max_dimension / 2 - offset / 2)
