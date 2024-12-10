from random import randint
import pygame
import config
from menu import Menu
from misc.action import Attack, Potion, Spell
from state import State


class Battle(State, Menu):
    def __init__(self, game, name, enemy, player):
        State.__init__(self, game, name)
        Menu.__init__(self, game)
        self.enemy = enemy
        self.player = player
        self.enemy_image = pygame.transform.scale(self.enemy.image, (256,256))
        self.enemy_rect = self.enemy_image.get_rect(topright=(config.DISPLAY_W, -40))
        self.player_image = pygame.transform.scale(self.player.image, (256,256))
        self.player_flip =  pygame.transform.flip(self.player_image, True, False)
        self.player_rect = self.player_flip.get_rect(bottomleft=(0, config.DISPLAY_H + 20))
        self.player_banner = pygame.transform.scale(pygame.image.load('assets/ui-banner.png').convert_alpha(), (500, 40))
        self.enemy_banner = pygame.transform.scale(pygame.image.load('assets/ui-banner.png').convert_alpha(), (500, 40))
        
        self.player_banner_rect = self.player_banner.get_rect(topleft=(20, 50))
        self.enemy_banner_rect = self.enemy_banner.get_rect(topleft=self.player_banner_rect.bottomleft)
        self.lunge_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))
        self.heavystrike_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))
        self.fireball_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))
        self.shieldthrow_img = pygame.transform.scale(pygame.image.load('assets/ui-banner2.png').convert_alpha(), (150, 50))

        self.lunge_rect = self.lunge_img.get_rect(bottomleft=(40, self.player_banner_rect.centery + 320))
        self.heavystrike_rect = self.heavystrike_img.get_rect(bottomleft=self.lunge_rect.bottomright)
        self.fireball_rect = self.fireball_img.get_rect(bottomleft=self.heavystrike_rect.bottomright)
        self.shieldthrow_rect = self.shieldthrow_img.get_rect(bottomleft=self.fireball_rect.bottomright)
        self.ribbon_image = pygame.transform.scale(pygame.image.load('assets/ui-banner.png').convert_alpha(), (150, 50))
        self.font = pygame.font.Font('assets/8-bit-hud.ttf', 15)
        self.font2 = pygame.font.Font('assets/8-bit-hud.ttf', 5)

        self.lunge_text = self.font2.render('Lunge 5mp', True, self.game.BLACK)
        self.heavystrike_text = self.font2.render('Heavy Strike 7mp', True, self.game.BLACK)
        self.fireball_text = self.font2.render('Fireball 5mp', True, self.game.BLACK)
        self.shieldthrow_text = self.font2.render('Shield Throw 3mp', True, self.game.BLACK)
        self.melee_text = self.font2.render('Melee Attack', True, self.game.BLACK)
        self.potion_text = self.font2.render(f'Health Potion: {self.player.inventory['Health']}', True, self.game.BLACK)
        self.mana_text = self.font2.render(f'Mana Potion: {self.player.inventory['Mana']}', True, self.game.BLACK)
        self.flee_text = self.font2.render('Flee', True, self.game.BLACK)

        self.lunge_text_rect = self.lunge_text.get_rect(center=(self.lunge_rect.centerx, self.lunge_rect.centery))
        self.heavystrike_text_rect = self.heavystrike_text.get_rect(center=(self.heavystrike_rect.centerx, self.heavystrike_rect.centery))
        self.fireball_text_rect = self.fireball_text.get_rect(center=(self.fireball_rect.centerx, self.fireball_rect.centery))
        self.shieldthrow_text_rect = self.shieldthrow_text.get_rect(center=(self.shieldthrow_rect.centerx, self.shieldthrow_rect.centery))

        self.melee_rect = self.ribbon_image.get_rect(bottomleft=self.heavystrike_rect.topleft)
        self.potion_rect = self.ribbon_image.get_rect(topleft=self.melee_rect.topright)
        self.mana_rect = self.ribbon_image.get_rect(topleft=self.potion_rect.topright)
        self.flee_rect = self.ribbon_image.get_rect(topleft=self.mana_rect.topright)

        self.melee_text_rect = self.melee_text.get_rect(center=self.melee_rect.center)
        self.potion_text_rect = self.potion_text.get_rect(center=self.potion_rect.center)
        self.mana_text_rect = self.mana_text.get_rect(center=self.mana_rect.center)
        self.flee_text_rect = self.flee_text.get_rect(center=self.flee_rect.center)

        self.header_text = 'You encountered an enemy!'
        self.header = self.font.render(self.header_text, True, self.game.BLACK)
        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)

        self.enemy_header_text = ''
        self.enemy_header = self.font.render(self.enemy_header_text, True, self.game.BLACK)
        self.enemy_header_rect = self.enemy_header.get_rect(center=self.enemy_banner_rect.center)

        self.enemy_hp = self.font.render(f'HP: {self.enemy.hp}', True, self.game.BLACK)
        self.enemy_hp_rect = self.enemy_hp.get_rect(center=(self.enemy_rect.centerx, self.enemy_rect.centery + 50))

        self.hp = self.font.render(f'HP: {self.player.hp}', True, self.game.BLACK)
        self.hp_rect = self.hp.get_rect(bottomleft=self.melee_rect.topleft)
        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
        self.mp_rect = self.mp.get_rect(bottomleft=self.hp_rect.topleft)

        self.menu_options = {
            0: (self.melee_text_rect.centerx - 40, config.DISPLAY_H - 75),
            1: (self.potion_text_rect.centerx - 40, config.DISPLAY_H - 75),
            2: (self.mana_text_rect.centerx - 40, config.DISPLAY_H - 75),
            3: (self.flee_text_rect.centerx - 40, config.DISPLAY_H - 75),
            4: (self.lunge_text_rect.centerx - 40, config.DISPLAY_H - 25),
            5: (self.heavystrike_text_rect.centerx - 40, config.DISPLAY_H - 25),
            6: (self.fireball_text_rect.centerx - 40, config.DISPLAY_H - 25),
            7: (self.shieldthrow_text_rect.centerx - 40, config.DISPLAY_H - 25),
        }
        
        self.index = 0
        self.cursor_rect.center = (self.melee_text_rect.centerx - 40, config.DISPLAY_H - 70)
        self.turn = 'Player'


    def update(self, delta_time, actions):
        self.enemy.update(delta_time)
        self.battle(actions)
        self.game.reset_keys()

    def render(self, surface):
        surface.fill(self.game.WHITE)
        surface.blit(self.enemy_image, self.enemy_rect)
        surface.blit(self.player_image, self.player_rect)
        surface.blit(self.player_banner, self.player_banner_rect)
        surface.blit(self.enemy_banner, self.enemy_banner_rect)
        surface.blit(self.lunge_img, self.lunge_rect)
        surface.blit(self.heavystrike_img, self.heavystrike_rect)
        surface.blit(self.fireball_img, self.fireball_rect)
        surface.blit(self.shieldthrow_img, self.shieldthrow_rect)
        surface.blit(self.ribbon_image, self.melee_rect)
        surface.blit(self.ribbon_image, self.potion_rect)
        surface.blit(self.ribbon_image, self.mana_rect)
        surface.blit(self.ribbon_image, self.flee_rect)
        surface.blit(self.lunge_text, self.lunge_text_rect)
        surface.blit(self.heavystrike_text, self.heavystrike_text_rect)
        surface.blit(self.fireball_text, self.fireball_text_rect)
        surface.blit(self.shieldthrow_text, self.shieldthrow_text_rect)
        surface.blit(self.melee_text, self.melee_text_rect)
        surface.blit(self.potion_text, self.potion_text_rect)
        surface.blit(self.mana_text, self.mana_text_rect)
        surface.blit(self.flee_text, self.flee_text_rect)
        surface.blit(self.header, self.header_rect)
        surface.blit(self.enemy_header, self.enemy_header_rect)
        surface.blit(self.enemy_hp, self.enemy_hp_rect)
        surface.blit(self.hp, self.hp_rect)
        surface.blit(self.mp, self.mp_rect)
        self.draw_cursor2()

    def move_cursor(self, actions):
        if actions['right']:
            self.index += 1
            if self.index == 8:
                self.index = 0
        if actions['move right']:
            self.index += 1
            if self.index == 8:
                self.index = 0
        if actions['left']:
            self.index -= 1
            if self.index < 0:
                self.index = 7
        if actions['move left']:
            self.index -= 1
            if self.index < 0:
                self.index = 7
        if actions['up']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        if actions['move up']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        if actions['down']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        if actions['move down']:
            if self.index >= 4:
                self.index -= 4
            else:
                self.index += 4
        self.cursor_rect.center = self.menu_options[self.index]

    def player_turn(self, actions):
        action = None
        if actions['enter']:
            if self.index == 0:
                action = 'Melee'
            elif self.index == 1:
                action = 'Health'
            elif self.index == 2:
                action = 'Mana'
            elif self.index == 3:
                action = 'Flee'
            elif self.index == 4:
                action = 'Lunge'
            elif self.index == 5:
                action = 'Heavy Strike'
            elif self.index == 6:
                action = 'Fireball'
            elif self.index == 7:
                action = 'Shield Throw'
            
            if self.index >= 4:
                move = Spell(action, self.player)
                chance = randint(1,20) + int((self.player.stats['AGI']-10)/2)
                dodge_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2)
                if self.player.mp >= move.mp_cost:
                    if chance > dodge_chance:
                        damage_amount = move.use()
                        self.player.mp -= move.mp_cost
                        self.enemy.hp -= damage_amount
                        self.enemy_hp = self.font.render(f'HP: {self.enemy.hp}', True, self.game.BLACK)
                        self.header_text = f'Your {move.type} dealt {damage_amount} damage to the Orc!'
                        self.header = self.font.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
                        self.turn = 'Enemy'
                    else:
                        self.player.mp -= move.mp_cost
                        self.header_text = f'Your move missed!'
                        self.header = self.font.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
                        self.turn = 'Enemy'
                else:
                    self.header_text = 'Not enough mana!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)

            elif action == 'Melee':
                chance = randint(1,20) + int((self.player.stats['AGI']-10)/2)
                dodge_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2)
                if chance > dodge_chance:
                    move = Attack(self.player)
                    damage_amount = move.use()
                    self.enemy.hp -= damage_amount
                    self.enemy_hp = self.font.render(f'HP: {self.enemy.hp}', True, self.game.BLACK)
                    self.header_text = f'Your melee attack does {damage_amount} damage to the Orc!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                else:
                    self.header_text = 'Your melee attack misses!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                self.turn = 'Enemy'

            elif action == 'Flee':
                chance = randint(1,20) + int((self.player.stats['AGI']-10)/2)
                fail_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2)
                if chance > fail_chance:
                    self.exit_state()
                else:
                    self.header_text = 'You fail to flee!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                    self.turn = 'Enemy'

            else:
                move = Potion(action, self.player)
                if self.player.inventory[action] >= 1:
                    amount = move.use()
                    if action == 'Health':
                        self.player.hp += amount
                        if self.player.hp >= self.player.max_hp:
                            self.player.hp = self.player.max_hp
                            self.header_text = f'You healed to full health!'
                        else:
                            self.header_text = f'You healed {amount} hp!'
                        self.player.inventory['Health'] -= 1
                        self.hp = self.font.render(f'HP: {self.player.hp}', True, self.game.BLACK)
                        self.potion_text = self.font2.render(f'Health Potion: {self.player.inventory["Health"]}', True, self.game.BLACK)
                        self.header = self.font.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.turn = 'Enemy'    
                    else:
                        self.player.mp += amount
                        if self.player.mp >= self.player.max_mp:
                            self.player.mp = self.player.max_mp
                            self.header_text = f'You recovered all your mana!'
                        else:
                            self.header_text = f'You healed {amount} mp!'
                        self.player.inventory['Mana'] -= 1
                        self.mp = self.font.render(f'MP: {self.player.mp}', True, self.game.BLACK)
                        self.mana_text = self.font2.render(f'Mana Potion: {self.player.inventory["Mana"]}', True, self.game.BLACK)
                        self.header = self.font.render(self.header_text, True, self.game.BLACK)
                        self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)
                        self.turn = 'Enemy'
                else:
                    self.header_text = 'You do not have any potions!'
                    self.header = self.font.render(self.header_text, True, self.game.BLACK)
                    self.header_rect = self.header.get_rect(center=self.player_banner_rect.center)


    def enemy_turn(self):
        dodge_chance = randint(1, 20) + int((self.player.stats['AGI'] - 10) / 2)
        hit_chance = randint(1, 20) + int((self.enemy.level.speed - 10) / 2)
        if hit_chance >= dodge_chance:
            damage = self.enemy.attack()
            self.player.hp -= damage
            self.hp = self.font.render(f'HP: {self.player.hp}', True, self.game.BLACK)
            self.enemy_header_text = f'The Orc attacks you for {damage} damage!'
            self.enemy_header = self.font.render(self.enemy_header_text, True, self.game.BLACK)
            self.enemy_header_rect = self.enemy_header.get_rect(center=self.enemy_banner_rect.center)
        else:
            self.enemy_header_text = f'You dodge the attack!'
            self.enemy_header = self.font.render(self.enemy_header_text, True, self.game.BLACK)
            self.enemy_header_rect = self.enemy_header.get_rect(center=self.enemy_banner_rect.center)
        self.turn = 'Player'

    def battle(self, actions):
        if self.player.hp > 0 and self.enemy.hp > 0:
            if self.turn == 'Player':
                self.move_cursor(actions)
                self.player_turn(actions)
            else:
                self.enemy_turn()
        elif self.enemy.hp <= 0:
            self.exit_state()
        elif self.player.hp <= 0:
            pass