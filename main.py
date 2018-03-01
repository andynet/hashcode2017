from pyeasyga import pyeasyga
import scoring as sc
import sys



def load_data(filename):
    return 2


if len(sys.argv) < 2:
    print("Usage: %s <file_name>" % sys.argv[0])
    sys.exit(0)


model = sc.Model(sys.argv[1])


data = load_data(sys.argv[1])


ga = pyeasyga.GeneticAlgorithm(data) 


def fitness(invidual, data):
    pass




ga.fitness_function = fitness

ga.run()

print(ga.best_individual())






