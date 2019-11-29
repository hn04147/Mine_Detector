#######
#
# BOARD
#
# A minesweeper board is a rectangular board consisting of
# a number of rows and a number of columns.
#   - Contrary to squares in the original game, each square
#     on our boards can store an unrestricted number of bombs.
#######

import copy


def make_board \
                (dimension=(10, 15), bomb_positions=(),
                 open_positions=frozenset(), flagged_positions=()):
    """
      Return a new board of the given dimension that is filled
      with bombs at the given bomb positions and with flags at
      the given flag positions, and with open squares at the
      given open positions.
        - The dimension is a tuple consisting of the number of
          rows on the board, followed by the number of columns.
        - The bomb positions and the flag positions are collected
          in a sequence. The number of bombs, respectively the
          number of flags on a position is equal to the number of
          times that position occurs in the corresponding sequence.
        - The open positions are collected in a frozen set.
          All open positions must have at least one adjacent bomb.
          (In this way, we avoid that squares must be disclosed at
          this point, or that other algorithms must take into account
          that not all open squares are fully disclosed).
        - You may assume that the sequence of bomb positions nor
          the sequence of flag positions has  elements in common
          with the frozen set of open positions.
      This function is introduced to be able to experiment with
      boards as they evolve during the game.
    """
    flags = []
    for element in flagged_positions:
        flags.append(element)
    bombs = []
    for element in bomb_positions:
        bombs.append(element)
    open_pos = []
    for i in range(dimension[0]):
        rij = []
        for j in range(dimension[1]):
            if (i,j) not in open_positions:
                rij.append(0)
            else:
                rij.append(1)
        open_pos.append(rij)
    board = {"dimensie": (dimension[0],dimension[1]),"vlaggen": flags,"bommen": bombs,"open": open_pos}
    return board
assert make_board()

def make_closed_board(dimension=(10, 15), *bomb_pos):
    """
      Return a new board of the given dimension that is filled
      with bombs at the given positions.
        - The dimension is a tuple consisting of the number of
          rows on the board, followed by the number of columns.
        - The number of bombs on a position is equal to the
          the number of times that position occurs in the given
          bomb positions.
    """
    open = []
    for i in range(dimension[0]):
        rij = []
        for j in range(dimension[1]):
            rij.append(0)
        open.append(rij)
    bombs = []
    for element in bomb_pos:
        bombs.append(element)
    closed_board = {"dimensie": dimension,"bommen": bombs,"vlaggen": [],"open": open}
    return closed_board


def copy_board(board):
    """
      Return a copy of the given board.
      - The resulting board is a different object whose squares are all
        identical to the corresponding squares on the given board.
    """
    kopie = copy.deepcopy(board)
    return kopie



def dimension(board):
    """
      Return the dimension of the given board.
        - The resulting value is a tuple consisting of the number of
          rows on the board, followed by the number of columns.
    """
    dimensie = board["dimensie"]
    return dimensie



def nb_rows(board):
    """
      Return the number of rows on the given board.
    """
    dim = board["dimensie"]
    aantal_rijen=dim[0]
    return aantal_rijen


def nb_cols(board):
    """
      Return the number of columns on the given board.
    """
    dim = board["dimensie"]
    aantal_kolommen=dim[1]
    return aantal_kolommen


def squares_with_bombs(board, min_nb_bombs=1):
    """
      Return a list of all positions of all squares having
      at least the given number of bombs.
      - The minimum number of bombs must be positive.
      - The positions in the resulting list are in ascending order.
      - The position of a square having at least the given number
        of bombs is included in the list as many times as the
        number of bombs on the given square.
    """
    square_bomb = []
    bombs = board["bommen"]
    for element in bombs:
        a = bombs.count(element)
        if a>=min_nb_bombs:
            square_bomb.append(element)
    list.sort(square_bomb)
    return square_bomb

def closed_squares(board):
    """
      Return a set of positions of all the closed squares
      on the given board.
    """
    closed = set([])
    open_toe = board["open"]
    for i in range(0,nb_rows(board)):
        for j in range(0,nb_cols(board)):
            if open_toe[i][j] == 0:
                closed.add((i,j))
    return closed


