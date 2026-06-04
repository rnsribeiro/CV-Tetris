# Tetris por Gestos com Visao Computacional

Jogo de Tetris em Python controlado por gestos da mao capturados pela webcam.

## Tecnologias

- Python
- Pygame
- OpenCV
- MediaPipe

## Instalacao

Use Python 3.11 ou 3.12. O Python 3.14 ainda pode causar erro de instalacao porque algumas bibliotecas deste projeto podem nao ter pacotes pre-compilados para ele.

Verifique as versoes instaladas:

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

Se o comando `py -3.12` nao funcionar, instale o Python 3.12 pelo site oficial e repita os comandos acima.

Evite instalar com Python 3.14 neste projeto:

```powershell
python --version
```

Se aparecer `Python 3.14.x`, instale e selecione o Python 3.12 para o ambiente virtual.

Instalacao simples, depois que o ambiente virtual correto estiver ativo:

```bash
pip install -r requirements.txt
```

## Como executar

```bash
python main.py
```

## Controles por gesto

A imagem da webcam e espelhada para deixar o controle mais natural.

- Indicador na esquerda da imagem: move a peca para a esquerda
- Indicador na direita da imagem: move a peca para a direita
- Mao aberta: rotaciona a peca
- Gesto indefinido ou nenhuma mao detectada: nenhum comando

## Controles de teclado para teste

- Seta esquerda: mover para esquerda
- Seta direita: mover para direita
- Seta para cima: rotacionar
- Seta para baixo: descer
- Espaco: queda instantanea
- R: reiniciar apos fim de jogo

## Estrutura

- `main.py`: loop principal, desenho da interface e integracao entre jogo e gestos
- `tetris.py`: regras, pecas, colisao, pontuacao e fim de jogo
- `gesture_controller.py`: captura da webcam, deteccao da mao e interpretacao dos comandos
- `config.py`: dimensoes, cores, velocidade e intervalos dos comandos

## Observacoes

Use boa iluminacao e mantenha a mao visivel para melhorar a deteccao do MediaPipe. Caso a webcam nao esteja disponivel, o jogo ainda pode ser testado pelo teclado.

Na versao atual do MediaPipe para Python 3.12, o projeto usa a API `tasks`. Na primeira execucao, o arquivo `hand_landmarker.task` pode ser baixado automaticamente para a pasta do projeto. Ele e o modelo usado para detectar a mao.

O tabuleiro mostra uma previsao de queda da peca atual: as colunas ocupadas pela peca ficam levemente destacadas e a posicao final estimada aparece com um bloco translucido.
