# 2048 Adaptation : Jake Levi : May 2018
# 5 hours (5/11/18 1:00)
# 3 hours (5/11/18 16:18) FINISHED ENGINE
# 4.5 hours (5/12/18 2:16) FINISHED GAME

import pygame
import copy
import random
from roundrects import aa_round_rect, round_rect


# World State
class Game2048:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.res = (128 * width, 128 * height)
        self.board = [[0] * self.width for i in range(self.height)]
        self.screen = None


# ----------------------------GAME FUNCTIONS---------------------------- #
# Board Direction -> Board
# Takes in the new board and returns the board 'tilted' in passed direction
def tilt(board, direction):
    # 1. Iterate through board until non-zero value
    # 2. Single tilt the non-zero, continue

    new_board = copy.deepcopy(board)
    has_changed = True

    while has_changed:
        has_changed = False

        if direction == "L" or direction == "U":
            for i in range(len(board)):
                for j in range(len(board[0])):
                    if new_board[i][j] != 0:
                        updated_board = single_tilt(new_board, direction, i, j)
                        has_changed = has_changed or updated_board != new_board
                        new_board = updated_board
        else:
            i = len(board) - 1
            j = len(board[i]) - 1
            while i >= 0:
                while j >= 0:
                    if new_board[i][j] != 0:
                        updated_board = single_tilt(new_board, direction, i, j)
                        has_changed = has_changed or updated_board != new_board
                        new_board = updated_board
                    j -= 1
                j = len(board[i]) - 1
                i -= 1

    return new_board


# Board Direction Number Number -> Game
# Takes in a direction and reference coordinates, changes the game board
def single_tilt(board, direction, i, j):
    # 1. Check space in direction of tilt (Checking for out of bounds error first)
    # 2.
    #   a. if space is 0, slide value over (change old spot to 0), return to step 2
    #   b. Else merge the two values (changing the old spot to 0)

    new_board = copy.deepcopy(board)

    new_i = i
    new_j = j
    if direction == "L" and j - 1 >= 0:
        new_j -= 1
    elif direction == "R" and j + 1 <= (len(new_board[0]) - 1):
        new_j += 1
    elif direction == "U" and i - 1 >= 0:
        new_i -= 1
    elif direction == "D" and i + 1 <= len(new_board) - 1:
        new_i += 1
    else:
        return new_board  # Out of Bounds, Same Board

    neighbour = new_board[new_i][new_j]
    if neighbour == 0:  # If the space is empty, slide down
        new_board[new_i][new_j] = new_board[i][j]
        new_board[i][j] = 0
        new_board = single_tilt(new_board, direction, new_i, new_j)
    elif neighbour == new_board[i][j]:  # If the two values are equal, merge 'em!
        new_board[new_i][new_j] *= 2
        new_board[i][j] = 0

    return new_board


# [Maybe Board] -> [Maybe Board]
# Spawns a random tile on the board, or game overs if there are no spaces left
# 1. Find all spaces in array with value 0, return an list of their indexes
# 2. If the game is False or the array is empty, return False
# 3. Randomly choose a value from the array from step 1 DONE
# 4. Place either a 4 (10%) or 2 (90%) at the board index of the result of step 2 DONE


def spawn_tile(board):
    free_spaces = index_of(board, 0)
    if len(free_spaces) == 0:
        return False

    empty = free_spaces[
        random.randrange(len(free_spaces))]  # A randomly chosen board space from the list of empty spaces
    new_num = random.choices([2, 4], [3, 1])

    # Takes (y, x) and converts it to board[y][x], sets the value to 2 or 4
    new_board = copy.deepcopy(board)
    new_board[empty[0]][empty[1]] = new_num[0]

    return new_board


# [Maybe Board] Number -> [List-of Number]
# Takes in a board and a value and returns a list of the indexes where the key appears
def index_of(board, key):
    if not board:
        return []
    else:
        indices = []
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == key:
                    indices.append((i, j))  # returns (y, x)
        return indices


# Game -> None
# Prints the board to the terminal
def print_board(game):
    for line in game.board:
        print(line)


# Game -> Boolean
# Determines whether the board has any other moves left
def is_game_over(game):
    # Tries tilting board, if the tilt changes the board, return False, otherwise, return True
    return tilt(game.board, "L") == game.board and tilt(game.board, "U") == game.board and \
           tilt(game.board, "R") == game.board and tilt(game.board, "D") == game.board


# Game -> None
# Greys out screen, displaying/returning score & board
def grey_screen(game):
    grey_out = pygame.Surface(game.res)
    grey_out.fill((47, 79, 79))
    grey_out.set_alpha(100)
    game.screen.blit(grey_out, (0, 0))
    pygame.display.flip()


def score(game):
    high_val = 0
    freq = 0
    for row in game.board:
        for num in row:
            if num > high_val:
                freq = 1
                high_val = num
            elif num == high_val:
                freq += 1
    # Deal with multiple high tiles
    if freq == 1:
        return high_val
    else:
        return int(high_val * (1 + (freq / (game.width * game.height))))


