import warnings
from typing import Union, Callable, List

from mapfw.problem import Problem
from time import time
import requests
from func_timeout import func_timeout, FunctionTimedOut


class MapfwBenchmarker:
    def __init__(self, token: str, problem_id: Union[int, iter], algorithm: str, version: str, debug=True,
                 solver: Callable[[Problem], List] = None):
        """
        Helper function to handle API requests

        :param token: User token
        :param problem_id: Id of the problem to solve
        :param algorithm: Name of your algorithm
        :param version: Version of your algorithm
        :param debug: Set to False to get your solution in the global rankings
        :param solver: Your MAPFW solving function
        """
        self.token = token
        self.solver = solver
        self.algorithm = algorithm
        self.version = version
        self.benchmarks = [problem_id] if isinstance(problem_id, int) else problem_id
        self.problems = None
        self.status = {"state": "UNINITIALIZED", "data": None}
        self.attempt_id = None
        self.timeout = None
        self.debug = debug

    def __iter__(self):
        warnings.warn("Consult the README for the new way of running benchmarks", DeprecationWarning, stacklevel=2)

        for problem_id in self.benchmarks:
            self.status = {"state": "UNINITIALIZED", "data": None}
            self.problem_id = problem_id
            self.load()

            assert not self.timeout, print("The benchmark that you are trying to solve uses a timeout.\n"
                                           "Iterating over the problems like this does not support timeouts.\n"
                                           "Consult the README for information about running timed benchmarks.")

            for problem in self.problems:
                problem.start_time = time()
                yield problem

    def run(self, solver: Callable[[Problem], List] = None):
        """
        Use your solver to solve all problems
        """
        if solver:
            self.solver = solver
        assert self.solver, print("No solver given.\n"
                                  "Consult the README for information about running timed benchmarks.")

        for problem_id in self.benchmarks:
            self.status = {"state": "UNINITIALIZED", "data": None}
            self.problem_id = problem_id
            self.load()

            while self.status["state"] == "RUNNING":
                for problem in self.problems:
                    if self.timeout:
                        problem.start_time = time()
                        try:
                            solution = func_timeout(self.timeout / 1000, self.solver, args=(problem,))
                        except FunctionTimedOut:
                            solution = None
                        problem.add_solution(solution)
                    else:
                        problem.start_time = time()
                        solution = self.solver(problem)
                        problem.add_solution(solution)

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
                } for problem in self.problems
            ]
        }

        r = requests.post(f"https://mapfw.nl/api/attempts/{self.attempt_id}/solutions", headers=headers, json=data)
        # r = requests.post(f"http://127.0.0.1:5000/api/attempts/{self.attempt_id}/solutions", headers=headers, json=data)

        assert r.status_code == 200, print(r.content)

        res = r.json()

        if res == "OK":
            self.status = {"state": "SUBMITTED", "data": None}
        else:
            self.problems = [Problem.from_json(part, self, pos) for pos, part in enumerate(r.json()["problems"])]
            self.attempt_id = r.json()["attempt"]

            if "timeout" in r.json():
                self.timeout = r.json()["timeout"]
            else:
                self.timeout = 0

            self.status = {"state": "RUNNING", "data": {"problem_states": [0 for _ in self.problems]}}

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
        # r = requests.post(f"http://127.0.0.1:5000/api/benchmarks/{self.problem_id}/problems", headers=headers,
        #                   json=data)

        assert r.status_code == 200, print(r.content)

        self.problems = [Problem.from_json(part, self, pos) for pos, part in enumerate(r.json()["problems"])]
        self.attempt_id = r.json()["attempt"]

        if "timeout" in r.json():
            self.timeout = r.json()["timeout"]
        else:
            self.timeout = 0

        self.status = {"state": "RUNNING", "data": {"problem_states": [0 for _ in self.problems]}}


def get_all_benchmarks(without: Union[int, iter] = None):
    if not without:
        without = []
    without = [without] if isinstance(without, int) else without

    r = requests.get("https://mapfw.nl/benchmarks/list.json")
    return [problem for problem in r.json() if problem not in without]
