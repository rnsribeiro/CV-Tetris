# Tamanho da janela principal do jogo.
SCREEN_WIDTH = 920
SCREEN_HEIGHT = 720
FPS = 60

# Medidas oficiais usadas no tabuleiro do Tetris.
BOARD_COLUMNS = 10
BOARD_ROWS = 20
BLOCK_SIZE = 32

# O tabuleiro fica separado em largura, altura e posicao para facilitar o desenho.
BOARD_WIDTH = BOARD_COLUMNS * BLOCK_SIZE
BOARD_HEIGHT = BOARD_ROWS * BLOCK_SIZE
BOARD_X = 48
BOARD_Y = 40

# Painel lateral usado para pontuacao, proxima peca e camera.
SIDE_PANEL_X = BOARD_X + BOARD_WIDTH + 48
SIDE_PANEL_Y = BOARD_Y
SIDE_PANEL_WIDTH = SCREEN_WIDTH - SIDE_PANEL_X - 48

# Tamanho em que a imagem da webcam aparece dentro da tela do jogo.
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240

# Tempo, em segundos, entre uma queda automatica e outra.
DROP_INTERVAL = 1.00

# Intervalo minimo entre comandos vindos da webcam.
# Esses valores deixam o controle menos sensivel e evitam comandos repetidos.
COMMAND_COOLDOWNS = {
    "LEFT": 0.22,
    "RIGHT": 0.22,
    "ROTATE": 0.85,
}

# Pequena trava entre qualquer comando, mesmo que o gesto detectado mude.
GLOBAL_COMMAND_COOLDOWN = 0.18

# Paleta de cores usada no jogo e nas pecas.
COLORS = {
    "background": (18, 20, 24),
    "panel": (32, 36, 42),
    "grid": (53, 59, 69),
    "text": (238, 241, 245),
    "muted": (158, 166, 178),
    "danger": (237, 93, 83),
    "board": (11, 13, 17),
    "I": (0, 184, 212),
    "O": (255, 202, 40),
    "T": (171, 71, 188),
    "S": (102, 187, 106),
    "Z": (239, 83, 80),
    "J": (92, 107, 192),
    "L": (255, 167, 38),
}
