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
% VERSIONE SEMPLIFICATA !
% Fare in modo che NON ci siano malati a distanza <= 2 dai precauzionali
%            e che NON ci siano malati a distanza <= 1 dai positivi sani
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


% Creo la matrice dei posti letto delle stanze dei corridoi
% Stanze con numero dispari sono a sx le altre a dx
% Quindi 1 avra' di fronte 2, 3 avra' davanti 4, ...

% ogni stanza puo' essere occupata da 
% 0 nessuno
% 1 un malato
% 2 un positivo
% 3 un osservazione
% 4 un quarantena precauzionale
% 5 due malati
% 6 due positivi
% 7 due quarantena precauzionale

set of int: tipo_ospite = 0..7;

% corridoi x stanze x lati
array[RangeCorridoi, RangeStanze, RangeLati] of var tipo_ospite: sol;



% Predicati Ausiliari
% True se camera contiene tipo_ospite empty/malato(uno o due)/positivo(uno o due)/...
predicate empty        (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 0);
predicate malato       (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 1);
predicate positivo     (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 2);
predicate osservazione (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 3);
predicate quarantena   (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 4);
predicate malati       (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 5);
predicate positivi     (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 6);
predicate quaranteni   (RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) = (sol[k1,s1,l1] == 7);
  


% True se camere sono Vicinato1
predicate vicini1(RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1,
                  RangeCorridoi: k2, RangeStanze: s2, RangeLati: l2) =
  (abs(k1-k2) == 1 /\ s1 == s2 /\ l1 == l2) \/ % sopra/sotto
  (k1 == k2 /\ abs(s1-s2) == 1 /\ l1 == l2) \/ % affianco
  (k1 == k2 /\ s1 == s2 /\ abs(l1-l2) == 1);   % di fronte

% True se camere sono Vicinato2
predicate vicini2(RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1,
                  RangeCorridoi: k2, RangeStanze: s2, RangeLati: l2) =
  not (k1==k2 /\ s1==s2 /\ l1==l2) /\ 
  exists(k3 in RangeCorridoi, s3 in RangeStanze, l3 in RangeLati)
    (vicini1(k1,s1,l1, k3,s3,l3) /\ (vicini1(k3,s3,l3, k2,s2,l2)))
  ;



% Vincoli
% Ogni malato/positivo/... deve essere associato ad una stanza(solo o con un altro)
constraint sum(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if malato(k1,s1,l1) then 1 elseif malati(k1,s1,l1) then 2 else 0 endif) == M;

constraint sum(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if positivo(k1,s1,l1) then 1 elseif positivi(k1,s1,l1) then 2 else 0 endif) == P;

constraint sum(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if osservazione(k1,s1,l1) then 1 else 0 endif) == O;

constraint sum(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if quarantena(k1,s1,l1) then 1 elseif quaranteni(k1,s1,l1) then 2 else 0 endif) == Q;


% Verifico che non ci siano malato/i vicini1 o vicini2 di quarantena/i
%        e che non ci siano malato/i vicini1 o vicini2 dai positivi
% Probabilmente altamente inefficiente
% Sarebbe meglio avere funzione che torna i vicini1 e 2
constraint forall(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if (malato(k1,s1,l1) \/ malati(k1,s1,l1)) then
    forall(k2 in vicini1_k(k1), s2 in vicini1_s(s1), l2 in vicini1_l(l1))
      (not ( (quarantena(k2,s2,l2) \/ quaranteni(k2,s2,l2)) )
       /\
       not ( (positivo(k2,s2,l2) \/ positivi(k2,s2,l2))
             /\
             (vicini1(k1,s1,l1, k2,s2,l2))
           ))
  endif);
  
% Funzioni Ausiliari
function array[int] of RangeCorridoi: vicini1_k(RangeCorridoi k1) =
  [ if (1 <= k1+d && k-d <= K) | d in -1..1];

function array[int] of RangeStanze: vicini1_s(RangeStanze s1) =
  [ if (1 <= s1+d && s-d <= H) | d in -1..1];
  % TODO!!!
  

% Ritorna l'insieme delle camere in Vicinato1 a quella data
function set of list[3] of int: 
    %TODO
  if     (k1 < K /\ quarantena(k1+1,s1,l1)) then 1 %camera sopra
  elseif (k1 < K /\ quaranteni(k1+1,s1,l1)) then 2 %camera sopra

% q_vicinato1 per ora inutile
function var int: q_vicinato1(RangeCorridoi: k1, RangeStanze: s1, RangeLati: l1) =
  if     (k1 < K /\ quarantena(k1+1,s1,l1)) then 1 %camera sopra
  elseif (k1 < K /\ quaranteni(k1+1,s1,l1)) then 2 %camera sopra
  else 0 endif +

  if     (k1 > 2 /\ quarantena(k1-1,s1,l1)) then 1 %camera sotto
  elseif (k1 > 2 /\ quaranteni(k1-1,s1,l1)) then 2 %camera sotto
  else 0 endif +

  if     (s1 < H /\ quarantena(k1,s1+1,l1)) then 1 %camera da un lato
  elseif (s1 < H /\ quaranteni(k1,s1+1,l1)) then 2 %camera da un lato
  else 0 endif +

  if     (s1 > 2 /\ quarantena(k1,s1-1,l1)) then 1 %camera altro lato
  elseif (s1 > 2 /\ quaranteni(k1,s1-1,l1)) then 2 %camera altro lato
  else 0 endif +

  if     (l1 == 1 /\ quarantena(k1,s1+1,2)) then 1 %camera di fronte caso 1
  elseif (l1 == 1 /\ quaranteni(k1,s1+1,2)) then 2 %camera di fronte caso 1
  elseif (l1 == 2 /\ quarantena(k1,s1-1,1)) then 1 %camera di fronte caso 2
  elseif (l1 == 2 /\ quaranteni(k1,s1-1,1)) then 2 %camera di fronte caso 2
  else 0 endif
  ;

% FINE % Funzioni Ausiliari
  
%% SYMMETRY
% Specifici del prblema semplificato
%constraint if M>1 then malato(1) endif;
%constraint if Q>1 then quarantena(2*H) endif;

% Per evitare rotazioni/specchiamenti
% Potrei fissare un malato sempre nel primo angolo del primo corridoio
% TODO
% Cercare di max distanza M->Q e min tra M->M e Q->Q

%% FINE % SYMMETRY


solve satisfy;

output
  [show(sol[k1,s1,l1])++
    if (s1==H) then "\n" else "  " endif |
        k1 in RangeCorridoi,
        l1 in RangeLati,
        s1 in RangeStanze
  ]
  ;
