import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import re
from . import assembly


class FileData():

    def __init__(self):
        self.job_name = ''
        self.lines = {}
        self.assemblies = []

    def read_file(self):
        # open persistance file and check status
        # file_path = os.path.dirname +
        with open(os.getcwd() + '/static/Build_Sheets/export.txt', 'r+', encoding='utf-16') as persistance:

            self.job_name = persistance.readline().strip()
            for line in persistance:
                split = line.rstrip().split(' ,')
                self.lines[split[0]] = split[1:]

    def file_lines(self):
        return self.lines

    def write_file(self, assemblies):
        with open(os.getcwd() + '/static/Build_Sheets/export.txt', 'w', encoding='utf-16') as persistance:
            persistance.write(self.job_name + '\n')
            for assembly in assemblies:
                status_string = ''.join(map(str, assembly.status))
                persistance.write(
                    f'{assembly.number} ,{assembly.face_type} ,{assembly.l_end} ,{assembly.r_end} ,{status_string} \n')

    def create_assembly(self, num, euro, left, right, light):

        self.assemblies.append(assembly(num, euro, left, right, light))

    # def split_pdf(self):

    #     ordered_pairs = []

    #     pdf = PdfFileReader(os.getcwd() + "/static/Build_Sheets/BS.pdf")
    #     if pdf is not None:

    #         for i in range(pdf.getNumPages()):
    #             page = pdf.getPage(pageNumber=i)
    #             text = page.extractText()
    #             lines = text.splitlines()

    #             # params for assembly
    #             number = 0
    #             euro = 0
    #             left_end = False
    #             right_end = False
    #             light_panel = False

    #             # extract data from PDF for assembly params
    #             for line in lines:

    #                 # assmebly number
    #                 assembly = re.match(r'Assembly.#([0-9])+', line)
    #                 if assembly != None:
    #                     split = assembly.group(0).split('#')
    #                     number = split[1]

    #                 # euro
    #                 euro_type = re.match(r'LEND=([a-zA-Z])+', line)
    #                 if euro_type != None:
    #                     euro = euro_type.group(0).split('=')

    #                 # left end type
    #                 lend = re.match(r'LEND=([a-zA-Z])+', line)
    #                 if lend != None:
    #                     split = lend.group(0).split('=')
    #                     if split != "Unfinished":
    #                         left_end = True

    #                 # right end type
    #                 rend = re.match(r'REND=([a-zA-Z])+', line)
    #                 if rend != None:
    #                     split = rend.group(0).split('=')
    #                     if split != "Unfinished":
    #                         right_end = True

    #                 # light panel
    #                 light = re.match(r'LIGHTRAIL=([a-zA-Z0-9])+', line)
    #                 if light != None:
    #                     split = light.group(0).split('=')
    #                     if split == "1":
    #                         light_panel = True

    #                 self.create_assembly(
    #                     number, euro, left_end, right_end, light_panel)

    #             pdf_writer = PdfFileWriter()
    #             pdf_writer.addPage(pdf.getPage(i))
    #             output_filename = f'{os.getcwd()}/static/Build_Sheets/{number}.pdf'

    #             # add number and link to list
    #             ordered_pairs.append((number, f'{number}.pdf'))

    #             # write PDF page file
    #             with open(f'{output_filename}', 'wb') as out:
    #                 pdf_writer.write(out)

    #             print('Created: {}'.format(output_filename))
