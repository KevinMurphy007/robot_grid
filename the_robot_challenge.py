import os
import csv
#read file
def read(reading):
    with open(reading) as input:
        reader = csv.reader(input)
        map = []
#distinguish values
        initial_position = next(reader)
        initial_position = [int(initial_position[0]), int(initial_position[1])]
        moves = int(next(reader)[0])
        for row in reader:
            num=[]
            for val in row:
                num.append(int(val))
            map.append(num)
    return moves, initial_position, map
#output format
def generate_file(list_moves, my_dir):
    with open(my_dir + '/' + 'robot.moves.40x40.Kevin.csv', 'w') as output:
        writer = csv.writer(output)
        heading = 'row',' col'
        writer.writerow(heading)
        writer.writerows(list_moves)

#pockets are destinations that contain a number of high values in the map
def find_pocket(map, x, y):
    pocket_size = map[y][x]

    if x + 1 < len(map[0]):
        pocket_size += map[y][x+1]
        if y + 1 < len(map):
            pocket_size += map[y+1][x+1]
        if y - 1 > 0:
            pocket_size += map[y-1][x+1]

    if x - 1 > 0:
        pocket_size += map[y][x-1]
        if y + 1 < len(map):
            pocket_size += map[y+1][x-1]
        if y - 1 > 0:
            pocket_size += map[y-1][x-1]

    if y + 1 < len(map):
        pocket_size += map[y+1][x]
    if y - 1 > 0:
        pocket_size += map[y-1][x]

    return pocket_size
def find_best_pocket(map, initial_position, moves):
    parameter_x = initial_position[0] + moves
    parameter_y = initial_position[1] + moves
    max = 0
    max_pocket = 0
    for y,list_of_num in enumerate(map):
        if initial_position[1] - moves < y < initial_position[1] + moves:
            for x,num in enumerate(list_of_num):
                if initial_position[0] - moves < y < initial_position[0] + moves:
                    pocket = find_pocket(map, x, y)
                    if pocket > max_pocket:
                        max_pocket = pocket
                        max = num
                        goal_coord = (x,y)
    return goal_coord
#check you surroundings each move to see if there is a big number
def scan_surround(position, map):
    max_num = 0
    movement = 0
    x = position[0]
    y = position[1]

    if x + 1 < len(map[0]):

        if map[y][x + 1]> max_num:
            max_num = map[y][x + 1]
            movement = [1,0]

        if y + 1 < len(map):
            if map[y + 1][x + 1]> max_num:
                max_num = map[y + 1][x + 1]
                movement = [1,1]

        if y - 1 > 0:
            if map[y - 1][x + 1]> max_num:
                max_num = map[y - 1][x + 1]
                movement = [1,-1]
    if x - 1 > 0:
        if map[y][x - 1]> max_num:
            max_num = map[y][x - 1]
            movement = [-1,0]

        if y + 1 < len(map):
            if map[y + 1][x - 1]> max_num:
                max_num = map[y + 1][x - 1]
                movement = [-1,1]

        if y - 1 > 0:
            if map[y - 1][x - 1]> max_num:
                max_num = map[y - 1][x - 1]
                movement = [-1,-1]

    if y + 1 < len(map):
        if map[y + 1][x]> max_num:
            max_num = map[y + 1][x]
            movement = [0,1]

    if y - 1 > 0:
        if map[y - 1][x]> max_num:
            max_num = map[y - 1][x]
            movement = [0,-1]

    return max_num, movement

#well, go explore you bot
def explore(moves, initial_position, map):

    destination = find_best_pocket(map, initial_position, moves)
    current_position = initial_position

    x_distance = destination[0] - current_position[0]
    y_distance = destination[1] - current_position[1]

    move_list = []
    points = map[current_position[1]][current_position[0]]

    for i in range(moves):
        #scan for bigs
        max_surround, movement = scan_surround(current_position, map)

        #detour to bigger Val
        if max_surround > 1:

            move_list.append(movement)
            current_position[0] += movement[0]
            current_position[1] += movement[1]
            max_surround = 0

        #else: move toward destination
        else:

            if x_distance == 0:
                x = 0
            elif x_distance / abs(x_distance) == -1:
                x = -1
                x_distance += 1
            elif x_distance / abs(x_distance) == 1:
                x = 1
                x_distance -= 1

            if y_distance == 0:
                y = 0
            elif y_distance / abs(y_distance) == -1:
                y = -1
                y_distance += 1
            elif y_distance / abs(y_distance) == 1:
                y = 1
                y_distance -= 1
            move_list.append([x,y])
            current_position[0] += x
            current_position[1] += y

        moves -= 1

        points += map[current_position[1]][current_position[0]]

        map[current_position[1]][current_position[0]] = 0
        #if at pocket, go again
        if current_position == destination:
            destination = find_best_pocket(map, current_position, moves)
            x_distance = destination[0] - current_position[0]
            y_distance = destination[1] - current_position[1]

    return move_list, points, map

#variable naming
my_dir = os.path.dirname(os.path.realpath(__file__))
location1 = '/' + 'robot.map.40x40.TO_USE.csv'

#def calling
moves, initial_position, map = read(my_dir + location1)
move_list, points, map = explore(moves, initial_position, map)
generate_file(move_list, my_dir)

#outputs for orientation:
print(points)
for row in map:
    print(row)
