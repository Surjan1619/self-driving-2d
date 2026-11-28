"""Assignment 1: Make a Car Drive Itself - starter code.

Run it with:   python main.py
Keys:  Left/Right arrows = steer   Up/Down = speed +/- 0.5
       A = autopilot on/off   R = reset   Esc = quit
"""
import math
import pygame

# ---------------- Settings ----------------
WIDTH, HEIGHT = 900, 600
BG_COLOR = (235, 235, 225)    # light floor
LINE_COLOR = (40, 40, 40)     # dark line the car must follow
CAR_COLOR = (220, 60, 50)
SENSOR_COLOR = (0, 120, 255)
FPS = 60                      # loop runs 60 times per second
TURN_RATE = 4.0               # degrees the car turns per frame at full steer
START = (450, 115, 0)         # x, y, heading (degrees, 0 = pointing right)

# Step 8: sensors.
# Each sensor is a point in front of the car. Its angle is measured FROM the car's heading:
#   -30 = 30 degrees to the LEFT of where the car points, +30 = 30 degrees to the RIGHT.
SENSOR_ANGLES = [-30, 30]     # degrees from the heading: negative = left, positive = right
SENSOR_DISTANCE = 25          # pixels ahead of the car's centre


class Car:
    def __init__(self, x, y, heading):
        self.x = x
        self.y = y
        self.heading = heading    # degrees: 0 = right, 90 = down (screen y grows downward)
        self.speed = 2.0          # pixels per frame

    def move(self, steer):
        """steer: -1.0 = full left, 0.0 = straight, +1.0 = full right.

        This is the ACT step of the loop. It runs once every frame (60 times a second)
        and does two things: (1) turn a little, (2) move forward a little.
        """
        # Safety clamp: whatever the brain or keyboard sends, keep steer between -1 and +1.
        # min(1.0, steer) cuts off anything above +1, max(-1.0, ...) cuts off anything below -1.
        # Example: steer = 3.0 -> min(1.0, 3.0) = 1.0 -> max(-1.0, 1.0) = 1.0
        steer = max(-1.0, min(1.0, steer))

        # 1. TURN.
        # TURN_RATE = 4.0 degrees per frame at full steer.
        #   steer = +1.0 -> heading grows by 4 degrees  -> car turns right (clockwise)
        #   steer = -1.0 -> heading shrinks by 4 degrees -> car turns left
        #   steer =  0.0 -> heading does not change      -> car goes straight
        # Adding to the heading turns RIGHT because in pygame y grows downwards.
        self.heading += steer * TURN_RATE

        # 2. DEGREES -> RADIANS.
        # math.cos() and math.sin() only understand radians (a full circle = 2*pi, not 360).
        # math.radians(90) = 1.5708...
        rad = math.radians(self.heading)

        # 3. MOVE FORWARD in the direction the car now points.
        # cos(angle) = how much of one step goes sideways (x),
        # sin(angle) = how much of one step goes up/down (y).
        # Examples (one step, speed = 1):
        #   heading   0 deg (right): cos = 1,    sin = 0    -> x + 1, y stays
        #   heading  90 deg (down):  cos = 0,    sin = 1    -> x stays, y + 1
        #   heading 180 deg (left):  cos = -1,   sin = 0    -> x - 1, y stays
        #   heading  45 deg (diag.): cos = 0.71, sin = 0.71 -> a bit right AND a bit down
        # cos^2 + sin^2 = 1, so the step is always exactly 1 pixel long,
        # and multiplying by self.speed makes it `speed` pixels long.
        # (draw() uses the same cos/sin idea to find where the car's nose is.)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

    def draw(self, screen):
        rad = math.radians(self.heading)
        nose = (self.x + math.cos(rad) * 14, self.y + math.sin(rad) * 14)
        left = (self.x + math.cos(rad + 2.5) * 10, self.y + math.sin(rad + 2.5) * 10)
        right = (self.x + math.cos(rad - 2.5) * 10, self.y + math.sin(rad - 2.5) * 10)
        pygame.draw.polygon(screen, CAR_COLOR, [nose, left, right])


def make_track():
    """Draw the track once on its own surface, so sensors can read it."""
    track = pygame.Surface((WIDTH, HEIGHT))
    track.fill(BG_COLOR)
    pygame.draw.ellipse(track, LINE_COLOR, (100, 100, 700, 400), 30)
    return track


# ---------------- SENSE ----------------
def sensor_points(car):
    """Return a list of (x, y) points just ahead of the car.

    It is the same cos/sin idea as Car.move(): "go N pixels in direction D".
    The only difference: the direction is the car's heading PLUS the sensor's angle.
    """
    points = []
    for angle in SENSOR_ANGLES:            # angle = -30 (left sensor), then +30 (right sensor)
        # Direction of this sensor = where the car points + the sensor's own angle.
        # Example: car heading 0 (right), left sensor -30 -> it looks 30 degrees up-right.
        rad = math.radians(car.heading + angle)
        # Start at the car's centre and go SENSOR_DISTANCE pixels in that direction.
        # cos -> how far in x, sin -> how far in y (exactly like in move()).
        sx = car.x + math.cos(rad) * SENSOR_DISTANCE
        sy = car.y + math.sin(rad) * SENSOR_DISTANCE
        points.append((sx, sy))
    # With 2 angles we return 2 points: [(left_x, left_y), (right_x, right_y)]
    return points


