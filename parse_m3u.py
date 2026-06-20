import json

def parse_m3u(file_path):
    channels = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    current_channel = {}
    for line in lines:
        line = line.strip()
        if line.startswith('# EXTINF:'):
            # Parse EXTINF line
            # Example: # EXTINF:-1 tvg-id="AL24News.dz@SD" tvg-logo="..." group-title="News",AL24 News
            
            # Extract name
            if ',' in line:
                current_channel['name'] = line.split(',')[-1].strip()
            
            # Extract category (group-title)
            if 'group-title="' in line:
                cat = line.split('group-title="')[1].split('"')[0]
                # Map categories to Arabic
                if 'News' in cat: current_channel['cat'] = 'أخبار'
                elif 'Sports' in cat: current_channel['cat'] = 'رياضة'
                elif 'Music' in cat: current_channel['cat'] = 'موسيقى'
                elif 'Movies' in cat: current_channel['cat'] = 'أفلام'
                elif 'Kids' in cat: current_channel['cat'] = 'أطفال'
                elif 'Religious' in cat: current_channel['cat'] = 'إسلامية'
                else: current_channel['cat'] = 'ترفيه'
            else:
                current_channel['cat'] = 'ترفيه'
                
            # Assign a generic icon based on category
            if current_channel['cat'] == 'أخبار': current_channel['icon'] = 'ph-newspaper'
            elif current_channel['cat'] == 'رياضة': current_channel['icon'] = 'ph-soccer-ball'
            elif current_channel['cat'] == 'موسيقى': current_channel['icon'] = 'ph-music-notes'
            elif current_channel['cat'] == 'أفلام': current_channel['icon'] = 'ph-film-strip'
            elif current_channel['cat'] == 'أطفال': current_channel['icon'] = 'ph-baby'
            elif current_channel['cat'] == 'إسلامية': current_channel['icon'] = 'ph-mosque'
            else: current_channel['icon'] = 'ph-television'
            
        elif line.startswith('http'):
            if 'name' in current_channel:
                current_channel['url'] = line
                # Try to guess country from name or tvg-id if we had parsed it
                name_lower = current_channel['name'].lower()
                if 'dz' in line or 'algeria' in name_lower or 'ennahar' in name_lower or 'echourouk' in name_lower or 'elheddaf' in name_lower:
                    current_channel['cat'] = 'جزائرية'
                    current_channel['icon'] = 'ph-flag'
                elif 'ma' in line or 'maroc' in name_lower or '2m' in name_lower or 'arryadia' in name_lower:
                    current_channel['cat'] = 'مغربية'
                    current_channel['icon'] = 'ph-flag'
                elif 'tn' in line or 'tunis' in name_lower or 'hannibal' in name_lower or 'nessma' in name_lower:
                    current_channel['cat'] = 'تونسية'
                    current_channel['icon'] = 'ph-flag'
                
                channels.append(current_channel)
                current_channel = {}
                
    return channels

if __name__ == '__main__':
    # Path to the downloaded ara.m3u
    m3u_path = r'C:\Users\smart\.gemini\antigravity\brain\00bbe9e8-acfa-49aa-afd8-df6f8a720f07\.system_generated\steps\57\content.md'
    
    try:
        channels = parse_m3u(m3u_path)
        
        # Output as a JS variable
        js_content = "const parsedChannels = " + json.dumps(channels, ensure_ascii=False, indent=2) + ";"
        
        with open('js/channels_data.js', 'w', encoding='utf-8') as f:
            f.write(js_content)
            
        print(f"Successfully extracted {len(channels)} channels to js/channels_data.js")
    except Exception as e:
        print(f"Error: {e}")
