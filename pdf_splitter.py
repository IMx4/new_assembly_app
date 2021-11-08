import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
from tkinter.ttk import *
from tkinter import simpledialog, TOP, END
import re

# importing askopenfile function
# from class filedialog
from tkinter.filedialog import askopenfile


root = tk.Tk()
root.geometry('600x300')
root.title('PDF Splitter')


def open_file():
    ordered_pairs = []

    file = askopenfile(mode='r', filetypes=[
        ('PDF Files', '*.pdf')])

    file_selected = file.name
    path = os.path.dirname(file.name)

    if file is not None:

        os.makedirs(f'{path}/Build_Sheets')

        pdf = PdfFileReader(file_selected)

        for i in range(pdf.getNumPages()):
            page = pdf.getPage(pageNumber=i)
            text = page.extractText()
            lines = text.splitlines()
            number = 0
            for line in lines:
                assembly = re.match(r'Assembly.#([0-9])+', line)
                if assembly != None:
                    split = assembly.group(0).split('#')
                    number = split[1]
                    break

            pdf_writer = PdfFileWriter()
            pdf_writer.addPage(pdf.getPage(i))

            output_filename = f'{path}/Build_Sheets/{number}.pdf'

            # add number and link to list
            ordered_pairs.append((number, f'{number}.pdf'))

            with open(f'{output_filename}', 'wb') as out:
                pdf_writer.write(out)

            print('Created: {}'.format(output_filename))

        file.close()


#btn = Button(root, text='Open File', command=lambda: open_file())
btn = Button(root, text='Open File', command=open_file)
btn.pack(side=TOP, pady=10)
t = tk.Text(root, height=15, width=500)
t.pack()
t.insert(END, 'Creating PDF Files\n')

root.mainloop()
