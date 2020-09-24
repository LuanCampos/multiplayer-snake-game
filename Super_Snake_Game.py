# importando blibliotecas
import pygame, random, os
from pygame.locals import *

# definindo função que gera posição aleatória
def grid_random():
    return ((random.randint(1,78))*10, (random.randint(1,58))*10)

# definindo função que gera tipos de maça
def apple_random():
    aux = random.randint(1,180)
    if aux % 9 == 0: apple = 3
    elif aux % 5 == 0: apple = 2
    elif aux % 4 == 0: apple = 1
    else: apple = 0
    return apple

# definindo função que pinta as maças
def apple_blit(apple_color, apple_pos):
    apple = pygame.Surface((10,10))
    if apple_color == 3:
        apple.fill((255,255,0))
    if apple_color == 2:
        apple.fill((0,255,255))
    if apple_color == 1:
        apple.fill((0,255,0))
    if apple_color == 0:
        apple.fill((255,0,0))
    return screen.blit(apple, apple_pos)

# definindo uma colisão
def collision(c1, c2):
    return (c1[0] == c2[0]) and (c1[1] == c2[1])

# definindo funcões de high_score
def get_high_score(option):
    high_score = 0
    if option == 0: high_score_file = open(cwd+'\\lib\\save\\single.txt', "r")
    if option == 2: high_score_file = open(cwd+'\\lib\\save\\multi.txt', "r")
    high_score = int(high_score_file.read())
    high_score_file.close()
    return high_score

def save_high_score(option, new_high_score):
    if option == 0: high_score_file = open(cwd+'\\lib\\save\\single.txt', "w")
    if option == 2: high_score_file = open(cwd+'\\lib\\save\\multi.txt', "w")
    high_score_file.write(str(new_high_score))
    high_score_file.close()

# iniciando a tela de jogo
pygame.init()
screen = pygame.display.set_mode((800,640))
pygame.display.set_caption('Super Snake Game v1.1 - Luan Campos - 2019')

# declarando os efeitos sonoros
cwd = os.getcwd()
pygame.mixer.pre_init(22050, -16, 2, 512)
pygame.mixer.init()
apple_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\apple_sound.wav')
ice_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\ice_sound.wav')
gold_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\gold_sound.wav')
game_over_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\game_over_sound.wav')
menu_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\menu.wav')
select_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\select.wav')
nice_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\nice.wav')
high_score_sound = pygame.mixer.Sound(cwd+'\\lib\\sounds\\high_score.wav')
musica = pygame.mixer.music.load(cwd+'\\lib\\sounds\\background_music.mp3')

# música de fundo
pygame.mixer.music.play(-1)

# definindo as direções para tornar o código mais limpo
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# declarando variáveis de pontuação
score1 = 0
score2 = 0
high_score = 0

