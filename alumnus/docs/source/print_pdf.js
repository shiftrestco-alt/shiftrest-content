// Prints playbook.html to the PDF with page numbers. Run from this folder: node print_pdf.js
const path = require('path');
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
  const page = await browser.newPage();
  await page.goto('file://' + path.join(__dirname, 'playbook.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const out = path.join(__dirname, '..', 'Alumnus-Website-Playbook-and-Higgsfield-Prompts.pdf');
  await page.pdf({
    path: out,
    format: 'Letter',
    printBackground: true,
    preferCSSPageSize: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `<div style="width:100%;font-family:Helvetica,Arial,sans-serif;font-size:7.5px;color:#8a8b96;padding:0 0.62in;display:flex;justify-content:space-between;">
      <span>alumnus. · Website playbook &amp; Higgsfield prompt pack</span><span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>`,
  });
  console.log('wrote', out);
  await browser.close();
})();
