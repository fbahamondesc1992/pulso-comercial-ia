/* Captura real del navegador público con demo ficticia; nunca llama a la IA. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE_PATH);
const fs=require('node:fs');
const path=require('node:path');
const assert=require('node:assert/strict');
const APP_URL='https://pulso-comercial-ia-njsqy6x3ka-tl.a.run.app/';
const root=path.resolve(__dirname,'..');
const dir=path.join(root,'evidencias');
const temp=path.join(root,'.venv','video-f7-temp');
fs.mkdirSync(temp,{recursive:true});
(async()=>{
 const browser=await chromium.launch({headless:true});
 const observed=[];let videoPath;
 try{
  for(const width of [1440,375]){
   const context=await browser.newContext({viewport:{width,height:900},recordVideo:width===1440?{dir:temp,size:{width:1440,height:900}}:undefined});
   await context.route('**/api/analisis',route=>route.abort());
   const page=await context.newPage();
   const errors=[];page.on('pageerror',err=>errors.push(err.message));
   await page.goto(APP_URL,{waitUntil:'domcontentloaded',timeout:30000});
   assert.equal(new URL(page.url()).origin,new URL(APP_URL).origin);
   if(width===1440)await page.waitForTimeout(1000);
   await page.getByRole('button',{name:'Probar con datos de demostración'}).click();
   await page.locator('#dashboard').waitFor({state:'visible',timeout:30000});
   await page.waitForFunction(()=>document.getElementById('period-label').textContent.includes('360 registros'));
   await page.waitForTimeout(width===1440?1800:300);
   const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);
   assert.equal(overflow,false,`desborde ${width}`);
   assert.equal(await page.locator('#kpis article').count(),5);
   assert.equal(await page.locator('#volumes .volume-card').count(),2);
   assert.deepEqual(errors,[]);
   const screenshot=`31_app_publica_demo_${width}.png`;
   await page.screenshot({path:path.join(dir,screenshot),fullPage:true});
   observed.push({width,url:page.url(),demo_rows:360,kpi_cards:5,volume_cards:2,overflow,js_errors:errors,screenshot});
   if(width===1440){
    await page.locator('#kpis').scrollIntoViewIfNeeded();
    await page.waitForTimeout(2200);
    await page.locator('#ranking-table').scrollIntoViewIfNeeded();
    await page.waitForTimeout(2200);
    await page.locator('#ai-btn').scrollIntoViewIfNeeded();
    await page.waitForTimeout(1800);
    await page.locator('#linea').scrollIntoViewIfNeeded();
    await page.locator('#linea').selectOption({index:1});
    await page.getByRole('button',{name:'Aplicar filtros'}).click();
    await page.locator('#dashboard').waitFor({state:'visible'});
    await page.locator('#kpis').scrollIntoViewIfNeeded();
    await page.waitForTimeout(1800);
    videoPath=await page.video().path();
   }
   await context.close();
  }
 }finally{await browser.close();}
 const output=path.join(dir,'31_app_publica_demo_sin_ia.webm');
 fs.copyFileSync(videoPath,output);
 fs.writeFileSync(path.join(dir,'31_capturas_video.json'),JSON.stringify({fecha_utc:new Date().toISOString(),modo:'NAVEGADOR_PUBLICO_REAL_DEMO_FICTICIA',video:output.split('/').pop(),analisis_ia:'NO EJECUTADO',resultados:observed},null,2)+'\n');
 console.log(JSON.stringify({resultados:observed,video:output,video_bytes:fs.statSync(output).size}));
})().catch(err=>{console.error(err);process.exitCode=1;});
