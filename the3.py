from collections import Counter


class Transition:
    def __init__(self, source, destination, reward):
        self.source = source
        self.destination = destination
        self.reward = reward

#TODO: use maybe
class Action:
    def __init__(self, action_id):
        self.action_id = action_id
        self.transitions = []


class Parser:
    def __init__(self, filename):
        self.filename = filename


    def parse_input(self):
        with open(self.filename) as f:
            
            node_counts = Counter(f.readline().rstrip())
            game_graph = GameGraph(node_counts)
            
            learning_rate, discount_factor = map(float, f.readline().split())
            
            num_transitions = int(f.readline())
            for i in range(num_transitions):
                src, dest, reward = map(int, f.readline().split())
                transition = Transition(src, dest, reward)
                game_graph.add_transition(transition)
       
            #num_actions = int(f.readline())
            #list_of_actions = []
            #for i in range(num_actions):
            #    _, action_id = f.readline().split()
            #    Action action = Action(action_id)
               
        return game_graph, learning_rate, discount_factor


#Represents the two environments as a directed graph
class GameGraph:
    def __init__(self, node_counts):
        self.transitions = []
        self.node_counts = node_counts

    def add_transition(self, transition):
        self.transitions.append(transition)

    def get_q_dimensions(self):
        return self.node_counts['R'] + self.node_counts['V'] + self.node_counts['O']

    def get_reward(self, src, dest):
        for trans in self.transitions:
            if trans.source == src and trans.destination == dest:
                return trans.reward

class QLearning:
    pass

class ValueIteration:
    pass


class Game:
    def __init__(self, filename = 'the3.inp'):
        self.parser = Parser(filename)
        self.q_table = None
        self.learning_rate = None
        self.discount_factor = None

        self.game_graph = None
        self.actions = []
    
    def run(self):
        self.initialize()
        self.run_session()

    def initialize(self):
        self.game_graph, self.learning_rate, self.discount_factor = self.parser.parse_input()
        
        q_dims = self.game_graph.get_q_dimensions()
        self.q_table = [[0 for _ in range(q_dims)] for _ in range(q_dims)]

    def run_session(self):
        self.run_q_session()
        #self.run_viter_session()

    def run_q_session(self):
        while True:
            inp = input()
            if inp == '$':
                self.print_q_table()
                self.print_q_policy()
                return

            episode = list(map(int, inp.split()))
            print(episode)
            self.update_q_table(episode)
    
    def run_viter_session(self):
        while True:
            inp = input()
            
            self.print_v_list()
            self.print_v_policy()
            
            if inp == '$':
                return
            
            elif inp == 'c':
                self.value_iterate()
            
            else:
                print("Incorrect input. Please enter 'c' or '$':\n")

    #TODO: implement
    def update_q_table(self, episode):
        episode = list(zip(episode, episode[1:]))
        print (episode)
        
        #Q(s,t) = a*(r + g*max(Q(s',t')) - Q(s,t))
        for src, dest in episode:
            reward = self.game_graph.get_reward(src, dest)
            curr_val = self.q_table[src][dest]
            next_state_values = self.q_table[dest]
            self.q_table[src][dest] += self.learning_rate * (reward + self.discount_factor * max(next_state_values) - curr_val)
        
        self.print_q_table()


    def print_q_table(self):
        for row in self.q_table:
            print ('\t'.join(map(str, row)))

    def print_q_policy(self):
        for row in self.q_table:
            row_vals = enumerate(row)
            sorted_row = list(sorted(row)) 
    
    def print_v_list(self):
        pass

    def print_v_policy(self):
        pass


if __name__ == '__main__':
    Game().run()
