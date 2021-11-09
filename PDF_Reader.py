import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
from tkinter.ttk import *
from tkinter import simpledialog, TOP, END
import re
from tkinter.filedialog import askopenfile


class pdf_reader():

    def __init__(self, data_store):
        self.root = tk.Tk()
        self.root.geometry('600x300')
        self.root.title('PDF Splitter')
        self.data_store = data_store
        btn = Button(self.root, text='Open File', command=self.open_file)
        btn.pack(side=TOP, pady=10)
        t = tk.Text(self.root, height=15, width=500)
        t.pack()
        t.insert(END, 'Creating PDF Files\n')

        self.root.mainloop()

    def open_file(self):
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

                # params for assembly
                number = 0
                euro = 0
                left_end = False
                right_end = False
                light_panel = False

                # extract data from PDF for assembly params
                for line in lines:

                    # assmebly number
                    assembly = re.match(r'Assembly.#([0-9])+', line)
                    if assembly != None:
                        split = assembly.group(0).split('#')
                        number = split[1]

                    # euro
                    euro_type = re.match(r'LEND=([a-zA-Z])+', line)
                    if euro_type != None:
                        euro = euro_type.group(0).split('=')

                    # left end type
                    lend = re.match(r'LEND=([a-zA-Z])+', line)
                    if lend != None:
                        split = lend.group(0).split('=')
                        if split != "Unfinished":
                            left_end = True

                    # right end type
                    rend = re.match(r'REND=([a-zA-Z])+', line)
                    if rend != None:
                        split = rend.group(0).split('=')
                        if split != "Unfinished":
                            right_end = True

                    # light panel
                    light = re.match(r'LIGHTRAIL=([a-zA-Z0-9])+', line)
                    if light != None:
                        split = light.group(0).split('=')
                        if split == "1":
                            light_panel = True

                    self.data_store.create_assembly(
                        number, euro, left_end, right_end, light_panel)

                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(i))
                output_filename = f'{os.getcwd()}/static/Build_Sheets/{number}.pdf'

                # add number and link to list
                ordered_pairs.append((number, f'{number}.pdf'))

                # write PDF page file
                with open(f'{output_filename}', 'wb') as out:
                    pdf_writer.write(out)

                print('Created: {}'.format(output_filename))

            file.close()
