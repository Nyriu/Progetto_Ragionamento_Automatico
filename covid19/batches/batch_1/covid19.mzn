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
%   - precauzionali % Devono stare in isolamento da soli: quelli in osservazione
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
%% Si vuole disporre le persone per avere MINIMO
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


% in totale ci sono 2*H*K stanze
% le prime H sono del primo corridio lato dx
% da H..2*H-1 sono del primo corridio lato sx
% da 2*H..3*H-1 sono del secondo corridio lato dx
% ecc...

set of int: stanze = 0..2*H*K-1;

% 
array[1..M] of var stanze: malati;
array[1..P] of var stanze: positivi;
array[1..O] of var stanze: osservazione;
array[1..Q] of var stanze: quarantena;


constraint
  % Al piu' due Malati nella stessa stanza
  forall(i in 1..M)
    (sum(j in i+1..M)
      (if (malati[i]==malati[j]) then 1 else 0 endif) <= 1)

  %at_most1(malati)
  %TODO
  %among(2, malati, stanze)

  /\
  % Al piu' due Positivi nella stessa stanza
  forall(i in 1..P)
    (sum(j in i+1..P)
      (if (positivi[i]==positivi[j]) then 1 else 0 endif) <= 1)
  /\
  % In Osservazione isolati uno per stanza
  alldifferent(osservazione)
  /\
  % Al piu' due Quarantena nella stessa stanza
  forall(i in 1..Q)
    (sum(j in i+1..Q)
      (if (quarantena[i]==quarantena[j]) then 1 else 0 endif) <= 1)
  /\
  % No stanze miste
  % TODO esiste un modo migliore?
  forall(i in 1..M)
    (forall(j in 1..P)(malati[i] != positivi[j]    ) /\
     forall(j in 1..O)(malati[i] != osservazione[j]) /\
     forall(j in 1..Q)(malati[i] != quarantena[j]  ))
  /\
  forall(i in 1..P)
    (forall(j in 1..O)(positivi[i] != osservazione[j]) /\
     forall(j in 1..Q)(positivi[i] != quarantena[j]  ))
  /\
  forall(i in 1..O)
     (forall(j in 1..Q)(osservazione[i] != quarantena[j]))
;

% Date due stanze verifico se sono in reciproco Vicinato1
predicate vicini1(var stanze: s1, var stanze: s2) =
  % Di fronte
  (
    % Sono sullo stesso piano
    (s1 div H == s2 div H + if ((s1 div H) mod 2 == 0) then -1 else 1 endif)
    /\
    % Sono di fronte
    (s1 == s2+H \/ s1 == s2-H)
  )
  \/
  % Sopra/Sotto
  (
    % TODO verificare che un vinocolo qua non serva
    % cfr gli altri casi

    % Sono sopra-sotto
    (s1 == s2+2*H \/ s1 == s2-2*H)
  )
  \/
  % Lato dx/sx
  (
    % Sono sullo stesso lato dello stesso piano
    (s1 div H == s2 div H)
    /\
    % Sono adiacenti
    (s1 == s2+1 \/ s1 == s2-1)
  )
;

% Date due stanze verifico se sono in reciproco Vicinato2
predicate vicini2(var stanze: s1, var stanze: s2) =
  (s1 != s2 /\
  % TODO non mi serve scandire tutte le stanze...
  % mi basta scandire quelle che potrebbero essere vicini1 = num costante
  %% se solo si riuscisse a fare delle cacchio di funzioni che tornino set of int
  %% e non var opt set of int che poi che cavolo vuol dire?!?
   exists (s3 in stanze)
    ( s3 != s1 /\ s3 != s2
      /\
      (vicini1(s1,s3) /\ vicini1(s3,s2))
    ) 
  );


var int: c =
  sum(i in 1..M, j in 1..Q)
    (if (vicini1(malati[i], quarantena[j]) \/
         vicini2(malati[i], quarantena[j]))
     then 1 else 0 endif)
  +
  sum(i in 1..M, j in 1..P)
    (if (vicini1(malati[i], positivi[j]))
     then 1 else 0 endif)
;


% Symmetry

constraint
  (malati[1] == 0)

  % DEBUG
  % DEBUG

  %/\
  %(quarantena[5] == 11)

  % END % DEBUG
  % END % DEBUG

  /\
  increasing(malati)
  /\
  increasing(positivi)
  /\
  increasing(osservazione)
  /\
  increasing(quarantena)
;
  

% solve minimize c;

% solve :: int_search(malati,
%                     dom_w_deg, 
%                     indomain_min,          % best
%                     complete) minimize c;

% solve :: int_search(malati,
%                     dom_w_deg, 
%                     indomain_max,           % poco furbo
%                     complete) minimize c;

% solve :: int_search(malati,
%                     dom_w_deg, 
%                     indomain_split,           % peggio di min
%                     complete) minimize c;

solve :: int_search(malati,
                    input_order, 
                    indomain_min,           % uguale al best
                    complete) minimize c;

%solve :: int_search(quarantena,               % ci mette una vita
%                    input_order, 
%                    indomain_min,
%                    complete) minimize c;

% solve :: int_search(malati,
%                     smallest, 
%                     indomain_min,             % quasi uguale al best
%                     complete) minimize c;



%% solve :: int_search(d, max_regret, indomain_split, complete) minimize distance;

output
  ["{\n"] ++
  [" \"c\":" ++ show(c)] ++
  [",\n"] ++
  [" \"K\":" ++ show(K)] ++
  [",\n"] ++
  [" \"H\":" ++ show(H)] ++
  [",\n"] ++

  [" \"M\":["] ++
  [show(malati[i]) ++ if i==M then "" else "," endif | i in 1..M] ++
  ["],\n"] ++

  [" \"P\":["] ++
  [show(positivi[i]) ++ if i==P then "" else "," endif | i in 1..P] ++
  ["],\n"] ++

  [" \"O\":["] ++
  [show(osservazione[i]) ++ if i==O then "" else "," endif | i in 1..O] ++
  ["],\n"] ++

  [" \"Q\":["] ++
  [show(quarantena[i]) ++ if i==Q then "" else "," endif | i in 1..Q] ++
  ["]\n"] ++

  ["}\n"]
  

  %%% DEBUG
  %%% in minizinc il debug e' la morte... non puoi manco stampare quello che vuoi
  %%++
  %%["Vicini1\n"] ++
  %%[ if i==h then "(" else ")" endif |
  %%  i in 1..M, j in 1..Q
  %%]
  %%++
  %%["\n"]



;


%% % Circa human readable
%% output
%%   ["Malati:\t\t["] ++
%%   [show(malati[i]) ++ if i==M then "" else "," endif | i in 1..M]
%%   ++ ["]\n"] ++
%% 
%%   ["Positivi:\t["] ++
%%   [show(positivi[i]) ++ if i==P then "" else "," endif | i in 1..P]
%%   ++ ["]\n"] ++
%% 
%%   ["Osservazione:\t["] ++
%%   [show(osservazione[i]) ++ if i==O then "" else "," endif | i in 1..O]
%%   ++ ["]\n"] ++
%% 
%%   ["Quarantena:\t["] ++
%%   [show(quarantena[i]) ++ if i==Q then "" else "," endif | i in 1..Q]
%%   ++ ["]\n"]
%% ;
