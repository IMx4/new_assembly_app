import os


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
