import re
import os
import json

OUT_FILE = os.path.join(os.path.dirname(__file__), "js", "channels_data.js")

reliable_channels = [
  { "name": "MBC 1",             "cat": "ترفيه", "icon": "ph-sparkle",     "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-1/15cf99af5de54063fdabfefe66adc075/index.m3u8" },
  { "name": "MBC Drama",         "cat": "ترفيه", "icon": "ph-mask-happy",  "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-drama/2c28a458e2f3253e678b07ac7d13fe71/index.m3u8" },
  { "name": "MBC Masr",          "cat": "ترفيه", "icon": "ph-pyramid",     "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-masr/956eac069c78a35d47245db6cdbb1575/index.m3u8" },
  { "name": "MBC Masr 2",        "cat": "ترفيه", "icon": "ph-pyramid",     "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-masr-2/754931856515075b0aabf0e583495c68/index.m3u8" },
  { "name": "MBC 4",             "cat": "ترفيه", "icon": "ph-sparkle",     "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-4/24f134f1cd63db9346439e96b86ca6ed/index.m3u8" },
  { "name": "MBC 5",             "cat": "ترفيه", "icon": "ph-sparkle",     "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-5/ee6b000cee0629411b666ab26cb13e9b/index.m3u8" },
  { "name": "MBC Bollywood",     "cat": "أفلام", "icon": "ph-film-strip",  "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-bollywood/546eb40d7dcf9a209255dd2496903764/index.m3u8" },
  { "name": "MBC Iraq",          "cat": "ترفيه", "icon": "ph-television",  "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-iraq/e38c44b1b43474e1c39cb5b90203691e/index.m3u8" },
  { "name": "MBC 3 Kids",        "cat": "أطفال", "icon": "ph-baby",        "url": "https://shd-gcp-live.edgenextcdn.net/live/bitmovin-mbc-3-usa/5d58265a862a476dc7f97694addb5ded/index.m3u8" },
  { "name": "Rotana Khalijia",   "cat": "موسيقى","icon": "ph-music-notes", "url": "https://shd-amg-fast.edgenextcdn.net/tx029/playlist.m3u8" },
  { "name": "Aflam أفلام",       "cat": "أفلام", "icon": "ph-film-slate",  "url": "https://shd-amg-fast.edgenextcdn.net/tx001/playlist.m3u8" },
  { "name": "Maraya مرايا",      "cat": "مسلسلات", "icon": "ph-film-strip",  "url": "https://shd-amg-fast.edgenextcdn.net/tx008/playlist.m3u8" },
  { "name": "Bab Al Hara",       "cat": "مسلسلات","icon":"ph-house",       "url": "https://shd-amg-fast.edgenextcdn.net/tx010/playlist.m3u8" },
  { "name": "CBC مصر",           "cat": "ترفيه", "icon": "ph-television",  "url": "https://flu.systemnet.tv/CBC/index.m3u8" },
  { "name": "CBC Drama مصر",     "cat": "مسلسلات","icon": "ph-mask-happy", "url": "https://flu.systemnet.tv/CBCDrama/index.m3u8" },
  { "name": "CBC Sofra",         "cat": "طبخ",   "icon": "ph-cooking-pot", "url": "https://flu.systemnet.tv/CBCSofra/index.m3u8" },
  { "name": "Echourouk TV",      "cat": "جزائرية", "icon": "ph-sun",       "url": "https://cdn.jwplayer.com/live/streams/GQi1n5cj.m3u8" },
  { "name": "Ennahar TV",        "cat": "جزائرية", "icon": "ph-sun-horizon","url": "https://streaming.ennaharonline.com/hls/live/2016166/ennahar-hd1/index.m3u8" },
  { "name": "El Heddaf",         "cat": "جزائرية", "icon": "ph-soccer-ball","url": "https://live.elheddaftv.com:8081/elheddaf/index.mpd" },
  { "name": "Nessma DZ",         "cat": "جزائرية", "icon": "ph-flower",    "url": "https://cdn.jwplayer.com/live/streams/Nessma_DZ.m3u8" }
]

with open(OUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# We will just insert these as raw JS at the top of the array
insert_str = ""
for c in reliable_channels:
    insert_str += f'  {json.dumps(c, ensure_ascii=False)},\n'

text = text.replace("const parsedChannels = [", f"const parsedChannels = [\n{insert_str}")

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("Injected reliable channels at the top!")
