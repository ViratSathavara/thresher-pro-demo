(function(){
var d=document,$=function(s,r){return (r||d).querySelector(s)},$$=function(s,r){return Array.prototype.slice.call((r||d).querySelectorAll(s))};
d.documentElement.classList.add('js');

/* remember language choice */
$$('[data-lang]').forEach(function(a){a.addEventListener('click',function(){try{localStorage.setItem('lang',a.getAttribute('data-lang'))}catch(e){}})});

/* header */
var hdr=$('#hdr');
function onScroll(){if(hdr)hdr.classList.toggle('scrolled',window.scrollY>30)}
window.addEventListener('scroll',onScroll,{passive:true});onScroll();

/* drawer */
var dr=$('#drawer');
function drawer(o){if(!dr)return;dr.classList.toggle('open',o);dr.setAttribute('aria-hidden',!o);var b=$('#burger');if(b)b.setAttribute('aria-expanded',o);d.body.style.overflow=o?'hidden':''}
var bg=$('#burger'),cl=$('#close');
if(bg)bg.onclick=function(){drawer(true)};if(cl)cl.onclick=function(){drawer(false)};
if(dr)dr.addEventListener('click',function(e){if(e.target.closest('a'))drawer(false)});

/* dropdowns: click toggles (touch), Esc closes */
$$('.dd>button').forEach(function(b){b.addEventListener('click',function(e){var p=b.parentNode,o=!p.classList.contains('open');$$('.dd.open').forEach(function(x){x.classList.remove('open');$('button',x).setAttribute('aria-expanded','false')});if(o){p.classList.add('open');b.setAttribute('aria-expanded','true')}e.stopPropagation()})});
d.addEventListener('click',function(){$$('.dd.open').forEach(function(x){x.classList.remove('open');$('button',x).setAttribute('aria-expanded','false')})});
window.addEventListener('keydown',function(e){if(e.key==='Escape'){drawer(false);$$('.dd.open').forEach(function(x){x.classList.remove('open');$('button',x).setAttribute('aria-expanded','false')})}});

/* reveal */
var rv=$$('.rv');
if('IntersectionObserver' in window){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.1,rootMargin:'0px 0px -4% 0px'});
  rv.forEach(function(el){io.observe(el)});
}else rv.forEach(function(el){el.classList.add('in')});

/* hero parallax */
var hi=$('#heroimg');
if(hi&&!window.matchMedia('(prefers-reduced-motion:reduce)').matches){
  window.addEventListener('scroll',function(){if(window.scrollY<900)hi.style.transform='scale(1.06) translateY('+Math.min(window.scrollY*.04,20)+'px)'},{passive:true});
}

/* crop picker tabs */
var tabs=$$('.tab');
if(tabs.length){
  var sel=function(i){tabs.forEach(function(b,j){b.setAttribute('aria-selected',j===i);b.tabIndex=j===i?0:-1});$$('.panel').forEach(function(p,j){p.hidden=j!==i})};
  tabs.forEach(function(b,i){
    b.onclick=function(){sel(i)};
    b.onkeydown=function(e){var n=null;if(e.key==='ArrowRight')n=(i+1)%tabs.length;if(e.key==='ArrowLeft')n=(i-1+tabs.length)%tabs.length;if(n!==null){e.preventDefault();sel(n);tabs[n].focus()}};
  });
}

/* forms -> WhatsApp */
$$('form[data-wa]').forEach(function(f){
  f.addEventListener('submit',function(e){
    e.preventDefault();
    if(!f.reportValidity())return;
    var lines=[];
    $$('[name]',f).forEach(function(el){var v=(el.value||'').trim();if(v)lines.push((el.getAttribute('data-l')||el.name)+': '+v)});
    window.open('https://wa.me/'+f.getAttribute('data-wa')+'?text='+encodeURIComponent(lines.join('\n')),'_blank','noopener');
  });
});
})();
