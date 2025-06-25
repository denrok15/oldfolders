# 🗂️ Файловый менеджер на Python с Tkinter

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Tkinter](https://img.shields.io/badge/Tkinter-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)

Простой файловый менеджер с графическим интерфейсом, написанный на Python с использованием Tkinter.

## 📋 Возможности

- **Просмотр файловой системы** с иконками
- **Создание** файлов и папок
- **Удаление** файлов и папок
- **Переименование** элементов
- **Навигация** (кнопка "Назад")
- **Информация о файлах**:
- 
  - Тип (файл/папка)
  - Размер
  - Дата создания
  - Дата изменения
- Двойной клик для **открытия** файлов/папок

## 🛠️ Требования

- Python 3.x
- Установите зависимости:
  ```bash
  pip install pillow
🚀 Установка
Клонируйте репозиторий:

bash
git clone https://github.com/ваш_username/python-file-manager.git
cd python-file-manager

bash
Добавьте иконки:
Поместите folder_icon.png и file_icon.png в папку проекта
Или измените пути к иконкам в коде

🖥️ Использование

Запустите приложение:

bash

python file_manager.py

Управление:


🆕 Создать - Новая папка/файл


🗑️ Удалить - Удалить выбранное


✏️ Переименовать - Изменить имя


🔙 Назад - В родительскую папку


Двойной клик - Открыть файл/папку


📂 Структура проекта
text
python-file-manager/
├── file_manager.py      # Основной код
├── folder_icon.png      # Иконка папки
├── file_icon.png        # Иконка файла
└── README.md            # Этот файл
