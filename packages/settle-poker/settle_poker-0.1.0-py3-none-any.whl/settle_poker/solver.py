from ortools.linear_solver import pywraplp


def solve_poker_settlement(balances):
    """Solves the poker settlement problem for minimum transactions.

    Args:
        balances: A list of integers representing the net balances of each player.
            Positive values indicate winnings, negative values indicate losses.

    Returns:
        A dictionary mapping (sender, receiver) pairs to transaction amounts.
    """

    n = len(balances)
    solver = pywraplp.Solver.CreateSolver('GLOP')

    # Create variables for transactions between each pair of players.
    transactions = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                transactions[(i, j)] = solver.NumVar(0, solver.infinity(), f't_{i}_{j}')

    # Balance constraints: total sent - total received = net balance
    for i in range(n):
        constraint = solver.Constraint(balances[i], balances[i])
        for j in range(n):
            if i != j:
                constraint.SetCoefficient(transactions[(i, j)], 1)  # Sending money
                constraint.SetCoefficient(transactions[(j, i)], -1)  # Receiving money

    # Objective: minimize the total number of transactions
    objective = solver.Objective()
    for transaction in transactions.values():
        objective.SetCoefficient(transaction, 1)
    objective.SetMinimization()

    # Solve the problem
    status = solver.Solve()

    # Extract and return the solution
    result = {}
    if status == pywraplp.Solver.OPTIMAL:
        for (i, j), transaction in transactions.items():
            if transaction.solution_value() > 0:
                result[(i, j)] = transaction.solution_value()
    else:
        print("The problem does not have an optimal solution!")

    return result


# Example usage:
balances = [40, -50, -20, 31, -1]  # Example balances for 4 players
result = solve_poker_settlement(balances)
print(result)
