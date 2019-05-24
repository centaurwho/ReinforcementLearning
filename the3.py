from collections import Counter
from copy import deepcopy

class Transition:
    def __init__(self, source, destination, reward):
        self.source = source
        self.destination = destination
        self.reward = reward

class Action:
    def __init__(self, action_id):
        self.action_id = action_id
        self.subactions = []

    def add_subaction(self, subaction):
        self.subactions.append(subaction)

    def get_next_states(self, state_id):
        res = []
        
        for subaction in self.subactions:
            if subaction.src == state_id:
                for dest in subaction.dests:
                    res.append((dest[0], dest[1], subaction.reward))
        
        return res

    def get_next_state_ids(self, state_id):
        res = []
        
        for subaction in self.subactions:
            if subaction.src == state_id:
                for dest in subaction.dests:
                    res.append(dest[0])
        return res

    def __repr__(self):
        return f'{self.action_id}: {self.subactions}\n'

class Subaction:
    def __init__(self):
        self.src = None
        self.reward = None
        self.dests = [] #list of probability dest pairs

    def add_dest(self, dest_id, prob):
        self.dests.append((dest_id, prob))

    def __repr__(self):
        return f'src: {self.src}\nreward: {self.reward}\ndests: {self.dests}\n'


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
       
            num_star_nodes = int(f.readline())
            state_action_map = dict()
            
            for i in range(num_star_nodes):
                line = list(map(int, f.readline().split()))
                state_action_map[line[0]] = line[1:]

            game_graph.state_action_map = state_action_map

            actions = []
            act_id = 0
            curr_action = None

            while True:
                line = f.readline().rstrip()
                if line == "E":
                    break
                else:
                    if 'action' in line:
                        curr_action = Action(act_id)
                        act_id += 1
                        subaction = None
                        
                        while True:
                            n_line = f.readline()
                            if '#' in n_line:
                                actions.append(curr_action)
                                break
                            subaction = Subaction()
                            subaction.src = int(n_line)
                            subaction.reward = float(f.readline())
                            while True:
                                dalga = f.readline()
                                if '$' in dalga:
                                    curr_action.add_subaction(subaction)
                                    break
                               
                                dest, prob = list(map(int, dalga.split()))
                                subaction.add_dest(dest, prob/100) 
        return game_graph, learning_rate, discount_factor, actions


#Represents the two environments as a directed graph
class GameGraph:
    def __init__(self, node_counts):
        self.transitions = []
        self.node_counts = node_counts
        self.state_action_map = None

    def add_transition(self, transition):
        self.transitions.append(transition)

    def get_q_dimensions(self):
        return self.node_counts['R'] + self.node_counts['V'] + self.node_counts['O']

    #KTÜ
    def get_v_ids(self):
        return list(self.state_action_map.keys()) + [list(self.state_action_map.keys())[-1] + 1]

    def get_reward(self, src, dest):
        for trans in self.transitions:
            if trans.source == src and trans.destination == dest:
                return trans.reward

    def get_possible_actions(self, state_id):
        if state_id not in self.state_action_map:
            return []
        return self.state_action_map[state_id]


class Game:
    def __init__(self, filename = 'the3.inp'):
        self.parser = Parser(filename)
        
        self.actions = []
    
    def run(self):
        self.initialize()
        self.run_session()

    def initialize(self):
        self.game_graph, self.learning_rate, self.discount_factor, self.actions = self.parser.parse_input()
        
        q_dims = self.game_graph.get_q_dimensions()
        self.q_table = [[0 for _ in range(q_dims)] for _ in range(q_dims)]
        
        self.v_list = {key: (0, []) for key in self.game_graph.get_v_ids()}

    def run_session(self):
        self.run_q_session()
        self.run_viter_session()

    def run_q_session(self):
        while True:
            inp = input('Q-Learning >> ')
            if inp == '$':
                self.print_q_table()
                return
            try:
                episode = list(map(int, inp.split()))
                self.update_q_table(episode)
            except:
                print("Please enter a valid episode")

    def run_viter_session(self):
        self.print_v_list()
        self.print_v_policy()
        while True:
            inp = input('Value Iter >> ')
            
            if inp == '$':
                return
            
            elif inp == 'c':
                self.value_iterate()
                self.print_v_list()
                self.print_v_policy()
            
            else:
                print("Incorrect input. Please enter 'c' or '$':\n")

    def update_q_table(self, episode):
        episode = list(zip(episode, episode[1:]))
        
        #Q(s,t) = a*(r + g*max(Q(s',t')) - Q(s,t))
        for src, dest in episode:
            reward = self.game_graph.get_reward(src, dest)
            if reward is None:
                print("Please enter a valid episode")
                return
            curr_val = self.q_table[src][dest]
            next_state_values = self.q_table[dest]
            self.q_table[src][dest] += self.learning_rate * (reward + self.discount_factor * max(next_state_values) - curr_val)
        
        self.print_q_table()

    def value_iterate(self):
        new_list = deepcopy(self.v_list)
        for state_id in self.v_list:
            action_values = []
            action_next_states = []
            for action_id in self.game_graph.get_possible_actions(state_id):
                val = 0
                next_state_list = self.actions[action_id].get_next_state_ids(state_id) 
                for next_state_id, prob, reward in self.actions[action_id].get_next_states(state_id):
                    val += prob*(reward + self.discount_factor*self.v_list[next_state_id][0])
                action_values.append(val)
                action_next_states.append(next_state_list)

            if action_values != []:
                new_list[state_id] = (max(action_values), action_next_states[action_values.index(max(action_values))])

        self.v_list = new_list

    def print_q_table(self):
        print_str = ""
        for i in range(len(self.q_table)):
            for j in range(len(self.q_table)):
                if self.game_graph.get_reward(i, j) is None:
                    print_str += "_"
                else:
                    print_str += str(self.q_table[i][j])
                print_str += "\t"
            print_str += "\n"

        print(print_str)

    def print_v_list(self):
        print("Value table: \n")
        for key, value in self.v_list.items():
            print(f"{key}:\t{value[0]}")

    def print_v_policy(self):
        print("Value policy: \n")
        for key, value in self.v_list.items():
            print(f"{key}:\t" + ', '.join(str(id) for id in value[1]))


if __name__ == '__main__':
    Game().run()
