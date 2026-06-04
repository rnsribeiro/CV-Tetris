# Explicação do projeto CV-Tetris

## Ideia geral

O CV-Tetris é um jogo de Tetris feito em Python. A diferença principal é que o jogador consegue controlar as peças usando a webcam, com ajuda de visão computacional.

A câmera captura a mão do jogador, o MediaPipe identifica os pontos da mão e o jogo transforma esses pontos em comandos. O Pygame fica responsável pela janela, pelo tabuleiro, pelas peças e por tudo que aparece na tela.

## Como o jogo funciona

O jogo roda em um loop principal dentro do arquivo `main.py`.

Em cada rodada desse loop, o programa faz basicamente isto:

1. Lê a imagem da webcam.
2. Detecta a mão com MediaPipe.
3. Interpreta o comando encontrado.
4. Move ou gira a peça no Tetris.
5. Atualiza a queda automática da peça.
6. Desenha novamente o tabuleiro, a peça, a câmera e a pontuação.

O Tetris em si fica separado no arquivo `tetris.py`. Isso deixa o projeto mais organizado, porque a regra do jogo não fica misturada com a câmera.

## Controles

### Pela webcam

- Indicador na esquerda da imagem: move a peça para a esquerda.
- Indicador na direita da imagem: move a peça para a direita.
- Mão aberta: rotaciona a peça.
- Centro da imagem ou gesto não reconhecido: nenhum comando.

A imagem da webcam é espelhada. Assim, quando a mão vai para a esquerda na tela, a peça também vai para a esquerda, ficando mais natural para jogar.

### Pelo teclado

Os controles de teclado foram mantidos para teste:

- Seta esquerda: move para esquerda.
- Seta direita: move para direita.
- Seta para cima: rotaciona.
- Seta para baixo: desce uma linha.
- Espaço: queda instantânea.
- R: reinicia depois do fim de jogo.

## Arquivos do projeto

### `main.py`

É o arquivo principal. Ele abre a janela do Pygame, inicia o Tetris, inicia o controlador de gestos e mantém o loop do jogo rodando.

Também desenha:

- tabuleiro;
- blocos já fixados;
- peça atual;
- previsão de onde a peça vai cair;
- próxima peça;
- pontuação;
- imagem da webcam.

### `tetris.py`

Contém as regras do Tetris.

Nesse arquivo ficam:

- criação das peças;
- matriz do tabuleiro;
- movimento para esquerda, direita e baixo;
- rotação;
- colisão com parede, fundo e outras peças;
- fixação da peça quando ela chega ao fim;
- remoção de linhas completas;
- pontuação;
- fim de jogo.

### `gesture_controller.py`

Cuida da parte de visão computacional.

Ele abre a webcam, detecta a mão, identifica a ponta do indicador e decide qual comando mandar para o jogo.

O arquivo também tem um intervalo mínimo entre comandos. Isso evita que a câmera leia muitos frames seguidos e acabe girando ou movendo a peça rápido demais.

### `config.py`

Guarda as configurações principais:

- tamanho da tela;
- tamanho do tabuleiro;
- tamanho dos blocos;
- velocidade de queda;
- tempo entre comandos;
- cores usadas no jogo.

### `requirements.txt`

Lista as bibliotecas que precisam ser instaladas:

- `pygame`;
- `opencv-python`;
- `mediapipe`.

## Previsão de queda

O tabuleiro mostra uma ajuda visual para a peça atual.

As colunas ocupadas pela peça ficam levemente marcadas e a posição final provável aparece como uma peça translúcida. Isso ajuda a jogar melhor, principalmente usando a webcam, porque o controle por gesto não tem a mesma precisão de um teclado.

## Instalação

O projeto foi pensado para rodar com Python 3.12.

Na pasta do projeto, crie o ambiente virtual:

```powershell
py -3.12 -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
pip install -r requirements.txt
```

Execute o jogo:

```powershell
python main.py
```

## Observações importantes

Para a webcam funcionar melhor, é bom jogar em um local bem iluminado. A mão precisa aparecer inteira na câmera, principalmente a ponta do dedo indicador.

Na primeira execução, o projeto pode baixar o arquivo `hand_landmarker.task`. Esse arquivo é o modelo usado pelo MediaPipe para detectar a mão.

Se a webcam não abrir, ainda dá para testar toda a lógica do Tetris pelo teclado.

## Possíveis melhorias

Algumas melhorias que podem ser feitas depois:

- tela inicial;
- tela de pausa;
- sons;
- ranking de pontuação;
- aumento de dificuldade mais elaborado;
- modo educativo com perguntas;
- ajustes finos nos gestos;
- escolha da câmera quando houver mais de uma.
