# Ver 0.01
# Ver 0.02 Proto-test for GUI
# Ver 0.1 modules include rudimentary physics, rudimentary graphics, refractoring modules
# Ver 0.1.1 Ball creation added, debugging
import Ball
import gui

def create_ball(ball_list, max_tries = 10):
    if len(ball_list) < 1:
        return Ball.Ball()
    for tries in range(0, max_tries):
        creation = Ball.Ball()
        if creation.touches_wall() == False:
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

    max_balls = 150
    for i in range(0,max_balls):
        ball = create_ball(ball_list, max_tries = 500)
        if ball != None:
            ball_list.append(ball)

    # for ball in ball_list:
    #    print(ball)

    print("Balls in list: ", len(ball_list))

    gui.main_gui(ball_list)
    return None

main()