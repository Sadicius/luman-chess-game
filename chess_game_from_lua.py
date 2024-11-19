from lupa import LuaRuntime

lua = LuaRuntime(unpack_returned_tuples=True)
with open("chess_game.lua", "r") as file:
    lua_code = file.read()
lua.execute(lua_code)
LUA_INDEX = 1

class Chess:
    def __init__(self):
        self.game = lua.globals().init_game()

    def get_valid_moves(self, pos):
        return self.game.make_move(self.game, pos[0] + LUA_INDEX, pos[1] + LUA_INDEX)

    def make_move(self, from_pos, to_pos):
        return self.game.make_move(self.game, from_pos[0] + LUA_INDEX, from_pos[1] + LUA_INDEX, to_pos[0] + LUA_INDEX, to_pos[1] + LUA_INDEX)

    def is_game_over(self):
        return self.game.is_game_over(self.game)

    def print_board(self):
        return self.game.print_board(self.game)
    
    def get_current_player(self):
        return self.game.get_current_player(self.game)
    
    def set_current_player(self, current_player):
        return self.game.set_current_player(self.game, current_player)
    
    def get_board(self):
        board = {}
        lua_board = dict(self.game.board)
        for k in lua_board:
            pos = list(dict(self.game._pos_unkey(self.game, k)).values())
            board[(pos[0] - LUA_INDEX, pos[1] - LUA_INDEX)] = tuple(dict(lua_board[k]).values())
        return board
    
    def clear_board(self):
        return self.game.clear_board(self.game)
    
    def get_piece(self, pos):
        piece = self.game.get_piece(self.game, pos[0] + LUA_INDEX, pos[1] + LUA_INDEX)
        return tuple(dict(piece).values())
    
    def set_piece(self, pos, piece):
        return self.game.set_piece(self.game, pos[0] + LUA_INDEX, pos[1] + LUA_INDEX, piece[0], piece[1])
    
    def get_valid_moves(self, pos):
        _valid_moves = self.game.get_valid_moves(self.game, pos[0] + LUA_INDEX, pos[1] + LUA_INDEX)
        valid_moves = []
        for val in list(_valid_moves.values()):
            move = list(val.values())
            valid_moves.append((move[0] - LUA_INDEX, move[1] - LUA_INDEX))
        return valid_moves
    
    def get_last_move(self):
        return self.game.last_move
    
    def _is_check(self, color):
        return self.game._is_check(self.game, color)


# Example usage:
if __name__ == "__main__":
    game = Chess()
    
    # Example game loop
    while True:
        game.print_board()
        print(f"\nCurrent player: {game.get_current_player()}")
        
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