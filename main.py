import pygame
from pygame.locals import *
import time
import random

SIZE = 40
WIDTH = 1000
HEIGHT = 760
class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = random.randint(1,23)*SIZE
        self.y = random.randint(1,17)*SIZE
    
    def draw(self):
        self.parent_screen.fill((30, 50, 100), (0, 0, self.parent_screen.get_width(), self.parent_screen.get_height()))
        self.parent_screen.fill((0, 0, 0), (SIZE, SIZE, self.parent_screen.get_width()-80, self.parent_screen.get_height()-80))            #this line fills the screen therefore hiding 
        self.parent_screen.blit(self.image, (self.x, self.y))                                                                              #previous blocks that were drawn

    def move(self):
        self.x = random.randint(1,23)*SIZE
        self.y = random.randint(1,17)*SIZE

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.alive = True
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE*((WIDTH/SIZE)//2)]*length
        self.y = [SIZE*((HEIGHT/SIZE)//2)]*length
        self.direction = "none"

    def draw(self):
        
        for i in range(self.length):                                                                                                
            self.parent_screen.blit(self.block, (self.x[i], self.y[i])) 
        pygame.display.flip()
    
    def move_left(self):
        self.direction = "left"
    def move_right(self):
        self.direction = "right"
    def move_up(self):
        self.direction = "up"
    def move_down(self):
        self.direction = "down"

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        self.draw()
    
    def grow(self):
        self.x.append(self.x[self.length-1])
        self.y.append(self.y[self.length-1])
        self.length += 1


        
class Enemy:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [random.randint(1,23)*SIZE]*length
        self.y = [random.randint(1,17)*SIZE]*length
        self.direction = "right"

    def draw(self):
        
        for i in range(self.length):                                                                                                
            self.parent_screen.blit(self.block, (self.x[i], self.y[i])) 
        pygame.display.flip()
    
    def move_right(self):
        self.direction = "right"
    def move_up(self):
        self.direction = "up"

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "right":
            self.x[0] += SIZE
        self.draw()
    
    def grow(self):
        self.x.append(self.x[self.length-1])
        self.y.append(self.y[self.length-1])
        self.length += 1



class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption("Snake")
        self.running = True
        self.pause = True
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.surface.fill((0, 255, 0), (0, SIZE, self.surface.get_width(), self.surface.get_height()-40))   
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.enemies = list()
        self.enemy_created = False

        self.play_background_music()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def apple_collision(self, x1, x2, y1, y2):
        if y1 == y2 and x1 == x2:
            self.play_sound("ding")
            self.snake.grow()
            return True
            
        return False

    def wall_collision(self, x, y):
        x_coord = x/40
        y_coord = y/40
        if x_coord < 1 or x_coord > 23 or y_coord < 1 or y_coord > 17:
            self.play_sound("crash")
            return True
        return False
    
    def body_collision(self):
        head_x = self.snake.x[0]
        head_y = self.snake.y[0]
        for i in range(4, len(self.snake.x)):
            if self.snake.x[i] == head_x and self.snake.y[i] == head_y:
                self.play_sound("crash")
                return True
        for j, enemy in enumerate(self.enemies):
            for i in range(enemy.length):
                if head_x == enemy.x[i] and head_y == enemy.y[i]:
                    self.play_sound("crash")
                    return True
            for i in range(self.snake.length):
                if self.snake.x[i] == enemy.x[0] and self.snake.y[i] == enemy.y[0]:
                    self.play_sound("crash")
                    del self.enemies[j]
            
        return False
    
    def enemy_apple_collision(self, x1, x2, y1, y2):
        if y1 == y2 and x1 == x2:
            self.play_sound("ding")
            return True
            
        return False


    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(score, (850, 5))

    def play(self):

        if self.apple_collision(self.snake.x[0], self.apple.x, self.snake.y[0], self.apple.y):
            self.apple.move()
            self.apple.draw()
        
        for enemy in self.enemies:
            if self.enemy_apple_collision(enemy.x[0], self.apple.x, enemy.y[0], self.apple.y):
                self.apple.move()
                self.apple.draw()
                enemy.grow()

        self.apple.draw()
        self.snake.walk()
        for enemy in self.enemies:
            enemy.walk()

        if self.wall_collision(self.snake.x[0], self.snake.y[0]):
            self.pause = True
            self.snake.alive = False
        if self.body_collision():
            self.pause = True
            self.snake.alive = False

        for enemy in self.enemies:
            x = enemy.x[0]/40
            y = enemy.y[0]/40
            if x > 23:
                enemy.x[0] = 40
            elif y < 1:
                enemy.y[0] = 680


        if self.snake.length % 5 == 0:
            if not self.enemy_created:
                self.enemies.append(Enemy(self.surface, 1))
                self.enemy_created = True
        else:
            self.enemy_created = False

        self.display_score()
        pygame.display.flip()



    def run(self):
        while self.running:
            for event in pygame.event.get():    #pygame.event.get() stores events that happened
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                    if event.key == K_RETURN:
                        if self.pause == True:
                            self.snake.x = [SIZE*((WIDTH/SIZE)//2)]
                            self.snake.y = [SIZE*((HEIGHT/SIZE)//2)]
                            self.snake.length = 1
                            self.snake.direction = "none"
                            self.apple.move()
                            self.apple.draw()
                            self.snake.draw()
                            self.snake.alive = True
                            self.enemies = list()
                        else:
                            continue
                    elif self.snake.alive == True:
                        if event.key == K_UP and self.snake.direction != "down":
                            self.snake.move_up()
                            self.pause = False
                        elif event.key == K_DOWN and self.snake.direction != "up":
                            self.snake.move_down()
                            self.pause = False
                        elif event.key == K_LEFT and self.snake.direction != "right":
                            self.snake.move_left()
                            self.pause = False
                        elif event.key == K_RIGHT and self.snake.direction != "left":
                            self.snake.move_right()
                            self.pause = False
                        break


                elif event.type == QUIT:
                    self.running = False
            
            for enemy in self.enemies:
                if enemy.x[0] == self.apple.x:
                    enemy.move_up()
                elif enemy.y[0] == self.apple.y:
                    enemy.move_right()

            if not self.pause:
                self.play()
            else:
                if self.snake.direction == "none":
                    font = pygame.font.SysFont('arial', 30)
                    score = font.render("Press any arrow key to start", True, (255, 255, 255))
                    self.surface.blit(score, (338, 230))
                    pygame.display.flip()
                elif self.snake.alive == False:
                    font = pygame.font.SysFont('arial', 30)
                    score = font.render(f"Game Over, your score was {self.snake.length}. Press enter to play again.", True, (255, 255, 255))
                    self.surface.blit(score, (200, 350))
                    pygame.display.flip()

            pygame.time.Clock().tick(10)




if __name__ == "__main__":
    game = Game()
    game.run()



    