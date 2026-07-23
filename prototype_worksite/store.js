// SHine-K 무가입 로컬 영구 저장 (IndexedDB) — 가입·클라우드 불필요
// 현장(좌표·바이탈)·관제(수신 전부)에서 브라우저 안에 영구 보관. 새로고침/종료 후에도 유지.
(function(){
  var dbp=null;
  function open(){
    if(dbp)return dbp;
    dbp=new Promise(function(res,rej){
      var r=indexedDB.open('shk-live',1);
      r.onupgradeneeded=function(){var db=r.result;if(!db.objectStoreNames.contains('events'))db.createObjectStore('events',{keyPath:'id',autoIncrement:true});};
      r.onsuccess=function(){res(r.result);};
      r.onerror=function(){rej(r.error);};
    });
    return dbp;
  }
  window.SHKStore={
    add:function(rec){return open().then(function(db){return new Promise(function(res){try{var tx=db.transaction('events','readwrite');tx.objectStore('events').add(rec);tx.oncomplete=function(){res(true);};tx.onerror=function(){res(false);};}catch(e){res(false);}});}).catch(function(){return false;});},
    count:function(){return open().then(function(db){return new Promise(function(res){try{var tx=db.transaction('events','readonly');var rq=tx.objectStore('events').count();rq.onsuccess=function(){res(rq.result);};rq.onerror=function(){res(0);};}catch(e){res(0);}});}).catch(function(){return 0;});},
    all:function(){return open().then(function(db){return new Promise(function(res){try{var tx=db.transaction('events','readonly');var rq=tx.objectStore('events').getAll();rq.onsuccess=function(){res(rq.result||[]);};rq.onerror=function(){res([]);};}catch(e){res([]);}});}).catch(function(){return [];});},
    clear:function(){return open().then(function(db){return new Promise(function(res){try{var tx=db.transaction('events','readwrite');tx.objectStore('events').clear();tx.oncomplete=function(){res(true);};tx.onerror=function(){res(false);};}catch(e){res(false);}});}).catch(function(){return false;});}
  };
})();
