# Dynamic Programming untuk 0/1 Knapsack dengan batas waktu dan fokus.

def run_dynamic_programming(data, max_duration, max_focus):
    n = len(data)
    dp = [[[0 for _ in range(max_focus + 1)] for _ in range(max_duration + 1)] for _ in range(n + 1)]
    keep = [[[False for _ in range(max_focus + 1)] for _ in range(max_duration + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = data[i - 1]
        duration = item["duration"]
        focus = item["focus"]
        benefit = item["benefit"]

        for w in range(max_duration + 1):
            for f in range(max_focus + 1):
                without_item = dp[i - 1][w][f]
                with_item = -1

                if duration <= w and focus <= f:
                    with_item = benefit + dp[i - 1][w - duration][f - focus]

                if with_item > without_item:
                    dp[i][w][f] = with_item
                    keep[i][w][f] = True
                else:
                    dp[i][w][f] = without_item

    selected = []
    w = max_duration
    f = max_focus

    for i in range(n, 0, -1):
        if keep[i][w][f]:
            item = data[i - 1]
            selected.append(item)
            w -= item["duration"]
            f -= item["focus"]

    selected.reverse()

    return {
        "selected": selected,
        "total_benefit": sum(item["benefit"] for item in selected),
        "total_duration": sum(item["duration"] for item in selected),
        "total_focus": sum(item["focus"] for item in selected),
    }
