import sys

MTU = 1500

def do_it(path):
    with open(path, 'r') as fin:
        for line in fin:
            num, host, tp_avgs = line.split(':')
            tp_avgs = [int(t) for t in tp_avgs.split(',')]
            with open("trace/%s-%s" % (num, host), 'w') as fout:
                last_delivery = 0
                bonus_bytes = 0
                print (host, tp_avgs)
                for tp in tp_avgs:
                    # TP is in bps
                    # we need to schedule the deliveries for five seconds of 
                    # observing a line rate of TP bps. A delivery is scheduled
                    # every time a full 1500 bytes could arrive
                    if tp == 0:
                        continue
                    packet_time = int(1500*1000. / tp)
                    if packet_time == 0: packet_time = 1
                    for _ in range(5000 / packet_time):
                        last_delivery += packet_time
                        fout.write(str(last_delivery) + "\n")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        do_it(sys.argv[1])
    else:
        print "Usage: python %s tp_avgs" % sys.argv[0]
