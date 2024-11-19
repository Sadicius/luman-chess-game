import chess
import random
import time
from chess_game import Chess
import traceback

class ChessValidator:
    def __init__(self):
        self.official_board = chess.Board()
        
        # Disable rules in official board that not implemented in our board
        def is_insufficient_material():
            return False
        self.official_board.is_insufficient_material = is_insufficient_material
        def is_seventyfive_moves():
            return False
        self.official_board.is_seventyfive_moves = is_seventyfive_moves
        def is_fivefold_repetition():
            return False
        self.official_board.is_fivefold_repetition = is_fivefold_repetition

        
        self.our_board = Chess()
        self.move_history = []
        
    def _convert_official_move_to_ours(self, move):
        """Convert chess library move to our format"""
        from_square = (7 - chess.square_rank(move.from_square),
                      chess.square_file(move.from_square))
        to_square = (7 - chess.square_rank(move.to_square),
                      chess.square_file(move.to_square))
        return from_square, to_square
    
    def _get_random_legal_move(self):
        """Get a random legal move from the official chess library"""
        move = None

        try:
            legal_moves = list(self.official_board.legal_moves)
            if legal_moves:
                # Filter moves and automatically promote to queen
                move_candidates = []
                for m in legal_moves:
                    if m.promotion is not None:
                        # Create a new move with queen promotion
                        move_candidates.append(chess.Move(
                            from_square=m.from_square,
                            to_square=m.to_square,
                            promotion=chess.QUEEN
                        ))
                    else:
                        move_candidates.append(m)
                        
                move = random.choice(move_candidates)
        except Exception as e:
            print(f"Error getting legal moves: {e}")
            self._print_comparison()
            
        return move
    
    def _board_states_match(self):
        """Compare board states between implementations"""
        try:
            official_to_our = {
                'P': ('white', 'p'), 'R': ('white', 'r'), 'N': ('white', 'n'),
                'B': ('white', 'b'), 'Q': ('white', 'q'), 'K': ('white', 'k'),
                'p': ('black', 'p'), 'r': ('black', 'r'), 'n': ('black', 'n'),
                'b': ('black', 'b'), 'q': ('black', 'q'), 'k': ('black', 'k')
            }
            
            for rank in range(8):
                for file in range(8):
                    official_piece = self.official_board.piece_at(chess.square(file, 7-rank))
                    our_pos = (rank, file)
                    
                    if official_piece is None:
                        if our_pos in self.our_board.get_board():
                            return False, f"Mismatch at {our_pos}: Official: Empty, Ours: {self.our_board.get_board()[our_pos]}"
                    else:
                        if our_pos not in self.our_board.get_board():
                            return False, f"Mismatch at {our_pos}: Official: {official_piece}, Ours: Empty"
                        if self.our_board.get_board()[our_pos] != official_to_our[official_piece.symbol()]:
                            return False, f"Mismatch at {our_pos}: Official: {official_piece}, Ours: {self.our_board.get_board()[our_pos]}"
            return True, ""
        except Exception as e:
            return False, f"Error comparing boards: {traceback.format_exc()}"
    
    def _print_comparison(self):
        """Print both boards side by side for visual comparison"""
        print("\nOfficial Chess Library Board:")
        print(self.official_board)
        print("\nOur Chess Implementation Board:")
        self.our_board.print_board()
        print("\nCurrent player (Official):", "White" if self.official_board.turn else "Black")
        print("Current player (Ours):", self.our_board.get_current_player())
        
        #print("\nMove history:")
        #for i, move in enumerate(self.move_history):
        #    print(f"Move {i+1}: {move}")
    
    def validate_n_random_games(self, num_games=10, max_moves=50):
        """Run multiple random games to validate implementations"""
        games_completed = 0
        total_moves = 0
        start_time = time.time()
        
        try:
            for game_num in range(num_games):
                print(f"\nStarting game {game_num + 1}")
                self.official_board.reset()
                self.our_board = Chess()
                self.move_history = []
                
                for move_num in range(max_moves):
                    if move_num % 100 == 0:
                        print(f"Move {move_num}")
                    
                    # Get random move from official library
                    move = self._get_random_legal_move()
                    
                    # Check for game end
                    if move is None or self.official_board.is_game_over():
                        print(f"Game {game_num + 1} completed after {move_num} moves")
                        games_completed += 1
                        total_moves += move_num
                        break
                    
                    try:
                        # Convert and apply move to both boards
                        from_square, to_square = self._convert_official_move_to_ours(move)
                        
                        # Store move in history
                        self.move_history.append(f"{move} ({from_square} to {to_square})")
                        
                        # Make moves on both boards
                        self.official_board.push(move)
                        move_success = self.our_board.make_move(from_square, to_square)
                        
                        # Validate move
                        if not move_success:
                            print(f"Move validation failed on move {move_num + 1}")
                            self._print_comparison()
                            return False
                        
                        # Validate board state
                        match_result, error_msg = self._board_states_match()
                        if not match_result:
                            print(f"Board state mismatch on move {move_num + 1}")
                            print(error_msg)
                            self._print_comparison()
                            return False
                        
                        # Validate game state
                        official_game_over = self.official_board.is_game_over()
                        official_outcome = self.official_board.outcome()
                        our_game_over = bool(self.our_board.is_game_over())
                        
                        if official_game_over != our_game_over:
                            print(f"Game state mismatch on move {move_num + 1}")
                            print(f"Official game over: {official_game_over} Outcome: {official_outcome}")
                            print(f"Our game over: {our_game_over}")
                            self._print_comparison()
                            return False
                            
                    except Exception as e:
                        print(f"Error during move {move_num + 1}: {e}")
                        self._print_comparison()
                        return False
        
        except Exception as e:
            print(f"Unexpected error during validation: {e}")
            self._print_comparison()
            return False
            
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\nValidation completed successfully!")
        print(f"Games completed: {games_completed}")
        print(f"Total moves: {total_moves}")
        print(f"Average moves per game: {total_moves/num_games:.1f}")
        print(f"Time taken: {duration:.2f} seconds")
        print(f"Moves per second: {total_moves/duration:.1f}")
        return True
    
def main():
    validator = ChessValidator()
    
    print("Starting chess implementation validation...")
    print("This will run multiple random games comparing our implementation")
    print("against the official chess library.\n")
    
    # Run validation with different parameters
    validation_scenarios = [
        (1, 5000),   # 5 quick games
        # (3, 30),   # 3 medium-length games
        # (2, 50)    # 2 longer games
    ]
    
    for num_games, max_moves in validation_scenarios:
        print(f"\nRunning {num_games} games with max {max_moves} moves each...")
        if not validator.validate_n_random_games(num_games, max_moves):
            print("Validation failed!")
            return
        
    print("\nAll validation scenarios completed successfully!")

if __name__ == "__main__":
    main()