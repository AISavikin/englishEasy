import random
import string
from typing import List, Tuple, Dict, Set


def calculate_grid_size(words: List[str]) -> int:
    """
    Автоматически рассчитывает оптимальный размер сетки на основе слов.

    Args:
        words: Список английских слов

    Returns:
        int: Оптимальный размер сетки
    """
    if not words:
        return 10  # минимальный размер по умолчанию

    # Параметры для расчета
    max_word_length = max(len(word) for word in words)
    word_count = len(words)
    total_letters = sum(len(word) for word in words)

    # Базовый расчет на основе самой длинного слова
    base_size = max(max_word_length + 2, 8)  # +2 для отступов, минимум 8

    # Учитываем количество слов
    if word_count > 10:
        base_size += 2
    if word_count > 20:
        base_size += 3
    if word_count > 30:
        base_size += 2

    # Учитываем общее количество букв
    density_factor = total_letters / (base_size ** 2)
    if density_factor > 0.25:  # слишком плотно
        base_size = int(base_size * 1.2)

    # Ограничиваем диапазоном
    min_size = 8
    max_size = 25

    # Особые случаи
    if max_word_length > 15:
        base_size = max(base_size, max_word_length + 3)

    # Округляем до ближайшего нечетного числа (для центрирования)
    base_size = int(base_size)
    if base_size % 2 == 0:
        base_size += 1

    # Применяем ограничения
    return max(min_size, min(base_size, max_size))

def generate_letter_soup(words: List[str], grid_size = None) -> Tuple[List[List[str]], List[Dict]]:
    """
    Генерирует буквенный суп (сетку с словами).

    Args:
        words: Список английских слов
        grid_size: Размер сетки (grid_size x grid_size)

    Returns:
        Tuple[grid, placed_words]:
            grid: Двумерный список букв
            placed_words: Информация о размещенных словах
    """
    if grid_size is None:
        grid_size = calculate_grid_size(words)

    # Инициализируем пустую сетку
    grid = [['' for _ in range(grid_size)] for _ in range(grid_size)]

    # Преобразуем слова в верхний регистр
    words_upper = [word.upper() for word in words]

    # Сортируем слова по длине (от самых длинных к самым коротким)
    words_upper.sort(key=len, reverse=True)

    placed_words = []

    # Преобразуем слова в верхний регистр
    words = [word.upper() for word in words]

    # Сортируем слова по длине (от самых длинных к самым коротким)
    words.sort(key=len, reverse=True)

    for word in words:
        placed = False
        attempts = 0
        max_attempts = 100

        while not placed and attempts < max_attempts:
            attempts += 1

            # Выбираем случайное направление: горизонтальное или вертикальное
            direction = random.choice(['horizontal', 'vertical'])

            if direction == 'horizontal':
                # Для горизонтального слова
                max_row = grid_size
                max_col = grid_size - len(word) + 1
                if max_col <= 0:
                    continue  # Слово слишком длинное

                row = random.randint(0, max_row - 1)
                col = random.randint(0, max_col - 1)

                # Проверяем, можно ли разместить слово
                can_place = True
                for i, letter in enumerate(word):
                    current_cell = grid[row][col + i]
                    if current_cell != '' and current_cell != letter:
                        can_place = False
                        break

                if can_place:
                    # Размещаем слово
                    for i, letter in enumerate(word):
                        grid[row][col + i] = letter

                    placed_words.append({
                        'word': word,
                        'row': row,
                        'col': col,
                        'direction': direction,
                        'length': len(word)
                    })
                    placed = True

            else:  # vertical
                # Для вертикального слова
                max_row = grid_size - len(word) + 1
                max_col = grid_size
                if max_row <= 0:
                    continue  # Слово слишком длинное

                row = random.randint(0, max_row - 1)
                col = random.randint(0, max_col - 1)

                # Проверяем, можно ли разместить слово
                can_place = True
                for i, letter in enumerate(word):
                    current_cell = grid[row + i][col]
                    if current_cell != '' and current_cell != letter:
                        can_place = False
                        break

                if can_place:
                    # Размещаем слово
                    for i, letter in enumerate(word):
                        grid[row + i][col] = letter

                    placed_words.append({
                        'word': word,
                        'row': row,
                        'col': col,
                        'direction': direction,
                        'length': len(word)
                    })
                    placed = True

        if not placed:
            print(f"Не удалось разместить слово: {word}")

    # Заполняем пустые клетки случайными буквами
    for i in range(grid_size):
        for j in range(grid_size):
            if grid[i][j] == '':
                grid[i][j] = random.choice(string.ascii_uppercase)

    return grid, placed_words


def validate_word_in_grid(word: str, grid: List[List[str]], placed_words: List[Dict]) -> bool:
    """
    Проверяет, есть ли слово в сетке.

    Args:
        word: Слово для проверки (в верхнем регистре)
        grid: Сетка букв
        placed_words: Информация о размещенных словах

    Returns:
        True если слово есть в сетке, иначе False
    """
    word = word.upper()

    # Проверяем по списку размещенных слов
    for placed_word in placed_words:
        if placed_word['word'] == word:
            return True

    # Также проверяем, можно ли найти слово в сетке (на случай, если алгоритм размещения не записал его)
    grid_size = len(grid)

    # Проверяем горизонтально
    for i in range(grid_size):
        for j in range(grid_size - len(word) + 1):
            found = True
            for k in range(len(word)):
                if grid[i][j + k] != word[k]:
                    found = False
                    break
            if found:
                return True

    # Проверяем вертикально
    for i in range(grid_size - len(word) + 1):
        for j in range(grid_size):
            found = True
            for k in range(len(word)):
                if grid[i + k][j] != word[k]:
                    found = False
                    break
            if found:
                return True

    return False


def get_grid_preview(grid: List[List[str]]) -> str:
    """
    Возвращает текстовое представление сетки.
    """
    return '\n'.join([' '.join(row) for row in grid])