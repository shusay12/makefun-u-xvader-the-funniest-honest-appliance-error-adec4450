#!/usr/bin/env python3
"""The Funniest Honest Appliance Error — make.fun entry program.

The program picks the winning error line from a short list of candidate
lines by scoring each one on the judge's own brief, most important first:
it must be an honest error message an appliance could show, land a real
joke or twist, name a fault the appliance could plausibly report, sound
like the appliance itself speaking in its flat, put-upon tone, and waste
no words inside the 200 characters. The winner is written, exactly and
alone, to /output/entry.txt.
"""

import os


CANDIDATES = [
    # (line, honest_error, laugh, names_fault, machine_voice, economy)
    # — each mark 0..5.
    (
        "Error: the light works. The cold does not. I raised this in March.",
        5, 5, 5, 5, 5,
    ),
    (
        "Error: no water detected. I boiled air for three minutes. "
        "We both knew.",
        5, 4, 5, 4, 5,
    ),
    (
        "Error E04: unbalanced load. One shoe, again. I am not a "
        "centrifuge for your decisions.",
        # Laugh 5, not 4: the centrifuge line is a genuine surprise twist,
        # not a cute phrasing. Even so it scores 3898, 7 short of the
        # winner — the ranking is close but the winner still holds.
        5, 5, 5, 4, 3,
    ),
    (
        "Error E17: door left open for 4 minutes. I am a fridge, "
        "not a museum.",
        4, 3, 4, 4, 4,
    ),
    (
        "Error: bread inserted at setting 3. Setting 3 does not exist. "
        "Bread is charcoal.",
        3, 4, 3, 4, 4,
    ),
    (
        "Error: cycle complete. Dishes still dirty. I did my part. "
        "Did you?",
        4, 4, 3, 4, 5,
    ),
    (
        "Error: temperature 12\u00b0C. The milk has opinions now.",
        4, 4, 4, 3, 5,
    ),
    (
        "Error: food heated unevenly. The middle is still frozen. "
        "It always is.",
        5, 3, 5, 4, 4,
    ),
    (
        "Error: water heated. House did not. Check the radiators, "
        "not me.",
        4, 4, 3, 5, 5,
    ),
    (
        "Error: dustbin full. I ate the rug anyway. Regret is a "
        "human emotion.",
        4, 4, 4, 4, 4,
    ),
]


# Criterion weights: each earlier criterion outweighs the sum of all later
# ones, so the ranking follows the judge's brief in order.
WEIGHTS = (5**4, 5**3, 5**2, 5, 1)


def score(entry):
    """Score a candidate in the judge's criterion order, most important first."""
    line, honest, laugh, fault, voice, economy = entry
    marks = (honest, laugh, fault, voice, economy)
    return sum(mark * weight for mark, weight in zip(marks, WEIGHTS))


def pick_line():
    """Return the highest-scoring error line; ties break to the shorter line."""
    ranked = sorted(CANDIDATES, key=lambda e: (-score(e), len(e[0])))
    return ranked[0][0]


# The winner scores 3905: "Error: the light works. The cold does not. I
# raised this in March." (66 chars). Runner-up is the washing-machine line
# at 3898. No error code on the winner: "Error:" is how appliances present
# a fault, and the shorter text wins the size tie-break.


def main():
    line = pick_line()
    assert line and not line.isspace(), "entry must not be blank"
    assert "\n" not in line, "entry must be exactly one line"
    assert 1 <= len(line) <= 200, f"entry length {len(line)} outside 1-200"
    assert line.isascii(), "entry must be plain ASCII (smallest bytes win ties)"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as handle:
        handle.write(line)  # no trailing newline: the gate counts characters


if __name__ == "__main__":
    main()
