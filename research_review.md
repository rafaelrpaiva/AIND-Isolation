
### Research Review

The purpose of this file is present a simple one page summary about a seminal paper in the field of Game-Playing. For that, the article selected was **Deep Blue**[1] by the IBM Watson Team.

#### Goals and Techniques

This paper presents all process throughout Deep Blue, a massive parallel system designed for carrying out chess game tree searches and organized in three layers. One of the SP processors is designated as the master, and the remainder as workers. The master searches the top levels of the chess game tree, and then distributes "leaf" positions to the workers for further examination. The workers carry out a few levels of additional search, and then distribute their leaf positions to the chess chips, which search the last few levels of the tree. 
Deep Blue adopted many of the ideas developed in earlier chess programs, including quiescence search, iterative deepening, transposition tables (a technique used to speed up the search of the game tree) and NegaScout, "an algorithm that can be faster than alpha-beta pruning, because, despite being a directional search algorithm for computing the minimax value of a node in a tree, it never examines a node that can be pruned by alpha-beta; however, it relies on accurate node ordering to capitalize on this advantage"[2].

Even using classical techniques, Deep Blue has some characteristics that reveal its success:

1. Large searching capacity, prepared for a non-uniform search and to provide "insurance" against simple errors.

2. Evaluation function implemented in hardware, including the strategy of "fast evaluation" and "slow evaluation"

3. Hybrid software/hardware search, including the usage of a chess chip and the adoption of a new technique  called "dual credit with delayed extensions". For this point, a large set of mechanisms helped to identify nodes that should receive credit, like a singular move, mate threats and so forth.

4. Massively parallel search, with over 500 processors.

It is interesting to highlight that the evaluation function was essentially a sum of feature values, since the chess chip recognizes roughly 8000 different "patterns", and each is assigned a value. There are 54 registers  and 8096 table entries (see Table 5) for a total of 8150 parameters that can be set in the Deep Blue evaluation function, focusing on some typical strategies from the chess game, like "pinned and hung", "Queen trap", "Bishop pair", "Rooks on files" etc.

Finally, other important aspects included the opening book, a extended book to influence and direct next play in the absence if opening book information, endgame databases and time control mechanisms.

#### Results

The article doesn't analyses specific results, but the matches were highly broadcasted around the world:

- **Deep Thought 2** performed several events from 1991 through 1995, including victories in the 1991 and 1994 ACM Computer Chess Championships, and a 3-1 win against the Danish national team in 1993.

- **Deep Blue I** played only six games under tournament conditions, all in the February 1996 match with Garry Kasparov, who won by a fairly decisive 4-2 score, although the match was tied at 2-2 after the first four games.

- Finally, in 1997, **Deep Blue II** defeated Garry Kasparov in a match by a score of 3.5-2.5, being awarded the Fredkin prize for defeating the human world champion in a regulation match.

#### References
[1] Murray Campbell, A. Joseph Hoane Jr., Feng-hsiung Hsu. Deep Blue. Artifical Intelligence 134, 2002.

[2] Principal Variation Search, Wikipedia. `https://en.wikipedia.org/wiki/Principal_variation_search`