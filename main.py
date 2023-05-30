import tkinter as tk
from tkinter import ttk
import random
import settings


class Minesweeper:
    def __init__(self, dimensions):
        self.cells = []
        self.game_area = None
        self.top_bar = None
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
        self.create_cells()
        self.initialize_gui()

    def generate_field(self):
        self.field = [[0 for i in range(self.dimensions)] for i in range(self.dimensions)]
        self.field_l = [[chr(97 + i + j) for i in range(self.dimensions)] for j in
                        range(0, (self.dimensions ** 2), self.dimensions)]

        self.root = tk.Tk()
        self.root.geometry(f'{settings.WIDTH}x{settings.HEIGHT}')
        self.root.title("Minesweeper")
        self.root.resizable(False, False)
        self.top_bar = tk.Frame(
            self.root,
            bg='blue',
            width=f'{settings.WIDTH}',
            height='100'
        )
        self.top_bar.place(x=0, y=0)
        self.game_area = tk.Frame(
            self.root,
            bg='green',
            width=f'{settings.WIDTH}',
            height='600'
        )
        self.game_area.place(x=0, y=100)

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
                    [(self.field[j[0]][j[1]]) for i, j in enumerate(neighbors_pos) if
                     self.field[j[0]][j[1]] != self.field[row][column]]
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

    def is_mine(self, row, column):
        value = self.field[row][column]
        return True if value == 1 else False

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

                    if self.is_mine(row, column):
                        print('bomb')
                        cell = self.cells[row][column]
                        cell.change_color()  # (row, column)
                        cell.write_on_cell('B')
                        self.lose_game()
                        return
                    elif self.neighbor_bombs[row][column] > 0:
                        self.change_visual_field(pos)
                        cell = self.cells[row][column]
                        cell.change_color()  # (row, column)
                        cell.write_on_cell(self.neighbor_bombs[row][column])
                    else:
                        neighbors_pos = self.get_neighbor_positions(row, column)
                        neighbors_pos = [item for item in neighbors_pos if
                                         item != pos and item not in self.neighbors_looped and item not in self.neighbor_clicked]
                        # print(neighbors_pos)
                        for neighbor in neighbors_pos:
                            # print(neighbor)
                            # print(neighbor_bombs[neighbor[0]][neighbor[1]])
                            self.neighbor_clicked.append(neighbor)
                            if self.neighbor_bombs[neighbor[0]][neighbor[
                                1]] == 0 and neighbor not in self.neighbor_to_loop and neighbor not in self.neighbors_looped:
                                self.neighbor_to_loop.append(neighbor)

                    self.neighbor_to_loop = [item for item in self.neighbor_to_loop if item != pos]
                    self.neighbors_looped.append(pos)
                    # print(neighbors)
                else:
                    if len(self.neighbor_to_loop) == 0:
                        for pos in self.neighbor_clicked:
                            self.change_visual_field(pos)
                            cell = self.cells[pos[0]][pos[1]]
                            cell.change_color()
                            cell.write_on_cell(self.neighbor_bombs[pos[0]][pos[1]])
                        break

    def create_cells(self):
        # pass
        for row in range(self.dimensions):
            self.cells.append([])
            for column in range(self.dimensions):
                x_pos = 100 + (60 * (column + 1))
                y_pos = 30 + (60 * (row + 1))
                # neighbors = self.neighbor_bombs[row][column]
                # is_mine = self.is_mine(row, column)
                self.cells[row].append(
                    Slot(self.game_area,
                         x_pos,
                         y_pos,
                         row,
                         column,
                         self) #,
                         # neighbors,
                         # is_mine,
                         # )
                )

    def initialize_gui(self):
        tk.mainloop()

    def get_neighbor_clicked(self):
        return self.neighbor_clicked


class Slot:
    def __init__(self, place, x_pos, y_pos, row, column, minesweeper): #, neighbors, is_mine, ):
        self.place = place
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.row = row
        self.column = column
        self.create_button()
        self.is_clicked = None
        self.minesweeper = minesweeper

    def create_button(self):
        self.cell = tk.Frame(self.place,
                             width=50,
                             height=50,
                             background='yellow',
                             borderwidth=1,
                             relief="solid")
        self.cell.place(x=self.x_pos, y=self.y_pos)
        self.cell.bind("<Button-1>", self.button_click)
        self.cell.bind("<Button-3>", self.write_on_cell)

    def change_color(self, _event=None):
        self.cell['bg'] = 'blue'

    def write_on_cell(self, cell_text):
        var = tk.StringVar()
        if type(cell_text) != int and cell_text != 'B':
            cell_text = "!"
        text = tk.Label(self.place,
                        textvariable=var,
                        width=1,
                        height=1,
                        bg='yellow',
                        font=("Arial", 15))
        var.set(f'{cell_text}')
        text_x = self.x_pos + (50 / 3.5)
        text_y = self.y_pos + (50 / 4)
        text.place(x=text_x, y=text_y)

    def button_click(self, _event):
        # if self.is_clicked:
        #     return
        # else:
        #     self.minesweeper.check_clicked_space((self.row, self.column))
        self.minesweeper.check_clicked_space((self.row, self.column))
        # if self.is_mine:
        #     print('game lost')
        #     return
        # elif (self.row, self.column) in self.minesweeper.get_neighbor_clicked():
        #     print('already clicked')
        # else:
        #     self.minesweeper.check_clicked_space((self.row, self.column))
        #     self.change_color()


        # tk.Button(
        #     self.place,
        #     bg='red',
        #     command=lambda: print_message((self.row, self.column))  # game.check_clicked_space((self.row, self.column))
        #     )
        # btn.place(x=str(self.x_pos), y='20', height='30', width='60')
        # btn.config(text=f'btn {self.printer}')


def print_message(msg):
    print(msg)


if __name__ == "__main__":
    game = Minesweeper(5)

    # print('test')

    # root = tk.Tk()
    #
    # root.geometry('600x700')
    # root.title("Minesweeper")
    # root.resizable(False, False)
    # top_bar = tk.Frame(
    #     root,
    #     bg='blue',
    #     width='600',
    #     height='100'
    # )
    # top_bar.place(x=0, y=0)
    #
    # game_area = tk.Frame(
    #     root,
    #     bg='green',
    #     width='600',
    #     height='600'
    # )
    # game_area.place(x=0, y=100)

    # for i in range(5):
    #     # btn_text = tk.StringVar(root)
    #     # btn_text.set(str(i))
    #     # btn = tk.Button(
    #     #     game_area,
    #     #     bg='red',
    #     #     command=lambda: print_message(btn_text)
    #     # )
    #
    #     pos_x = (20 + 40) * i
    #     # pos_y = (20 + 5) * i
    #     btn = Slot(pos_x, 20, str(i))
    #     # btn.place(x=str(pos_x), y='20', height='30', width='60')
    #     # btn.config(text=str(f'btn {i}'))
    # tk.mainloop()

    # game = Minesweeper(5)
    #
    # while game.game_status:
    #     input_row = int(input('insert row: '))
    #     input_column = int(input('insert column '))
    #     click = (input_row, input_column)
    #     game.check_clicked_space(click)
    #     game.print_visual_field()
    #
    # print('show items: ', game.neighbor_clicked)
