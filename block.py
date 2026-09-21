import random
import pygame
from constants import CELL_SIZE, LETTERS_POOL  

class Block:
    """Объект со строковой переменной и координатами матрицы"""
    def __init__(self, col, row, char=None):
        self.col = col
        self.row = row
        #Буква: если не передана — берём из LETTERS_POOL (гласные чаще)
        self.char = char if char else random.choice(LETTERS_POOL)
        self.is_active = False
        self.is_selected = False

    def get_rect(self):
        return pygame.Rect( #Прямоугольник отрисовки
            self.col * CELL_SIZE,
            self.row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
            )