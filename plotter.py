import os
import sys
import matplotlib.pyplot as plt
import re

NUM_CHUNKS = 65

class Plotter:
    
    def __init__(self):
        self.QOEs = []
        self.lambd = 1
        self.mu = 3000
        self.mu_s = 3000
        self.numPlots = 0

    def clearQOEs(self):
        self.QOEs = []

    def addQOE(self, filename):
        bitrates, downloadTimes, bufferSizes, startupTime = self.parseRun(filename)
        numChunks = len(downloadTimes)
        quality = variation = rebuffering = 0
        for k in range(numChunks):
            quality += bitrates[k]
            rebuffering += downloadTimes[k] - bufferSizes[k]
            if k == 0:
                continue
            variation += bitrates[k] - bitrates[k-1]

        qoe = quality - self.lambd * variation - self.mu * rebuffering \
                      - self.mu_s * startupTime
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
            
    def normalize(self, data, opt=None):
        if not opt:
            opt = max(data)
        return map(lambda d: float(d) / opt, data)

    def startPlot(self):
        plt.rcParams["figure.figsize"] = [20, 8]


    def plotOne(self, title):
        filteredQOEs = sorted(self.QOEs)[5:-5]

        plt.subplot(1, 3, self.numPlots)
        plt.plot(filteredQOEs, 'o')
        plt.tick_params(
            axis='x',          
            which='both',      
            bottom='off',      
            top='off',
            labelbottom='off')
        plt.ylabel('QOE value')
        plt.title(title)

        self.numPlots += 1

    def savePlot(self, plotname):
        plt.savefig(plotname)
        plt.close()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: plotter.py <directory-name>'
        exit(0)

    topDir = sys.argv[1].replace('/', '')
    
    dirs = ['output-fcc-traces', 'output-hsdpa-traces', 'output-synthetic-traces']
    titles = ['FCC', 'HSDPA', 'Synthetic']
    plotter = Plotter()
    plotter.startPlot()

    for dirname, title in zip(dirs, titles):
        fullDir = topDir + '/' + dirname
        for filename in os.listdir(fullDir):
            plotter.addQOE(os.path.join(fullDir, filename))
        plotter.plotOne(title)
        plotter.clearQOEs()

    plotter.savePlot(topDir + '/VLC_QOE_Outputs.png')

'''if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: plotter.py <directory name> <output name>'
        exit(0)
    
    dirname, outname = sys.argv[1:3]
    plotter = Plotter()
    for filename in os.listdir(dirname):
        plotter.addQOE(os.path.join(dirname, filename))

    plotter.plot(outname)'''





