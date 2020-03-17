 % Knapsack by AD
 
int: n=11;

array [1..n] of int: weight= [1, 2, 4, 8,16,32, 64,128,256,512,1024];
array [1..n] of int: cost  = [1, 3, 7,15,31,63,127,255,511,1023,2047];

%%% Examples (of "yes" limits)
% 127, 247
% 255, 502
% 511, 1013
% 1023, 2036

int: space  =1023;
var int: profit; %% =2037;

array [1..n] of var 0..100: sol; % 0..1 in the standard case

constraint
    sum(i in 1..n)(sol[i]*weight[i]) <=  space
/\
    sum(i in 1..n)(sol[i]*cost[i]) =  profit
;


    
solve maximize profit;
%satisfy;
 
output[
  show(sol) ++ show(profit)
] ;





