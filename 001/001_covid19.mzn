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

int: K; % corridoi/piani
int: H; % stanze per lato
int: N; % persone

% condizioni delle persone
int: M; % malati
int: P; % positivi
int: O; % osservazione
int: Q; % quarantena precauzionale


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

constraint
  % Ogni persona deve essere associata ad un letto
  ( sum( i in RangeCorridoi,
         j in RangeStanze,
         k in RangeLetti)
       (if letto[i,j,k] > 0 then 1 else 0 endif)
  ) = N;
constraint
  % Ogni persona deve mantenere la sua condizione
  % Caso: malato
  ( sum( i in RangeCorridoi,
         j in RangeStanze,
         k in RangeLetti)
       (if letto[i,j,k] = 1 then 1 else 0 endif) % 
  ) = M;
constraint
  % Caso: positivo
  ( sum( i in RangeCorridoi,
         j in RangeStanze,
         k in RangeLetti)
       (if letto[i,j,k] = 2 then 1 else 0 endif) % 
  ) = P;
constraint
  % Caso: osservazione
  ( sum( i in RangeCorridoi,
         j in RangeStanze,
         k in RangeLetti)
       (if letto[i,j,k] = 3 then 1 else 0 endif) % 
  ) = O;
constraint
  % Caso: quarantena precauzionale
  ( sum( i in RangeCorridoi,
         j in RangeStanze,
         k in RangeLetti)
       (if letto[i,j,k] = 4 then 1 else 0 endif) % 
  ) = Q;




% - Voglio minimizzare il numero di malati a distanza <= 2 dai precauzionali
int malati_scomodi =
  % distanza 1 da precauzionale
  ( sum( i in RangeCorridoi,
         j in RangeStanze,
         k in RangeLetti)
       (
        % Considero i malati
        if letto[i,j,k] = 1
        then
          % se precauzionale di fronte
          if (
              ((j mod 2 = 1) /\ (letto[i,j+1,1] = 4 \/ letto[i,j+1,2] = 4))
              \/
              ((j mod 2 = 0) /\ (letto[i,j-1,1] = 4 \/ letto[i,j-1,2] = 4))
              )
then 1
        else 0 endif)

        endif)
  ) = N;
  % distanza 2 da precauzionale





%solve satisfy;
solve minimize malati_scomodi;
