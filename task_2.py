from dataclasses import dataclass
from typing import List, Dict

@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int

@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int

def _validate_jobs_and_constraints(jobs: List[PrintJob], limits: PrinterConstraints) -> None:
    """Validate inputs to ensure feasible scheduling."""
    if limits.max_volume <= 0 or limits.max_items <= 0:
        raise ValueError("Invalid printer constraints")
    for j in jobs:
        if j.volume <= 0 or j.print_time <= 0:
            raise ValueError(f"Job {j.id} has invalid volume or print_time")
        if j.priority not in (1, 2, 3):
            raise ValueError(f"Job {j.id} has invalid priority (1..3)")
        if j.volume > limits.max_volume:
            raise ValueError(f"Job {j.id} exceeds printer max volume")

def optimize_printing(print_jobs: List[Dict], printer_limits: Dict) -> Dict:
    """Greedily batch jobs by priority respecting volume/items limits."""
    jobs = [PrintJob(**j) for j in print_jobs]
    limits = PrinterConstraints(**printer_limits)
    _validate_jobs_and_constraints(jobs, limits)
    jobs_sorted = sorted(jobs, key=lambda j: j.priority)

    total_time = 0
    print_order: List[str] = []
    group: List[PrintJob] = []
    group_volume = 0.0

    for job in jobs_sorted:
        can_add = (len(group) + 1 <= limits.max_items) and (group_volume + job.volume <= limits.max_volume)
        if can_add:
            group.append(job)
            group_volume += job.volume
        else:
            if group:
                total_time += max(x.print_time for x in group)
                print_order.extend([x.id for x in group])
            group = [job]
            group_volume = job.volume

    if group:
        total_time += max(x.print_time for x in group)
        print_order.extend([x.id for x in group])

    return {"print_order": print_order, "total_time": total_time}

if __name__ == "__main__":
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 3, "print_time": 150}
    ]
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]
    constraints = {"max_volume": 300, "max_items": 2}

    print("Тест 1 (однаковий пріоритет):")
    r1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {r1['print_order']}")
    print(f"Загальний час: {r1['total_time']} хвилин")

    print("\nТест 2 (різні пріоритети):")
    r2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {r2['print_order']}")
    print(f"Загальний час: {r2['total_time']} хвилин")

    print("\nТест 3 (перевищення обмежень):")
    r3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {r3['print_order']}")
    print(f"Загальний час: {r3['total_time']} хвилин")
