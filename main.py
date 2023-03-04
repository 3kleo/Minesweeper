# from tkinter import *
# from tkinter import ttk
import random


class Minesweeper:
    def __init__(self, dimensions):
        self.neighbors_looped = []
        self.neighbor_to_loop = []
        self.neighbor_clicked = []
        self.neighbor_bombs = []
        self.field_l = None
        self.field = None
        self.dimensions = dimensions
        self.generate_field()
        self.generate_bombs()
        self.calculate_bombs_in_neighbors()
        self.print_field()

    def generate_field(self):
        self.field = [[0 for i in range(self.dimensions)] for i in range(self.dimensions)]
        self.field_l = [[chr(97 + i + j) for i in range(self.dimensions)] for j in
                        range(0, (self.dimensions ** 2), self.dimensions)]

    def generate_bombs(self):
        bombs = []
        for i in range(self.dimensions):
            bombs.append((random.choice(range(self.dimensions)), random.choice(range(self.dimensions))))
            # print(bombs[i])
            self.field[bombs[i][0]][bombs[i][1]] = 1

    def print_field(self):
        for i in range(len(self.field)):
            print(self.field[i])

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
                    elif self.neighbor_bombs[row][column] > 0:
                        print(self.neighbor_bombs[row][column])  # working
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
                        break


if __name__ == "__main__":
    game = Minesweeper(5)

    # check if bomb and show numbers
    click = (1, 2)
    game.check_clicked_space(click)

# prin;t('show items: ', neighbor_clicked)
