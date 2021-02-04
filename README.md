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
      
Output will be in 2 files:
 * my_propositions.txt, contains two types of lines
   * Lists (surrounded in square brackets) are jumps in the following format:
     * INDEX [Peg doing the jumping, Peg that will be jumped, Landing hole for jumping peg, time step of jump]
   * Tuples (surrounded in parenthesis) are pegs in the following format:
     * INDEX (Peg, time step)
     
     
 * my_output.txt refers to the indices in my_propositions.txt and generates clauses in CNF.
   * `-1 17` in this example encodes: ¬[1, 2, 3, 1] ∨ (1, 1)
     * this simply means NOT(Peg 1 jumps Peg 2 and lands in hole 3 at time step 1) OR (Peg in hole 1 at time step 1)
     * "either there is a Peg in hole 1 at start time, or it's impossible to jump from hole 1 at start time"
  
#### If you'd like to read the rest of the logic behind the encoding, read notes.txt
