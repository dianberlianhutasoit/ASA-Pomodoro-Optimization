# Simulated Annealing untuk mencari kombinasi aktivitas mendekati optimal.

import math
import random

def evaluate_solution(data, solution, max_duration, max_focus):
    selected = [item for item, chosen in zip(data, solution) if chosen == 1]

    total_duration = sum(item["duration"] for item in selected)
    total_focus = sum(item["focus"] for item in selected)
    total_benefit = sum(item["benefit"] for item in selected)

    if total_duration > max_duration or total_focus > max_focus:
        penalty = 0
        if total_duration > max_duration:
            penalty += (total_duration - max_duration) * 1000
        if total_focus > max_focus:
            penalty += (total_focus - max_focus) * 1000
        score = total_benefit - penalty
    else:
        score = total_benefit

    return score, selected, total_benefit, total_duration, total_focus


def make_initial_solution(data, max_duration, max_focus):
    solution = [0] * len(data)
    total_duration = 0
    total_focus = 0

    indexes = list(range(len(data)))
    random.shuffle(indexes)

    for idx in indexes:
        item = data[idx]
        if total_duration + item["duration"] <= max_duration and total_focus + item["focus"] <= max_focus:
            solution[idx] = 1
            total_duration += item["duration"]
            total_focus += item["focus"]

    return solution


def run_simulated_annealing(
    data,
    max_duration,
    max_focus,
    initial_temperature=1000,
    cooling_rate=0.95,
    minimum_temperature=0.01,
    iterations_per_temperature=100,
    random_seed=42,
):
    random.seed(random_seed)

    current_solution = make_initial_solution(data, max_duration, max_focus)
    current_score, _, _, _, _ = evaluate_solution(data, current_solution, max_duration, max_focus)

    best_solution = current_solution[:]
    best_score = current_score
    temperature = initial_temperature

    while temperature > minimum_temperature:
        for _ in range(iterations_per_temperature):
            candidate_solution = current_solution[:]
            index = random.randrange(len(candidate_solution))
            candidate_solution[index] = 1 - candidate_solution[index]

            candidate_score, _, _, _, _ = evaluate_solution(data, candidate_solution, max_duration, max_focus)
            delta = candidate_score - current_score

            if delta > 0 or random.random() < math.exp(delta / temperature):
                current_solution = candidate_solution
                current_score = candidate_score

            if current_score > best_score:
                best_solution = current_solution[:]
                best_score = current_score

        temperature *= cooling_rate

    score, selected, total_benefit, total_duration, total_focus = evaluate_solution(
        data, best_solution, max_duration, max_focus
    )

    return {
        "selected": selected,
        "total_benefit": total_benefit,
        "total_duration": total_duration,
        "total_focus": total_focus,
    }
