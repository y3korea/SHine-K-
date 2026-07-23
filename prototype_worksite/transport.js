// SHine-K 공용 전송 모듈 — 한 코드, 3가지 연결
//   (없음)        → 같은 PC 창 2개 (BroadcastChannel, 무료·자동)
//   ?ws=IP:8787   → 같은 와이파이 로컬 서버 (server.js, 완전 오프라인)
//   ?room=코드     → 무료 공개 MQTT 브로커 (설치/계정 0, 인터넷만 되면 어디서나)
// 영상은 보내지 않습니다 — 골격 좌표·이벤트만.
(function(){
  function qp(k){return new URLSearchParams(location.search).get(k);}
  window.SHKBus=function(opts){
    opts=opts||{};
    var onMsg=opts.onMessage||function(){};
    var onConn=opts.onConn||function(){};
    var ws=qp('ws'), room=qp('room');

    if(room){
      if(typeof mqtt==='undefined'){onConn(false,'MQTT 라이브러리 미로드');return {send:function(){},mode:'mqtt'};}
      var topic='shk-safety/'+room;
      var client=mqtt.connect('wss://broker.emqx.io:8084/mqtt',{reconnectPeriod:2500,connectTimeout:8000});
      client.on('connect',function(){client.subscribe(topic);onConn(true,'인터넷 룸 · '+room);});
      client.on('message',function(t,p){try{onMsg(JSON.parse(p.toString()));}catch(e){}});
      client.on('reconnect',function(){onConn(false,'재연결 중…');});
      client.on('error',function(){onConn(false,'브로커 오류');});
      client.on('offline',function(){onConn(false,'오프라인');});
      return {send:function(o){try{client.publish(topic,JSON.stringify(o));}catch(e){}},mode:'mqtt'};
    }

    if(ws){
      var sock=new WebSocket('ws://'+ws), open=false;
      sock.onopen=function(){open=true;onConn(true,'로컬 서버 · '+ws);};
      sock.onclose=function(){open=false;onConn(false,'연결 끊김');};
      sock.onerror=function(){onConn(false,'서버 오류');};
      sock.onmessage=function(e){try{onMsg(JSON.parse(e.data));}catch(err){}};
      return {send:function(o){if(open)sock.send(JSON.stringify(o));},mode:'ws'};
    }

    var bc=new BroadcastChannel('shk-safety');
    bc.onmessage=function(e){onMsg(e.data);};
    onConn(true,'같은 PC · 자동');
    return {send:function(o){bc.postMessage(o);},mode:'local'};
  };
})();
