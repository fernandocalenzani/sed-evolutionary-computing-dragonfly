def ranking(results):
    ranked_results = []
    costs = [result[13] for result in results]

    sorted_costs = sorted(costs)

    for cost in sorted_costs:
        index = costs.index(cost)
        ranked_results.append(results[index])

    return ranked_results
