import time
import copy

class Conway:
    """Main code to generate the cellular automata"""

    def __init__(self):
        """Initialize the game"""
        #set grid height and width
        height = 38
        width = 31
        self.height = height
        self.width = width

        #define and create graph
        self.graph = []
        self.leave = False
        for _ in range(width):

            col = [' '] * height
            self.graph.append(col)

        #creates starting phase
        print("Initial Phase:")
        self.initial_setup()
        self.print_graph()
        time.sleep(0.5)
        
        #start main loop of code
        for i in range(1,61):
            time.sleep(0.5)
            self.graph = self.check_neighbours(self.width, self.height)
            print('\n\n')
            print("Phase", i, flush=True)
            self.print_graph()

            if self.leave:
                break

    def exit(self):
        self.leave = True

    def has_top_left(self, i, j):
        return i - 1 >= 0 and j - 1 >= 0

    def has_top(self, i, _):
        return i - 1 >= 0

    def has_top_right(self, i, j):
        return i - 1 >= 0 and j + 1 < len(self.graph[i])

    def has_left(self, i, j):
        return j - 1 >= 0

    def has_right(self, i, j):
        return j + 1 < len(self.graph[i])

    def has_bottom_left(self, i, j):
        return i + 1 < len(self.graph) and j - 1 >= 0

    def has_bottom(self, i, _):
        return i + 1 < len(self.graph)

    def has_bottom_right(self, i, j):
        return i + 1 < len(self.graph) and j + 1 < len(self.graph[i])

    def check_neighbours(self, height, width):
        """Checks the neighbours of every cell to determine which cell should be alive or dead"""
        new_graph = copy.deepcopy(self.graph)

        for i in range(height):
            for j in range(width):
                top_left = self.graph[i - 1][j - 1] if self.has_top_left(i, j) else None
                top = self.graph[i - 1][j] if self.has_top(i, j) else None
                top_right = self.graph[i - 1][j + 1] if self.has_top_right(i, j) else None
                left = self.graph[i][j - 1] if self.has_left(i, j) else None
                right = self.graph[i][j + 1] if self.has_right(i, j) else None
                bottom_left = self.graph[i + 1][j - 1] if self.has_bottom_left(i, j) else None
                bottom = self.graph[i + 1][j] if self.has_bottom(i, j) else None
                bottom_right = self.graph[i + 1][j + 1] if self.has_bottom_right(i, j) else None

                neighbours = [top_left, top, top_right, left, right, bottom_left, bottom, bottom_right]
                new_graph[i][j] = self._check_conditions(neighbours, self.graph[i][j])

        return new_graph

    def _check_conditions(self, neighbours, cell):
        """Checks the neighbours of a cell for the specific conditions in order to live or die"""
        alive_count = sum(1 for neighbour in neighbours if neighbour == 'O')

        # If a living square has 2 or 3 neighbours, it continues living
        if cell == 'O' and (alive_count == 2 or alive_count == 3):
            return 'O'

        # If a dead square has exactly 3 neighbours, it comes alive
        if cell == ' ' and alive_count == 3:
            return 'O'

        # Every other square will die or remain dead
        return ' '

    def initial_setup(self):
        """Sets up the start of the simulation"""
        for i in range(len(self.graph)):
            for j in range(len(self.graph[i])):
                self.graph[i][j] = ' '

        # Glider gun setup
        self.graph[3][36] = "O"
        self.graph[4][36] = "O"
        self.graph[3][35] = "O"
        self.graph[4][35] = "O"
        self.graph[1][25] = "O"
        self.graph[2][25] = "O"
        self.graph[2][23] = "O"
        self.graph[3][22] = "O"
        self.graph[3][21] = "O"
        self.graph[4][22] = "O"
        self.graph[4][21] = "O"
        self.graph[5][22] = "O"
        self.graph[5][21] = "O"
        self.graph[6][23] = "O"
        self.graph[6][25] = "O"
        self.graph[7][25] = "O"
        self.graph[6][18] = "O"
        self.graph[5][17] = "O"
        self.graph[6][17] = "O"
        self.graph[7][17] = "O"
        self.graph[8][16] = "O"
        self.graph[4][16] = "O"
        self.graph[6][15] = "O"
        self.graph[9][14] = "O"
        self.graph[3][14] = "O"
        self.graph[9][13] = "O"
        self.graph[3][13] = "O"
        self.graph[4][12] = "O"
        self.graph[8][12] = "O"
        self.graph[7][11] = "O"
        self.graph[6][11] = "O"
        self.graph[5][11] = "O"
        self.graph[5][1] = "O"
        self.graph[6][1] = "O"
        self.graph[5][2] = "O"
        self.graph[6][2] = "O"

    def print_graph(self):
        """Prints the graph in a readable form"""
        for row in self.graph:
            print("".join(row))


if __name__ == '__main__':
    Conway()  # Make a game instance and run the game
