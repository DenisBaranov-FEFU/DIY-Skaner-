import json, re
from pathlib import Path
from packageurl import PackageURL

files = [
    "requirements.txt",
    "requirements-flake8.txt",
    "docs/requirements.txt",
    "docs/cpp/requirements.txt",
    "caffe2/requirements.txt",
    "scripts/release_notes/requirements.txt",
    ".circleci/ecr_gc_docker/requirements.txt"
]

deps = []
seen = set()
pattern = re.compile(r'^([A-Za-z0-9_.-]+)\s*([<>=!~]+)?\s*([A-Za-z0-9_.+-]+)?')

for file in files:
    path = Path(file)
    if not path.exists():
        continue

    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("-"):
            continue

        line = line.split("#")[0].strip()
        m = pattern.match(line)
        if not m:
            continue

        name = m.group(1)
        version = m.group(3) or "unknown"

        key = (name.lower(), version)
        if key in seen:
            continue
        seen.add(key)

        deps.append({
            "name": name,
            "version": version,
            "ecosystem": "pypi",
            "url": f"https://pypi.org/project/{name}/",
            "purl": PackageURL(type="pypi", name=name, version=version).to_string()
        })

with open("../result_task_1.json", "w", encoding="utf-8") as f:
    json.dump(deps, f, ensure_ascii=False, indent=4)

print(f"Готово: найдено зависимостей: {len(deps)}")
print("Файл создан: ~/lab3/result_task_1.json")
