% solver - clingo, online https://potassco.org/clingo/run/
% w zbiorze w rozwiazaniu mamy pet(fish,4) i nat(german,4), czyli Rybki hoduje Niemiec
% zalozenia
house(1..5).
natname(norwegian; english; danish; german; swedish).
colorname(red; green; white; yellow; blue).
drinkname(tea; coffee; milk; beer; water).
smokename(light; unfiltered; menthol; pipe; cigar).
petname(cats; dogs; birds; horses; fish).

% dla kazdego domu jedna cecha
1 { nat(N,H) : natname(N) } 1 :- house(H).
1 { color(C,H) : colorname(C) } 1 :- house(H).
1 { drink(D,H) : drinkname(D) } 1 :- house(H).
1 { smoke(S,H) : smokename(S) } 1 :- house(H).
1 { pet(P,H) : petname(P) } 1 :- house(H).

% kazda cecha tylko w jednym domu
1 { nat(N,H) : house(H) } 1 :- natname(N).
1 { color(C,H) : house(H) } 1 :- colorname(C).
1 { drink(D,H) : house(H) } 1 :- drinkname(D).
1 { smoke(S,H) : house(H) } 1 :- smokename(S).
1 { pet(P,H) : house(H) } 1 :- petname(P).

% sasiedztwo domow
adj(X,Y) :- house(X), house(Y), X+1 = Y.
adj(X,Y) :- house(X), house(Y), X = Y+1.

% info z tresci
nat(norwegian,1).
color(red,H) :- nat(english,H).
color(white,H2) :- color(green,H), H2 = H+1, house(H2).
drink(tea,H) :- nat(danish,H).
:- smoke(light,H1), not 1 { pet(cats,H2) : adj(H1,H2) }.
color(yellow,H) :- smoke(cigar,H).
smoke(pipe,H) :- nat(german,H).
drink(milk,3).
:- smoke(light,H1), not 1 { drink(water,H2) : adj(H1,H2) }.
pet(birds,H) :- smoke(unfiltered,H).
pet(dogs,H) :- nat(swedish,H).
:- nat(norwegian,H1), not 1 { color(blue,H2) : adj(H1,H2) }.
:- pet(horses,H1), not 1 { color(yellow,H2) : adj(H1,H2) }.
drink(beer,H) :- smoke(menthol,H).
drink(coffee,H) :- color(green,H).

% zwierze i narodowosc
#show pet/2.
#show nat/2.