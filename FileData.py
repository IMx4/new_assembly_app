import os
# from PyPDF2 import PdfFileReader, PdfFileWriter
# import re
# from . import assembly


class FileData():

    def __init__(self):
        self.job_name = ''
        self.lines = {}
        self.assemblies = []

    def read_file(self, job):
        # open persistance file and check status
        # file_path = os.path.dirname +
        with open(os.getcwd() + f'/static/Build_Sheets/{job}/{job}-status.txt', 'r+', encoding='utf-8') as persistance:

            self.job_name = persistance.readline().strip()
            for line in persistance:
                split = line.rstrip().split(',')
                self.lines[split[0]] = split[1:]
            return self.lines

    def file_lines(self):
        return self.lines
