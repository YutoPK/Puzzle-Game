import pygame
import random
import sys
import os
#import pkg_resources.py2_warn
from pathlib import Path


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


size_of_window_x = 900
size_of_window_y = 650
writer_x = 290
writer_y = 85

b1 = [(0, 127, 0, 255), (0, 255, 255, 255), (0, 0, 255, 255), (255, 0, 255, 255), (255, 0, 0, 255),
      (0, 0, 0, 255), (0, 255, 0, 255), (255, 255, 0, 255), (255, 255, 255, 255)]

b2 = [(255, 0, 0, 255), (255, 255, 0, 255), (255, 0, 255, 255), (0, 0, 255, 255), (0, 255, 255, 255),
      (0, 255, 0, 255), (0, 0, 0, 255), (255, 255, 255, 255)]

b3 = [(255, 0, 255, 255), (0, 0, 255, 255), (0, 255, 255, 255), (0, 255, 0, 255), (255, 255, 255, 255),
      (255, 255, 0, 255), (255, 0, 0, 255), (0, 0, 0, 255)]

s = str(Path(__file__).absolute())
s = s[0:len(s)-7]
print(s)

f = r"media\fonts\""
f = f[0:len(f)-1]

m = r"media\pics\""
m = m[0:len(m)-1]

q = r"media\questions\""
q = q[0:len(q)-1]

window = pygame.display.set_mode((size_of_window_x, size_of_window_y))
pygame.init()
pygame.font.init()
pygame.display.set_icon(pygame.image.load(s+m+"icon.jfif"))
pygame.display.set_caption("Kviz")

class Game:
    def __init__(self, r, r2):
        self.run = True

        self.white = (255, 255, 255)
        self.writer_arr_x = [320, 320, 320]
        self.writer_arr_y = [465, 465, 465]
        self.correct_size = [200, 110]

        self.array_of_writers = ["dositej", "vuk", "njegos"]
        self.ar_colors = r2
        self.all_pieces = set()
        self.save_color = []
        self.used_colors = []
        self.final = len(self.ar_colors)

        self.num_of_writer = r
        self.num_of_pieces = 0
        self.counter = 0

        self.bool_fade_window = False

        self.gray_writer = -1
        self.correct_img = -1
        self.wrong_img = -1
        self.the_end = -1
        self.fade_window = -1
        self.colors = -1
        self.question = -1
        self.final_line = -1
        self.bcg = -1
        self.set_images()

        self.time = 90

    def set_images(self):

        asset_url = resource_path(s+m+"pozadina.png")
        self.bcg = pygame.image.load(asset_url).convert_alpha()

        asset_url = resource_path(s+m+"tacno.png")
        self.correct_img = pygame.image.load(asset_url).convert_alpha()

        asset_url = resource_path(s+m+"netacno.png")
        self.wrong_img = pygame.image.load(asset_url).convert_alpha()

        asset_url = resource_path(s+m+"kraj.png")
        self.the_end = pygame.image.load(asset_url).convert_alpha()

        asset_url = resource_path(s+m+"transparent.png")
        self.fade_window = pygame.image.load(asset_url).convert_alpha()
        self.fade_window.fill((0, 0, 0, 128), None, pygame.BLEND_RGBA_MULT)

        asset_url = resource_path(s+m+str(self.array_of_writers[self.num_of_writer]) + "ime.png")
        self.final_line = pygame.image.load(asset_url).convert_alpha()

        asset_url = resource_path(s+m+str(self.array_of_writers[self.num_of_writer]) + "boja.png")
        self.colors = pygame.image.load(asset_url).convert_alpha()

        asset_url = resource_path(s+m+str(self.array_of_writers[self.num_of_writer]) + ".png")
        self.gray_writer = pygame.image.load(asset_url).convert_alpha()

    def redraw(self):
        window.fill(self.white)
        self.draw_img(self.bcg, 0, 0)
        self.draw_img(self.gray_writer, writer_x, writer_y)

        for i in self.all_pieces:
            img = pygame.image.load(
                s+m+self.array_of_writers[self.num_of_writer] + str(i + 1) + ".png").convert_alpha()
            self.draw_img(img, writer_x, writer_y)

        if self.bool_fade_window:
            self.draw_img(self.fade_window, 0, 0)
            self.draw_img(self.question, 75, 80)
            self.draw_img(self.correct_img, 10, 500)
            self.draw_img(self.wrong_img, 690, 500)
        else:
            self.draw_img(self.the_end, 10, 10)

        if self.num_of_pieces == self.final:
            self.draw_img(self.final_line, 0, 0)

        pygame.display.update()

    def end(self):
        for i in self.ar_colors:
            if i not in self.used_colors:
                self.all_pieces.add(self.ar_colors.index(i))
                self.used_colors.append(i)
        self.num_of_pieces = self.final

    def draw_img(self, img, x1, y1):
        window.blit(img, (x1, y1))

    def if_in_colors(self, arr):
        if arr in self.ar_colors and arr not in self.used_colors:
            self.bool_fade_window = True

            p = (self.ar_colors.index(arr))
            asset_url = resource_path(s+q+str(self.array_of_writers[self.num_of_writer])+"pitanje"+str(p+1)+".png")
            self.question = pygame.image.load(asset_url).convert_alpha()

            self.save_color = arr

    def mainloop(self):
        a = 0
        for i in range(0, 10000):
            a = i
        #t = 0
        while self.run:
            #t += 1
            if self.counter == self.time:
                self.run = False

            if self.num_of_pieces == self.final:
                self.counter += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    press_x, press_y = event.pos

                    if not self.bool_fade_window and writer_x < press_x < self.writer_arr_x[self.num_of_writer] + writer_x \
                            and writer_y < press_y < self.writer_arr_y[self.num_of_writer] + writer_y:
                        self.if_in_colors(self.colors.get_at((press_x - writer_x, press_y - writer_y)))

                    if self.bool_fade_window and 10 <= press_x <= 10 + self.correct_size[0] and 500 <= press_y <= \
                            500 + self.correct_size[1]:
                        self.all_pieces.add(self.ar_colors.index(self.save_color))
                        self.used_colors.append(self.save_color)
                        self.num_of_pieces += 1
                        self.bool_fade_window = False

                    if not self.bool_fade_window and 10 <= press_x <= 160 and 10 <= press_y <= 70:
                        self.end()

                    if self.bool_fade_window and 690 <= press_x <= 690 + self.correct_size[0] and 500 <= press_y <= \
                            500 + self.correct_size[1]:
                        self.bool_fade_window = False

            self.redraw()
        return True


