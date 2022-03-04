import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import tkinter as tk
from tkinter.ttk import *
from tkinter import simpledialog, TOP, END
import re
from tkinter.filedialog import askopenfile
from assembly import Assembly


class pdf_reader():

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('600x300')
        self.root.title('PDF Splitter')
        self.assemblies = []
        self.job_name = ''
        btn = Button(self.root, text='Load New File', command=self.open_file)
        btn.pack(side=TOP, pady=10)
        btn2 = Button(self.root, text='Skip', command=self.close_window)
        btn2.pack(side=TOP, pady=10)
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

            if not os.path.exists(f'{path}/Build_Sheets'):
                os.makedirs(f'{path}/Build_Sheets')

            pdf = PdfFileReader(file_selected)

            for i in range(pdf.getNumPages()):
                page = pdf.getPage(pageNumber=i)
                text = page.extractText()
                lines = text.splitlines()

                # params for assembly
                number = 0
                case = 0
                hardware = -1
                euro = -1
                left_end = -1
                right_end = -1
                light_panel = -1
                single_door = -1
                pair_door = -1
                false_front = -1
                drw_front = -1
                garbage = -1

                # extract data from PDF for assembly params
                for line in lines:

                    # job name
                    name = re.match(r'Job:([a-zA-Z])+', line)
                    if name != None:
                        split = name.group(0).split(':')
                        self.job_name = split[1]

                    # assmebly number
                    assembly = re.match(r'Assembly.#([0-9])+', line)
                    if assembly != None:
                        split = assembly.group(0).split('#')
                        number = split[1]

                    # euro
                    euro_type = re.match(r'EURO=([0-9])+', line)
                    if euro_type != None:
                        split = euro_type.group(0).split('=')[1]
                        if split == '0':                          
                            euro = 0

                    # left end type
                    lend = re.match(r'LEND=([a-zA-Z])+', line)
                    if lend != None:
                        split = lend.group(0).split('=')[1]
                        if split != "Unfinished":
                            left_end = 0

                    # right end type
                    rend = re.match(r'REND=([a-zA-Z])+', line)
                    if rend != None:
                        split = rend.group(0).split('=')[1]
                        if split != "Unfinished":
                            right_end = 0

                    # light panel
                    light = re.match(r'LIGHTRAIL=([0-9])+', line)
                    if light != None:
                        split = light.group(0).split('=')[1]
                        if split == "1":
                            light_panel = 0

                    # single door
                    s_door = re.match(r'SINGLE_DOOR=([a-zA-Z0-9])+', line)
                    if s_door != None:
                        split = s_door.group(0).split('=')[1]
                        if split != "0":
                            single_door = 0
                            hardware = 0

                    # pair door
                    p_door = re.match(r'PAIR_DOOR=([a-zA-Z0-9])+', line)
                    if p_door != None:
                        split = p_door.group(0).split('=')[1]
                        if split != "0":
                            pair_door = 0
                            hardware = 0

                     # false front
                    f_front = re.match(r'FALSE_FRONT=([a-zA-Z0-9])+', line)
                    if f_front != None:
                        split = f_front.group(0).split('=')[1]
                        if split != "0":
                            false_front = 0

                    # drw front
                    d_front = re.match(r'DRW_FRONT=([a-zA-Z0-9])+', line)
                    if d_front != None:
                        split = d_front.group(0).split('=')[1]
                        if split != "0":
                            drw_front = 0
                            hardware = 0

                    # garbage
                    g_front = re.match(r'GARBAGE_FRONT=([a-zA-Z0-9])+', line)
                    if g_front != None:
                        split = g_front.group(0).split('=')[1]
                        if split != "0":
                            garbage = 0
                            hardware = 0

                assembly = Assembly(
                    name, number, case, hardware, euro, left_end, right_end, light_panel, pair_door, single_door, drw_front, false_front, garbage)

                self.assemblies.append(assembly)

                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(i))
                file_path = f'{os.getcwd()}/static/Build_Sheets/{self.job_name}'
                output_filename = f'{file_path}/{number}.pdf'

                if not os.path.exists(file_path):
                    os.makedirs(f'{file_path}')

                # add number and link to list
                ordered_pairs.append((number, f'{number}.pdf'))

                # write PDF page file
                with open(f'{output_filename}', 'wb') as out:
                    pdf_writer.write(out)

                print('Created: {}'.format(output_filename))
                self.write_status()
            file.close()

    def write_status(self):
        ######## write status file #########
        with open(f'{os.getcwd()}/static/Build_Sheets/{self.job_name}/{self.job_name}-status.txt', 'w') as w:
            w.write(self.job_name + '\n')
            for assembly in self.assemblies:
                w.write(str(assembly._number))
                status = assembly.get_assembly_status()
                for stat in status:
                    w.write(',' + str(stat))

                w.write('\n')
            w.close()

    def close_window(self):
        self.root.destroy()


#p = pdf_reader()
# p.write_status()
# p.close_window()
