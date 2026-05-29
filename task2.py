import json
import os
import requests

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

        print("Проверяю:", dep["name"])

        r = requests.post(
            API_URL,
            headers=headers,
            json={
                "query": query,
                "variables": {
                    "package": dep["name"],
                    "ecosystem": "PIP"
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
                "first_patched_version":
                    patched["identifier"] if patched else None
            })

        secure_versions = [
            x["first_patched_version"]
            for x in vulns
            if x["first_patched_version"]
        ]

        result.append({
            "name": dep["name"],
            "version": dep["version"],
            "ecosystem": dep["ecosystem"],
            "url": dep["url"],
            "purl": dep["purl"],
            "vulnerabilities": vulns,
            "secure_version":
                secure_versions[-1]
                if secure_versions else None
        })

    except Exception as e:

        print("Ошибка:", dep["name"], e)

with open("result_task_2.json", "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=4)

print()
print("ГОТОВО")
print("Файл: result_task_2.json")
print("Пакетов:", len(result))
