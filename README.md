# About

Chess Game written in Python with the help of https://claude.ai/. Game mechanics are validated with the help of https://python-chess.readthedocs.io/. 

## Installation

Install requirements:
```
pip install -r requirement.txt
```

## Playing

To start the game:
```
python chess_game.py
```

Output:
```
  a b c d e f g h
  ---------------
8| ♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜ |8
7| ♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟ |7
6| . . . . . . . . |6
5| . . . . . . . . |5
4| . . . . . . . . |4
3| . . . . . . . . |3
2| ♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙ |2
1| ♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖ |1
  ---------------
  a b c d e f g h

Current player: white
Enter move (e.g., 'e2 e4'):
```



## Validation

Run game validation with the help of external chess library.
```
python chess_validator.py
```

## Tests

Run test scenarios.
```
pytest chess_tests.py
```
