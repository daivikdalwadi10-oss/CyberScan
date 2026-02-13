import axios from 'axios';

let cache: any = null;
let lastFetch = 0;
const CACHE_DURATION = 60 * 60 * 1000; // 1 hour

async function fetchThreats() {
  if (Date.now() - lastFetch < CACHE_DURATION && cache) return cache;
  const resp = await axios.get('https://services.nvd.nist.gov/rest/json/cves/2.0?resultsPerPage=10');
  cache = (resp.data.vulnerabilities || []).map((v: any) => ({
    id: v.cve.id,
    published: v.cve.published,
    severity: v.cve.metrics?.cvssMetricV31?.[0]?.cvssData?.baseSeverity || 'UNKNOWN',
    description: v.cve.descriptions?.[0]?.value || ''
  }));
  lastFetch = Date.now();
  return cache;
}

export async function getThreats() {
  return await fetchThreats();
}
