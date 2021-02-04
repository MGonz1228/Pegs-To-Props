# Pegs-To-Props
Command line application that converts a Peg Solitaire board into boolean logic in Conjunctive Normal Form.

## Usage
To run: ```pegs_to_props.py```

Input file information:
  * file name must be `input.txt`
  * input file format:
    * Line 1: [number of holes] [hole that is empty when the game begins]
    * Next lines: encoding of the puzzle as a set of triples.
      * [1 2 3] means that pegs 1, 2 and 3 are in a row. (1 can jump over 2 and reach 3, and vice versa)
      
#### If you'd like to read the logic behind the encoding, read notes.txt
