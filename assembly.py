

class Assembly():

    def __init__(self, job_name, number, case, hardware, face_type, l_end, r_end, light, p_door, s_door, d_front, f_front, garbage):

        self._job_name = job_name
        self._number = number
        self._case = {"case": case, "complete": 0}
        self._face_type = {"face": face_type, "complete": face_type}
        self._l_end = {"lend": l_end, "complete": l_end}
        self._r_end = {"rend": r_end, "complete": r_end}
        self._p_door = {"pair door": p_door, "complete": p_door}
        self._s_door = {"single door": s_door, "complete": s_door}
        self._d_front = {"drw front": d_front, "complete": d_front}
        self._f_front = {"false front": f_front, "complete": f_front}
        self._garbage = {"garbage": garbage, "complete": garbage}
        self._light_pan = {"light": light, "complete": light}
        self._hardware = {"hardware": hardware, "complete": hardware}
        self.data = [self._case, self._hardware, self._face_type, self._l_end, self._r_end, self._light_pan,
                     self._p_door, self._s_door, self._d_front, self._f_front, self._garbage]

    def __str__(self):
        status = ','.join(map(str, self.get_assembly_status()))
        return repr(f'{self._number},{status}')

    def filter_out_unused(self, data):
        active_count = 0
        for d in data:
            keys = list(d)
            if d.get(keys[0]) >= 0:
                active_count += 1

        return active_count

    def calc_percent_complete(self):

        total = self.filter_out_unused(self.data)
        total_complete = 0
        for d in self.data:
            if d.get('complete') == 1:
                total_complete += 1

        return int((total_complete/total)*100)

    def set_complete(self, item):
        i = -1
        for d in self.data:
            i += 1
            keys = list(d)
            if item == keys[0]:
                print(f'Key Used: {keys[0]} - Index: {i}')
                d['complete'] = 1
                break

    def get_assembly_status(self):
        status = []

        for d in self.data:
            status.append(d.get('complete'))

        # print(f'{self._number},{self._l_end},{status}')
        return status
