import os
import time
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import Treeview
import shutil
from PIL import Image, ImageTk

def get_icon(path):
    if os.path.isdir(path):
        return folder_icon
    else:
        return file_icon

def get_file_info(path):
    size = os.path.getsize(path) if os.path.isfile(path)  else "-"
    modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(path)))
    created = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(path)))
    file_type = "Папка" if os.path.isdir(path) else "Файл"
    return size, modified, created, file_type


def create_item_window():
    def create_item():
        item_name = entry.get().strip()
        if not item_name:
            messagebox.showwarning("Ошибка", "Имя не может быть пустым.")
            return

        item_path = os.path.join(current_dir, item_name)

        try:
            if var.get() == 'folder':
                if not os.path.exists(item_path):
                    os.mkdir(item_path)
                else:
                    messagebox.showwarning("Ошибка", "Папка с таким именем уже существует.")
            else:
                if not os.path.exists(item_path):
                    open(item_path, 'w').close()
                else:
                    messagebox.showwarning("Ошибка", "Файл с таким именем уже существует.")
            refresh_treeview()
            create_window.destroy()
        except PermissionError:
            messagebox.showerror("Ошибка", "Недостаточно прав для создания объекта.")

    create_window = Toplevel(root)
    create_window.title("Создать новый элемент")
    create_window.geometry("300x150")
    create_window.resizable(False, False)

    Label(create_window, text="Имя файла или папки:").pack(pady=5)
    entry = Entry(create_window)
    entry.pack(pady=5)

    var = StringVar(value='file')
    Radiobutton(create_window, text="Файл", variable=var, value='file').pack(anchor=W)
    Radiobutton(create_window, text="Папка", variable=var, value='folder').pack(anchor=W)

    Button(create_window, text="Создать", command=create_item).pack(pady=10)


def delete_item():
    selected_item = file_tree.selection()
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите элемент для удаления.")
        return

    item_path = file_tree.item(selected_item[0], 'values')[0]

    try:
        if os.path.isfile(item_path):
            os.remove(item_path)
        else:
            shutil.rmtree(item_path)
        refresh_treeview()
        messagebox.showinfo("Успех", "Элемент успешно удален.")
    except PermissionError:
        messagebox.showerror("Ошибка", "Недостаточно прав для удаления.")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось удалить элемент: {e}")


def rename_item():
    selected_item = file_tree.selection()
    if not selected_item:
        messagebox.showwarning("Ошибка", "Выберите элемент для переименования.")
        return

    item_path = file_tree.item(selected_item[0], 'values')[0]

    def rename():
        new_name = rename_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Ошибка", "Имя не может быть пустым.")
            return

        new_path = os.path.join(current_dir, new_name)

        try:
            os.rename(item_path, new_path)
            refresh_treeview()
            rename_window.destroy()
            messagebox.showinfo("Успех", "Элемент успешно переименован.")
        except FileExistsError:
            messagebox.showerror("Ошибка", "Элемент с таким именем уже существует.")
        except PermissionError:
            messagebox.showerror("Ошибка", "Недостаточно прав для переименования.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось переименовать элемент: {e}")

    rename_window = Toplevel(root)
    rename_window.title("Переименовать элемент")
    rename_window.geometry("300x150")
    rename_window.resizable(False, False)

    Label(rename_window, text="Новое имя:").pack(pady=5)
    rename_entry = Entry(rename_window)
    rename_entry.pack(pady=5)

    Button(rename_window, text="Переименовать", command=rename).pack(pady=10)


def open_item(event):
    # Открытие файла или папки
    selected_item = file_tree.selection()
    if selected_item:
        item_path = file_tree.item(selected_item[0], 'values')[0]
        if os.path.isfile(item_path):
            os.startfile(item_path)
        else:
            os.chdir(item_path)
            refresh_treeview()

def go_back():
    # Переход на родительскую директорию
    global current_dir
    current_dir = os.path.dirname(current_dir)
    refresh_treeview()

def refresh_treeview():
    # Обновление содержимого Treeview
    for item in file_tree.get_children():
        file_tree.delete(item)
    for item in os.listdir(current_dir):
        item_path = os.path.join(current_dir, item)
        size, modified, created, file_type = get_file_info(item_path)
        file_tree.insert('', 'end', text=item, image=get_icon(item_path),
                         values=(item_path, file_type, size, modified, created))

root = Tk()
root.title('Файловый менеджер')
root.geometry('1000x600')

current_dir = os.getcwd()

# Загрузка иконок
folder_icon = ImageTk.PhotoImage(Image.open("folder_icon.png").resize((16, 16)))
file_icon = ImageTk.PhotoImage(Image.open("file_icon.png").resize((16, 16)))

# Верхняя панель инструментов
toolbar = Frame(root, bd=1, relief=RAISED)
ttk.Button(toolbar, text='Создать', command=create_item_window).pack(side=LEFT, padx=2, pady=2)
ttk.Button(toolbar, text='Удалить', command=delete_item).pack(side=LEFT, padx=2, pady=2)
ttk.Button(toolbar, text='Переименовать', command=rename_item).pack(side=LEFT, padx=2, pady=2)
ttk.Button(toolbar, text='Назад', command=go_back).pack(side=LEFT, padx=2, pady=2)
toolbar.pack(side=TOP, fill=X)

# Дерево файлов и папок с дополнительными столбцами
file_tree = Treeview(root, columns=('path', 'type', 'size', 'modified', 'created'), show='headings')
file_tree.heading('path', text='Путь')
file_tree.heading('type', text='Тип')
file_tree.heading('size', text='Размер')
file_tree.heading('modified', text='Дата изменения')
file_tree.heading('created', text='Дата создания')
file_tree.column('path', width=300)
file_tree.column('type', width=100)
file_tree.column('size', width=100, anchor='e')
file_tree.column('modified', width=150)
file_tree.column('created', width=150)
file_tree.pack(fill=BOTH, expand=True, padx=10, pady=5)

file_tree.bind('<Double-1>', open_item)

refresh_treeview()
root.mainloop()
