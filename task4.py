import json
import subprocess
import datetime
import uuid

def run(cmd):
    """Выполняет команду в оболочке и возвращает результат."""
    return subprocess.check_output(cmd, shell=True, text=True).strip()

# 1. Считываем информацию об операционной системе
os_release = {}
try:
    with open("/etc/os-release") as f:
        for line in f:
            if "=" in line:
                k, v = line.strip().split("=", 1)
                os_release[k] = v.strip('"')
except FileNotFoundError:
    os_release = {"NAME": "Unknown Linux", "VERSION": "Unknown", "ID": "linux"}

arch = run("uname -m")
os_name = os_release.get("NAME", "Linux")
os_version = os_release.get("VERSION", "Unknown")
distro_id = os_release.get("ID", "linux").lower() # Нужно для формирования purl (например, 'redos', 'centos', 'ubuntu')

# 2. Получаем список установленных RPM-пакетов
# Формат: NAME|VERSION-RELEASE|ARCH|SIZE|SUMMARY
packages_raw = run(
    r"rpm -qa --queryformat '%{NAME}|%{VERSION}-%{RELEASE}|%{ARCH}|%{SIZE}|%{SUMMARY}\n'"
)

components = []
for line in packages_raw.splitlines():
    parts = line.split("|")
    if len(parts) < 3:
        continue
    
    name = parts[0]
    version = parts[1]
    pkg_arch = parts[2]
    size = parts[3] if len(parts) > 3 else "unknown"
    summary = parts[4] if len(parts) > 4 else ""

    # Формируем Package URL (purl) в стандарте CycloneDX для RPM
    # Формат: pkg:rpm/<distro>/<name>@<version>?arch=<arch>
    purl = f"pkg:rpm/{distro_id}/{name}@{version}?arch={pkg_arch}"
    
    component = {
        "type": "library",
        "name": name,
        "version": version,
        "purl": purl,
        "description": summary
    }
    
    # Добавляем дополнительные свойства, если они есть
    if size != "unknown":
        component["properties"] = [{"name": "size", "value": size}]
        
    components.append(component)

# 3. Собираем итоговый словарь в строгом формате CycloneDX 1.4
sbom = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.4",
    "serialNumber": f"urn:uuid:{uuid.uuid4()}",
    "version": 1,
    "metadata": {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "component": {
            "type": "operating-system",
            "name": os_name,
            "version": os_version,
            "description": os_release.get("PRETTY_NAME", f"{os_name} {os_version}")
        }
    },
    "components": components
}

# 4. Сохраняем результат
# Сохраняем как sbom.json, так как это стандартное имя для osv-scanner, 
# но этот файл также является полноценным результатом Задания 4.
output_filename = "bom.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(sbom, f, indent=4, ensure_ascii=False)

print(f"✅ Готово. Сформирован SBOM (CycloneDX) с {len(components)} пакетами.")
print(f"📁 Файл сохранен как: {output_filename}")
