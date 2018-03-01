from pyeasyga import pyeasyga
import scoring as sc
import sys
import numpy as np
import random


class Debug(pyeasyga.GeneticAlgorithm):

    def run(self):
        self._i = 0
        super(Debug, self).run()

    def create_next_generation(self):
        self._i += 1
        print("NextGeberation %d" % self._i)
        super(Debug, self).create_next_generation()

def load_data(model):
    data = []
    for cache in range(model._numCaches):
        for video in range(model._numVideos):
            data.append({'video':video, 'cache':cache})
    return data


def checkVideoSizeInCaches(model, invidual):
    for cache in range(model._numCaches):
        size = 0
        for video, video_size in zip(range(model._numVideos), model._videosSize):
            if invidual[cache,video] == 1:
                size += video_size

            if size > model._cachesSize:
                return False
    return True
            




if len(sys.argv) < 4:
    print("Usage: %s <file_name> <num_population> <num_generation>" % sys.argv[0])
    sys.exit(0)


model = sc.Model(sys.argv[1])
population = int(sys.argv[2])
generation = int(sys.argv[3])

data = load_data(model)


ga = Debug(data,
        maximise_fitness=True,
        elitism = True,
        population_size=population,
        generations=generation) 

def create_individual(data):
    global model
    temp = np.array(model._videosSize)
    to_generate = int(model._cachesSize/temp.mean())
    if (to_generate - 2) > 0:
        to_generate-=2
    invi = np.array([])

    for cache in range(model._numCaches):
        temp = np.random.choice([0, 1],
                size=(model._numCaches*model._numVideos),
                p=[1-(to_generate/model._numVideos),
                    to_generate/model._numVideos])
        if cache == 0:
            invi = np.append(invi, temp)
        else:
            invi = np.vstack([invi, temp])

    return invi

def crossover(parent_1, parent_2):
    index = random.randrange(1, len(parent_1))
    child_1 = np.vstack([parent_1[:index,:], parent_2[index:,:]])
    child_2 = np.vstack([parent_2[:index,:], parent_1[index:,:]])
    return child_1, child_2


def mutate(invidual):
    global model
    mutate_cache = random.randrange(model._numCaches)
    mutate_video = random.randrange(model._numVideos)
    invidual[mutate_cache, mutate_video] = (0, 1)[invidual[mutate_cache, mutate_video] == 0]




def fitness(invidual, data):
    global model
    if not checkVideoSizeInCaches(model, invidual):
        return 0
    def videoIn(invidual, video, cache_id, num_videos):
        return 1 == invidual[cache_id, video]

    return model.rate(invidual, videoIn)


ga.fitness_function = fitness

ga.create_individual = create_individual

ga.crossover_function = crossover

ga.mutate_function = mutate
ga.run()

print(ga.best_individual()[0])






