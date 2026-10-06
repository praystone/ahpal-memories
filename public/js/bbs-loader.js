(function() {
  var box = document.getElementById("bbs-posts");
  if (!box) return;
  var tid = parseInt(box.dataset.tid, 10);
  var fid = parseInt(box.dataset.fid, 10);
  if (!tid || !fid) return;

  var base   = "/data/";                       // A 站：無 /bbs2/ 前綴
  var fidStr = String(fid).padStart(2, "0");

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function(c) {
      return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c];
    });
  }
  function safeBody(s) { return esc(s || "").replace(/\n/g, "<br>"); }
  function render(posts) {
    if (!posts.length) { box.innerHTML = '<p class="bbs-empty">此主題無帖子</p>'; return; }
    posts.sort(function(a,b){ return a.pid - b.pid; });
    box.innerHTML = posts.map(function(p){
      var d  = new Date(p.dateline * 1000);
      var ds = d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");
      var au = p.author ? esc(p.author) : "匿名";
      var su = p.subject ? esc(p.subject) : "";
      return '<div class="bbs-post">'
           + (su ? '<div class="bbs-post-subject">'+su+'</div>' : '')
           + '<div class="bbs-post-meta">'+au+' · '+ds+' · #'+p.pid+'</div>'
           + '<div class="bbs-post-body">'+safeBody(p.message)+'</div>'
           + '</div>';
    }).join("");
  }

  // 先試索引，不存在則退回單檔（給未拆分版塊）
  fetch(base + "posts-fid" + fidStr + "-index.json")
    .then(function(r){ if(!r.ok) throw 0; return r.json(); })
    .then(function(idx){
      var pages = idx[String(tid)];
      if (!pages || !pages.length) {
        box.innerHTML = '<p class="bbs-empty">找不到此主題</p>';
        return;
      }
      return Promise.all(pages.map(function(pg){
        var url = base + "posts-fid" + fidStr + "-p" + String(pg).padStart(2,"0") + ".json";
        return fetch(url).then(function(r){ return r.json(); });
      })).then(function(arrays){
        var all = [];
        arrays.forEach(function(a){ all = all.concat(a); });
        render(all.filter(function(p){ return p.tid === tid; }));
      });
    })
    .catch(function(){
      fetch(base + "posts-fid" + fidStr + ".json")
        .then(function(r){ return r.json(); })
        .then(function(all){ render(all.filter(function(p){ return p.tid === tid; })); })
        .catch(function(e){ box.innerHTML = '<p class="bbs-error">載入失敗：'+esc(e)+'</p>'; });
    });
})();
