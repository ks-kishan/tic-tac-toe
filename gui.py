import tic_tac_toe_engine as te
import customtkinter as ctk

WHITE = '#FFF'
BLUE = "#398ac7"
HOVER_COLOR = "#aaaaaa"
RED = "#bf3e3e"
RESET_COLOR = '#ff6767'

class Game(ctk.CTk):
  def __init__(self):
    super().__init__()
    self.geometry('300x400')
    self.title('tic-tac-toe')
    self.engine = te.TicTacToe()
    self.output_string = ctk.StringVar(value=self.engine.get_current_player())

    self.game_over = False

    self.rowconfigure((0,1,2,3), weight=1)
    self.columnconfigure((0,1,2), weight=1)

    self.cells = [[Cell(self, row, col, self.on_click) for col in range(3)] for row in range(3)]
    self.output_cell = ctk.CTkLabel(
      self,
      fg_color='white',
      text_color='black',
      textvariable=self.output_string
      )
    self.output_cell.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=1, pady=1)

    self.reset_button = ctk.CTkButton(
      self,
      fg_color=RESET_COLOR,
      text_color='white',
      text='Reset game',
      command=self.reset_game,
      corner_radius=0
    )
    self.reset_button.grid(row=3, column=2, sticky='nsew', padx=1, pady=1)

    self.mainloop()

  def on_click(self, row, col):

    if not self.game_over:
      move = (row, col)
      if not self.engine.make_move(move):
        self.output_string.set('invalid move, go again')
        self.output_cell.configure(fg_color=RESET_COLOR)
        self.output_cell.configure(text_color='white')
        self.after(700, lambda: self.reset_status())
        return
      
      self.update_gui()
      
      if self.engine.check_win():
        self.output_string.set(f'{self.engine.get_current_player()} wins!')
        self.game_over = True
        self.disable_all_cells()
        return
      
      if self.engine.is_draw():
        self.output_string.set('draw!')
        self.game_over = True
        return

      self.engine.switch_player()
      self.output_string.set(self.engine.get_current_player())
    else: # not reachable due to cells not clickable (state='disabled')
      self.output_string.set('click reset button')

  def reset_game(self):
    self.game_over = False
    self.engine.reset_engine()
    self.update_gui()
    self.enable_all_cells()
    self.output_string.set(self.engine.get_current_player())


  def update_gui(self):
    board = self.engine.get_board()
    for r in range(3):
      for c in range(3):
        value = board[r][c]

        if value == 'O':
          color = BLUE   # blue
        elif value == 'X':
          color = RED  # red
        else:
          color = WHITE

        self.cells[r][c].configure(
          text=value,
          fg_color=color
        )

  def reset_status(self):
    self.output_string.set(self.engine.get_current_player())
    self.output_cell.configure(fg_color='white', text_color='black')

  def disable_all_cells(self):
    for row in self.cells:
      for cell in row:
        cell.configure(state="disabled")

  def enable_all_cells(self):
    for row in self.cells:
      for cell in row:
        cell.configure(state="normal")
        

class Cell(ctk.CTkButton):
  def __init__(self, parent, row, col, func):
    super().__init__(
      master=parent,
      fg_color=WHITE,
      text=' ',
      text_color=WHITE,
      corner_radius=0,
      border_width=0,
      hover_color=HOVER_COLOR,
      command=lambda: func(row, col)
    )
    self.grid(row=row, column=col, sticky='nsew', padx=1, pady=1)

Game()