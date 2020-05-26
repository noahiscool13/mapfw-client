from typing import Union

from mapfw.problem import Problem
from time import time
import requests


class MapfwBenchmarker:
    def __init__(self, token: str, problem_id: Union[int, iter], algorithm: str, version: str, debug=True):
        """
        Helper function to handle API requests

        :param token: User token
        :param problem_id: Id of the problem to solve
        :param algorithm: Name of your algorithm
        :param version: Version of your algorithm
        :param debug: Set to False to get your solution in the global rankings
        """
        self.token = token
        self.algorithm = algorithm
        self.version = version
        self.benchmarks = [problem_id] if isinstance(problem_id, int) else problem_id
        self.problems = None
        self.status = {"state": "UNINITIALIZED", "data": None}
        self.attempt_id = None
        self.debug = debug

    def __iter__(self):
        for problem_id in self.benchmarks:
            self.status = {"state": "UNINITIALIZED", "data": None}
            self.problem_id = problem_id
            self.load()
            for problem in self.problems:
                problem.start_time = time()
                yield problem

    def submit(self):
        """"
        Submit your solution
        You never have to call this function yourself,
        This will automatically be done when you solve all challenges.
        """

        headers = {
            'X-API-Token': self.token
        }

        data = {
            "solutions": [
                {
                    "problem": problem.id,
                    "time": round(problem.time * 1000),
                    "solution": problem.paths
                }
            ] for problem in self.problems
        }

        r = requests.post(f"https://mapfw.nl/api/attempts/{self.attempt_id}/solutions", headers=headers, json=data)
        assert r.status_code == 200, print(r.content)

        self.status = {"state": "SUBMITTED", "data": None}

    def load(self):
        """
        Load the benchmark from the server
        You never have to call this function yourself,
        This will automatically be done when you create an instance of this class.
        """

        assert self.status["state"] == "UNINITIALIZED", print("The benchmark seems to already been initialized\n")

        headers = {
            'X-API-Token': self.token
        }

        data = {
            "algorithm": self.algorithm,
            "version": self.version,
            "debug": self.debug
        }

        r = requests.post(f"https://mapfw.nl/api/benchmarks/{self.problem_id}/problems", headers=headers, json=data)

        assert r.status_code == 200, print(r.content)

        self.problems = [Problem.from_json(part, self, pos) for pos, part in enumerate(r.json()["problems"])]
        self.attempt_id = r.json()["attempt"]

        self.status = {"state": "RUNNING", "data": {"problem_states": [0 for _ in self.problems]}}


def get_all_benchmarks(without: Union[int, iter] = None):
    if not without:
        without = []
    without = [without] if isinstance(without, int) else without

    r = requests.get("https://mapfw.nl/benchmarks/list.json")
    return [problem for problem in r.json() if problem not in without]
