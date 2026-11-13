/* Recorrido público real de duración de pauta; demo ficticia, sin llamadas IA. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH);
const fs=require('node:fs');const path=require('node:path');const assert=require('node:assert/strict');
const APP_URL='https://pulso-comercial-ia-njsqy6x3ka-tl.a.run.app/';
const root=path.resolve(__dirname,'..');const tmp=path.join(root,'.venv','video-f7-temp');fs.mkdirSync(tmp,{recursive:true});
const target=path.join(root,'evidencias','32_recorrido_publico_duracion_pauta_sin_ia.webm');
(async()=>{const browser=await chromium.launch({headless:true});let context,page,videoPath;const started=Date.now();
 try{
  context=await browser.newContext({viewport:{width:1440,height:900},recordVideo:{dir:tmp,size:{width:1440,height:900}}});
  await context.route('**/api/analisis',route=>route.abort());page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const hold=async(ms)=>page.waitForTimeout(ms);
  const show=async(selector,ms)=>{await page.locator(selector).scrollIntoViewIfNeeded();await hold(ms);};
  await page.goto(APP_URL,{waitUntil:'domcontentloaded',timeout:30000});assert.equal(new URL(page.url()).origin,new URL(APP_URL).origin);
  await hold(12000);
  await page.getByRole('button',{name:'Probar con datos de demostración'}).click();
  await page.locator('#dashboard').waitFor({state:'visible',timeout:30000});
  await page.waitForFunction(()=>document.getElementById('period-label').textContent.includes('360 registros'));
  await show('#period-label',13000);
  await show('#kpis',20000);
  await show('#chart',20000);
  await show('#ranking-table',19000);
  await show('#volumes',16000);
  await show('#ai-btn',13000);
  await page.locator('#facts').scrollIntoViewIfNeeded();await hold(9000);
  await page.locator('#linea').scrollIntoViewIfNeeded();await page.locator('#linea').selectOption({index:1});
  await page.getByRole('button',{name:'Aplicar filtros'}).click();
  await page.waitForFunction(()=>document.getElementById('period-label').textContent.includes('180 registros'));
  await show('#kpis',12000);
  await show('#ranking-table',10000);
  await show('#ai-btn',9000);
  assert.deepEqual(errors,[]);videoPath=await page.video().path();
  await context.close();context=null;
 }finally{if(context)await context.close();await browser.close();}
 fs.copyFileSync(videoPath,target);
 console.log(JSON.stringify({video:target,bytes:fs.statSync(target).size,elapsed_wall_seconds:Math.round((Date.now()-started)/1000),url:APP_URL,ia_invocada:false,demo_ficticia:true}));
})().catch(e=>{console.error(e);process.exitCode=1;});