# declarando o modo de jogo single player
def single():

    # carregando pontuação
    score = 0
    high_score = get_high_score(0)

    # declarando a snake
    snake = [(50,30),(40,30),(30,30)]
    snake_skin = pygame.Surface((10,10))
    snake_skin.fill((255,255,255))

    # setando algumas propriedades da maça
    apple = pygame.Surface((10,10))
    apple.fill((255,0,0))
    apple_pos = grid_random()

    # declarando aparencia da cabeça quando morre
    dead_head = pygame.Surface((10,10))
    dead_head.fill((200,100,100))

    # declarando retângulo do texto
    rect_position = [(0,600),(800,40)]
    myfont = pygame.font.SysFont('comicsansms', 16)

    # border_edges = [x_initial,x_final,y_initial,y_final]
    border_edges = [0,790,0,590]
    border = pygame.Surface((10,10))
    border.fill((255,255,0))

    # outras propriedades da snake
    my_direction = RIGHT
    future_direction = RIGHT
    is_dead = False

    # declarando clock
    clock = pygame.time.Clock()

    # laço de jogo
    while True:

        # lendo "quit"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            #lendo teclado
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    future_direction = UP
                if event.key == K_RIGHT:
                    future_direction = RIGHT
                if event.key == K_DOWN:
                    future_direction = DOWN
                if event.key == K_LEFT:
                    future_direction = LEFT
                if event.key == K_w:
                    future_direction = UP
                if event.key == K_d:
                    future_direction = RIGHT
                if event.key == K_s:
                    future_direction = DOWN
                if event.key == K_a:
                    future_direction = LEFT
                # se morto, jogar outra vez
                if event.key == K_RETURN:
                    if is_dead == True:
                        single()
                # se morto, sair
                if event.key == K_ESCAPE:
                    if is_dead == True:
                        menu()

        # definindo que o jogo só funciona com a snake viva
        if is_dead == False:

            # velocidade do jogo
            clock.tick(20)

            # setando direção futura
            if my_direction == UP and future_direction != DOWN:
                my_direction = future_direction
            if my_direction == RIGHT and future_direction != LEFT:
                my_direction = future_direction
            if my_direction == DOWN and future_direction != UP:
                my_direction = future_direction
            if my_direction == LEFT and future_direction != RIGHT:
                my_direction = future_direction

            # conferindo se a snake pegou a maça
            if collision(snake[0], apple_pos):
                apple_sound.play()
                apple_pos = grid_random()
                snake.append(snake[0])
                score += 10
                
            # snake movimenta a cabeça               
            if my_direction == UP:
                snake[0] = (snake[0][0], snake[0][1] - 10)
            if my_direction == RIGHT:
                snake[0] = (snake[0][0] + 10, snake[0][1])
            if my_direction == DOWN:
                snake[0] = (snake[0][0], snake[0][1] + 10)
            if my_direction == LEFT:
                snake[0] = (snake[0][0] - 10, snake[0][1])

            # snake movimenta o corpo
            for i in range(len(snake)-1, 0, -1):
                snake[i] = (snake[i-1][0], snake[i-1][1])
                    
                # confere se snake não bateu em si mesma
                if i > 1:
                    if collision (snake[i], snake[0]):
                        is_dead = True

            # pinta a tela
            screen.fill((0,0,0))

            # pinta o retângulo da pontuação
            pygame.draw.rect(screen,(150,150,150),rect_position,0)
            textsurface1 = myfont.render("Score:  {}".format(score), True, (30,30,30))
            textsurface2 = myfont.render("High Score:  {}".format(high_score), True, (30,30,30))
            screen.blit(textsurface1,(40,608))
            screen.blit(textsurface2,(350,608))

            # pinta as bordas: superior e inferior (e a grade)
            for i in range(border_edges[1],border_edges[0]-10,-10):
                pygame.draw.line(screen, (35,35,35), (i,border_edges[2]), (i,border_edges[3]), 1)
                screen.blit(border, (i,border_edges[2]))
                screen.blit(border, (i,border_edges[3]))
                
                # confere se snake não bateu na borda superior ou inferior
                if collision (snake[0], (i,border_edges[2])):
                    is_dead = True
                if collision (snake[0], (i,border_edges[3])):
                    is_dead = True

            # pinta as bordas laterais (e a grade)
            for i in range(border_edges[3],border_edges[2],-10):
                pygame.draw.line(screen, (35,35,35), (border_edges[0],i), (border_edges[1],i), 1)
                screen.blit(border, (border_edges[0],i))
                screen.blit(border, (border_edges[1],i))

                # confere se snake não bateu na borda lateral
                if collision (snake[0], (border_edges[0],i)):
                    is_dead = True
                if collision (snake[0], (border_edges[1],i)):
                    is_dead = True

            # pinta a maça
            screen.blit(apple, apple_pos)

            # pinta a snake
            for pos in snake:
                screen.blit(snake_skin, pos)

            # lidando com a morte da snake
            if is_dead == True:
                pygame.draw.rect(screen,(200,200,200),[(50,200),(700,40)],0)
                textsurface = myfont.render('Aperte "ENTER" para jogar outra vez ou "ESC" para sair.', True, (30,30,30))
                if score <= high_score:
                    textsurface2 = myfont.render("Morreu.", True, (150,30,30))
                    game_over_sound.play()
                if score > high_score:
                    textsurface2 = myfont.render("New High Score!", True, (100,255,0))
                    save_high_score(0, score)
                    high_score_sound.play()
                screen.blit(textsurface,(180,208))
                screen.blit(dead_head,snake[0])
                screen.blit(textsurface2,(620,608))

            # repintando a tela
            pygame.display.update()

