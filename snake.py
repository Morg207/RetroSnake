import tkinter as tk
from tkinter import font
import pygame
import random
import time

pygame.mixer.init()

BLOCK_SIZE = 20
WIDTH_IN_BLOCKS = 540 // BLOCK_SIZE
HEIGHT_IN_BLOCKS = 540 // BLOCK_SIZE

class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake")
        self.window.resizable(False, False)
        self.canvas = self.init_canvas()
        self.snake = Snake()
        self.apple = Apple()
        self.init_sounds()
        self.score = 0
        self.draw_booster = False
        self.booster_x = 0
        self.booster_y = 0
        self.booster_count = 0
        self.score_booster = "+1"
        self.score_font = font.Font(family="Segoe UI",size=17,weight="bold")
        self.game_font = font.Font(family="Segoe UI",size=16,weight="bold")
        self.hunger_bar = HungerBar(self.lose_sound, self.snake)
        self.draw()

    def init_canvas(self):
        canvas = tk.Canvas(self.window, width=540, height=540, bg="#282828")
        canvas.pack(expand=True, fill="both")
        canvas.bind("<KeyPress>", lambda e: self.handle_keyboard(e))
        canvas.focus_set()
        return canvas

    def init_sounds(self):
        self.eat_sound = pygame.mixer.Sound("Sound/eat sound.ogg")
        self.lose_sound = pygame.mixer.Sound("Sound/lose.mp3")
        self.ga_sound = pygame.mixer.Sound("Sound/golden apple.wav")

    def handle_keyboard(self, event):
        self.snake.handle_keyboard(event)

    def collide_with_apple(self, head):
        if head.x == self.apple.x_tile and head.y == self.apple.y_tile:
            if self.apple.colour == "#c4372d":
                self.score += 1
                self.score_booster = "+1"
                self.eat_sound.play()
            elif self.apple.colour == "#b59b35" or self.apple.colour == "#f2d25a":
                self.score += 5
                self.score_booster = "+5"
                self.ga_sound.play()
            self.hunger_bar.fill_bar()
            self.apple.gen_new_position()
            self.booster_x = head.x * BLOCK_SIZE
            self.booster_y = head.y * BLOCK_SIZE
            self.booster_count = 0
            self.draw_booster = True
            self.snake.extend = True

    def collide_with_walls(self, head):
        if head.x < 0 or head.x > WIDTH_IN_BLOCKS-1 or head.y < 0 or head.y > HEIGHT_IN_BLOCKS-1:
            self.lose_sound.play()
            self.score = 0
            self.snake.reset()
            self.apple.gen_new_position()
            self.hunger_bar.reset()

    def collide_with_body(self, head):
        for x in range(1, len(self.snake.body)):
            body_part = self.snake.body[x]
            if body_part.x == head.x and body_part.y == head.y:
                self.lose_sound.play()
                self.score = 0
                self.snake.reset()
                self.apple.gen_new_position()
                self.hunger_bar.reset()
                break

    def handle_collision(self):
        head = self.snake.body[0]
        self.collide_with_apple(head)
        self.collide_with_walls(head)
        self.collide_with_body(head)

    def draw_score_booster(self):
        if self.draw_booster:
            self.canvas.create_text(self.booster_x, self.booster_y, text=self.score_booster, fill="white",
                                    font=self.game_font)
            self.booster_count += 1
            if self.booster_count > 5:
                self.draw_booster = False
                self.booster_count = 0

    def draw_score(self):
        self.canvas.create_text(540 // 2, 30, text=f"Score: {self.score}", fill="white", font=self.score_font)

    def draw(self):
        self.canvas.delete("all")
        self.apple.draw(self.canvas)
        self.snake.move()
        self.snake.draw(self.canvas)
        self.handle_collision()
        self.draw_score_booster()
        self.draw_score()
        self.hunger_bar.draw(self.canvas)
        self.window.after(150,self.draw)

    def run_game(self):
        self.window.mainloop()

class HungerBar:
    def __init__(self, lose_sound, snake):
        self.snake = snake
        self.lose_sound = lose_sound
        self.x = 390
        self.y = 50
        self.text_x = 448
        self.text_y = 28
        self.bar_length = 115
        self.start_bar_length = 115
        self.eat_amount = 30
        self.bar_height = 15
        self.hunger_font = font.Font(family="Segoe UI",size=16,weight="bold")

    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x+self.start_bar_length, self.y+self.bar_height, fill="#b35a1b", outline="white", width=2)
        canvas.create_rectangle(self.x, self.y, self.x+self.bar_length, self.y+self.bar_height, fill="orange", outline="white",width=2)
        canvas.create_text(self.text_x,self.text_y,text="Hunger", font=self.hunger_font, fill="white")
        self.bar_length -= 1
        self.bar_length = max(0, self.bar_length)
        if self.bar_length == 0:
            self.lose_sound.play()
            self.snake.reset()
            self.bar_length = self.start_bar_length

    def fill_bar(self):
        self.bar_length += self.eat_amount
        self.bar_length = min(self.bar_length, self.start_bar_length)

    def reset(self):
        self.bar_length = self.start_bar_length

