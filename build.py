import re, pathlib

D = pathlib.Path.home() / "Downloads" / "everest-n50-brief"
SRC = D / "source"
A = (SRC / "Everest_N50_Brief.html").read_text()
B = (SRC / "Everest_Briefing_Jason_v2.html").read_text()

def grab(src, start_re, end_re):
    s = re.search(start_re, src)
    e = re.search(end_re, src[s.end():])
    return src[s.end(): s.end() + e.start()]

def prefix_ids(html, p):
    html = re.sub(r'id="tldr"', 'id="%s-tldr"' % p, html)
    html = re.sub(r'href="#tldr"', 'href="#%s-tldr"' % p, html)
    html = re.sub(r'id="s(\d\d)"', lambda m: 'id="%s%s"' % (p, m.group(1)), html)
    html = re.sub(r'href="#s(\d\d)"', lambda m: 'href="#%s%s"' % (p, m.group(1)), html)
    return html

head_a   = grab(A, r'<head>', r'</head>')
style_a  = grab(A, r'<style>', r'</style>')
style_b  = grab(B, r'<style>', r'</style>')
mast_a   = grab(A, r'<header class="mast">', r'</header>')
rule_a   = '<div class="rule-band">' + grab(A, r'<div class="rule-band">', r'\n</div>') + '\n</div>'
nav_a    = prefix_ids(grab(A, r'<nav class="nav" aria-label="Sections">', r'</nav>'), 'a')
nav_b    = prefix_ids(grab(B, r'<nav class="nav" aria-label="Sections">', r'</nav>'), 'b')
main_a   = prefix_ids(grab(A, r'<main class="main">', r'\n  </main>'), 'a')
main_b   = prefix_ids(grab(B, r'<main class="main">', r'\n  </main>'), 'b')

# meta/font links from A's head, minus the title
head_links = "\n".join(l for l in head_a.strip().split("\n")
                       if l.strip().startswith(("<meta", "<link")))

# rules that exist only in v2, scoped to part B where they conflict with part A
extra_css = """
  /* ---- merge layer: part B overrides + combined-page chrome ---- */
  :root{--cream-40:rgba(247,245,237,.40)}

  #part-b .figwrap{padding:24px 22px 18px;display:grid;grid-template-columns:1fr;gap:20px;align-items:center}
  @media (min-width:680px){#part-b .figwrap{grid-template-columns:minmax(0,320px) minmax(0,1fr);gap:30px;padding:26px 30px}}
  #part-b .figwrap svg{max-width:none;margin:0}
  #part-b .figcap{margin:0;max-width:none}
  #part-b .figcap p{margin:0 0 10px}
  #part-b .figcap p:last-child{margin:0}
  #part-b .conf{border:1px solid var(--navy-14);background:none;color:var(--steel)}
  #part-b .conf.low{border-color:var(--gold);background:rgba(242,184,68,.22);color:var(--navy)}

  .red{list-style:none;margin:0;padding:0;max-width:68ch}
  .red li{padding:13px 0;border-bottom:1px solid var(--navy-14)}
  .red .was{font-family:var(--mono);font-size:12px;color:var(--navy-55);text-decoration:line-through;display:block;margin-bottom:5px}
  .red .now{display:block;font-size:15.5px;line-height:1.55}
  .red .now b{font-weight:600}

  .nav .grp{font-family:var(--mono);font-size:9px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--gold);padding:0 0 6px 14px;margin:0}
  .nav .grp.next{margin-top:22px;padding-top:18px;border-top:1px solid var(--navy-14);margin-left:-1px}
  .nav ol + .grp{margin-top:22px}

  .part-open{margin:0;padding:70px 0 0}
  #part-b .part-open{margin-top:34px;border-top:3px solid var(--navy);padding-top:46px}
  .part-tag{font-family:var(--mono);font-size:10px;font-weight:600;letter-spacing:.2em;text-transform:uppercase;color:var(--gold);margin:0 0 8px}
  .part-open h2{font-family:var(--display);font-weight:900;text-transform:uppercase;letter-spacing:-.02em;font-size:clamp(23px,3.4vw,34px);line-height:1.02;margin:0 0 10px}
  .part-open p{margin:0;max-width:62ch;color:var(--navy-80);font-size:15.5px;line-height:1.6}
  .part-open + .tldr{margin-top:24px}
  @media print{.part-open{break-before:page;page-break-before:always}#part-a .part-open{break-before:auto;page-break-before:auto}}

  /* ---- tab bar ---- */
  .tabs{position:sticky;top:0;z-index:20;background:var(--cream);border-bottom:1px solid var(--navy-14)}
  .tabs-in{max-width:1180px;margin:0 auto;padding:0 28px;display:flex;gap:0;overflow-x:auto;scrollbar-width:none}
  .tabs-in::-webkit-scrollbar{display:none}
  .tab{appearance:none;background:none;border:0;border-bottom:3px solid transparent;cursor:pointer;
       padding:15px 0 12px;margin-right:34px;flex:0 0 auto;text-align:left;color:var(--navy-55);
       font-family:var(--mono);font-size:11px;letter-spacing:.13em;text-transform:uppercase;font-weight:600;
       display:flex;align-items:baseline;gap:9px;white-space:nowrap;transition:color .12s}
  .tab:last-child{margin-right:0}
  .tab i{font-style:normal;font-size:9.5px;color:var(--navy-14);letter-spacing:.1em}
  .tab:hover{color:var(--navy)}
  .tab[aria-selected="true"]{color:var(--navy);border-bottom-color:var(--gold)}
  .tab[aria-selected="true"] i{color:var(--gold)}
  .tab b{font-weight:600}
  @media (max-width:620px){.tab{font-size:10px;margin-right:22px}.tab i{display:none}}

  /* tabbed mode: only the active part is shown (JS adds .tabbed to <body>) */
  .tabbed .part{display:none}
  .tabbed .part.on{display:block}
  .tabbed .part-open{padding-top:46px}
  .tabbed #part-b .part-open{margin-top:0;border-top:0}
  .tabbed .nav .grp,.tabbed .nav ol{display:none}
  .tabbed .nav .grp.on,.tabbed .nav ol.on{display:block}
  .tabbed .nav .grp.on{margin-top:0;padding-top:0;border-top:0}
  @media print{.tabs{display:none}.tabbed .part{display:block !important}}
  @media (min-width:1020px){.nav{top:74px}}
  .part:focus{outline:none}
  .sec,.tldr{scroll-margin-top:62px}
"""

