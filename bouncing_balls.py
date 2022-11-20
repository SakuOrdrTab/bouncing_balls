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
    ball = Ball.Ball()
    ball2 = Ball.Ball()
    print("ball1: ", ball.radius)
    print(ball.x, ball.y)
    print("ball2: ", ball2.radius)
    print(ball2.x, ball2.y)
    print(ball.touches_wall())
    print(ball2.touches_wall())
    
    return None

main()