# declarando o modo de jogo "versus"
def versus(score1, score2):

    # carregando pontuação
    score1 = score1
    score2 = score2

    # declarando a 1° snake
    snake1 = [(50,30),(40,30),(30,30)]
    snake1_skin = pygame.Surface((10,10))
    snake1_skin.fill((255,255,255))

    # declarando a 2° snake
    snake2 = [(740,560),(750,560),(760,560)]
    snake2_skin = pygame.Surface((10,10))
    snake2_skin.fill((150,150,255))

    # declarando as maçãs
    comum = 0
    verde = 1
    gelo = 2
    ouro = 3

    # setando algumas propriedades das maças
    apple = [0,0,0]
    apple_pos = [grid_random(),grid_random(),grid_random()]
    catch_green = 0
    freeze_time = 80

    # declarando aparencia da cabeça quando morre
    dead_head = pygame.Surface((10,10))
    dead_head.fill((200,100,100))

    # declarando retângulo do texto
    rect_position = [(0,600),(800,40)]
    myfont = pygame.font.SysFont('comicsansms', 16)
    textsurface1 = myfont.render("Jogador 1:      {}".format(score1), True, (30,30,30))
    textsurface2 = myfont.render("Jogador 2:      {}".format(score2), True, (30,30,30))

    # border_edges = [x_initial,x_final,y_initial,y_final]
    border_edges = [0,790,0,590]
    border = pygame.Surface((10,10))
    border.fill((255,255,0))

    # outras propriedades da snake1
    my_direction1 = RIGHT
    future_direction1 = RIGHT
    is_dead1 = False
    catch_green1 = False
    freeze1 = False

    # outras propriedades da snake2
    my_direction2 = LEFT
    future_direction2 = LEFT
    is_dead2 = False
    catch_green2 = False
    freeze2 = False

    # declarando clock
    clock = pygame.time.Clock()

    # laço de jogo
    while True:

        # lendo "quit"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            #lendo teclado
            if event.type == KEYDOWN:
                # snake1
                if event.key == K_UP:
                    future_direction1 = UP
                if event.key == K_RIGHT:
                    future_direction1 = RIGHT
                if event.key == K_DOWN:
                    future_direction1 = DOWN
                if event.key == K_LEFT:
                    future_direction1 = LEFT
                # snake2
                if event.key == K_w:
                    future_direction2 = UP
                if event.key == K_d:
                    future_direction2 = RIGHT
                if event.key == K_s:
                    future_direction2 = DOWN
                if event.key == K_a:
                    future_direction2 = LEFT
                # se morto, jogar outra vez
                if event.key == K_RETURN:
                    if is_dead1 == True or is_dead2 == True:
                        versus(score1, score2)
                # se morto, sair
                if event.key == K_ESCAPE:
                    if is_dead1 == True or is_dead2 == True:
                        menu()

        # definindo que o jogo só funciona com ambas as snakes vivas
        if is_dead1 == False and is_dead2 == False:

            # velocidade do jogo
            clock.tick(20)

            # setando direção futura da snake1 se não estiver congelada
            if freeze1 == False:
                if my_direction1 == UP and future_direction1 != DOWN:
                    my_direction1 = future_direction1
                if my_direction1 == RIGHT and future_direction1 != LEFT:
                    my_direction1 = future_direction1
                if my_direction1 == DOWN and future_direction1 != UP:
                    my_direction1 = future_direction1
                if my_direction1 == LEFT and future_direction1 != RIGHT:
                    my_direction1 = future_direction1

            # setando direção futura da snake2 se não estiver congelada
            if freeze2 == False:
                if my_direction2 == UP and future_direction2 != DOWN:
                    my_direction2 = future_direction2
                if my_direction2 == RIGHT and future_direction2 != LEFT:
                    my_direction2 = future_direction2
                if my_direction2 == DOWN and future_direction2 != UP:
                    my_direction2 = future_direction2
                if my_direction2 == LEFT and future_direction2 != RIGHT:
                    my_direction2 = future_direction2

            # conferindo se as snakes pegaram alguma maça
            for i in range(3):
                
                # snake1 pegou qualquer maça
                if collision(snake1[0], apple_pos[i]):
                    # maça comum
                    if apple[i] == comum:
                        apple_sound.play()
                    # maça verde
                    if apple[i] == verde:
                        catch_green = 1
                        apple_sound.play()
                    # maça de gelo
                    if apple[i] == gelo:
                        freeze2 = True
                        ice_sound.play()
                    # maça de ouro
                    if apple[i] == ouro:
                        gold_sound.play()
                        if len(snake2) < 3:
                            del snake2[-1]
                            is_dead2 = True
                        else: del snake2[-1]
                    # todas as maças
                    apple[i] = apple_random()
                    apple_pos[i] = grid_random()
                    snake1.append(snake1[0])

                # snake2 pegou qualquer maça
                if collision(snake2[0], apple_pos[i]):
                    # maça comum
                    if apple[i] == comum:
                        apple_sound.play()
                    # maça verde
                    if apple[i] == verde:
                        catch_green = 2
                        apple_sound.play()
                    # maça de gelo
                    if apple[i] == gelo:
                        freeze1 = True
                        ice_sound.play()
                    # maça de ouro
                    if apple[i] == ouro:
                        gold_sound.play()
                        if len(snake1) < 3:
                            del snake1[-1]
                            is_dead1 = True
                        else: del snake1[-1]
                    # todas as maças
                    apple[i] = apple_random()
                    apple_pos[i] = grid_random()
                    snake2.append(snake2[0])

            # conferindo se alguma havia pegado maça verde
            if catch_green1 == True:
                snake1.append(snake1[0])
                catch_green1 = False
            if catch_green2 == True:
                snake2.append(snake2[0])
                catch_green2 = False
                
            # snake1 movimenta a cabeça se não estiver congelada
            if freeze1 == False:                
                if my_direction1 == UP:
                    snake1[0] = (snake1[0][0], snake1[0][1] - 10)
                if my_direction1 == RIGHT:
                    snake1[0] = (snake1[0][0] + 10, snake1[0][1])
                if my_direction1 == DOWN:
                    snake1[0] = (snake1[0][0], snake1[0][1] + 10)
                if my_direction1 == LEFT:
                    snake1[0] = (snake1[0][0] - 10, snake1[0][1])

            # snake1 movimenta o corpo
            for i in range(len(snake1)-1, 0, -1):
                if freeze1 == False:
                    snake1[i] = (snake1[i-1][0], snake1[i-1][1])
                    
                    # confere se snake1 não bateu em si mesma
                    if i > 1:
                        if collision (snake1[i], snake1[0]):
                            is_dead1 = True
                            
                # confere se snake2 não bateu em snake1
                if collision (snake1[i], snake2[0]):
                    is_dead2 = True

            # snake2 movimenta a cabeça se não estiver congelada
            if freeze2 == False:            
                if my_direction2 == UP:
                    snake2[0] = (snake2[0][0], snake2[0][1] - 10)
                if my_direction2 == RIGHT:
                    snake2[0] = (snake2[0][0] + 10, snake2[0][1])
                if my_direction2 == DOWN:
                    snake2[0] = (snake2[0][0], snake2[0][1] + 10)
                if my_direction2 == LEFT:
                    snake2[0] = (snake2[0][0] - 10, snake2[0][1])

            # snake2 movimenta o corpo
            for i in range(len(snake2)-1, 0, -1):
                if freeze2 == False:
                    snake2[i] = (snake2[i-1][0], snake2[i-1][1])
                    
                    # confere se snake1 não bateu em si mesma
                    if i > 1:
                        if collision (snake2[i], snake2[0]):
                            is_dead2 = True
                            
                # confere se snake1 não bateu em snake2
                if collision (snake2[i], snake1[0]):
                    is_dead1 = True
                    
            # confere se não bateu cabeça com cabeça
            if collision (snake1[0], snake2[0]):
                is_dead1 = True
                is_dead2 = True

            # conferindo se alguma pegou maça verde
            if catch_green != 0:
                if catch_green == 1:
                    catch_green1 = True
                    catch_green = 0
                if catch_green == 2:
                    catch_green2 = True
                    catch_green = 0

            # lidando com a snake congelada
            if freeze1 == True or freeze2 == True:
                freeze_time = freeze_time - 1
                if freeze_time < 1:
                    freeze1 = False
                    freeze2 = False
                    freeze_time = 80

            # pinta a tela
            screen.fill((0,0,0))

            # pinta o retângulo da pontuação
            pygame.draw.rect(screen,(150,150,150),rect_position,0)
            screen.blit(textsurface1,(40,608))
            screen.blit(textsurface2,(300,608))

            # pinta as bordas: superior e inferior (e a grade)
            for i in range(border_edges[1],border_edges[0]-10,-10):
                pygame.draw.line(screen, (35,35,35), (i,border_edges[2]), (i,border_edges[3]), 1)
                screen.blit(border, (i,border_edges[2]))
                screen.blit(border, (i,border_edges[3]))
                
                # confere se snake1 não bateu na borda superior ou inferior
                if collision (snake1[0], (i,border_edges[2])):
                    is_dead1 = True
                if collision (snake1[0], (i,border_edges[3])):
                    is_dead1 = True

                # confere se snake2 não bateu na borda superior ou inferior
                if collision (snake2[0], (i,border_edges[2])):
                    is_dead2 = True
                if collision (snake2[0], (i,border_edges[3])):
                    is_dead2 = True

            # pinta as bordas laterais (e a grade)
            for i in range(border_edges[3],border_edges[2],-10):
                pygame.draw.line(screen, (35,35,35), (border_edges[0],i), (border_edges[1],i), 1)
                screen.blit(border, (border_edges[0],i))
                screen.blit(border, (border_edges[1],i))

                # confere se snake1 não bateu na borda lateral
                if collision (snake1[0], (border_edges[0],i)):
                    is_dead1 = True
                if collision (snake1[0], (border_edges[1],i)):
                    is_dead1 = True

                # confere se snake2 não bateu na borda lateral
                if collision (snake2[0], (border_edges[0],i)):
                    is_dead2 = True
                if collision (snake2[0], (border_edges[1],i)):
                    is_dead2 = True

            # pinta as maças
            for i in range(3):
                apple_blit(apple[i], apple_pos[i])

            # pinta a snake1
            for pos in snake1:
                screen.blit(snake1_skin, pos)

            # pinta a snake2
            for pos in snake2:
                screen.blit(snake2_skin, pos)

            # lidando com a morte da snake1
            if is_dead1 == True and is_dead2 == False:
                score2 += 1
                screen.blit(dead_head,snake1[0])
                textsurface = myfont.render("Jogador 2 venceu.", True, (150,30,30))
                textsurface2 = myfont.render("Jogador 2:      {}".format(score2), True, (30,30,30))
                screen.blit(textsurface,(550,608))

            # lidando com a morte da snake2
            if is_dead2 == True and is_dead1 == False:
                score1 += 1
                screen.blit(dead_head,snake2[0])
                textsurface = myfont.render("Jogador 1 venceu.", True, (150,30,30))
                textsurface1 = myfont.render("Jogador 1:      {}".format(score1), True, (30,30,30))
                screen.blit(textsurface,(550,608))

            # lidando com empate
            if is_dead2 == True and is_dead1 == True:
                screen.blit(dead_head,snake1[0])
                screen.blit(dead_head,snake2[0])
                textsurface = myfont.render("Empate!", True, (150,30,30))
                screen.blit(textsurface,(550,608))

            # lidando com qualquer morte
            if is_dead1 == True or is_dead2 == True:
                
                # pergunta se quer jogar de novo
                pygame.draw.rect(screen,(200,200,200),[(50,200),(700,40)],0)
                textsurface = myfont.render('Aperte "ENTER" para jogar outra vez ou "ESC" para sair.', True, (30,30,30))
                screen.blit(textsurface,(180,208))
                # atualiza pontuação
                pygame.draw.rect(screen,(150,150,150),[(0,600),(500,40)],0)
                screen.blit(textsurface1,(40,608))
                screen.blit(textsurface2,(300,608))
                game_over_sound.play()

            # repintando a tela
            pygame.display.update()

