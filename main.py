import pygame
import math


pygame.init()
screen = pygame.display.set_mode((880, 650))
clock = pygame.time.Clock()
running = True


class Bala:
    def __init__(self, x, y, vx, vy, dono, cor_bala):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.dono = dono
        self.cor_bala = cor_bala

    def update(self):
        self.x += self.vx
        self.y += self.vy
        return 0 <= self.x <= 880 and 0 <= self.y <= 650

    def draw(self):
        pygame.draw.circle(screen, self.cor_bala, (int(self.x), int(self.y)), 5)

class Tanque:
    def __init__(self, x, y, cor, teclas, image):
        self.x = x
        self.y = y
        self.angulo = 0
        self.cor = cor
        self.teclas = teclas
        self.movendo = False
        self.sentido_rotacao = True  #True: horario // False: anti-horario
        self.vidas = 3
        self.balas = 3
        self.ultimo_reload = pygame.time.get_ticks()
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.vx = 0
        self.vy = 0

    def update(self):
        if self.movendo:
            rad = math.radians(self.angulo)
            novo_x = self.x + math.cos(rad) * 3
            novo_y = self.y + math.sin(rad) * 3

            if 0 <= novo_x <= 880 - 64:
                self.x = novo_x
            if 0 <= novo_y <= 650:
                self.y = novo_y

        if self.balas < 3 and pygame.time.get_ticks() - self.ultimo_reload > 2000:
            self.balas += 1
            self.ultimo_reload = pygame.time.get_ticks()

        if self.sentido_rotacao:
            self.angulo -= 2
        else:
            self.angulo += 2

    def draw(self):
        imagem_rodada = pygame.transform.rotate(self.image, -self.angulo)
        rect_rodado = imagem_rodada.get_rect(center=(self.x, self.y))
        screen.blit(imagem_rodada, rect_rodado.topleft)

    def atirar(self, balas):
        if self.balas > 0:
            rad = math.radians(self.angulo)
            bala_x = self.x + math.cos(rad) * 32
            bala_y = self.y + math.sin(rad) * 32
            balas.append(Bala(bala_x, bala_y, math.cos(rad) * 5, math.sin(rad) * 5, self, self.cor))
            if self.balas == 3:
              self.ultimo_reload = pygame.time.get_ticks()
            self.balas -= 1


    def checar_colisao(self, balas):
        tank_rect = self.image.get_rect(center=(self.x, self.y))
        for bala in balas[:]:
            bala_rect = pygame.Rect(bala.x - 5, bala.y - 5, 10, 10)
            if bala_rect.colliderect(tank_rect) and bala.dono != self:
                balas.remove(bala)
                self.vidas -= 1
                if self.vidas <= 0:
                    return True
        return False

def display_winner(cor_vencedor):
    screen.fill((255, 255, 255))
    font = pygame.font.Font(None, 74)
    text = font.render(f"Tanque {cor_vencedor} ganhou!", True, (0, 0, 0))
    text_rect = text.get_rect(center=(880 // 2, 650 // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(3000)

#==================# IMAGENS #===========================#
muni_blue = pygame.image.load("muni_blue.png")
muni_red = pygame.image.load("muni_red.png")
coracao_blue = pygame.transform.scale(pygame.image.load("coracao_blue.png"), (52, 48))
coracao_red = pygame.transform.scale(pygame.image.load("coracao_red.png"), (52, 48))
#========================================================#



def main():
    jogando = False

    vidas_blue_lista = [(0, 598), (52, 598), (104, 598)]
    vidas_red_lista = [(828, 0), (776, 0), (724, 0)]

    balas_blue_lista = [(170, 586), (192, 586), (214, 586)]
    balas_red_lista = [(699, 0), (677, 0), (655, 0)]

    running = True
    balas = []
    tank1 = Tanque(100, 550, (66, 135, 245), {"move": pygame.K_w, "shoot": pygame.K_e}, "tank_azul.png")
    tank2 = Tanque(780, 100, (214, 24, 65), {"move": pygame.K_DOWN, "shoot": pygame.K_RIGHT}, "tank_vermelho.png")
    
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP and not jogando:
              if botao_rect.collidepoint(pygame.mouse.get_pos()):
                jogando = True
            elif event.type == pygame.KEYDOWN:
                if event.key == tank1.teclas["move"]:
                    tank1.movendo = True
                elif event.key == tank2.teclas["move"]:
                    tank2.movendo = True
                elif event.key == tank1.teclas["shoot"]:
                    tank1.atirar(balas)
                elif event.key == tank2.teclas["shoot"]:
                    tank2.atirar(balas)
            elif event.type == pygame.KEYUP:
                if event.key == tank1.teclas["move"]:
                    tank1.movendo = False
                    tank1.sentido_rotacao = not tank1.sentido_rotacao
                elif event.key == tank2.teclas["move"]:
                    tank2.movendo = False
                    tank2.sentido_rotacao = not tank2.sentido_rotacao
        
        if not jogando:
          screen.blit(pygame.image.load("fundo_inicio.jpg"), (0,0))

          botao_rect = pygame.Rect(355, 480, 140, 60)
          pygame.draw.rect(screen, (181, 181, 181), botao_rect, 0, 15)

          fonte = pygame.font.Font('freesansbold.ttf', 36)
          texto_play = fonte.render('Play', True, (194, 0, 0), (181, 181, 181))
          textRect = texto_play.get_rect()
          textRect.center = (425, 510)
          screen.blit(texto_play, textRect)

        else:
          screen.blit(pygame.image.load("fundo_game.jpg"), (0,0))
          for i in range(tank1.vidas):
            screen.blit(coracao_blue, vidas_blue_lista[i])
          for i in range(tank2.vidas):
            screen.blit(coracao_red, vidas_red_lista[i])

          for i in range(tank1.balas):
            screen.blit(muni_blue, balas_blue_lista[i])
          for i in range(tank2.balas):
            screen.blit(muni_red, balas_red_lista[i])

          tank1.update()
          tank2.update()
          balas = [b for b in balas if b.update()]
          
          tank1.draw()
          tank2.draw()
          for bala in balas:
              bala.draw()
          
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()