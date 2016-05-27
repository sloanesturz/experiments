from pyOpt import pySNOPT
import pyOpt
import math

LAMBDA = 1
MU = 3000
MU_S = 3000

BITRATES = [3000000, 2000000, 1000000, 600000, 349952]

CHUNKSIZE = 4 * 10**6 # 2 seconds in micro-seconds

"""
# sloane wrote
def solve(throughputs):
    K = len(throughputs)

    def qoe(throughputs, buffer_sizes, startupTime):
        return \
            1. * sum(throughputs) / len(throughputs) + \
            -1. * LAMBDA *  sum(math.abs(q_i - q_j) for q_i, q_j in zip(throughputs, throughputs[1:])) + \
            -1. * MU * sum(max(0, bs - CHUNKSIZE) for bs in buffer_sizes) + \
            -1 * MU_S * startupTime

    def objfunc(variables):
        if len(variables) != 2*K + 1:
            raise 'Variables is incorrect size. Expected', 2*K+1, 'Got', len(variables)
        throughputs, bitrates, startupTime = \
                variables[0:K], variables[K:K*2], variables[2*K]


"""
    
def C_t(time):
    return 1.2


# all times are in milliseconds
def solve(K):
    # first numChunks are bitrates, last is startupTime
    def qoe_max(vs):
        t = vs[0:K+1] # times
        br = vs[K+1: K*2+1] #bitrates
        buf = vs[K*2+1: K*3+1]
        startupTime = buf[0]

        C_k = [0]* K

        print t, br, buf, startupTime
        for k in range(K):
            t_k = int(t[k])
            t_k_1 = int(t[k+1])
            C_k[k] =  1 / (t_k_1 - t_k) * sum(C_t(dt) for dt in range(t_k, t_k_1))
        
        f = sum(br) + \
            - LAMBDA * sum(abs(br - br_prev) for br, br_prev in zip(br[1:], br)) + \
            - MU * sum(CHUNKSIZE * br[k] / C_k[k] - buf[k] for k in range(K)) \
            - MU_S  * startupTime
        f = -f # maybe?

        g = [0] * (2 * K + 1)

        for k in range(K):
            g[k] = t[k] - t[k+1] + CHUNKSIZE * br[k] / C_k[k]
            g[K+k] = max(0, max(0, buf[k] - CHUNKSIZE * br[k] / C_k[k]) + CHUNKSIZE)
        
        g[-1] = -t[0]

        fail = 0
        return f, g, fail

    opt_qoe = pyOpt.Optimization('QOE MAX', qoe_max)
    opt_qoe.addObj('f')
    for k in range(K+1):
        opt_qoe.addVar('t%d' % k, type='c', lower=0, upper=360000, value=1) # right timescale?

    for k in range(K):
        opt_qoe.addVar('b%d' % (K + k), type='d', choices=BITRATES, value=0)

    for k in range(K):
        opt_qoe.addVar('buf%d' % (2*K + k), type='c', lower=0, upper=30000000, value=10000) # 30 seconds
    
    
    for i in range(K*2):
        opt_qoe.addCon('g%s' % (i+1), 'e')
    
    opt_qoe.addCon('g%s' % (i+1), 'e')
        
    #print opt_qoe
    psqp = pyOpt.ALHSO()

    psqp(opt_qoe, sens_type='FD')
    print opt_qoe.solution(0)

if __name__ == '__main__':
    throughputs = []
    with open('ex_throughputs') as f:
        for line in f:
            throughputs.append(int(line))
    solve(2)

    
    
