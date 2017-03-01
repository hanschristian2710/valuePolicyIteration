#Policy Iteration and Value Iteration

**Value Iteration**
This algorithm works by always choosing the action that maximize the expected utility and we don't know initial state true value, but we know the reward. 

**Policy Iteration**
This algorithm works a little bit different from value iteration, it start with a random policy, compute each state’s utility given that policy, and then select a new optimal policy. 

**Description**
There are 4 files (prob_*.txt) - each containing a transition matrix for one of the 4 actions - WEST, NORTH, EAST, SOUTH. The columns are in the order s, s’, P(s’ | s, a). “rewards.txt” contains 81 values corresponding to R(s). We will use value and policy iteration to find the optimal policy for the MDP. 

# Running
1. Clone repo
2. Run from terminal

simply, 
``` 
cd dir
python policy_iteration.py
or
python value_iteration.py
```

# Thanks
CSE 150 - UCSD
