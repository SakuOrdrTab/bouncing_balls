# Ver 0.01
# Ver 0.02 Proto-test for GUI
# Ver 0.1 modules include rudimentary physics, rudimentary graphics, refractoring modules

import Ball
import gui

def main():
    # create balls
    # loop:
    #   move balls
    #   bounce balls
    #   draw balls
    #   wait to 10 ms
    # exit  
    
    # debug:
    ball1 = Ball.Ball()
    ball2 = Ball.Ball()
    print(ball1)
    print(ball2)
    print("Ball distance: {:.1f}".format(Ball.Ball.ball_distance(ball1, ball2)),
          "Balls overlap: ", Ball.Ball.overlap(ball1, ball2))
    ball_list = [ball1, ball2]
    gui.main_gui(ball_list)
    return None

main()