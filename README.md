# Connect4MLSolver
This project brings you Connect Four in a remastered version, allowing you to enjoy the classic gameplay. 
However, what makes this project unique is the integration of an ML-powered solver that enables you to challenge a smart opponent.

### Minimax Algorithm

- Classic decision-making technique for two-player games like Connect Four or Chess
- Explores all possible moves up to a certain depth (5) in the game tree, maximizing own advantage and minimizing opponent's advantage
- Considers current game state and simulates potential future moves, creating game tree representing all possible paths
- Each leaf node of tree is assigned a score, representing expected outcome of the game for that move
- ML Solver then backpropagates these scores to determine the best move to make at the current state

### Data Pruning (Alpha-Beta Pruning)

- Implemented to improve performance and reduce computational overload during the Minimax algorithm
- Alpha-Beta Pruning allows ML solver to discard less promising branches of the game tree, reducing the number of nodes to evaluate
- When move is found that guarantees worse outcome than any previously examined move, ML Solver immediately stops evaluating that branch
- Enables Connect 4 ML Solver to explore deeper into the game tree while making timely and informed decisions