def print_board(board, bombs_revealed=True):
    """
      Print the given board one row per line with or without bombs
      on the given board revealed.
      - Each square is printed in a field of 3 characters wide.
      - An open square with no adjacent bombs is represented by a white
        square. An open square with adjacent bombs is represented by the
        number of adjacent bombs.
      - A closed square is represented by a filled square.
      - A square with at least one bomb is represented by a black circle
        if bombs on the given board must be revealed.
      - A square with at least one flag is represented by a flag.
      - Squares having both bombs and flag are represented by both symbols
        (at least if bombs must be revealed).
    """
    white_square = "\u25a2"
    closed_square = "\u25a4"
    bomb_symbol = "\u25cf"  # Actual bomb symbol (\U01F4A3)does not print well.
    flag_symbol = "\u2691"

    for row in range(0, nb_rows(board)):
        for col in range(0, nb_cols(board)):
            if is_open_at(board, (row, col)):
                if nb_adjacent_bombs(board, (row, col)) == 0:
                   # print("  {0}  ".format(white_square), end="")
                    pass
                else:
                    print(str.format('{:^5}', nb_adjacent_bombs(board, (row, col))), end="")
            elif nb_flags_at(board, (row, col)) > 0:
                if (nb_bombs_at(board, (row, col)) > 0) and bombs_revealed:
                    print("  {0}{1} ".format(bomb_symbol, flag_symbol), end="")
                else:
                    print("  {0}  ".format(flag_symbol), end="")
            elif (nb_bombs_at(board, (row, col)) > 0) and bombs_revealed:
                print("  {0}  ".format(bomb_symbol), end="")
            else:
                print("  {0}  ".format(closed_square), end="")
        print()


##############
#
# SQUARE
#   - A square is either open or closed.
#   - Open squares cannot have bombs nor flags.
#
##############



def add_bomb_at(board, position):
    """
      Add a bomb to the square at the given position on the given
      board.
      - No squares on the given board may have been opened yet.
    """
    board_closed = True
    for rij in board["open"]:
        for positie in rij:
            if positie == 1:
                board_closed = False
    if board_closed:
        board["bommen"] += [position]
    return board



def nb_bombs_at(board, position):
    """
      Return the number of bombs at the given position
      on the given board.
      - This function must be applicable to all squares
        on the board, including open squares and flagged
        squares.
    """
    aantal_bommen = board["bommen"].count(position)
    return aantal_bommen



def add_flag_at(board, position):
    """
      Add a flag to the square at the given position on the given
      board.
      - The given square may not have been opened yet.
    """
    if not is_open_at(board, position):
        board["vlaggen"] += [position]
    return board



def remove_flag_from(board, position):
    """
      Remove a flag from the square at the given position on the given
      board.
      - The given square contains at least one flag.
    """
    board["vlaggen"].remove(position)
    return board



def nb_flags_at(board, position):
    """
      Return the number of flags at the given position
      on the given board.
      - This function must be applicable to all squares
        on the board, including opened squares.
    """
    aantal_vlaggen = board["vlaggen"].count(position)
    return aantal_vlaggen


def open_at(board, pos):
    """
      Open the square at the given position on the
      given board.
      - You may assume that the given square does not have
        any bombs.
    """
    board["open"][pos[0]][pos[1]] = 1
    return board



def is_open_at(board, pos):
    """
      Check whether the square at the given position
      on the given board has been opened.
      - This function must be applicable to all squares
        on the board.
    """
    if board["open"][pos[0]][pos[1]] == 0:
        return False
    return True




#######
#
# POSITION
#
# Positions on a minesweeper board are tuples consisting
# of the number of the row followed by the number of the column.
#   - Rows and columns are numbered starting from 0.
#   - Position (0,0) corresponds with the left upper corner
#     on the screen.
#
#######



def is_in_boundaries(board, position):
    """
      Check whether the given position is withing the boundaries
      of the given board.
    """
    if position[0]<0 or position[1]<0:
        return False
    elif position[0]>=board["dimensie"][0] or position[1]>=board["dimensie"][1]:
        return False
    return True


def left(board, position):
    """
      Return the position on the given board immediately to
      the left of the given position.
      - None is returned if the given position is the
        leftmost position of its row.
    """
    i, j = position[0], position[1]
    positie = (i,j-1)
    if is_in_boundaries(board, positie):
        return positie
    return None



