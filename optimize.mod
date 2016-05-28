param LAMBDA := 1;
param MU := 3000;
param MU_S := 3000;

param CHUNKSIZE := 4;
param K := 2;
set C_t := {1200000, 1200000, 1200000};

set BR;
#param BITRATES {k in 1..5} integer;

#set BITRATES{b in 1...5} := b;
set BITRATES;

#var t {K + 1};
var br{k in {1..K}} integer >= 0;

maximize qoe:
  sum{k in 1..K} br[k];

#s.t. choice{k in 1..K}: br[k] = BITRATES[1] or br[k]=BITRATES[2];
#s.t. choice{k in 1..K} := br[k] in BITRATES;
#s.t. bitratehoice: forall{k in 1..K} : br[k] in BITRATES;
#s.t. bitrateChoice{k in 1..K} : br[k] >= 0 or br[k]=2;# in BITRATES;
check: {} within BITRATES;
#s.t. bitrateChoice{k in 1..K} : {} within BITRATES;

solve;

data;

set BR := d du dum dumm dummy;

#printf {k in {1..K}} " %i", br[k];
set BITRATES := 3000000 2000000 1000000 600000 349952;

/*param BITRATES := 1 3000000 
                  2 2000000
		  3 1000000
		  4 600000
		  5 349952;*/


end;
