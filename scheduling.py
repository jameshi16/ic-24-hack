class Schedule:
    def __init__(self, agents: [int], total_interval: float, shift_length: float) -> None: 
        # interval and shift length is in hours
        # agents is the ids of the soldiers
        self.agents = agents
        self.total_interval = total_interval
        self.shift_length = shift_length
        pass

    # db_caller for data
    # intensity of sleep

    # soft constraints: sleep schedule peak times, same no of shifts across the board, i.e. uniformly distributed
    # things to think about: combination for metrics, make sure as much time is covered as possible