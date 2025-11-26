import os
import re

REPLACEMENTS = {
    r"ρ": "rho",
    r"ɸ600": "phi600",
    r"ɸ300": "phi300",
    r"ɸ3": "phi3",
    r"τ30": "tau30",
    r"μ": "mu",
    r"Δp/L": "dp_per_ft",
    r"ΔPdpc": "dPdpc",
    r"ΔPdph": "dPdph",
    r"ΔPdch": "dPdch",
    r"Δp\b": "dp",
    r"Δpb": "dpb",
    r"γb": "gb",
    r"γp": "gp",
    r"τp": "tp",
    r"ρe": "rhoe",
}

def replace_keys_safely(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = content
    for pattern, replacement in REPLACEMENTS.items():
        new_content = re.sub(pattern, replacement, new_content)

    if new_content != content:
        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"✅ Updated: {path}")

for root, _, files in os.walk("."):
    for file in files:
        if file.endswith((".py", ".json", ".yaml", ".yml", ".md", ".txt")):
            replace_keys_safely(os.path.join(root, file))
