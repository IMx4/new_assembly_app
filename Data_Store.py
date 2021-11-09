#import FileData as fd
import assembly as assembly


class Data():

    def __init__(self):
        self.assemblies = []

    #     self.current_assembly = 0
    #     self.file_data = fd.FileData()
    #     self.file_data.split_pdf()
    #     # read file and compose Assemblies
    #     self.file_data.read_file()
    #     self.job_name = self.file_data.job_name
    #     self.assemblies = self.file_data.file_lines()
    #     self.assembly_list = self.create_assembly_list()

    # def assembly_numbers(self):
    #     return [x for x, y in self.assemblies.items()]

    # def create_assembly_list(self):
    #     temp_list = []
    #     for num, spec in self.assemblies.items():
    #         temp_list.append(Assembly(num, spec[0], spec[1], spec[2], spec[3]))

    #     return temp_list

    # def get_assemblies_dict(self):
    #     temp_dict = {}
    #     for assembly in self.assembly_list:
    #         temp_dict[assembly.number] = assembly

    #     return temp_dict

    # def get_assemblies_list(self):
    #     return self.assembly_list

    # def get_job_name(self):
    #     return self.job_name

    # def change_state(self, assembly, index):
    #     temp_dict = self.get_assemblies_dict()
    #     cab = temp_dict.get(assembly)
    #     cab.change_state(index)
    #     self.file_data.write_file(self.get_assemblies_list())

    def create_assembly(self, num, euro, left, right, light):

        self.assemblies.append(assembly(num, euro, left, right, light))
