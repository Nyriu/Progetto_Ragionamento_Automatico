% Isolamento persone su cociera
%
% Crociera con camere doppie
% K corridoi con h camere per lato (h a dx e h a sx)
% corridoi sono uno sopra l'altro con possibilita'
% che i condotti d'aerazione diffondano il virus
% N persone etichettabili con:
%   - malate
%   - positive sane
%   - osservazione (possibile contatto con positivo
%   - quarantena precauzionale
% Possono stare assieme nella stessa stanza:
%   - malati
%   - positivi sani
%   - precauzionali
% Devono stare in isolamento da soli: quelli in osservazione
%
% Definizione di Vicinanaza tra stanze
% Vicinato 1
% Le camere adiacenti, quella di fronte, quelle sopra e sotto
% Ovviamente camere agli estremi dei corridoi e quelle dei corridoi
% 1 e k hanno meno Vicini 1
%
% Vicinato 2
% Applico Vicinato 1 due volte
%
%
% Si vuole disporre le persone per MINIMIZZARE
% numero di malati a distanza <= 2 dai precauzionali e
%                  a distanza <= 1 dai positivi sani
%
% (eventuali vincoli extra su positivi sani)
%




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





