from FileData import FileData
from assembly import Assembly
import os


class Data():

    def get_jobs(self):

        path = f'{os.getcwd()}/static/Build_Sheets/'
        files = [f for f in os.listdir(path)]
        return files

    def load_job(self, job):

        assemblies = {}
        fd = FileData()
        job_data = fd.read_file(job)

        for num, status in job_data.items():
            assembly = Assembly(
                job, num,
                int(status[0]),
                int(status[1]),
                int(status[2]),
                int(status[3]),
                int(status[4]),
                int(status[5]),
                int(status[6]),
                int(status[7]),
                int(status[8]),
                int(status[9]),
                int(status[10]))
            assemblies[num] = assembly
        return assemblies

    def write_status(self, assemblies, job_name):
        ######## write status file #########

        with open(f'{os.getcwd()}/static/Build_Sheets/{job_name}/{job_name}-status.txt', 'w') as w:
            w.write(job_name + '\n')
            for assembly in assemblies:
                data = str(assemblies.get(assembly))
                w.write(data[1:-1])
                w.write('\n')
            w.close()
