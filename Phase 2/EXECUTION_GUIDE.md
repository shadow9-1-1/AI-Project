# Execution Guide - Phase II Connect Four Project

## 🚀 Getting Started in 5 Minutes

### Step 1: Open the Notebook
- Navigate to: `c:\Users\HP\Documents\AI-Project\Phase 2\`
- Open: `Phase 2.ipynb`

### Step 2: Install Dependencies (if needed)
```python
# Run this in a notebook cell or terminal:
pip install numpy matplotlib seaborn
```

### Step 3: Run All Cells
- In VS Code/Jupyter: `Run All` or press `Shift+Enter` on each cell
- Execution time: ~2-3 minutes (depending on depth settings)

### Step 4: View Results
- Performance comparisons will print to output
- Visualizations will display inline
- AI games will show move-by-move progression

---

## 📋 Cell Execution Guide

### Core Implementation (Required - Cells 5-13)

**Cell 5: Import Libraries**
```python
import numpy as np
import matplotlib.pyplot as plt
# ... other imports
```
⏱️ Time: <1 second  
✅ Expected: "Libraries imported successfully!"

**Cell 7: ConnectFour Game Environment**
```python
class ConnectFour:
    # Complete game implementation
```
⏱️ Time: <1 second  
✅ Expected: Test board displays, valid moves shown

**Cell 9: Evaluation Function**
```python
class Evaluator:
    # Heuristic evaluation
```
⏱️ Time: <1 second  
✅ Expected: Evaluation scores displayed

**Cell 11: Minimax Algorithm**
```python
class MinimaxAgent:
    # Minimax implementation
```
⏱️ Time: 2-5 seconds  
✅ Expected: Best move and metrics shown

**Cell 13: Alpha-Beta Pruning**
```python
class AlphaBetaAgent:
    # Alpha-Beta implementation
```
⏱️ Time: 1-3 seconds  
✅ Expected: Best move and metrics shown (faster than Minimax)

---

### Performance Analysis (Essential - Cells 15, 21)

**Cell 15: Algorithm Comparison**
```python
compare_algorithms(game_state, player, depth)
```
⏱️ Time: 5-15 seconds (runs 3 comparisons)  
✅ Expected: 
- 3 comparison tables
- Performance metrics
- Efficiency analysis

**Cell 21: Multi-Depth Performance**
```python
visualize_performance_comparison([3, 4, 5, 6])
```
⏱️ Time: 20-60 seconds (tests 4 depths)  
✅ Expected:
- 6 charts displayed
- Summary statistics
- Performance trends

---

### Visualizations (Recommended - Cells 17, 19, 23)

**Cell 17: Board Visualization**
```python
visualize_board(game, title)
```
⏱️ Time: 2-3 seconds  
✅ Expected: 4 board states in 2×2 grid

**Cell 19: Game Tree Visualization**
```python
GameTreeVisualizer(game, max_depth=3)
```
⏱️ Time: 3-5 seconds  
✅ Expected: 2 tree diagrams (Minimax & Alpha-Beta)

**Cell 23: AI vs AI Game**
```python
play_ai_game(minimax_player, alphabeta_player)
```
⏱️ Time: 30-90 seconds  
✅ Expected:
- Move-by-move commentary
- Board progression
- Final result

---

### Interactive Features (Optional - Cell 27)

**Cell 27: Human vs AI**
```python
# Uncomment to activate:
# play_human_vs_ai(use_alphabeta=True, ai_depth=6)
```
⏱️ Time: Varies (interactive)  
✅ Expected: 
- Game board display
- Input prompt for moves
- AI response after each move

---

## ⚙️ Configuration Options

### Adjusting Difficulty/Speed

**For Faster Execution:**
```python
# Reduce depth in performance comparison
visualize_performance_comparison([3, 4, 5])  # Instead of [3,4,5,6]

