import time
import random
import string
from colorama import Fore
from collections import defaultdict
from search_methods.scripts.lineare_probing_hash_table import LinearProbingHashTable
from search_methods.scripts.tree_node import TreeNode, BinarySearchTree

# Генерация случайных строк
def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

# Замер времени выполнения
def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, end_time - start_time
    return wrapper

@measure_time
def insert_into_table(table, elements):
    for key, value in elements:
        table.insert(key, value)

@measure_time
def search_in_table(table, keys):
    for key in keys:
        table.search(key)

# Основная функция для проведения анализа
def main():
    sizes = [45, 90, 223, 300]  # Разные размеры данных
    for size in sizes:
        print(f"Размер данных: {size}")
        
        # Генерация случайных данных
        elements = [(generate_random_string(), random.randint(1, 1000)) for _ in range(size)]
        keys = [key for key, _ in elements]
        
        # Простое рехеширование
        lp_table = LinearProbingHashTable(size * 2)  # Увеличенный размер таблицы для уменьшения числа коллизий
        _, insert_time_lp = insert_into_table(lp_table, elements)
        _, search_time_lp = search_in_table(lp_table, keys)
        
        # Бинарное дерево
        bst = BinarySearchTree()
        _, insert_time_bst = insert_into_table(bst, elements)
        _, search_time_bst = search_in_table(bst, keys)
        
        print(f"{Fore.LIGHTMAGENTA_EX}Простое рехеширование{Fore.RESET} - Вставка: {insert_time_lp:.6f} с, Поиск: {search_time_lp:.6f} с")
        print(f"{Fore.LIGHTGREEN_EX}Бинарное дерево{Fore.RESET} - Вставка: {insert_time_bst:.6f} с, Поиск: {search_time_bst:.6f} с")
        print()

if __name__ == "__main__":
    main()