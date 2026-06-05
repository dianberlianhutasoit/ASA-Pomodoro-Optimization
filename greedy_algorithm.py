# Greedy Algorithm untuk memilih aktivitas berdasarkan rasio efisiensi.

def run_greedy(data, max_duration, max_focus):
    alpha = 1
    beta = 1

    items = []

    for item in data:
        duration_ratio = item["duration"] / max_duration
        focus_ratio = item["focus"] / max_focus

        ratio = item["benefit"] / (
            alpha * duration_ratio + beta * focus_ratio
        )

        new_item = item.copy()
        new_item["ratio"] = ratio
        items.append(new_item)

    items = sorted(items, key=lambda x: x["ratio"], reverse=True)

    selected = []
    total_duration = 0
    total_focus = 0
    total_benefit = 0

    for item in items:
        new_duration = total_duration + item["duration"]
        new_focus = total_focus + item["focus"]

        if new_duration <= max_duration and new_focus <= max_focus:
            selected.append(item)
            total_duration = new_duration
            total_focus = new_focus
            total_benefit += item["benefit"]

    return {
        "selected": selected,
        "total_benefit": total_benefit,
        "total_duration": total_duration,
        "total_focus": total_focus,
    }