def right(board, position):
    """
      Return the position on the given board immediately to
      the right of the given position.
      - None is returned if the given position is the
        rightmost position of its row.
    """
    i, j = position[0], position[1]
    positie = (i,j+1)
    if is_in_boundaries(board, positie):
        return positie
    return None



def up(board, position):
    """
      Return the position on the given board immediately
      above the given position.
      - None is returned if the given position is the
        top position of its column (i.e position in row 0).
    """
    i, j = position[0], position[1]
    positie = (i-1,j)
    if is_in_boundaries(board, positie):
        return positie
    return None



def down(board, position):
    """
      Return the position on the given board immediately
      below the given position.
      - None is returned if the given position is the
        bottom position of its column (i.e. position with the
        highest possible row number).
    """
    i, j = position[0], position[1]
    positie = (i+1,j)
    if is_in_boundaries(board,positie):
        return positie
    return None



def left_up(board,position):
    """
    Returns the coordinate "left-up" of the given position.
    None is returned if the "left-up" coordinate isn't in the boundaries of the board.
    """
    position = left(board,position)
    if position is None:
        return position
    position = up(board,position)
    return position



def left_down(board,position):
    """
    Returns the coordinate "left-down" of the given position.
    None is returned if the "left-down" coordinate isn't in the boundaries of the board.
    """
    position = left(board,position)
    if position is None:
        return None
    position = down(board,position)
    return position



def right_up(board,position):
    """
    Returns the coordinate "right-up" of the given position.
    None is returned if the "right-up" coordinate isn't in the boundaries of the board.
    """
    position = right(board,position)
    if position is None:
        return None
    position = up(board,position)
    return position


def right_down(board,position):
    """
    Returns the coordinate "right-down" of the given position.
    None is returned if the "right-down" coordinate isn't in the boundaries of the board.
    """
    position = right(board,position)
    if position is None:
        return None
    position = down(board,position)
    return position



def next_position(board, position):
    """
    Return the position next to the given position
    on the given board.
    - If the given position is not at the end of a row,
      the position right to the given position is returned.
      Otherwise, the first position of the next row is
      returned. If that next row does not exist,
      None is returned.
    """
    if position is None:
        return None
    if (nb_cols(board)-1) == position[1]:
        if (nb_rows(board)-1) == (position[0]):
            return None
        return (position[0]+1,0)
    else:
        return right(board,position)



def adjacent_positions(board, position):
    """
      Return a collection of all the positions on the given
      board that are adjacent to the given position and within
      the boundaries of the given board.
    """
    buren = [right(board,position),right_up(board,position),up(board,position),left_up(board,position),\
             left(board,position),left_down(board,position),down(board,position),right_down(board,position)]
    buren2 = []
    for element in buren:
        if element is not None:
            buren2.append(element)
    return buren2


###########
# PATTERNS
###########



def all_closed_adjacent_squares_with_bombs(board, start=(0, 0)):
    """
      Starting from the given start position, return the
      position of the first open square whose closed adjacent
      squares all have a bomb.
      - The resulting position is to the right of the start
        position and/or below the start position.
      - None is returned if no such position exists.
      - The square at the resulting position must have at least
        one adjacent bomb and at least one closed adjacent
        square that has not been flagged. In other words, there
        must be at least one non-flagged closed square adjacent
        to the resulting position that can be flagged as having
        a bomb.
      - You may assume that each square on the given board has at
        most one bomb.
    """
    positie = start
    while positie is not None:
        if is_open_at(board, positie):
            if nb_adjacent_bombs(board, positie) == nb_adjacent_closed(board, positie) and nb_adjacent_bombs(board, positie) > 0:
                return positie
        positie = next_position(board, positie)
    return None


def all_closed_nonflagged_adjacent_squares_without_bombs(board, start=(0, 0)):
    """
      Starting from the given start position, return the
      position of the first open square whose adjacent bombs
      have all been flagged.
      - The resulting position is to the right of the start
        position and/or below the start position.
      - None is returned if no such position exists.
      - The resulting square must have at least one adjacent bomb
        and at least one other closed adjacent square that has
        not been flagged. In other words, there must be at least
        one non-flagged closed square adjacent to the resulting
        position that can be opened safely.
      - This function is only defined for boards in in which
        each square can have at most one bomb.
    """
    positie = start
    while positie is not None:
        if is_open_at(board, positie):
            if nb_adjacent_bombs(board, positie) == nb_adjacent_flags(board, positie):
                if nb_adjacent_closed(board, positie) > nb_adjacent_bombs(board, positie):
                    return positie
        positie = next_position(board, positie)
    return positie


