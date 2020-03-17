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

include "globals.mzn"; 

%============================================================%
% INPUT 1

int: K=2; % corridoi/piani
int: H=3; % stanze per lato
int: N=10; % persone

% condizioni delle persone
int: M = 4; % malati
int: P = 3; % positivi
int: O = 1; % osservazione
int: Q = 2; % quarantena precauzionale

% FINE % INPUT 1
%============================================================%

%%============================================================%
%% INPUT 2
%
%int: K=2; % corridoi/piani
%int: H=3; % stanze per lato
%int: N=10; % persone
%
%% condizioni delle persone
%int: M = 10; % malati
%int: P = 0; % positivi
%int: O = 0; % osservazione
%int: Q = 0; % quarantena precauzionale
%
%% FINE % INPUT 2
%%============================================================%

% Verifico correttezza input
constraint M + P + O + Q = N; % ogni persona deve avere esattamente una condizione
% FINE % Verifico correttezza input

set of int: RangeCorridoi = 1..K;
set of int: RangeStanze   = 1..2*H;
set of int: RangeLetti    = 1..2;


% Creo la matrice dei posti letto delle stanze dei corridoi
% Stanze con numero dispari sono a sx le altre a dx
% Quindi 1 avra' di fronte 2, 3 avra' davanti 4, ...

% ogni letto puo' essere occupato da 
% 0 nessuno
% 1 malato
% 2 positivo
% 3 osservazione
% 4 quarantena precauzionale
set of int: labels = 0..4;

% corridoi x stanze x posti letto
array[RangeCorridoi, RangeStanze, RangeLetti] of var labels: letto;


% Per ora
% - Considero solo stanze a destra e a sinistra
% - Voglio minimizzare il numero di malati a distanza <= 2 dai precauzionali

%% constraint forall(i in RangeCorridoi, j in RangeStanze, k in RangeLetti) (t[i,0] = left);
constraint
 (
  sum( i in RangeCorridoi,
       j in RangeStanze,
       k in RangeLetti)
     (letto[i,j,k] div 4) % 
 ) = N;











%solve minimize profit;
solve satisfy;
