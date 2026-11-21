const assert = require('node:assert/strict');
const fs = require('node:fs');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');

const phase = process.env.AUDIT_PHASE || 'after';
const base = process.env.SITE_BASE || 'http://127.0.0.1:4179';
const slug = 'post-build-technical-educator';
const articleUrl = `${base}/blog/${slug}/`;
const raw = 'seo-audit/2026-11-21/raw';
const expected = fs.readFileSync(`prompt-sources/${slug}.md`, 'utf8').trimEnd();

async function verify() {
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  try {
    const context = await browser.newContext({
      viewport: { width: 1440, height: 1000 },
      permissions: ['clipboard-read', 'clipboard-write'],
    });
    const page = await context.newPage();
    await page.goto(articleUrl, { waitUntil: 'domcontentloaded' });
    const hero = page.locator('.article-visual img');
    await hero.evaluate(image => image.decode());
    assert.equal((await page.locator('code.language-markdown').textContent()).trimEnd(), expected);
    await page.locator('.code-block-toolbar button').click();
    assert.equal((await page.evaluate(() => navigator.clipboard.readText())).trimEnd(), expected);
    await page.evaluate(() => scrollTo(0, 0));
    await page.screenshot({ path: `${raw}/post-${phase}-desktop.png` });

    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(articleUrl, { waitUntil: 'domcontentloaded' });
    await hero.evaluate(image => image.decode());
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth > innerWidth), false);
    await page.screenshot({ path: `${raw}/post-${phase}-mobile.png` });

    const noJs = await browser.newContext({ javaScriptEnabled: false });
    const listing = await noJs.newPage();
    for (const path of ['/', '/blog/', '/coding/']) {
      await listing.goto(base + path);
      assert(await listing.locator(`main a[href*="${slug}"]`).count(), `Missing static discovery at ${path}`);
    }

    const receipt = { result: 'PASS', base, verbatim: true, clipboard: true, heroDecoded: true,
      mobileOverflow: false, noJsListings: ['/', '/blog/', '/coding/'] };
    fs.writeFileSync(`${raw}/browser-${phase}.json`, JSON.stringify(receipt, null, 2) + '\n');
  } finally {
    await browser.close();
  }
}

verify().catch(error => { console.error(error); process.exitCode = 1; });
