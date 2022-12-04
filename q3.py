def robotPosition(input):
    # Declare the robot start pos
    robot_up_down = 0
    robot_left_right = 0

    # split the input into a list
    words_split = input.split(" ")

    # will only run if the first word is BEGIN
    if words_split[0] == "BEGIN":
        words_split.pop(0)
        print(words_split)
    else:
        print("Please use 'BEGIN' as the first word in the command list")
        return

    # Splits the list intp tuples of each command e.g. DIRECTION, DISTANCE
    dir_dis_split = [words_split[i:i + 2] for i in range(0, len(words_split), 2)]

    # for loop to for each tuple, updated the location of the robot after ever if statement and then combines the
    # x and y axis at the end before returning the value
    for i in dir_dis_split:
        if i[0] == "LEFT":
            robot_left_right = robot_left_right - int(i[1])
        elif i[0] == "RIGHT":
            robot_left_right = robot_left_right + int(i[1])
        elif i[0] == "UP":
            robot_up_down = robot_up_down + int(i[1])
        elif i[0] == "DOWN":
            robot_up_down = robot_up_down - int(i[1])
        elif i[0] == "STOP":
            # if STOP is detected it will end the process
            print("STOP detected")
            final_position = [robot_left_right,robot_up_down]
            return final_position

        print("No more inputs detected")
        final_position = [robot_left_right,robot_up_down]
        return final_position


# Robot input
robot_directions= "BEGIN left 3 UP 5 RIGHT 4 DOWN 7 STOP"

robot_final_position = robotPosition(robot_directions.upper())
print("The final position of the robot is: ", robot_final_position)
