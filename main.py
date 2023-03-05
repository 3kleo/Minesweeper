# from tkinter import *
# from tkinter import ttk
import random


class Minesweeper:
    def __init__(self, dimensions):
        self.field_visual = None
        self.neighbors_looped = []
        self.neighbor_to_loop = []
        self.neighbor_clicked = []
        self.neighbor_bombs = []
        self.field_l = None
        self.field = None
        self.dimensions = dimensions
        self.generate_field()
        self.generate_bombs()
        self.generate_visual_field()
        self.calculate_bombs_in_neighbors()
        self.print_field()
        self.print_neighbor_bombs()
        self.print_visual_field()
        self.game_status = True

    def generate_field(self):
        self.field = [[0 for i in range(self.dimensions)] for i in range(self.dimensions)]
        self.field_l = [[chr(97 + i + j) for i in range(self.dimensions)] for j in
                        range(0, (self.dimensions ** 2), self.dimensions)]

    def generate_bombs(self):
        bombs = []
        while len(bombs) < self.dimensions:
            bomb_pos = (random.choice(range(self.dimensions)), random.choice(range(self.dimensions)))
            if bomb_pos not in bombs:
                bombs.append(bomb_pos)

        for bomb in bombs:
            self.field[bomb[0]][bomb[1]] = 1
            
    def generate_visual_field(self):
        self.field_visual = [['X' for i in range(self.dimensions)] for j in range(self.dimensions)]

    def print_visual_field(self):
        for i in range(len(self.field_visual)):
            print(self.field_visual[i])

        print()

    def print_field(self):
        for i in range(len(self.field)):
            print(self.field[i])

        print()

    def change_visual_field(self, position):
        row = position[0]
        column = position[1]
        if self.field[row][column]:  # is bomb
            self.field_visual[row][column] = 'B'
            return
        value = self.neighbor_bombs[row][column]
        if value == 0:
            self.field_visual[row][column] = ' '
        else:
            self.field_visual[row][column] = str(value)

    def get_neighbor_positions(self, row_num, column_num):
        positions = {(max(0, row_num - 1), max(0, column_num - 1)),
                     (max(0, row_num - 1), column_num),
                     (max(0, row_num - 1), min(self.dimensions - 1, column_num + 1)),
                     (row_num, max(0, column_num - 1)),
                     (row_num, min(self.dimensions - 1, column_num + 1)),
                     (min(self.dimensions - 1, row_num + 1), max(0, column_num - 1)),
                     (min(self.dimensions - 1, row_num + 1), column_num),
                     (min(self.dimensions - 1, row_num + 1), min(self.dimensions - 1, column_num + 1))
                     }
        return positions

    def calculate_bombs_in_neighbors(self):
        self.neighbor_bombs = []
        for row in range(self.dimensions):
            self.neighbor_bombs.append([])
            for column in range(self.dimensions):
                neighbors_pos = self.get_neighbor_positions(row, column)
                # print(neighbors_pos)
                neighbors = sum(
                    [(self.field[j[0]][j[1]]) for i, j in enumerate(neighbors_pos) if self.field[j[0]][j[1]] != self.field[row][column]]
                )
                # neighbors = sorted([(field_l[j[0]][j[1]]) for i, j in enumerate(neighbors_pos) if field_l[j[0]][j[1]] != field_l[row][column]])
                # print(neighbors)
                self.neighbor_bombs[row].append(neighbors)

    def print_neighbor_bombs(self):
        for i in range(len(self.neighbor_bombs)):
            print(self.neighbor_bombs[i])

        print()

    def lose_game(self):
        for row in range(self.dimensions):
            for column in range(self.dimensions):
                self.change_visual_field((row, column))
        self.game_status = False

    def check_clicked_space(self, clicked: tuple):
        if clicked not in self.neighbor_clicked:
            self.neighbor_clicked.append(clicked)
            self.neighbor_to_loop.append(clicked)
        else:
            print('already clicked')
            return
        # self.neighbors_looped = []

        while True:
            if len(self.neighbor_to_loop) > 0:
                for pos in self.neighbor_to_loop:
                    row = pos[0]
                    column = pos[1]

                    if self.field[row][column] == 1:
                        print('bomb')
                        self.lose_game()
                    elif self.neighbor_bombs[row][column] > 0:
                        # print('direct adjacent')  # working
                        self.change_visual_field(pos)
                    else:
                        neighbors_pos = self.get_neighbor_positions(row, column)
                        neighbors_pos = [item for item in neighbors_pos if item != pos and item not in self.neighbors_looped and item not in self.neighbor_clicked]
                        # print(neighbors_pos)
                        for neighbor in neighbors_pos:
                            # print(neighbor)
                            # print(neighbor_bombs[neighbor[0]][neighbor[1]])
                            self.neighbor_clicked.append(neighbor)
                            if self.neighbor_bombs[neighbor[0]][neighbor[1]] == 0 and neighbor not in self.neighbor_to_loop and neighbor not in self.neighbors_looped:
                                self.neighbor_to_loop.append(neighbor)

                    self.neighbor_to_loop = [item for item in self.neighbor_to_loop if item != pos]
                    self.neighbors_looped.append(pos)
                    # print(neighbors)
                else:
                    if len(self.neighbor_to_loop) == 0:
                        for pos in self.neighbor_clicked:
                            self.change_visual_field(pos)
                        break


if __name__ == "__main__":
    game = Minesweeper(5)

    while game.game_status:
        input_row = int(input('insert row: '))
        input_column = int(input('insert column '))
        click = (input_row, input_column)
        game.check_clicked_space(click)
        game.print_visual_field()

    print('show items: ', game.neighbor_clicked)
