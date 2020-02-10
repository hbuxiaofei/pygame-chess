# -*- coding: utf-8 -*-

# 红方:0 黑方:1
SIDE_RED = 0
SIDE_BLACK = 1

# 棋盘数组长度
BOARD_MAX_LEN = 256


#各种棋子走法数组
KingDir =    [-0x10, -0x01, +0x01, +0x10,     0,     0,     0,     0]  # 将
AdvisorDir = [-0x11, -0x0f, +0x0f, +0x11,     0,     0,     0,     0]  # 士
BishopDir =  [-0x22, -0x1e, +0x1e, +0x22,     0,     0,     0,     0]  # 象
KnightDir =  [-0x21, -0x1f, -0x12, -0x0e, +0x0e, +0x12, +0x1f, +0x21]  # 马
RookDir =    [-0x01, +0x01, -0x10, +0x10,     0,     0,     0,     0]  # 车
CannonDir =  [-0x01, +0x01, -0x10, +0x10,     0,     0,     0,     0]  # 炮
PawnDir =   [[-0x01, +0x01, -0x10,     0,     0,     0,     0,     0],
             [-0x01, +0x01, +0x10,     0,     0,     0,     0,     0]] # 兵

KnightCheck = [-0x10,-0x10,-0x01,+0x01,-0x01,+0x01,+0x10,+0x10] # 马腿位置
BishopCheck = [-0x11,-0x0f,+0x0f,+0x11,0,0,0,0]                 # 象眼位置
kingpalace =  [54,55,56,70,71,72,86,87,88]                      # 黑方九宫位置

#各种棋子合理位置数组
LegalPosition = [
	[
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 1,25, 1, 9, 1,25, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 1, 9, 1, 9, 1, 9, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 17, 1, 1, 7, 19, 7, 1, 1, 17, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 1, 3, 7, 3, 1, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 17, 7, 3, 7, 17, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	    ],
	[
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 17, 7, 3, 7, 17, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 1, 1, 1, 3, 7, 3, 1, 1, 1, 0, 0, 0, 0,
	    0, 0, 0, 17, 1, 1, 7, 19, 7, 1, 1, 17, 0, 0, 0, 0,
	    0, 0, 0, 9, 1, 9, 1, 9, 1, 9, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 1,25, 1, 9, 1,25, 1, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
	    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
	    ]
	]
PositionMask = [2, 4, 16, 1, 1, 1, 8]


class ChessboardMove(object):
    def __init__(self):
        self.from_pos = 0
        self.to_pos = 0
        self.capture = 0

