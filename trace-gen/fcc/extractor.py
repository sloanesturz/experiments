#!usr/bin/python
from collections import defaultdict
import sys

# Ignore throughput traces faster than 3 Mbps; solution would be trivial
HIGH_SPEED_CUTOFF = 3 * 10**6 

# Test video is 4:24, so assume a minimum download time is twice that
# Each trace entry represents 5 seconds of time
REQUIRED_LEN = int((4 * 60 + 24) * 2 / 5)

# line looks like:
# id, dtime, host, throughput,  ...
# Returns (host, throughput)
def extract_line(line):
    segments = line.split(',')
    return segments[2], int(segments[3])

def extract_trace(path):
    found = 0
    traces = defaultdict(list)
    with open(path + ".out", "w") as out:
        with open(path, 'r') as in_:
            for line in in_:
                hostname, tp = extract_line(line)
                if tp > 0:
                    traces[hostname].append(tp)
                    if len(traces[hostname]) >= REQUIRED_LEN:
                        trace = traces[hostname]
                        if sum(trace) / len(trace) < HIGH_SPEED_CUTOFF:
                            out_str = "%s:%s:%s\n" % \
                                    (found, hostname, ",".join(str(t) for t in trace[0:REQUIRED_LEN]))
                            out.write(out_str)
                            found += 1
                        del traces[hostname]
    print found

if __name__ == "__main__":
    if len(sys.argv) == 2:
        extract_trace(sys.argv[1])
    else:
        print "Usage: python %s trace_file" % sys.argv[0]