# ----------------------------GRAPHICS---------------------------- #
# Game -> Surface
# Takes in the width and height (# of squares) of the desired grid
def draw_board(game):
    res = (128 * game.width, 128 * game.height)
    background = pygame.Surface(res)
    for x in range(game.width):
        for y in range(game.height):
            aa_round_rect(background, (128 * x, 128 * y, 128, 128), (169, 169, 169), 5, 8)
            pygame.draw.rect(background, (169, 169, 169), (128 * x, 128 * y, 128, 128), 8)
    return background


def write(val):
    # Divide 100 by the number of digits to reach the correct size
    # 1 digit = 100
    # 2 digits = 90
    my_font = pygame.font.SysFont("Arial", 100 - (len(val) * 10), True)
    my_text = my_font.render(val, True, (255, 255, 255))
    my_text = my_text.convert_alpha()
    return my_text


# Number -> Surface
# Takes in a value and produces a tile with unique colour
def make_tile(val):
    tile = pygame.Surface((112, 112))
    round_rect(tile, (0, 0, 112, 112), val_to_colour(val), 4)
    tile.set_colorkey((0, 0, 0))
    text_surface = write(str(val))
    # 1 digit = 35, 0
    # 2 digits = 20, 5
    # 3 digits = 5, 10
    # 4 digits  = 0, 15
    x = 35 - (15 * (len(str(val)) - 1))
    if len(str(val)) >= 4:
        x = 0
    y = (len(str(val)) - 1) * 5
    tile.blit(text_surface, (x, y))
    return tile


# Number -> (Number, Number, Number)
# Takes in a value and produces a colour tuple according to the dictionary
def val_to_colour(val):
    return {
        2: (173, 216, 230),
        4: (102, 205, 170),
        8: (176, 196, 222),
        16: (60, 179, 113),
        32: (255, 160, 122),
        64: (0, 191, 255),
        128: (244, 164, 96),
        256: (50, 205, 50),
        512: (218, 165, 32),
        1024: (34, 139, 34),
        2048: (30, 144, 255),
        4096: (147, 112, 219),
        8192: (255, 69, 0),
        16384: (220, 20, 60),
        32768: (210, 105, 30),
        65536: (255, 127, 80),
        131072: (124, 252, 0)
    }.get(val, (47, 79, 79))


# Game -> Image
# Outputs the graphical representation of the board (tiles only)
def tiles_render(game):
    tiles = pygame.Surface((128 * game.width, 128 * game.height))
    for x in range(game.width):
        for y in range(game.height):
            if game.board[y][x] != 0:
                tiles.blit(make_tile(game.board[y][x]), ((128 * x) + 8, (128 * y) + 8))
    tiles.set_colorkey((0, 0, 0))
    return tiles


# Number Number [Number] -> Number
def main(w=5, h=5, ai=0):
    # ----------------------------SETUP---------------------------- #
    game = Game2048(w, h)

    if ai == 0:
        pygame.init()
        game.screen = pygame.display.set_mode(game.res)
        max_tile = pow(2, (game.width * game.height + 1))
        pygame.display.set_caption("Max Tile Possible: " + str(max_tile))
        clock = pygame.time.Clock()
        fps = 60  # FPS cap
        background = draw_board(game)
        game.screen.blit(background, (0, 0))
        pygame.display.flip()

        # ----------------------------GAME LOOP---------------------------- #
        #   1. Take in keypress
        #   2. Tilt board
        #   3. Spawn a random tile
        # Initial double spawn_tile() to begin the game with 2 tiles

        game.board = spawn_tile(spawn_tile(game.board))
        print_board(game)
        game.screen.blit(tiles_render(game), (0, 0))
        pygame.display.flip()

        while True:
            old_board = copy.deepcopy(game.board)
            clock.tick(fps)
            if ai == 0:
                wait_input = True
                while wait_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                            game.board = tilt(game.board, "L")
                            wait_input = False
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                            game.board = tilt(game.board, "R")
                            wait_input = False
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                            game.board = tilt(game.board, "U")
                            wait_input = False
                        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                            game.board = tilt(game.board, "D")
                            wait_input = False
                        if event.type == pygame.QUIT:
                            # Return Score if user quits
                            return score(game)
            elif ai == 1:
                tilt(game.board, random.choice(["L", "R", "U", "D"]))
            else:
                print("Invalid AI Setting")
                exit(1)

            if game.board != old_board:
                game.board = spawn_tile(game.board)
                # Make board animation look more natural in console
                print("\n" * 100)
                game.screen.blit(background, (0, 0))
                game.screen.blit(tiles_render(game), (0, 0))
                pygame.display.flip()
                print_board(game)
            elif is_game_over(game):
                grey_screen(game)
                wait_input = True
                while wait_input:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                            print("Score", score(game))
                            print("\n" * 100)
                            print("New Game")
                            print("\n")
                            main(game.width, game.height)
                        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                            return score(game)


if __name__ == "__main__":
    # call the main function
    w = int(input("Width: "))
    h = int(input("Height: "))
    print_board()
    print("score: ", main(w, h))
