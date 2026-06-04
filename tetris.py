import random
from copy import deepcopy

from config import BOARD_COLUMNS, BOARD_ROWS


# Matrizes das peças clássicas do Tetris.
# O número 1 representa um bloco ocupado e o 0 representa espaço vazio.
SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}


class Piece:
    """Guarda o tipo, formato e posição de uma peça em movimento."""

    def __init__(self, kind):
        self.kind = kind
        self.shape = deepcopy(SHAPES[kind])
        # A peça nasce centralizada no topo do tabuleiro.
        self.x = BOARD_COLUMNS // 2 - len(self.shape[0]) // 2
        self.y = 0

    @property
    def cells(self):
        # Devolve as coordenadas reais ocupadas pela peça no tabuleiro.
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value:
                    yield self.x + col_index, self.y + row_index

    def rotated_shape(self):
        # Rotação simples em sentido horário usando transposição da matriz.
        return [list(row) for row in zip(*self.shape[::-1])]


class TetrisGame:
    """Concentra as regras do Tetris, sem depender do Pygame ou da webcam."""

    def __init__(self):
        self.reset()

    def reset(self):
        # O tabuleiro guarda None em espaços vazios e a letra da peça em blocos fixos.
        self.board = [[None for _ in range(BOARD_COLUMNS)] for _ in range(BOARD_ROWS)]
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.current_piece = self._new_piece()
        self.next_piece = self._new_piece()

    def _new_piece(self):
        # Cada nova peça é escolhida aleatoriamente entre os sete formatos.
        return Piece(random.choice(list(SHAPES)))

    def _collides(self, piece, shape=None, x=None, y=None):
        # Verifica se uma peça encosta nas paredes, no fundo ou em blocos já fixados.
        shape = shape or piece.shape
        x = piece.x if x is None else x
        y = piece.y if y is None else y

        for row_index, row in enumerate(shape):
            for col_index, value in enumerate(row):
                if not value:
                    continue

                board_x = x + col_index
                board_y = y + row_index

                if board_x < 0 or board_x >= BOARD_COLUMNS or board_y >= BOARD_ROWS:
                    return True
                if board_y >= 0 and self.board[board_y][board_x] is not None:
                    return True

        return False

    def move(self, dx, dy):
        # Tenta mover a peça. Se ela não puder descer, fixa no tabuleiro.
        if self.game_over:
            return False

        new_x = self.current_piece.x + dx
        new_y = self.current_piece.y + dy
        if not self._collides(self.current_piece, x=new_x, y=new_y):
            self.current_piece.x = new_x
            self.current_piece.y = new_y
            return True

        if dy > 0:
            self._lock_piece()
        return False

    def move_left(self):
        # Atalho usado pelo teclado e pelo controle por gesto.
        return self.move(-1, 0)

    def move_right(self):
        # Atalho usado pelo teclado e pelo controle por gesto.
        return self.move(1, 0)

    def move_down(self):
        # Movimento de queda de uma linha.
        return self.move(0, 1)

    def rotate_piece(self):
        # A peça O não muda de formato ao girar, então não precisa rotacionar.
        if self.game_over or self.current_piece.kind == "O":
            return False

        rotated = self.current_piece.rotated_shape()
        # Pequenos ajustes laterais permitem girar perto da parede.
        kick_offsets = (0, -1, 1, -2, 2)
        for offset in kick_offsets:
            new_x = self.current_piece.x + offset
            if not self._collides(self.current_piece, shape=rotated, x=new_x):
                self.current_piece.shape = rotated
                self.current_piece.x = new_x
                return True
        return False

    def hard_drop(self):
        # Queda instantânea usada apenas no teclado para teste.
        if self.game_over:
            return
        while self.move_down():
            self.score += 1

    def landing_cells(self):
        # Calcula onde a peça pararia se caísse direto na posição atual.
        if self.game_over:
            return []

        landing_y = self.current_piece.y
        while not self._collides(self.current_piece, y=landing_y + 1):
            landing_y += 1

        cells = []
        for row_index, row in enumerate(self.current_piece.shape):
            for col_index, value in enumerate(row):
                if value:
                    cells.append((self.current_piece.x + col_index, landing_y + row_index))
        return cells

    def current_piece_columns(self):
        # Colunas ocupadas pela peça atual, usadas no destaque visual do tabuleiro.
        if self.game_over:
            return []
        return sorted({x for x, y in self.current_piece.cells if 0 <= x < BOARD_COLUMNS and y >= 0})

    def _lock_piece(self):
        # Transfere os blocos da peça atual para o tabuleiro fixo.
        for x, y in self.current_piece.cells:
            if y < 0:
                self.game_over = True
                return
            self.board[y][x] = self.current_piece.kind

        cleared = self._clear_lines()
        if cleared:
            # Pontuação no estilo clássico: limpar mais linhas de uma vez vale mais.
            self.lines += cleared
            self.score += {1: 100, 2: 300, 3: 500, 4: 800}[cleared] * self.level
            self.level = 1 + self.lines // 10

        # Depois de fixar, a próxima peça entra em jogo.
        self.current_piece = self.next_piece
        self.next_piece = self._new_piece()
        if self._collides(self.current_piece):
            self.game_over = True

    def _clear_lines(self):
        # Mantém apenas linhas incompletas e coloca linhas vazias no topo.
        remaining_rows = [row for row in self.board if any(cell is None for cell in row)]
        cleared = BOARD_ROWS - len(remaining_rows)
        new_rows = [[None for _ in range(BOARD_COLUMNS)] for _ in range(cleared)]
        self.board = new_rows + remaining_rows
        return cleared

    def update(self):
        # Atualização chamada pelo loop principal para a queda automática.
        if not self.game_over:
            self.move_down()
