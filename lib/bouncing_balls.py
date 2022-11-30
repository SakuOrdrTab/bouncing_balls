# Ver 0.01
# Ver 0.02 Proto-test for GUI
# Ver 0.1 modules include rudimentary physics, rudimentary graphics, refractoring modules
# Ver 0.1.1 Ball creation added, debugging
# Ver 0.2 Added ball graphic scene frame
# Ver 0.2.1 Directory restructuring

import Ball
import gui
import Ball_frame

def create_ball(ball_list, frame, max_tries = 10):
    if len(ball_list) < 1:
        return Ball.Ball(frame)
    for tries in range(0, max_tries):
        creation = Ball.Ball(frame)
        if creation.touches_wall(frame) == False:
            ok_ball = True
        else:
            ok_ball = False
        for ball in ball_list:
            if ball.overlaps(creation) == True:
                ok_ball = False
        if ok_ball:
            return creation
    return None


def main():
    # create balls
    # loop:
    #   move balls
    #   bounce balls
    #   draw balls
    #   wait to 10 ms
    # exit  
    
    # debug:
    ball_list = []
    ballframe = Ball_frame.Ball_frame(1, 1, 1080, 780)

    max_balls = 100
    for i in range(0,max_balls):
        ball = create_ball(ball_list, ballframe, max_tries = 10)
        if ball != None:
            ball_list.append(ball)

    # for ball in ball_list:
    #    print(ball)

    print("Balls in list: ", len(ball_list))

    gui.main_gui(ball_list, ballframe)
    return None

main()