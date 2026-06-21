import json
import os

OUT_FILE = os.path.join(os.path.dirname(__file__), "js", "channels_data.js")

with open(OUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

json_str = text[text.find("["):text.rfind("]")+1]
channels = json.loads(json_str)

# Remove channels that the user reported as broken
bad_keywords = ["Echourouk", "Ennahar", "El Heddaf", "Alkass", "Nessma DZ"]

new_channels = []
for c in channels:
    is_bad = any(bk.lower() in c["name"].lower() for bk in bad_keywords)
    if not is_bad:
        new_channels.append(c)

# Write back
js = "// SEFIANE VIP TV — Cleaned up broken channels\n"
js += f"// Total: {len(new_channels)} channels\n\n"
js += "const parsedChannels = " + json.dumps(new_channels, ensure_ascii=False, indent=2) + ";\n"

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(js)

print("Removed broken channels successfully!")