nav = """  <nav class="nav" aria-label="Sections">
    <p class="grp" data-part="a">Part I &middot; Strategic brief</p>%s
    <p class="grp next" data-part="b">Part II &middot; Corrections (v2)</p>%s
  </nav>""" % (nav_a.replace('<ol>', '<ol data-part="a">', 1),
               nav_b.replace('<ol>', '<ol data-part="b">', 1))

tabs = """<div class="tabs">
  <div class="tabs-in" role="tablist" aria-label="Brief sections">
    <button class="tab" type="button" role="tab" id="tab-a" aria-controls="part-a" aria-selected="true"><i>I</i><b>Strategic brief</b></button>
    <button class="tab" type="button" role="tab" id="tab-b" aria-controls="part-b" aria-selected="false"><i>II</i><b>Corrections &amp; fact check</b></button>
  </div>
</div>"""

open_a = """    <div class="part-open">
      <p class="part-tag">Part I</p>
      <h2>Strategic and technical brief</h2>
      <p>Who Everest is, what they can actually make, and where North 50 fits. Read this first.</p>
    </div>"""

open_b = """    <div class="part-open">
      <p class="part-tag">Part II</p>
      <h2>Corrections and fact check</h2>
      <p>Version 2 of the Jason briefing. Where Part I is wrong or incomplete, this section overrides it.</p>
    </div>"""

doc = """<!DOCTYPE html>
<html lang="en">
<head>
%s
<title>Everest &times; North 50 | Strategic Brief and Corrections</title>
<style>
%s
%s
</style>
</head>
<body>

%s

%s

%s

<div class="shell">
%s

  <main class="main">
    <div class="part on" id="part-a" role="tabpanel" aria-labelledby="tab-a" tabindex="-1">
%s
%s
    </div>

    <div class="part" id="part-b" role="tabpanel" aria-labelledby="tab-b" tabindex="-1">
%s
%s
    </div>
  </main>
</div>

<script>
(function(){
  var PARTS = ['a','b'];
  var tabs = PARTS.map(function(p){ return document.getElementById('tab-' + p); });
  var panels = PARTS.map(function(p){ return document.getElementById('part-' + p); });
  var navGroups = Array.prototype.slice.call(document.querySelectorAll('.nav [data-part]'));
  var links = Array.prototype.slice.call(document.querySelectorAll('.nav a'));

  document.body.classList.add('tabbed');

  function show(part, focusPanel){
    PARTS.forEach(function(p, i){
      var on = p === part;
      tabs[i].setAttribute('aria-selected', on ? 'true' : 'false');
      panels[i].classList.toggle('on', on);
    });
    navGroups.forEach(function(el){ el.classList.toggle('on', el.getAttribute('data-part') === part); });
    if(focusPanel) panels[PARTS.indexOf(part)].focus({preventScroll:true});
  }

  function partOfHash(h){
    if(!h || h.length < 2) return null;
    var el = document.getElementById(h.slice(1));
    if(!el) return null;
    var host = el.closest('.part');
    return host ? host.id.slice(5) : null;
  }

  tabs.forEach(function(t, i){
    t.addEventListener('click', function(){
      show(PARTS[i], true);
      window.scrollTo({top:0, behavior:'smooth'});
      history.replaceState(null, '', '#part-' + PARTS[i]);
    });
    t.addEventListener('keydown', function(e){
      if(e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      e.preventDefault();
      var next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) %% tabs.length];
      next.focus(); next.click();
    });
  });

  // deep links: #part-b, or any section anchor inside a part
  function sync(){
    var h = location.hash;
    var p = h === '#part-b' ? 'b' : (h === '#part-a' ? 'a' : partOfHash(h));
    if(p){
      show(p, false);
      if(h.indexOf('#part-') !== 0){
        var target = document.getElementById(h.slice(1));
        if(target) target.scrollIntoView();
      }
    }
  }
  show('a', false);
  sync();
  window.addEventListener('hashchange', sync);

  // sidebar scroll highlighting
  var secs = links.map(function(a){ return document.querySelector(a.getAttribute('href')); }).filter(Boolean);
  if('IntersectionObserver' in window && secs.length){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(!e.isIntersecting) return;
        links.forEach(function(a){ a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, {rootMargin:'-12%% 0px -75%% 0px', threshold:0});
    secs.forEach(function(s){ io.observe(s); });
  }
})();
</script>
</body>
</html>
""" % (head_links, style_a, extra_css,
       '<header class="mast">' + mast_a + '</header>',
       rule_a, tabs, nav, open_a, main_a, open_b, main_b)

(D / "index.html").write_text(doc)
print("wrote index.html", len(doc), "bytes")
print("part A sections:", len(re.findall(r'id="a\d\d"', doc)))
print("part B sections:", len(re.findall(r'id="b\d\d"', doc)))
print("dangling #s refs:", re.findall(r'href="#s\d\d"', doc))
print("nav links:", len(re.findall(r'class="nav"', doc)), len(re.findall(r'<a href="#[ab]', doc)))
