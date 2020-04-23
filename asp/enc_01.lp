% Distribuire malati e quarantena uno per stanza in un corridoio con 2*stanze_per_lato stanze
% Minimizzare numero malati a distanza <= 2 da quarantena

% Stanze valide
stanza(S) :- corridoi(K), stanze_per_lato(H), S=0..2*K*H-1.

% Ad ogni malato/quarantena deve essere associata una stanza
1 { malato(M,S)     : stanza(S) } 1 :- malato(M).
1 { quarantena(Q,S) : stanza(S) } 1 :- quarantena(Q).

% Ogni stanza al piu' un ospite
:- malato(M,S), quarantena(Q,S).
:- malato(M,S), malato(M1,S), M!=M1.
:- quarantena(Q,S), quarantena(Q1,S), Q!=Q1.

% Vicini1
vicini1(S,S1) :-                    % CASO: di fronte
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S/H == S1/H + (-1)**(1+ (S/H)\2), % sullo stesso piano
  S == S1 + H*(-1)**(1+ (S/H)\2).   % sono di fronte

vicini1(S,S1) :-                    % CASO: sopra
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S == S1 +2*H.

vicini1(S,S1) :-                    % CASO: sotto
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S == S1 -2*H.

vicini1(S,S1) :-                    % CASO: adiacenti dx
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S/H == S1/H,                      % sullo lato dello stesso piano
  S == S1 + 1.                      % a dx

vicini1(S,S1) :-                    % CASO: adiacenti sx
  stanza(S), stanza(S1), S!=S1,
  stanze_per_lato(H),
  S/H == S1/H,                      % sullo lato dello stesso piano
  S == S1 - 1.                      % a sx

% Vicini2
vicini2(S,S1) :-
  stanza(S), stanza(S1), S!=S1,
  stanza(S2), S2!=S, S2!=S1,
  vicini1(S,S2), vicini1(S2,S1).
  


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% DEBUGGING SKILLZ

% vicini1
debug1(0).
debug1(S,S1) :- vicini1(S,S1), debug1(S).
#show debug1/2.

%% vicini2
%debug2(1).
%debug2(S,S1) :- vicini2(S,S1), debug2(S).
%#show debug2/2.

%#show stanza/1.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

scomodo(M) :- malato(M,S), quarantena(Q,S1), vicini1(S,S1).
scomodo(M) :- malato(M,S), quarantena(Q,S1), vicini2(S,S1).

#minimize { M : scomodo(M) }.
#show malato/2.
#show quarantena/2.

% Instance
corridoi(1).
stanze_per_lato(2).

malato(2).
quarantena(1).
