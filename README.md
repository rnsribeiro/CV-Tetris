# Tetris por Gestos com Visão Computacional

Jogo de Tetris em Python controlado por gestos da mão capturados pela webcam.

## Tecnologias

- Python
- Pygame
- OpenCV
- MediaPipe

## Instalação

Use Python 3.11 ou 3.12. O Python 3.14 ainda pode causar erro de instalação porque algumas bibliotecas deste projeto podem não ter pacotes pré-compilados para ele.

Verifique as versões instaladas:

```powershell
py -0p
```

Crie e ative um ambiente virtual com Python 3.12, se ele estiver instalado:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

Se o comando `py -3.12` não funcionar, instale o Python 3.12 pelo site oficial e repita os comandos acima.

Evite instalar com Python 3.14 neste projeto:

```powershell
python --version
```

Se aparecer `Python 3.14.x`, instale e selecione o Python 3.12 para o ambiente virtual.

Instalação simples, depois que o ambiente virtual correto estiver ativo:

```bash
pip install -r requirements.txt
```

## Como executar

```bash
python main.py
```

## Controles por gesto

A imagem da webcam é espelhada para deixar o controle mais natural.

- Indicador na esquerda da imagem: move a peça para a esquerda
- Indicador na direita da imagem: move a peça para a direita
- Mão aberta: rotaciona a peça
- Gesto indefinido ou nenhuma mão detectada: nenhum comando

## Controles de teclado para teste

- Seta esquerda: mover para esquerda
- Seta direita: mover para direita
- Seta para cima: rotacionar
- Seta para baixo: descer
- Espaço: queda instantânea
- R: reiniciar após fim de jogo

## Estrutura

- `main.py`: loop principal, desenho da interface e integração entre jogo e gestos
- `tetris.py`: regras, peças, colisão, pontuação e fim de jogo
- `gesture_controller.py`: captura da webcam, detecção da mão e interpretação dos comandos
- `config.py`: dimensões, cores, velocidade e intervalos dos comandos

## Observações

Use boa iluminação e mantenha a mão visível para melhorar a detecção do MediaPipe. Caso a webcam não esteja disponível, o jogo ainda pode ser testado pelo teclado.

Na versão atual do MediaPipe para Python 3.12, o projeto usa a API `tasks`. Na primeira execução, o arquivo `hand_landmarker.task` pode ser baixado automaticamente para a pasta do projeto. Ele é o modelo usado para detectar a mão.

O tabuleiro mostra uma previsão de queda da peça atual: as colunas ocupadas pela peça ficam levemente destacadas e a posição final estimada aparece com um bloco translúcido.
