import pygame 
import sys   #Выход из программы Rename-Item -Path "README.md.txt" -NewName "README.md"
from constants import *   
from game import Game

def show_menu(screen, font):
    screen.fill(COLORS["bg"])
    title = font.render("WORD BLOCKS", True, COLORS["text"])
    subtitle = font.render("ENTER for start",True, COLORS["text"]) 
    #Заголовок и подсказка

    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//2-50))
    screen.blit(subtitle, (WINDOW_WIDTH//2 - subtitle.get_width()//2, WINDOW_HEIGHT//2))
    #Центрирование: середина ширины окна - середина ширины текста, середина высоты окна

    pygame.display.flip()

def show_game_over(screen, font, score):
    screen.fill(COLORS["bg"])
    title = font.render("GAME IS OVER", True, COLORS["game_over"])
    score_text = font.render(f"Score: {score}", True, COLORS["text"])
    screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, WINDOW_HEIGHT//2-50))
    screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, WINDOW_HEIGHT//2))
    pygame.display.flip()

def main():
    #Инициализация Pygame и шрифты
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  #Игровое окно
    pygame.display.set_caption("WORD BLOCKS")

    clock = pygame.time.Clock() #Контроль частоты кадров
    font = pygame.font.SysFont("Consolas", 30)
    big_font = pygame.font.SysFont("Consolas", 52)

    state = STATE_MENU  #начальное сосстояние

    game = Game()  #(поле, счет, текущий блок)
    while True:
        dt = clock.tick(FPS) #время с прошлого кадра
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if state == STATE_MENU and event.key == pygame.K_SPACE:
                    state = STATE_PLAY  #Запуск, если пробел в начале игры
                elif state == STATE_PLAY:
                    if event.key == pygame.K_LEFT:
                        game.move_left_right(-1)
                    elif event.key == pygame.K_RIGHT:
                        game.move_left_right(1)
                    elif event.key == pygame.K_DOWN:
                        game.move_down()
                    elif event.key == pygame.K_RETURN:
                        game.handle_enter() #Проверка собранного слова

            if event.type == pygame.MOUSEBUTTONDOWN and state == STATE_PLAY:
                game.handle_mouse_click(event.pos)

        if state == STATE_PLAY:
            game.fall_timer += dt #Накопление времени
            if game.fall_timer>=FALL_SPEED:
                game.move_down()
                game.fall_timer = 0

            #Проверка: если поле заполнено — переход на экран проигрыша
            if game.game_over:
                state = STATE_OVER

        if state == STATE_MENU:
            show_menu(screen, big_font)
        elif state == STATE_PLAY:
            game.draw(screen, font) #поле, блоки, счет
        elif state == STATE_OVER:
            show_game_over(screen, big_font, game.score)
        pygame.display.flip()

if __name__ == "__main__":
    main()
    #Точка входа: прямой запуск файла (не модуль)