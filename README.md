
# Scrabble Solver App

![Scrabble Solver](sample_image.png)

This is a Scrabble Solver app built using the Kivy framework. It helps you find the best words you can play on your Scrabble board, given your current tiles and the tiles on the board.

## Features

- **Scrabble Solver**: Input the letters on your rack and the tiles on the Scrabble board, and the app will suggest valid words and their scores.
- **Interactive Board**: You can input your current game state by clicking on the individual tiles of the Scrabble board. The app highlights the triple-word, double-word, triple-letter, and double-letter score multipliers.
- **Navigation**: You can navigate through the list of suggested words using the "<" and ">" buttons.

## Installation

To run the Scrabble Solver app, make sure you have Kivy installed. You can install it using pip:

```bash
pip install kivy
```

You also need a `backend` module that contains the `Board` class, which is used for solving Scrabble boards. Make sure this module is in the same directory as your main script.

## Usage

1. Run the app by executing the `MyApp` class in your Python environment.

```bash
python main.py
```

2. Input the tiles on your rack in the bottom section of the app. Use the "Clear" button to reset both your rack and the Scrabble board.
3. Click on the tiles on the Scrabble board to fill in the board state. The app will highlight special score multipliers for triple-word, double-word, triple-letter, and double-letter.
4. Click the "Enter" button to find the best words based on the current game state. The suggested words and their scores will appear on the board.
5. Use the "<" and ">" buttons to navigate through the list of suggested words.

## Sample Images

Here's a sample image of the Scrabble Solver app in action:

![Scrabble Solver](sample_image.png)

## Acknowledgments

This app was created by Levi Chinecherem C. It is powered by the `backend` module for Scrabble solving.

## License

This project is licensed under the [Your License] - see the [LICENSE](LICENSE) file for details.
