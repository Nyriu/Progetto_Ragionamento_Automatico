include "globals.mzn"; 

int: M=4;
% Cosi' NON funziona
%array[1..10] of var (int,int,int): malati;
%array[1..10] of var [int,int,int]: malati;
%array[1..10] of var set of int: malati; % questo manda tipo in loop tutto

% dato che si aspetta un set dopo "of"
% ho trovato escamotage...
% posso entrare in profondità per ogni malato
% in posizione 1 metto il corridoio
% in posizione 2 metto la stanza
% in posizione 3 metto il lato
% cosi' e' come se ci fosse una tripletta
array[1..M, 1..3] of var int: malati;


% Richesta stupida giusto
% per vedere se va
var int: s;
constraint s >= 0;
solve minimize s;
