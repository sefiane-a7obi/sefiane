const fs = require('fs');

const path = './js/channels_data.js';
let content = fs.readFileSync(path, 'utf8');

// Use regex to remove lines containing certain bad channels
const badWords = ['Echourouk', 'Ennahar', 'El Heddaf', 'Alkass', 'Nessma DZ'];

// Since each channel is formatted as `{ "name": "...", ... },` we can't just delete lines easily if they span multiple lines.
// However, the json was written using `json.dumps(..., indent=2)`. Let's just evaluate it as JS.
try {
    // strip the 'const parsedChannels = ' part
    let jsonStr = content.substring(content.indexOf('['), content.lastIndexOf(']') + 1);
    
    // fix trailing comma if any
    jsonStr = jsonStr.replace(/,\s*\]$/, ']');

    let channels = JSON.parse(jsonStr);
    
    let filtered = channels.filter(c => {
        let isBad = false;
        badWords.forEach(bw => {
            if (c.name.toLowerCase().includes(bw.toLowerCase())) isBad = true;
        });
        return !isBad;
    });

    let newFile = `// SEFIANE VIP TV — Cleaned up broken channels
// Total: ${filtered.length} channels

const parsedChannels = ${JSON.stringify(filtered, null, 2)};
`;
    fs.writeFileSync(path, newFile, 'utf8');
    console.log("Successfully removed broken channels using Node!");
} catch (e) {
    console.error("Error:", e);
}
