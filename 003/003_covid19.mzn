% Isolamento persone su cociera
% Versione semplificata
%
% N passeggeri
% K CORRIDOI con h camere SINGOLE per lato
% etichette: malato(M) e quarantena(Q)
%
% Vicinato1: camere adj, di fronte, sopra e sotto
% Vicinato2: Vicinato1 applicato 2 volte
%
% Posizionare gli M in modo che NON siano Vicinato1 o
% Vicinato2 di NESSUN Q
%

include "globals.mzn"; 

int: K; % corridoi
int: H; % stanze per lato
%%int: N; % persone

% condizioni delle persone
int: M; % malati
int: Q; % quarantena precauzionale

% Verifico correttezza input
%%constraint M + Q = N; % ogni persona deve avere esattamente una condizione
% FINE % Verifico correttezza input



% Nella soluzione assegno ad ogni camera un valore:
% 0 = camera vuota
% 1 = camera con malato
% 2 = camera con quarantenato
set of int: Conditions = 0..2;
set of int: CorridorRange = 1..K;
set of int: RoomRange = 1..2*H;
array[CorridorRange, RoomRange] of var Conditions: sol;


% Verifico se la camera è vuota
predicate empty(CorridorRange: cu, RoomRange: u) =
  (sol[cu,u] == 0);

% Verifico se la camera contiene malato
predicate malato(CorridorRange: cu, RoomRange: u) =
  (sol[cu,u] == 1);

% Verifico se la camera contiene quarantena
predicate quarantena(CorridorRange: cu, RoomRange: u) =
  (sol[cu,u] == 2);



% Ogni stanza indentificata da un numero e da un corridoio (c,cu)
set of int: ai_lati     = {-2,2}; % ai lati
set of int: di_fronte   = {1};    % di fronte (se pari -1 se dispari +1)
set of int: sopra_sotto = {-1, 1};    % di fronte (se pari -1 se dispari +1)

% true se u vicino1 di v
predicate vicini1(CorridorRange: cu, RoomRange: u,
                  CorridorRange: cv, RoomRange: v) =
  if (cu == cv) then
    exists(d in ai_lati)(u == v + d) \/
    exists(d in di_fronte)(u == v -(-1)^(v mod 2) * d)
  else
    u == v /\ 
    exists(d in sopra_sotto)(cu == cv + d)
  endif;

% true se u vicino2 di v
predicate vicini2(CorridorRange: cu, RoomRange: u,
                  CorridorRange: cv, RoomRange: v) =
  exists(cv1 in CorridorRange, v1 in RoomRange)
    ((v != u) /\ vicini1(cu,u,cv1,v1) /\ vicini1(cv1,v1,cv,v));

% Ogni malato/quarantenato deve essere associato ad una stanza
constraint sum(cu in CorridorRange, u in RoomRange)
  (if (malato(cu,u)) then 1 else 0 endif) == M;
constraint sum(cu in CorridorRange, u in RoomRange)
  (if (quarantena(cu,u)) then 1 else 0 endif) == Q;


% Verifico che non ci siano malati v1 o v2 di quarantenati
% Probabilmente altamente inefficiente
constraint forall(cu in CorridorRange, u in RoomRange)
  (if (malato(cu,u)) then
    forall(cv in CorridorRange, v in RoomRange)
        (not ( quarantena(cv,v) /\ ( vicini1(cu,u,cv,v) \/ vicini2(cu,u,cv,v) ) ))
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
int: cmal=1;
int: mal =1;
constraint (sol[cmal,mal] == 1 \/
            sol[cmal,mal] == 2);
%% %% FINE % DEBUGGING



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


  [show(sol[cu,u]) ++
    if (u == 2*H-1 \/ u == 2*H) then "\n" else " " endif |
        cu in CorridorRange,
        u in [j | j in 1..2*H where (j mod 2 == 1)] ++ % prima i dispari (sx)
             [j | j in 1..2*H where (j mod 2 == 0)]    % poi i pari (dx)
  ]
  ;
