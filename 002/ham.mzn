%% Based on
%% https://ozanerdem.github.io/jekyll/update/2019/12/01/representation-in-csp.html

include "globals.mzn"; 

%% INPUT
array[1..6] of 1..5: source = [1, 1, 2, 3, 3, 4];
array[1..6] of 1..5: target = [3, 5, 5, 4, 5, 2];
%% FINE % INPUT


array[1..5] of var 1..5: path;

predicate edge(int: u, int: v) =
    exists(e in 1..6)(source[e] == u /\ target[e] == v);

predicate precedes(int: u, int: v) =
    exists(i in 1..4)(path[i] == u /\ path[i + 1] == v);

%% (There is not an edge between u and v) => (u cannot precede v)
constraint forall(v1, v2 in 1..5)
    (not edge(v1, v2) -> not precedes(v1, v2));

constraint alldifferent(path);

solve satisfy;
output ["Path: " ++ show(path)]
