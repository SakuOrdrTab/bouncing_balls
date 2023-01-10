# bouncing_balls
Python exercise to bounce balls all over the screen

Project plan:

1. Game logic: balls, balls bouncing, graphics without GUI >> ver 1.0
  - Pyside6

2. Gui >> ver 2.0
  - Pyside6

3. Functionality, add balls, destroy balls, gamification (achievements, score, etc)  ver 3.0
  - ??

5. Statistics incorporation? ver 4.0
  - (some)SQL, seaborn?

Current stable version:
0.1

Known issues:
- Warning issued: "QObject::startTimer: Timers cannot be started from another thread" but this does not halt program
- Program freezes after some time
- ballcount is not right
- physics are still wrong; the collisions are not physical on intent, but the balls overlap etc
- Invisible balls exist?
- The program works only with certain parameters of balls and max_tries
- Graphics are with artefacts