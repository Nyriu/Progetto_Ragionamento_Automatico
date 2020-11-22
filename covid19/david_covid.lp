% Distribuire i quattro tipi di ospite nelle stanze (2 per tipo tranne osservazione 1 per stanza)
% In corridoi con 2*stanze_per_lato stanze
% Minimizzare numero malati a distanza <= 2 da quarantena e 
%             numero malati a distanza <= 1 da positivi sani

% Stanze valide
stanza(S) :- corridoi(K), stanze_per_lato(H), S=0..2*K*H-1.

%Tipologie:
% 0 malato
% 1 positivo
% 2 osservazione
% 3 quarantena
%tipo(0..3).

% Ad ogni ospite (numero ospite, tipologia) deve essere associata esattamente una stanza
%1 { in_stanza(P,T,S) : stanza(S), tipo(T) } 1 :- soggetto(P,T).
1 { in_stanza(P,T,S) : stanza(S) } 1 :- soggetto(P,T).
%1 { in_stanza(P,S) : stanza(S) } 1 :- soggetto(P,T). % TODO provare cosi'

% Ogni stanza ha capacita' limitata
:- T!=2, in_stanza(P,T,S), in_stanza(P1,T,S),
   in_stanza(P2,T,S),
   P!=P1, P!=P2, P1!=P2.

% Nel caso osservazione limito di piu'
:- T=2, in_stanza(P,T,S), in_stanza(P1,T,S),
   P!=P1.

% No misti
:- in_stanza(P,T,S), in_stanza(P1,T1,S), T!=T1.


% Vicini1 tra malato e (quarantena o positivo)
scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1,S1),
  T!=T1, T!=2, T1!=2, % Sono diversi e nessuno e' osservazione
  T*T1==0,            % almeno uno dei due e' malato
  % Vicini1 % CASO: di fronte
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano
  S == S1 + H*(-1)**(1+ (S/H)\2).   % sono di fronte

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1,S1),
  T!=T1, T!=2, T1!=2, % Sono diversi e nessuno e' osservazione
  T*T1==0,            % almeno uno dei due e' malato
  % Vicini1 % CASO: sopra
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S == S1 +2*H.

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1,S1),
  T!=T1, T!=2, T1!=2, % Sono diversi e nessuno e' osservazione
  T*T1==0,            % almeno uno dei due e' malato
  % Vicini1 % CASO: sotto
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S == S1 -2*H.

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1,S1),
  T!=T1, T!=2, T1!=2, % Sono diversi e nessuno e' osservazione
  T*T1==0,            % almeno uno dei due e' malato
  % Vicini1 % CASO: adiacenti dx
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S/H == S1/H,                      % sul lato dello stesso piano
  S == S1 + 1.                      % a dx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  T!=T1, T!=2, T1!=2, % Sono diversi e nessuno e' osservazione
  T*T1==0,            % almeno uno dei due e' malato
  % Vicini1 % CASO: adiacenti sx
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S/H == S1/H,                      % sul lato dello stesso piano
  S == S1 - 1.                      % a sx






% Vicini2 tra malato e quarantena
scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: sx sx
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  %S/H == S1/H, S2/H == S1/H,       % tutti stesso lato dello stesso piano
  S - 2 == S1,                     % sx
  S - 1 == S2.                     % sx sx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: dx dx
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S/H == S1/H, S2/H == S1/H,        % tutti stesso lato dello stesso piano
  S  + 1 == S2,                     % dx
  S2 + 1 == S1.                     % dx dx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: sx front
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano
  S - 1 == S2,                      % a sx
  S2 == S1 + H*(-1)**(1+ (S2/H)\2). % di fronte al sx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: dx front
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano
  S + 1 == S2,                      % a dx
  S2 == S1 + H*(-1)**(1+ (S2/H)\2). % di fronte al dx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: sx up
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S/H == S2/H,                      % sul lato dello stesso piano
  S - 1 == S2,                      % a sx
  S1 == S2 +2*H.                    % sopra al sx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: dx up
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S/H == S2/H,                      % sul lato dello stesso piano
  S + 1 == S2,                      % a dx
  S1 == S2 +2*H.                    % sopra al dx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: sx down
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S/H == S2/H,                      % sul lato dello stesso piano
  S - 1 == S2,                      % a sx
  S1 == S2 -2*H.                    % sotto al sx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: dx down
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S/H == S2/H,                      % sul lato dello stesso piano
  S + 1 == S2,                      % a dx
  S1 == S2 -2*H.                    % sotto al dx

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: up front
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S2 == S + 2*H, % sopra
  %S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano % TODO
  S2 == S1 + H*(-1)**(1+ (S2/H)\2).  % di fronte al sopra

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: down front
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1, 
  stanze_per_lato(H),
  S2 == S - 2*H, % sotto
  %S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano % TODO
  S2 == S1 + H*(-1)**(1+ (S2/H)\2).  % di fronte al sotto

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: down down
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S1 == S - 4*H. % sotto sotto

scomodo(P,S,P1,S1) :-
  P<P1,
  in_stanza(P,T,S), in_stanza(P1,T1, S1),
  |(T-T1)|==3, % Uno dei due e' quarantena l'altro e' malato
  % Vicini2 % CASO: up up
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S1 == S + 4*H. % sopra sopra

% Symmetry
in_stanza(1,0,0).
% Ai primi malati assegno prime stanze (idem per gli altri)
:- in_stanza(P,T,S), in_stanza(P1,T1,S1), T=T1, P<T1, S>S1.

cost(C) :- C == #count { P,S,P1,S1 : scomodo(P,S,P1,S1) }.
#minimize {C : cost(C)}.


#show corridoi/1.
#show stanze_per_lato/1.
%#show stanza/1.
%#show soggetto/2.
#show in_stanza/3.
%#show scomodo/4.
