# Greedy Algorithm untuk memilih aktivitas berdasarkan rasio manfaat.

def run_greedy(data, max_duration, max_focus):
    items = []

    for item in data:
        copied = item.copy()
        copied["ratio"] = copied["benefit"] / (copied["duration"] + copied["focus"])
        items.append(copied)

    items.sort(key=lambda x: x["ratio"], reverse=True)

    selected = []
    total_duration = 0
    total_focus = 0
    total_benefit = 0

    for item in items:
        if total_duration + item["duration"] <= max_duration and total_focus + item["focus"] <= max_focus:
            selected.append(item)
            total_duration += item["duration"]
            total_focus += item["focus"]
            total_benefit += item["benefit"]

    return {
        "selected": selected,
        "total_benefit": total_benefit,
        "total_duration": total_duration,
        "total_focus": total_focus,
    }
