"""This file contains all the classes you must complete for this project.

You can use the test cases in agent_test.py to help during development, and
augment the test suite with your own test cases to further test your code.

You must test your agent's strength against a set of agents with known
relative strength using tournament.py and include the results in your report.
"""


class Timeout(Exception):
    """Subclass base exception for code clarity."""
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    return privilege_center(game, player)


def difference_of_moves(game, player):
    """
    Heuristic 1: simple evaluation of my moves versus the adversary moves, applying some "aggressiveness" factor.
    The number chosen below was a result of some empirical tests, which pointed that being more aggressive presented
    better final results.
    """
    AGGR_RATIO = 2.2
    my_moves = len(game.get_legal_moves(player))
    adv_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves - AGGR_RATIO * adv_moves)


def final_countdown(game, player):
    """
    Heuristic 2: be cool in the beginning and try to be aggressive in the end of the game. Try to 
    run this listening 'The Final Countdown'... "pararan-ran  parara-raran"... it's the final sprint. :)
    """
    AGGRESSIVE_START = 1.5
    AGGRESSIVE_END = 3.2
    FINAL_APPROACHING_BOUNDARY = 1 / 3

    my_moves = len(game.get_legal_moves(player))
    adv_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # We define if the end is going to the end comparing the number of blank spaces
    if len(game.get_blank_spaces()) > (game.width * game.height) * FINAL_APPROACHING_BOUNDARY:
        return float(my_moves - AGGRESSIVE_START * adv_moves)
    else:
        return float(my_moves - AGGRESSIVE_END * adv_moves)


def privilege_center(game, player):
    """
    Heuristic 1: simple evaluation of my moves versus the adversary moves, applying some "aggressiveness" factor.
    The number chosen below was a result of some empirical tests, which pointed that being more aggressive presented
    better final results.
        ** Modified to privilege the center of the board.
    """
    AGGR_RATIO = 2
    bonus = 0.

    center = (int(game.width/2), int(game.height/2))
    r, c = center
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    off_center = [(r + dr, c + dc) for dr, dc in directions
                  if 0 <= r + dr < game.height and 0 <= c + dc < game.width]
    player_location = game.get_player_location(player)
    if player_location == center:
        bonus = 1.5
    elif player_location in off_center:
            bonus = 0.5
    my_moves = len(game.get_legal_moves(player))
    adv_moves = len(game.get_legal_moves(game.get_opponent(player)))
    return float(my_moves - AGGR_RATIO * adv_moves) + bonus


def final_countdown_with_center(game, player):
    """
    Heuristic 2: be cool in the beginning and try to be aggressive in the end of the game. Try to 
    run this listening 'The Final Countdown'... "pararan-ran  parara-raran"... it's the final sprint. :)
       ** Modified to privilege the center.
    """
    AGGRESSIVE_START = 1.5
    AGGRESSIVE_END = 3.2
    FINAL_APPROACHING_BOUNDARY = 1 / 3

    bonus = 0.

    center = (int(game.width / 2), int(game.height / 2))
    r, c = center
    directions = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    off_center = [(r + dr, c + dc) for dr, dc in directions
                  if 0 <= r + dr < game.height and 0 <= c + dc < game.width]
    player_location = game.get_player_location(player)
    if player_location == center:
        bonus = 2.0
    elif player_location in off_center:
        bonus = 0.1

    my_moves = len(game.get_legal_moves(player))
    adv_moves = len(game.get_legal_moves(game.get_opponent(player)))

    # We define if the end is going to the end comparing the number of blank spaces
    if len(game.get_blank_spaces()) > (game.width * game.height) * FINAL_APPROACHING_BOUNDARY:
        return float(my_moves - AGGRESSIVE_START * adv_moves) + bonus
    else:
        return float(my_moves - AGGRESSIVE_END * adv_moves) + bonus


def run_from_the_adversary(game, player):
    """
    Heuristic 3: this strategy focuses on running from the adversary assuming that, with this movement, there are more 
     chances of legal movements and winning.
    """
    my_location = game.get_player_location(player)
    adv_location = game.get_player_location(game.get_opponent(player))
    distance = abs(my_location[0] - adv_location[0]) + abs(my_location[1] - adv_location[1])

    return float(distance)


