from pyOpt import pySNOPT
import pyOpt
import math

LAMBDA = 1
MU = 3000
MU_S = 3000

BITRATES = [3000000, 2000000, 1000000, 600000, 349952]

CHUNKSIZE = 4 * 10**6 # 2 seconds in micro-seconds
CHUNKSIZE = 4
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
    return 1200000 # 1.2 Mbps


# all times are in milliseconds
def solve(K):
    # first numChunks are bitrates, last is startupTime
    def qoe_max(vs):
        t = [0.0] + list(vs[:K]) # times
        if any(t[k+1] - t[k] < 1 for k in range(K)):
            return None, None, 1

        br_i = vs[K: K*2] #bitrate indices
        br = [BITRATES[int(i)-1] for i in br_i]
        buf = vs[K*2: K*3]
        startupTime = buf[0]

        C = [0]* K

        for k in range(K):
            t_k = t[k]
            t_k_1 = t[k+1]
            C[k] =  1.0 / (t_k_1 - t_k) * sum(C_t(dt) for dt in range(int(t_k), int(t_k_1)))
        
        if any(C[k] == 0 for k in range(K)):
            return None, None, 1
        
        f = sum(br) \
            - LAMBDA * sum(abs(br - br_prev) for br, br_prev in zip(br[1:], br)) \
            - MU * sum(CHUNKSIZE * br[k] / C[k] - buf[k] for k in range(K)) \
            - MU_S  * startupTime
        f = -f # maybe?

        print "time", t, "bitrate", br, "buffer", buf, "C", C, "f", f

        g = [0] * (2 * K - 1)

        for k in range(K):
            g[k] = t[k] - t[k+1] + CHUNKSIZE * br[k] / C[k]
        for k in range(K-1):
            g[K+k] = max(0, max(0, buf[k] - CHUNKSIZE * br[k] / C[k]) + CHUNKSIZE) - buf[k+1]
        
        fail = 0
        return f, g, fail

    opt_qoe = pyOpt.Optimization('QOE MAX', qoe_max)
    opt_qoe.addObj('f')
    for k in range(K):
        opt_qoe.addVar('t%d' % k, type='c', lower=0, upper=15, value=1) # right timescale?

    for k in range(K):
        opt_qoe.addVar('b%d' % (K + k), type='d', choices=BITRATES, value=0)

    for k in range(K):
        # buffer can never be bigger than size of video
        opt_qoe.addVar('buf%d' % (2*K + k), type='c', lower=0, upper=CHUNKSIZE*K, value=10)
    
    
    for i in range(2 * K -1):
        opt_qoe.addCon('g%s' % (i+1), 'e')
    
        
    #print opt_qoe
    psqp = pyOpt.ALHSO()
    psqp(opt_qoe, sens_type='FD')
    print opt_qoe.solution(0)

if __name__ == "__main__":
    solve(2)
