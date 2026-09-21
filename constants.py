#Константы
WINDOW_WIDTH = 800       #было 800 — теперь сетка занимает всю ширину
WINDOW_HEIGHT = 600
CELL_SIZE = 40

#Игровое поле  python main.py
GRID_COLUMNS = 20 
GRID_ROWS = 15

FPS = 60    #кадры
FALL_SPEED = 900    #миллисекунды

#Словарь
VALID_WORDS = {"GO", "NO", "CAT", "DOG", "TOP", "BAG", "RED", "TEN", "BAD", 
             "HAT", "HAG", "SAD", "BAR", "RAB", "HIT", "LOL", "BOLL", "BOW", 
             "SOS", "LOW", "WOW", "ROW", "POP", "BOT", "BIN", "BOSS", "BOB",  
             }

COLORS = {
    "bg": (64, 42, 28),              #тёмно-коричневый фон
    "grid": (110, 85, 65),           #линии сетки
    "block": (240, 220, 180),        #бежевый
    "block_selected": (255, 255, 0), #жёлтый (выделенные)
    "active_block": (245, 130, 140), #розовый (падающий)
    "text": (255, 255, 255),         #белый текст
    "game_over": (255, 0, 0),        #красный (экран проигрыша)
}

#Состояния
STATE_MENU = "MENU"
STATE_PLAY = "PLAY"
STATE_OVER = "OVER"

LETTER_FREQUENCY = {}                 #Пустой словарь: {буква: сколько раз}
for word in VALID_WORDS:              #Перебираем все слова
    for ch in word:                   #Перебираем все буквы в слове
        LETTER_FREQUENCY[ch] = LETTER_FREQUENCY.get(ch, 0) + 1
        #получает букву (или по умолчанию 0) и увеличивает счетчик


VOWEL_BOOST = 1.5         #Частота класных
VOWELS = "AEIOU"        #Список гласных латинского алфавита

LETTERS_POOL = ""                              #начало с пустой строки
for ch, count in LETTER_FREQUENCY.items():     #Перебираем все буквы и их частоты
#items() возвращает пары: ключ ch, число count из словаря LETTER_FREQUENCY
    LETTERS_POOL += ch * count                 #Основной вес буквы
    if ch in VOWELS:                           
        LETTERS_POOL += ch * round(count * VOWEL_BOOST)   #добавляем вес, если гласная

#Буква повторяется так часто, как встречается в словаре:
#создание строки из count копий буквы