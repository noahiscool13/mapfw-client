# MAPFW Client

This is a client library for the https://mapfw.nl/ MAPFW problems
## The MAPFW problem
MAPFW is an abbreviation of  "Multi-agent pathfinding (with) waypoints".
With MAPFW problems, you are given:
-	A grid/maze
-	A list of agent starting positions
-	A list of agent goal positions
-	A list of agent waypoints

The solution for that problem is a list of paths, one for each agent st.
-	Each path starts on the starting position of the corresponding agent
-	Each path ends on the goal position of the corresponding agent
-	Each path crosses all waypoints of the corresponding agent
-	No path crosses a wall in the grid
-	No 2 agents are ever on the same position at the same time
-	No 2 agents  ever cross the same edge (in opposite directions) at the same time
This solution is optimal if there is no other solution st. the sum of the lengths of the paths of all the agents is smaller than the this solution.
## Using the client library
Install the library with:
```bash
pip install mapfw
```
Then go to https://mapfw.nl/benchmarks/. Here you can find a list of benchmarks. If you click on a benchmark you can see prefiously posted solutions. By clicking on a solution, You can see what the problem looks like. Find a problem that you like, and find its index on the https://mapfw.nl/benchmarks/ page (Sorry, you will have to count yourself, starting from 1. This will change later).

Now go to your account page at https://mapfw.nl/auth/account. To find your API Token

This is all the info you need to start coding. The basic outline of your code should look like this:
```python
from mapfw import MapfwBenchmarker

benchmarker = MapfwBenchmarker("<YOUR API TOKEN>", <BENCHMARK INDEX>, "<YOUR ALGORITHMS NAME>",
                               "<YOUR ALGORITHMS VERSION>", <DEBUG_MODE>)
for problem in benchmarker:
    problem.add_solution(solve(problem))
```
The only things that you need to do are to fill in your own API Token, and the number of the benchmark that you want to solve. The name of your algorithm, and its version. And the debug mode. This should be set to True while you are developing your algorithm. This means that your attempts will not be shown on the global leader boards. You can however still see your own solution at https://mapfw.nl/auth/latest-debug.

When your are ready, set the debug mode to False. The next time you run your code, your attempt will be publicly listed.
You should also implement the "solve" function yourself.
This function should take in a problem and return the solution.
A basic outline of this function can be as follows:
```python
class Agent:
    def __init__(self, start, goal, waypoints):
        self.start = start
        self.goal = goal
        self.waypoints = waypoints


class Maze:
    def __init__(self, grid, width, height):
        self.grid = grid
        self.width = width
        self.height = height


def solve(problem):
    number_of_agents = len(problem.starts)
    agents = []
    for i in range(number_of_agents):
        agents.append(Agent(problem.starts[i], problem.starts[i], problem.goals[i], problem.waypoints[i]))
    maze = Maze(problem.grid, problem.width, problem.height)

    paths = []
    for agent in agents:
        paths.append(find_path(agent, maze))

    """
    Now paths looks like:
    
    paths = [path agent 1, path agent 2, ..]
    path agent 1 = [pos agent 1 at time 0, pos agent 1 at time 1, .., pos agent 1 at finishing time]
    pos = [x coordinate, y coordinate]
    """

    return paths
```
This should be all that you need to know to get started!
Please note that this is just some example code and feel free to change it however you like.

Good luck! And let us know if you have any questions.
