import time
import urllib.request
from pathlib import Path

import cv2
import mediapipe as mp

from config import COMMAND_COOLDOWNS, GLOBAL_COMMAND_COOLDOWN


# Modelo oficial do MediaPipe usado pela API nova de deteccao de maos.
MODEL_URL = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")


# Pontos dos dedos usados para descobrir se a mao esta aberta.
FINGER_TIPS = (8, 12, 16, 20)
FINGER_PIPS = (6, 10, 14, 18)


def dedos_estendidos(landmarks):
    # Um dedo e considerado estendido quando a ponta fica acima da articulacao.
    return [
        tip
        for tip, pip in zip(FINGER_TIPS, FINGER_PIPS)
        if landmarks[tip].y < landmarks[pip].y - 0.025
    ]


def interpretar_gesto(landmarks):
    # Mao aberta foi escolhida para rotacionar porque e um gesto facil de manter.
    extended = dedos_estendidos(landmarks)
    extended_count = len(extended)

    if extended_count >= 4:
        return "ROTATE"

    return "NONE"


def interpretar_movimento_horizontal(x, largura):
    # O movimento lateral continua usando a posicao do indicador na imagem.
    # Ficou mais confiavel do que tentar interpretar a direcao do dedo.
    if x < largura * 0.35:
        return "LEFT"
    if x > largura * 0.65:
        return "RIGHT"
    return "NONE"


class GestureController:
    """Cuida da webcam, da deteccao da mao e da conversao para comandos."""

    def __init__(self, camera_index=0):
        # Abre a camera padrao do computador.
        self.camera = cv2.VideoCapture(camera_index)
        self.mode = None
        self.hands = None
        self.landmarker = None
        self.drawer = None
        # Guarda o ultimo momento em que cada comando foi aceito.
        self.last_command_at = {command: 0 for command in COMMAND_COOLDOWNS}
        self.last_any_command_at = 0
        self.current_command = "NONE"
        self.hand_detected = False
        self._initialize_detector()

    def _initialize_detector(self):
        # Algumas versoes antigas do MediaPipe possuem a API solutions.
        if hasattr(mp, "solutions"):
            self.mode = "solutions"
            self.hands = mp.solutions.hands.Hands(
                max_num_hands=1,
                min_detection_confidence=0.65,
                min_tracking_confidence=0.55,
            )
            self.drawer = mp.solutions.drawing_utils
            return

        # Nas versoes novas, a deteccao de maos fica na API tasks.
        self.mode = "tasks"
        self._ensure_task_model()
        from mediapipe.tasks import python
        from mediapipe.tasks.python import vision

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=str(MODEL_PATH)),
            num_hands=1,
            min_hand_detection_confidence=0.65,
            min_hand_presence_confidence=0.55,
            min_tracking_confidence=0.55,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def _ensure_task_model(self):
        # O modelo fica salvo na pasta do projeto para nao baixar toda vez.
        if MODEL_PATH.exists():
            return
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)

    def get_command(self):
        # Captura um frame da webcam e devolve o comando detectado.
        ok, frame = self.camera.read()
        if not ok:
            self.current_command = "NONE"
            return "NONE", None

        # Espelha a imagem para o jogador sentir o controle de forma natural.
        frame = cv2.flip(frame, 1)
        height, width = frame.shape[:2]
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        command = "NONE"
        self.hand_detected = False

        if self.mode == "solutions":
            command = self._detect_with_solutions(frame, rgb_frame, width, height)
        elif self.mode == "tasks":
            command = self._detect_with_tasks(frame, rgb_frame, width, height)

        self.current_command = self._apply_cooldown(command)
        self._draw_debug_overlay(frame, self.current_command)
        return self.current_command, frame

    def _detect_with_solutions(self, frame, rgb_frame, width, height):
        # Caminho usado quando o MediaPipe antigo esta instalado.
        result = self.hands.process(rgb_frame)
        if result.multi_hand_landmarks:
            self.hand_detected = True
            hand_landmarks = result.multi_hand_landmarks[0]
            index_tip = hand_landmarks.landmark[8]
            x = int(index_tip.x * width)
            y = int(index_tip.y * height)
            command = interpretar_gesto(hand_landmarks.landmark)
            if command == "NONE":
                command = interpretar_movimento_horizontal(x, width)

            self.drawer.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)
            cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)
            return command

        return "NONE"

    def _detect_with_tasks(self, frame, rgb_frame, width, height):
        # Caminho usado pela versao atual do MediaPipe.
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self.landmarker.detect(mp_image)
        if not result.hand_landmarks:
            return "NONE"

        self.hand_detected = True
        landmarks = result.hand_landmarks[0]
        index_tip = landmarks[8]
        x = int(index_tip.x * width)
        y = int(index_tip.y * height)

        for landmark in landmarks:
            point = (int(landmark.x * width), int(landmark.y * height))
            cv2.circle(frame, point, 3, (80, 220, 255), -1)
        cv2.circle(frame, (x, y), 10, (0, 255, 255), -1)

        command = interpretar_gesto(landmarks)
        if command == "NONE":
            command = interpretar_movimento_horizontal(x, width)
        return command

    def _apply_cooldown(self, command):
        # Evita que a camera repita o mesmo comando muitas vezes por segundo.
        if command == "NONE":
            return "NONE"

        now = time.monotonic()
        if now - self.last_any_command_at < GLOBAL_COMMAND_COOLDOWN:
            return "NONE"

        cooldown = COMMAND_COOLDOWNS.get(command, 0.25)
        if now - self.last_command_at.get(command, 0) >= cooldown:
            self.last_command_at[command] = now
            self.last_any_command_at = now
            return command

        return "NONE"

    def _draw_debug_overlay(self, frame, command):
        # Textos mostrados por cima da camera para facilitar os testes.
        cv2.putText(frame, f"Comando: {command}", (12, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "Indicador nas laterais: mover", (12, 56), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 230, 230), 1)
        cv2.putText(frame, "Mao aberta: girar", (12, 78), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (230, 230, 230), 1)

    def release(self):
        # Fecha camera e detector ao encerrar o jogo.
        self.camera.release()
        if self.hands is not None:
            self.hands.close()
        if self.landmarker is not None:
            self.landmarker.close()