# declarando o modo de jogo "co-op"
def multiplayer():

    # carregando pontuação
    score = 0
    high_score = get_high_score(2)

    # declarando a 1° snake
    snake1 = [(50,30),(40,30),(30,30)]
    snake1_skin = pygame.Surface((10,10))
    snake1_skin.fill((255,255,255))

    # declarando a 2° snake
    snake2 = [(740,560),(750,560),(760,560)]
    snake2_skin = pygame.Surface((10,10))
    snake2_skin.fill((150,150,255))

    # declarando as maçãs
    comum = 0
    verde = 1
    gelo = 2
    ouro = 3

    # setando algumas propriedades das maças
    apple = [0,0,0]
    apple_pos = [grid_random(),grid_random(),grid_random()]
    catch_green = 0
    freeze_time = 80

    # declarando aparencia da cabeça quando morre
    dead_head = pygame.Surface((10,10))
    dead_head.fill((200,100,100))

    # declarando retângulo do texto
    rect_position = [(0,600),(800,40)]
    myfont = pygame.font.SysFont('comicsansms', 16)

    # border_edges = [x_initial,x_final,y_initial,y_final]
    border_edges = [0,790,0,590]
    border = pygame.Surface((10,10))
    border.fill((255,255,0))

    # outras propriedades da snake1
    my_direction1 = RIGHT
    future_direction1 = RIGHT
    is_dead1 = False
    catch_green1 = False
    freeze1 = False

    # outras propriedades da snake2
    my_direction2 = LEFT
    future_direction2 = LEFT
    is_dead2 = False
    catch_green2 = False
    freeze2 = False

    # declarando clock
    clock = pygame.time.Clock()

    # laço de jogo
    while True:

        # lendo "quit"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()

            #lendo teclado
            if event.type == KEYDOWN:
                # snake1
                if event.key == K_UP:
                    future_direction1 = UP
                if event.key == K_RIGHT:
                    future_direction1 = RIGHT
                if event.key == K_DOWN:
                    future_direction1 = DOWN
                if event.key == K_LEFT:
                    future_direction1 = LEFT
                # snake2
                if event.key == K_w:
                    future_direction2 = UP
                if event.key == K_d:
                    future_direction2 = RIGHT
                if event.key == K_s:
                    future_direction2 = DOWN
                if event.key == K_a:
                    future_direction2 = LEFT
                # se morto, jogar outra vez
                if event.key == K_RETURN:
                    if is_dead1 == True or is_dead2 == True:
                        multiplayer()
                # se morto, sair
                if event.key == K_ESCAPE:
                    if is_dead1 == True or is_dead2 == True:
                        menu()

        # definindo que o jogo só funciona com ambas as snakes vivas
        if is_dead1 == False and is_dead2 == False:

            # velocidade do jogo
            clock.tick(20)

            # setando direção futura da snake1 se não estiver congelada
            if freeze1 == False:
                if my_direction1 == UP and future_direction1 != DOWN:
                    my_direction1 = future_direction1
                if my_direction1 == RIGHT and future_direction1 != LEFT:
                    my_direction1 = future_direction1
                if my_direction1 == DOWN and future_direction1 != UP:
                    my_direction1 = future_direction1
                if my_direction1 == LEFT and future_direction1 != RIGHT:
                    my_direction1 = future_direction1

            # setando direção futura da snake2 se não estiver congelada
            if freeze2 == False:
                if my_direction2 == UP and future_direction2 != DOWN:
                    my_direction2 = future_direction2
                if my_direction2 == RIGHT and future_direction2 != LEFT:
                    my_direction2 = future_direction2
                if my_direction2 == DOWN and future_direction2 != UP:
                    my_direction2 = future_direction2
                if my_direction2 == LEFT and future_direction2 != RIGHT:
                    my_direction2 = future_direction2

            # conferindo se as snakes pegaram alguma maça
            for i in range(3):
                
                # snake1 pegou qualquer maça
                if collision(snake1[0], apple_pos[i]):
                    # maça comum
                    if apple[i] == comum:
                        apple_sound.play()
                    # maça verde
                    if apple[i] == verde:
                        catch_green = 1
                        score += 10
                        apple_sound.play()
                    # maça de gelo
                    if apple[i] == gelo:
                        freeze2 = True
                        ice_sound.play()
                    # maça de ouro
                    if apple[i] == ouro:
                        score += 10
                        gold_sound.play()
                        if len(snake2) < 3:
                            del snake2[-1]
                            is_dead2 = True
                        else: del snake2[-1]
                    # todas as maças
                    score += 10
                    apple[i] = apple_random()
                    apple_pos[i] = grid_random()
                    if apple[i] != gelo: snake1.append(snake1[0])

                # snake2 pegou qualquer maça
                if collision(snake2[0], apple_pos[i]):
                    # maça comum
                    if apple[i] == comum:
                        apple_sound.play()
                    # maça verde
                    if apple[i] == verde:
                        catch_green = 2
                        score += 10
                        apple_sound.play()
                    # maça de gelo
                    if apple[i] == gelo:
                        freeze1 = True
                        ice_sound.play()
                    # maça de ouro
                    if apple[i] == ouro:
                        score += 10
                        gold_sound.play()
                        if len(snake1) < 3:
                            del snake1[-1]
                            is_dead1 = True
                        else: del snake1[-1]
                    # todas as maças
                    score += 10
                    apple[i] = apple_random()
                    apple_pos[i] = grid_random()
                    if apple[i] != gelo: snake2.append(snake2[0])

            # conferindo se alguma havia pegado maça verde
            if catch_green1 == True:
                snake1.append(snake1[0])
                catch_green1 = False
            if catch_green2 == True:
                snake2.append(snake2[0])
                catch_green2 = False
                
            # snake1 movimenta a cabeça se não estiver congelada
            if freeze1 == False:                
                if my_direction1 == UP:
                    snake1[0] = (snake1[0][0], snake1[0][1] - 10)
                if my_direction1 == RIGHT:
                    snake1[0] = (snake1[0][0] + 10, snake1[0][1])
                if my_direction1 == DOWN:
                    snake1[0] = (snake1[0][0], snake1[0][1] + 10)
                if my_direction1 == LEFT:
                    snake1[0] = (snake1[0][0] - 10, snake1[0][1])

            # snake1 movimenta o corpo
            for i in range(len(snake1)-1, 0, -1):
                if freeze1 == False:
                    snake1[i] = (snake1[i-1][0], snake1[i-1][1])
                    
                    # confere se snake1 não bateu em si mesma
                    if i > 1:
                        if collision (snake1[i], snake1[0]):
                            is_dead1 = True
                            
                # confere se snake2 não bateu em snake1
                if collision (snake1[i], snake2[0]):
                    is_dead2 = True

            # snake2 movimenta a cabeça se não estiver congelada
            if freeze2 == False:            
                if my_direction2 == UP:
                    snake2[0] = (snake2[0][0], snake2[0][1] - 10)
                if my_direction2 == RIGHT:
                    snake2[0] = (snake2[0][0] + 10, snake2[0][1])
                if my_direction2 == DOWN:
                    snake2[0] = (snake2[0][0], snake2[0][1] + 10)
                if my_direction2 == LEFT:
                    snake2[0] = (snake2[0][0] - 10, snake2[0][1])

            # snake2 movimenta o corpo
            for i in range(len(snake2)-1, 0, -1):
                if freeze2 == False:
                    snake2[i] = (snake2[i-1][0], snake2[i-1][1])
                    
                    # confere se snake1 não bateu em si mesma
                    if i > 1:
                        if collision (snake2[i], snake2[0]):
                            is_dead2 = True
                            
                # confere se snake1 não bateu em snake2
                if collision (snake2[i], snake1[0]):
                    is_dead1 = True
                    
            # confere se não bateu cabeça com cabeça
            if collision (snake1[0], snake2[0]):
                is_dead1 = True
                is_dead2 = True

            # conferindo se alguma pegou maça verde
            if catch_green != 0:
                if catch_green == 1:
                    catch_green1 = True
                    catch_green = 0
                if catch_green == 2:
                    catch_green2 = True
                    catch_green = 0

            # lidando com a snake congelada
            if freeze1 == True or freeze2 == True:
                freeze_time = freeze_time - 1
                if freeze_time < 1:
                    freeze1 = False
                    freeze2 = False
                    freeze_time = 80

            # pinta a tela
            screen.fill((0,0,0))

            # pinta o retângulo da pontuação
            pygame.draw.rect(screen,(150,150,150),rect_position,0)
            textsurface1 = myfont.render("Score:  {}".format(score), True, (30,30,30))
            textsurface2 = myfont.render("High Score:  {}".format(high_score), True, (30,30,30))
            screen.blit(textsurface1,(40,608))
            screen.blit(textsurface2,(350,608))

            # pinta as bordas: superior e inferior (e a grade)
            for i in range(border_edges[1],border_edges[0]-10,-10):
                pygame.draw.line(screen, (35,35,35), (i,border_edges[2]), (i,border_edges[3]), 1)
                screen.blit(border, (i,border_edges[2]))
                screen.blit(border, (i,border_edges[3]))
                
                # confere se snake1 não bateu na borda superior ou inferior
                if collision (snake1[0], (i,border_edges[2])):
                    is_dead1 = True
                if collision (snake1[0], (i,border_edges[3])):
                    is_dead1 = True

                # confere se snake2 não bateu na borda superior ou inferior
                if collision (snake2[0], (i,border_edges[2])):
                    is_dead2 = True
                if collision (snake2[0], (i,border_edges[3])):
                    is_dead2 = True

            # pinta as bordas laterais (e a grade)
            for i in range(border_edges[3],border_edges[2],-10):
                pygame.draw.line(screen, (35,35,35), (border_edges[0],i), (border_edges[1],i), 1)
                screen.blit(border, (border_edges[0],i))
                screen.blit(border, (border_edges[1],i))

                # confere se snake1 não bateu na borda lateral
                if collision (snake1[0], (border_edges[0],i)):
                    is_dead1 = True
                if collision (snake1[0], (border_edges[1],i)):
                    is_dead1 = True

                # confere se snake2 não bateu na borda lateral
                if collision (snake2[0], (border_edges[0],i)):
                    is_dead2 = True
                if collision (snake2[0], (border_edges[1],i)):
                    is_dead2 = True

            # pinta as maças
            for i in range(3):
                apple_blit(apple[i], apple_pos[i])

            # pinta a snake1
            for pos in snake1:
                screen.blit(snake1_skin, pos)

            # pinta a snake2
            for pos in snake2:
                screen.blit(snake2_skin, pos)

            # lidando com a morte das snakes
            if is_dead1 == True or is_dead2 == True:
                pygame.draw.rect(screen,(200,200,200),[(50,200),(700,40)],0)
                textsurface = myfont.render('Aperte "ENTER" para jogar outra vez ou "ESC" para sair.', True, (30,30,30))
                if score <= high_score:
                    textsurface2 = myfont.render("Morreu.", True, (150,30,30))
                    game_over_sound.play()
                if score > high_score:
                    textsurface2 = myfont.render("New High Score!", True, (100,255,0))
                    save_high_score(2, score)
                    high_score_sound.play()
                screen.blit(textsurface,(180,208))
                screen.blit(textsurface2,(620,608))
                if is_dead1 == True: screen.blit(dead_head,snake1[0])
                if is_dead2 == True: screen.blit(dead_head,snake2[0])

            # repintando a tela
            pygame.display.update()

