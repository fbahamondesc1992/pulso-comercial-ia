/* Prueba local real de navegador; requiere Playwright y Chromium disponibles. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH||'playwright');
(async()=>{
  const browser=await chromium.launch({headless:true});
  const url=process.env.PULSO_URL||'http://127.0.0.1:8080';
  const prefix=process.env.PULSO_EVIDENCE_PREFIX||'02';
  assert.match(prefix,/^\d{2}$/);
  assert.ok(['127.0.0.1','localhost'].includes(new URL(url).hostname),'Esta prueba solo admite servidor local');
  const results=[];
  try {
    for(const width of [1440,375]){
      const context=await browser.newContext({viewport:{width,height:1000}});
      const page=await context.newPage();
      const errors=[];page.on('pageerror',e=>errors.push(e.message));
      await page.goto(url);
      await page.keyboard.press('Tab');
      assert.equal(await page.evaluate(()=>document.activeElement.textContent),'Ir al contenido');
      await page.getByRole('button',{name:'Probar con datos de demostración'}).click();
      await page.locator('#dashboard').waitFor({state:'visible'});
      await page.waitForFunction(()=>!document.getElementById('ai-btn').disabled);
      const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
      assert.equal(overflow,false,`Desborde a ${width}px`);
      assert.equal(await page.locator('#kpis article').count(),5);
      assert.equal(await page.locator('#volumes .volume-card').count(),2);
      await page.screenshot({path:`evidencias/${prefix}_demo_local_${width}.png`,fullPage:true});
      await page.locator('#ai-btn').click();
      await page.locator('.fallback').waitFor({state:'visible'});
      assert.match(await page.locator('.fallback').innerText(),/Resumen automático sin IA/);
      await page.locator('#canal').selectOption('Tradicional');
      assert.equal(await page.locator('#ai-btn').isDisabled(),true);
      assert.equal(await page.locator('.fallback').count(),0);
      await page.getByRole('button',{name:'Aplicar filtros'}).click();
      await page.waitForFunction(()=>document.getElementById('period-label').textContent.includes('120 registros'));
      assert.equal(await page.locator('#ai-btn').isDisabled(),false);
      const filtered=await page.locator('#kpis').innerText();
      await page.locator('#csv-input').setInputFiles({name:'invalido.csv',mimeType:'text/csv',buffer:Buffer.from('a,b\n1,2')});
      await page.waitForFunction(()=>document.getElementById('status').classList.contains('error'));
      assert.match(await page.locator('#status').innerText(),/columnas/);
      assert.equal(await page.locator('#dashboard').isVisible(),false,'Un CSV nuevo inválido no debe conservar resultados de otro archivo');
      assert.equal(errors.length,0,errors.join(';'));
      results.push({width,overflow,keyboard_skip_link:true,fallback_identificado:true,filtros_consistentes:true,csv_invalido_controlado:true,errores_js:errors,filtered});
      await context.close();
    }
    fs.writeFileSync(`evidencias/${prefix}_revision_navegador.json`,JSON.stringify({fecha:new Date().toISOString(),url,modo:'LOCAL_SIN_IA_REAL',resultados:results},null,2));
    console.log(JSON.stringify(results));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
