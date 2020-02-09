# -*- coding: utf-8 -*-

from chess.chessboard import *


class Chess(object):
    def __init__(self, fen):
        self.bd = ChessBoard() # 当前棋盘状态
        self.piece = [0]*48    # 当前棋子数组
        self.movestack = []    # 历史棋盘走棋列表

        array = get_array_by_fen(fen)
        for i in range(BOARD_MAX_LEN):
            if array[i]:
                self.bd.board[i] = array[i]
                pc = array[i]
                self.piece[pc] = i

        self.bd.side = get_side_by_fen(fen)

    def get_2d_board(self):
        rows = 10
        cols= 9
        array_2d = [[0] * cols for i in range(rows)]
        for index in range(16, len(self.piece)):
            k = self.piece[index]
            if k:
                i = k // 16
                j = k % 16
                array_2d[i-3][j-3] = index
        return array_2d

    def is_match_side_pc(self, side, pc):
        sidetag = 16 + side * 16

        # 走方是否正确
        if (pc >= sidetag) and (pc < sidetag + 16):
            return True
        else:
            return False

    def get_can_move_list(self, pos):
        board = self.bd.board
        from_pos = pos
        pc = board[from_pos]

        sidetag = 0
        if (pc >= 16) and (pc < 16 + 16):
            sidetag = 16
        else:
            sidetag = 16 + 16

        n_list = []
        i = pc - sidetag
        n_list = []
        if (i == 0):   # 将
            n_list = self.bd.king_next_positions(from_pos)
        elif i == 1 or i == 2:  # 仕
            n_list = self.bd.advisor_next_positions(from_pos)
        elif i == 3 or i == 4:  # 相
            n_list = self.bd.bishop_next_positions(from_pos)
        elif i == 5 or i == 6:  # 马
            n_list = self.bd.knight_next_positions(from_pos)
        elif i == 7 or i == 8:  # 车
            n_list = self.bd.rook_next_positions(from_pos)
        elif i == 9 or i == 10: # 炮
            n_list = self.bd.cannon_next_positions(from_pos)
        elif i == 11 or i == 12 or i == 13 or i == 14 or i == 15: # 兵
            n_list = self.bd.pawnMove_next_positions(from_pos)
        return n_list

    def check_move(self, m):
        side = self.bd.side
        board = self.bd.board

        from_pos = m.from_pos
        dest_pos = m.to_pos

        pc = board[from_pos]

        # 走方是否正确
        if not self.is_match_side_pc(side, pc):
            return False
        # 目的位置是否在可走位置上
        n_list = self.get_can_move_list(from_pos)
        if dest_pos in n_list:
            return True
        else:
            return False

    def make_move(self, m):
        side = self.bd.side
        board = self.bd.board
        piece = self.piece

        sidetag = 16   # 此处为对方将帅的值，其它地方多表示本方将帅值
        if (side == 0):
            sidetag = 32
        else:
            sidetag = 16

        from_pos = m.from_pos
        dest_pos = m.to_pos

        # 设置走法栈
        mv = ChessboardMove()
        mv.from_pos = from_pos
        mv.to_pos = dest_pos
        p = board[dest_pos]
        mv.capture = p
        self.movestack.append(mv)

        # 设置棋子数组
        if (p > 0):
            piece[p] = 0
        piece[board[from_pos]] = dest_pos

        # 设置棋盘数组
        board[dest_pos] = board[from_pos]
        board[from_pos] = 0

        self.bd.change_side()

        return (p == sidetag)


    def unmake_move(self):
        piece = self.piece
        board = self.bd.board

        self.bd.change_side()

        p = self.movestack.pop()
        from_pos = p.from_pos
        dest_pos = p.to_pos
        capture = p.capture

        # 设置棋盘数组
        board[from_pos] = board[dest_pos]
        board[dest_pos] = capture

        # 设置棋子数组
        if (capture > 0):
            piece[capture] = dest_pos
        piece[board[from_pos]] = from_pos


    def check_king_danger(self, lside):
        """
        检测lside一方是否被将军，是被将军返回1，否则返回0
        """
        piece = self.piece
        board = self.bd.board

        sidetag = 32 - lside * 16 # 此处表示lside对方的将的值
        fside = 1 - lside	# 对方标志
        pos_add = 0	# 位置增量

        # w_king, b_king 红黑双方将帅的位置
        w_king = piece[16]
        b_king = piece[32]

        if (not w_king) or (not b_king):
            return 0

        # 检测将帅是否照面
        r = 1       # r=1表示将军，否则为0
        if (w_king%16 == b_king%16):
            w_king = w_king - 16
            while (w_king != b_king):
                if (board[w_king]):
                    r=0
                    break
                w_king = w_king - 16
            if (r):
                return r # 将帅照面

        q = piece[48-sidetag] # lside方将的位置

        # 检测将是否被马攻击
        for i in range(5, 7):
            p = piece[sidetag+i]
            if (not p):
                continue
            for k in range(0, 8): # 8个方向
                n = p + KnightDir[k] # n为新的可能走到的位置
                if (n != q):
                    continue
                if (LegalPosition[fside][n] & PositionMask[3]): # 马将对应下标为3
                    m = p + KnightCheck[k] # 马腿位置
                    if (not board[m]): # 马腿位置无棋子占据
                        return 1

        # 检测将是否被车攻击
        r = 1
        for i in range(7, 9):
            p = piece[sidetag+i]
            if (not p):
                continue
            if (p%16 == q%16): # 在同一纵线上
                pos_add = 16
                if p > q:
                    pos_add = -16
                else:
                    pos_add = 16

                p = p + pos_add
                while (p != q):
                    if (board[p]): # 车将中间有子隔着
                        r = 0
                        break
                    p = p + pos_add
                if (r):
                    return r
            elif (p//16 == q//16): # 在同一横线上
                pos_add = 1
                if p > q:
                    pos_add = -1
                else:
                    pos_add = 1

                p = p + pos_add
                while (p != q):
                    if (board[p]):
                        r = 0
                        break
                    p = p + pos_add
                if (r):
                    return r

        # 检测将是否被炮攻击
        overflag = 0 # 翻山标志
        for i in range(9, 11):
            p = piece[sidetag+i]
            if (not p):
                continue
            if (p%16 == q%16): # 在同一纵线上
                pos_add = 16
                if (p > q):
                    pos_add = -16
                else:
                    pos_add = 16

                p = p + pos_add
                while (p != q):
                    if (board[p]):
                        if(not overflag):  # 隔一子
                            overflag = 1
                        else:           # 隔两子
                            overflag = 2
                            break
                    p = p + pos_add
                if (overflag == 1):
                    return 1
            elif (p//16 == q//16): # 在同一横线上
                pos_add = 1
                if (p > q):
                    pos_add = -1
                else:
                    pos_add = 1

                p = p + pos_add
                while (p != q):
                    if(board[p]):
                        if (not overflag):
                            overflag = 1
                        else:
                            overflag = 2
                            break
                    p = p + pos_add
                if (overflag==1):
                    return 1

        # 检测将是否被兵攻击
        for i in range(11, 16):
            p = piece[sidetag + i]
            if (not p):
                continue
            for k in range(3): # 3个方向
                n = p + PawnDir[fside][k] # n为新的可能走到的位置
                if ((n == q) and (LegalPosition[fside][n] & PositionMask[6])): # 兵士将对应下标为6
                    return 1
        return 0


    def _save_move(self, from_pos, to_pos, mv):
        board = self.bd.board
        piece = self.piece
        side = self.bd.side

        p = board[to_pos]
        piece[board[from_pos]] = to_pos
        if (p):
            piece[p]=0
        board[to_pos] = board[from_pos]
        board[from_pos] = 0

        r = self.check_king_danger(side)
        board[from_pos] = board[to_pos]
        board[to_pos] = p
        piece[board[from_pos]] = from_pos
        if (p):
            piece[p] = to_pos

        if (not r):
            mv.from_pos = from_pos
            mv.to_pos = to_pos
            return 1
        return 0


    def gen_all_move(self):
        piece = self.piece
        board = self.bd.board
        side = self.bd.side

        sidetag = 16 + 16 * side
        p = piece[sidetag] # 将的位置
        if (not p):
            return 0

        mv_array = []
        # 将的走法
        for k in range(4):       # 4个方向
            n = p + KingDir[k]   # n为新的可能走到的位置
            if (LegalPosition[side][n] & PositionMask[0]): # 将对应下标为0
                if (not (board[n] & sidetag)): #目标位置上没有本方棋子
                    mv = ChessboardMove()
                    if self._save_move(p, n, mv):
                        mv_array.append(mv)

        # 士的走法
        for i in range(1, 3):
            p = piece[sidetag + i]
            if (not p):
                continue
            for k in range(4):        # 4个方向
                n = p + AdvisorDir[k] # n为新的可能走到的位置
                if (LegalPosition[side][n] & PositionMask[1]): # 士将对应下标为1
                    if (not (board[n] & sidetag)): # 目标位置上没有本方棋子
                        mv = ChessboardMove()
                        if self._save_move(p, n, mv):
                            mv_array.append(mv)

        # 象的走法
        for i in range(3, 5):
            p = piece[sidetag + i]
            if (not p):
                continue
            for k in range(4):        # 4个方向
                n = p + BishopDir[k]  # n为新的可能走到的位置
                if (LegalPosition[side][n] & PositionMask[2]):    # 象将对应下标为2
                    m = p + BishopCheck[k]
                    if not board[m]:  # 象眼位置无棋子占据
                        if (not (board[n] & sidetag)): # 目标位置上没有本方棋子
                            mv = ChessboardMove()
                            if self._save_move(p, n, mv):
                                mv_array.append(mv)

        # 马的走法
        for i in range(5, 7):
            p = piece[sidetag + i]
            if (not p):
                continue
            for k in range(8):        # 8个方向
                n = p + KnightDir[k]  # n为新的可能走到的位置
                if (LegalPosition[side][n] & PositionMask[3]): # 马将对应下标为3
                    m = p + KnightCheck[k] # 马腿位置
                    if (not board[m]):     # 马腿位置无棋子占据
                        if (not (board[n] & sidetag)): # 目标位置上没有本方棋子
                            mv = ChessboardMove()
                            if self._save_move(p, n, mv):
                                mv_array.append(mv)

        # 车的走法
        for i in range(7, 9):
            p = piece[sidetag + i]
            if (not p):
                continue
            for k in range(4):          # 4个方向
                for j in range(1, 10):  # 横的最多有8个可能走的位置，纵向最多有9个位置
                    n = p + j * RookDir[k]
                    if (not (LegalPosition[side][n] & PositionMask[4])): # 车士将对应下标为4
                        break
                    if (not board[n]): # 目标位置上无子
                        mv = ChessboardMove()
                        if self._save_move(p, n, mv):
                            mv_array.append(mv)
                    elif (board[n] & sidetag): # 目标位置上有本方棋子
                        break
                    else: # 目标位置上有对方棋子
                        mv = ChessboardMove()
                        if self._save_move(p, n, mv):
                            mv_array.append(mv)
                        break

        # 炮的走法
        for i in range(9, 11):
            p = piece[sidetag + i]
            if (not p):
                continue
            for k in range(4):          # 4个方向
                OverFlag = 0
                for j in range(1, 10):  # 横的最多有8个可能走的位置，纵向最多有9个位置
                    n = p + j * CannonDir[k]
                    if (not (LegalPosition[side][n] & PositionMask[5])): # 炮士将对应下标为5
                        break
                    if (not board[n]):     # 目标位置上无子
                        if (not OverFlag): # 未翻山
                            mv = ChessboardMove()
                            if self._save_move(p, n, mv):
                                mv_array.append(mv)
                        # 已翻山则不作处理，自动考察向下一个位置
                    else: # 目标位置上有子
                        if (not OverFlag): # 未翻山则置翻山标志
                            OverFlag = 1
                        else: # 已翻山
                            if (not (board[n] & sidetag)): # 对方棋子
                                mv = ChessboardMove()
                                if self._save_move(p, n, mv):
                                    mv_array.append(mv)
                            break  # 不论吃不吃子，都退出此方向搜索

        # 兵的走法
        for i in range(11, 16):
            p = piece[sidetag + i]
            if (not p):
                continue
            for k in range(3): # 3个方向
                n = p + PawnDir[side][k] # n为新的可能走到的位置
                if (LegalPosition[side][n] & PositionMask[6]):    # 兵士将对应下标为6
                    if (not (board[n] & sidetag)): # 目标位置上没有本方棋子
                        mv = ChessboardMove()
                        if self._save_move(p, n, mv):
                            mv_array.append(mv)
        return mv_array

    def get_side(self):
        return self.bd.side

    def get_board(self):
        return self.bd.board

    def output_piece(self):
        """ 输出棋子数组 """
        piece = self.piece
        for i in range(0, 16):
            print("%4d" % piece[i], end='')
        print("")
        for i in range(16, 32):
            print("%4d" % piece[i], end='')
        print("")
        for i in range(32, 48):
            print("%4d" % piece[i], end='')
        print("")


if __name__ == "__main__":
    fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
    chs = Chess(fen)

    print("side:", chs.bd.side)
    output_board_array(chs.bd.board)

    all_move_array = chs.gen_all_move()
    for i in range(len(all_move_array)):
        print(all_move_array[i].from_pos, all_move_array[i].to_pos, end='')
        print("(%d, %d)" %(chs.bd.board[all_move_array[i].from_pos], chs.bd.board[all_move_array[i].to_pos]))
    chs.output_piece()
    chs.get_2d_board()
