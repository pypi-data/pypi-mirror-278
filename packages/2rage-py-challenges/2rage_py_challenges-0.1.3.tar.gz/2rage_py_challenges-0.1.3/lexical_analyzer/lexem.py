import re
import os
from colorama import Fore

# Функция для генерации input.txt
def generate_input_file(file_path):
    content = """\
    // This is a single line comment
    /* This is a 
       multi-line comment */
    int main() {
        int x = 10;
        if (x >= 10) {
            x = x + 1;
        } else {
            x = x - 1;
        }
        return x;
    }
    """
    with open(file_path, 'w') as file:
        file.write(content)


# Ключевые слова и операторы языка
KEYWORDS = {"if", "else", "while", "return"}
OPERATORS = {"+", "-", "*", "/", "=", "==", "!=", "<", ">", "<=", ">="}
DELIMITERS = {"(", ")", "{", "}", ";", ","}

# Функция для чтения файла
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Функция для определения типа лексемы
def get_token_type(token):
    if token in KEYWORDS:
        return f"{Fore.GREEN}Ключевое слово{Fore.RESET}"
    elif token in OPERATORS:
        return f"{Fore.CYAN}Оператор{Fore.RESET}"
    elif token in DELIMITERS:
        return f"{Fore.RED}Разделитель{Fore.RESET}"
    elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]{0,31}', token):
        return "Переменная"
    elif re.fullmatch(r'\d+', token):
        return f"{Fore.LIGHTYELLOW_EX}Целочисленный_литерал{Fore.RESET}"
    elif re.fullmatch(r'"[^"\n]{0,31}"', token):
        return f"Строковый_литерал"
    else:
        return "UNKNOWN"

# Лексический анализатор
def lexical_analysis(text):
    # Убираем комментарии
    text = re.sub(r'//.*|/\*[\s\S]*?\*/', '', text)
    
    # Разделяем текст на лексемы
    tokens = re.findall(r'\w+|".*?"|<=|>=|==|!=|[^\s\w]', text)
    
    # Таблица лексем
    token_table = []
    for token in tokens:
        token_type = get_token_type(token)
        token_table.append((token, token_type))
        
    return token_table

# Главная функция
def main():
    file_path = os.path.abspath("input.txt")  # Путь к входному файлу
    
    if not os.path.exists(file_path):
        print(f"Файл {file_path} отсутствует. Генерируем input.txt...")
        generate_input_file(file_path)

    print(f"\nВыполняется чтение из файла: {file_path}\n")
    
    try:
        text = read_file(file_path)
        token_table = lexical_analysis(text)
        
        # Вывод таблицы лексем
        print("Таблица Токенов:")
        for token, token_type in token_table:
            print(f"{token} -> {token_type}")
        
        # Проверка на ошибки (например, неизвестные лексемы)
        for token, token_type in token_table:
            if token_type == "UNKNOWN":
                print(f"Ошибка: Неизвестный токен '{token}'")
    except FileNotFoundError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
