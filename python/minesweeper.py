import random


MINE = '*'
HIDDEN = '?'


class Position():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Position(x={0}, y={1})'.format(self.x, self.y)


class MineSweeper():
    def __init__(self, board_size):
        self.board = []
        self.isExploded = False
        self.isWon = False
        self.numHidden = board_size * board_size
        self.numMines = max(self.numHidden // 10, 1)

        for i in range(board_size):
            self.board.append([HIDDEN] * board_size)

        for _ in range(self.numMines):
            i = random.randint(0, board_size - 1)
            j = random.randint(0, board_size - 1)

            self.board[i][j] = MINE

    def _iterate_box(self, position):
        board_size = len(self.board)
        for x in range(position.x - 1, position.x + 2):
            for y in range(position.y - 1, position.y + 2):
                if x >= 0 and x < board_size and \
                        y >= 0 and y < board_size and \
                        not (x == position.x and y == position.y):
                    yield x, y

    def _minesAround(self, position):
        mines = []
        for x, y in self._iterate_box(position):
                if self.board[x][y] == MINE:
                    mines.append(Position(x, y))
        return mines

    def _numMinesAround(self, position):
        num = 0
        for x, y in self._iterate_box(position):
            if self.board[x][y] == MINE:
                num += 1
        return num

    def doTurn(self, position):
        ret = False
        if self.board[position.x][position.y] == MINE:
            self.board[position.x][position.y] = 'X'
            self.isExploded = True
        else:
            ret = True
            to_process = [position]
            while len(to_process) > 0:
                current = to_process[0]
                around_current = self._numMinesAround(current)

                if around_current == 0 and \
                        self.board[current.x][current.y] == HIDDEN:
                    self.board[current.x][current.y] = ' '
                    self.numHidden -= 1

                    for x, y in self._iterate_box(current):
                            to_process.append(Position(x, y))

                elif self.board[current.x][current.y] == HIDDEN:
                    self.board[current.x][current.y] = str(around_current)
                    self.numHidden -= 1

                to_process = to_process[1:]

        if self.numHidden == self.numMines:
            self.isWon = True

        return ret

    def boardString(self):
        a = ord('A')
        board_size = len(self.board)

        s = '   ' + ' '.join([chr(a + i) for i in range(board_size)])
        for x in range(board_size):
            s += '\n{0:02} '.format(x)
            for y in range(board_size):
                if self.board[x][y] == MINE and not self.isWon:
                    s += '?'
                else:
                    s += self.board[x][y]
                s += ' '

        return s


if __name__ == '__main__':
    a = ord('A')
    m = MineSweeper(12)
    board_size = len(m.board)

    while not m.isExploded and not m.isWon:
        print(m.boardString())
        inp = input('Enter a position: ')

        err = False
        x = 0
        y = 0
        try:
            x = int(inp[1:])
            y = ord(inp[0].upper()) - a
        except ValueError:
            err = True

        if err or x < 0 or x >= board_size or y < 0 or y >= board_size:
            print('Invalid position. Try again.')
            continue

        if not m.doTurn(Position(x, y)):
            print(m.boardString())
            print('Sorry, you lose!')
            break

    if m.isWon:
        print(m.boardString())
        print('You win!')
