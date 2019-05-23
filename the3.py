from collections import Counter

class Node:
    def __init__(self, node_id):
        #List of possible nodes to go, i.e edges
        self.node_id = node_id
        self.transitions = [] 
    
class Transition:
    def __init__(self):
        self.source = source
        self.destination = destination
        self.reward = reward

#Regular nodes in the bridge world
class RoundNode(Node): 
    pass

#Regular nodes in my world
class StarNode(Node):
    pass 

#Teleportation nodes, The rooms i.e. bridges between the universes
class SquareNode(Node):
    pass

#Vortext nodes, like black holes
class CrossNode(Node):
    pass

#Destination
class GoalNode(Node):
    pass

class Action:
    def __init__(self, action_id, ):
        pass



class Parser:
    def __init__(self, filename):
        self.filename = filename

    def parse_input(self):
        with open(self.filename) as f:
            node_counts = Counter(f.readline().rstrip())
            for key, value in node_counts:
                pass
            
            learning_rate, discount_factor = map(float, f.readline().split())
            
            num_transitions = int(f.readline())
            for i in range(num_transitions):
                src, dest, reward = map(int, f.readline().split())
                print(src, dest, reward)
        
        return game_graph, actions

#Represents the two environments as a directed graph
class GameGraph:
    def __init__(self):
        self.transitions = [] 

class Game:
    def __init__(self, filename = 'the3.inp'):
        self.parser = Parser(filename)

        self.game_graph = None
        self.actions = []
    
    def run(self):
        self.game_graph, self.actions = self.parser.parse_input()




if __name__ == '__main__':
    Game().run()