class Apple:
    def __init__(self):
        self.x_tile = random.randint(0, WIDTH_IN_BLOCKS-1)
        self.y_tile = random.randint(0, HEIGHT_IN_BLOCKS-1)
        self.colour = "#c4372d"
        self.pulse = False
        self.pulse_counter = 0
        self.counter = 0

    def draw(self, canvas):
        if self.pulse:
                if self.pulse_counter % 2 == 0:
                    self.colour = "#b59b35"
                else:
                    self.colour = "#f2d25a"
                self.pulse_counter += 1
                if self.pulse_counter > 1:
                    self.pulse_counter = 0

        canvas.create_rectangle(self.x_tile * BLOCK_SIZE, self.y_tile * BLOCK_SIZE,
                                self.x_tile * BLOCK_SIZE + BLOCK_SIZE, self.y_tile * BLOCK_SIZE + BLOCK_SIZE, fill=self.colour, outline=self.colour)

    def gen_new_position(self):
        self.x_tile = random.randint(0, WIDTH_IN_BLOCKS - 1)
        self.y_tile = random.randint(0, HEIGHT_IN_BLOCKS - 1)
        choices = [1,2,3,4,5,6,7,8,9,10]
        choice = random.choice(choices)
        if choice == 1 or choice == 2:
            self.colour = "#b59b35"
            self.pulse = True
        else:
            self.colour = "#c4372d"
            self.pulse = False

class Snake:
    def __init__(self):
        self.body = [pygame.Vector2(22,22), pygame.Vector2(23,22), pygame.Vector2(24,22)]
        self.direction = "a"
        self.extend = False
        self.key_buffer = []

    def reset(self):
        self.body = [pygame.Vector2(22, 22), pygame.Vector2(23, 22), pygame.Vector2(24, 22)]
        self.direction = "a"
        self.extend = False

    def handle_keyboard(self, event):
        key = event.keysym
        if key not in self.key_buffer:
            self.key_buffer.append(key)

    def set_direction(self):
        if self.key_buffer:
            key = self.key_buffer.pop()
            if key=="w" and self.direction != "s":
                self.direction = "w"
            elif key=="s" and self.direction != "w":
                self.direction = "s"
            elif key=="a" and self.direction != "d":
                self.direction = "a"
            elif key=="d" and self.direction != "a":
                self.direction = "d"

    def move(self):
        self.set_direction()
        new_head = self.body[0].copy()
        if self.direction == "a":
            new_head.x -= 1
        elif self.direction == "d":
            new_head.x += 1
        elif self.direction == "w":
            new_head.y -= 1
        elif self.direction == "s":
            new_head.y += 1

        self.body.insert(0, new_head)

        if not self.extend:
            self.body.pop()
        else:
            self.extend = False

    def draw(self, canvas):
        for index, body_part in enumerate(reversed(self.body)):
            if index == len(self.body)-1:
                body_colour="darkgreen"
            else:
                body_colour = "green"
            canvas.create_rectangle(body_part.x*BLOCK_SIZE,body_part.y*BLOCK_SIZE,
                                    body_part.x*BLOCK_SIZE + BLOCK_SIZE, body_part.y*BLOCK_SIZE + BLOCK_SIZE, fill=body_colour, outline="green")

if __name__ == "__main__":
    game = Game()
    game.run_game()

