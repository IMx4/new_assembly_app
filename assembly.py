import os
import math


class Assembly():

    def __init__(self, number, face_type, l_end, r_end, string_status):

        self.number = number
        self.face_type = face_type
        self.l_end = l_end
        self.r_end = r_end
        self.status = [int(x) for x in string_status.strip(' \n')]
        self.task_count = len(self.status)

    def change_state(self, index):

        if self.status[index] == 0:
            self.status[index] = 1

    def percent_complete(self):
        return math.ceil((sum(self.status) / self.task_count)*100)
