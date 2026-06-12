import json
import os
import requests
from packaging.version import parse as parse_version # Добавляем для корректного сравнения версий

TOKEN = os.getenv("GITHUB_TOKEN")
API_URL = "https://api.github.com/graphql"

query = """
query($package: String!, $ecosystem: SecurityAdvisoryEcosystem!) {
  securityVulnerabilities(first: 100, package: $package, ecosystem: $ecosystem) {
    nodes {
      vulnerableVersionRange
      firstPatchedVersion {
        identifier
      }
      advisory {
        ghsaId
        severity
      }
    }
  }
}
"""

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

with open("result_task_1.json", "r", encoding="utf-8") as f:
    deps = json.load(f)

result = []
for dep in deps:
    try:
        print("Проверяю: ", dep["name"])

        r = requests.post(
            API_URL,
            headers=headers,
            json={
                "query": query,
                "variables": {
                    "package": dep["name"],
                    "ecosystem": "PIP" # GitHub API требует PIP в верхнем регистре для Python
                }
            },
            timeout=30
        )

        data = r.json()
        vulns = []

        for item in data.get("data", {}).get("securityVulnerabilities", {}).get("nodes", []):
            patched = item.get("firstPatchedVersion")
            vulns.append({
                "name": item["advisory"]["ghsaId"],
                "severity": item["advisory"]["severity"].lower(),
                "vulnerable_range": item["vulnerableVersionRange"],
                "first_patched_version": patched["identifier"] if patched else None
            })

        # Собираем все версии, в которых были исправления
        secure_versions = [
            x["first_patched_version"]
            for x in vulns
            if x["first_patched_version"]
        ]

        # ИСПРАВЛЕНИЕ: Находим максимальную версию, чтобы закрыть все уязвимости сразу
        final_secure_version = None
        if secure_versions:
            final_secure_version = str(max(secure_versions, key=parse_version))

        result.append({
            "name": dep["name"],
            "version": dep["version"],
            "ecosystem": dep["ecosystem"],
            "url": dep["url"],
            "purl": dep["purl"],
            "vulnerabilities": vulns,
            "secure_version": final_secure_version # Записываем корректную максимальную версию
        })

    except Exception as e:
        print("Ошибка: ", dep["name"], e)

with open("result_task_2.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print("\nГОТОВО")
print("Файл: result_task_2.json")
print("Пакетов:", len(result))
