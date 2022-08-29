from tkinter import *
from tkinter import messagebox
import random
import customtkinter
from PIL import ImageTk, Image


class Minesweeper(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title('Minesweeper')
        self.iconbitmap('bomb.ico')
        self.font = ('Tahoma Bold', 12)
        if self.appearance_mode:
            self.bg_color = '#2a2c2f'
            self.btn_bg = '#565b5e'
        else:
            self.bg_color = '#d0d4d8'
            self.btn_bg = 'light gray'
        self.img = ImageTk.PhotoImage(Image.open('flag.png').resize((30,30)))
        self.img_flag = ImageTk.PhotoImage(Image.open('flag.png').resize((60,60)))
        self.img_bomb = ImageTk.PhotoImage(Image.open('bomb.png').resize((30,30)))
        self.img_watch = ImageTk.PhotoImage(Image.open('watch.png').resize((60,60)))
        self.img_happy = ImageTk.PhotoImage(Image.open('happy.png').resize((60,60)))
        self.img_sad = ImageTk.PhotoImage(Image.open('sad.png').resize((60,60)))
        self.img_cool = ImageTk.PhotoImage(Image.open('cool.png').resize((60,60)))
        self.frame_header = customtkinter.CTkFrame(master=self)
        self.frame_header.pack(side='top', fill='x')
        self.difficulty_var = customtkinter.StringVar(value="Easy")
        combobox = customtkinter.CTkComboBox(master=self.frame_header,
                                            values=["Easy", "Medium", "Hard"],
                                            command=self.change_difficulty,
                                            variable=self.difficulty_var)
        combobox.pack(side='left', padx=10, pady=5)
        self.frame_info = customtkinter.CTkFrame(self.frame_header, bg_color=self.bg_color, fg_color=self.bg_color)
        self.frame_info.pack(side='left', padx=10, pady=5, expand=True)
        self.frame_board = customtkinter.CTkFrame(master=self)
        self.frame_board.pack(side='top', fill='both', expand=True)
        self.board = []
        self.timer_id = None
        self.colors = ['none', 'blue', 'green', 'red', 'dark blue', 'brown', 'cyan', 'black', 'grey']
        self.center(self)
        self.build_board()


    def face_click(self, e):
        if self.game_start:
            if messagebox.askyesno("Game in Progress", "A game is already in progress, are you sure you want to start a new game?"):
                self.build_board()
        else:
            self.build_board()

    def build_board(self):
        self.game_start = False
        self.timer = 0
        if self.timer_id:
            self.after_cancel(self.timer_id)
        for child in self.frame_board.winfo_children():
            child.grid_forget()
        for child in self.frame_info.winfo_children():
            child.grid_forget()
        for i in range(len(self.board)):
            self.frame_board.grid_rowconfigure(i, weight=0)
            for j in range(len(self.board[i])):
                self.frame_board.grid_columnconfigure(j, weight=0)
        if self.difficulty_var.get() == 'Easy':
            self.rows = 8
            self.cols = 10
            self.num_mines = 10
        elif self.difficulty_var.get() == 'Medium':
            self.rows = 14
            self.cols = 18
            self.num_mines = 40
        elif self.difficulty_var.get() == 'Hard':
            self.rows = 20
            self.cols = 24
            self.num_mines = 99
        self.current_mines = self.num_mines
        self.label_mines = customtkinter.CTkLabel(master=self.frame_info, text=str(self.current_mines), bg_color=self.bg_color, 
                width=40, text_font=('Tahoma', 18))
        self.label_mines.grid(row=0, column=0)
        Label(self.frame_info, image=self.img_flag, bg=self.bg_color, width=45).grid(row=0, column=1)
        self.label_face = Label(self.frame_info, image=self.img_happy, width=60, bg=self.bg_color)
        self.label_face.grid(row=0, column=2, padx=80)
        self.label_face.bind('<Button-1>', self.face_click)
        self.label_timer = customtkinter.CTkLabel(master=self.frame_info, text='000', bg_color=self.bg_color, 
                width=40, text_font=('Tahoma', 18))
        self.label_timer.grid(row=0, column=3, padx=(5,5))
        Label(self.frame_info, image=self.img_watch, bg=self.bg_color, width=55).grid(row=0, column=4)
        self.board = [[0 for i in range(0,self.cols)] for j in range(0,self.rows)]
        self.buttons = []
        for i in range(len(self.board)):
            self.frame_board.grid_rowconfigure(i, weight=1)
            buttons = []
            for j in range(len(self.board[i])):
                self.frame_board.grid_columnconfigure(j, weight=1)
                btn = customtkinter.CTkButton(master=self.frame_board, text='', width=30, text_font = self.font,
                        command=lambda i=i, j=j:self.start_game(i,j), rcommand=lambda i=i, j=j:self.btn_mine(i,j))
                btn.grid(row=i, column=j, sticky='NSEW', padx=1, pady=1)
                buttons.append(btn)
            self.buttons.append(buttons)
        self.buttons_disabled = []


    def check_end(self):
        if self.current_mines == 0:
            for i in range(self.rows):
                for j in range(self.cols):
                    if (i,j) not in self.buttons_disabled:
                        return
            self.label_face.configure(image=self.img_cool)
            for buttons in self.buttons:
                for button in buttons:
                    button.configure(state='disabled')
            self.after_cancel(self.timer_id)
            self.game_start = False


    def btn_mine(self, x, y):
        if not self.buttons[x][y].image and self.current_mines > 0:
            self.buttons[x][y].configure(image=self.img)
            self.buttons_disabled.append((x,y))
            self.current_mines -= 1
            self.label_mines.configure(text=str(self.current_mines))
        elif self.buttons[x][y].image:
            self.buttons[x][y].configure(image=None)
            self.buttons_disabled.remove((x,y))
            self.current_mines += 1
            self.label_mines.configure(text=str(self.current_mines))
        self.check_end()


    def start_timer(self):
        self.timer += 1
        string = ''
        if len(str(self.timer)) == 2:
            string = '0'+str(self.timer)
        elif len(str(self.timer)) == 1:
            string = '00'+str(self.timer)
        else:
            string = str(self.timer)
        self.label_timer.configure(text=string)
        self.timer_id = self.after(1000, self.start_timer)


    def start_game(self, a, b):
        self.game_start = True
        self.timer_id = self.after(1000, self.start_timer)
        starting_point = (a,b)
        neighbors = [(a-1,b), (a-1,b+1), (a,b-1), (a+1,b-1), (a+1,b), (a+1,b+1), (a,b+1) ,(a-1,b-1)]
        board_coordinates = [(x, y) for x in range(self.rows) for y in range(self.cols) if (x,y) != starting_point and (x,y) not in neighbors]
        mine_coordinates = random.sample(board_coordinates, self.num_mines)
        for mine in mine_coordinates:
            x,y = mine 
            self.board[x][y] = 9
            neighbors = [(x-1,y),(x-1,y+1),(x,y-1),(x+1,y-1),(x+1,y),(x+1,y+1),(x,y+1),(x-1,y-1)]
            for n in neighbors:
                if 0 <= n[0] <= self.rows-1 and 0 <= n[1] <= self.cols-1 and n not in mine_coordinates:
                    self.board[n[0]][n[1]] += 1
        self.buttons[a][b].configure(fg_color=self.btn_bg, command=None, rcommand=None)
        self.buttons_disabled.append((a,b))
        self.check_neighbors(a,b)
        for i in range(self.rows):
            for j in range(self.cols):
                if (i,j) not in self.buttons_disabled:
                    self.buttons[i][j].configure(command=lambda i=i, j=j:self.uncover(i,j))


    def uncover(self, x, y):
        if self.board[x][y] == 9:
            self.game_start = False
            self.after_cancel(self.timer_id)
            self.label_face.configure(image=self.img_sad)
            self.buttons[x][y].configure(fg_color=self.btn_bg, image=self.img_bomb)
            for buttons in self.buttons:
                for button in buttons:
                    button.configure(state='disabled')
        elif self.board[x][y] == 0:
            self.buttons[x][y].configure(fg_color=self.btn_bg, command=None, rcommand=None)
            self.buttons_disabled.append((x,y))
            self.check_neighbors(x,y)
        else:
            self.buttons[x][y].configure(fg_color=self.btn_bg, text=str(self.board[x][y]), command=None, 
            rcommand=None, text_color=self.colors[self.board[x][y]])
            self.buttons_disabled.append((x,y))
        self.check_end()

    def check_neighbors(self, x, y):
        check = [(x,y)]
        check_previous = []
        while check != check_previous:
            check_previous = check.copy()
            for pair in check:
                x,y = pair
                neighbors = []
                if x-1 >= 0:
                    neighbors.append((x-1,y))
                if x-1 >= 0 and y+1 < self.cols:
                    neighbors.append((x-1,y+1))
                if y-1 >= 0:
                    neighbors.append((x,y-1))
                if x+1 < self.rows and y-1 >= 0:
                    neighbors.append((x+1,y-1))
                if x+1 < self.rows:
                    neighbors.append((x+1,y))
                if x+1 < self.rows and y+1 < self.cols:
                    neighbors.append((x+1,y+1))
                if y+1 < self.cols:
                    neighbors.append((x,y+1))
                if x-1 >= 0 and y-1 >= 0:
                    neighbors.append((x-1,y-1))
                for neighbor in neighbors:
                    a,b = neighbor
                    if self.board[a][b] == 0 and (a,b) not in check:
                        check.append((a,b))
                    elif self.board[a][b] != 0:
                        self.buttons[a][b].configure(fg_color=self.btn_bg, text=str(self.board[a][b]), command=None, 
                            rcommand=None, text_color=self.colors[self.board[a][b]])
                        self.buttons_disabled.append((a,b))
                self.buttons[x][y].configure(fg_color=self.btn_bg, command=None, rcommand=None)
                self.buttons_disabled.append((x,y))


    def change_difficulty(self, choice):
        if self.game_start:
            if messagebox.askyesno("Game in Progress", "A game is already in progress, are you sure you want to start a new game?"):
                self.difficulty_var.set(choice)
                self.build_board()
        else:
            self.difficulty_var.set(choice)
            self.build_board()


    def center(self, window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        size = tuple(int(_) for _ in window.geometry().split('+')[0].split('x'))
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        window.geometry("+%d+%d" % (x, y-50))



if __name__ == '__main__':
    minesweeper = Minesweeper()
    minesweeper.mainloop()
