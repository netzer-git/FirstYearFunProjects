import numpy as np
import matplotlib.pyplot as plt
import random as rnd

# --------------------------------playground-----------------------------------
# enter population number
HUMANS = 50
# enter the starting number of sick people
SICK = 10
# enter the percentage of people in quarantine
IN_QUARANTINE = 0.3
# enter chance of infection
INFECTION_RATE = 0.8
# enter the simulation length in days
TIME = 500
# enter the time it takes to recover in days
RECOVERY_TIME = 50
# can recovered people get sick again ?
REINFECT = False
# enter chance of immunity after recovery (if REINFECT is True - enter 1)
IMMUNE = 0.5
# enter chance of death
DEATH = 0.1

# PLEASE DONT TOUCH
SIM_AREA = 100
COLORS = np.array(["blue", "red", "green"])
MOVEMENT_CHANGE = 15
UPDATE = 0.01
RADIUS = 2
OUTSIDE = 1 - IN_QUARANTINE
WALKING_AROUND = 1


# -----------------------------------dots--------------------------------------
class Dot:
    def __init__(self, x, y):

        self.x = x  # x axis
        self.y = y  # y axis
        self.status = 0  # pandemic status
        self.duration = 0  # sick duration
        self.pattern = -1  # move pattern
        self.x_move = 0  # x move speed
        self.y_move = 0  # y move speed

    def check_collision(self, b):
        """
        check collision with another dot
        """
        if abs(self.x - b.x) < RADIUS and abs(self.y - b.y) < RADIUS:
            return True
        return False

    def update_pattern(self):
        self.x_move = rnd.randint(-1, 1)
        self.y_move = rnd.randint(-1, 1)
        self.pattern = 0
        while not self.x_move and not self.y_move:
            self.x_move = rnd.randint(-1, 1)
            self.y_move = rnd.randint(-1, 1)

    def go_the_other_way(self):
        self.x_move = -self.x_move
        self.y_move = -self.y_move

    def update_move(self):
        """
        the function move the dots axis if possible and updates the movment pattern if needed
        """
        # in case of death
        if self.status == -1:
            self.x = -10
            self.y = -10
        # update move pattern if needed
        if self.pattern >= MOVEMENT_CHANGE:
            self.update_pattern()
        # in case of non-moving dots
        elif self.pattern == -1:
            return
        else:
            self.pattern += 1
        # update axis by axis-movement
        if self.x >= 100 or self.x <= 0:
            # move y axis, update x and pattern
            self.go_the_other_way()
            self.x += self.x_move * 2
        elif self.y >= 100 or self.y <= 0:
            # move x axis, update y and pattern
            self.go_the_other_way()
            self.y += self.y_move * 2
        else:
            self.x += self.x_move * WALKING_AROUND
            self.y += self.y_move * WALKING_AROUND
        self.pattern += 1

    def update_recover(self):
        if self.status == 1:
            self.duration += 1
            if self.duration == RECOVERY_TIME:
                if rnd.random() < IMMUNE:
                    self.status = 2
                else:
                    self.status = 0
                if rnd.random() < DEATH:
                    self.status = -1

    def infect(self, b):
        if rnd.random() < INFECTION_RATE:
            # לבדוק דברים
            if self.status == 2 or b.status == 2:
                if not REINFECT:
                    return
            if self.status != 1:
                self.duration = 0
            if b.status != 1:
                b.duration = 0
            if self.status == 1:
                b.status = 1
            elif b.status == 1:
                self.status = 1


# -----------------------------------init--------------------------------------
def create_dots():
    """
    create 2D list including the X and the Y axis of the people
    """
    all_dots = []
    sick_count = 0
    quarantine_count = 0
    # create all the people
    for i in range(HUMANS):
        # create new dot
        dot = Dot(rnd.randint(0, SIM_AREA), rnd.randint(0, SIM_AREA))
        # creates the infected
        if sick_count < SICK:
            dot.status = 1
            sick_count += 1
        # crate the moving dots
        if quarantine_count < HUMANS * OUTSIDE:
            dot.update_pattern()
            quarantine_count += 1
        # add to dot list
        all_dots.append(dot)

    # return the full dots information
    return all_dots


def create_color_map(dots):
    """
    creates color map for pyplot color map
    """
    color_map = []
    for i in range(HUMANS):
        color_map.append(dots[i].status)
    return np.array(color_map)


# --------------------------------plot update-----------------------------------
def update_dots(dots):
    """
    updates each one of the moving dots
    checks for recovered dots
    """
    for i in range(HUMANS):
        dots[i].update_move()
        dots[i].update_recover()


def infect_dots(dots):
    """
    checks for infection and move dots from healthy to infected
    """
    for i in range(HUMANS):
        for j in range(i + 1, HUMANS):
            if dots[i].check_collision(dots[j]):
                dots[i].go_the_other_way()
                dots[i].update_move()
                dots[i].infect(dots[j])


def get_x_list(dots):
    """
    :return: the list of x axis of all the dots
    """
    return [dot.x for dot in dots]


def get_y_list(dots):
    """
    :return: the list of y axis of all the dots
    """
    return [dot.y for dot in dots]


def get_state(dots, state):
    count = 0
    for i in range(HUMANS):
        if dots[i].status == state:
            count += 1
    return count


# -----------------------------------main--------------------------------------
def run_plot():
    """
    main function - runs the plot and updates it
    """
    # creating people
    dots = create_dots()

    for i in range(TIME):
        print("day ", i + 1)
        # set frame
        plt.xlim(0, SIM_AREA)
        plt.ylim(0, SIM_AREA)
        state = 'Healthy: ' + str(get_state(dots, 0)) + ' --> Sick: ' + str(get_state(dots, 1)) + ' --> Recovered: '\
                + str(get_state(dots, 2))
        death = '\n Deaths: ' + str(get_state(dots, -1))
        plt.xlabel(state + death)
        # update plot
        update_dots(dots)
        infect_dots(dots)
        color_map = create_color_map(dots)
        # plot
        x_axis = get_x_list(dots)
        y_axis = get_y_list(dots)
        plt.scatter(x_axis, y_axis, c=COLORS[color_map])
        # update each
        plt.draw()  # draw
        plt.pause(UPDATE)  # pause
        plt.clf()  # clear


if __name__ == '__main__':
    run_plot()
