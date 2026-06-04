import sys
import time

import cv2
import pygame

from config import (
    BLOCK_SIZE,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    BOARD_X,
    BOARD_Y,
    CAMERA_HEIGHT,
    CAMERA_WIDTH,
    COLORS,
    DROP_INTERVAL,
    FPS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SIDE_PANEL_WIDTH,
    SIDE_PANEL_X,
    SIDE_PANEL_Y,
)
from gesture_controller import GestureController
from tetris import TetrisGame


class App:
    """Janela do jogo, entrada do usuário e desenho da interface."""

    def __init__(self):
        # Inicializa o Pygame e cria a janela principal.
        pygame.init()
        pygame.display.set_caption("Tetris por Gestos")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Fontes usadas no painel lateral e nas mensagens do jogo.
        self.font = pygame.font.SysFont("Segoe UI", 24)
        self.large_font = pygame.font.SysFont("Segoe UI", 42, bold=True)
        self.small_font = pygame.font.SysFont("Segoe UI", 18)

        # A lógica do Tetris e o controle por gestos ficam em classes separadas.
        self.game = TetrisGame()
        self.gestures = GestureController()
        self.last_drop_at = time.monotonic()
        self.last_camera_frame = None

    def run(self):
        # Loop principal: lê entrada, atualiza o jogo e redesenha a tela.
        running = True
        while running:
            now = time.monotonic()
            command, frame = self.gestures.get_command()
            if frame is not None:
                self.last_camera_frame = frame

            # Eventos do Pygame incluem fechar janela e comandos de teclado.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self._handle_key(event.key)

            self._apply_gesture_command(command)

            # A queda automática fica mais rápida conforme o nível aumenta.
            interval = max(0.15, DROP_INTERVAL - (self.game.level - 1) * 0.04)
            if now - self.last_drop_at >= interval:
                self.game.update()
                self.last_drop_at = now

            self._draw(command)
            pygame.display.flip()
            self.clock.tick(FPS)

        self.gestures.release()
        pygame.quit()
        sys.exit()

    def _handle_key(self, key):
        # O teclado fica como alternativa para teste e apresentação.
        if key == pygame.K_LEFT:
            self.game.move_left()
        elif key == pygame.K_RIGHT:
            self.game.move_right()
        elif key == pygame.K_UP:
            self.game.rotate_piece()
        elif key == pygame.K_DOWN:
            self.game.move_down()
        elif key == pygame.K_SPACE:
            self.game.hard_drop()
        elif key == pygame.K_r and self.game.game_over:
            self.game.reset()

    def _apply_gesture_command(self, command):
        # Traduz os comandos vindos da webcam para a lógica do Tetris.
        if command == "LEFT":
            self.game.move_left()
        elif command == "RIGHT":
            self.game.move_right()
        elif command == "ROTATE":
            self.game.rotate_piece()

    def _draw(self, command):
        # Ordem do desenho: fundo, tabuleiro, previsão, peça e painel.
        self.screen.fill(COLORS["background"])
        self._draw_board()
        self._draw_drop_preview()
        self._draw_piece(self.game.current_piece)
        self._draw_side_panel(command)

        if self.game.game_over:
            self._draw_game_over()

    def _draw_board(self):
        # Desenha o tabuleiro, os blocos fixados e a grade.
        board_rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.screen, COLORS["board"], board_rect)
        pygame.draw.rect(self.screen, COLORS["grid"], board_rect, 2)

        for row_index, row in enumerate(self.game.board):
            for col_index, kind in enumerate(row):
                if kind:
                    self._draw_block(BOARD_X + col_index * BLOCK_SIZE, BOARD_Y + row_index * BLOCK_SIZE, COLORS[kind])

        for col in range(1, 10):
            x = BOARD_X + col * BLOCK_SIZE
            pygame.draw.line(self.screen, COLORS["grid"], (x, BOARD_Y), (x, BOARD_Y + BOARD_HEIGHT), 1)
        for row in range(1, 20):
            y = BOARD_Y + row * BLOCK_SIZE
            pygame.draw.line(self.screen, COLORS["grid"], (BOARD_X, y), (BOARD_X + BOARD_WIDTH, y), 1)

    def _draw_piece(self, piece):
        # Desenha a peça que está caindo no momento.
        for x, y in piece.cells:
            if y >= 0:
                self._draw_block(BOARD_X + x * BLOCK_SIZE, BOARD_Y + y * BLOCK_SIZE, COLORS[piece.kind])

    def _draw_drop_preview(self):
        # Mostra as colunas da peça e a posição provável onde ela vai parar.
        if self.game.game_over:
            return

        overlay = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)

        for col in self.game.current_piece_columns():
            column_rect = pygame.Rect(col * BLOCK_SIZE, 0, BLOCK_SIZE, BOARD_HEIGHT)
            pygame.draw.rect(overlay, (255, 255, 255, 20), column_rect)

        piece_color = COLORS[self.game.current_piece.kind]
        ghost_fill = (*piece_color, 72)
        ghost_outline = (*piece_color, 190)
        for x, y in self.game.landing_cells():
            if y < 0:
                continue
            rect = pygame.Rect(x * BLOCK_SIZE + 3, y * BLOCK_SIZE + 3, BLOCK_SIZE - 6, BLOCK_SIZE - 6)
            pygame.draw.rect(overlay, ghost_fill, rect, border_radius=3)
            pygame.draw.rect(overlay, ghost_outline, rect, 2, border_radius=3)

        self.screen.blit(overlay, (BOARD_X, BOARD_Y))

    def _draw_block(self, x, y, color):
        # Desenha um bloco individual com uma borda simples.
        rect = pygame.Rect(x + 1, y + 1, BLOCK_SIZE - 2, BLOCK_SIZE - 2)
        pygame.draw.rect(self.screen, color, rect, border_radius=3)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1, border_radius=3)

    def _draw_side_panel(self, command):
        # Painel com pontuação, próxima peça, comando detectado e webcam.
        panel_rect = pygame.Rect(SIDE_PANEL_X, SIDE_PANEL_Y, SIDE_PANEL_WIDTH, BOARD_HEIGHT)
        pygame.draw.rect(self.screen, COLORS["panel"], panel_rect, border_radius=8)

        self._draw_text("Tetris por Gestos", SIDE_PANEL_X + 20, SIDE_PANEL_Y + 20, self.large_font)
        self._draw_text(f"Pontuação: {self.game.score}", SIDE_PANEL_X + 20, SIDE_PANEL_Y + 86)
        self._draw_text(f"Linhas: {self.game.lines}", SIDE_PANEL_X + 20, SIDE_PANEL_Y + 118)
        self._draw_text(f"Nível: {self.game.level}", SIDE_PANEL_X + 20, SIDE_PANEL_Y + 150)
        self._draw_text(f"Comando: {command}", SIDE_PANEL_X + 20, SIDE_PANEL_Y + 190)

        self._draw_text("Próxima peça", SIDE_PANEL_X + 20, SIDE_PANEL_Y + 238)
        self._draw_next_piece(SIDE_PANEL_X + 28, SIDE_PANEL_Y + 274)

        self._draw_camera(SIDE_PANEL_X + 20, SIDE_PANEL_Y + 390)
        self._draw_text("Teclado: setas, espaço, R", SIDE_PANEL_X + 20, SIDE_PANEL_Y + 650, self.small_font, COLORS["muted"])

    def _draw_next_piece(self, origin_x, origin_y):
        # Miniatura da próxima peça.
        shape = self.game.next_piece.shape
        color = COLORS[self.game.next_piece.kind]
        preview_size = 24
        for row_index, row in enumerate(shape):
            for col_index, value in enumerate(row):
                if value:
                    rect = pygame.Rect(origin_x + col_index * preview_size, origin_y + row_index * preview_size, preview_size - 2, preview_size - 2)
                    pygame.draw.rect(self.screen, color, rect, border_radius=3)

    def _draw_camera(self, x, y):
        # Converte o frame do OpenCV para uma imagem que o Pygame consegue mostrar.
        camera_rect = pygame.Rect(x, y, CAMERA_WIDTH, CAMERA_HEIGHT)
        pygame.draw.rect(self.screen, COLORS["board"], camera_rect)

        if self.last_camera_frame is None:
            self._draw_text("Câmera indisponível", x + 24, y + 104, self.font, COLORS["muted"])
            return

        frame = cv2.resize(self.last_camera_frame, (CAMERA_WIDTH, CAMERA_HEIGHT))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        surface = pygame.image.frombuffer(frame.tobytes(), (CAMERA_WIDTH, CAMERA_HEIGHT), "RGB")
        self.screen.blit(surface, camera_rect)
        pygame.draw.rect(self.screen, COLORS["grid"], camera_rect, 2)

    def _draw_game_over(self):
        # Mensagem final com fundo escurecido sobre o tabuleiro.
        overlay = pygame.Surface((BOARD_WIDTH, BOARD_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (BOARD_X, BOARD_Y))
        self._draw_text("Fim de jogo", BOARD_X + 72, BOARD_Y + 270, self.large_font, COLORS["danger"])
        self._draw_text("Pressione R para reiniciar", BOARD_X + 58, BOARD_Y + 326, self.font)

    def _draw_text(self, text, x, y, font=None, color=None):
        # Atalho para renderizar texto sem repetir o mesmo código em todo lugar.
        rendered = (font or self.font).render(text, True, color or COLORS["text"])
        self.screen.blit(rendered, (x, y))


if __name__ == "__main__":
    # Ponto de entrada quando o arquivo é executado pelo terminal.
    App().run()
