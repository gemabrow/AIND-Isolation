"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import numpy as np


# LM_COEFF = 0.8
# TM_COEFF = 0.75
# OP_M_COEFF = 1
MOVEMENT_VECTORS = [(1, -2), (1, 2), (-2, -1), (-2, 1),
                    (-1, -2), (-1, 2), (2, -1), (2, 1)]


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def get_tertiary_moves(game, legal_moves):
    """Using MOVEMENT_VECTORS, return the list of unoccupied positions
    """
    tertiary_moves = {(lm_y + v_y, lm_x + v_x)
                      for v_y, v_x in MOVEMENT_VECTORS
                      for lm_y, lm_x in legal_moves
                      if game.move_is_legal((lm_y + v_y, lm_x + v_x))}
    return tertiary_moves


def get_manhattan_distance(position_a, position_b):
    """Calculates the discrete manhattan distance between
    two (y, x) tuples and returns this value
    """
    y_a, x_a = position_a
    y_b, x_b = position_b
    return abs(y_a - y_b) + abs(x_a - x_b)


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

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
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    player_pos = game.get_player_location(player)
    legal_moves = game.get_legal_moves(player)
    tertiary_moves = get_tertiary_moves(game, legal_moves)
    opponent = game.get_opponent(player)
    opponent_pos = game.get_player_location(opponent)
    opponent_moves = game.get_legal_moves(opponent)
    # 0.375 to 0.5
    return (len(legal_moves)
            + 0.5 * float(len(tertiary_moves)
                            / get_manhattan_distance(player_pos, opponent_pos))
            - len(opponent_moves))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters6
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
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")
    opponent = game.get_opponent(player)
    player_pos = game.get_player_location(player)
    opponent_pos = game.get_player_location(opponent)

    return float(len(game.get_legal_moves(player))**2
                 / (get_manhattan_distance(player_pos, opponent_pos)
                    + len(game.get_legal_moves(opponent))**2))


def custom_score_3(game, player):
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
    if game.is_winner(player):
        return float("inf")
    if game.is_loser(player):
        return float("-inf")

    player_pos = game.get_player_location(player)
    legal_moves = game.get_legal_moves(player)
    tertiary_moves = get_tertiary_moves(game, legal_moves)
    opponent = game.get_opponent(player)
    opponent_pos = game.get_player_location(opponent)
    # 0.5 * len(legal_moves) + len(tertiary_moves) for numerator
    return (float((0.5 * len(legal_moves) + len(tertiary_moves))
                  / get_manhattan_distance(player_pos, opponent_pos))
            - len(game.get_legal_moves(opponent)))


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # get moves available to this MinimaxPlayer instance
        legal_moves = game.get_legal_moves(self)

        if not legal_moves or depth == 0:
            return -1, -1

        # array of scores of values at depth 1 of the minimax tree
        scores_depth_1 = np.array([self.min_max_value(game.forecast_move(move),
                                                      depth - 1) for move in legal_moves])
        max_idx = np.argmax(scores_depth_1)
        return legal_moves[max_idx]

    def min_max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if self == game.active_player:
            player = self
            min_or_max = np.argmax
        else:
            player = game.get_opponent(self)
            min_or_max = np.argmin

        legal_moves = game.get_legal_moves(player)
        if not legal_moves or depth == 0:
            return self.score(game, self)

        scores = np.array([self.min_max_value(game.forecast_move(move),
                                              depth - 1) for move in legal_moves])
        player_best = min_or_max(scores)
        return scores[player_best]


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

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

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            # NOTE: best_move is initialized to (-1, -1) and accounts
            # for the 0th iteration of iterative deepening,
            # thus, the 0th iteration is skipped here
            for depth in range(1, game.width * game.height):
                best_move = self.alphabeta(game, depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

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

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        # return the best move from max_value at index 1
        return self.max_value(game, depth, alpha, beta)[1]

    def max_value(self, game, depth, alpha, beta):
        """ Based on the Max-Value pseudo-code from the AIMA text

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            game state being explored

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            The resultant score from making the best move found in the current
            search; "-inf" if there are no legal moves

        (int, int)
            The board coordinates of the best move found in the current search;
            returns (-1, -1) if search depth is 0 or there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        legal_moves = game.get_legal_moves(self)
        if len(legal_moves) == 0 or depth == 0:
            return self.score(game, self), (-1, -1)

        move = random.choice(legal_moves)
        max_score = float("-inf")
        for _move in legal_moves:
            _game = game.forecast_move(_move)
            prev_best = max_score
            max_score = max(max_score, self.score(_game, self) if depth == 1
                            else self.min_value(_game, depth - 1, alpha, beta))
            if max_score != prev_best:
                move = _move
            # pruning condition
            if max_score >= beta:
                return max_score, move
            alpha = max(alpha, max_score)
        return max_score, move

    def min_value(self, game, depth, alpha, beta):
        """ Based on the Min-Value pseudo-code from the AIMA text

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            game state being explored

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            The resultant score from making the best move for the opponent
            found in the current search; "inf" if there are no legal moves
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        opponent = game.get_opponent(self)
        legal_moves = game.get_legal_moves(opponent)
        if len(legal_moves) == 0:
            return self.score(game, self)

        min_score = float("inf")
        for _move in legal_moves:
            _game = game.forecast_move(_move)
            min_score = min(min_score, self.score(_game, self) if depth == 1
            else self.max_value(_game, depth - 1, alpha, beta)[0])
            # pruning condition
            if min_score <= alpha:
                return min_score
            beta = min(beta, min_score)
        return min_score