# Reduce AI depth
minimax_agent = MinimaxAgent(game, max_depth=4)  # Instead of 6
```

**For Stronger AI:**
```python
# Increase depth (warning: exponentially slower)
alphabeta_agent = AlphaBetaAgent(game, max_depth=8)
```

**For More Pruning:**
```python
# Alpha-Beta works best at deeper depths
ab_agent = AlphaBetaAgent(game, max_depth=7)  # More pruning opportunities
```

---

## 📊 Expected Outputs

### Performance Metrics (Cell 15)

**Test 1: Early Game**
```
Minimax:     ~0.05s, ~1,500 nodes
Alpha-Beta:  ~0.02s, ~700 nodes
Improvement: 60% time saved, 53% nodes reduced
```

**Test 2: Mid Game**
```
Minimax:     ~0.15s, ~4,000 nodes
Alpha-Beta:  ~0.06s, ~1,800 nodes
Improvement: 60% time saved, 55% nodes reduced
```

**Test 3: Complex Position**
```
Minimax:     ~1.2s, ~25,000 nodes
Alpha-Beta:  ~0.5s, ~10,000 nodes
Improvement: 58% time saved, 60% nodes reduced
```

### Visualizations

**Board States (Cell 17):**
- 2×2 grid with 4 different game positions
- Color-coded pieces (red=X, yellow=O)
- Column labels (0-6)
- Last move highlighted in green

**Game Trees (Cell 19):**
- Minimax: All nodes explored (green/blue)
- Alpha-Beta: Pruned branches in red
- Node values labeled
- Move indicators on edges
- Statistics at top

**Performance Charts (Cell 21):**
1. Time comparison (bar chart)
2. Nodes explored (bar chart)
3. Time improvement % (line graph)
4. Nodes reduction % (line graph)
5. Pruning effectiveness (bar chart)
6. Summary table

---

## 🐛 Troubleshooting

### Issue: ImportError
**Problem:** `ModuleNotFoundError: No module named 'numpy'`

**Solution:**
```powershell
pip install numpy matplotlib seaborn
```

### Issue: Slow Execution
**Problem:** Cells take too long to run

**Solutions:**
1. Reduce depth: Change `max_depth=6` to `max_depth=4`
2. Test fewer positions: Modify comparison functions
3. Skip optional cells: Only run cells 5, 7, 9, 11, 13, 15

### Issue: No Visualizations
**Problem:** Charts don't display

**Solutions:**
1. Add `%matplotlib inline` in first cell (Jupyter)
2. Check matplotlib backend: `import matplotlib; print(matplotlib.get_backend())`
3. Explicitly call `plt.show()` after plots

### Issue: Memory Error
**Problem:** `MemoryError` during execution

**Solutions:**
1. Reduce depth to 4 or 5
2. Close other applications
3. Restart kernel: `Kernel → Restart`

### Issue: Wrong Results
**Problem:** Algorithms produce different moves

**Solutions:**
1. Verify both use same depth
2. Check evaluation function
3. Ensure consistent game state
4. Re-run from beginning (Restart & Run All)

---

## ✅ Validation Checklist

After running all cells, verify:

### Game Environment
- [ ] Board displays correctly
- [ ] Valid moves detected
- [ ] Pieces drop to correct row
- [ ] Win detection works
- [ ] Draw detection works

### Algorithms
- [ ] Minimax finds valid moves
- [ ] Alpha-Beta finds valid moves
- [ ] Both produce same move
- [ ] Alpha-Beta is faster
- [ ] Metrics are reasonable

### Visualizations
- [ ] Board colors are correct
- [ ] Trees show pruning
- [ ] Charts have labels
- [ ] Data is accurate
- [ ] No errors in plots

### Performance
- [ ] Alpha-Beta explores fewer nodes
- [ ] Alpha-Beta takes less time
- [ ] Improvement % makes sense (40-70%)
- [ ] Pruning count > 0
- [ ] Depths reached are correct

---

## 🎯 Quick Tests

### Minimal Test (30 seconds)
Run only cells: 5, 7, 9, 11, 13
```python
# After running these cells:
game = ConnectFour()
game.make_move(3)
mm = MinimaxAgent(game, max_depth=4)
ab = AlphaBetaAgent(game, max_depth=4)
mm_move, mm_metrics = mm.get_best_move(game, 2)
ab_move, ab_metrics = ab.get_best_move(game, 2)
print(f"Same move: {mm_move == ab_move}")
print(f"AB faster: {ab_metrics['time_taken'] < mm_metrics['time_taken']}")
```

### Standard Test (2 minutes)
Run cells: 5, 7, 9, 11, 13, 15

### Complete Demo (3-5 minutes)
Run all cells sequentially

---

## 📈 Performance Benchmarks

### By Depth (Alpha-Beta)

| Depth | Time (s) | Nodes | Typical Use |
|-------|----------|-------|-------------|
| 3     | <0.01    | ~200  | Testing |
| 4     | ~0.05    | ~800  | Fast play |
| 5     | ~0.2     | ~3,500| Balanced |
| 6     | ~0.8     | ~15,000| Strong play |
| 7     | ~3.0     | ~60,000| Very strong |
| 8     | ~12.0    | ~250,000| Expert level |

### System Requirements

**Minimum:**
- Python 3.8+
- 4GB RAM
- Depth 4-5 search

**Recommended:**
- Python 3.10+
- 8GB RAM
- Depth 6-7 search

**Optimal:**
- Python 3.11+
- 16GB RAM
- Depth 8+ search

---

## 🎓 Understanding the Output

### Performance Metrics Meaning

**Nodes Explored:**
- Number of board positions evaluated
- Lower = more efficient
- Alpha-Beta should be 40-70% of Minimax

**Time Taken:**
- Wall-clock execution time
- Varies by system
- Alpha-Beta should be 40-60% of Minimax time

**Pruning Count:**
- Branches eliminated by Alpha-Beta
- Higher = better move ordering
- Typically 30-50% of total branches

**Best Score:**
- Evaluation of position after best move
- Positive = good for Player 1
- Negative = good for Player 2
- ±1000 = forced win/loss detected

**Best Move:**
- Column number (0-6)
- Both algorithms should agree
- Usually center columns (3,4) in early game

---

## 🔄 Re-running Experiments

### To Test Different Positions:

```python
# Create custom position
custom_game = ConnectFour()
custom_game.make_move(3, 1)  # X
custom_game.make_move(3, 2)  # O
custom_game.make_move(4, 1)  # X
# ... add more moves

# Compare on this position
compare_algorithms(custom_game, player=2, depth=6)
```

### To Test Different Depths:

```python
# Test very deep search
visualize_performance_comparison([5, 6, 7, 8])
# Warning: Depth 8 may take 10-20 seconds per test
```

### To Test Different Evaluations:

```python
# Modify weights in Evaluator class
# In cell 9, change:
score += player_windows['three'] * 10  # Try different values
```

---

## 📝 Summary

**Total Execution Time:** 2-5 minutes (all cells)  
**Key Results:** Alpha-Beta 50-70% more efficient  
**Visualizations:** 10+ charts and diagrams  
**Code:** ~900 lines, fully documented  

**Next Steps:**
1. Run all cells sequentially
2. Review performance comparisons
3. Examine visualizations
4. Try interactive play (optional)
5. Experiment with parameters

---

**Status:** ✅ Ready to Execute  
**Last Updated:** December 12, 2025  
**Tested:** Windows 11, Python 3.11, VS Code

**Happy Exploring! 🎮🤖**