###########
#
# GAME
#
############



def nb_adjacent_bombs(board, pos):
    """
      Return the total number of bombs at all positions
      adjacent to the given position.
      - This function must be applicable to all squares
        on the board, including squares with bombs, flagged
        squares and opened squares.
    """
    buren = adjacent_positions(board,pos)
    adj_bombs = 0
    for element in buren:
        adj_bombs += nb_bombs_at(board, element)
    return adj_bombs



def nb_adjacent_flags(board, pos):
    """
      Return the total number of flags at all positions
      adjacent to the given position.
      - This function must be applicable to all squares
        on the board, including squares with bombs, flagged
        squares and opened squares.
    """
    adj_flags = 0
    for element in adjacent_positions(board,pos):
        adj_flags += nb_flags_at(board, element)
    return adj_flags


def nb_adjacent_closed(board, pos):
    """
      Return the total number of closed squares at all positions
      adjacent to the given position.
      - This function must be applicable to all squares
        on the board, including squares with bombs, flagged
        squares and opened squares.
    """
    adj_closed = 0
    for element in adjacent_positions(board,pos):
        if not is_open_at(board, element):
            adj_closed += 1
    return adj_closed



def flag_all_bombs(board):
    """
      Adds flags for all the bombs on the board.
      - At the end, the number of flags on each square will be
        equal to the number of bombs on that square.
    """
    vlaggen = []
    for positie in board["bommen"]:
        vlaggen.append(positie)
    board["vlaggen"] = vlaggen
    return board



def getneighbours(board,position):
    """
    Returns a set of adjacent positions.
    """
    return set(adjacent_positions(board,position))


def disclose(board, pos, viewed):
    """
    Returns a set of positions who are disclosed.
    It discloses a square,
    if the given square has no adjacent bombs then it discloses the adjacent squares of the given square recursively.
    """
    if pos is not open_at(board,pos):
        viewed.add(pos)
    buren = getneighbours(board,pos)
    returnset = set()
    if nb_adjacent_bombs(board,pos) == 0:
        for i in buren:
            if i not in viewed:
                returnset = returnset.union(disclose(board, i, viewed))
    return returnset


def disclose_square(board, pos):
    """
      Disclose the square at the given position on the
      given board.
      - No effect if the square has already been opened.
      - If the square at the given position has no adjacent
        bombs, all adjacent squares are disclosed recursively.
      - Returns a set of positions of all squares that have
        been opened in disclosing the given square.
      - You may assume that the square at the given position
        does not have any bombs.
    """
    viewed = set()
    te_openen = disclose(board, pos, viewed)
    for element in te_openen:
        open_at(board, element)
    return te_openen


def disclose_squares(board, positions):
    """
      Disclose all the squares at all positions on the
      given board in the given collection of positions.
      - This function just changes the given board. It does not
        return a result.
      - You may assume that the squares at all given positions
        do not have any bombs or flags.
    """
    for element in positions:
            disclose_square(board,element)


def disclose_as_far_as_possible(board):
    """
      Disclose the given board as far as possible only using
      patterns (i.e. without any guess).
      - The function will disclose all squares that can be proven
        not to have a bomb. It will flag all squares that can be
        proven to have a bomb. All other squares will be left
        untouched.
      - The function is only defined for boards that do not have
        more than one bomb at a single square.
    """
    is_still_disclosing = True
    while is_still_disclosing:
        kopie = copy_board(board)
        positie = (0,0)
        while positie is not None:
            positie = all_closed_adjacent_squares_with_bombs(board, positie)
            if positie is not None:
                for element in adjacent_positions(board, positie):
                    if not is_open_at(board, element) and nb_flags_at(board, element) == 0:
                        add_flag_at(board, element)
                positie = next_position(board, positie)
        positie = (0, 0)
        while positie is not None:
            positie = all_closed_nonflagged_adjacent_squares_without_bombs(board, positie)
            if positie is not None:
                for element in adjacent_positions(board, positie):
                    if not is_open_at(board, element) and nb_flags_at(board, element) == 0:
                        disclose_square(board, element)
            positie = next_position(board, positie)
        if kopie == board:
            is_still_disclosing = False
    return board




