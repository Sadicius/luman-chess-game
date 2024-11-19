class Chess:
    def __init__(self):
        self.board = self._initial_board()
        self.current_player = 'white'
        self.last_move = None
        self.castling_rights = {'white': {'kingside': True, 'queenside': True},
                              'black': {'kingside': True, 'queenside': True}}
        
    def _initial_board(self):
        pieces = 'rnbqkbnr'
        board = {}
        for i in range(8):
            # Black pieces
            board[(0, i)] = ('black', pieces[i])
            board[(1, i)] = ('black', 'p')
            # White pieces
            board[(7, i)] = ('white', pieces[i])
            board[(6, i)] = ('white', 'p')
        return board

    def _is_valid_pos(self, pos):
        return 0 <= pos[0] < 8 and 0 <= pos[1] < 8

    def _get_piece_moves(self, pos, checking_moves=False):
        if pos not in self.board:
            return []
        color, piece = self.board[pos]
        moves = []
        row, col = pos

        if piece == 'p':  # Pawn
            direction = -1 if color == 'white' else 1
            # Forward move
            next_pos = (row + direction, col)
            if self._is_valid_pos(next_pos) and next_pos not in self.board:
                moves.append(next_pos)
                # Initial two-square move
                if (color == 'white' and row == 6) or (color == 'black' and row == 1):
                    next_pos = (row + 2*direction, col)
                    if next_pos not in self.board:
                        moves.append(next_pos)
            # Captures
            for dcol in [-1, 1]:
                next_pos = (row + direction, col + dcol)
                if self._is_valid_pos(next_pos):
                    if next_pos in self.board and self.board[next_pos][0] != color:
                        moves.append(next_pos)
                    # En passant
                    elif self.last_move and self.last_move[1] == 'p':
                        last_from, last_to = self.last_move[2:4]
                        if abs(last_from[0] - last_to[0]) == 2:  # Double pawn move
                            if last_to[1] == col + dcol and last_to[0] == row:
                                moves.append(next_pos)

        elif piece == 'n':  # Knight
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1),
                          (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for dr, dc in knight_moves:
                next_pos = (row + dr, col + dc)
                if self._is_valid_pos(next_pos):
                    if next_pos not in self.board or self.board[next_pos][0] != color:
                        moves.append(next_pos)

        elif piece in ['b', 'r', 'q']:  # Bishop, Rook, Queen
            directions = []
            if piece in ['b', 'q']:  # Diagonal moves
                directions += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            if piece in ['r', 'q']:  # Straight moves
                directions += [(0, 1), (0, -1), (1, 0), (-1, 0)]
            
            for dr, dc in directions:
                next_pos = (row + dr, col + dc)
                while self._is_valid_pos(next_pos):
                    if next_pos not in self.board:
                        moves.append(next_pos)
                    elif self.board[next_pos][0] != color:
                        moves.append(next_pos)
                        break
                    else:
                        break
                    next_pos = (next_pos[0] + dr, next_pos[1] + dc)

        elif piece == 'k':  # King
            king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1),
                         (1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dr, dc in king_moves:
                next_pos = (row + dr, col + dc)
                if self._is_valid_pos(next_pos):
                    if next_pos not in self.board or self.board[next_pos][0] != color:
                        moves.append(next_pos)
            
            # Castling (only check if not in check-checking mode)
            if not checking_moves and self.castling_rights[color]['kingside']:
                if (row, 5) not in self.board and (row, 6) not in self.board:
                    if (row, 7) in self.board and self.board[(row, 7)] == (color, 'r'):
                        if not self._is_check(color):
                            moves.append((row, 6))
            
            if not checking_moves and self.castling_rights[color]['queenside']:
                if (row, 3) not in self.board and (row, 2) not in self.board and (row, 1) not in self.board:
                    if (row, 0) in self.board and self.board[(row, 0)] == (color, 'r'):
                        if not self._is_check(color):
                            moves.append((row, 2))

        return moves if checking_moves else [m for m in moves if self._is_legal_move(pos, m)]

    def _is_check(self, color):
        # Find king position
        king_pos = None
        positions = list(self.board.items())  # Create a list before iterating
        
        for pos, piece in positions:
            if piece == (color, 'k'):
                king_pos = pos
                break
        
        if king_pos is None:  # Safety check
            return False
        
        # Check if any opponent piece can capture the king
        opponent = 'black' if color == 'white' else 'white'
        for pos, piece in positions:  # Use the same list for second iteration
            if piece[0] == opponent:
                moves = self._get_piece_moves(pos, checking_moves=True)
                if king_pos in moves:
                    return True
        return False

    def _is_legal_move(self, from_pos, to_pos):
        # Make temporary move
        temp_board = self.board.copy()
        temp_piece = self.board[from_pos]
        self.board[to_pos] = temp_piece
        del self.board[from_pos]
        
        # Check if king is in check after move
        is_legal = not self._is_check(temp_piece[0])
        
        # Restore board
        self.board = temp_board
        return is_legal

    def get_valid_moves(self, pos):
        if pos not in self.board or self.board[pos][0] != self.current_player:
            return []
        return self._get_piece_moves(pos)
    
    def get_current_player(self):
        return self.current_player
    
    def set_current_player(self, current_player):
        self.current_player = current_player
    
    def get_board(self):
        return self.board
    
    def clear_board(self):
        self.board = {}
    
    def get_piece(self, pos):
        return self.board[pos]

    def set_piece(self, pos, piece):
        self.board[pos] = piece
    
    def get_last_move(self):
        return self.last_move


    def make_move(self, from_pos, to_pos):
        if to_pos not in self.get_valid_moves(from_pos):
            return False

        piece = self.board[from_pos]
        
        # Handle castling
        if piece[1] == 'k':
            if abs(to_pos[1] - from_pos[1]) == 2:  # Castling move
                row = from_pos[0]
                if to_pos[1] == 6:  # Kingside
                    self.board[(row, 5)] = self.board[(row, 7)]
                    del self.board[(row, 7)]
                else:  # Queenside
                    self.board[(row, 3)] = self.board[(row, 0)]
                    del self.board[(row, 0)]
            self.castling_rights[piece[0]] = {'kingside': False, 'queenside': False}
        
        # Handle rook moves (for castling rights)
        elif piece[1] == 'r':
            if from_pos[1] == 0:  # Queenside rook
                self.castling_rights[piece[0]]['queenside'] = False
            elif from_pos[1] == 7:  # Kingside rook
                self.castling_rights[piece[0]]['kingside'] = False

        # Handle en passant capture
        if piece[1] == 'p' and to_pos[1] != from_pos[1] and to_pos not in self.board:
            captured_pawn_pos = (from_pos[0], to_pos[1])
            del self.board[captured_pawn_pos]

        # Make the move
        self.board[to_pos] = piece
        del self.board[from_pos]

        # Handle pawn promotion
        if piece[1] == 'p' and (to_pos[0] == 0 or to_pos[0] == 7):
            self.board[to_pos] = (piece[0], 'q')  # Auto-promote to queen

        # Store last move for en passant
        self.last_move = (piece[0], piece[1], from_pos, to_pos)
        
        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        return True

    def is_game_over(self):
        # Create a list of positions and pieces before iterating
        positions = list(self.board.items())
        
        # Check if current player has any legal moves
        for pos, piece in positions:
            if piece[0] == self.current_player and self.get_valid_moves(pos):
                return False
        
        # No legal moves available
        if self._is_check(self.current_player):
            return 'checkmate'
        return 'stalemate'

    def print_board(self):
        symbols = {
            ('white', 'p'): '♙', ('white', 'r'): '♖', ('white', 'n'): '♘',
            ('white', 'b'): '♗', ('white', 'q'): '♕', ('white', 'k'): '♔',
            ('black', 'p'): '♟', ('black', 'r'): '♜', ('black', 'n'): '♞',
            ('black', 'b'): '♝', ('black', 'q'): '♛', ('black', 'k'): '♚'
        }
        print('  a b c d e f g h')
        print('  ---------------')
        for i in range(8):
            print(f"{8-i}|", end=' ')
            for j in range(8):
                piece = self.board.get((i, j))
                if piece:
                    print(symbols[piece], end=' ')
                else:
                    print('.', end=' ')
            print(f"|{8-i}")
        print('  ---------------')
        print('  a b c d e f g h')

# Example usage:
if __name__ == "__main__":
    game = Chess()
    
    # Example game loop
    while True:
        game.print_board()
        print(f"\nCurrent player: {game.current_player}")
        
        # Get move from player
        try:
            move = input("Enter move (e.g., 'e2 e4'): ").split()
            if len(move) != 2:
                print("Invalid input format")
                continue
            
            # Convert chess notation to coordinates
            from_pos = (8 - int(move[0][1]), ord(move[0][0]) - ord('a'))
            to_pos = (8 - int(move[1][1]), ord(move[1][0]) - ord('a'))
            
            if game.make_move(from_pos, to_pos):
                result = game.is_game_over()
                if result:
                    game.print_board()
                    print(f"\nGame over: {result}")
                    break
            else:
                print("Invalid move")
        
        except (ValueError, IndexError):
            print("Invalid input format")