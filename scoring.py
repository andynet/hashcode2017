class Model(object):

    """Scoring model"""

    def __init__(self, filename):
        """TODO: to be defined1.

        :filename: TODO

        """
        self._filename = filename
        f = open(filename, 'r')

        line = f.readline()
        line = line.split()
        self._numVideos = int(line[0])
        self._numEndpoints = int(line[1])
        self._numRequests = int(line[2])
        self._numCaches = int(line[3])
        self._cachesSize = int(line[4])
        
        self._endpoints = []
        self._requests = []

        line = f.readline()
        self._videosSize = list(map(lambda x: int(x),line.split()))
        
        

        for i in range(self._numEndpoints):
            endp = f.readline().split()
            ms = int(endp[0])
            connected = int(endp[1])
            
            caches = []

            for j in range(connected):
                line = f.readline().split()
                caches.append((int(line[0]), int(line[1])))

            self._endpoints.append((ms, caches))


        for i in range(self._numRequests):
            line = f.readline().split()
            self._requests.append((int(line[0]), int(line[1]), int(line[2])))
        f.close()



if __name__ == "__main__":
    model = Model("./test.in")
    print(vars(model))