def is_fully_disclosed(board):
    """
      Check whether all squares on the given board have been opened.
      - True if and only if the collection of closed squares is equal
        to the collection of squares with bombs.
      - The function is only defined for boards that do not have
        more than one bomb at a single square.
    """
    positie = (0,0)
    while positie is not None:
        if not is_open_at(board,positie):
            if nb_bombs_at(board, positie) == 0:
                return False
        positie = next_position(board,positie)
    return True


def solve_bruteforce(board, start_position=(0, 0)):
    """
      Return a sequence of successive positions that lead
      to a complete disclosure of all the squares on the board
      that do not have any bombs.
      - Disclosing each of the squares in the order that they
        appear in the resulting positions, leads to a complete
        disclosure of the board.
      - The positions in the resulting sequence are in ascending
        order.
      - None is returned if no such sequence exists.
      - No bombs are stored on any of the resulting positions.
        Moreover, none of the resulting positions will be open
        at the moment they are to be disclosed.
      - During execution, squares on the given board may be
        changed (bombs may be added, squares may be flagged
        or disclosed, ...). However, upon return, the given
        board must be in the state it was in upon entry to
        the function.
      - All positions in front of the start position are either
        already disclosed or they have a bomb.
      - No square on the given board stores more than 1 bomb.
    """
    board = copy_board(board)
    list1 = []
    for i in range(start_position[0], nb_rows(board)):
        for j in range(start_position[1], nb_cols(board)):
            if not is_open_at(board, (i,j)) and nb_bombs_at(board, (i,j)) == 0:
                disclose_square(board,(i,j))
                list1.append((i,j))
    list.sort(list1)
    return list1


def shortest_solution(board, start_position=(0, 0), max_length=None):
    """
      Return the shortest sequence of successive positions not
      exceeding the given maximum length that lead to a complete
      disclosure of all the squares on the board.
      - Disclosing each of the squares in the order that they
        appear in the resulting positions, leads to a complete
        disclosure of the board.
      - The positions in the resulting sequence are in ascending
        order.
      - None is returned if no such sequence exists.
      - No bombs are stored on any of the resulting positions.
        Moreover, none of the resulting positions will be open
        at the moment they are to be disclosed.
      - During execution, squares on the given board may be
        changed (bombs may be added, squares may be flagged
        or disclosed, ...). However, upon return, the given
        board must be in the state it was in upon entry to
        the function.
      - All positions in front of the start position are either
        already disclosed or they have a bomb.
      - No square on the given board stores more than 1 bomb.
    """
    board = copy_board(board)
    solution = []
    pos = start_position
    while pos is not None:
        if nb_adjacent_bombs(board, pos) == 0 and not is_open_at(board, pos) and nb_bombs_at(board, pos) == 0:
            solution.append(pos)
            disclose_square(board, pos)
        pos = next_position(board, pos)
    # for i in range(start_position[0], nb_rows(board)):
    #     for j in range(start_position[1], nb_cols(board)):
    #         if nb_adjacent_bombs(board, (i,j)) == 0 and not is_open_at(board, (i,j)) and nb_bombs_at(board, (i,j)) == 0:
    #             solution.append((i,j))
    #             disclose_square(board, (i,j))
    # for i in range(start_position[0], nb_rows(board)):
    #     for j in range(start_position[1], nb_cols(board)):
    #         if not is_open_at(board, (i,j)) and nb_bombs_at(board, (i,j)) == 0:
    #             solution.append((i,j))
    pos = start_position
    while pos is not None:
        if not is_open_at(board, pos) and nb_bombs_at(board, pos) == 0:
            solution.append(pos)
        pos = next_position(board, pos)
    if max_length is not None:
        if len(solution) > max_length:
            return None
    return solution

    # for i in range(start_position[0], nb_rows(board)):
    #     for j in range(start_position[1], nb_cols(board)):
    #         if nb_adjacent_bombs(board, (i,j)) == 0 and not is_open_at(board, (i,j)) and nb_bombs_at(board, (i,j)) == 0:
    #             solution.append((i,j))
    #             disclose_square(board, (i,j))
    # for i in range(start_position[0], nb_rows(board)):
    #     for j in range(start_position[1], nb_cols(board)):
    #         if not is_open_at(board, (i,j)) and nb_bombs_at(board, (i,j)) == 0:
    #             solution.append((i,j))



