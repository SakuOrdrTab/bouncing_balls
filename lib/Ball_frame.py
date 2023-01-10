# Frame for ballfield
# Ver 0.1 First creation

class Ball_frame():
    """
    Class to hold the wanted dimensions of frame to hold the balls and physics
    """    
    # variables:
    # min_x
    # min_y
    # max_x
    # max_y

    def __init__(self, min__x, min__y, max__x, max__y):
        """constructor for Ball_frame.

        Args:
            min__x (int): minimum x of frame
            min__y (int): min y
            max__x (int): maximum x of frame
            max__y (int): max y

        Returns:
            None
        """        
        self.min_x = min__x
        self.min_y = min__y
        self.max_x = max__x
        self.max_y = max__y
        return None
