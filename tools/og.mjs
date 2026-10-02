// Renders the 1200×630 share images (Open Graph) from tools/og-cards.html.
// Usage: node tools/og.mjs   (needs playwright-core and a Chromium; see HANDOVER.md)
import { chromium } from 'playwright-core';
import { fileURLToPath } from 'url';
import path from 'path';
const here = path.dirname(fileURLToPath(import.meta.url));
const b = await chromium.launch({ executablePath: process.env.CHROME_PATH, args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
for (const id of ['index', 'about', 'hospitality', 'fmcg', 'ajuni-luxe', 'contact']) {
  await p.goto('file://' + path.join(here, 'og-cards.html') + '#' + id);
  await p.reload();
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(here, '../src/assets/og', id + '.jpg'), type: 'jpeg', quality: 82 });
}
await b.close();
