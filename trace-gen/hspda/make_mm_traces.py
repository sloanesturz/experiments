import os

def extract_line(line):
    segments = line.split()
    numbytes = segments[4]
    ms = segments[5]
    return int(numbytes), int(ms)

for filename in os.listdir('traces'):
    with open('mm-traces/' + filename, 'w') as fout:
        with open('traces/' + filename, 'r') as fin:
            time = 0
            for line in fin:
                numbytes, ms = extract_line(line)
                tp = 1. * numbytes / ms
                if tp == 0:
                    continue
                mtu_time = int(1500 / tp) # ms for a MTU
                for _ in range(1000 / mtu_time):
                    time += mtu_time
                    fout.write(str(time) + "\n")




