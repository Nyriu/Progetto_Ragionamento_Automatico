% Distribuire i quattro tipi di ospite nelle stanze (2 per tipo tranne osservazione 1 per stanza)
% In corridoi con 2*stanze_per_lato stanze
% Minimizzare numero malati a distanza <= 2 da quarantena e 
%             numero malati a distanza <= 1 da positivi sani

% Stanze valide
stanza(S) :- corridoi(K), stanze_per_lato(H), S=0..2*K*H-1.

% Ad ogni ospite deve essere associata esattamente una stanza
1 { malato(M,S)       : stanza(S) } 1 :- malato(M).
1 { positivo(P,S)     : stanza(S) } 1 :- positivo(P).
1 { osservazione(O,S) : stanza(S) } 1 :- osservazione(O).
1 { quarantena(Q,S)   : stanza(S) } 1 :- quarantena(Q).

% Ogni stanza ha capacita' limitata
:- malato(M,S), malato(M1,S), malato(M2,S),             % Al piu' 2 malati
   M!=M1, M!=M2, M1!=M2.
:- positivo(P,S), positivo(P1,S), positivo(P2,S),       % Al piu' 2 positivi
   P!=P1, P!=P2, P1!=P2.
:- osservazione(O,S), osservazione(O1,S), O!=O1.        % Al piu' 1 osservazione
:- quarantena(Q,S), quarantena(Q1,S), quarantena(Q2,S), % Al piu' 2 quarantena
   Q!=Q1, Q!=Q2, Q1!=Q2.

% No misti % TODO migliorabile?
:- malato(M,S), positivo(P,S).
:- malato(M,S), osservazione(O,S).
:- malato(M,S), quarantena(Q,S).

:- positivo(P,S), osservazione(O,S).
:- positivo(P,S), quarantena(Q,S).

:- osservazione(O,S), quarantena(Q,S).


% Symmetry
malato(1,0).
% Ai primi malati assegno prime stanze (idem per gli altri)
:- malato(M,S),       malato(M1,S1),       M<M1, S>S1.
:- positivo(P,S),     positivo(P1,S1),     P<P1, S>S1.
:- osservazione(O,S), osservazione(O1,S1), O<O1, S>S1.
:- quarantena(Q,S),   quarantena(Q1,S1),   Q<Q1, S>S1.
  


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DEBUGGING SKILLZ

%% vicini1
%debug1(10).
%debug1(S,S1) :- vicini1(S,S1), debug1(S).
%#show debug1/2.

%% vicini2
%debug2(10).
%debug2(S,S1) :- vicini2(S,S1), debug2(S).
%#show debug2/2.

%#show stanza/1.
%#show scomodo/4.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%% Vicini 1 tra Malati e Quaranteni %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 
                     % CASO: di fronte
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano
                     S == S1 + H*(-1)**(1+ (S/H)\2).   % sono di fronte

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 
                     % CASO: sopra
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S == S1 +2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 
                     % CASO: sotto
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S == S1 -2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 
                     % CASO: adiacenti dx
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S/H == S1/H,                      % sullo lato dello stesso piano
                     S == S1 + 1.                      % a dx

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 
                     % CASO: adiacenti sx
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S/H == S1/H,                      % sullo lato dello stesso piano
                     S == S1 - 1.                      % a sx



%% Vicini 2 tra Malati e Quaranteni %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1),
%                      % Vicini 2
%                      stanza(S), stanza(S1), S!=S1,
%                      stanza(S2), S!=S2, S2!=S1,
%                      vicini1(S,S2), vicini1(S2,S1).


%%% 
scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: di fronte
                     S/H == S2/H + (-1)**(1+ (S/H)\2),
                     S == S2 + H*(-1)**(1+ (S/H)\2),

                     % CASO: sopra
                     S2 == S1 +2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: di fronte
                     S/H == S2/H + (-1)**(1+ (S/H)\2),
                     S == S2 + H*(-1)**(1+ (S/H)\2),

                     % CASO: sotto
                     S2 == S1 -2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: di fronte
                     S/H == S2/H + (-1)**(1+ (S/H)\2),
                     S == S2 + H*(-1)**(1+ (S/H)\2),

                     % CASO: adiacenti dx
                     S2/H == S1/H,
                     S2 == S1 + 1.


scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: di fronte
                     S/H == S2/H + (-1)**(1+ (S/H)\2),
                     S == S2 + H*(-1)**(1+ (S/H)\2),

                     % CASO: adiacenti sx
                     S2/H == S1/H,
                     S2 == S1 - 1.
