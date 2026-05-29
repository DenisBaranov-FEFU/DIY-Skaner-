import json
import subprocess

def run(cmd):
    return subprocess.check_output(cmd, shell=True, text=True).strip()

os_release = {}

with open("/etc/os-release") as f:
    for line in f:
        if "=" in line:
            k, v = line.strip().split("=", 1)
            os_release[k] = v.strip('"')

arch = run("uname -m")

packages_raw = run(
    r"rpm -qa --queryformat '%{NAME}|%{VERSION}-%{RELEASE}|%{ARCH}|%{SIZE}|%{SUMMARY}\n'"
)

packages = []

for line in packages_raw.splitlines():
    parts = line.split("|")

    if len(parts) != 5:
        continue

    name, version, pkg_arch, size, summary = parts

    pkg = {
        "name": name,
        "version": version,
        "arch": pkg_arch,
        "description": summary,
        "size": size
    }

    packages.append(pkg)

result = {
    "OS": {
        "name": os_release.get("NAME"),
        "version": os_release.get("VERSION"),
        "arch": arch,
        "id": os_release.get("ID"),
        "version_id": os_release.get("VERSION_ID"),
        "description": os_release.get(
            "PRETTY_NAME",
            f"{os_release.get('NAME')} {os_release.get('VERSION')}"
        ),
        "codename": os_release.get("REDOS_CODENAME", "")
    },
    "packages": packages
}

with open("result_task_4.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"Готово. Пакетов найдено: {len(packages)}")
