// SHine-K 순수연산 벤치마크 (브라우저 모델 추론 제외, 후처리 연산만 실측)
function angle(a,b,c){const ab={x:a.x-b.x,y:a.y-b.y},cb={x:c.x-b.x,y:c.y-b.y};
  const dot=ab.x*cb.x+ab.y*cb.y;const m=Math.hypot(ab.x,ab.y)*Math.hypot(cb.x,cb.y)||1e-6;
  return Math.acos(Math.max(-1,Math.min(1,dot/m)))*180/Math.PI;}
function vTrunk(sh,hip){const dx=sh.x-hip.x,dy=sh.y-hip.y;return Math.abs(Math.atan2(dx,-dy)*180/Math.PI);}
// two-cue posture-strain index (trunk inclination + upper-arm elevation, binned 1-4; a REBA-inspired proxy, not a REBA score)
function postureIndex(lm){const shM={x:(lm[11].x+lm[12].x)/2,y:(lm[11].y+lm[12].y)/2};
  const hipM={x:(lm[23].x+lm[24].x)/2,y:(lm[23].y+lm[24].y)/2};
  const trunk=vTrunk(shM,hipM);const arm=180-angle(lm[23],lm[11],lm[13]);
  let r=1;if(trunk>20||arm>45)r=2;if(trunk>45||arm>90)r=3;if(trunk>60||arm>120)r=4;return [r,trunk,arm];}
// 화재감지: 80x60 RGBA 픽셀 분석
function fire(d,w,h){let flame=0,grayLow=0;const n=w*h;
  for(let i=0,p=0;i<d.length;i+=4,p++){const r=d[i],g=d[i+1],b=d[i+2];
    const mx=Math.max(r,g,b),mn=Math.min(r,g,b);
    if(r>180&&g>80&&g<200&&b<110&&r>=g&&g>=b&&(mx-mn)>40)flame++;
    const sat=mx===0?0:(mx-mn)/mx;if(sat<0.18&&((r+g+b)/3)>90&&((r+g+b)/3)<210)grayLow++;}
  return [flame/n*100,grayLow/n*100];}

// 데이터 준비
const lm=Array.from({length:33},()=>({x:Math.random(),y:Math.random()}));
const W=80,H=60;const img=new Uint8ClampedArray(W*H*4);
for(let i=0;i<img.length;i++)img[i]=Math.floor(Math.random()*256);

function timeit(fn,iters){const t0=process.hrtime.bigint();let s=0;
  for(let i=0;i<iters;i++){const r=fn();s+=(r&&r[0])||0;}
  const t1=process.hrtime.bigint();return {ms:Number(t1-t0)/1e6/iters, sink:s};}

// warmup
timeit(()=>postureIndex(lm),20000); timeit(()=>fire(img,W,H),5000);
const N=50000;
const rb=timeit(()=>postureIndex(lm),N);
const fr=timeit(()=>fire(img,W,H),20000);
const node=process.version;
const postureMs=rb.ms, fireMs=fr.ms;
console.log("Node "+node);
console.log("자세부하지수(2단서) 산출: "+postureMs.toFixed(4)+" ms/frame  → 이론상 "+Math.round(1000/postureMs).toLocaleString()+" fps 상한");
console.log("화재 픽셀분석(80x60):    "+fireMs.toFixed(4)+" ms/frame  → 이론상 "+Math.round(1000/fireMs).toLocaleString()+" fps 상한");
console.log("후처리 합계:             "+(postureMs+fireMs).toFixed(4)+" ms/frame");