# declarando o menu
def inicio():
    
    while True:

        # lendo "quit"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            # lendo teclado
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    menu()
                if event.key == K_ESCAPE:
                    pygame.quit()

        menu_image = pygame.image.load(cwd+'\\lib\\inicio.png')
        screen.blit(menu_image,(0,0))
        pygame.display.flip()

def menu():

    option = 0
    position = [(257,280),(257,344),(257,408)]
    select = False
    menu_image = pygame.image.load(cwd+'\\lib\\menu.png')
    apple_image = pygame.image.load(cwd+'\\lib\\apple.png')
    
    while True:

        # lendo "quit"
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()                
                
            # lendo teclado
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    select = True
                if event.key == K_ESCAPE:
                    inicio()
                    
                    # andar para cima
                if event.key == K_UP:
                    if option == 1: option = 0
                    if option == 2: option = 1
                    menu_sound.play()

                    # andar para baixo
                if event.key == K_DOWN:
                    if option == 1: option = 2
                    if option == 0: option = 1
                    menu_sound.play()
                    
        screen.blit(menu_image,(0,0))

        if option == 0:
            screen.blit(apple_image,position[0])
        if option == 1:
            screen.blit(apple_image,position[1])
        if option == 2:
            screen.blit(apple_image,position[2])

        if select == True:
            select_sound.play()
            if option == 0:
                single()
            if option == 1:
                versus(score1, score2)
            if option == 2:
                multiplayer()
        
        pygame.display.flip()

# chamando a tela de apresentação
inicio()
