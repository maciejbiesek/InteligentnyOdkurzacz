import copy
import Genetic
import Game
import Player

INTEGER_ENCODE_BITS = 8
PLAYER_PARAMETERS = 1
CHROMOSOME_LENGTH = PLAYER_PARAMETERS * INTEGER_ENCODE_BITS


class Generation:
    def __init__(self, game, num):
        self.game = game
        self.num = num
        self.players = [None] * num
        for i in range(0, num):
            self.players[i] = Genetic.Chromosome(CHROMOSOME_LENGTH)
            self.players[i].randomize()
        self.iteration = 0

    def next(self, mutation_rate, crossover_rate):
        self.iteration += 1
        self.game.generation = self.iteration
        self.game.population_size = self.num

        new = []
        fitness = [0] * self.num

        for i in range(0, self.num):
            player = Player.Player(3, 7, 'textures/roomba_down.png', 'textures/roomba_up.png',
                                   'textures/roomba_left.png', 'textures/roomba_right.png')
            bits = self.players[i].getPart(INTEGER_ENCODE_BITS * 0, INTEGER_ENCODE_BITS)
            player.capacity = 1 + Genetic.GrayCodeRank(bits)
            self.game.evaluated_player = i
            fitness[i] = self.game.evaluatePlayer(player)

        for i in range(0, self.num, 2):
            j1 = Genetic.FitnessSelection(fitness)
            fitness2 = fitness[:]
            fitness2[j1] = 0
            j2 = Genetic.FitnessSelection(fitness2)

            ch1 = copy.deepcopy(self.players[j1])
            ch2 = copy.deepcopy(self.players[j2])
            Genetic.Crossover(ch1, ch2, crossover_rate)

            Genetic.Mutation(ch1, mutation_rate)
            Genetic.Mutation(ch2, mutation_rate)

            new.append(ch1)
            new.append(ch2)

        self.players = new
        self.num = len(self.players)
