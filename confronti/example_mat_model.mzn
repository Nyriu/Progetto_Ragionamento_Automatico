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


% Funzioni Ausiliari
%%function set of RangeCorridoi: vicini1_k(RangeCorridoi k1) =
function set of RangeCorridoi: vicini1_k(RangeCorridoi: k1) =
  { if (1 <= k1+d /\ k1+d <= K) then k1+d else k1 endif | d in -1..1};

function set of RangeStanze: vicini1_s(RangeStanze: s1) =
  { if (1 <= s1+d /\ s1+d <= H) then s1+d else s1 endif | d in -1..1};

function set of RangeLati: vicini1_l(RangeLati: l1) =
  {1,2};

function set of RangeCorridoi: vicini2_k(RangeCorridoi: k1) =
  { k3
  | k2 in vicini1_k(k1), k3 in vicini1_k(k2)
  };

function set of RangeStanze: vicini2_s(RangeStanze: s1) =
  { s3
  | s2 in vicini1_s(s1), s3 in vicini1_s(s2)
  };

function set of RangeLati: vicini2_l(RangeLati: l1) =
  {1,2};
% FINE % Funzioni Ausiliari


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
  exists(k3 in vicini1_k(k1), s3 in vicini1_s(s1), l3 in vicini1_l(l1))
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


% Conto il numero di stanze con almeno un M a dist <= 2 da stanze con almeno un Q
% e quelle con almeno un M a dist <= 1 da stanze con almeno un P
var int: c;
constraint c =
% TODO ottimizzare
%%forall(k2 in vicini1_k(k1), s2 in vicini1_s(s1), l2 in vicini1_l(l1))
sum([
      if ( (malato(k1,s1,l1) \/
            malati(k1,s1,l1)
           ) /\
           (quarantena(k2,s2,l2) \/
            quaranteni(k2,s2,l2) \/
            positivo(k2,s2,l2)   \/
            positivi(k2,s2,l2)
           ) /\
           vicini1(k1,s1,l1, k2,s2,l2)
         ) then 1 else 0
      endif
      | k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati,
        k2 in vicini1_k(k1), s2 in vicini1_s(s1), l2 in vicini1_l(l1)
    ])
+
sum([
      if ( (malato(k1,s1,l1) \/
            malati(k1,s1,l1)
           ) /\
           (quarantena(k2,s2,l2) \/
            quaranteni(k2,s2,l2)
           ) /\
           vicini2(k1,s1,l1, k2,s2,l2)
         ) then 1 else 0
      endif
      | k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati,
        k2 in vicini2_k(k1), s2 in vicini2_s(s1), l2 in vicini2_l(l1)
    ]);
  
  


%% SYMMETRY % TODO

%% Fissare un malato o due in (1,1,1)
constraint (sol[1,1,1]==1 \/ sol[1,1,1]==5);


% Specifici del prblema semplificato
%constraint if M>1 then malato(1) endif;
%constraint if Q>1 then quarantena(2*H) endif;

% Per evitare rotazioni/specchiamenti
% Potrei fissare un malato sempre nel primo angolo del primo corridoio
% TODO
% Cercare di max distanza M->Q e min tra M->M e Q->Q

%% FINE % SYMMETRY

%% %% DEBUG STUFF
%% int: kx=2;
%% int: sx=2;
%% int: lx=2;
%% %% END %DEBUG STUFF


solve minimize c;

%% output
%% 
%%   %% %% DEBUG STUFF
%%   %% ["Considero ("++ show(kx) ++","++ show(sx)++","++ show(lx) ++")\n"]++
%%   %% ["Vicini1\n"]++
%%   %% [ if (vicini1(kx,sx,lx, k2,s2,l2)) then
%%   %%   "("++ show(k2) ++","++ show(s2)++","++ show(l2) ++") " else "" endif 
%%   %%   | k2 in vicini1_k(kx), s2 in vicini1_s(sx), l2 in vicini1_l(lx)
%%   %% ]
%% 
%%   %% ++["\n"]++
%% 
%%   %% ["Vicini2\n"]++
%%   %% [ if (vicini2(kx,sx,lx, k3,s3,l3)) then
%%   %%   "("++ show(k3) ++","++ show(s3)++","++ show(l3) ++") " else "" endif 
%%   %%   | k3 in vicini2_k(kx), s3 in vicini2_s(sx), l3 in vicini2_l(lx)
%%   %% ]
%%   %% ++["\n"]++
%% 
%%   %% ["Vicini2 Forall\n"]++
%%   %% [ if (vicini2(kx,sx,lx, k3,s3,l3)) then
%%   %%   "("++ show(k3) ++","++ show(s3)++","++ show(l3) ++") " else "" endif 
%%   %%   | k3 in RangeCorridoi, s3 in RangeStanze, l3 in RangeLati
%%   %% ]
%%   %%  ++["\n"]++
%%   %%  ["Vicini2 True\n"]++
%%   %%  %%[ if (vicini2(kx,sx,lx, k3,s3,l3)) then
%%   %%  [ if (true) then
%%   %%    "("++ show(k3) ++","++ show(s3)++","++ show(l3) ++") " else "" endif 
%%   %%    | k3 in vicini2_k(kx), s3 in vicini2_s(sx), l3 in vicini2_l(lx)
%%   %%  ]
%%   %% ++["\n\n"]++
%%   %% %% END %DEBUG STUFF
%% 
%%   ["Valore:"++ show(c) ++"\n"]
%%   ++
%%   [" "++ show(sol[k1,s1,l1])++
%%     if (s1==H) then "\n" else " " endif |
%%         k1 in RangeCorridoi,
%%         l1 in RangeLati,
%%         s1 in RangeStanze
%%   ]
%%   ;
