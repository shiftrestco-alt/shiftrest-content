const path = require('path');
const { check } = require('@shopify/theme-check-node');
(async () => {
  const root = process.argv[2];
  const offenses = await check(root);
  const sev = ['ERROR', 'WARN', 'INFO'];
  offenses.sort((a, b) => a.severity - b.severity || a.uri.localeCompare(b.uri));
  for (const o of offenses) {
    const file = o.uri.replace('file://' + root + '/', '');
    console.log(`${sev[o.severity] || o.severity}\t${o.check}\t${file}:${(o.start && o.start.line + 1) || ''}\t${o.message}`);
  }
  console.log(`\nTotal: ${offenses.length} (errors: ${offenses.filter(o => o.severity === 0).length}, warnings: ${offenses.filter(o => o.severity === 1).length})`);
})().catch(e => { console.error('FAILED', e); process.exit(1); });