class Menu:
    def __init__(self):
        self.run = True
        self.white = (255, 255, 255)
        self.size_img = [275, 110]
        self.arr = []
        self.r123 = [0, 1, 2]

        self.start_x = 310
        self.start_y = 170
        self.exit_x = 310
        self.exit_y = 370

        asset_url = resource_path(s+m+"kreni.png")
        self.start = pygame.image.load(asset_url).convert_alpha()
        asset_url = resource_path(s+m+"izlaz.png")
        self.exit = pygame.image.load(asset_url).convert_alpha()
        asset_url = resource_path(s+m+"pozadina.png")
        self.bcg = pygame.image.load(asset_url).convert_alpha()

    def redraw(self):
        window.fill(self.white)
        self.draw_img(self.bcg, 0, 0)
        self.draw_img(self.start, self.start_x, self.start_y)
        self.draw_img(self.exit, self.exit_x, self.exit_y)
        pygame.display.update()

    def draw_img(self, img, x1, y1):
        window.blit(img, (x1, y1))

    def random_writer(self):
        if len(self.arr) == 0:
            self.arr.append(random.randrange(0, 3))
        elif len(self.arr) == 1:
            x = self.arr[0]
            self.r123.remove(x)
            f = random.randrange(0, 2)
            self.arr.append(self.r123[f])
            self.r123.append(x)
        else:
            x1 = self.arr[0]
            x2 = self.arr[1]
            self.r123.remove(x1)
            self.r123.remove(x2)

            self.arr.clear()
            self.arr.append(self.r123[0])

            self.r123.append(x1)
            self.r123.append(x2)

        return self.arr[-1]

    def start_game(self):
        c = self.random_writer()
        t = False
        if c == 0:
            game = Game(c, b1)
            t=game.mainloop()
        elif c == 1:
            game = Game(c, b2)
            t=game.mainloop()
        else:
            game = Game(c, b3)
            t=game.mainloop()
        if not t:
            self.run = False
    def mainloop(self):
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        press_x, press_y = event.pos
                        if self.start_x <= press_x <= self.start_x + self.size_img[0] and self.start_y <= press_y <= self.start_y  + self.size_img[1]:
                            self.start_game()
                        elif self.exit_x <= press_x <= self.exit_x + self.size_img[0] and self.exit_y <= press_y <= self.exit_y + self.size_img[1]:
                            self.run = False
            self.redraw()


menu = Menu()
menu.mainloop()