class ChessBoard(object):
    def __init__(self):
        self.board = [0]*BOARD_MAX_LEN             # 棋盘数组
        self.side = SIDE_RED             # 轮到哪方走

    def change_side(self):
        self.side = 1 - self.side

    def king_next_positions(self, p):
        """
        将 下一步可走位置
        """
        n_list = []
        sidetag = 16 + self.side * 16  # 走棋方，红方16，黑方32
        for k in range(4):       # 4个方向
            n = p + KingDir[k]   # n为新的可能走到的位置
            if (LegalPosition[self.side][n] & PositionMask[0]): # 将对应下标为0
                if (not (self.board[n] & sidetag)): # 目标位置上没有本方棋子
                    n_list.append(n)
        return n_list

    def advisor_next_positions(self, p):
        """
        仕 下一步可走位置
        """
        n_list = []
        sidetag = 16 + self.side * 16  # 走棋方，红方16，黑方32
        for k in range(4):        # 4个方向
            n = p + AdvisorDir[k] # n为新的可能走到的位置
            if (LegalPosition[self.side][n] & PositionMask[1]): # 士将对应下标为1
                if (not (self.board[n] & sidetag)): # 目标位置上没有本方棋子
                    n_list.append(n)
        return n_list

    def bishop_next_positions(self, p):
        """
        相 下一步可走位置
        """
        n_list = []
        sidetag = 16 + self.side * 16  # 走棋方，红方16，黑方32
        for k in range(4):        # 4个方向
            n = p + BishopDir[k]  # n为新的可能走到的位置
            if (LegalPosition[self.side][n] & PositionMask[2]):    # 象将对应下标为2
                m = p + BishopCheck[k]
                if not self.board[m]:  # 象眼位置无棋子占据
                    if (not (self.board[n] & sidetag)): # 目标位置上没有本方棋子
                        n_list.append(n)
        return n_list


    def knight_next_positions(self, p):
        """
        马 下一步可走位置
        """
        n_list = []
        sidetag = 16 + self.side * 16  # 走棋方，红方16，黑方32
        for k in range(8):        # 8个方向
            n = p + KnightDir[k]  # n为新的可能走到的位置
            if (LegalPosition[self.side][n] & PositionMask[3]): # 马将对应下标为3
                m = p + KnightCheck[k] # 马腿位置
                if (not self.board[m]):     # 马腿位置无棋子占据
                    if (not (self.board[n] & sidetag)): # 目标位置上没有本方棋子
                        n_list.append(n)
        return n_list


    def rook_next_positions(self, p):
        """
        车 下一步可走位置
        """
        n_list = []
        sidetag = 16 + self.side * 16    # 走棋方，红方16，黑方32
        for k in range(4):          # 4个方向
            for j in range(1, 10):  # 横的最多有8个可能走的位置，纵向最多有9个位置
                n = p + j * RookDir[k]
                if (not (LegalPosition[self.side][n] & PositionMask[4])): # 车士将对应下标为4
                    break
                if (not self.board[n]): # 目标位置上无子
                    n_list.append(n)
                elif (self.board[n] & sidetag): # 目标位置上有本方棋子
                    break
                else: # 目标位置上有对方棋子
                    n_list.append(n)
                    break
        return n_list


    def cannon_next_positions(self, p):
        """
        炮 下一步可走位置
        """
        n_list = []
        sidetag = 16 + self.side * 16    # 走棋方，红方16，黑方32
        for k in range(4):          # 4个方向
            overflag = 0
            for j in range(1, 10):  # 横的最多有8个可能走的位置，纵向最多有9个位置
                n = p + j * CannonDir[k]
                if (not (LegalPosition[self.side][n] & PositionMask[5])): # 炮士将对应下标为5
                    break
                if (not self.board[n]):     # 目标位置上无子
                    if (not overflag): # 未翻山
                        n_list.append(n)
                    # 已翻山则不作处理，自动考察向下一个位置
                else: # 目标位置上有子
                    if (not overflag): # 未翻山则置翻山标志
                        overflag = 1
                    else: # 已翻山
                        if (not (self.board[n] & sidetag)): # 对方棋子
                            n_list.append(n)
                        break  # 不论吃不吃子，都退出此方向搜索
        return n_list


    def pawnMove_next_positions(self, p):
        """
        卒 下一步可走位置
        """
        n_list = []
        sidetag = 16 + self.side * 16 # 走棋方，红方16，黑方32
        for k in range(3): # 3个方向
            n = p + PawnDir[self.side][k] # n为新的可能走到的位置
            if (LegalPosition[self.side][n] & PositionMask[6]):    # 兵士将对应下标为6
                if (not (self.board[n] & sidetag)): # 目标位置上没有本方棋子
                    n_list.append(n)
        return n_list


def int2fen_char(i):
    """  棋子整数值转换成字符表示 """
    if (i < 32):
        if i == 16:
            return 'K'
        elif i == 17 or i == 18:
            return 'A'
        elif i == 19 or i == 20:
            return 'B'
        elif i == 21 or i == 22:
            return 'N'
        elif i == 23 or i == 24:
            return 'R'
        elif i == 25 or i == 26:
            return 'C'
        elif i == 27 or i == 28 or i == 29 or i == 30 or i == 31:
            return 'P'
        else:
            return 0
    else:
        i = i - 16
        if i == 16:
            return 'k'
        elif i == 17 or i == 18:
            return 'a'
        elif i == 19 or i == 20:
            return 'b'
        elif i == 21 or i == 22:
            return 'n'
        elif i == 23 or i == 24:
            return 'r'
        elif i == 25 or i == 26:
            return 'c'
        elif i == 27 or i == 28 or i == 29 or i == 30 or i == 31:
            return 'p'
        else:
            return 0


