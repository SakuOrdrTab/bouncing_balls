# Ver 0.01

import Ball

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
    return None

main()