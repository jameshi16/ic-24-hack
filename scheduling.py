import numpy as np

# TODO: put elsewhere
class Soldier:
    def __init__(self, soldier_id: str, sleep_scores: [float]):
        self.soldier_id = soldier_id
        self.__sleep_scores = sleep_scores

        self.optimum_time = self.__get_optimum_time()

    def __get_optimum_time(self):
        # so far just based on sleep scores
        return np.argmin(np.array(self.__sleep_scores))[0]

class Schedule:
    def __init__(self, soldiers: [Soldier], slot_length: float, total_interval: float) -> None: 
        # interval and slot length is in hours
        if self.total_interval % slot_length != 0:
            raise ValueError("Condition not satisfied during initialization, total_interval should be a multiple of shift_length")
        self.soldiers = soldiers
        self.slot_length = slot_length
        self.total_interval = total_interval

    def make_schedule(self):
        # sort soldiers by optimum time
        self.soldiers.sort(key=lambda x: x.optimum_time)
        # split total_interval into slots (by shift_length)
        slots = []
        for i in range(int(self.total_interval) self.slot_length)):
            slots.append(i + (1/2) * self.slot_length)
        # while soldiers, loop over slots (use central time of slot), add agent w closest optimum_time to slot
        schedule = [[] * len(slots)]
        break_loop = False
        while not break_loop:
            for s in slots:
                if not self.soldiers:
                    break_loop = True
                    break
                soldier_index = np.argmin(np.array(self.soldiers), key=lambda x: abs(s - x.optimum_time))
                schedule[s - (1/2) * self.slot_length].append(self.soldiers.pop(soldier_index))
                

        # return slots (each slot has list of soldiers)
        return schedule
    

    # db_caller for data
    # intensity of sleep
    def check_match(self, soft_limit, idx):
        return idx in soft_limit[:10]
        
    def get_optimum_time():
        
    
    def make_schedule0(self):
        optimum_time = self.get_optimum_time()
        sorted_optimum = np.argsort(optimum_time)
        schedule = []
        for i in range(int(self.total_interval/self.slot_length)):
            time = (slot_length * i) % 24 
            count = 0
            while not check_match(self.soldier[-(time % len(self.agent))]):
                count += 1
                time += count
                count += 1
                time -= count
                # oscillator for in front behind which makes hard constraint on number of days
            schedule.append(self.soldier[-(time % len(self.agent))])
    # soft constraints: sleep schedule peak times, same no of shifts across the board, i.e. uniformly distributed
    # things to think about: combination for metrics, make sure as much time is covered as possible
    
sch = Schedule([Soldier("1", [1,3,4])])
