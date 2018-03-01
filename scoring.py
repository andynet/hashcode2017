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


    def rate(self, invidual, videoIn):
        saved = 0
        sum_times = 0
        for video, endpoint, times in self._requests:
            latency = self._endpoints[endpoint][0]
            sum_times += times
            for cached_id, ms in self._endpoints[endpoint][1]:
                if videoIn(invidual, video, cached_id, self._numVideos) and latency > ms:
                    latency = ms
            #print("##################")
            #print("(%d - %d)*%d" % (self._endpoints[endpoint][0],
            #    latency, times))
            save = (self._endpoints[endpoint][0] - latency)*times
            saved+=save
        
        return (saved*1000)/sum_times




if __name__ == "__main__":
    model = Model("./test.in")
    print(vars(model))
    def videoIn(invidual, video, cache_id, num_videos):
        return 1 == invidual[cache_id*num_videos + video]
    invidual = [0,0,1,0,0, 0,1,0,1,0, 1,1,0,0,0]
    print(model.rate(invidual, videoIn))
