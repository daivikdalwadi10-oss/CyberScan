import axios from 'axios';
const urls = [
    'https://google.com',
    'https://github.com',
    'https://cloudflare.com'
];
let results = [];
let failures = 0;
let total = 0;
async function checkUptime() {
    const now = Date.now();
    for (const url of urls) {
        try {
            const start = Date.now();
            await axios.get(url, { timeout: 5000 });
            const responseTime = Date.now() - start;
            results.push({ url, responseTime, success: true, timestamp: now });
        }
        catch {
            failures++;
            results.push({ url, responseTime: null, success: false, timestamp: now });
        }
        total++;
    }
    if (results.length > 100)
        results = results.slice(-100);
}
setInterval(checkUptime, 30000);
checkUptime();
export function getUptime() {
    const avail = total ? ((total - failures) / total) * 100 : 100;
    return { results, availability: avail, timestamp: Date.now() };
}
