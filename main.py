# Program utama untuk menjalankan eksperimen algoritma ASA Pomodoro.

import os
import time
import pandas as pd

from greedy_algorithm import run_greedy
from dynamic_programming import run_dynamic_programming
from simulated_annealing import run_simulated_annealing

INPUT_FILE = "Lampiran Dataset ASA.xlsx"
OUTPUT_EXCEL = "Hasil eksperimen algoritma.xlsx"
OUTPUT_CSV = "Hasil eksperimen algoritma.csv"

SCENARIOS = {
    "Data Kecil": {"sheet": "Data Kecil", "max_duration": 8, "max_focus": 18},
    "Data Sedang": {"sheet": "Data Sedang", "max_duration": 16, "max_focus": 36},
    "Data Besar": {"sheet": "Data Besar", "max_duration": 24, "max_focus": 54},
}

SA_PARAMETERS = {
    "initial_temperature": 1000,
    "cooling_rate": 0.95,
    "minimum_temperature": 0.01,
    "iterations_per_temperature": 100,
    "random_seed": 42,
}

SA_TESTS = {
    "K1": {
        "initial_temperature": 100,
        "cooling_rate": 0.90,
        "minimum_temperature": 0.01,
        "iterations_per_temperature": 100,
        "random_seed": 42,
        "keterangan": "Pencarian cepat, tetapi eksplorasi solusi masih terbatas.",
    },
    "K2": {
        "initial_temperature": 1000,
        "cooling_rate": 0.95,
        "minimum_temperature": 0.01,
        "iterations_per_temperature": 100,
        "random_seed": 42,
        "keterangan": "Eksplorasi cukup luas, hasil stabil, dan waktu masih wajar.",
    },
    "K3": {
        "initial_temperature": 1000,
        "cooling_rate": 0.99,
        "minimum_temperature": 0.01,
        "iterations_per_temperature": 100,
        "random_seed": 42,
        "keterangan": "Eksplorasi lebih luas, tetapi waktu eksekusi menjadi lebih lama.",
    },
}


def load_dataset(sheet_name):
    df = pd.read_excel(INPUT_FILE, sheet_name=sheet_name)
    df = df.dropna(subset=["Kode", "Aktivitas Belajar"])

    data = []
    for _, row in df.iterrows():
        data.append(
            {
                "code": str(row["Kode"]).strip(),
                "activity": str(row["Aktivitas Belajar"]).strip(),
                "duration": int(row["Durasi Pomodoro"]),
                "focus": int(row["Beban Fokus"]),
                "benefit": int(row["Nilai Manfaat"]),
            }
        )
    return data


def selected_codes(result):
    return ", ".join(item["code"] for item in result["selected"])


def run_with_time(function, data, max_duration, max_focus, **kwargs):
    start = time.perf_counter()
    result = function(data, max_duration, max_focus, **kwargs)
    end = time.perf_counter()
    runtime_ms = (end - start) * 1000
    return result, runtime_ms


def calculate_gap(optimal_benefit, algorithm_benefit):
    if optimal_benefit == 0:
        return 0
    return ((optimal_benefit - algorithm_benefit) / optimal_benefit) * 100


def add_result(rows, scenario_name, algorithm_name, result, runtime_ms, optimal_benefit):
    rows.append(
        {
            "Skenario": scenario_name,
            "Algoritma": algorithm_name,
            "Aktivitas Terpilih": selected_codes(result),
            "Total Manfaat": result["total_benefit"],
            "Total Durasi": result["total_duration"],
            "Total Fokus": result["total_focus"],
            "Waktu Eksekusi (ms)": round(runtime_ms, 3),
            "Optimality Gap (%)": round(calculate_gap(optimal_benefit, result["total_benefit"]), 2),
        }
    )

def run_sa_test():
    data = load_dataset("Data Kecil")
    max_duration = SCENARIOS["Data Kecil"]["max_duration"]
    max_focus = SCENARIOS["Data Kecil"]["max_focus"]

    dp_result, _ = run_with_time(run_dynamic_programming, data, max_duration, max_focus)
    optimal_benefit = dp_result["total_benefit"]

    rows = []

    for config_name, params in SA_TESTS.items():
        sa_params = {
            "initial_temperature": params["initial_temperature"],
            "cooling_rate": params["cooling_rate"],
            "minimum_temperature": params["minimum_temperature"],
            "iterations_per_temperature": params["iterations_per_temperature"],
            "random_seed": params["random_seed"],
        }

        result, runtime_ms = run_with_time(
            run_simulated_annealing,
            data,
            max_duration,
            max_focus,
            **sa_params,
        )

        rows.append(
            {
                "Konfigurasi": config_name,
                "Initial Temperature": params["initial_temperature"],
                "Cooling Rate": params["cooling_rate"],
                "Minimum Temperature": params["minimum_temperature"],
                "Iterasi per Temperatur": params["iterations_per_temperature"],
                "Aktivitas Terpilih": selected_codes(result),
                "Total Manfaat": result["total_benefit"],
                "Total Durasi": result["total_duration"],
                "Total Fokus": result["total_focus"],
                "Waktu Eksekusi (ms)": round(runtime_ms, 3),
                "Optimality Gap (%)": round(calculate_gap(optimal_benefit, result["total_benefit"]), 2),
                "Keterangan": params["keterangan"],
            }
        )

    preliminary_df = pd.DataFrame(rows)
    preliminary_df.to_excel("uji SA.xlsx", index=False)
    preliminary_df.to_csv("uji SA.csv", index=False)

    print("Uji pendahuluan SA selesai.")
    print("Output Excel: uji SA.xlsx")
    print("Output CSV  : uji SA.csv")

def main():
    if not os.path.exists(INPUT_FILE):
        raise FileNotFoundError(
            f"File '{INPUT_FILE}' belum ada. Letakkan file Excel dataset dalam folder yang sama dengan main.py."
        )

    rows = []

    for scenario_name, scenario in SCENARIOS.items():
        data = load_dataset(scenario["sheet"])
        max_duration = scenario["max_duration"]
        max_focus = scenario["max_focus"]

        greedy_result, greedy_time = run_with_time(run_greedy, data, max_duration, max_focus)
        dp_result, dp_time = run_with_time(run_dynamic_programming, data, max_duration, max_focus)
        sa_result, sa_time = run_with_time(
            run_simulated_annealing, data, max_duration, max_focus, **SA_PARAMETERS
        )

        optimal_benefit = dp_result["total_benefit"]

        add_result(rows, scenario_name, "Greedy", greedy_result, greedy_time, optimal_benefit)
        add_result(rows, scenario_name, "Dynamic Programming", dp_result, dp_time, optimal_benefit)
        add_result(rows, scenario_name, "Simulated Annealing", sa_result, sa_time, optimal_benefit)

    result_df = pd.DataFrame(rows)
    result_df.to_excel(OUTPUT_EXCEL, index=False)
    result_df.to_csv(OUTPUT_CSV, index=False)

    run_sa_test()

    print("Eksperimen selesai.")
    print(f"Output Excel: {OUTPUT_EXCEL}")
    print(f"Output CSV  : {OUTPUT_CSV}")


main()

