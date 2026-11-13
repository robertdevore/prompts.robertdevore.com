const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs');
(async()=>{
const browser=await chromium.launch({headless:true,channel:'chrome'});
const context=await browser.newContext({viewport:{width:1440,height:1000},permissions:['clipboard-read','clipboard-write']});
const page=await context.newPage();
const base=process.env.SITE_BASE||'http://127.0.0.1:4179';
const slug='ogilvy-mather-universal-strategic-review';
const expected=fs.readFileSync(`prompt-sources/${slug}.md`,'utf8').trimEnd();
await page.goto(`${base}/blog/${slug}/`,{waitUntil:'domcontentloaded'});
await page.locator('.article-visual img').evaluate(i=>i.decode());
if((await page.locator('code.language-markdown').textContent()).trimEnd()!==expected)throw Error('Prompt mismatch');
await page.locator('.code-block-toolbar button').click();
if((await page.evaluate(()=>navigator.clipboard.readText())).trimEnd()!==expected)throw Error('Clipboard mismatch');
await page.evaluate(()=>scrollTo(0,0));
await page.screenshot({path:'seo-audit/2026-11-12/raw/post-desktop.png'});
await page.setViewportSize({width:390,height:844});
await page.goto(`${base}/blog/${slug}/`,{waitUntil:'domcontentloaded'});
if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Mobile overflow');
await page.screenshot({path:'seo-audit/2026-11-12/raw/post-mobile.png'});
const nojs=await browser.newContext({javaScriptEnabled:false});
const staticPage=await nojs.newPage();
for(const category of ['marketing','business']){
await staticPage.goto(`${base}/${category}/`);
if(!await staticPage.locator(`a[href*="${slug}"]`).count())throw Error('Missing static category discovery');
}
fs.writeFileSync('seo-audit/2026-11-12/raw/browser-verification.json',JSON.stringify({result:'PASS',base,verbatim:true,clipboard:true,heroDecoded:true,mobileOverflow:false,noJsCategories:true},null,2)+'\n');
await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
