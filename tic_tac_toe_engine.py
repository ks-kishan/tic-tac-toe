class TicTacToe:
  def __init__(self):
    self.board = [[' '] * 3 for _ in range(3)]
    self.current_player = 'O'
    self.count = 0

    # 3 rows + 3 cols + 2 diagonals
    self.player_counts = {
        'O': [0] * 8,
        'X': [0] * 8
    }

  def is_valid_move(self, move):
    r, c = move
    return (
        0 <= r < 3 and
        0 <= c < 3 and
        self.board[r][c] == ' '
    )

  def make_move(self, move):
    if not self.is_valid_move(move):
        return False

    r, c = move
    p = self.current_player

    self.board[r][c] = p

    counts = self.player_counts[p]
    counts[r] += 1
    counts[3 + c] += 1

    if r == c:
        counts[6] += 1
    if r + c == 2:
        counts[7] += 1

    self.count += 1
    return True

  def check_win(self):
    counts = self.player_counts[self.current_player]
    return any(x == 3 for x in counts)

  def is_draw(self):
    return self.count == 9

  def switch_player(self):
    self.current_player = 'X' if self.current_player == 'O' else 'O'

  def get_board(self):
    return self.board

  def get_current_player(self):
    return self.current_player
  
  def reset_engine(self):
    self.board = [[' '] * 3 for _ in range(3)]
    self.current_player = 'O'
    self.count = 0

    self.player_counts = {
        'O': [0] * 8,
        'X': [0] * 8
    }


if __name__ == '__main__':
  game = TicTacToe()

  while True:
    # display
    for row in game.get_board():
      print('|'.join(row))
      print('-'*5)

    # input
    row, col = map(int, input("Enter move (row col): ").split())
    move = (row - 1, col - 1)

    if not game.make_move(move):
      print("Invalid move")
      continue

    if game.check_win():
      print(f"{game.get_current_player()} wins!")
      break

    if game.is_draw():
      print("Draw!")
      break

    game.switch_player()