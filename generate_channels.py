"""
Downloads the full iptv-org Arabic M3U playlist and generates channels_data.js
"""
import urllib.request
import re
import json
import os

M3U_URL = "https://iptv-org.github.io/iptv/languages/ara.m3u"
OUT_FILE = os.path.join(os.path.dirname(__file__), "js", "channels_data.js")

CAT_MAP = {
    "News":        "أخبار",
    "Sports":      "رياضة",
    "Movies":      "أفلام",
    "Kids":        "أطفال",
    "Music":       "موسيقى",
    "Religious":   "إسلامية",
    "Documentary": "وثائقية",
    "Series":      "مسلسلات",
    "Comedy":      "كوميديا",
    "Education":   "تعليمية",
    "Business":    "اقتصاد",
    "Lifestyle":   "حياة",
    "Family":      "عائلية",
    "Entertainment":"ترفيه",
    "General":     "عام",
    "Culture":     "ثقافة",
    "Cooking":     "طبخ",
}

ICON_MAP = {
    "أخبار":    "ph-newspaper",
    "رياضة":    "ph-soccer-ball",
    "أفلام":    "ph-film-strip",
    "أطفال":    "ph-baby",
    "موسيقى":   "ph-music-notes",
    "إسلامية":  "ph-mosque",
    "وثائقية":  "ph-film-slate",
    "مسلسلات":  "ph-mask-happy",
    "كوميديا":  "ph-smiley",
    "تعليمية":  "ph-graduation-cap",
    "اقتصاد":   "ph-chart-line-up",
    "ترفيه":    "ph-popcorn",
    "عام":      "ph-television",
    "ثقافة":    "ph-books",
    "طبخ":      "ph-cooking-pot",
    "عائلية":   "ph-house",
    "حياة":     "ph-sparkle",
}

COUNTRY_MAP = {
    ".dz":  "جزائرية",
    "dz@":  "جزائرية",
    ".tn":  "تونسية",
    "tn@":  "تونسية",
    ".ma":  "مغربية",
    "ma@":  "مغربية",
}

SKIP_KEYWORDS = [
    "http-user-agent", "http-referrer", "EXTVLCOPT",
    "#", "://", "null", "undefined"
]

def map_country(tvg_id, group):
    tvg_lower = tvg_id.lower()
    for key, cat in COUNTRY_MAP.items():
        if key in tvg_lower:
            return cat
    return None

def map_cat(group_title, tvg_id):
    country = map_country(tvg_id, group_title)
    if country:
        return country
    # split on semicolons, take first part
    first = group_title.split(";")[0].strip()
    return CAT_MAP.get(first, "ترفيه")

def get_icon(cat):
    return ICON_MAP.get(cat, "ph-television")

def clean_name(raw):
    # Remove resolution tag like (1080p), (720p), etc. and [Not 24/7], [Geo-blocked]
    name = re.sub(r'\s*\(\d+[pi]\)\s*', '', raw)
    name = re.sub(r'\s*\[.*?\]\s*', '', name)
    return name.strip()

print("⬇  Downloading iptv-org Arabic playlist…")
try:
    req = urllib.request.Request(
        M3U_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; iptv-bot/1.0)"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read().decode("utf-8", errors="ignore")
    print(f"   Downloaded {len(raw):,} bytes")
except Exception as e:
    print(f"❌ Download failed: {e}")
    exit(1)

lines = raw.splitlines()
channels = []
info = {}

i = 0
while i < len(lines):
    line = lines[i].strip()

    if line.startswith("#EXTINF"):
        # Parse attributes
        tvg_id    = re.search(r'tvg-id="([^"]*)"', line)
        tvg_logo  = re.search(r'tvg-logo="([^"]*)"', line)
        group     = re.search(r'group-title="([^"]*)"', line)
        # Name is after the last comma
        name_raw  = line.split(",", 1)[-1].strip() if "," in line else ""

        info = {
            "tvg_id":  tvg_id.group(1)  if tvg_id  else "",
            "logo":    tvg_logo.group(1) if tvg_logo else "",
            "group":   group.group(1)    if group    else "General",
            "name":    name_raw
        }
        i += 1
        continue

    # Skip EXTVLCOPT lines
    if line.startswith("#EXTVLCOPT") or line.startswith("#EXTM3U"):
        i += 1
        continue

    # URL line
    if (line.startswith("http://") or line.startswith("https://")) and info:
        url = line.strip()

        # Skip m3u8-incompatible formats
        if url.endswith(".mpd") or url.endswith(".ts") or url.endswith(".mp4"):
            info = {}
            i += 1
            continue

        name = clean_name(info["name"]) or "قناة"
        cat  = map_cat(info["group"], info["tvg_id"])
        icon = get_icon(cat)

        channels.append({
            "name": name,
            "cat":  cat,
            "icon": icon,
            "url":  url
        })
        info = {}

    i += 1

print(f"✅ Parsed {len(channels)} channels")

# Remove duplicate URLs
seen = set()
unique = []
for ch in channels:
    if ch["url"] not in seen:
        seen.add(ch["url"])
        unique.append(ch)

print(f"✅ {len(unique)} unique channels after dedup")

# Sort: sports/news first, then by category, then by name
CAT_ORDER = {"رياضة":1,"أخبار":2,"جزائرية":3,"تونسية":4,"مغربية":5}
unique.sort(key=lambda c: (CAT_ORDER.get(c["cat"], 99), c["name"]))

# Write JS file
js = "// SEFIANE VIP TV — auto-generated from iptv-org\n"
js += "// Generated: " + __import__("datetime").datetime.utcnow().strftime("%Y-%m-%d") + "\n"
js += f"// Total: {len(unique)} channels\n\n"
js += "const parsedChannels = " + json.dumps(unique, ensure_ascii=False, indent=2) + ";\n"

os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(js)

print(f"✅ Saved to {OUT_FILE}")
print(f"\n🎉 Done! {len(unique)} channels ready.")
