import os
from pathlib import Path
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import argparse
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as messagebox

blocklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script']

def select_file():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("EPUB files", "*.epub")])  # Only show EPUB files
    return file_path


def add_file_to_json(filename, dest):
    book = epub.read_epub(filename)
    book_name = Path(filename).stem

    output_path = os.path.join(dest, book_name +'.txt')

    with open(output_path, 'w+', encoding='utf-8') as f:
        chapters = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                chapters.append(item.get_content())

        for chapter in chapters:
            text = chapter_to_text(chapter)
            f.write(text+'\n')

    messagebox.showinfo("Success", f"File was successfully saved at {output_path}")

def chapter_to_text(chap):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(string=True)  # Use 'string' instead of 'text'
    prev = ''
    for t in text:
        if t.parent.name not in blocklist:
            if not t.isspace():
                if not (str(prev).endswith(' ') or str(t).startswith(' ')):
                    output += '\n\n'
                output += '{}'.format(t)
            prev = t
    return output

def main():
    file_path = select_file()
    if file_path:
        print(f"Selected file: {file_path}")
        add_file_to_json(file_path, '.')
    else:
        print("No file selected.")

if __name__ == '__main__':
    main()


# import os
# from pathlib import Path
# import ebooklib
# from ebooklib import epub
# from bs4 import BeautifulSoup
# import argparse

# # https://medium.com/@zazazakaria18/turn-your-ebook-to-text-with-python-in-seconds-2a1e42804913
# blocklist = ['[document]', 'noscript', 'header', 'html', 'meta', 'head', 'input', 'script']

# def main():
#     parser = argparse.ArgumentParser(description='Convert epub to txt',
#             formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#     parser.add_argument('-f', '--files', action='append', help='epub file')
#     parser.add_argument('-s', '--src', action='store', help='Source location')
#     parser.add_argument('-d', '--dest', action='store',  help='Destination location')
#     args = parser.parse_args()

#     files = args.files
#     if files == None:
#         print('Must provide file')
#         quit()
#     src = args.src
#     if src == None:
#         src = ''
#     dest = args.dest
#     if dest == None:
#         dest = '.'

#     for file_name in args.files:
#         file_path = os.path.join(src, file_name)
#         add_file_to_json(file_path, dest)


# def add_file_to_json(filename, dest):
#     book = epub.read_epub(filename)
#     book_name = Path(filename).stem

#     output_path = os.path.join(dest, book_name +'.txt')

#     with open(output_path, 'w+', encoding='utf-8') as f:
#         chapters = []
#         for item in book.get_items():
#             if item.get_type() == ebooklib.ITEM_DOCUMENT:
#                 chapters.append(item.get_content())

#         for chapter in chapters:
#             text = chapter_to_text(chapter)
#             f.write(text+'\n')

# def chapter_to_text(chap):
#     output = ''
#     soup = BeautifulSoup(chap, 'html.parser')
#     text = soup.find_all(text=True)
#     prev = ''
#     for t in text:
#         if t.parent.name not in blocklist:
#             if not t.isspace():
#                 if not (str(prev).endswith(' ') or str(t).startswith(' ')):
#                     output += '\n\n'
#                 output += '{}'.format(t)
#             prev = t
#     return output

# import tkinter as tk
# from tkinter import filedialog

# def select_file():
#     root = tk.Tk()
#     root.withdraw()  # Hide the main window
#     file_path = filedialog.askopenfilename()  # Open the file dialog
#     return file_path

# def main():
#     file_path = select_file()
#     print(f"Selected file: {file_path}")

# if __name__ == '__main__':
#     main()