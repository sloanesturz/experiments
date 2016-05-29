param LAMBDA := 1;
param MU := 3000;
param MU_S := 3000;

param CHUNKSIZE := 4;
param K := 2;
set C_t := {1200000, 1200000, 1200000};

set BR;

#set BITRATES;
param BITRATES;

var t {k in {1..K+1}} integer >= 0;
var br{k in {1..K}} integer >= 0;
var buf{k in {1..K}} integer >= 0;
var C{k in {1..K}} integer >= 0; # shouldnt be var

#printf{b in BITRATES}: "bitrate %s\n", b;

maximize qoe:
  sum{k in 1..K} br[k] - 
  LAMBDA * sum{k in 1..K-1} (BITRATES[br[k+1]] - BITRATES[br[k]])
#  - MU *  sum{k in 1..K-1} (CHUNKSIZE * br[k] /
 #     (1.0 / (t[k+1]-t[k]) * sum{t in t[k]..t[k+1]} (C_t[t]))
  #   - buf[k]
  - MU_S * buf[1];

#s.t. choice{k in 1..K}: br[k] = BITRATES[1] or br[k]=BITRATES[2];
#s.t. choice{k in 1..K} := br[k] in BITRATES;
#s.t. bitratehoice: forall{k in 1..K} : br[k] in BITRATES;
#s.t. bitrateChoice{k in 1..K} : br[k] >= 0 or br[k]=2;# in BITRATES;
#set asdf{k in 1..K} := br[k];
#check: {} within BITRATES;
#s.t. bitrateChoice2{k in 1..K} : br[k] >= 349952;
#s.t. bitrateChoice{k in 1..K} : {} within BITRATES;

s.t. bitrateChoice{k in 1..K} : br[k] <= 5;
s.t. bitrateChoice2{k in 1..K} : br[k] >= 0;


#s.t. bufferSizes{k in 1..K-1} : buf[k] - CHUNKSIZE * br[k] / C[k] + CHUNKSIZE - b[k+1] = 0;
#s.t. times{k in 1..K} : t[k] - t[k+1] + CHUNKSIZE * br[k] / C[k] = 0;

solve;

data;


#printf {k in {1..K}} " %i", br[k];
#set BITRATES := 3000000 2000000 1000000 600000 349952;

param BITRATES := 1 3000000 
                  2 2000000
		  3 1000000
		  4 600000
		  5 349952;


end;
