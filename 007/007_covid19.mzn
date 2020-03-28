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
%% Si vuole disporre le persone per MINIMIZZARE
%% numero di malati a distanza <= 2 dai precauzionali e
%%                  a distanza <= 1 dai positivi sani
%%
%% (eventuali vincoli extra su positivi sani)
%

include "globals.mzn"; 

int: K; % corridoi/piani
int: H; % stanze per lato

% condizioni delle persone
int: M; % malati
int: P; % positivi
int: O; % osservazione
int: Q; % quarantena precauzionale


set of int: RangeCorridoi = 1..K;
set of int: RangeStanze   = 1..H;
set of int: RangeLati     = 1..2;

% dato che si aspetta un set dopo "of"
% ho trovato escamotage...
% posso entrare in profondità per ogni malato
% in posizione 1 metto il corridoio
% in posizione 2 metto la stanza
% in posizione 3 metto il lato
% cosi' e' come se ci fosse una tripletta
array[1..M, 1..3] of var int: malati;
array[1..P, 1..3] of var int: positivi;
array[1..O, 1..3] of var int: osservazione;
array[1..Q, 1..3] of var int: quarantena;


% TODO ampliare
% Per ora una camera per ospite
constraint alldifferent(malati);




%% %% DEBUG STUFF
%% int: kx=2;
%% int: sx=2;
%% int: lx=2;
%% %% END %DEBUG STUFF

% Richesta stupida giusto
% per vedere se va
var int: s;
constraint s >= 0;
solve minimize s;


output

  %% %% DEBUG STUFF
  %% ["Considero ("++ show(kx) ++","++ show(sx)++","++ show(lx) ++")\n"]++
  %% ["Vicini1\n"]++
  %% [ if (vicini1(kx,sx,lx, k2,s2,l2)) then
  %%   "("++ show(k2) ++","++ show(s2)++","++ show(l2) ++") " else "" endif 
  %%   | k2 in vicini1_k(kx), s2 in vicini1_s(sx), l2 in vicini1_l(lx)
  %% ]

  %% ++["\n"]++

  %% ["Vicini2\n"]++
  %% [ if (vicini2(kx,sx,lx, k3,s3,l3)) then
  %%   "("++ show(k3) ++","++ show(s3)++","++ show(l3) ++") " else "" endif 
  %%   | k3 in vicini2_k(kx), s3 in vicini2_s(sx), l3 in vicini2_l(lx)
  %% ]
  %% ++["\n"]++

  %% ["Vicini2 Forall\n"]++
  %% [ if (vicini2(kx,sx,lx, k3,s3,l3)) then
  %%   "("++ show(k3) ++","++ show(s3)++","++ show(l3) ++") " else "" endif 
  %%   | k3 in RangeCorridoi, s3 in RangeStanze, l3 in RangeLati
  %% ]
  %%  ++["\n"]++
  %%  ["Vicini2 True\n"]++
  %%  %%[ if (vicini2(kx,sx,lx, k3,s3,l3)) then
  %%  [ if (true) then
  %%    "("++ show(k3) ++","++ show(s3)++","++ show(l3) ++") " else "" endif 
  %%    | k3 in vicini2_k(kx), s3 in vicini2_s(sx), l3 in vicini2_l(lx)
  %%  ]
  %% ++["\n\n"]++
  %% %% END %DEBUG STUFF

  ["ROBA:"++ show(s) ++"\n"]
  ++
  [show(malati[i,j]) ++"\n"]
  ;
