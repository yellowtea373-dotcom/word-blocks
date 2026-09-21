import pygame
from constants import * #all
from block import Block

class Game:
    def __init__(self):
        #Пустые клетки для каждой колонки в строке (список)
        self.field = [[None for _ in range(GRID_COLUMNS)] for _ in range(GRID_ROWS)]

        self.current_block = None
        self.selected_blocks = [] #изначально пустой список выбранных
        self.score = 0
        self.fall_timer = 0 #Управление скоростью падения
        self.game_over = False  #Флаг проигрыша
        self.create_block()     #Первый блок — поле пустое, всегда создаётся

    def create_block(self):
        """Создаёт новый блок сверху. Возвращает False, если места нет."""
        col = GRID_COLUMNS // 2    #Середина верхней строки
        row = 0                    #Верхняя строка

        #Проверка: свободна ли клетка в верхней строке?
        if self.field[row][col] is not None:
            return False    #Место занято — проигрыш

        #Создаём блок
        self.current_block = Block(col, row)
        self.current_block.is_active = True
        return True

    def check_collision(self, block, drow=0, dcol=0): #Смещение по колонкам и рядам
        new_row = block.row + drow
        new_col = block.col + dcol
        #Обработка выхода за границы
        if new_row >= GRID_ROWS or new_col < 0 or new_col >= GRID_COLUMNS:
            return True
        if self.field[new_row][new_col] is not None:
            return True
        return False

    def move_down(self):
        if not self.check_collision(self.current_block, drow=1):
            self.current_block.row += 1
        else:
            #Фиксация на месте
            self.field[self.current_block.row][self.current_block.col] = self.current_block
            self.current_block.is_active = False

            #Пытаемся создать новый блок — если не получилось, игра окончена
            if not self.create_block():
                self.game_over = True
                self.current_block = None

    def move_left_right(self, direction):
        if self.check_collision(self.current_block, dcol=direction):
            return
        #Смещение +1 или -1
        self.current_block.col += direction

    def handle_mouse_click(self, pos):
        col = pos[0] // CELL_SIZE
        row = pos[1] // CELL_SIZE
        if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLUMNS:
            block = self.field[row][col]
            if block is not None and not block.is_active: #Блок не падает
                if not self.selected_blocks: #Список выбранных блоков еще пуст
                    block.is_selected = True
                    self.selected_blocks.append(block)
                else:
                    last_block = self.selected_blocks[-1]
                    #манхэттенское расстояние (смежность по вертикали/горизонтали)
                    is_neighbor = abs(block.col - last_block.col) + abs(block.row - last_block.row) == 1
                    if is_neighbor:
                        block.is_selected = True
                        self.selected_blocks.append(block)
                    else:
                        #Очистка и новая последовательность для слова
                        self.clear_selection()
                        block.is_selected = True
                        self.selected_blocks.append(block)
            else:
                self.clear_selection()

    def clear_selection(self):
        for b in self.selected_blocks:
            b.is_selected = False
        self.selected_blocks = []

    def handle_enter(self):
        #Enter: проверка собранного слова и очистка матрицы
        if not self.selected_blocks:
            return
        word = "".join([b.char for b in self.selected_blocks])

        if word in VALID_WORDS:
            self.score += len(word) * 10
            for b in self.selected_blocks:
                self.field[b.row][b.col] = None #Очистка
            self.selected_blocks = []
            self.apply_gravity() #Падение блоков
        else:
            self.clear_selection()

    def apply_gravity(self): #Гравитация после удаления блоков слова
        for col in range(GRID_COLUMNS):
            blocks_in_col = []
            #старт, стоп, шаг (индекс УВЕЛИЧИВАЕТСЯ ВНИЗ)
            for row in range(GRID_ROWS - 1, -1, -1):
                if self.field[row][col] is not None:
                    #Сохранение обратного порядка
                    #(те, что упали раньше, в массиве остаются раньше)
                    blocks_in_col.append(self.field[row][col])
            for row in range(GRID_ROWS):
                self.field[row][col] = None
            #Расстановка сохраненной последовательности с нижней строки
            new_row = GRID_ROWS - 1
            for block in blocks_in_col:
                self.field[new_row][col] = block
                block.row = new_row
                new_row -= 1 #сдвиг ВВЕРХ

    def draw(self, screen, font):
        screen.fill(COLORS["bg"])  #Фон берём из констант
        #Сетка экрана
        for x in range(0, WINDOW_WIDTH, CELL_SIZE): #старт, стоп, шаг
            #(Линия от верха до низа)
            pygame.draw.line(screen, COLORS["grid"], (x, 0), (x, WINDOW_HEIGHT))

        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
            #(Линия от левого края до правого)
            pygame.draw.line(screen, COLORS["grid"], (0, y), (WINDOW_WIDTH, y))

        for row in range(GRID_ROWS):
            for col in range(GRID_COLUMNS):
                block = self.field[row][col]
                if block is not None:
                    color = COLORS["block"]  #Обычный цвет из констант
                    if block.is_selected:
                        color = COLORS["block_selected"]  #Цвет выделенных
                    #x, y, ширина, высота
                    pygame.draw.rect(screen, color, (col * CELL_SIZE + 2, row * CELL_SIZE + 2,
                                                     CELL_SIZE - 4, CELL_SIZE - 4))

                    text = font.render(block.char, True, (0, 0, 0)) #Буква в графику, True – сглаживание
                    screen.blit(text, (col * CELL_SIZE + 10, row * CELL_SIZE + 10)) #Текст поверх игрового экрана

        #Отрисовка падающего блока
        if self.current_block:
            color = COLORS["active_block"]  #Кораллово-розовый из констант
            pygame.draw.rect(screen, color, (self.current_block.col * CELL_SIZE + 2,
                                             self.current_block.row * CELL_SIZE + 2,
                                             CELL_SIZE - 4, CELL_SIZE - 4))
            text = font.render(self.current_block.char, True, (0, 0, 0))
            screen.blit(text, (self.current_block.col * CELL_SIZE + 10,
                               self.current_block.row * CELL_SIZE + 10))

        #Слово и счет
        #Сбор слова: извлечение одной буквы из каждого блока b в массиве, добавление к слову
        current_word = "".join([b.char for b in self.selected_blocks])
        score_text = font.render(f"Word: {current_word} | Score: {self.score}", True, COLORS["text"])
        screen.blit(score_text, (10, 10))