import os
from random import gauss, random, uniform
import sys


def gen_params():
    # select mu uniform randomly from 1mbps to 40mbps
    # IDK what's going on
    mu = uniform(1, 10) * 8 * 10 ** 4 # bytes / sec
    sigma = (uniform(0.01, 0.1) * mu) ** 1/2

    return mu, sigma

def generate(dirpath):
    for i in range(1, 1001):
        mu, sigma = gen_params()
        with open(os.path.join(dirpath, "%s.trace" % i), "w") as f:
            last_delivery = 0
            tp = []
            for j in range(60*4):
                throughput = gauss(mu, sigma)
                tp.append(throughput)
                packet_time = int(1500 * 1000. / throughput)
                if packet_time <= 0: continue
                for _ in range(1000 / packet_time):
                    last_delivery += packet_time
                    f.write("%s\n" % last_delivery)
            print sum(tp) / len(tp)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print "Usage %s output-dir" % sys.argv[0]
    else:
        generate(sys.argv[1])
