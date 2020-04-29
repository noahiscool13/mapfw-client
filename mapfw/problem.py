import json
from time import time


class Problem:
    def __init__(self, grid, width, height, starts, goals, waypoints, benchmark, id, batch_pos):
        """"
        MAPFW problem with some extra data for the benchmark
        """
        # USEFUL FOR PROBLEM SOLVING
        self.grid = grid
        self.width = width
        self.height = height
        self.starts = starts
        self.goals = goals
        self.waypoints = waypoints

        # NOT NEEDED FOR THE PROBLEM SOLVING
        # FOR THE BENCHMARK ONLY
        self.benchmark = benchmark
        self.id = id
        self.batch_pos = batch_pos
        self.start_time = time()
        self.time = 0

    def __str__(self):
        out = f"<Problem\n" \
            f"\tWidth: {self.width}\n" \
            f"\tHeight: {self.height}\n" \
            f"\tStarts: {self.starts}\n" \
            f"\tGoals: {self.goals}\n" \
            f"\tGrid:\n"
        out += "\n".join("\t" + "".join(" " if it == 0 else "X" for it in row) for row in self.grid)
        out += "\n>"
        return out

    def add_solution(self, paths):
        """
        Add the solution to the problem

        paths = [path agent 1, path agent 2, ..]
        path agent 1 = [pos agent 1 at time 0, pos agent 1 at time 1, .., pos agent 1 at finishing time]
        pos = [x coordinate, y coordinate]

        :param paths: list of paths that the agents take
        """
        assert self.benchmark.status["state"] == "RUNNING", print(
            f"Benchmark seems to be inactive. state: {self.benchmark.status(['state'])}")
        assert self.benchmark.status["data"]["problem_states"][self.batch_pos] == 0, print(
            "Problem seems to be already solved")

        self.paths = paths
        self.time = time() - self.start_time
        self.benchmark.status["data"]["problem_states"][self.batch_pos] = 1

        if all(self.benchmark.status["data"]["problem_states"]):
            self.status = {"state": "SUBMITTING", "data": None}
            self.benchmark.submit()

    @staticmethod
    def from_json(data, benchmark, batch_pos):
        """
        Generate problem from json

        :param data: json data
        :param benchmark: benchmark for submission callback
        :param batch_pos: position in benchmark
        :return:
        """
        problem_part = json.loads(data["problem"])
        return Problem(problem_part["grid"], problem_part["width"], problem_part["height"], problem_part["starts"],
                       problem_part["goals"], problem_part["waypoints"], benchmark, data["id"], batch_pos)
