// SHine-K PPE 감지 플러그인 (YOLOv11 ONNX, onnxruntime-web)
// 사용: ppe.onnx 파일을 이 폴더에 두면 worksite가 자동 로드합니다.
//   best.pt → ppe.onnx 변환:  yolo export model=best.pt format=onnx imgsz=640
// 클래스 순서는 학습 dataset.yaml의 names 와 반드시 일치해야 합니다(아래 NAMES 수정).
window.SHKPPE = (function(){
  // 건설현장 PPE 데이터셋(css-data) 기본 순서 — dataset.yaml 과 다르면 수정하세요.
  var NAMES = ['Hardhat','Mask','NO-Hardhat','NO-Mask','NO-Safety Vest','Person','Safety Cone','Safety Vest','Machinery','Vehicle'];
  var sess=null, IN=640, NC=0;
  var cnv=document.createElement('canvas'); cnv.width=IN; cnv.height=IN;
  var cx=cnv.getContext('2d',{willReadFrequently:true});

  async function load(url){
    if(typeof ort==='undefined')return false;
    try{ sess=await ort.InferenceSession.create(url,{executionProviders:['wasm']}); return true; }
    catch(e){ sess=null; return false; }
  }
  function preprocess(video){
    cx.drawImage(video,0,0,IN,IN);
    var d=cx.getImageData(0,0,IN,IN).data, n=IN*IN, f=new Float32Array(n*3);
    for(var i=0;i<n;i++){ f[i]=d[i*4]/255; f[i+n]=d[i*4+1]/255; f[i+2*n]=d[i*4+2]/255; }
    return new ort.Tensor('float32',f,[1,3,IN,IN]);
  }
  function iou(a,b){
    var ax1=a[0]-a[2]/2,ay1=a[1]-a[3]/2,ax2=a[0]+a[2]/2,ay2=a[1]+a[3]/2;
    var bx1=b[0]-b[2]/2,by1=b[1]-b[3]/2,bx2=b[0]+b[2]/2,by2=b[1]+b[3]/2;
    var ix=Math.max(0,Math.min(ax2,bx2)-Math.max(ax1,bx1)), iy=Math.max(0,Math.min(ay2,by2)-Math.max(ay1,by1));
    var inter=ix*iy, u=a[2]*a[3]+b[2]*b[3]-inter; return u<=0?0:inter/u;
  }
  function nms(b,th){ b.sort(function(p,q){return q.score-p.score;}); var keep=[]; b.forEach(function(x){ if(keep.every(function(k){return iou(x.box,k.box)<th;}))keep.push(x); }); return keep; }

  async function detect(video,conf){
    if(!sess||!video||video.readyState<2)return [];
    conf=conf||0.4;
    var feeds={}; feeds[sess.inputNames[0]]=preprocess(video);
    var out=await sess.run(feeds), o=out[sess.outputNames[0]], dims=o.dims, data=o.data;
    // 기대 형태 [1, 4+nc, N] (YOLOv11). 다르면 빈 배열.
    if(dims.length!==3||dims[1]<5)return [];
    var nc=dims[1]-4, N=dims[2], res=[]; NC=nc;
    for(var i=0;i<N;i++){
      var best=0,bi=0;
      for(var c=0;c<nc;c++){ var s=data[(4+c)*N+i]; if(s>best){best=s;bi=c;} }
      if(best<conf)continue;
      res.push({cls:bi,name:NAMES[bi]||('c'+bi),score:best,box:[data[i],data[N+i],data[2*N+i],data[3*N+i]]});
    }
    return nms(res,0.45);
  }
  return { load:load, detect:detect, setNames:function(n){NAMES=n;}, get loaded(){return !!sess;}, get classes(){return NC;}, get nameCount(){return NAMES.length;} };
})();
