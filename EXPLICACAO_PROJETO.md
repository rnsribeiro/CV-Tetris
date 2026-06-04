# Explicacao do projeto CV-Tetris

## Ideia geral

O CV-Tetris e um jogo de Tetris feito em Python. A diferenca principal e que o jogador consegue controlar as pecas usando a webcam, com ajuda de visao computacional.

A camera captura a mao do jogador, o MediaPipe identifica os pontos da mao e o jogo transforma esses pontos em comandos. O Pygame fica responsavel pela janela, pelo tabuleiro, pelas pecas e por tudo que aparece na tela.

## Como o jogo funciona

O jogo roda em um loop principal dentro do arquivo `main.py`.

Em cada rodada desse loop, o programa faz basicamente isto:

1. Le a imagem da webcam.
2. Detecta a mao com MediaPipe.
3. Interpreta o comando encontrado.
4. Move ou gira a peca no Tetris.
5. Atualiza a queda automatica da peca.
6. Desenha novamente o tabuleiro, a peca, a camera e a pontuacao.

O Tetris em si fica separado no arquivo `tetris.py`. Isso deixa o projeto mais organizado, porque a regra do jogo nao fica misturada com a camera.

## Controles

### Pela webcam

- Indicador na esquerda da imagem: move a peca para a esquerda.
- Indicador na direita da imagem: move a peca para a direita.
- Mao aberta: rotaciona a peca.
- Centro da imagem ou gesto nao reconhecido: nenhum comando.

A imagem da webcam e espelhada. Assim, quando a mao vai para a esquerda na tela, a peca tambem vai para a esquerda, ficando mais natural para jogar.

### Pelo teclado

Os controles de teclado foram mantidos para teste:

- Seta esquerda: move para esquerda.
- Seta direita: move para direita.
- Seta para cima: rotaciona.
- Seta para baixo: desce uma linha.
- Espaco: queda instantanea.
- R: reinicia depois do fim de jogo.

## Arquivos do projeto

### `main.py`

E o arquivo principal. Ele abre a janela do Pygame, inicia o Tetris, inicia o controlador de gestos e mantem o loop do jogo rodando.

Tambem desenha:

- tabuleiro;
- blocos ja fixados;
- peca atual;
- previsao de onde a peca vai cair;
- proxima peca;
- pontuacao;
- imagem da webcam.

### `tetris.py`

Contem as regras do Tetris.

Nesse arquivo ficam:

- criacao das pecas;
- matriz do tabuleiro;
- movimento para esquerda, direita e baixo;
- rotacao;
- colisao com parede, fundo e outras pecas;
- fixacao da peca quando ela chega ao fim;
- remocao de linhas completas;
- pontuacao;
- fim de jogo.

### `gesture_controller.py`

Cuida da parte de visao computacional.

Ele abre a webcam, detecta a mao, identifica a ponta do indicador e decide qual comando mandar para o jogo.

O arquivo tambem tem um intervalo minimo entre comandos. Isso evita que a camera leia muitos frames seguidos e acabe girando ou movendo a peca rapido demais.

### `config.py`

Guarda as configuracoes principais:

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

## Previsao de queda

O tabuleiro mostra uma ajuda visual para a peca atual.

As colunas ocupadas pela peca ficam levemente marcadas e a posicao final provavel aparece como uma peca translucida. Isso ajuda a jogar melhor, principalmente usando a webcam, porque o controle por gesto nao tem a mesma precisao de um teclado.

## Instalacao

O projeto foi pensado para rodar com Python 3.12.

Na pasta do projeto, crie o ambiente virtual:

```powershell
py -3.12 -m venv .venv
```

Ative o ambiente:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Execute o jogo:

```powershell
python main.py
```

## Observacoes importantes

Para a webcam funcionar melhor, e bom jogar em um local bem iluminado. A mao precisa aparecer inteira na camera, principalmente a ponta do dedo indicador.

Na primeira execucao, o projeto pode baixar o arquivo `hand_landmarker.task`. Esse arquivo e o modelo usado pelo MediaPipe para detectar a mao.

Se a webcam nao abrir, ainda da para testar toda a logica do Tetris pelo teclado.

## Possiveis melhorias

Algumas melhorias que podem ser feitas depois:

- tela inicial;
- tela de pausa;
- sons;
- ranking de pontuacao;
- aumento de dificuldade mais elaborado;
- modo educativo com perguntas;
- ajustes finos nos gestos;
- escolha da camera quando houver mais de uma.
