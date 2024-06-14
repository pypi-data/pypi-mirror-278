import os
import platform
import requests

def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def main():
    while True:
        clear_console()  # Очистка консоли в зависимости от операционной системы
        print("Made by Avinion")
        print("Telegram: @akrim\n")

        file_input = input("Введите URL аудиофайла или локальный путь к файлу: ")
        is_url = False
        if file_input.startswith('http://') or file_input.startswith('https://'):
            is_url = True

        if is_url:
            url = file_input
            file_data = None
            file_name = None
        else:
            if os.path.isfile(file_input):  # Проверяем, является ли введенный путь файлом
                with open(file_input, 'rb') as file:
                    file_data = file.read()
                file_name = os.path.basename(file_input)
                url = None
            else:
                print("Введенная строка не является URL или локальным путем к файлу.")
                continue  # Переходим к следующей итерации цикла

        services = input("Введите список сервисов для возврата (через запятую): ")
        api_token = '6db1fa57104af98adf3bea41916eabcd' # Обновите токен API

        data = {
            'api_token': api_token,
            'return': services
        }

        if url:
            data['url'] = url
            result = requests.post('https://api.audd.io/', data=data).json()
        else:
            files = {'file': (file_name, file_data)}
            result = requests.post('https://api.audd.io/', data=data, files=files).json()

        if 'result' in result:
            output = "\nРезультат распознавания:\n"
            for key, value in result['result'].items():
                output += f"{key.capitalize()}: {value}\n"
        else:
            output = "\nОшибка распознавания:\n"
            output += f"Код ошибки: {result['error']['error_code']}\n"
            output += f"Сообщение об ошибке: {result['error']['error_message']}\n"
            if 'warning' in result:
                output += f"Предупреждение: {result['warning']['error_message']}\n"

        # Сохранение результата в файл
        save_option = input("Хотите ли вы сохранить результат в текстовый файл? (y/n): ").lower()
        if save_option == 'y':
            file_name = input("Введите имя файла для сохранения: ")
            with open(f"{file_name}.txt", 'w') as file:
                file.write(output)
                print(f"Результат сохранен в файле {file_name}.txt")
        else:
            print(output)

        # Запрос на продолжение работы
        continue_option = input("Хотите продолжить работу? (Y/N): ").lower()
        if continue_option != 'y':
            break  # Выход из цикла при ответе отличном от 'y'

if __name__ == "__main__":
    main()
