import numpy as np

class Platoon:
    def __init__(self, soldiers_json) -> None:
        # soldiers_json is a dict, contains: soldier id, wellbeing scores
        self.soldiers = soldiers_json          # ids have to be indexed 0, 1, 2, ...
        self.queue = [[], [], [], [], []]
    # return True if to_searh in q, else False
    def __is_present(self, to_search):
        for tup in self.queue:
            for element in tup:
                if element == to_search:
                    return True
        return False
           
    def get_soldier_ids(self, start_time, end_time, num_people):
        wellbeings = self.soldiers["wellbeing"]
        wellbeing_sums = [sum(wellbeing[start_time: end_time + 1]) for wellbeing in wellbeings]
        idx_soldier = []
        while len(idx_soldier) < num_people:
            if max(wellbeing_sums) == -1:
                break
            curr_idx = np.argmax(np.array(wellbeing_sums))
            if not self.__is_present(curr_idx):
                idx_soldier.append(curr_idx)
            wellbeing_sums[curr_idx] = -1
        self.queue = self.queue[1:]
        self.queue.append(idx_soldier)
        # print(self.queue)
        return idx_soldier

# dict0 = {"wellbeing": [[1,2,2,1,4,5,1,2,4,3,2,1,1,2,2,1,4,5,1,2,4,3,2,1], [41,8,2,8,4,5,1,2,8,3,2,1,8,2,2,1,4,8,1,2,4,8,2,1],
#          [1,2,7,1,4,7,1,2,4,1,2,1,4,2,2,9,4,5,1,2,4,3,2,1], [8,2,2,1,4,5,9,2,4,3,2,9,1,2,2,5,4,5,1,4,4,2,29,1]], "id": [0, 1, 2, 3]}
# plat = Platoon(dict0)
# print(plat.get_soldier_ids(3, 5, 1))
# print(plat.get_soldier_ids(6, 12, 2))
# print(plat.get_soldier_ids(15, 20, 1))
# print(plat.get_soldier_ids(21, 22, 1))