def read_sensors(car, track):
    """Return one True/False per sensor point: is it on the dark line?

    This is the SENSE step: for every sensor point, look at the colour of the TRACK
    under it. True = dark line, False = light floor.
    Result example: [True, False] = left sensor on the line, right sensor off it.
    """
    # List comprehension = a short for-loop that builds a list:
    # "for every (x, y) from sensor_points, put on_line(track, x, y) into the list".
    return [on_line(track, x, y) for (x, y) in sensor_points(car)]


# ---------------- THINK ----------------
# The brain's memory. It lives OUTSIDE the function, so its value survives from one
# frame to the next. (A normal variable inside brain() would be forgotten every frame.)
last_steer = 0.0


def brain(readings):
    """Turn the sensor readings into a steering value from -1.0 to +1.0.

    This is the THINK step. The rule: steer TOWARDS the sensor that sees the line.

        left   right   meaning                       steer
        True   True    centred on the line           0.0  (straight)
        True   False   line is to the LEFT           -1.0 (full left)
        False  True    line is to the RIGHT          +1.0 (full right)
        False  False   lost the line                 keep doing what we did last

    This is called "bang-bang" control: only full left, straight or full right.
    """
    # "global" tells Python: when I write last_steer = ... here, change the variable
    # ABOVE the function, do not create a new one that disappears after this frame.
    global last_steer

    # readings is a list like [True, False]. readings[0] = first (left) sensor,
    # readings[-1] = last (right) sensor. Using -1 keeps working even if we add a
    # middle sensor later: the last one is always the rightmost.
    left, right = readings[0], readings[-1]

    if left and right:
        # Both sensors are on the line: the car is centred. Go straight.
        last_steer = 0.0
    elif left and not right:
        # Only the LEFT sensor sees the line: the line is slipping away to the left.
        # Steer left (negative) to get back on top of it.
        last_steer = -1.0
    elif right and not left:
        # Only the RIGHT sensor sees the line: steer right (positive).
        last_steer = 1.0
    else:
        # Neither sensor sees the line: we lost it. We do not know where it is,
        # so we keep the last decision. If we were turning left when we lost it,
        # the line is probably still on the left, so turning left again brings us back.
        # (We do NOT change last_steer here, that is the whole trick.)
        pass

    return last_steer


# ---------------- Manual driving ----------------
def keyboard_steer():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        return -1.0
    if keys[pygame.K_RIGHT]:
        return 1.0
    return 0.0


def on_line(track, x, y):
    """True if the point (x, y) is inside the window and on the dark line."""
    if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
        return False
    r, g, b, _ = track.get_at((int(x), int(y)))
    return r + g + b < 300


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Self-driving 2D car")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 26)
    track = make_track()
    car = Car(*START)
    autopilot = False
    frames_off_line = 0
    steer = 0.0
    last_readings = None          # Step 8: remembers the previous readings (for printing changes)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # A and R: we check BOTH the letter (event.key) and the physical key
                # on the keyboard (event.scancode). With a Russian layout the R key
                # sends the letter "к", so event.key alone would not match K_r.
                # The scancode is the same whatever the layout is.
                elif event.key == pygame.K_a or event.scancode == pygame.KSCAN_A:
                    autopilot = not autopilot
                elif event.key == pygame.K_r or event.scancode == pygame.KSCAN_R:
                    car = Car(*START)
                    frames_off_line = 0
                # Step 7: speed control.
                # KEYDOWN fires ONCE per key press (not every frame while held),
                # so one press of Up = exactly +0.5 speed.
                elif event.key == pygame.K_UP:
                    car.speed += 0.5             # gas: 0.5 pixels per frame faster
                elif event.key == pygame.K_DOWN:
                    # brake: 0.5 slower, but max(0, ...) never lets speed go below 0,
                    # so the car can stop but never drive backwards.
                    car.speed = max(0.0, car.speed - 0.5)

        readings = read_sensors(car, track)                     # SENSE
        # Step 8 observation: print the readings to the terminal, but ONLY when they change.
        # (Printing every frame would flood the terminal with 60 lines per second.)
        # Delete these 3 lines when you have filled in the table.
        if readings != last_readings:
            print("left, right =", readings)
            last_readings = readings
        steer = brain(readings) if autopilot else keyboard_steer()   # THINK
        car.move(steer)                                          # ACT

        if not on_line(track, car.x, car.y):
            frames_off_line += 1

        screen.blit(track, (0, 0))
        car.draw(screen)
        for (sx, sy) in sensor_points(car):
            pygame.draw.circle(screen, SENSOR_COLOR, (int(sx), int(sy)), 4)
        mode = "AUTOPILOT" if autopilot else "MANUAL"
        # speed is shown too, so you can see Up/Down working (needed for the Step 7 experiments).
        text = f"{mode}   speed {car.speed:.1f}   steer {steer:+.2f}   frames off line: {frames_off_line}"
        screen.blit(font.render(text, True, (20, 20, 20)), (12, 12))
        screen.blit(font.render("[Up/Down] speed   [A] autopilot   [R] reset   [Esc] quit", True, (90, 90, 90)), (12, 36))
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
