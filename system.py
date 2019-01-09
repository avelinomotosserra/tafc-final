import numpy as np
import networkx as nx

# Visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns


class system:

    def __init__ (self, structure = 'grid', distribution = 'uniform', dimensions = (2,2), rules = np.matrix([[0.,0.],[0.,0.]])):

        # This will define a class that generates a grid of n by m elemets of agents

        # Input Testing
        if (isinstance(structure, str)):

            self.rules = {}
            self.define_rules(rules)

            # Building a grid with dimensions specified by the args
            if structure == 'grid':
                if len(dimensions) < 3 and isinstance(dimensions[0], int) and isinstance(dimensions[1], int):
                    self.network = nx.grid_2d_graph(dimensions[0], dimensions[1], periodic = True)
                else:
                    ValueError('Too many arguments for option for grid')

            elif structure == 'BA':
                if len(dimensions) < 3 and isinstance(dimensions[0], int) and isinstance(dimensions[1], int):
                    self.network = nx.barabasi_albert_graph(dimensions[0], dimensions[1])

                else:
                    ValueError('Too many arguments for option for grid')

            elif structure == 'ER':
                if len(dimensions) < 3 and isinstance(dimensions[0], int) and isinstance(dimensions[1], float):
                    print('here')
                    self.network = nx.erdos_renyi_graph(dimensions[0], dimensions[1])

                else:
                    ValueError('Too many arguments for option for grid')
            else:
                raise ValueError('Unknown option for structure')

        if (isinstance(distribution, str)):

            # Building a uniform distribution of strategies
            if distribution == 'uniform':
                cooperation_prob = {}
                strategies = {}

                for node in self.network.nodes():
                    cooperation_prob[node] = np.random.rand()
                    if cooperation_prob[node] > 0.5:
                        strategies[node] = 0
                    else:
                        strategies[node] = 1

                # Setting the p attributes
                nx.set_node_attributes(self.network, strategies, name='strategy')

                # for node in self.network.nodes():
                #     print(nx.get_node_attributes(self.network,'strategy'))

            else:
                raise ValueError('Unknown option for distribution')

        else:
            raise TypeError('Option argument requires a string type')

    def define_rules(self,rules):

        rules = np.matrix(rules)

        #This function recieves a dictionary with the game costs/rewards
        if rules.shape[0] == rules.shape[1]:
            self.rules = rules


    def uniform_conditions(self):

        cooperation_prob = {}
        strategies = {}

        for node in self.network.nodes():
            cooperation_prob[node] = np.random.rand()
            if cooperation_prob[node] > 0.5:
                strategies[node] = 0
            else:
                strategies[node] = 1

        # Setting the p attributes
        nx.set_node_attributes(self.network, strategies, name='strategy')


    def plot_grid(self):

        pos = {}
        colors = []
        for node in self.network.nodes():
            pos[node] = node

        strat = nx.get_node_attributes(self.network,'strategy')

        for x in strat:
            if strat[x] == 0:
                colors.append('b')
            elif strat[x] == 1:
                colors.append('r')

        # print(colors)
        nx.draw_networkx(self.network, pos=pos, node_color=colors, node_size = 10, with_labels = False)
        plt.show()

    def get_scores(self, atrs):
        # Returns the score optained after a round of the game

        score = {}


        # Calculating the scores resulting of playing the game
        for node in self.network.nodes():
            score[node] = 0
            for n in self.network.neighbors(node):
                # print('neighbor',n)
                # print(atrs[n])
                # print(atrs[node])
                score[node] += self.rules[atrs[node], atrs[n]]

            # Normalization that is introduced in the article
            # score[node] = score[node] / self.network.degree(node)
            # print(score[node])

        return score

    def update_strategies(self, score, atrs):

        # calculting the outcome of the round
        for node in self.network.nodes():
            winner = node
            for n in self.network.neighbors(node):
                if score[winner] < score[n]:
                    winner = n

            atrs[node] = atrs[winner]

        nx.set_node_attributes(self.network, atrs, 'strategy')

    def update_strategies_stochastic(self, score, atrs):

        # Flag that when True interrupts the code
        interrupt_flag = True

        D_max = max([self.rules[1,0], 1]) - min([self.rules[0,1], 0])

        # calculting the outcome of the round
        for node in self.network.nodes():
            nei_list = list(self.network.neighbors(node))
            nei = nei_list[np.random.randint(0,len(nei_list))]

            # Maximum degree of the involved nodes
            k_max = (max([self.network.degree(nei), self.network.degree(node)]))

            if score[nei] > score[node]:
                # print((score[nei] - score[node])/(k_max * D_max))
                interrupt_flag = False

                if np.random.rand() < (score[nei] - score[node])/(k_max * D_max):
                    atrs[node] = atrs[nei]

        nx.set_node_attributes(self.network, atrs, 'strategy')

        return interrupt_flag

    def evolve (self, N = 1):
        for i in range(0,N):
            atrs = nx.get_node_attributes(self.network,'strategy')
            score = self.get_scores(atrs)
            # self.update_strategies(score, atrs)
            int_flag = self.update_strategies_stochastic(score, atrs)

            if int_flag == True:
                # print('Interrupted')
                break

    def evaluate(self):
        '''This function evaluates the number of elements of each species'''
        sys_cmp = {}

        atrs = nx.get_node_attributes(self.network,'strategy')
        for node in self.network.nodes():
            if atrs[node]  not in sys_cmp:
                sys_cmp[atrs[node]] = 1
            else:
                sys_cmp[atrs[node]] +=1

        return sys_cmp

    def grid_test(self, points = 21, repetitions = 10):

        # Gurantee that the rules are inaccordance for every dilema
        self.rules[0,0] = 1

        dic = {}
        for i in range(0,2):
            dic[i] = np.empty([points, points])

        i = 0
        j = 0

        for S in np.linspace(-1, 1, num = points, endpoint = True):
            self.rules[0, 1] = S
            j = 0
            for T in np.linspace(0, 2, num  = points, endpoint = True):
                self.rules[1,0] = T

                print(self.rules)

                for iteration in range(0,repetitions):
                    self.uniform_conditions()

                    print(self.evaluate())
                    self.evolve(1000)

                    sol = self.evaluate()

                    for key in dic:
                        if key in sol:
                            dic[key][i,j] += sol[key]
                        else:
                            dic[key][i,j] = 0
                        # print(dic[key][i,j])
                    print(self.evaluate())

                j += 1
                print('i:', i, 'j:', j)
                # print(dic)

            i += 1

        np.save('txt/data_0',dic[0])
        np.save('txt/data_1',dic[1])


    def plot_solution(self, points = 10):
        sol_1 = np.load('txt/data_0.npy')
        sol_2 = np.load('txt/data_1.npy')

        S_values = np.linspace(-1, 1, num = points, endpoint = True)
        T_values = np.linspace(0, 2, num  = points, endpoint = True)

        sns.heatmap(sol_1, xticklabels = S_values, yticklabels = T_values)
        plt.show()

        # sns.heatmap(sol_2)
        # plt.show()
