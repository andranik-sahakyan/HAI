from random import randint
from BoardClasses import Board, Move
from copy import deepcopy


class StudentAI():
    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def get_move(self, move):        
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)
        moveValues = []

        for i in range(len(moves)):
            for j in range(len(moves[i])):
                self.board.make_move(moves[i][j], self.color)
                moveValues.append((moves[i][j], self.minimax(self.board, 3, self.opponent[self.color], float('-inf'), float('inf'))))
                self.board.undo()   

        move = max(moveValues, key=lambda x:x[1])[0]
        self.board.make_move(move, self.color)
        return move

    def static_eval(self, boardState):
        blackValue = 0
        whiteValue = 0

        for i in range(boardState.row):
            for j in range(boardState.col):
                checker = boardState.board[i][j]
                if checker.color == '.':
                    continue
                elif checker.color == 'B':
                    if checker.is_king:
                        blackValue += 7 + boardState.row
                    else:
                        blackValue += 5 + checker.row
                else:
                    if checker.is_king:
                        whiteValue += 7 + boardState.row
                    else:
                        whiteValue += 5 + (boardState.row - checker.row)
        
        if self.color == 1:
            return blackValue - whiteValue
        else:
            return whiteValue - blackValue
        
    def generate_children(self, player) -> [Board]:
        children = []
        checkers = self.board.get_all_possible_moves(player)

        for moveList in checkers:
            for move in moveList:
                boardCopy = deepcopy(self.board)
                boardCopy.make_move(move, player)
                children.append(boardCopy)
        return children

    def minimax(self, boardState, depth, max_player, alpha, beta):
        if depth == 0 or boardState.is_win(max_player):
            return self.static_eval(boardState)

        if max_player:
            best = float('-inf')
            for child in self.generate_children(self.color):
                candidate = self.minimax(child, depth - 1, False, alpha, beta)
                best = max(best, candidate)
                alpha = max(alpha, candidate)
                if alpha >= beta:
                    break
            return best
        else:
            best = float('inf')
            for child in self.generate_children(self.opponent[self.color]):
                candidate = self.minimax(child, depth - 1, True, alpha, beta)
                best = min(best, candidate)
                beta = min(beta, candidate)
                if alpha >= beta:
                    break
            return best
