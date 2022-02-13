import cv2
from copy import deepcopy


# pixel Id - identify by greyscale value
BLACK = 0
WHITE = 255
ALREADY_VISITED = 127
PATH_REDVALUE = 255


def get_options(maze, position):
    options = []
    x, y = position
    height = len(maze)
    width = len(maze[0])

    pixels_to_check = [(x - 1, y),
                       (x + 1, y),
                       (x, y - 1),
                       (x, y + 1)]

    for x, y in pixels_to_check:
        if x > 0 and x < width and y > 0 and y < height and maze.item(x, y) == WHITE:
            options.append((x, y))

    return options


def get_starting_position(maze):
    for i in range(len(maze[0])):
        if maze[0][i] == WHITE:
            return (0, i)
    
    for i in range(len(maze)):
        if maze[i][0] == WHITE:
            return (i, 0)

    raise ValueError('did not find an entry point')


def isfinish(maze, position):
    x, y = position
    bottom_border = len(maze) - 1
    right_border = len(maze[0]) - 1

    if maze.item(x, y) == WHITE and x == right_border or y == right_border:
        return True
    else:
        return False


def traverse(maze, position, path): 
    if isfinish(maze, position):
        path.append(position)
        return path

    maze.itemset(position, ALREADY_VISITED)
    options = get_options(maze, position)
    num_options = len(options)

    if num_options == 0:
        return None

    elif num_options == 1:
        if traverse(maze, options[0], path) != None:
            path.append(position)
            return path
        else:
            return None

    elif num_options > 1:
        path_found = False
        
        for option in options:
            subpath = [position]

            if traverse(maze, option, subpath) != None:
                path += subpath
                path_found = True
                return path

        return None


def paint_path(maze, path):
    colour_maze = cv2.cvtColor(maze, cv2.COLOR_GRAY2BGR)

    for x, y in path:
        colour_maze.itemset(x, y, 0, 0)
        colour_maze.itemset(x, y, 1, 0)
        colour_maze.itemset(x, y, 2, PATH_REDVALUE)

    return colour_maze


def solve_maze(maze):
    solved_maze = deepcopy(maze)
    start_position = get_starting_position(maze)
    path = traverse(solved_maze, start_position, path = [start_position])

    if path == None:
        raise ValueError('no solution available')

    solved_maze = paint_path(solved_maze, path)

    return solved_maze


def main(image_path):
    maze_img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    if maze_img is None:
        raise ValueError('file ' + image_path + ' does not exist')
        
    solution = solve_maze(maze_img)

    cv2.imshow('raw_maze', maze_img)
    cv2.imshow('solved_maze', solution)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        main('mazes/bigbigmaze.png')