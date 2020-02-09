# -*- coding: utf-8 -*-

from chess.chessboard import *
from chess.chess import Chess
from engine import estimate


class Engine(Chess):

    def __init__(self):
        self._max_depth = 0
        self._best_move = None
        fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1"
        super(Engine, self).__init__(fen)

    def _load_fen(self, fen):
        for i in range(len(self.bd.board)):
            self.bd.board[i] = 0
        for i in range(len(self.piece)):
            self.piece[i] = 0

        array = get_array_by_fen(fen)
        for i in range(BOARD_MAX_LEN):
            if array[i]:
                self.bd.board[i] = array[i]
                pc = array[i]
                self.piece[pc] = i
        self.bd.side = get_side_by_fen(fen)

    def _eval(self):
        """
        评估函数
        """
        piece = self.piece
        side = self.get_side()
        board = self.get_board()
        return estimate.eval(board, piece, side)

    def _alpha_beta(self, depth, alpha, beta):
        '''
        Alpha-Beta搜索算法
        '''
        if (depth == 0):
            return self._eval()

        mv = ChessboardMove()
        mv_array = self.gen_all_move()
        for i in range(len(mv_array)):
            mv = mv_array[i]
            self.make_move(mv)
            value = -self._alpha_beta(depth - 1, -beta, -alpha)
            self.unmake_move()
            if (value >= beta):
                return beta
            if (value > alpha):
                alpha = value
                if (depth == self._max_depth):
                    self._best_move = mv
        return alpha

    def alpha_beta_search(self, max_depth, alpha, beta):
        self._max_depth = max_depth
        self._alpha_beta(max_depth, alpha, beta)
        return self._best_move

    def put(self, buf):
        buf_ret = ''
        buf_list = buf.split()
        if buf_list[0] == 'ucci':
            buf_ret = 'ucciok'
        elif buf_list[0] == 'position':
            fen = ''
            for i in range(2, 8):
                fen = fen + ' ' +buf_list[i]
            fen = fen.strip()

            self._load_fen(fen)

            depth = 3
            max_value = 10000

            mv_best = self.alpha_beta_search(depth, -max_value, max_value)
            return (mv_best.from_pos, mv_best.to_pos)

        return buf_ret
