import json
from collections import Counter
from packaging.version import parse as parse_version

with open("result_task_2.json", "r", encoding="utf-8") as f:
    data = json.load(f) # Здесь теперь плоский список, а не словарь с ключом "dependencies"

rows = []
for dep in data:
    vulns = dep.get("vulnerabilities", []) # Исправлено имя ключа
    if not vulns:
        continue

    severity = Counter()
    for v in vulns:
        sev = v.get("severity", "unknown").lower()
        severity[sev] += 1

    fixed_versions = []
    for v in vulns:
        if v.get("first_patched_version"): # Исправлено имя ключа
            fixed_versions.append(v["first_patched_version"])

    # Убираем дубликаты и сортируем версии по возрастанию
    fixed_versions = sorted(list(set(fixed_versions)), key=parse_version)

    strategy = (
        f"Обновить пакет до версии {fixed_versions[-1]} или выше"
        if fixed_versions else
        "Ограничить использование и мониторить обновления (патча нет)"
    )

    row = {
        "name": dep.get("name"),
        "version": dep.get("version"),
        "ecosystem": dep.get("ecosystem"), # Добавлено для соответствия ТЗ
        "critical": severity.get("critical", 0),
        "high": severity.get("high", 0),
        "medium": severity.get("medium", 0),
        "low": severity.get("low", 0),
        "secure_version": fixed_versions[-1] if fixed_versions else None, # Добавлено для соответствия ТЗ
        "strategy": strategy
    }

    rows.append(row)

# Сортировка по убыванию критичности (critical -> high -> medium -> low)
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
