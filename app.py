import math
import sys
import tkinter.filedialog


import pickle

import pygame

pygame.init()

DISPLAYWIDTH = 1280
DISPLAYHEIGHT = 720

TILE_SIZE = 100
ROW_TILE = 3

TILE_VIEW_START_X = 40 + TILE_SIZE * ROW_TILE
display = pygame.display.set_mode((DISPLAYWIDTH, DISPLAYHEIGHT))

basicfont = pygame.font.Font("resources/fonts/neodgm.ttf", 20)

ok_button_img = pygame.image.load("resources/images/ok_button.png")
open_button_img = pygame.image.load("resources/images/open_button.png")
save_button_img = pygame.image.load("resources/images/save_button.png")
load_button_img = pygame.image.load("resources/images/load_button.png")
add_Tile_img = pygame.image.load("resources/images/add_tile.png")
input_field_img = pygame.transform.scale(pygame.image.load("resources/images/input_field.png"), (256, 32))

SCREEN_TILE_WIDTH = math.ceil((DISPLAYWIDTH - TILE_VIEW_START_X) / TILE_SIZE)
SCREEN_TILE_HEIGHT = math.ceil((DISPLAYWIDTH - 100) / TILE_SIZE)

print(SCREEN_TILE_WIDTH)
def showtextscreencenter( pos, text, color, font):
    textsurf = font.render(text, True, color)
    textrect = textsurf.get_rect()
    textrect.center = pos

    display.blit(textsurf, textrect)

def showtextscreen( pos, text, color, font):
    textsurf = font.render(text, True, color)


    display.blit(textsurf, pos)


