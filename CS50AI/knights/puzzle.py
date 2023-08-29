from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Helper -- From Lecture 1 --

# For each knowledge base, you’ll likely want to encode two different types of information:
#   (1) information about the structure of the problem itself (i.e., information given in the definition of a Knight and Knave puzzle),
#   and (2) information about what the characters actually said.


# In each of the above puzzles,
#   Each character is either a knight or a knave.
#   A knight will always tell the truth: if knight states a sentence, then that sentence is true.
#   Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false.

# Consider what it means if a sentence is spoken by a character.
#   Under what conditions is that sentence true?
#   Under what conditions is that sentence false?
#   How can you express that as a logical sentence?

# --------------------------

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Rules
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),

    # A said:
    # If it's a knight what they said is True
    Implication(And(AKnight, AKnave), AKnight),
    # If it's a Knave what they said is False
    Implication(Not(And(AKnight, AKnave)), AKnave)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Rules
    # A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A said:
    # If it's a knight what they said is True
    Implication(And(AKnave, BKnave), AKnight),

    # If it's a Knave what they said is False
    Implication(Not(And(AKnave, BKnave)), AKnave)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Rules
    # A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),

    # A said:
    # If it's a knight what they said is True
    Implication(
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        ),
        And(AKnight, BKnight)
    ),

    # If it's a Knave what they said is False
    Implication(Not(
        Or(
            And(AKnight, BKnight),
            And(AKnave, BKnave)
        )),
        And(AKnave, BKnight)
    ),

    # B said:
    # If it's a knight what they said is True
    Implication(
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight)
        ),
        And(BKnight, AKnave)
    ),

    # If it's a Knave what they said is False
    Implication(Not(
        Or(
            And(AKnight, BKnave),
            And(AKnave, BKnight))
    ),
        And(AKnave, BKnave)
    ),


)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Rules
    # A
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    # B
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    # C
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),

    # A said
    # If it's a knight what they said is True
    Implication(Or(AKnight, AKnave), AKnight),

    # If it's a Knave what they said is False
    Implication(Not(Or(AKnight, AKnave)), AKnave),

    # B said
    # If it's a knight what they said is True
    Implication(And(AKnave, CKnave), BKnight),

    # If it's a Knave what they said is False
    Implication(Not(And(AKnave, CKnave)), BKnave),

    # C said
    # If it's a knight what they said is True
    Implication(AKnight, CKnight),

    # If it's a Knave what they said is False
    Implication(Not(AKnight), CKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