%%% 
scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: sopra
                     S == S2 +2*H,

                     % CASO: di fronte
                     S2/H == S/H + (-1)**(1+ (S2/H)\2),
                     S2 == S + H*(-1)**(1+ (S2/H)\2).

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: sopra
                     S == S2 +2*H,

                     % CASO: sotto
                     S2 == S1 -2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: sopra
                     S == S2 +2*H,

                     % CASO: adiacenti dx
                     S2/H == S1/H,
                     S2 == S1 + 1.


scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: sopra
                     S == S2 +2*H,

                     % CASO: adiacenti sx
                     S2/H == S1/H,
                     S2 == S1 - 1.

%%% 
scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),


                     % CASO: sotto
                     S == S2 -2*H,

                     % CASO: di fronte
                     S2/H == S/H + (-1)**(1+ (S2/H)\2),
                     S2 == S + H*(-1)**(1+ (S2/H)\2).

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),


                     % CASO: sotto
                     S == S2 -2*H,

                     % CASO: sopra
                     S2 == S1 +2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),


                     % CASO: sotto
                     S == S2 -2*H,

                     % CASO: adiacenti dx
                     S2/H == S1/H,
                     S2 == S1 + 1.


scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: sotto
                     S == S2 -2*H,

                     % CASO: adiacenti sx
                     S2/H == S1/H,
                     S2 == S1 - 1.

%%% 
scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti dx
                     S/H == S2/H,
                     S == S2 + 1,

                     % CASO: di fronte
                     S2/H == S/H + (-1)**(1+ (S2/H)\2),
                     S2 == S + H*(-1)**(1+ (S2/H)\2).

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti dx
                     S/H == S2/H,
                     S == S2 + 1,

                     % CASO: sopra
                     S2 == S1 +2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti dx
                     S/H == S2/H,
                     S == S2 + 1,


                     % CASO: sotto
                     S2 == S1 -2*H.


scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti dx
                     S/H == S2/H,
                     S == S2 + 1,

                     % CASO: adiacenti sx
                     S2/H == S1/H,
                     S2 == S1 - 1.

%%% 
scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti sx
                     S/H == S2/H,
                     S == S2 - 1,

                     % CASO: sopra
                     S2 == S1 +2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti sx
                     S/H == S2/H,
                     S == S2 - 1,

                     % CASO: sotto
                     S2 == S1 -2*H.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti sx
                     S/H == S2/H,
                     S == S2 - 1,

                     % CASO: adiacenti dx
                     S2/H == S1/H,
                     S2 == S1 + 1.

scomodo(M,Q,S,S1) :- malato(M,S), quarantena(Q,S1), 

                     stanza(S), stanza(S1), S!=S1,
                     stanza(S2), S!=S2, S2!=S1,
                     stanze_per_lato(H),

                     % CASO: adiacenti sx
                     S/H == S2/H,
                     S == S2 - 1,

                     % CASO: di fronte
                     S2/H == S/H + (-1)**(1+ (S2/H)\2),
                     S2 == S + H*(-1)**(1+ (S2/H)\2).






%% Vicini 1 tra Malati e Positivi %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
scomodo(M,Q,S,S1) :- malato(M,S), positivo(Q,S1), 
                     % CASO: di fronte
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano
                     S == S1 + H*(-1)**(1+ (S/H)\2).   % sono di fronte

scomodo(M,Q,S,S1) :- malato(M,S), positivo(Q,S1), 
                     % CASO: sopra
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S == S1 +2*H.

scomodo(M,Q,S,S1) :- malato(M,S), positivo(Q,S1), 
                     % CASO: sotto
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S == S1 -2*H.

scomodo(M,Q,S,S1) :- malato(M,S), positivo(Q,S1), 
                     % CASO: adiacenti dx
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S/H == S1/H,                      % sullo lato dello stesso piano
                     S == S1 + 1.                      % a dx

scomodo(M,Q,S,S1) :- malato(M,S), positivo(Q,S1), 
                     % CASO: adiacenti sx
                     stanza(S), stanza(S1), S!=S1,
                     stanze_per_lato(H),
                     S/H == S1/H,                      % sullo lato dello stesso piano
                     S == S1 - 1.                      % a sx



cost(C) :- C == #count { M,F,S,S1 : scomodo(M,F,S,S1) }.
#minimize {C : cost(C)}.


#show malato/2.
#show positivo/2.
#show osservazione/2.
#show quarantena/2.

% #show scomodo/4.
%#show vicini1/2.
