"""merge dalamud plugin repos into repo.json & keep the newest version of each plugin."""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from itertools import zip_longest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

REPOS = [
    "https://aetherment.sevii.dev/plugin",
    "https://puni.sh/api/plugins",
    "https://puni.sh/api/repository/akechi",
    "https://puni.sh/api/repository/croizat",
    "https://puni.sh/api/repository/erdelf",
    "https://puni.sh/api/repository/herc",
    "https://puni.sh/api/repository/ice",
    "https://puni.sh/api/repository/kawaii",
    "https://puni.sh/api/repository/knightmore",
    "https://puni.sh/api/repository/vera",
    "https://puni.sh/api/repository/veyn",
    "https://raw.githubusercontent.com/Aether-Tools/DalamudPlugins/main/repo.json",
    "https://raw.githubusercontent.com/Aida-Enna/XIVPlugins/refs/heads/main/repo.json",
    "https://raw.githubusercontent.com/Aireil/MyDalamudPlugins/master/pluginmaster.json",
    "https://raw.githubusercontent.com/anomek/MyDalamudPlugins/master/pluginmaster.json",
    "https://raw.githubusercontent.com/Eternita-S/MyDalamudPlugins/main/pluginmaster.json",
    "https://raw.githubusercontent.com/Etheirys/Brio/main/repo.json",
    "https://raw.githubusercontent.com/FFXIV-CombatReborn/CombatRebornRepo/main/pluginmaster.json",
    "https://raw.githubusercontent.com/KangasZ/DalamudPluginRepository/refs/heads/main/plugin_repository.json",
    "https://raw.githubusercontent.com/NightmareXIV/MyDalamudPlugins/main/pluginmaster.json",
    "https://raw.githubusercontent.com/Ottermandias/Glamourer/main/repo.json",
    "https://raw.githubusercontent.com/UnknownX7/DalamudPluginRepo/master/pluginmaster.json",
    "https://raw.githubusercontent.com/jawslouis/MakePlacePlugin/master/MakePlacePlugin.json",
    "https://raw.githubusercontent.com/lichie567/LMeter/main/repo.json",
    "https://raw.githubusercontent.com/marzent/IINACT/main/repo.json",
    "https://raw.githubusercontent.com/paissaheavyindustries/Dalamud-Repo/main/repo.json",
    "https://raw.githubusercontent.com/reckhou/DalamudPlugins-Ori/api6/pluginmaster.json",
    "https://repo.caraxian.com",
]
IGNORE_STATUS = {"https://repo.caraxian.com"}  # serves a valid repo with a non-2xx status


def fetch(url):
    try:
        # Some hosts (Cloudflare) reject urllib's default User-Agent with 403.
        resp = urlopen(Request(url, headers={"User-Agent": "ffxiv-plugins-uni"}), timeout=60)
    except HTTPError as e:
        if url not in IGNORE_STATUS:
            raise
        resp = e
    return json.loads(resp.read().decode("utf-8-sig"))


def version(plugin):
    """'7.5.8.1' -> [7, 5, 8, 1]; non-numeric parts count as 0."""
    parts = str(plugin.get("AssemblyVersion", "")).split(".")
    return [int(m.group()) if (m := re.match(r"\d+", p)) else 0 for p in parts]


def is_newer(a, b):
    diffs = (x > y for x, y in zip_longest(version(a), version(b), fillvalue=0) if x != y)
    return next(diffs, False)


def main():
    with ThreadPoolExecutor(len(REPOS)) as pool:
        jobs = [(url, pool.submit(fetch, url)) for url in REPOS]

    unique = {}
    for url, job in jobs:
        try:
            data = job.result()
        except Exception as e:
            print(f"Error fetching {url}: {e}", file=sys.stderr)
            continue
        plugins = [p for p in (data if isinstance(data, list) else [data])
                   if isinstance(p, dict) and isinstance(p.get("Name"), str)]
        print(f"Added {len(plugins)} plugin(s) from {url}")
        for p in plugins:
            old = unique.get(p["Name"])
            if old is None or is_newer(p, old):
                if old is not None:
                    print(f"Found duplicate, updating {p['Name']} from {old.get('AssemblyVersion')} to {p.get('AssemblyVersion')}")
                unique[p["Name"]] = p

    result = sorted(unique.values(), key=lambda p: p["Name"].casefold())
    with open("repo.json", "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
