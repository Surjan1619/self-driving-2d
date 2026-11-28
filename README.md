# Self-driving 2D car

A red car in a pygame window that will learn to follow a dark oval line by itself, using the same **sense → think → act** loop as a real self-driving car.

Made for *Assignment 1: Make a Car Drive Itself*.

## Run it

Needs Python 3.11+ and pygame-ce.

```bash
python -m venv .venv
.venv/bin/pip install pygame-ce
.venv/bin/python main.py
```

## Keys

| Key | Action |
|---|---|
| Left / Right arrows | Steer |
| Up / Down arrows | Speed +0.5 / −0.5 |
| A | Autopilot on / off |
| R | Reset the car to the start |
| Esc | Quit |

## Progress

- [x] Step 6: starter code runs
- [x] Step 7: drive with the keyboard
- [x] Step 8: sensors
- [ ] Step 9: autopilot
- [ ] Step 10: measure and improve

## Files

- `main.py`: the game and the car's loop
- `week1-research-notes.md`: Week 1 research (loop, sensors, SAE levels, crash analysis)
- `docs/`: NTSB crash report HAR-17/02 and its Russian translation
- `diagrams/`: pictures used in the notes
