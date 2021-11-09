
class Assembly():

    def __init__(self, number, face_type, l_end, r_end, light):

        self.number = number
        self.case = {"case": True, "complete": 0}
        self.face_type = {"face": face_type, "complete": 0}
        self.l_end = {"lend": l_end, "complete": 0}
        self.r_end = {"rend": r_end, "complete": 0}
        self.hardware = {"hardware": True, "complete": 0}
        self.doors = {"doors": True, "complete": 0}
        self.light_pan = {"light": light, "complete": 0}

    def calc_percent_complete(self):

        total_steps = 3
        if self.face_type["face"]:
            total_steps += 1
        if self.l_end["lend"]:
            total_steps += 1
        if self.r_end["rend"]:
            total_steps + 1
        if self.light_pan["light"]:
            total_steps += 1

        completed_steps = 0
        if self.case["complete"]:
            completed_steps += 1
        if self.face_type["face"] & self.face_type["complete"]:
            completed_steps += 1
        if self.l_end["lend"] & self.l_end["complete"]:
            completed_steps += 1
        if self.r_end["rend"] & self.r_end["complete"]:
            completed_steps += 1
        if self.hardware["complete"]:
            completed_steps += 1
        if self.doors["complete"]:
            completed_steps += 1
        if self.light_pan["light"] & self.light_pan["complete"]:
            completed_steps += 1

        return (completed_steps/total_steps)*100
