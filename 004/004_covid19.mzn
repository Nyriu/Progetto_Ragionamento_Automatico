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
%

include "globals.mzn"; 

int: K; % corridoi/piani
int: H; % stanze per lato
%int: N; % persone

% condizioni delle persone
int: M; % malati
int: P; % positivi
int: O; % osservazione
int: Q; % quarantena precauzionale


%% % Verifico correttezza input
%% constraint M + P + O + Q = N; % ogni persona deve avere esattamente una condizione
%% % FINE % Verifico correttezza input

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

set of int: ospite = 0..4;

% corridoi x stanze x lati
array[RangeCorridoi, RangeStanze, RangeLati] of var ospite: sol;

% Predicati Ausiliari
% True se camera contiene ospite empty/malato(uno o due)/positivo(uno o due)/...
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
  (if malato(k1,s1,l1) then 1 else if malati(k1,s1,l1) then 2 else 0 endif endif) == M;
constraint sum(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if positivo(k1,s1,l1) then 1 else if positivi(k1,s1,l1) then 2 else 0 endif endif) == P;
constraint sum(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if osservazione(k1,s1,l1) then 1 else 0 endif) == O;
constraint sum(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if quarantena(k1,s1,l1) then 1 else if quaranteni(k1,s1,l1) then 2 else 0 endif endif) == Q;


% Verifico che non ci siano malato/i vicini1 o vicini2 di quarantena/i
% Probabilmente altamente inefficiente
% Sarebbe meglio avere funzione che torna i vicini
constraint forall(k1 in RangeCorridoi, s1 in RangeStanze, l1 in RangeLati)
  (if (malato(k1,s1,l1) \/ malati(k1,s1,l1)) then
    forall(k2 in RangeCorridoi, s2 in RangeStanze, l2 in RangeLati)
      (not ( (quarantena(k2,s2,l2) \/ quaranteni(k2,s2,l2))
             /\
             (vicini1(k1,s1,l1, k2,s2,l2) \/ vicini2(k1,s1,l1, k2,s2,l2))
           ))
  endif);
  
%% SYMMETRY
% Specifici del prblema semplificato
%constraint if M>1 then malato(1) endif;
%constraint if Q>1 then quarantena(2*H) endif;

% Per evitare permutazioni
% TODO
% Cercare di max distanza M->Q e min tra M->M e Q->Q

%% FINE % SYMMETRY


%% %% DEBUGGING
%% int: cmal=1;
%% int: mal =1;
%% constraint (sol[cmal,mal] == 1 \/
%%             sol[cmal,mal] == 2);
%% %% %% FINE % DEBUGGING



solve satisfy;

output
  %% %% DEBUGGING
  %% ["("++show(cu)++","++show(u)++") " ++
  %%   if (u == 2*H-1 \/ u == 2*H) then "\n" else " " endif |
  %%       cu in CorridorRange,
  %%       u in [j | j in 1..2*H where (j mod 2 == 1)] ++ % prima i dispari (sx)
  %%            [j | j in 1..2*H where (j mod 2 == 0)]    % poi i pari (dx)
  %% ]
  %% ++
  %% ["\n"]
  %% ++
  %% ["Vicinato1\n"]
  %% ++
  %% ["("++show(cu)++","++show(u)++") " |
  %%       cu in CorridorRange,
  %%       u in RoomRange where (vicini1(cmal,mal,cu,u))
  %% ]
  %% ++
  %% ["\n"]
  %% ++
  %% ["Vicinato2\n"]
  %% ++
  %% ["("++show(cu)++","++show(u)++") " |
  %%       cu in CorridorRange,
  %%       u in RoomRange where (vicini2(cmal,mal,cu,u))
  %% ]
  %% ++
  %% ["\n\n"]
  %% ++
  %% %% FINE % DEBUGGING


  [show(sol[k1,s1,l1]) ++
    if (s1==H) then "\n" else " " endif |
        k1 in RangeCorridoi,
        l1 in RangeLati,
        s1 in RangeStanze
  ]
  ;
