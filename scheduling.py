import numpy as np

class Schedule:
    def __init__(self, agents: [int], total_interval: float, shift_length: float, sleep_times: [[float]]) -> None: 
        # interval and shift length is in hours
        # agents is the ids of the soldiers
        self.agents = agents
        self.total_interval = total_interval
        self.shift_length = shift_length
        self.sleep_times = sleep_times

        self.optimum_times = []
        self.__get_optimum_times

    def __get_optimum_times(self):
        # so far just sleep
        optimum_times = []
        for sleep in range(len(self.sleep_times)):
            optimum_times.append(max(sleep))
        self.optimum_times = optimum_times

    def make_schedule(self):
        # sort agents by optimum time
        
        # split total_interval into slots (by shift_length)

        # while agents, loop over slots (use central time of slot), add agent w closest optimum_time to slot

        # return slots (each slot has list of agents)
        pass


    # db_caller for data
    # intensity of sleep

    # soft constraints: sleep schedule peak times, same no of shifts across the board, i.e. uniformly distributed
    # things to think about: combination for metrics, make sure as much time is covered as possible