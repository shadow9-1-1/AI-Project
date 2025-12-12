# Phase II: Adversarial Search Algorithms - Connect Four

## Project Overview

This project implements and compares **Minimax** and **Alpha-Beta Pruning** algorithms for the Connect Four game. It provides a complete game environment, AI agents, performance analysis, and comprehensive visualizations.

## Features

### ✅ Complete Implementation

1. **Connect Four Game Environment**
   - Full game state representation (6×7 board)
   - Move validation and state transitions
   - Win/draw detection (horizontal, vertical, diagonal)
   - Efficient board operations

2. **Minimax Algorithm**
   - Recursive implementation with depth limiting
   - Performance metrics tracking
   - Optimal move selection
   - Evaluation function for non-terminal states

3. **Alpha-Beta Pruning**
   - Optimized search with branch pruning
   - Alpha/Beta bound maintenance
   - Pruning count tracking
   - Same optimal results as Minimax

4. **Evaluation Function**
   - Window-based pattern recognition
   - Center column control heuristic
   - Threat detection (2-in-a-row, 3-in-a-row)
   - Balanced offensive/defensive scoring

5. **Visualizations**
   - Professional board state rendering
   - Game tree exploration diagrams
   - Performance comparison charts
   - AI move progression tracking

6. **Performance Analysis**
   - Time complexity comparison
   - Node exploration metrics
   - Pruning effectiveness analysis
   - Multiple depth testing

## File Structure

```
Phase 2/
├── Phase 2.ipynb          # Main implementation notebook
├── README.md              # This file
└── (generated outputs)    # Visualizations and results
```

## Requirements

- Python 3.8+
- NumPy
- Matplotlib
- Seaborn

Install dependencies:
```bash
pip install numpy matplotlib seaborn
```

## Usage

### Running the Notebook

1. Open `Phase 2.ipynb` in Jupyter Notebook or VS Code
2. Run all cells sequentially (Shift+Enter)
3. View outputs, visualizations, and performance metrics

### Key Components

#### Game Environment
```python
game = ConnectFour()
game.make_move(3)  # Drop piece in column 3
game.display()     # Show current board
```

#### Minimax Agent
```python
minimax_agent = MinimaxAgent(game, max_depth=6)
best_move, metrics = minimax_agent.get_best_move(game, player=1)
```

#### Alpha-Beta Agent
```python
alphabeta_agent = AlphaBetaAgent(game, max_depth=6)
best_move, metrics = alphabeta_agent.get_best_move(game, player=1)
```

#### Performance Comparison
```python
compare_algorithms(game_state, player=1, depth=6)
```

#### Visualization
```python
visualize_board(game, title="My Board")
visualize_performance_comparison([3, 4, 5, 6])
```

### Interactive Play

Uncomment and run the interactive play section to play against the AI:
```python
play_human_vs_ai(use_alphabeta=True, ai_depth=6)
```

## Performance Results

### Typical Metrics (Depth 6)

| Algorithm | Time (s) | Nodes Explored | Branches Pruned |
|-----------|----------|----------------|-----------------|
| Minimax   | 0.5-2.0  | 20,000-50,000  | 0               |
| Alpha-Beta| 0.2-0.8  | 8,000-20,000   | 5,000-15,000    |

**Improvements:**
- ⚡ 50-60% faster execution
- 📉 60-70% fewer nodes explored
- ✅ Identical optimal moves

## Game Description

### State Representation
- **Board**: 6 rows × 7 columns
- **Players**: 1 (X/Red) and 2 (O/Yellow)
- **Empty cells**: 0
- **Turn tracking**: Alternates between players

### Terminal Conditions
- **Win**: Four consecutive pieces (horizontal/vertical/diagonal)
- **Draw**: Board full with no winner
- **Max moves**: 42

### Complexity
- **Branching factor**: ~4-5 (average)
- **Max depth**: 42 moves
- **State space**: ~4.5 × 10¹² reachable states

## Algorithm Details

### Minimax
- Explores all possible move sequences
- Maximizes score for Player 1, minimizes for Player 2
- Guarantees optimal play
- Time: O(b^d)

### Alpha-Beta Pruning
- Eliminates provably suboptimal branches
- Maintains alpha (MAX lower bound) and beta (MIN upper bound)
- Prunes when β ≤ α
- Time: O(b^(d/2)) to O(b^(3d/4))

### Evaluation Function
- **Wins**: ±1000
- **Three-in-a-row**: ±10
- **Two-in-a-row**: ±2
- **Center control**: +3 per piece

## Visualizations

The notebook generates:

1. **Board States**: Color-coded pieces with move highlighting
2. **Game Trees**: Node exploration with pruning visualization
3. **Performance Charts**: 
   - Time comparison (bar charts)
   - Nodes explored (bar charts)
   - Improvement percentages (line graphs)
   - Pruning effectiveness (bar charts)
4. **AI vs AI Games**: Step-by-step move progression

## Discussion Topics

### Pruning Effectiveness
- Best case: 50% reduction per level
- Depends on move ordering
- Greater benefits at deeper depths
- Critical moves prune more aggressively

### Heuristic Evaluation
- Enables practical play with depth limits
- Balances accuracy and computation
- Pattern recognition approximates full search
- Trade-offs between evaluation complexity and speed

### Practical Considerations
- Depth 6-8: Strong tactical play
- Center columns: Strategically important
- Move ordering: Significantly impacts pruning
- Time constraints: Iterative deepening useful

## Future Enhancements

- [ ] Transposition tables (position caching)
- [ ] Iterative deepening with time limits
- [ ] Opening book for common positions
- [ ] Endgame databases for perfect play
- [ ] Neural network evaluation function
- [ ] Parallel search (multi-threading)

## Author

**Course**: CSAI 301  
**Project**: Phase II - Adversarial Search  
**Date**: December 12, 2025

## License

This project is for educational purposes as part of CSAI 301 coursework.

---

## Quick Start Guide

1. **Open notebook**: `Phase 2.ipynb`
2. **Run all cells**: Execute sequentially
3. **View results**: Check performance comparisons and visualizations
4. **Experiment**: Modify depths, positions, or parameters
5. **Play**: Uncomment interactive play to challenge the AI

**Enjoy exploring adversarial search algorithms!** 🎮🤖
