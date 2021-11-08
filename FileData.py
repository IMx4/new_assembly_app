import os
from PyPDF2 import PdfFileReader, PdfFileWriter
import re


class FileData():

    def __init__(self):
        self.job_name = ''
        self.lines = {}

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

    def split_pdf(self):

        ordered_pairs = []

        pdf = PdfFileReader(os.getcwd() + "/static/Build_Sheets/BS.pdf")
        if pdf is not None:

            for i in range(pdf.getNumPages()):
                page = pdf.getPage(pageNumber=i)
                text = page.extractText()
                lines = text.splitlines()

                # 
                number = 0

                # extract data from PDF
                for line in lines:

                    # assmebly number
                    assembly = re.match(r'Assembly.#([0-9])+', line)
                    if assembly != None:
                        split = assembly.group(0).split('#')
                        number = split[1]
                    
                    # left end type
                    lend = re.match(r'LEND=([a-zA-Z])+', line)
                    if lend != None:
                        split = assembly.group(0).split('=')
                        number = split[1]

                pdf_writer = PdfFileWriter()
                pdf_writer.addPage(pdf.getPage(i))

                output_filename = f'{os.getcwd()}/static/Build_Sheets/{number}.pdf'

                # add number and link to list
                ordered_pairs.append((number, f'{number}.pdf'))

                with open(f'{output_filename}', 'wb') as out:
                    pdf_writer.write(out)

                print('Created: {}'.format(output_filename))
