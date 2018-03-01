from pyeasyga import pyeasyga
import scoring as sc
import sys



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
            if invidual[cache*model._numVideos + video] == 1:
                size += video_size

            if size > model._cachesSize:
                return False
    return True
            


if len(sys.argv) < 2:
    print("Usage: %s <file_name>" % sys.argv[0])
    sys.exit(0)


model = sc.Model(sys.argv[1])


data = load_data(model)


ga = pyeasyga.GeneticAlgorithm(data) 


def fitness(invidual, data):
    global model
    if not checkVideoSizeInCaches(model, invidual):
        return 0
    print("skusam")
    def videoIn(invidual, video, cache_id, num_videos):
        return 1 == invidual[cache_id*num_videos + video]

    return model.rate(invidual, videoIn)


ga.fitness_function = fitness

ga.run()

print(ga.best_individual())






