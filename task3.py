import json
from collections import Counter

with open("result_task_2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

rows = []

for dep in data.get("dependencies", []):
    vulns = dep.get("vulns", [])

    if not vulns:
        continue

    severity = Counter()

    for v in vulns:
        sev = v.get("severity", "unknown").lower()
        severity[sev] += 1

    fixed_versions = []

    for v in vulns:
        fixed_versions.extend(v.get("fix_versions", []))

    fixed_versions = sorted(set(fixed_versions))

    strategy = (
        "Обновить пакет до безопасной версии"
        if fixed_versions else
        "Ограничить использование и мониторить обновления"
    )

    row = {
        "name": dep.get("name"),
        "version": dep.get("version"),
        "critical": severity.get("critical", 0),
        "high": severity.get("high", 0),
        "medium": severity.get("medium", 0),
        "low": severity.get("low", 0),
        "fix_versions": fixed_versions,
        "strategy": strategy
    }

    rows.append(row)

rows.sort(
    key=lambda x: (
        x["critical"],
        x["high"],
        x["medium"],
        x["low"]
    ),
    reverse=True
)

with open("result_task_3.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=4, ensure_ascii=False)

print(f"Готово. Уязвимых пакетов: {len(rows)}")
