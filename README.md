# DOCE.AI 
This is an AI for a board game DOCE
The executable is in DOCE_Final.py and final development version is in DOCE_Final.ipynb.
A Human player, A Random Player and a smart AI player is implemented in this game

### Implementation of AI

The AI player was implemented using the Minimax algorithm using alpha-beta pruning.
Also, the evaluation function is used to check the goodness of the move by returning an evaluation value.

The max function is called before AI takes any decision to move. The max function returns values such as:
Row and column number of the move.
The dice number to face up.
The value from the evaluation function.
The value from the evaluation function is the value used to decide the best possible move.
The max depth that the minimax algorithm goes to right now is set at 3.


To place the blocker, we implemented it a little differently. 
The blocker can be placed only once, so we keep track of the blocker and only check the possible move for the blocker while blockCount=0. The blocker is placed if :
We can’t place our dice where the opponent is winning.
There are two possible places where the opponent is winning and it places where we can’t place our dice
We are not winning the game before we place the blocker.
To do this, a function is called that returns all the valid places where the opponent can place a dice and win. And, blocker is placed at a place whose conditions satisfies as above.

For the best placement, the minimax() function is called which performs every combination of placement of both the maximizing player and the minimizing player on the board. The function returns the best placement position for AI. It also analyzes what face of the die should be facing up so that the results are best possible for AI. The max function is provided with the current state of the board, player’s turn, previous move of the AI, previous move of the user, count of user’s turn, count of AI’s turn, depth, and the values of alpha and beta. The minimax function, after getting the best value from the evaluation function, returns the best position for placement of the AI. Along with the best position, it returns the best value of the die to place, and the value it received from the evaluation function.  Small description of the max function is as follows:
If the function reaches the maximum depth provided, or if the state of the board is terminal, then it returns the current maximum value provided by the state.
If not terminal, or max depth reached, it will place every combination of dice into each possible position for AI, and then the user, calling the min back to back.
If alpha value is greater than beta in any situation, it performs alpha-beta pruning and returns the maximum state of the board.
Alpha-beta pruning in the minimax function happens when the updated alpha value is greater than or equal to the beta value i.e. the function, when receives the alpha value that is greater or equal to the beta value, will not have to traverse to every possible position as it has already received the best possible value maximizer function can guarantee. 

Evaluation function punishes or rewards AI for every move that it predicts. The evaluation function is constructed such that it tries to build up every possible trap on the board until the board is in the terminal condition for it to win. If the situation is such that the user wins in the next turn, it places the die such that the user will have a hard time winning. The evaluation function is strictly offensive and will barely play for a tie.

For the building up process for AI, the value that returns from the evaluation function switches between 5 and -5. If the AI is winning in the current state of the board, the evaluation function returns a positive 10 whilst returns negative 10 if the user has their next move winning in the current state. Thus, if the evaluation function returns 10, the minimax function will place the die on the winning position with the correct die. If the evaluation function returns -10, the minimax function will place the die in such a manner that it blocks the user from winning the game if blocker is not available or the blocker’s conditions don’t satisfy.

Some of the heuristics that we used are to place the dice 3 in the board position (3,3) if it is available in the very first step, if not, at the top-left corner and if this is not available too, then place it at the top-right corner of the board. 





### Sample Output that shows the result of 100 games between the random player and AI

Random:  0
Ace (AI):  99
TIE:  1