def _fen_char2index(ch):
    """
    FEN串中棋子对应的数组下标
    下标0，1，2，3，4，5，6分别对应表示将，仕，象，马，车，炮，兵
    """
    if ch == 'k' or ch == 'K':
        return 0
    elif ch == 'a' or ch == 'A':
        return 1
    elif ch == 'b' or ch == 'B':
        return 2
    elif ch == 'n' or ch == 'N':
        return 3
    elif ch == 'r' or ch == 'R':
        return 4
    elif ch == 'c' or ch == 'C':
        return 5
    elif ch == 'p' or ch == 'P':
        return 6
    else:
        return 7


def get_side_by_fen(fen):
    if len(fen) == 0:
        return None

    fen_split = fen.split()

    if len(fen_split) < 2:
        return None

    if fen_split[1] == 'b':
        return SIDE_BLACK
    else:
        return SIDE_RED


def get_array_by_fen(fen):
    """
    将FEN串表示的局面转换成一维数组
    """
    pc_white = [16, 17, 19, 21, 23, 25, 27]
    pc_black = [32, 33, 35, 37, 39, 41, 43]

    if len(fen) == 0:
        return None

    board = [0]*BOARD_MAX_LEN

    fen_list = list(fen)
    i = 3
    j = 3
    for index in range(len(fen_list)):
        if fen_list[index] == ' ':
            break

        if fen_list[index] == '/':
            j = 3
            i = i + 1
            if i > 12:
                break
        elif fen_list[index] >= '1' and fen_list[index] <= '9':
            for k in range(ord(fen_list[index]) - ord('0')):
                if (j >= 11):
                    break;
                j = j + 1
        elif fen_list[index] >= 'A' and fen_list[index] <= 'Z':
            if (j <= 11):
                k = _fen_char2index(fen_list[index])
                if (k < 7):
                    if (pc_white[k] < 32):
                        board[(i<<4)+j] = pc_white[k]
                        pc_white[k] = pc_white[k] + 1
                j = j + 1
        elif fen_list[index] >= 'a' and fen_list[index] <= 'z':
            if (j <= 11):
                k = _fen_char2index(fen_list[index])
                if (k < 7):
                    if (pc_black[k] < 48):
                        board[(i<<4)+j] = pc_black[k]
                        pc_black[k] = pc_black[k] + 1
                j = j + 1
    return board


def get_fen_by_array(bd_array, side):
    """
    将一维数组表示的局面转换成FEN串
    """

    fen_list = [' ']*BOARD_MAX_LEN
    index = 0
    for i in range(3, 13):
        k = 0
        for j in range(3, 12):
            pc = bd_array[(i << 4) + j]
            if (pc != 0):
                if (k > 0):
                    fen_list[index] = chr(k + ord('0'))
                    index = index + 1
                    k = 0
                fen_list[index] = int2fen_char(pc)
                index = index + 1
            else:
                k = k + 1
        if (k > 0):
            fen_list[index] = chr(k + ord('0'))
            index = index + 1
        fen_list[index] = '/'
        index = index + 1
    index = index - 1
    fen_list[index] = ' '
    index = index + 1
    if side == SIDE_RED:
        fen_list[index] = 'w'
    else:
        fen_list[index] = 'b'
    fen_string = ("".join(fen_list))
    return fen_string.strip()


def output_board_array(bd_array):
    """ 输出棋盘数组 """
    for i in range(1, len(bd_array)+1):
        print("%3d" % bd_array[i-1], end='')
        if (i%16 == 0):
            print("")


if __name__ == "__main__":
    chsman = ChessBoard()
    print(chsman.side)
    fen = "rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w"
    print(get_side_by_fen(fen))
    array = get_array_by_fen(fen)
    side = get_side_by_fen(fen)
    print(get_fen_by_array(array, side))
    output_board_array(array)
