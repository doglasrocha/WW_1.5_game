from guns import Weapon
from pygame import Surface
import pygame
import cores
from movivel import Movivel
from time import time

fonte_30 = pygame.font.SysFont('arial', 30, True)

class Personagem(Movivel):
    
    def __init__(self, screen: Surface):
        self.SPEED = 1
        self.x_speed = 0
        self.y_speed = 0
        self.screen = screen
        self.max_hp = 100
        self.hp = 100
        self.weapon = None
        self.direction = 'NORTH'
        self.state = 'ALIVE'
        self.time_passed_since_death = None
        self.time_passed = 0
        self.size = None

    def pintar(self):
        pygame.draw.rect(self.screen, cores.CIANO, (self.x, self.y, self.size, self.size))
        self.paint_hp()
        self.weapon.paint(self.size, True)
        
    def paint_hp(self):
        hp = f'HP: {self.hp}'
        hp_render = fonte_30.render(hp, True, cores.BRANCO)
        width_to_center = hp_render.get_width() / 2
        self.screen.blit(hp_render, (1350 - width_to_center, 750))
        
    def reinicia_stats(self):
        self.hp = 100
        self.weapon.reinit_stats()
        self.state = 'ALIVE'
        self.direction = 'NORTH'
    
    def processar_eventos(self, evento, teclado, mouse):
        w = pygame.K_w
        a = pygame.K_a
        s = pygame.K_s
        d = pygame.K_d
        
        w_pressionado = bool(teclado[w])
        a_pressionado = bool(teclado[a])
        s_pressionado = bool(teclado[s])
        d_pressionado = bool(teclado[d])
            
        if w_pressionado and a_pressionado:
            self.y_speed = -self.SPEED
            self.x_speed = -self.SPEED
            self.direction = 'NORTH WEST'
        elif w_pressionado and d_pressionado:
            self.y_speed = -self.SPEED
            self.x_speed = self.SPEED
            self.direction = 'NORTH EAST'
        elif s_pressionado and a_pressionado:
            self.y_speed = self.SPEED
            self.x_speed = -self.SPEED
            self.direction = 'SOUTH WEST'
        elif s_pressionado and d_pressionado:
            self.y_speed = self.SPEED
            self.x_speed = self.SPEED
            self.direction = 'SOUTH EAST'
        elif s_pressionado and w_pressionado:
            self.y_speed = 0
        elif a_pressionado and d_pressionado:
            self.x_speed = 0
            
        elif w_pressionado:
            self.y_speed = -self.SPEED
            self.direction = 'NORTH'
        elif a_pressionado:
            self.x_speed = -self.SPEED
            self.direction = 'WEST'
        elif s_pressionado:
            self.y_speed = self.SPEED
            self.direction = 'SOUTH'
        elif d_pressionado:
            self.x_speed = self.SPEED
            self.direction = 'EAST'
            
        tecla_solta = evento.type == pygame.KEYUP   
        if tecla_solta:
            tecla = evento.key
            if tecla == w:
                self.y_speed = 0
            if tecla == a:
                self.x_speed = 0
            if tecla == s:
                self.y_speed = 0
            if tecla == d:
                self.x_speed = 0
        
        if any(mouse[0]):
            self.weapon.shoot(mouse[1][0], mouse[1][1], self.x, self.y)
    
    def receive_weapon(self, weapon: Weapon):
        self.weapon = weapon
        