class CustomPlayer:
    """Game-playing agent that chooses a move using your evaluation function
    and a depth-limited minimax algorithm with alpha-beta pruning. You must
    finish and test this player to make sure it properly uses minimax and
    alpha-beta to return a good move before the search time limit expires.

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    iterative : boolean (optional)
        Flag indicating whether to perform fixed-depth search (False) or
        iterative deepening search (True).

    method : {'minimax', 'alphabeta'} (optional)
        The name of the search method to use in get_move().

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score,
                 iterative=True, method='minimax', timeout=10.):
        self.search_depth = search_depth
        self.iterative = iterative
        self.score = score_fn
        self.method = method
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, legal_moves, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        This function must perform iterative deepening if self.iterative=True,
        and it must use the search method (minimax or alphabeta) corresponding
        to the self.method value.

        **********************************************************************
        NOTE: If time_left < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        legal_moves : list<(int, int)>
            A list containing legal moves. Moves are encoded as tuples of pairs
            of ints defining the next (row, col) for the agent to occupy.

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """

        self.time_left = time_left

        final_board = (-1, -1)
        if not legal_moves:
            return (-1, -1)

        # Perform any required initializations, including selecting an initial
        # move from the game board (i.e., an opening book), or returning
        # immediately if there are no legal moves
        depth = 1 if self.iterative else self.search_depth

        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            board_choice = final_board
            while True:
                if self.method == "minimax":
                    _, board_choice = self.minimax(game, depth)

                elif self.method == "alphabeta":
                    _, board_choice = self.alphabeta(game, depth)
                final_board = board_choice

                if not self.iterative:
                    break

                depth += 1

        except Timeout:
            # Handle any actions required at timeout, if necessary
            pass

        # Return the best move from the last completed search iteration
        return final_board

    def minimax(self, game, depth, maximizing_player=True):
        """Implement the minimax search algorithm as described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Minimax implementation following reference of algorithm in "Artifical Intelligence 3rd ed" book, Chapter 5.
        # pseudocode available in https://github.com/aimacode/aima-pseudocode
        actions = game.get_legal_moves()

        # Stop condition - reaching the depth defined or having no more legal moves possible
        if depth <= 0 or not actions:
            return self.score(game, self), None

        action = None

        if maximizing_player:
            # Calling the max_value
            value = float("-inf")
            for a in actions:
                next_state = game.forecast_move(a)
                next_value, _ = self.minimax(next_state, depth - 1, False)  # Time to call min, only using the best value
                if next_value > value:
                    value = next_value
                    action = a
        else:
            # Calling the min_value
            value = float("inf")
            for a in actions:
                next_state = game.forecast_move(a)
                next_value, _ = self.minimax(next_state, depth - 1, True)  # Time to call min, only using the best value
                if next_value < value:
                    value = next_value
                    action = a

        return value, action


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf"), maximizing_player=True):
        """Implement minimax search with alpha-beta pruning as described in the
        lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        maximizing_player : bool
            Flag indicating whether the current search depth corresponds to a
            maximizing layer (True) or a minimizing layer (False)

        Returns
        -------
        float
            The score for the current search branch

        tuple(int, int)
            The best move for the current branch; (-1, -1) for no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project unit tests; you cannot call any other
                evaluation function directly.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise Timeout()

        # Alpha-beta pruning following reference in "Artifical Intelligence 3rd ed" book, Chapter 5, page 170.
        # The code is similar to minimax, except for the lines related to alpha e beta.
        legal_moves = game.get_legal_moves()

        # Stop condition - reaching the depth defined or having no more legal moves possible
        if depth <= 0 or not legal_moves:
            return self.score(game, self), None

        action = None

        if maximizing_player:
            value = float("-inf")
            for a in legal_moves:
                next_state = game.forecast_move(a)
                next_value, _ = self.alphabeta(next_state, depth - 1, alpha, beta, False)
                alpha = max(alpha, next_value)
                if next_value > value:
                    value = next_value
                    action = a
                if alpha >= beta:
                    break
        else:
            value = float("inf")
            for a in legal_moves:
                next_state = game.forecast_move(a)
                next_value, _ = self.alphabeta(next_state, depth - 1, alpha, beta, True)
                beta = min(beta, next_value)
                if next_value < value:
                    value = next_value
                    action = a
                if alpha >= beta:  # TODO: evaluate this code
                    break

        return value, action
