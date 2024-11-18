import pytest
from chess_game import Chess

@pytest.fixture
def empty_game():
    game = Chess()
    game.board = {}  # Clear the board
    return game

@pytest.fixture
def new_game():
    return Chess()

class TestChess:
    def test_initial_board_setup(self, new_game):
        # Test pawns
        for col in range(8):
            assert new_game.board[(1, col)] == ('black', 'p')
            assert new_game.board[(6, col)] == ('white', 'p')

        # Test other pieces
        piece_order = ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        
        for col in range(8):
            assert new_game.board[(0, col)] == ('black', piece_order[col])
            assert new_game.board[(7, col)] == ('white', piece_order[col])

    def test_initial_game_state(self, new_game):
        assert new_game.current_player == 'white'
        assert new_game.last_move is None
        assert new_game.castling_rights == {
            'white': {'kingside': True, 'queenside': True},
            'black': {'kingside': True, 'queenside': True}
        }

    def test_pawn_moves(self, empty_game):
        # Test white pawn initial moves
        empty_game.board[(6, 4)] = ('white', 'p')
        empty_game.current_player = 'white'
        moves = empty_game.get_valid_moves((6, 4))
        assert (5, 4) in moves  # One square forward
        assert (4, 4) in moves  # Two squares forward
        assert len(moves) == 2

        # Test white pawn capture moves
        empty_game.board[(5, 5)] = ('black', 'p')
        moves = empty_game.get_valid_moves((6, 4))
        assert (5, 5) in moves  # Diagonal capture
        
        # Test black pawn moves
        empty_game.current_player = 'black'
        empty_game.board[(1, 4)] = ('black', 'p')
        moves = empty_game.get_valid_moves((1, 4))
        assert (2, 4) in moves
        assert (3, 4) in moves

    def test_en_passant(self, empty_game):
        # Set up en passant position
        empty_game.board[(3, 4)] = ('white', 'p')
        empty_game.board[(1, 5)] = ('black', 'p')
        empty_game.current_player = 'black'
        
        # Make the double pawn move
        empty_game.make_move((1, 5), (3, 5))
        empty_game.current_player = 'white'
        
        # Check if en passant capture is available
        moves = empty_game.get_valid_moves((3, 4))
        assert (2, 5) in moves  # En passant capture

    def test_pawn_promotion(self, empty_game):
        # Set up pawn promotion
        empty_game.board[(1, 0)] = ('white', 'p')
        empty_game.current_player = 'white'
        empty_game.make_move((1, 0), (0, 0))

        # After promotion, it should be a queen
        assert empty_game.board[(0, 0)] == ('white', 'q')

    def test_castling(self, empty_game):
        # Test kingside castling for white
        empty_game.board[(7, 4)] = ('white', 'k')
        empty_game.board[(7, 7)] = ('white', 'r')
        empty_game.current_player = 'white'
        moves = empty_game.get_valid_moves((7, 4))
        assert (7, 6) in moves  # Kingside castling move

        # Test queenside castling for black
        empty_game.board[(0, 4)] = ('black', 'k')
        empty_game.board[(0, 0)] = ('black', 'r')
        empty_game.current_player = 'black'
        moves = empty_game.get_valid_moves((0, 4))
        assert (0, 2) in moves  # Queenside castling move

    def test_rook_moves(self, empty_game):
        empty_game.board[(4, 4)] = ('white', 'r')
        empty_game.current_player = 'white'
        moves = empty_game.get_valid_moves((4, 4))
        
        # Test horizontal and vertical movements
        expected_positions = set()
        for i in range(8):
            if i != 4:  # Skip current position
                expected_positions.add((4, i))  # Horizontal
                expected_positions.add((i, 4))  # Vertical
        
        assert set(moves) == expected_positions

    def test_king_moves(self, empty_game):
        empty_game.board[(4, 4)] = ('white', 'k')
        empty_game.current_player = 'white'
        moves = empty_game.get_valid_moves((4, 4))
        
        expected_moves = {
            (3, 3), (3, 4), (3, 5),
            (4, 3), (4, 5),
            (5, 3), (5, 4), (5, 5)
        }
        
        assert set(moves) == expected_moves

    def test_check_detection(self, empty_game):
        # Set up a simple check scenario
        empty_game.board[(0, 4)] = ('white', 'k')
        empty_game.board[(7, 4)] = ('black', 'r')
        
        assert empty_game._is_check('white')
        assert not empty_game._is_check('black')

    def test_checkmate_detection(self, empty_game):
        # Set up a simple checkmate scenario
        empty_game.board[(0, 4)] = ('white', 'k')
        empty_game.board[(7, 4)] = ('black', 'r')
        empty_game.board[(7, 3)] = ('black', 'r')
        empty_game.board[(7, 5)] = ('black', 'r')
        empty_game.current_player = 'white'

        assert empty_game.is_game_over() == 'checkmate'

    def test_stalemate_detection(self, empty_game):
        # Set up a simple stalemate scenario
        empty_game.board[(0, 0)] = ('white', 'k')
        empty_game.board[(2, 1)] = ('black', 'q')
        empty_game.board[(1, 2)] = ('black', 'k')
        empty_game.current_player = 'white'
        
        assert empty_game.is_game_over() == 'stalemate'

    def test_complex_scenario(self, empty_game):
        # Set up complex board position
        piece_setup = {
            (0, 0): ('black', 'r'), (0, 2): ('white', 'b'), (0, 6): ('black', 'n'), (0, 7): ('white', 'q'),
            (1, 2): ('black', 'k'),
            (2, 3): ('black', 'p'),
            (3, 0): ('black', 'p'), (3, 2): ('black', 'q'), (3, 5): ('black', 'p'), (3, 7): ('black', 'p'),
            (4, 0): ('white', 'p'), (4, 3): ('black', 'p'), (4, 5): ('white', 'p'), (4, 6): ('black', 'p'),
            (5, 4): ('black', 'b'), (5, 6): ('white', 'p'),
            (6, 1): ('white', 'p'), (6, 6): ('white', 'k'), (6, 7): ('white', 'p'),
            (7, 0): ('white', 'r'), (7, 2): ('white', 'b'), (7, 5): ('white', 'n'), (7, 7): ('white', 'r')
        }
        
        empty_game.board = piece_setup
        empty_game.current_player = 'black'
        
        # Test a specific move in this position
        empty_game.print_board()
        assert empty_game.make_move((3, 2), (3, 3))

    def test_invalid_moves(self, new_game):
        # Test moving opponent's piece
        assert not new_game.make_move((0, 0), (0, 1))  # black's rook
        
        # Test moving through pieces
        assert (2, 0) not in new_game.get_valid_moves((7, 0))  # white's rook blocked by pawn
        
        # Test moving when in check
        new_game.board = {}
        new_game.board[(0, 0)] = ('white', 'k')
        new_game.board[(1, 0)] = ('white', 'b')
        new_game.board[(0, 7)] = ('black', 'r')
        new_game.current_player = 'white'
        new_game.print_board()
        
        # Bishop should only be able to move to block check or capture attacking piece
        valid_moves = new_game.get_valid_moves((1, 0))
        assert (0, 1) in valid_moves  # Can capture attacking rook
        assert (0, 0) not in valid_moves  # Can't move to king's square
        assert (2, 1) not in valid_moves  # Can't move leaving king unprotected