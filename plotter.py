import sys
import matplotlib.pyplot as plt
import re
import os

NUM_CHUNKS = 65

class Plotter:
    
    def __init__(self):
        self.QOEs = []
        self.lambd = 1
        self.mu = 3000
        self.mu_s = 3000

    def parseData(self, filenames):
        pass

    def addQOE(self, filename):
        bitrates, downloadTimes, bufferSizes, startupTime = self.parseRun(filename)
        print startupTime, filename
        numChunks = len(downloadTimes)
        # assert same?
        quality = variation = rebuffering = 0
        for k in range(numChunks):
            quality += bitrates[k]
            rebuffering += downloadTimes[k] - bufferSizes[k]
            if k == 0:
                continue
            variation += bitrates[k] - bitrates[k-1]

        qoe = quality - self.lambd * variation - self.mu * rebuffering \
                      - self.mu_s * startupTime
        print qoe
        self.QOEs.append(qoe)

    def parseRun(self, filename):
        bitrates = [0] * NUM_CHUNKS
        downloadTimes = [0] * NUM_CHUNKS
        bufferSizes = [0] * NUM_CHUNKS
        startupTime = None
        
        with open(filename) as f:
            for line in f:
                if re.match('Buffer size', line):
                    idx, val = line.split()[-2:]
                    bufferSizes[int(idx)-1] = int(val)
                if re.match('Chunk bitrate', line):
                    idx, val = line.split()[-2:]
                    bitrates[int(idx)-1] = int(val)
                if re.match('Download time', line):
                    time = int(line.split(':')[1].strip())
                    downloadTimes.append(time)
                if re.match('Startup', line):
                    time = int(line.split(':')[1].strip())
                    startupTime = time
        
        return bitrates, downloadTimes, bufferSizes, startupTime
            
    def normalize(data, opt=None):
        if not opt:
            opt = max(data)
        return map(lambda d: float(d) / opt, data)

    def plot(self):
        pass


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: plotter.py <directory name> <output name>'
        exit(0)
    
    dirname, outname = sys.argv[1:3]
    plotter = Plotter()
    for filename in os.listdir(dirname):
        plotter.addQOE(os.path.join(dirname, filename))

    plotter.plot(outname)

