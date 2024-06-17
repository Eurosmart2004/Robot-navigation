# Robot Navigation Program

## Overview

This program facilitates robot navigation using various pathfinding algorithms. It includes a graphical user interface (GUI) option and a jump feature for enhanced pathfinding with 6 methods.

## Installation

Before running the program, ensure that you have Python installed on your system. Then, follow these steps to set up a virtual environment and install the necessary packages:

1. Create a virtual environment:

```
python -m venv venv
```

2. Activate the virtual environment:

- On Windows:

```
.\venv\Scripts\activate
```

- On macOS and Linux:

```
source venv/bin/activate
```

3. Install the required packages:

```
pip install -r requirements.txt
```

## Running the Program

Execute the program via the terminal using the following structure:

```
./search <filename> <method>
```

- `<filename>`: Name of the file containing navigation data.
- `<method>`: Search method to use. Options include:
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - Greedy Best-First Search (GBFS)
  - A\* Search (A_star)
  - Bidirectional Search (Bidirection)
  - Bidirectional A\* Search (A_star_bidirection)

### GUI Version

For a GUI experience, append `--gui`:

```
./search <filename> <method> --gui
```

Example:

```
./search RobotNav-test.txt a_star --gui
```

### Jump Feature

Enable jump actions with `--jump` for A\* or Bidirectional A\* methods:

```
./search <filename> a_star --jump
./search <filename> a_star_bidirection --jump
```

Combine GUI with jump feature:

```
./search <filename> a_star --jump --gui
./search <filename> a_star_bidirection --jump --gui
```

### Performance Tracking

To track execution time, use `--calc`:

```
./search <filename> <method> --calc
```

This can be combined with `--jump` and/or `--gui`.
