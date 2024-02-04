import numpy as np
# from fetch import Fetcher
# from all_well import WellnessCalc


class Scheduler:
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


if __name__ == "__main__":
    fetcher = Fetcher()
    wellbeings, ids = [], []
    for i in range(6):
        calc = WellnessCalc(fetcher.activity_cleanup(f"{i}"),
                            fetcher.sleep_cleanup(f"{i}"))
        activity, sleep = calc.get_activity_score(), calc.get_sleep_scores()
        overall = calc.get_overall_score(activity, sleep, 4)
        wellbeings.append(overall)
        ids.append(i)

    # print(wellbeings)
    # exit()

    dict0 = {"wellbeing": wellbeings, "id": ids}
    scheduler = Scheduler(dict0)
    print(scheduler.get_soldier_ids(4, 5, 2))
    print(plat.get_soldier_ids(6, 12, 2))
    print(plat.get_soldier_ids(15, 19, 1))
    print(plat.get_soldier_ids(21, 22, 1))
