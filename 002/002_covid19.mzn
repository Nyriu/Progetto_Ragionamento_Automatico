% Isolamento persone su cociera
% Versione semplificata
%
% N passeggeri
% 1 CORRIDOIO con h camere SINGOLE per lato
% etichette: malato(M) e quarantena(Q)
%
% Vicinato1: camere adj e di fronte
% Vicinato2: Vicinato1 applicato 2 volte
%
% Posizionare gli M in modo che NON siano Vicinato1 o
% Vicinato2 di NESSUN Q
%
%
% Soluzione proposta
% 
% Grafo non orientato con due file di nodi: dispari a sx, pari a dx
% V = {1..2*h}
% E = { (i,j) : 0<i,j<n, j=i+k
%               con k in { -2,-1,1,2,        % ai lati
%                          -h,h,             % di fronte
%                          -h-1,-h+1,h-1,h+1} % ai lati di quello di fronte
%

include "globals.mzn"; 

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
set of int: RoomRange = 1..2*H;
array[RoomRange] of var 0..2: sol;


% Verifico se la camera è vuota
predicate empty(RoomRange: v) =
  (sol[v] == 0);

% Verifico se la camera contiene malato
predicate malato(RoomRange: v) =
  (sol[v] == 1);

% Verifico se la camera contiene quarantena
predicate quarantena(RoomRange: v) =
  (sol[v] == 2);



set of int: ai_lati   = {-2,2}; % ai lati
set of int: di_fronte = {1};    % di fronte (se pari -1 se dispari +1)
%%set of int: kRange = {-2,-1,1,2,         % lati
%%                      -H,H,              % di fronte
%%                      -H-1,-H+1,H-1,H+1  % ai lati di quello di fronte
%%                     };

% true se u vicino1 di v
predicate vicini1(RoomRange: u, RoomRange: v) =
  %exists(k in kRange)(u == v + k);
  exists(k in ai_lati)(u == v + k) \/
  exists(k in di_fronte)(u == v -(-1)^(v mod 2) * k);

% true se u vicino2 di v
predicate vicini2(RoomRange: u, RoomRange: v) =
  exists(v1 in RoomRange)(v != u /\ vicini1(u,v1) /\ vicini1(v1,v));

% Ogni malato/quarantenato deve essere associato ad una stanza
constraint sum(u in RoomRange)(if (malato(u)) then 1 else 0 endif) == M;
constraint sum(u in RoomRange)(if (quarantena(u)) then 1 else 0 endif) == Q;


% Verifico che non ci siano malati v1 o v2 di quarantenati
% Probabilmente altamente inefficiente
constraint forall(u in RoomRange)
  (if (malato(u)) then
    forall(v in RoomRange)
        (not ( quarantena(v) /\ ( vicini1(u,v) \/ vicini2(u,v) ) ))
  endif);
  

%% DEBUGGING
int: mal=1;
constraint sol[mal] == 1;
%% FINE % DEBUGGING



solve satisfy;

output
  %%["Malato     = 1\n"] ++
  %%["Quarantena = 2\n\n"] ++
  %%["P0:\n"] ++
  ["V1(" ++ show(mal) ++ ")= " ] ++
  [show(i) ++ " " | i in RoomRange where (vicini1(mal,i))]
  ++
  ["\n"]
  ++
  ["V2(" ++ show(mal) ++ ")= " ] ++
  [show(i) ++ " " | i in RoomRange where (vicini2(mal,i))]
  ++
  ["\n"]
  ++
  [show(sol[i]) ++
    if (i == 2*H-1 \/ i == 2*H) then "\n" else " " endif |
        i in [j | j in 1..2*H where (j mod 2 == 1)] ++ % prima i dispari (sx)
             [j | j in 1..2*H where (j mod 2 == 0)]    % poi i pari (dx)
  ]
  ;
