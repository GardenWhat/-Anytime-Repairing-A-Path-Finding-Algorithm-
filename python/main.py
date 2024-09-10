import time
import os
import pygame
import utils
import node
import yaml


def read_config():
    config_path = "config/config.yml"
    with open(config_path, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return conf


def get_colors(colors_list):
    return_dict = {}
    for color_dict in colors_list:
        for name, values in color_dict.items():
            return_dict.update({name: values})
    return return_dict


config = read_config()

GRID_SIZE = config.get('GRID_SIZE')
GRID_X = config.get('GRID_X')
GRID_Y = config.get('GRID_Y')
MARGIN = config.get('MARGIN')
COLORS = get_colors(config.get('COLORS'))

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
screen = pygame.display.set_mode(
    (GRID_X * GRID_SIZE + GRID_X * MARGIN + MARGIN, GRID_Y * GRID_SIZE + GRID_Y * MARGIN + MARGIN),
    pygame.RESIZABLE)
pygame.display.set_caption('A* Algorithm')


def update_keys_in_open(open_list, path_cost):
    for item in open_list:
        if item.G + item.H >= path_cost:
            open_list.remove(item)
    return open_list


def araStar(start, weight, weightDelta):
    path_cost = 1000000000000
    incumbent = []
    open_list = []
    current = start
    open_list.append(current)
    while open_list:
        print(str(open_list))
        newSolution = improvedSolution(open_list, weight, path_cost)

        if newSolution:
            path_cost = newSolution[-1].G
            incumbent = newSolution
            utils.drawPath(incumbent, utils.randomColor(), screen, MARGIN, GRID_SIZE)
            time.sleep(.5)
        else:
            return incumbent

        weight = weight - weightDelta
        for child in current.children:
            if child.G + child.H >= path_cost and child not in open_list:
                open_list.append(child)
        open_list = update_keys_in_open(open_list, path_cost)
    return incumbent


def improvedSolution(open_list, weight, path_cost):
    while open_list:
        current = min(open_list, key=lambda o: o.G + weight * o.H)
        open_list.remove(current)   # pop the node with the lowest g + wh
        if path_cost <= current.G + weight * current.H:
            return None   # pathCost is proven to be w-admissible

        for child in current.children:
            if current.G + utils.ED(current, child) < child.G:
                child.G = current.G + utils.ED(current, child)
                child.parent = current
                utils.drawRect(COLORS.get('CYAN'), child.x, child.y, screen, MARGIN, GRID_SIZE)
                pygame.display.update()
            if child.G + child.H < path_cost:
                if child.is_goal:
                    path = []
                    while child.parent:
                        path.append(child)
                        child = child.parent
                    path.append(child)
                    return path[::-1]
                if child not in open_list:
                    open_list.append(child)
    return None


def main():

    percentChanceForWall = config.get('percentChanceForWall')
    actualPercentOfWalls = config.get('actualPercentOfWalls')
    weight = config.get('weight')
    weightDelta = config.get('weightDelta')



    grid = [[node.Node(i, j) for j in range(GRID_X)] for i in range(GRID_Y)]

    start = grid[0][GRID_Y - 1]
    start.is_start = True
    start.G = 0
    goal = grid[GRID_X - 1][0]
    goal.is_goal = True

    grid = utils.setChildren(GRID_X, GRID_Y, grid, percentChanceForWall, actualPercentOfWalls, start, goal)
    utils.drawGrid(GRID_X, GRID_Y, grid, screen, MARGIN, GRID_SIZE, COLORS)

    pygame.display.flip()
    startTime = time.time()
    path = araStar(start, weight, weightDelta)
    print('It took %s seconds to run' % str(round(time.time() - startTime, 3)))
    if path:
        utils.drawPath(path, COLORS.get('PINK'), screen, MARGIN, GRID_SIZE)
        print(f"Finished with a weight of {round(path[-1].G, 3)}")
        print(f"Perfect weight would be {round(utils.ED(start, goal), 3)}")
        utils.drawRect(COLORS.get('GREEN'), start.x, start.y, screen, MARGIN, GRID_SIZE)
        utils.drawRect(COLORS.get('RED'), goal.x, goal.y, screen, MARGIN, GRID_SIZE)
        pygame.display.update()
    else:
        print('No path from start to goal.')

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


if __name__ == "__main__":
    main()
