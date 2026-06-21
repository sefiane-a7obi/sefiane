import re
import os

OUT_FILE = os.path.join(os.path.dirname(__file__), "js", "channels_data.js")

with open(OUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Bad channels
bad_words = ["Echourouk", "Ennahar", "El Heddaf", "Alkass", "Nessma DZ"]

# The file looks like:
#  {
#    "name": "Alkass One",
#    ...
#  },
# We can use regex to remove objects where the name contains one of the bad words.
for bw in bad_words:
    # Match an object like: { ... "name": "...bw...", ... },
    pattern = r'\{\s*"name":\s*"[^"]*' + bw + r'[^"]*".*?\},?'
    text = re.sub(pattern, '', text, flags=re.DOTALL | re.IGNORECASE)

# Cleanup any empty spaces or trailing commas before the array ends
text = re.sub(r',\s*\]', '\n]', text)

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("Removed bad channels via regex!")