class Button:
    def __init__(self, x, y, w, h, image=None, text=None, color=(50, 50, 50, 0), font=None, ):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.image = pygame.transform.scale(image, (w, h))
        self.text = text
        self.font = font

        self.rect = pygame.Rect(x, y, w, h)
        assert image == None or text == None, "Image and text shouldn't None"

    def draw(self):

        if self.image == None:

            showtextscreencenter(self.rect.center, self.text, self.color, self.font)
        else:
            display.blit(self.image, self.rect)

    def click(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                return True

        return False
class InputField:
    def __init__(self, x, y, placeholder):
        self.placeholder = placeholder
        self.text = ""
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 128, 32)
        self.active = False
    def draw(self):
        display.blit(input_field_img, (self.x, self.y))
        if self.text:
            showtextscreen((self.x + 8, self.y + 8), self.text, (50, 50, 50), basicfont)
        else:
            showtextscreen((self.x + 8, self.y + 8), self.placeholder, (150, 150, 150), basicfont)
    def update(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:

            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode


def add_tile():
    # return {'file_path': 'C:/Users/영민/Pictures/brick.png', 'tile_name': 'asdf123'}
    ok_button = Button(DISPLAYWIDTH / 2 - 50, DISPLAYHEIGHT / 2 + 75, 100, 50, ok_button_img)
    name_input_field = InputField(DISPLAYWIDTH / 2 - 128, DISPLAYHEIGHT / 2 - 50, "이름 입력")
    open_button = Button(DISPLAYWIDTH / 2 + 45, DISPLAYHEIGHT / 2, 100, 50, open_button_img)
    file_info = {}
    while True:

        pygame.draw.rect(display, (180, 180, 180), (DISPLAYWIDTH / 2 - 200, DISPLAYHEIGHT / 2 - 150, 400, 300))
        pygame.draw.rect(display, (150, 150, 150), (DISPLAYWIDTH / 2 - 200, DISPLAYHEIGHT / 2 - 150, 400, 300), 2)
        ok_button.draw()
        open_button.draw()
        name_input_field.draw()
        showtextscreencenter((DISPLAYWIDTH / 2, DISPLAYHEIGHT / 2 - 70), "Add Tile", (50, 50, 50), basicfont)
        showtextscreencenter((DISPLAYWIDTH / 2 - 35, DISPLAYHEIGHT / 2 + 25), "이미지 선택", (50, 50, 50), basicfont)
        for event in pygame.event.get():
            name_input_field.update(event)
            if open_button.click(event):
                file_path = tkinter.filedialog.askopenfilename(initialdir="/", title="이미지 선택", filetypes=(("*.png", "*png"), ("*.jpg", "*jpg")), )
                file_info["file_path"] = file_path
            if ok_button.click(event):
                file_info["tile_name"] = name_input_field.text

                print(file_info)
                return file_info
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def update_tile_buttons(tile_images, tile_buttons):

    i = len(tile_images) - 1
    tile_buttons.append(Button((i % ROW_TILE) * TILE_SIZE + 20, (i // ROW_TILE) * TILE_SIZE + 120, TILE_SIZE, TILE_SIZE, image=tile_images[-1]))

def draw_tiles(tiles, tile_images_dict, x, y):

    for x1 in range(x, SCREEN_TILE_WIDTH + x):
        for y1 in range(y, SCREEN_TILE_HEIGHT + y):

            if tile_images_dict.get(tiles[y1][x1]):

                display.blit(tile_images_dict.get(tiles[y1][x1]), ((x1 - x) * TILE_SIZE + 60 + TILE_SIZE * ROW_TILE, (y1 - y) * TILE_SIZE + 90))

def get_tile_pos_from_mouse(mousepos):
    for tx in range((DISPLAYWIDTH - TILE_VIEW_START_X) // TILE_SIZE):
        for ty in range((DISPLAYWIDTH - 100) // TILE_SIZE):
            rx, ry = tx * 100 + TILE_VIEW_START_X, ty * 100 + 100
            rect = pygame.Rect(rx, ry, TILE_SIZE, TILE_SIZE)
            if rect.collidepoint(mousepos):
                return tx, ty

    return -1, -1


def get_width_and_height():
    width_input_field = InputField(DISPLAYWIDTH / 2 - 70, DISPLAYHEIGHT / 2 - 75, "너비 입력")
    height_input_field = InputField(DISPLAYWIDTH / 2 - 70, DISPLAYHEIGHT / 2, "너비 입력")
    ok_button = Button(DISPLAYWIDTH / 2 - 50, DISPLAYHEIGHT / 2 + 75, 100, 50, ok_button_img)
    while True:
        pygame.draw.rect(display, (180, 180, 180), (DISPLAYWIDTH / 2 - 200, DISPLAYHEIGHT / 2 - 150, 400, 300))
        pygame.draw.rect(display, (150, 150, 150), (DISPLAYWIDTH / 2 - 200, DISPLAYHEIGHT / 2 - 150, 400, 300), 2)
        width_input_field.draw()
        height_input_field.draw()
        ok_button.draw()
        showtextscreencenter((DISPLAYWIDTH / 2 - 125, DISPLAYHEIGHT / 2 - 66), "너비 입력", (50, 50, 50), basicfont)
        showtextscreencenter((DISPLAYWIDTH / 2 - 125, DISPLAYHEIGHT / 2 + 16), "높이 입력", (50, 50, 50), basicfont)
        for event in pygame.event.get():
            width_input_field.update(event)
            height_input_field.update(event)
            if ok_button.click(event):
                return int(width_input_field.text), int(height_input_field.text)


        pygame.display.update()

def main():

    tile_images = {}
    tile_width, tile_height = get_width_and_height()


    tile_buttons = []
    x = 0
    y = 0
    add_tile_button = Button(10, 10, 200, 50, add_Tile_img)
    save_button = Button(220, 10, 100, 50, save_button_img)
    load_button = Button(330, 10, 100, 50, load_button_img)
    selectedtileidx = -1
    tiles = [[""] * tile_width for _ in range(tile_height)]
    tile_kinds = []
    selectedrect = None
    while True:

        display.fill((200, 200, 200))
        add_tile_button.draw()
        save_button.draw()
        load_button.draw()
        pygame.draw.line(display, (0, 0, 0), (50, 80), (DISPLAYWIDTH - 50, 80), 2)
        pygame.draw.line(display, (0, 0, 0)z, (TILE_VIEW_START_X - 20, 100), (TILE_VIEW_START_X - 20, DISPLAYHEIGHT - 20), 2)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and x + SCREEN_TILE_WIDTH < (tile_width - 5):
                    x += 1
                if event.key == pygame.K_LEFT and x > 0:
                    x -= 1
                if event.key == pygame.K_UP and y > 0:
                    y -= 1
                if event.key == pygame.K_DOWN and x + SCREEN_TILE_HEIGHT < (tile_height - 5):
                    y += 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                tx, ty = get_tile_pos_from_mouse(event.pos)
                if tx != -1 and selectedtileidx != -1:

                    tiles[y + ty][x + tx] = tile_kinds[selectedtileidx]["tile_name"]

            for i, button in enumerate(tile_buttons):
                if button.click(event):
                    selectedrect = button.rect
                    selectedtileidx = i
            if add_tile_button.click(event):
                new_tile = add_tile()
                tile_images[new_tile["tile_name"]] = (pygame.transform.scale(pygame.image.load(new_tile["file_path"]), (TILE_SIZE, TILE_SIZE)))
                update_tile_buttons([keyval[1] for keyval in tile_images.items()], tile_buttons)
                tile_kinds.append(new_tile)


                print(tiles)
                print(tiles[1])
                print(tiles[1][0])
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for button in tile_buttons:
            button.draw()
        if selectedrect:
            pygame.draw.rect(display, (200, 200, 200), selectedrect, 5)
        draw_tiles(tiles, tile_images, x, y)
        pygame.display.update()

main()