# Generates index.html for this client's portfolio from data.py and client.py. Run: python3 tools/build_site.py
import os, sys, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import SITES, CLIENT, CLIENT_SHORT, CLIENT_GREETING, CLIENT_SALUTATION, CLIENT_SURNAME, CLIENT_SIGNOFF, SLUG, AGENT, DATE
import urllib.parse
import json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSS = r"""
:root{
  --onyx:#0b0a08; --umber:#14110e; --smoke:#1e1a15; --ivory:#efe7d8; --ash:#9a907e; --ash-2:#6d6557;
  --brass:#b8935a; --brass-hi:#e6cb92; --brass-lo:#7c6136;
  --bone:#f2ece1; --bone-2:#e8e0d1; --ink:#1a1611; --ink-2:#5b5347;
  --fd:"Gilda Display",Georgia,"Times New Roman",serif;
  --fi:"Cormorant Garamond",Georgia,"Times New Roman",serif;
  --fs:"Instrument Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  --ease:cubic-bezier(.77,0,.18,1); --ease-o:cubic-bezier(.16,1,.3,1);
  --gut:clamp(20px,5vw,72px);
  color-scheme:dark;
}
*,*::before,*::after{box-sizing:border-box}
html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
html,body{overflow-x:clip}
body{margin:0;background:var(--onyx);color:var(--ivory);font-family:var(--fs);font-size:16px;line-height:1.5;-webkit-font-smoothing:antialiased;-webkit-tap-highlight-color:transparent}
body.locked{position:fixed;left:0;right:0;width:100%;overflow:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;background:none;border:0;padding:0;cursor:pointer}
:focus-visible{outline:1px solid var(--brass);outline-offset:3px}
::selection{background:var(--brass);color:var(--onyx)}
h1,h2,h3{font-weight:400;margin:0;text-wrap:balance}
p{margin:0}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* grain + vignette */
body::before{content:"";position:fixed;inset:0;z-index:1000;pointer-events:none;opacity:.07;mix-blend-mode:overlay;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='220' height='220'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .6 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")}

/* pages */
.pg{position:relative;background:var(--bg);color:var(--fg);padding-block:clamp(84px,12vh,150px);--bg:var(--onyx);--fg:var(--ivory);--mute:var(--ash);--acc:var(--brass);--acc-hi:var(--brass-hi);--rule:rgba(239,231,216,.14);--panel:var(--umber);--rule-2:rgba(239,231,216,.07)}
.pg[data-shade="light"]{--bg:var(--bone);--fg:var(--ink);--mute:var(--ink-2);--acc:var(--brass-lo);--acc-hi:var(--brass);--rule:rgba(26,22,17,.16);--panel:var(--bone-2);--rule-2:rgba(26,22,17,.08);color-scheme:light}
.wrap{padding-inline:var(--gut);max-width:1560px;margin-inline:auto}
.eyebrow{font-family:var(--fs);font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:var(--acc);display:flex;align-items:center;gap:14px;font-weight:500}
.eyebrow::before{content:"";width:28px;height:1px;background:var(--acc);flex:none}
.eyebrow.plain::before{display:none}
.t-display{font-family:var(--fd);line-height:.98;letter-spacing:-.012em}
.t-2{font-family:var(--fd);font-size:clamp(2.4rem,5vw,4.4rem);line-height:1.02;letter-spacing:-.012em}
.t-3{font-family:var(--fd);font-size:clamp(1.6rem,2.6vw,2.2rem);line-height:1.15}
.t-i{font-family:var(--fi);font-style:italic;font-weight:400}
.lede{font-family:var(--fi);font-size:clamp(1.2rem,1.6vw,1.45rem);line-height:1.5;max-width:60ch}
.small{font-size:12.5px;color:var(--mute);letter-spacing:.02em}
.rule{height:1px;background:var(--rule);border:0;margin:0}
.num{font-variant-numeric:tabular-nums}

/* chips */
.chip{display:inline-flex;align-items:center;gap:8px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;font-weight:500;padding:7px 12px;border:1px solid var(--rule);border-radius:999px;white-space:nowrap}
.chip i{width:6px;height:6px;border-radius:50%;background:currentColor;display:inline-block}
.chip[data-s="Ready"]{color:#9fd3a6}.chip[data-s="Selling"]{color:var(--acc-hi)}.chip[data-s="Off-plan"]{color:var(--mute)}
.pg[data-shade="light"] .chip[data-s="Ready"]{color:#2f6b3a}.pg[data-shade="light"] .chip[data-s="Selling"]{color:var(--brass-lo)}

/* veil */
#veil{position:fixed;inset:0;top:0;right:0;bottom:0;left:0;z-index:300;background:var(--onyx);color:var(--ivory);display:flex;flex-direction:column;align-items:center;justify-content:center;gap:28px;transition:transform 1.1s var(--ease),visibility 0s 1.1s;will-change:transform}
#veil.off{transform:translateY(-101%);visibility:hidden}
#veil .mark{width:64px;height:64px;color:var(--ivory);animation:markin 1.2s var(--ease-o) both}
#veil .vt{font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--ash)}
#veil .bar{width:min(320px,60vw);height:1px;background:var(--rule-2,rgba(239,231,216,.1));position:relative;overflow:hidden}
#veil .bar i{position:absolute;inset:0;background:var(--brass);transform-origin:left;transform:scaleX(0)}
#veil .ct{font-family:var(--fd);font-size:14px;letter-spacing:.1em;color:var(--brass);min-width:3ch;text-align:center}
@keyframes markin{from{opacity:0;transform:scale(.9)}to{opacity:1;transform:none}}

/* header */
.top{position:fixed;top:0;left:0;right:0;z-index:120;height:68px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;padding-inline:clamp(16px,3vw,36px);mix-blend-mode:difference;color:#efe7d8;opacity:0;transform:translateY(-8px);transition:opacity .9s ease 1.2s,transform .9s var(--ease-o) 1.2s;pointer-events:none}
body.ready .top{opacity:1;transform:none;pointer-events:auto}
.top .brand{display:flex;align-items:center;gap:12px;font-size:11px;letter-spacing:.22em;text-transform:uppercase}
.top .brand svg{width:30px;height:30px}
.top .brand span b{display:block;font-weight:500}
.top .brand span small{display:block;font-size:9.5px;letter-spacing:.2em;opacity:.7}
.top .ttl{font-family:var(--fd);font-size:15px;letter-spacing:.14em;text-transform:uppercase;text-align:center}
.top .ttl em{font-family:var(--fi);font-style:italic;text-transform:none;letter-spacing:0;font-size:17px;opacity:.85}
.top .acts{display:flex;justify-content:flex-end;gap:8px}
.top .btn{display:inline-flex;align-items:center;gap:10px;font-size:11px;letter-spacing:.2em;text-transform:uppercase;font-weight:500;padding:9px 14px;border:1px solid rgba(239,231,216,.35);border-radius:999px;transition:border-color .3s}
.top .btn:hover{border-color:#efe7d8}
.top .btn .n{font-family:var(--fd);font-size:13px;min-width:1.2ch;text-align:center}
.top .btn.sl .n:empty{display:none}
@media (max-width:760px){.top .ttl{display:none}.top{grid-template-columns:1fr auto}.top .brand span small{display:none}}
@media (max-width:480px){.top .btn.sl{display:none}#welcome .meta span:first-child{display:none}}

/* side tabs */
.tabs{position:fixed;right:18px;top:50%;transform:translateY(-50%);z-index:110;display:flex;flex-direction:column;gap:6px;mix-blend-mode:difference;color:#efe7d8;opacity:0;transition:opacity .8s ease}
body.ready .tabs{opacity:1}
.tabs button{display:flex;align-items:center;justify-content:flex-end;gap:10px;height:22px;position:relative}
.tabs button .l{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;opacity:0;transform:translateX(6px);transition:.35s;white-space:nowrap}
.tabs button:hover .l,.tabs button.on .l{opacity:1;transform:none}
.tabs button .k{font-family:var(--fd);font-size:11px;letter-spacing:.08em;opacity:.55;min-width:2ch;text-align:right;transition:opacity .3s}
.tabs button i{width:14px;height:1px;background:currentColor;opacity:.5;transition:.35s;flex:none}
.tabs button.on .k{opacity:1}.tabs button.on i{width:30px;opacity:1}
.tabs button.sec .k{font-size:9px;letter-spacing:.2em}
@media (max-width:1000px){.tabs{display:none}}
.progress{position:fixed;left:0;right:0;bottom:0;height:2px;z-index:115;background:transparent;pointer-events:none}
.progress i{display:block;height:100%;width:100%;background:var(--brass);transform-origin:left;transform:scaleX(0)}

/* welcome */
#welcome{position:relative;min-height:100svh;display:grid;grid-template-rows:1fr auto;overflow:hidden;background:var(--onyx);color:var(--ivory)}
#welcome .bg{position:absolute;inset:0;overflow:hidden}
#welcome .bg img{width:100%;height:100%;object-fit:cover;object-position:50% 42%;transform:scale(1.14);opacity:0;transition:opacity 1.6s ease .2s}
body.ready #welcome .bg img{opacity:1;animation:kb 16s var(--ease-o) .1s forwards}
@keyframes kb{from{transform:scale(1.14)}to{transform:scale(1.02)}}
#welcome .bg::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,10,8,.35) 0%,rgba(11,10,8,.15) 35%,rgba(11,10,8,.72) 72%,rgba(11,10,8,.96) 100%),linear-gradient(90deg,rgba(11,10,8,.55) 0%,rgba(11,10,8,0) 60%)}
#welcome .stage{position:relative;z-index:2;padding:calc(68px + 4vh) var(--gut) 5vh;display:flex;flex-direction:column;justify-content:flex-end;max-width:1560px;width:100%;margin-inline:auto}
#welcome .meta{position:absolute;top:calc(68px + 2vh);left:var(--gut);right:var(--gut);display:flex;justify-content:space-between;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:rgba(239,231,216,.7);opacity:0;transition:opacity 1s ease 1.6s}
body.ready #welcome .meta{opacity:1}
#welcome .meta .mono{font-family:var(--fd);letter-spacing:.2em}
.w-eye{opacity:0;transform:translateY(10px);transition:opacity .9s ease 1.3s,transform .9s var(--ease-o) 1.3s}
body.ready .w-eye{opacity:1;transform:none}
.w-back{font-family:var(--fi);font-style:italic;font-weight:300;font-size:clamp(1.9rem,4.2vw,3.6rem);color:var(--brass-hi);line-height:1.15;margin-top:22px;display:flex;flex-wrap:wrap;gap:0 .3em;overflow:hidden}
.w-back span{display:inline-block;transform:translateY(110%);opacity:0;transition:transform 1s var(--ease-o),opacity .6s ease}
body.ready .w-back span{transform:none;opacity:1}
body.ready .w-back span:nth-child(1){transition-delay:1.55s}body.ready .w-back span:nth-child(2){transition-delay:1.65s}body.ready .w-back span:nth-child(3){transition-delay:1.75s}body.ready .w-back span:nth-child(4){transition-delay:1.85s}
.w-name{font-family:var(--fd);font-size:clamp(3.4rem,10vw,10rem);line-height:.98;letter-spacing:-.015em;margin-top:.1em;display:flex;flex-wrap:wrap;column-gap:.24em;color:var(--ivory)}
.w-name .w{display:inline-flex;overflow:hidden;padding-bottom:.08em;margin-bottom:-.08em}
.w-name .ch{display:inline-block;transform:translateY(112%) rotate(3deg);opacity:0;filter:blur(6px);transition:transform 1.1s var(--ease-o),opacity .7s ease,filter .9s ease;transition-delay:calc(1.9s + var(--i)*.045s)}
body.ready .w-name .ch{transform:none;opacity:1;filter:none}
.w-name.shine{background:linear-gradient(105deg,var(--ivory) 0%,var(--ivory) 38%,var(--brass-hi) 48%,#fff6df 52%,var(--brass-hi) 56%,var(--ivory) 66%,var(--ivory) 100%);background-size:260% 100%;background-position:120% 0;-webkit-background-clip:text;background-clip:text;color:transparent;animation:shine 2.6s var(--ease) both}
.w-name.shine .ch{transform:none;opacity:1;filter:none;transition:none}
@keyframes shine{from{background-position:120% 0}to{background-position:-120% 0}}
.w-line{height:1px;background:var(--brass);width:min(520px,60vw);transform-origin:left;transform:scaleX(0);transition:transform 1.4s var(--ease) 3s;margin-top:clamp(20px,3vh,34px)}
body.ready .w-line{transform:none}
.w-sub{font-family:var(--fi);font-size:clamp(1.15rem,1.7vw,1.5rem);line-height:1.5;max-width:58ch;margin-top:clamp(18px,2.6vh,28px);color:rgba(239,231,216,.86);opacity:0;transform:translateY(12px);transition:opacity 1s ease 3.3s,transform 1s var(--ease-o) 3.3s}
body.ready .w-sub{opacity:1;transform:none}
.w-cta{display:flex;align-items:center;gap:26px;margin-top:clamp(24px,4vh,40px);opacity:0;transition:opacity 1s ease 3.7s}
body.ready .w-cta{opacity:1}
.btn-ring{display:inline-flex;align-items:center;gap:14px;font-size:11px;letter-spacing:.24em;text-transform:uppercase;font-weight:500;padding:15px 26px;border:1px solid var(--brass);border-radius:999px;color:var(--ivory);position:relative;overflow:hidden;transition:color .4s}
.btn-ring::before{content:"";position:absolute;inset:0;background:var(--brass);transform:translateY(101%);transition:transform .5s var(--ease);z-index:-1}
.btn-ring:hover{color:var(--onyx)}.btn-ring:hover::before{transform:none}
.btn-ring svg{width:14px;height:14px}
.w-scroll{display:flex;align-items:center;gap:12px;font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:rgba(239,231,216,.65)}
.w-scroll i{width:1px;height:38px;background:rgba(239,231,216,.35);position:relative;overflow:hidden}
.w-scroll i::after{content:"";position:absolute;left:0;top:-100%;width:100%;height:100%;background:var(--brass-hi);animation:drop 2.2s var(--ease) infinite}
@keyframes drop{0%{top:-100%}60%{top:100%}100%{top:100%}}
.ticker{position:relative;z-index:2;border-top:1px solid rgba(239,231,216,.14);background:rgba(11,10,8,.55);backdrop-filter:blur(8px);overflow:hidden;padding-block:14px;opacity:0;transition:opacity 1s ease 3.9s}
body.ready .ticker{opacity:1}
.ticker .row{display:flex;gap:0;width:max-content;animation:tick 70s linear infinite}
.ticker .row span{display:inline-flex;align-items:center;gap:22px;padding-inline:22px;font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:rgba(239,231,216,.7);white-space:nowrap}
.ticker .row span::after{content:"";width:5px;height:5px;background:var(--brass);transform:rotate(45deg)}
@keyframes tick{to{transform:translateX(-50%)}}
.ticker:hover .row{animation-play-state:paused}

/* reveal */
.rv{opacity:0;transform:translateY(26px);transition:opacity 1s ease,transform 1.1s var(--ease-o)}
.rv.in{opacity:1;transform:none}
.rv-stag>*{opacity:0;transform:translateY(22px);transition:opacity .9s ease,transform 1s var(--ease-o)}
.rv-stag.in>*{opacity:1;transform:none}
.rv-stag.in>*:nth-child(1){transition-delay:.05s}.rv-stag.in>*:nth-child(2){transition-delay:.15s}.rv-stag.in>*:nth-child(3){transition-delay:.25s}.rv-stag.in>*:nth-child(4){transition-delay:.35s}.rv-stag.in>*:nth-child(5){transition-delay:.45s}.rv-stag.in>*:nth-child(6){transition-delay:.55s}.rv-stag.in>*:nth-child(7){transition-delay:.65s}.rv-stag.in>*:nth-child(8){transition-delay:.75s}
.wipe{clip-path:inset(0 0 calc(100% - 1px) 0);transition:clip-path 1.3s var(--ease)}
.wipe.in{clip-path:inset(0 0 0 0)}

/* brief */
.brief-g{display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(36px,6vw,110px);align-items:start}
.brief-g .lhs{position:sticky;top:96px}
.brief-g .lhs .t-2{margin-top:22px}
.brief-g .lhs .small{margin-top:26px;max-width:36ch;line-height:1.6}
.letter{font-family:var(--fi);font-size:clamp(1.2rem,1.55vw,1.42rem);line-height:1.55;max-width:62ch;display:grid;gap:1.1em}
.letter .sal{font-family:var(--fd);font-size:1.15em;letter-spacing:.01em}
.letter .sig{margin-top:.6em;display:grid;gap:4px}
.letter .sig b{font-family:var(--fd);font-weight:400;font-size:1.05em}
.letter .sig span{font-family:var(--fs);font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute)}
.letter .sig svg{width:150px;height:auto;color:var(--acc);margin-bottom:6px}
.terms{margin-top:clamp(56px,8vh,96px);border-top:1px solid var(--rule);display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(24px,3vw,48px);padding-top:32px}
.terms h3{font-family:var(--fd);font-size:1.3rem;margin-bottom:10px}
.terms p{font-size:14px;line-height:1.6;color:var(--mute);max-width:36ch}
.terms .k{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:12px}
@media (max-width:900px){.brief-g{grid-template-columns:1fr}.brief-g .lhs{position:static}.terms{grid-template-columns:1fr}}

/* glance */
.stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));border-top:1px solid var(--rule);border-bottom:1px solid var(--rule)}
.stats>div{padding:28px 22px 26px 0;border-right:1px solid var(--rule-2)}
.stats>div:last-child{border-right:0}
.stats>div+div{padding-left:22px}
.stats .v{font-family:var(--fd);font-size:clamp(2.2rem,3.6vw,3.6rem);line-height:1;letter-spacing:-.01em}
.stats .v.rng{font-size:clamp(1.5rem,2.3vw,2.3rem);line-height:1.15}
.stats .v small{font-size:.5em;letter-spacing:0;color:var(--mute);margin-left:.15em}
.stats .k{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute);margin-top:12px}
@media (max-width:760px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}.stats>div:nth-child(2n){border-right:0}.stats>div:nth-child(odd){padding-left:0}.stats>div:nth-child(even){padding-left:18px}.stats>div{border-bottom:1px solid var(--rule-2)}}
.map-h{display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap;margin-top:clamp(56px,8vh,96px)}
.map-h .t-3{margin-top:16px}
.map-ctl{display:flex;gap:10px;flex-wrap:wrap}
.seg{display:inline-flex;border:1px solid var(--rule);border-radius:999px;padding:3px}
.seg button{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;font-weight:500;padding:8px 14px;border-radius:999px;color:var(--mute);transition:.3s;white-space:nowrap}
.seg button:hover{color:var(--fg)}
.seg button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
.map-g{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(280px,1fr);gap:clamp(20px,3vw,44px);align-items:stretch;margin-top:26px}
.lmap-wrap{position:relative;height:clamp(460px,64vh,720px);border:1px solid var(--rule);background:var(--panel);overflow:hidden;isolation:isolate}
#lmap{width:100%;height:100%;background:var(--panel);opacity:0;transition:opacity 1.2s ease}
.lmap-wrap.ready #lmap{opacity:1}
.lmap-wrap.night:not(.aerial) .leaflet-tile-pane .leaflet-tile{filter:invert(1) hue-rotate(180deg) grayscale(.92) brightness(.78) contrast(1.08);-webkit-filter:invert(1) hue-rotate(180deg) grayscale(.92) brightness(.78) contrast(1.08)}
.lmap-wrap .leaflet-container{font-family:var(--fs);font-size:12px}
.lmap-wrap .leaflet-container a{color:inherit}
.lmap-wrap .leaflet-control-zoom{border:1px solid var(--rule);border-radius:0;overflow:hidden;margin:14px;box-shadow:none}
.lmap-wrap .leaflet-bar a{background:var(--umber);color:var(--ivory);border-bottom:1px solid var(--rule);width:34px;height:34px;line-height:32px;font-family:var(--fd);font-size:20px}
.lmap-wrap .leaflet-bar a:last-child{border-bottom:0}
.lmap-wrap .leaflet-bar a:hover{background:var(--smoke);color:var(--brass-hi)}
.lmap-wrap .leaflet-bar a.leaflet-disabled{color:var(--ash-2)}
.lmap-wrap .leaflet-control-attribution{background:rgba(11,10,8,.7);color:var(--ash);font:400 9.5px/1.4 var(--fs);letter-spacing:.02em;padding:3px 8px}
.lmap-wrap .leaflet-control-scale{margin:0 0 12px 14px}
.lmap-wrap .leaflet-control-scale-line{border:1px solid rgba(239,231,216,.5);border-top:0;background:rgba(11,10,8,.6);color:var(--ivory);font:500 9.5px/1.7 var(--fs);letter-spacing:.1em;padding:1px 6px}
.lmap-wrap .lm-pin{width:0!important;height:0!important;margin:0!important;border:0;background:none}
.lmap-wrap .lm-pin i{position:absolute;left:-13px;top:-13px;width:26px;height:26px;border-radius:50%;background:var(--brass);color:var(--onyx);border:1.5px solid var(--onyx);box-shadow:0 0 0 4px rgba(184,147,90,.22),0 2px 10px rgba(0,0,0,.5);font:400 11px/23px var(--fd);letter-spacing:.06em;text-align:center;font-style:normal;transition:.3s}
.lmap-wrap .lm-pin b{position:absolute;left:18px;top:-9px;white-space:nowrap;font:500 10px/18px var(--fs);letter-spacing:.16em;text-transform:uppercase;color:var(--ivory);text-shadow:0 0 4px #0b0a08,0 0 8px #0b0a08,0 1px 2px #0b0a08}
.lmap-wrap.aerial .lm-pin b{text-shadow:0 0 4px #000,0 0 8px #000}
.lmap-wrap.far .lm-pin:not(.on):not(:hover) b{opacity:0}
.lmap-wrap .lm-pin b{transition:opacity .3s}
.lmap-wrap .lm-pin.on i,.lmap-wrap .lm-pin:hover i{background:var(--brass-hi);transform:scale(1.15)}
.lmap-wrap .lm-pin.ap i{background:var(--umber);color:var(--brass-hi);border-color:var(--brass)}
.lmap-wrap .leaflet-popup-content-wrapper{background:var(--umber);color:var(--ivory);border-radius:0;border:1px solid var(--rule);box-shadow:0 14px 40px rgba(0,0,0,.5);padding:0}
.lmap-wrap .leaflet-popup-content{margin:16px 18px 15px;font:400 13px/1.5 var(--fs);min-width:220px}
.lmap-wrap .leaflet-popup-tip{background:var(--umber);box-shadow:none}
.lmap-wrap .leaflet-container a.leaflet-popup-close-button{color:var(--ash);font:300 20px/22px var(--fs);padding:6px 8px 0 0;width:auto;height:auto}
.lm-pop .k{font-family:var(--fd);color:var(--brass);letter-spacing:.2em;font-size:11px}
.lm-pop .n{font-family:var(--fd);font-size:18px;margin:4px 0 2px}
.lm-pop .a{color:var(--ash);font-size:12px}
.lm-pop .p{font-family:var(--fd);font-size:15px;margin-top:8px}
.lm-pop .x{display:flex;gap:14px;margin-top:12px;font-size:10px;letter-spacing:.18em;text-transform:uppercase;font-weight:500;color:var(--brass-hi)}
.map-h .t-3 em{color:var(--acc-hi)}
.lm-panel{border:1px solid var(--rule);background:var(--panel);display:flex;flex-direction:column;max-height:clamp(460px,64vh,720px);overflow:auto;scrollbar-width:thin}
.lm-grp{border-bottom:1px solid var(--rule-2)}
.lm-gh{display:flex;justify-content:space-between;gap:12px;padding:12px 18px 8px;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute);background:rgba(239,231,216,.03)}
.lm-panel .mrow{display:grid;grid-template-columns:26px 1fr auto;gap:14px;align-items:center;text-align:left;padding:12px 18px;border-top:1px solid var(--rule-2);width:100%;transition:background .3s,color .3s}
.lm-panel .mrow:hover{background:rgba(239,231,216,.04)}
.lm-panel .mrow[aria-pressed="true"]{background:rgba(184,147,90,.12)}
.lm-panel .mrow .k{width:26px;height:26px;border-radius:50%;background:var(--brass);color:var(--onyx);font:400 11px/25px var(--fd);text-align:center;letter-spacing:.06em;border:1px solid var(--onyx);box-shadow:0 0 0 3px rgba(184,147,90,.18)}
.lm-panel .mrow .t{font-size:14.5px;line-height:1.25}
.lm-panel .mrow .t small{display:block;font-size:11.5px;color:var(--mute);margin-top:3px}
.lm-panel .mrow .dist{font-size:11px;letter-spacing:.06em;color:var(--mute);white-space:nowrap;text-align:right}
.lm-panel .mrow .dist b{font-family:var(--fd);font-weight:400;font-size:15px;color:var(--fg);letter-spacing:0}
.lm-note{padding:14px 18px;font-size:12px;line-height:1.55;color:var(--mute);margin-top:auto}
.lm-hint{position:absolute;left:50%;top:14px;transform:translateX(-50%);z-index:500;font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--ivory);background:rgba(11,10,8,.72);border:1px solid var(--rule);padding:8px 14px;pointer-events:none;transition:opacity .5s;white-space:nowrap}
.lmap-wrap.wheel .lm-hint,.lmap-wrap.failed .lm-hint{opacity:0}
.lmap-wrap .lm-ref{width:0!important;height:0!important;margin:0!important;border:0;background:none}
.lmap-wrap .lm-ref i{position:absolute;left:-5px;top:-5px;width:10px;height:10px;border-radius:50%;background:var(--onyx);border:1.5px solid var(--ivory);opacity:.85}
.lmap-wrap .lm-ref.dest i{background:var(--ivory);border-color:var(--onyx);width:12px;height:12px;left:-6px;top:-6px}
.lmap-wrap .lm-ref b{position:absolute;left:11px;top:-8px;white-space:nowrap;font:500 9.5px/16px var(--fs);letter-spacing:.14em;text-transform:uppercase;color:rgba(239,231,216,.8);text-shadow:0 0 4px #0b0a08,0 0 8px #0b0a08}
.lmap-wrap.far .lm-ref:not(.dest) b{opacity:0}
.lmap-wrap .leaflet-tooltip{background:var(--umber);color:var(--ivory);border:1px solid var(--rule);border-radius:0;font:400 11px/1.4 var(--fs);letter-spacing:.06em;box-shadow:none}
.lmap-wrap .leaflet-tooltip::before{display:none}
@media (max-width:900px){.lm-panel{max-height:420px}}
.map-fb{position:absolute;inset:0;padding:clamp(20px,3vw,36px);overflow:auto;background:var(--panel)}
.map-fb p{margin:14px 0 18px;color:var(--mute);max-width:52ch;font-size:14px;line-height:1.6}
.map-fb .fbrows{border-top:1px solid var(--rule)}
.map-fb .fbrows a,.map-side .districts button{display:grid;grid-template-columns:3ch 1fr auto;gap:16px;align-items:baseline;text-align:left;padding:12px 0;border-bottom:1px solid var(--rule-2);transition:color .3s;width:100%}
.map-fb .fbrows a:hover,.map-side .districts button:hover,.map-side .districts button.on{color:var(--acc-hi)}
.map-fb .fbrows .k,.map-side .districts .k{font-family:var(--fd);font-size:13px;color:var(--acc)}
.map-fb .fbrows small,.map-side .districts small{display:block;font-size:11px;color:var(--mute);margin-top:2px;letter-spacing:.02em}
.map-fb .fbrows .d,.map-side .districts .d{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);white-space:nowrap}
.map-side p{color:var(--mute);font-size:14.5px;line-height:1.65}
.map-side .districts{margin-top:18px;border-top:1px solid var(--rule)}
@media (max-width:900px){.map-g{grid-template-columns:1fr}.lmap-wrap{height:min(70vh,520px)}.lm-hint{display:none}}

/* ledger */
.ledger-h{display:flex;justify-content:space-between;align-items:end;gap:20px;margin-top:clamp(64px,9vh,110px);flex-wrap:wrap}
.ledger-h .t-2{margin-top:18px}
.ledger-h .sorts{display:flex;gap:8px;flex-wrap:wrap}
.ledger-h .sorts button{font-size:11px;letter-spacing:.18em;text-transform:uppercase;padding:9px 14px;border:1px solid var(--rule);border-radius:999px;color:var(--mute);transition:.3s}
.ledger-h .sorts button.on,.ledger-h .sorts button:hover{color:var(--fg);border-color:var(--acc)}
.ledger-w{overflow-x:auto;margin-top:26px;-webkit-overflow-scrolling:touch}
.ledger{width:100%;min-width:900px;border-collapse:collapse;font-size:14px}
.ledger th{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute);font-weight:500;text-align:left;padding:0 14px 14px 0;border-bottom:1px solid var(--rule);white-space:nowrap}
.ledger td{padding:16px 14px 16px 0;border-bottom:1px solid var(--rule-2);vertical-align:top}
.ledger tr{transition:background .3s}
.ledger tbody tr{cursor:pointer}
.ledger tbody tr:hover td{background:rgba(239,231,216,.03)}
.ledger .k{font-family:var(--fd);color:var(--acc);font-size:15px}
.ledger .nm{font-family:var(--fd);font-size:19px;letter-spacing:-.005em}
.ledger .nm small{display:block;font-family:var(--fs);font-size:11.5px;color:var(--mute);letter-spacing:.06em;margin-top:3px}
.ledger .pr{font-family:var(--fd);font-size:17px;white-space:nowrap}
.ledger .vw{color:var(--mute);max-width:26ch;font-size:13px;line-height:1.5}
.ledger .st{text-align:right;padding-right:0}
.ledger td.star-c{width:44px}

/* star */
.star{width:38px;height:38px;border:1px solid var(--rule);border-radius:50%;display:inline-grid;place-items:center;color:var(--mute);transition:.35s;flex:none;position:relative}
.star svg{width:14px;height:14px;fill:none;stroke:currentColor;stroke-width:1.2;transition:.35s}
.star:hover{border-color:var(--acc);color:var(--acc-hi)}
.star.on{border-color:var(--acc);color:var(--acc-hi);background:rgba(184,147,90,.12)}
.star.on svg{fill:currentColor}
.star.pop{animation:pop .5s var(--ease-o)}
@keyframes pop{0%{transform:scale(1)}40%{transform:scale(1.22)}100%{transform:scale(1)}}

/* shelf */
.shelf-h{display:flex;justify-content:space-between;align-items:end;gap:20px;flex-wrap:wrap}
.shelf-h .t-2{margin-top:18px}
.shelf-h .arrows{display:flex;gap:8px}
.shelf-h .arrows button{width:46px;height:46px;border:1px solid var(--rule);border-radius:50%;display:grid;place-items:center;transition:.3s}
.shelf-h .arrows button:hover{border-color:var(--acc);color:var(--acc-hi)}
.shelf-h .arrows svg{width:16px;height:16px}
.shelf{display:flex;gap:clamp(14px,1.6vw,22px);overflow-x:auto;scroll-snap-type:x mandatory;padding-block:36px 8px;margin-inline:calc(-1*var(--gut));padding-inline:var(--gut);scrollbar-width:none;cursor:grab}
.shelf::-webkit-scrollbar{display:none}
.shelf.drag{cursor:grabbing;scroll-snap-type:none}
.card{flex:0 0 clamp(250px,24vw,330px);scroll-snap-align:start;display:grid;gap:14px}
.card .pl{position:relative;aspect-ratio:3/4;overflow:hidden;background:var(--panel);border:1px solid var(--rule-2)}
.card .pl img{width:100%;height:100%;object-fit:cover;transition:transform 1.2s var(--ease-o),filter .6s}
.card:hover .pl img{transform:scale(1.05)}
.card .pl .k{position:absolute;left:14px;top:12px;font-family:var(--fd);font-size:13px;letter-spacing:.14em;color:var(--ivory);text-shadow:0 1px 8px rgba(0,0,0,.5)}
.card .pl .chip{position:absolute;right:12px;top:12px;background:rgba(11,10,8,.55);backdrop-filter:blur(6px);border-color:rgba(239,231,216,.2)}
.card .pl .dg{position:absolute;inset:0;display:grid;place-items:center;background:linear-gradient(180deg,var(--smoke),var(--umber))}
.card .pl .dg svg{width:70%;height:auto}
.card .nm{font-family:var(--fd);font-size:1.45rem;line-height:1.1}
.card .nm small{display:block;font-family:var(--fs);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);margin-top:6px}
.card .pr{display:flex;justify-content:space-between;align-items:baseline;border-top:1px solid var(--rule-2);padding-top:12px;font-size:13px;color:var(--mute)}
.card .pr b{font-family:var(--fd);font-weight:400;font-size:16px;color:var(--fg)}

/* dossier */
.dz .run{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:16px;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute);padding-bottom:18px;border-bottom:1px solid var(--rule)}
.dz .run .r{display:flex;justify-content:flex-end;align-items:center;gap:12px}
.dz .run .c{font-family:var(--fd);letter-spacing:.2em;color:var(--fg)}
@media (max-width:640px){.dz .run{grid-template-columns:1fr auto}.dz .run .c{display:none}}
.dz .head{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(0,.8fr);gap:clamp(24px,4vw,64px);align-items:end;padding-top:clamp(28px,5vh,52px)}
.dz .head .nm{font-family:var(--fd);font-size:clamp(3rem,7vw,6.6rem);line-height:.95;letter-spacing:-.018em;margin-top:18px}
.dz .head .sc{font-family:var(--fi);font-style:italic;font-size:clamp(1.3rem,2vw,1.8rem);color:var(--mute);margin-top:12px}
.dz .head .addr{font-size:13px;letter-spacing:.06em;color:var(--mute);margin-top:18px;display:flex;flex-wrap:wrap;gap:6px 18px}
.dz .head .addr b{font-weight:500;color:var(--fg)}
.dz .head .addr .gm{display:inline-flex;align-items:center;gap:8px;color:var(--acc);letter-spacing:.14em;text-transform:uppercase;font-size:10.5px;font-weight:500;border-bottom:1px solid transparent;transition:.3s}
.dz .head .addr .gm:hover{border-color:var(--acc)}
.dz .head .addr .gm svg{width:12px;height:12px}
.dz .head .pr{text-align:right}
.dz .head .pr .v{font-family:var(--fd);font-size:clamp(1.8rem,3.4vw,3rem);line-height:1;white-space:nowrap}
.dz .head .pr .k{font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute);margin-top:10px}
@media (max-width:760px){.dz .head{grid-template-columns:1fr}.dz .head .pr{text-align:left}}
.plate{position:relative;overflow:hidden;background:var(--panel)}
.plate .pi{position:absolute;inset:-8% 0;will-change:transform;transform:translate3d(0,var(--py,0),0)}
.plate .pi img{width:100%;height:100%;object-fit:cover}
.plate.zoom{cursor:zoom-in}
.plate .cap{position:absolute;left:18px;bottom:16px;right:18px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:rgba(239,231,216,.85);text-shadow:0 1px 10px rgba(0,0,0,.55);display:flex;gap:12px;align-items:center}
.plate .cap::before{content:"";width:5px;height:5px;background:var(--brass-hi);transform:rotate(45deg);flex:none}
.dz .wide{margin-top:clamp(30px,5vh,56px);aspect-ratio:21/9;min-height:320px}
.dz .body{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(32px,5vw,90px);margin-top:clamp(40px,6vh,72px);align-items:start}
.dz .body.split{grid-template-columns:minmax(0,1.05fr) minmax(0,.95fr)}
.dz .body>*,.brief-g>*,.map-g>*,.desk-g>*{min-width:0}
.dz .body .sticky{position:sticky;top:92px}
.dz .body .plate.sp{aspect-ratio:16/11}
.dz .body .plate.tall{aspect-ratio:4/5;max-height:80vh}
.dz .body .plate.sq{aspect-ratio:1/1}
.dz .flip .sticky{order:2}
@media (max-width:900px){.dz .body,.dz .body.split{grid-template-columns:1fr}.dz .body .sticky{position:static;order:0}.dz .body .plate.tall{max-height:none}.dz .wide{aspect-ratio:16/10;min-height:0}}
.facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:0;border-top:1px solid var(--rule);margin:0}
.facts>div{padding:20px 18px 20px 0;border-bottom:1px solid var(--rule-2)}
.facts>div:nth-child(even){padding-left:18px;border-left:1px solid var(--rule-2)}
.facts dt{font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute)}
.facts dd{margin:8px 0 0;font-family:var(--fd);font-size:clamp(1.5rem,2.2vw,2rem);line-height:1}
.facts dd small{font-family:var(--fs);font-size:12px;letter-spacing:.02em;color:var(--mute);margin-left:6px;white-space:normal}
.facts dd small.b{display:block;margin:6px 0 0}
.types-w{margin-top:26px;overflow-x:auto}
.types{width:100%;border-collapse:collapse}
@media (max-width:640px){.types td.p{white-space:normal}.types td,.types th{padding-right:8px}}
.types th{font-size:10.5px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute);font-weight:500;text-align:left;padding:0 12px 12px 0;border-bottom:1px solid var(--rule)}
.types td{padding:14px 12px 14px 0;border-bottom:1px solid var(--rule-2);font-size:14px;vertical-align:top}
.types td.t{font-family:var(--fd);font-size:17px}
.types td.t small{display:block;font-family:var(--fs);font-size:12px;color:var(--mute);margin-top:3px;letter-spacing:.02em}
.types td.p{font-family:var(--fd);font-size:17px;white-space:nowrap;text-align:right;padding-right:0}
.types td.p.off{font-family:var(--fi);font-style:italic;color:var(--mute);font-size:16px}
.types th.p{text-align:right;padding-right:0}
.types td.n{text-align:right;font-variant-numeric:tabular-nums}
.types th.n{text-align:right}
.view{margin-top:34px;border-left:1px solid var(--acc);padding-left:clamp(18px,2vw,28px)}
.view .eyebrow{margin-bottom:14px}
.view p{font-family:var(--fi);font-size:clamp(1.15rem,1.5vw,1.36rem);line-height:1.55;max-width:56ch}
.reco{margin-top:28px;border:1px solid var(--acc);padding:clamp(20px,2.4vw,30px);position:relative;background:linear-gradient(135deg,rgba(184,147,90,.1),transparent 60%)}
.reco::after{content:"";position:absolute;inset:5px;border:1px solid var(--rule-2);pointer-events:none}
.reco .eyebrow{margin-bottom:12px}
.reco .t{font-family:var(--fd);font-size:clamp(1.5rem,2.4vw,2.1rem);line-height:1.15}
.reco p{margin-top:12px;font-size:14px;line-height:1.6;color:var(--mute);max-width:48ch}
.steps{margin-top:22px;display:grid;gap:0;border-top:1px solid var(--rule)}
.steps div{display:grid;grid-template-columns:3ch 1fr;gap:14px;padding:14px 0;border-bottom:1px solid var(--rule-2);font-size:14px;line-height:1.55}
.steps div b{font-family:var(--fd);font-weight:400;color:var(--acc)}
.credits{margin-top:26px;display:grid;gap:6px;font-size:12.5px;color:var(--mute);line-height:1.55}
.credits b{font-weight:500;color:var(--fg)}
.gal-h{display:flex;justify-content:space-between;align-items:baseline;margin-top:clamp(40px,6vh,72px);padding-bottom:14px;border-bottom:1px solid var(--rule);gap:16px;flex-wrap:wrap}
.gal-h .groups{display:flex;gap:8px;flex-wrap:wrap}
.gal-h .groups button{font-size:11px;letter-spacing:.18em;text-transform:uppercase;padding:8px 13px;border:1px solid var(--rule);border-radius:999px;color:var(--mute);transition:.3s}
.gal-h .groups button.on,.gal-h .groups button:hover{color:var(--fg);border-color:var(--acc)}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:10px;margin-top:18px}
.gal figure{margin:0;position:relative;aspect-ratio:4/3;overflow:hidden;background:var(--panel);cursor:zoom-in;border:1px solid var(--rule-2)}
.gal figure.hide{display:none}
.gal figure img{width:100%;height:100%;object-fit:cover;transition:transform 1s var(--ease-o),opacity .6s}
.gal figure:hover img{transform:scale(1.06)}
.gal figure figcaption{position:absolute;left:0;right:0;bottom:0;padding:22px 12px 10px;font-size:10.5px;letter-spacing:.14em;text-transform:uppercase;color:rgba(239,231,216,.9);background:linear-gradient(180deg,transparent,rgba(11,10,8,.7));opacity:0;transition:.4s}
.gal figure:hover figcaption{opacity:1}
.gal figure .g{position:absolute;left:10px;top:9px;font-size:9.5px;letter-spacing:.18em;text-transform:uppercase;color:rgba(239,231,216,.85);background:rgba(11,10,8,.5);padding:4px 8px;border-radius:999px;backdrop-filter:blur(4px)}
.gal figure.plan img{object-fit:contain;background:#fff;padding:6px}
.dz .foot{margin-top:clamp(40px,6vh,64px);padding-top:16px;border-top:1px solid var(--rule);display:flex;justify-content:space-between;gap:16px;font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute);flex-wrap:wrap}
.dz .foot b{font-family:var(--fd);font-weight:400;color:var(--fg);letter-spacing:.2em}

/* diagram */
.diagram{position:relative;border:1px solid var(--rule);background:var(--panel);aspect-ratio:16/11;overflow:hidden}
.diagram svg{width:100%;height:100%;display:block;font-family:var(--fs)}
.diagram .b{fill:none;stroke:var(--acc);stroke-width:.35;stroke-dasharray:1.4 1}
.diagram .hx{fill:url(#hx);stroke:rgba(239,231,216,.4);stroke-width:.25}
.diagram .nw{fill:rgba(230,203,146,.06);stroke:var(--brass-hi);stroke-width:.4;stroke-dasharray:.4 1.2;stroke-linecap:round}
.diagram text{fill:var(--fg);font-size:2.2px;letter-spacing:.2px}
.diagram text.s{font-size:1.9px;fill:var(--mute);text-transform:uppercase;letter-spacing:.35px}
.diagram text.r{fill:var(--brass-hi)}
.diagram .road{stroke:rgba(239,231,216,.25);stroke-width:.3}
.diagram .cap{position:absolute;left:18px;bottom:16px;font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);display:flex;gap:12px;align-items:center}
.diagram .cap::before{content:"";width:5px;height:5px;background:var(--brass);transform:rotate(45deg)}
.pg[data-shade="light"] .diagram .hx{stroke:rgba(26,22,17,.4)}
.pg[data-shade="light"] .diagram .road{stroke:rgba(26,22,17,.3)}

/* desk */
.desk-g{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(36px,6vw,110px);align-items:start;margin-top:clamp(40px,6vh,72px)}
.contacts{display:grid;gap:0;border-top:1px solid var(--rule)}
.contacts a{display:grid;grid-template-columns:1fr auto;align-items:center;gap:16px;padding:18px 0;border-bottom:1px solid var(--rule-2);transition:.3s}
.contacts a:hover{color:var(--acc-hi)}
.contacts .v{font-family:var(--fd);font-size:clamp(1.25rem,1.8vw,1.6rem);letter-spacing:.01em}
.contacts .v small{display:block;font-family:var(--fs);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute);margin-top:5px}
.contacts .chip{color:var(--acc)}
.agent{margin-top:34px;display:grid;grid-template-columns:auto 1fr;gap:18px;align-items:center}
.agent .av{width:54px;height:54px;border-radius:50%;border:1px solid var(--acc);display:grid;place-items:center;font-family:var(--fd);font-size:18px;color:var(--acc)}
.agent b{font-family:var(--fd);font-weight:400;font-size:1.3rem;display:block}
.agent span{font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute)}
.next{display:grid;gap:0;border-top:1px solid var(--rule)}
.next>div{display:grid;grid-template-columns:3ch 1fr;gap:18px;padding:20px 0;border-bottom:1px solid var(--rule-2)}
.next>div b{font-family:var(--fd);font-weight:400;color:var(--acc);font-size:1.1rem}
.next>div h3{font-family:var(--fd);font-size:1.3rem;margin-bottom:6px}
.next>div p{font-size:14px;color:var(--mute);line-height:1.6;max-width:44ch}
.sl-box{margin-top:34px;border:1px solid var(--rule);padding:clamp(20px,2.4vw,28px);background:var(--panel)}
.sl-box .t-3{margin-top:12px}
.sl-box ul{list-style:none;margin:16px 0 0;padding:0;display:grid;gap:0;border-top:1px solid var(--rule-2)}
.sl-box li{display:grid;grid-template-columns:3ch 1fr auto;gap:14px;align-items:center;padding:12px 0;border-bottom:1px solid var(--rule-2);font-size:14px}
.sl-box li .k{font-family:var(--fd);color:var(--acc)}
.sl-box li .rm{font-size:10.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--mute)}
.sl-box li .rm:hover{color:var(--acc-hi)}
.sl-box .empty{margin-top:14px;font-family:var(--fi);font-style:italic;font-size:1.15rem;color:var(--mute)}
.sl-box .send{margin-top:20px;display:flex;gap:12px;flex-wrap:wrap}
.credit-g{margin-top:clamp(56px,8vh,96px);border-top:1px solid var(--rule);padding-top:32px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(24px,3vw,48px);font-size:13px;line-height:1.65;color:var(--mute)}
.credit-g b{display:block;font-family:var(--fs);font-weight:500;font-size:11px;letter-spacing:.22em;text-transform:uppercase;color:var(--fg);margin-bottom:10px}
.credit-g .lg{display:flex;align-items:center;gap:12px;margin-bottom:12px;color:var(--fg)}
.credit-g .lg svg{width:36px;height:36px}
.credit-g .lg span{font-family:var(--fd);font-size:15px;letter-spacing:.04em;line-height:1.15}
.credit-g .lg span small{display:block;font-family:var(--fs);font-size:9.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--mute);margin-top:2px}
.fin{margin-top:clamp(56px,8vh,96px);display:flex;justify-content:space-between;align-items:center;gap:16px;flex-wrap:wrap;font-size:10.5px;letter-spacing:.24em;text-transform:uppercase;color:var(--mute)}
.fin .seal{font-family:var(--fd);color:var(--acc);letter-spacing:.3em}
@media (max-width:900px){.desk-g{grid-template-columns:1fr}.credit-g{grid-template-columns:1fr}}

/* index overlay */
#index{position:fixed;inset:0;top:0;right:0;bottom:0;left:0;overscroll-behavior:contain;-webkit-overflow-scrolling:touch;z-index:150;background:rgba(11,10,8,.97);color:var(--ivory);overflow:auto;opacity:0;visibility:hidden;transition:opacity .6s ease,visibility 0s .6s}
#index.open{opacity:1;visibility:visible;transition:opacity .6s ease}
#index .in{padding:calc(68px + 4vh) var(--gut) 8vh;max-width:1200px;margin-inline:auto}
#index .ih{display:flex;justify-content:space-between;align-items:end;gap:20px;border-bottom:1px solid rgba(239,231,216,.14);padding-bottom:22px}
#index .ih .t-2{margin-top:14px}
#index .close{width:48px;height:48px;border:1px solid rgba(239,231,216,.3);border-radius:50%;display:grid;place-items:center;transition:.3s}
#index .close:hover{border-color:var(--brass);color:var(--brass-hi)}
#index .close svg{width:16px;height:16px}
#index .secs{display:flex;gap:8px;flex-wrap:wrap;margin-top:22px}
#index .secs a{font-size:11px;letter-spacing:.18em;text-transform:uppercase;padding:9px 14px;border:1px solid rgba(239,231,216,.2);border-radius:999px;transition:.3s}
#index .secs a:hover{border-color:var(--brass);color:var(--brass-hi)}
#index .rows{margin-top:26px;display:grid}
#index .rows a{display:grid;grid-template-columns:3ch 84px 1fr auto auto;gap:18px;align-items:center;padding:14px 0;border-bottom:1px solid rgba(239,231,216,.08);transition:.3s;opacity:0;transform:translateY(10px)}
#index.open .rows a{opacity:1;transform:none;transition:opacity .6s ease,transform .7s var(--ease-o)}
#index .rows a:hover{color:var(--brass-hi)}
#index .rows .k{font-family:var(--fd);color:var(--brass)}
#index .rows .th{width:84px;height:56px;overflow:hidden;background:var(--umber)}
#index .rows .th img{width:100%;height:100%;object-fit:cover}
#index .rows .th .dg{width:100%;height:100%;display:grid;place-items:center;color:var(--brass)}
#index .rows .th .dg svg{width:60%}
#index .rows .nm{font-family:var(--fd);font-size:1.3rem}
#index .rows .nm small{display:block;font-family:var(--fs);font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--ash);margin-top:4px}
#index .rows .pr{font-family:var(--fd);white-space:nowrap}
@media (max-width:640px){#index .rows a{grid-template-columns:3ch 1fr auto}#index .rows .th,#index .rows .pr{display:none}}

/* lightbox */
#lb{position:fixed;inset:0;top:0;right:0;bottom:0;left:0;overscroll-behavior:contain;touch-action:none;z-index:170;background:rgba(6,5,4,.96);color:var(--ivory);opacity:0;visibility:hidden;transition:opacity .5s ease,visibility 0s .5s;display:grid;grid-template-rows:auto 1fr auto}
#lb.open{opacity:1;visibility:visible;transition:opacity .5s ease}
#lb .bar{display:flex;justify-content:space-between;align-items:center;padding:18px var(--gut);font-size:11px;letter-spacing:.2em;text-transform:uppercase;color:var(--ash)}
#lb .bar b{font-family:var(--fd);font-weight:400;color:var(--ivory);letter-spacing:.14em}
#lb .bar .x{display:flex;gap:8px}
#lb .bar button{width:44px;height:44px;border:1px solid rgba(239,231,216,.25);border-radius:50%;display:grid;place-items:center;transition:.3s}
#lb .bar button:hover{border-color:var(--brass);color:var(--brass-hi)}
#lb .bar button svg{width:16px;height:16px}
#lb .st{position:relative;overflow:hidden;touch-action:none}
#lb .st img{position:absolute;inset:0;top:0;right:0;bottom:0;left:0;width:100%;height:100%;object-fit:contain;opacity:0;transition:opacity .5s ease;user-select:none;-webkit-user-drag:none;transform-origin:center}
#lb .st img.on{opacity:1}
#lb.zoomed .st img.on{cursor:grab}
#lb .nav{position:absolute;top:50%;transform:translateY(-50%);width:54px;height:54px;border:1px solid rgba(239,231,216,.25);border-radius:50%;display:grid;place-items:center;background:rgba(11,10,8,.4);transition:.3s;z-index:2}
#lb .nav:hover{border-color:var(--brass);color:var(--brass-hi)}
#lb .nav.p{left:clamp(12px,3vw,40px)}#lb .nav.n{right:clamp(12px,3vw,40px)}
#lb .nav svg{width:18px;height:18px}
#lb .cap{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:16px var(--gut) 22px;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--ash);flex-wrap:wrap}
#lb .cap .c{color:var(--ivory)}
#lb .cap .k{font-family:var(--fd);color:var(--brass);letter-spacing:.2em}
@media (max-width:640px){#lb .nav{display:none}}

/* cursor */
.cur{position:fixed;left:0;top:0;z-index:400;pointer-events:none;width:10px;height:10px;border-radius:50%;background:var(--brass-hi);transform:translate(-50%,-50%);mix-blend-mode:difference;display:none}
.cur2{position:fixed;left:0;top:0;z-index:399;pointer-events:none;width:36px;height:36px;border-radius:50%;border:1px solid rgba(230,203,146,.7);transform:translate(-50%,-50%);transition:width .3s,height .3s,background .3s,opacity .3s;display:none;place-items:center;font-size:9px;letter-spacing:.2em;text-transform:uppercase;color:var(--onyx);font-weight:600}
.cur2.big{width:74px;height:74px;background:rgba(230,203,146,.92);border-color:transparent}
.cur2.big::after{content:"View"}
@media (pointer:fine) and (min-width:900px){.cur,.cur2{display:grid}body{cursor:none}a,button,.gal figure,.plate.zoom,.shelf{cursor:none}}

@media (hover:none){
  body::before{display:none}
  .top{mix-blend-mode:normal;color:var(--ivory);background:linear-gradient(180deg,rgba(11,10,8,.85) 0%,rgba(11,10,8,.55) 55%,rgba(11,10,8,0) 100%);height:76px}
  .tabs{display:none}
  .plate .pi{inset:0;transform:none!important;will-change:auto}
  .ticker{backdrop-filter:none;-webkit-backdrop-filter:none;background:rgba(11,10,8,.82)}
  .gal figure .g,.card .pl .chip{backdrop-filter:none;-webkit-backdrop-filter:none;background:rgba(11,10,8,.72)}
  .gal figure img,.card .pl img{transition:none}
  .lm-hint{display:none}
  #lb{background:#060504}
}
@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;transition-duration:.01ms!important;transition-delay:0s!important;scroll-behavior:auto!important}
  .rv,.rv-stag>*,.wipe,.w-back span,.w-name .ch,.w-eye,.w-sub,.w-cta,.w-line,.ticker,.top,.tabs,#welcome .meta,#welcome .bg img{opacity:1!important;transform:none!important;filter:none!important;clip-path:none!important}
  #veil{display:none}
}
@media print{#veil,.top,.tabs,.progress,.cur,.cur2,#index,#lb,.ticker{display:none!important}.pg{padding-block:40px}.rv,.rv-stag>*,.wipe,.w-back span,.w-name .ch{opacity:1!important;transform:none!important;clip-path:none!important}}
"""

# ---------------------------------------------------------------- markup helpers
MARK = '<svg viewBox="0 0 100 100" aria-hidden="true"><circle cx="48" cy="46" r="44" fill="currentColor"/><g fill="var(--onyx)"><rect x="18" y="22" width="11" height="48"/><rect x="67" y="22" width="11" height="48"/><path d="M29 22h11l8 18-6 12z"/><path d="M67 22H56l-8 18 6 12z"/></g><rect x="66" y="72" width="32" height="12" fill="currentColor" transform="rotate(45 82 78)"/></svg>'
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.5c.9 5.6 3.9 8.6 9.5 9.5-5.6.9-8.6 3.9-9.5 9.5-.9-5.6-3.9-8.6-9.5-9.5 5.6-.9 8.6-3.9 9.5-9.5z"/></svg>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M4 12h16M13 5l7 7-7 7"/></svg>'
CHEV_L = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M15 5l-7 7 7 7"/></svg>'
CHEV_R = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M9 5l7 7-7 7"/></svg>'
CLOSE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><path d="M5 5l14 14M19 5L5 19"/></svg>'
ZOOM = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="M16 16l5 5M11 8v6M8 11h6"/></svg>'
FLOURISH = '<svg viewBox="0 0 150 40" fill="none" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" aria-hidden="true"><path d="M3 30c14-18 26-22 30-14 3 6-6 14-9 9-2-5 12-20 26-20 10 0 7 16 16 16 8 0 10-14 18-14 7 0 6 12 12 12 8 0 12-16 22-16 8 0 10 8 18 8 5 0 8-3 12-6"/></svg>'

def esc(s): return H.escape(s, quote=True)

_DIM = {}
def dim(name):
    if name not in _DIM:
        from PIL import Image
        try: _DIM[name] = Image.open(os.path.join(ROOT, "assets", name)).size
        except Exception: _DIM[name] = None
    return _DIM[name]

def img(name, alt, sizes, extra=""):
    """<img> for an asset; JPEGs get a 1400 px phone edition in srcset (assets/m/), PNG plans do not."""
    if name.endswith(".jpg") and dim(name):
        w = dim(name)[0]
        return f'<img src="assets/{name}" srcset="assets/m/{name} 1400w, assets/{name} {w}w" sizes="{sizes}" alt="{alt}" decoding="async" {extra}>'
    return f'<img src="assets/{name}" alt="{alt}" decoding="async" {extra}>'

def name_markup(text):
    words = []
    i = 0
    for w in text.split(" "):
        chars = "".join(f'<span class="ch" style="--i:{i+k}">{esc(c)}</span>' for k, c in enumerate(w))
        i += len(w) + 1
        words.append(f'<span class="w" aria-hidden="true">{chars}</span>')
    return "".join(words)

def chip(status): return f'<span class="chip" data-s="{esc(status)}"><i></i>{esc(status)}</span>'

def star(site): return f'<button class="star" type="button" data-id="{site["id"]}" aria-pressed="false" aria-label="Add {esc(site["name"])} to your shortlist" title="Shortlist">{STAR}</button>'

def diagram_svg(cls="diagram"):
    return f'''<div class="{cls}" aria-label="Illustrative plot diagram for Mississippi Street">
<svg viewBox="0 0 100 68" role="img">
 <defs><pattern id="hx" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="rgba(184,147,90,.55)" stroke-width=".25"/></pattern></defs>
 <line class="road" x1="4" y1="60" x2="96" y2="60"/><line class="road" x1="4" y1="63" x2="96" y2="63"/>
 <text class="s" x="50" y="66.6" text-anchor="middle">Mississippi Street</text>
 <path class="b" d="M16 8 L84 8 L86 54 L14 54 Z"/>
 <text class="s" x="16" y="6">Plot boundary · indicative</text>
 <rect class="hx" x="30" y="20" width="34" height="22"/>
 <text x="47" y="29.5" text-anchor="middle">Existing house</text>
 <text class="s" x="47" y="33.2" text-anchor="middle">5 bedrooms · to be cleared</text>
 <rect class="hx" x="68" y="14" width="12" height="9"/>
 <text class="s" x="74" y="27" text-anchor="middle">Guest chalet</text>
 <path class="nw" d="M20 13 L80 13 L80 50 L20 50 Z"/>
 <text class="r" x="22" y="47.6">Proposed new residence</text>
 <text class="s" x="22" y="51" style="fill:var(--brass-hi);opacity:.8">to your brief · footprint indicative</text>
 <g transform="translate(90 44)"><circle r="3.2" fill="none" stroke="rgba(239,231,216,.35)" stroke-width=".25"/><path d="M0-2.6 L1 1 L0 .2 L-1 1 Z" fill="var(--brass)"/><text class="s" y="6.2" text-anchor="middle">N</text></g>
</svg>
<div class="cap">Illustrative diagram · not a survey · not to scale</div></div>'''

# ---------------------------------------------------------------- sections
def welcome():
    hero_img = img("cova-corner.jpg", "", "100vw", 'fetchpriority="high"')
    addresses = " ".join(f'<span>{esc(s["name"])} · {esc(s["district"])}</span>' for s in SITES)
    return f'''
<section id="welcome" aria-label="Welcome">
  <div class="bg">{hero_img}</div>
  <div class="meta"><span>Mizan Qist Limited · Private client</span><span class="mono">Confidential · {esc(DATE)}</span></div>
  <div class="stage">
    <div class="eyebrow w-eye">Private portfolio · Abuja · Ten addresses</div>
    <div class="w-back" aria-hidden="true">{"".join(f"<span>{esc(w)}</span>" for w in CLIENT_GREETING.split(" "))}</div>
    <h1 class="w-name" id="wname"><span class="sr">{esc(CLIENT_GREETING)} {esc(CLIENT_SHORT)}</span>{name_markup(CLIENT_SHORT)}</h1>
    <div class="w-line"></div>
    <p class="w-sub">Your portfolio is ready: ten addresses, sourced and prepared for you by Mizan Qist. Nine in Abuja, one in Lagos, each with its prices, the state of the site, and our view.</p>
    <div class="w-cta"><a class="btn-ring" href="#brief">Open the portfolio {ARROW}</a><div class="w-scroll"><i></i>Scroll</div></div>
  </div>
  <div class="ticker" aria-hidden="true"><div class="row">{addresses}{addresses}</div></div>
</section>'''

def brief():
    return f'''
<section class="pg" id="brief" data-shade="light" aria-label="Your brief">
 <div class="wrap brief-g">
  <div class="lhs rv"><div class="eyebrow">Your brief</div><h2 class="t-2">Ten addresses,<br>one file.</h2><p class="small">Compiled {esc(DATE)} · Prices as quoted by the developers and owners · Confidential, prepared for {esc(CLIENT)}</p></div>
  <div class="letter rv-stag">
    <p class="sal">{esc(CLIENT_SALUTATION)}</p>
    <p>We have sourced and compiled the ten addresses in this file. Nine are in the capital: four in Maitama, and one each in Wuse II, Katampe Extension, Mabushi District, Guzape and Asokoro. The tenth, Cova Manor in Victoria Island, Lagos, we include for a base of matching quality outside the capital.</p>
    <p>Each dossier carries the address, the house types and prices as quoted to us, the state of the site where we have photographed it, the concept where drawings exist, and our view. Off-plan prices are as at {esc(DATE)} and subject to the developer's confirmation. Where we recommend a course of action we say so plainly; Mississippi Street is one such case.</p>
    <p>Your desk is open at any hour. Mark the addresses that interest you and we will arrange viewings and drawings in the order you prefer.</p>
    <div class="sig">{FLOURISH}<b>Sadiq Babalele</b><span>For Mizan Qist Limited · Real Estate Advisory</span></div>
  </div>
 </div>
 <div class="wrap"><div class="terms rv-stag">
   <div><div class="k">{chip("Ready")}{chip("Selling")}{chip("Off-plan")}</div><h3>Status</h3><p>Ready: complete, and can be viewed and occupied. Selling: on the market while construction continues. Off-plan: sold from the drawings, before or during early works, at pre-completion prices.</p></div>
   <div><h3>Carcass</h3><p>A home sold structurally complete but unfinished inside: walls, roof, windows and services in place, with the finishes, joinery and fittings left to the buyer's own specification, at a lower price.</p></div>
   <div><h3>BQ</h3><p>Boys' quarters: separate staff accommodation within the plot, usually with its own bath. "1 BQ" is one staff room; "2 BQ", two.</p></div>
 </div></div>
</section>'''

LANDMARKS = [
 dict(id="cbd", n="Central Business District", s="Central Bank of Nigeria, Tafawa Balewa Way", ll=[9.0508926, 7.4929880], city="Abuja", dest=True),
 dict(id="hilton", n="Transcorp Hilton", s="Zambezi Crescent, Maitama", ll=[9.074966, 7.494881], city="Abuja"),
 dict(id="assembly", n="National Assembly", s="Three Arms Zone", ll=[9.068124, 7.511193], city="Abuja"),
 dict(id="wuse", n="Wuse Market", s="Wuse Market Road", ll=[9.068555, 7.465938], city="Abuja"),
 dict(id="jabi", n="Jabi Lake Mall", s="Jabi", ll=[9.076275, 7.42548], city="Abuja"),
 dict(id="aso", n="Aso Rock", s="The Presidential Villa below it", ll=[9.08039, 7.536039], city="Abuja"),
 dict(id="eko", n="Eko Hotel & Suites", s="Adetokunbo Ademola Street, Victoria Island", ll=[6.427074, 3.430286], city="Lagos", dest=True),
]
ROUTES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "routes.json")))

def map_data():
    return [dict(id=x["id"], n=x["n"], name=x["name"], addr=x["addr"], price=x["price"], status=x["status"], ll=list(x["ll"]) if x["ll"] else None, gmaps=x["gmaps"], approx=x["approx"], city=x["city"], district=x["district"], route=ROUTES.get(x["id"])) for x in SITES]

def glance():
    n_sell = sum(1 for x in SITES if x["status"] == "Selling"); n_off = sum(1 for x in SITES if x["status"] == "Off-plan")
    assert n_sell + n_off == len(SITES), "a status other than Selling / Off-plan needs its own tile"
    ORDER = ["Maitama", "Wuse II", "Katampe Ext.", "Mabushi District", "Guzape", "Asokoro", "Victoria Island, Lagos"]
    groups = [(g, []) for g in ORDER]
    for x in SITES:
        g = x["district"] + (", Lagos" if x["city"] == "Lagos" else "")
        dict(groups)[g].append(x)
    panel = ""
    for g, items in groups:
        rows = ""
        for x in items:
            r = ROUTES.get(x["id"], {})
            dist = f'<span class="dist"><b>{r["km"]}</b> km · <b>{r["min"]}</b> min</span>' if r else '<span class="dist">—</span>'
            rows += f'<button type="button" class="mrow" data-m="{x["id"]}" aria-pressed="false"><span class="k">{x["n"]}</span><span class="t">{esc(x["name"])}<small>{esc(x["addr"])}{" · approximate" if x["approx"]=="district" else " · nearest pin" if x["approx"]=="nearest" else ""}</small></span>{dist}</button>'
        panel += f'<div class="lm-grp"><div class="lm-gh"><span>{esc(g)}</span><span>{len(items)} {"address" if len(items)==1 else "addresses"}</span></div>{rows}</div>'
    fallback = "".join(f'<a href="{esc(x["gmaps"])}" target="_blank" rel="noopener"><span class="k">{x["n"]}</span><span>{esc(x["name"])}<small>{esc(x["addr"])}</small></span><span class="d">Google Maps</span></a>' for x in SITES)
    return f'''
<section class="pg" id="glance" aria-label="At a glance">
 <div class="wrap">
  <div class="rv"><div class="eyebrow">At a glance</div><h2 class="t-2" style="margin-top:18px">Ten addresses. Seven districts. Two cities.</h2></div>
  <div class="stats rv-stag" style="margin-top:clamp(36px,5vh,56px)">
    <div><div class="v num"><span data-count="10">10</span></div><div class="k">Addresses</div></div>
    <div><div class="v num"><span data-count="7">7</span></div><div class="k">Districts</div></div>
    <div><div class="v rng">₦350m<small>to</small> ₦6.6bn</div><div class="k">Price range</div></div>
    <div><div class="v num"><span data-count="{n_sell}">{n_sell}</span><small>·</small><span data-count="{n_off}">{n_off}</span></div><div class="k">Selling · off-plan</div></div>
  </div>
  <div class="map-h rv"><div><div class="eyebrow">The map</div><h3 class="t-3">Every address, and the drive to the centre, <em class="t-i">on one map.</em></h3></div>
   <div class="map-ctl"><div class="seg" role="group" aria-label="Map layer"><button type="button" data-layer="streets" aria-pressed="true">Streets</button><button type="button" data-layer="aerial" aria-pressed="false">Aerial</button></div><div class="seg" role="group" aria-label="View"><button type="button" data-city="Maitama" aria-pressed="false">Maitama</button><button type="button" data-city="Abuja" aria-pressed="true">Abuja</button><button type="button" data-city="Lagos" aria-pressed="false">Lagos</button></div></div></div>
  <div class="map-g">
   <div class="lmap-wrap night rv" id="lmapwrap"><div id="lmap" aria-label="Interactive map of the ten addresses"></div><div class="lm-hint" id="lmhint">Click the map, then scroll to zoom</div>
    <div class="map-fb" id="mapfb" hidden><div class="eyebrow plain">Map</div><p>The map could not load here. Each address opens in Google Maps:</p><div class="fbrows">{fallback}</div></div></div>
   <div class="lm-panel rv" id="mrows">{panel}<div class="lm-note">Distances are by road to the Central Business District (the Central Bank of Nigeria on Tafawa Balewa Way), routed on OpenStreetMap; Cova Manor is measured to the Eko Hotel. Drive times are approximate and off-peak. Choose a row to fly to the address and draw its route.</div></div>
  </div>
  {ledger()}
 </div>
</section>'''

STATUS_ORDER = {"Ready": 0, "Selling": 1, "Off-plan": 2}
def ledger():
    rows = ""
    for s in SITES:
        types = " · ".join(t[0] for t in s["types"])
        price_sort = s["pmin"] if s["pmin"] else 99999
        availcell = "" if s["avail"]=="—" else '<span class="small"> · ' + esc(s["avail"]) + ' avail.</span>'
        rows += f'''<tr data-go="{s["id"]}" data-n="{s["n"]}" data-price="{price_sort}" data-status="{STATUS_ORDER[s["status"]]}">
<td class="k">{s["n"]}</td><td class="nm">{esc(s["name"])}<small>{esc(s["addr"])}</small></td>
<td>{esc(types)}</td><td class="num">{esc(s["beds"])}</td><td class="num">{s.get("homes_cell") or (esc(s["units"]) + availcell)}</td><td class="pr">{esc(s["price"])}</td><td>{chip(s["status"])}</td><td class="vw">{esc(s["short"])}</td><td class="star-c st">{star(s)}</td></tr>'''
    return f'''
  <div class="ledger-h rv"><div><div class="eyebrow">The ledger</div><h2 class="t-2">Every address on one page.</h2></div>
   <div class="sorts" role="group" aria-label="Sort the ledger"><button type="button" class="on" data-sort="n">In order</button><button type="button" data-sort="price">By price</button><button type="button" data-sort="status">By status</button></div></div>
  <div class="ledger-w rv"><table class="ledger" id="ledger"><thead><tr><th>No.</th><th>Address</th><th>House types</th><th>Beds</th><th>Homes</th><th>Price</th><th>Status</th><th>In a line</th><th class="st">Shortlist</th></tr></thead><tbody>{rows}</tbody></table></div>'''

def shelf():
    cards = ""
    for s in SITES:
        hero = s["hero"][0]
        pl = img(hero + ".jpg", esc(s["name"]), "(max-width:900px) 70vw, 24vw", 'loading="lazy"') if hero else '<div class="dg">' + diagram_mini() + '</div>'
        cards += f'''<a class="card" href="#{s["id"]}" data-go="{s["id"]}"><div class="pl">{pl}<span class="k">{s["n"]}</span>{chip(s["status"])}</div>
<div class="nm">{esc(s["name"])}<small>{esc(s["district"])}{", Lagos" if s["city"]=="Lagos" else ""}</small></div><div class="pr"><span>{esc(s["short"])}</span><b>{esc(s["price"])}</b></div></a>'''
    return f'''
<section class="pg" id="collection" data-shade="light" aria-label="The collection">
 <div class="wrap">
  <div class="shelf-h rv"><div><div class="eyebrow">The collection</div><h2 class="t-2">Ten dossiers, in order.</h2></div><div class="arrows"><button type="button" data-shelf="-1" aria-label="Scroll the collection left">{CHEV_L}</button><button type="button" data-shelf="1" aria-label="Scroll the collection right">{CHEV_R}</button></div></div>
  <div class="shelf rv" id="shelf">{cards}</div>
 </div>
</section>'''

def diagram_mini():
    return '<svg viewBox="0 0 100 68" aria-hidden="true"><defs><pattern id="hx2" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="1.6" stroke="rgba(184,147,90,.6)" stroke-width=".25"/></pattern></defs><path d="M16 8 L84 8 L86 54 L14 54 Z" fill="none" stroke="#b8935a" stroke-width=".4" stroke-dasharray="1.4 1"/><rect x="30" y="20" width="34" height="22" fill="url(#hx2)" stroke="rgba(239,231,216,.4)" stroke-width=".25"/><path d="M20 13 L80 13 L80 50 L20 50 Z" fill="none" stroke="#e6cb92" stroke-width=".45" stroke-dasharray=".4 1.2" stroke-linecap="round"/></svg>'

def facts_html(s):
    out = ""
    for k, v, u in s["facts"]:
        unit = f'<small>{esc(u)}</small>' if u and len(u) <= 6 else (f'<small class="b">{esc(u)}</small>' if u else "")
        out += f'<div><dt>{esc(k)}</dt><dd>{esc(v)}{unit}</dd></div>'
    return f'<dl class="facts">{out}</dl>'

def types_html(s):
    rows = ""
    for name, spec, size, avail, price in s["types"]:
        off = price in ("Sold out", "Not listed", "On application")
        rows += f'<tr><td class="t">{esc(name)}<small>{esc(spec)}</small></td><td>{esc(size) or "—"}</td><td class="n">{esc(avail) or "—"}</td><td class="p{" off" if off else ""}">{esc(price)}</td></tr>'
    return f'<div class="types-w"><table class="types"><thead><tr><th>Type</th><th>Size</th><th class="n">Available</th><th class="p">Price</th></tr></thead><tbody>{rows}</tbody></table></div>'

def credits_html(s):
    lines = []
    if s["dev"]: lines.append(f'<span><b>Developer</b> · {esc(s["dev"])}</span>')
    if s["arch"]: lines.append(f'<span><b>Architect</b> · {esc(s["arch"])}</span>')
    src = "Mizan Qist residential portfolio, August 2026"
    if s["name"] == "Maitama View": src += "; Maitama View brochure and working drawings; gate design drawings, September 2026"
    if s["name"] == "Cova Manor": src += "; Cova Manor brochure and construction documentation"
    if s["name"] == "Heights 777": src += "; Heights 777 brochure and drawings"
    lines.append(f'<span><b>Source</b> · {esc(src)}</span>')
    return f'<div class="credits">{"".join(lines)}</div>'

def plate_html(s, cls):
    src, kind, cap = s["hero"]
    sizes = "100vw" if cls == "wide" else "(max-width:900px) 100vw, 55vw"
    tag = img(src + ".jpg", esc(cap), sizes, 'loading="lazy"')
    return f'<div class="plate {cls} zoom wipe" data-lb="{s["id"]}" data-src="assets/{src}.jpg" role="button" tabindex="0" aria-label="Open the visualisation of {esc(s["name"])}"><div class="pi">{tag}</div><div class="cap">{esc(cap)}</div></div>'

def gallery_html(s):
    if not s["gallery"]: return ""
    groups = []
    for g, _, _ in s["gallery"]:
        if g not in groups: groups.append(g)
    figs = ""
    for g, src, cap in s["gallery"]:
        plan = " plan" if src.startswith("cova-plan") or src in ("kat-plan2",) else ""
        ext = "png" if src.startswith("cova-plan") else "jpg"
        tag = img(src + "." + ext, esc(cap), "(max-width:900px) 46vw, 14vw", 'loading="lazy"')
        figs += f'<figure class="gi{plan}" data-g="{esc(g)}" data-lb="{s["id"]}" data-src="assets/{src}.{ext}" data-cap="{esc(cap)}" tabindex="0" role="button" aria-label="Open {esc(cap)}">{tag}<span class="g">{esc(g)}</span><figcaption>{esc(cap)}</figcaption></figure>'
    btns = '<button type="button" class="on" data-g="*">All</button>' + "".join(f'<button type="button" data-g="{esc(g)}">{esc(g)}</button>' for g in groups)
    n = len(s["gallery"])
    return f'<div class="gal-h rv"><div class="eyebrow">Plates · {n} {"view" if n==1 else "views"}</div><div class="groups" role="group" aria-label="Filter the plates">{btns}</div></div><div class="gal rv-stag">{figs}</div>'

def dossier(s, shade, flip):
    n = s["n"]; kind = s["hero"][1]
    availtxt = "Availability on request" if s["avail"]=="—" else "<b>" + esc(s["avail"]) + "</b> available"
    head = f'''<div class="head rv-stag">
    <div><div class="eyebrow">{esc(s["street"])}{(" · " + esc(s["plot"])) if s["plot"] else ""}</div><h2 class="nm">{esc(s["name"])}</h2>{f'<p class="sc">{esc(s["scheme"])}</p>' if s["scheme"] else ""}
      <div class="addr"><span><b>{esc(s["addr"])}</b></span>{s.get("units_line") and f'<span>{s["units_line"]}</span>' or f'<span><b>{esc(s["units"])}</b> {"home" if s["units"]=="1" else "homes"} in the scheme</span><span>{availtxt}</span>'}<a class="gm" href="{esc(s["gmaps"])}" target="_blank" rel="noopener">Open in Google Maps{" · nearest pin" if s["approx"]=="nearest" else " · street" if s["approx"]=="street" else " · district, approximate" if s["approx"]=="district" else ""} {ARROW}</a></div></div>
    <div class="pr"><div class="v">{esc(s["price"])}</div><div class="k">{"Price band" if "–" in s["price"] else "Price"} · {esc(s["beds"])} bedrooms</div></div></div>'''
    left = facts_html(s) + types_html(s)
    view = f'<div class="view"><div class="eyebrow">Our view</div><p>{esc(s["view"])}</p></div>'
    if s["name"] == "Mississippi":
        view += '''<div class="reco rv"><div class="eyebrow">Recommendation</div><div class="t">Best use: demolition and new construction.</div><p>Buy the plot for its street and its ground. Clear the existing house and chalet, and build a new residence to your brief, rather than renovate a building that has reached the end of its life. Mizan Qist is in construction and can take on the project, from design to handover.</p></div>
<div class="steps"><div><b>I</b><span>A private viewing, arranged with the owner's consent and at a time of his choosing.</span></div><div><b>II</b><span>A survey of the plot and a search of the title before any offer.</span></div><div><b>III</b><span>A concept design for the new residence, so that the purchase and the build are priced together.</span></div></div>'''
    right = view + credits_html(s)
    if kind == "wide":
        body = f'{plate_html(s, "wide")}<div class="body"><div class="rv">{left}</div><div class="rv">{right}</div></div>'
    elif kind == "diagram":
        body = f'<div class="body split{" flip" if flip else ""}"><div class="sticky rv">{diagram_svg()}</div><div class="rv">{left}{right}</div></div>'
    else:
        pcls = {"split": "sp", "tall": "tall"}.get(kind, "sp")
        if s["name"] == "Cova Manor": pcls = "sq"
        body = f'<div class="body split{" flip" if flip else ""}"><div class="sticky">{plate_html(s, pcls)}</div><div class="rv">{left}{right}</div></div>'
    return f'''
<section class="pg dz" id="{s["id"]}" data-shade="{shade}" data-n="{n}" data-name="{esc(s["name"])}" aria-label="Dossier {n}, {esc(s["name"])}">
 <div class="wrap">
  <div class="run rv"><div>Dossier {n} / 10</div><div class="c">{esc(s["district"])} · {esc(s["city"])}</div><div class="r">{chip(s["status"])}{star(s)}</div></div>
  {head}
  {body}
  {gallery_html(s)}
  <div class="foot"><span>Prepared for {esc(CLIENT)} · Mizan Qist Limited</span><span><b>{n}</b> / 10</span></div>
 </div>
</section>'''

def desk():
    return f'''
<section class="pg" id="desk" aria-label="Your desk">
 <div class="wrap">
  <div class="rv"><div class="eyebrow">Your desk</div><h2 class="t-2">Open at any hour.</h2><p class="lede" style="margin-top:22px;color:var(--mute)">Everything in this file can be set in motion with one message: a private viewing, the full drawings, or a valuation. {esc(AGENT)} holds your file.</p></div>
  <div class="desk-g">
   <div class="rv">
    <div class="contacts">
     <a href="https://wa.me/message/CL4UJVGMQEHBK1?src=qr" target="_blank" rel="noopener"><span class="v">+44 7931 814601<small>Mizan Qist · United Kingdom</small></span><span class="chip">WhatsApp</span></a>
     <a href="tel:+2348086666206"><span class="v">+234 808 6666 206<small>Mizan Qist · Abuja</small></span><span class="chip">Call now</span></a>
     <a href="mailto:mizanqistltd@gmail.com?subject={urllib.parse.quote("Portfolio for " + CLIENT)}"><span class="v">mizanqistltd@gmail.com<small>Email</small></span><span class="chip">Write</span></a>
     <a href="https://www.instagram.com/mizanqistltd?stkn=MTNvcmwzc2F5MjVvMQ%3D%3D&amp;utm_source=qr" target="_blank" rel="noopener"><span class="v">@mizanqistltd<small>Instagram</small></span><span class="chip">Follow</span></a>
    </div>
    <div class="agent"><div class="av">SB</div><div><b>{esc(AGENT)}</b><span>Your agent · Mizan Qist Limited · Abuja</span></div></div>
   </div>
   <div class="rv">
    <div class="next">
     <div><b>I</b><div><h3>Mark your shortlist</h3><p>Use the star on any dossier or ledger row. Your selection is kept on this device and listed below.</p></div></div>
     <div><b>II</b><div><h3>We arrange the viewings</h3><p>Site visits and walk-throughs of the drawings, in the order you prefer and at the hours that suit you.</p></div></div>
     <div><b>III</b><div><h3>We negotiate and complete</h3><p>Offers, title checks, contracts and, where you choose carcass or new build, the design and finishing to follow.</p></div></div>
    </div>
    <div class="sl-box" id="slbox"><div class="eyebrow">Your shortlist</div><h3 class="t-3">Addresses you have marked.</h3><ul id="sllist"></ul><p class="empty" id="slempty">Nothing marked yet. Star a dossier to add it here.</p>
     <div class="send"><a class="btn-ring" id="slsend" href="https://wa.me/447931814601" target="_blank" rel="noopener">Send the shortlist to Sadiq {ARROW}</a></div></div>
   </div>
  </div>
  <div class="credit-g rv-stag">
   <div><div class="lg">{MARK}<span>Mizan Qist Limited<small>Where ideas become reality</small></span></div><p>Compiled by the Real Estate Advisory department of Mizan Qist Limited, Abuja, {esc(DATE)}. Agent: {esc(AGENT)}.</p></div>
   <div><b>Sources</b><p>Prices, unit counts and statuses as quoted to Mizan Qist by the developers and owners, August and September 2026. Site photography by Mizan Qist, including drone photography of 22 August 2026. Visualisations and plans supplied by the developers and their architects; Maitama View and Cova Manor facts from their working drawings and construction documentation, July 2026.</p></div>
   <div><b>Confidential</b><p>Prepared for {esc(CLIENT)} and not for onward circulation. Visualisations are artists' impressions. Areas are indicative. Prices are subject to confirmation and to contract; nothing here forms part of an offer or contract.</p></div>
  </div>
  <div class="fin"><span>Prepared for {esc(CLIENT)} · Confidential · {esc(DATE)}</span><span class="seal">Mizan Qist · MQL</span></div>
 </div>
</section>'''

def chrome():
    tabs = "".join(f'<button type="button" data-go="{s["id"]}"><span class="l">{esc(s["name"])}</span><span class="k">{s["n"]}</span><i></i></button>' for s in SITES)
    rows = ""
    for s in SITES:
        hero = s["hero"][0]
        th = img(hero + ".jpg", "", "84px", 'loading="lazy"') if hero else '<div class="dg">' + diagram_mini() + '</div>'
        rows += f'<a href="#{s["id"]}" data-go="{s["id"]}"><span class="k">{s["n"]}</span><span class="th">{th}</span><span class="nm">{esc(s["name"])}<small>{esc(s["district"])}{", Lagos" if s["city"]=="Lagos" else ""} · {esc(s["status"])}</small></span><span class="pr">{esc(s["price"])}</span>{chip(s["status"])}</a>'
    return f'''
<div id="veil" aria-hidden="true"><div class="mark">{MARK}</div><div class="vt">Preparing your portfolio</div><div class="bar"><i id="vbar"></i></div><div class="ct" id="vct">00</div></div>
<header class="top">
  <a class="brand" href="#welcome" data-go="welcome">{MARK}<span><b>Mizan Qist</b><small>Private client</small></span></a>
  <div class="ttl">The <em>{esc(CLIENT_SURNAME)}</em> Portfolio</div>
  <div class="acts"><button type="button" class="btn sl" data-go="desk" aria-label="Your shortlist"><span class="n" id="slcount"></span>Shortlist</button><button type="button" class="btn" id="idxbtn" aria-haspopup="dialog" aria-controls="index">Index</button></div>
</header>
<nav class="tabs" aria-label="Dossiers"><button type="button" class="sec" data-go="brief"><span class="l">Your brief</span><span class="k">Brief</span><i></i></button><button type="button" class="sec" data-go="collection"><span class="l">The collection</span><span class="k">All</span><i></i></button><button type="button" class="sec" data-go="glance"><span class="l">Map &amp; ledger</span><span class="k">Map</span><i></i></button>{tabs}<button type="button" class="sec" data-go="desk"><span class="l">Your desk</span><span class="k">Desk</span><i></i></button></nav>
<div class="progress" aria-hidden="true"><i id="pbar"></i></div>
<div id="index" role="dialog" aria-modal="true" aria-label="Index"><div class="in">
  <div class="ih"><div><div class="eyebrow">Index</div><h2 class="t-2">The ten dossiers.</h2></div><button type="button" class="close" id="idxclose" aria-label="Close the index">{CLOSE}</button></div>
  <div class="secs"><a href="#welcome" data-go="welcome">Welcome</a><a href="#brief" data-go="brief">Your brief</a><a href="#collection" data-go="collection">The collection</a><a href="#glance" data-go="glance">Map &amp; ledger</a><a href="#desk" data-go="desk">Your desk</a></div>
  <div class="rows">{rows}</div>
</div></div>
<div id="lb" role="dialog" aria-modal="true" aria-label="Plate viewer"><div class="bar"><span><b id="lbsite"></b> · <span id="lbgroup"></span></span><div class="x"><button type="button" id="lbzoom" aria-label="Zoom">{ZOOM}</button><button type="button" id="lbclose" aria-label="Close">{CLOSE}</button></div></div>
 <div class="st" id="lbst"><img id="lbA" alt=""><img id="lbB" alt=""><button type="button" class="nav p" id="lbprev" aria-label="Previous plate">{CHEV_L}</button><button type="button" class="nav n" id="lbnext" aria-label="Next plate">{CHEV_R}</button></div>
 <div class="cap"><span class="c" id="lbcap"></span><span><span class="k" id="lbct"></span> · swipe or use the arrows · esc closes</span></div></div>
<div class="cur" id="cur"></div><div class="cur2" id="cur2"></div>'''

JS = r"""
(function(){
'use strict';
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
const touch=matchMedia('(hover: none)').matches;
let lockY=0, locks=0;
function lockScroll(){ if(locks++>0) return; lockY=window.scrollY||window.pageYOffset||0; body.style.top=(-lockY)+'px'; body.classList.add('locked'); }
function jump(y){ const de=document.documentElement, prev=de.style.scrollBehavior; de.style.scrollBehavior='auto'; window.scrollTo(0,y); de.style.scrollBehavior=prev; }
function unlockScroll(){ if(locks===0||--locks>0) return; body.classList.remove('locked'); body.style.top=''; const y=lockY; jump(y); requestAnimationFrame(()=>{ jump(y); setTimeout(()=>jump(y),60); }); }
const R=s=>(s&&window.__A&&window.__A[s.replace(/^assets\//,'')])||s;
const useM=Math.min(innerWidth,innerHeight)<=700;
const M=s=>(useM&&/^assets\/[\w-]+\.jpg$/.test(s))?s.replace('assets/','assets/m/'):s;
const body=document.body;

/* ---------- veil + arrival ---------- */
const veil=$('#veil'), vbar=$('#vbar'), vct=$('#vct'), wname=$('#wname');
const heroImg=$('#welcome .bg img');
let booted=false;
function boot(){
  if(booted) return; booted=true;
  body.classList.add('ready'); veil.classList.add('off');
  const chars=$$('.ch',wname).length;
  setTimeout(()=>wname.classList.add('shine'), rm?0:1900+chars*45+900);
  if(location.hash && $(location.hash)) setTimeout(()=>go(location.hash.slice(1),true), rm?0:600);
}
if(rm){ boot(); }
else{
  const t0=performance.now(), dur=1500;
  const tick=now=>{
    const p=Math.min(1,(now-t0)/dur), e=1-Math.pow(1-p,3);
    vbar.style.transform='scaleX('+e+')'; vct.textContent=String(Math.round(e*100)).padStart(2,'0');
    if(p<1) requestAnimationFrame(tick);
    else if(heroImg.complete||!heroImg.src) setTimeout(boot,220);
    else { heroImg.addEventListener('load',()=>setTimeout(boot,120),{once:true}); setTimeout(boot,1800); }
  };
  requestAnimationFrame(tick);
}

/* ---------- navigation ---------- */
function go(id,instant){
  const el=document.getElementById(id); if(!el) return;
  closeIndex();
  if(id==='welcome') window.scrollTo({top:0,behavior:(instant||rm)?'auto':'smooth'});
  else el.scrollIntoView({behavior:(instant||rm)?'auto':'smooth',block:'start'});
  if(history.replaceState) history.replaceState(null,'','#'+id);
}
let shelfDragged=false;
document.addEventListener('click',e=>{
  const st=e.target.closest('.star'); if(st){ e.preventDefault(); e.stopPropagation(); toggleStar(st.dataset.id, st); return; }
  const rmv=e.target.closest('[data-rm]'); if(rmv){ toggleStar(rmv.dataset.rm); return; }
  const t=e.target.closest('[data-go]'); if(!t) return;
  if(shelfDragged){ e.preventDefault(); return; }
  e.preventDefault(); go(t.dataset.go);
});
document.addEventListener('keydown',e=>{
  if((e.key==='Enter'||e.key===' ')&&e.target.matches('[data-go][tabindex], .gi, .plate.zoom')){
    e.preventDefault();
    if(e.target.matches('.gi, .plate.zoom')) openLb(e.target); else go(e.target.dataset.go);
  }
});

/* ---------- index overlay ---------- */
const idx=$('#index'), idxbtn=$('#idxbtn');
let lastFocus=null;
function openIndex(){ lastFocus=document.activeElement; idx.classList.add('open'); lockScroll(); setTimeout(()=>$('#idxclose').focus(),50); }
function closeIndex(){ if(!idx.classList.contains('open')) return; idx.classList.remove('open'); unlockScroll(); if(lastFocus&&lastFocus.focus){ try{ lastFocus.focus({preventScroll:true}); }catch(e){} } }
idxbtn.addEventListener('click',()=>idx.classList.contains('open')?closeIndex():openIndex());
$('#idxclose').addEventListener('click',closeIndex);

/* ---------- scroll: progress, parallax, active tab ---------- */
const pbar=$('#pbar'), plates=$$('.plate .pi'), tabs=$$('.tabs button'), sections=$$('#welcome, section.pg');
let ticking=false;
function onScroll(){
  if(ticking) return; ticking=true;
  requestAnimationFrame(()=>{
    const vh=innerHeight, y=scrollY, dh=document.documentElement.scrollHeight-vh;
    pbar.style.transform='scaleX('+(dh>0?y/dh:0)+')';
    if(!rm&&!touch) for(const pi of plates){
      const r=pi.parentElement.getBoundingClientRect();
      if(r.bottom<0||r.top>vh) continue;
      const p=Math.max(-1,Math.min(1,(r.top+r.height/2-vh/2)/vh));
      pi.style.setProperty('--py',(p*-0.06*r.height).toFixed(1)+'px');
    }
    let cur=null;
    for(const s of sections){ if(s.getBoundingClientRect().top<=vh*0.45) cur=s; }
    const id=cur?cur.id:'welcome';
    for(const t of tabs) t.classList.toggle('on',t.dataset.go===id);
    ticking=false;
  });
}
addEventListener('scroll',onScroll,{passive:true}); addEventListener('resize',onScroll); onScroll();

/* ---------- reveals ---------- */
const rvEls=$$('.rv, .rv-stag, .wipe');
if(rm||!('IntersectionObserver' in window)) rvEls.forEach(el=>el.classList.add('in'));
else{
  const io=new IntersectionObserver(es=>{ for(const en of es) if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } },{rootMargin:'0px 0px -8% 0px',threshold:0});
  rvEls.forEach(el=>io.observe(el));
}
/* counters */
const cnt=$$('[data-count]');
function runCount(el){
  const to=parseFloat(el.dataset.count), t0=performance.now(), dur=1400;
  const step=now=>{ const p=Math.min(1,(now-t0)/dur), e=1-Math.pow(1-p,3); el.textContent=Math.round(to*e).toLocaleString('en-GB'); if(p<1) requestAnimationFrame(step); };
  requestAnimationFrame(step);
}
if(rm||!('IntersectionObserver' in window)) cnt.forEach(el=>el.textContent=parseFloat(el.dataset.count).toLocaleString('en-GB'));
else{ const io2=new IntersectionObserver(es=>{ for(const en of es) if(en.isIntersecting){ runCount(en.target); io2.unobserve(en.target); } },{threshold:.4}); cnt.forEach(el=>{ el.textContent='0'; io2.observe(el); }); }

/* ---------- ledger sort ---------- */
const ledger=$('#ledger tbody');
$$('.sorts button').forEach(b=>b.addEventListener('click',()=>{
  $$('.sorts button').forEach(x=>x.classList.toggle('on',x===b));
  const k=b.dataset.sort, rows=$$('tr',ledger);
  rows.sort((a,c)=>{ const va=parseFloat(a.dataset[k]), vc=parseFloat(c.dataset[k]); return va-vc || parseFloat(a.dataset.n)-parseFloat(c.dataset.n); });
  rows.forEach(r=>ledger.appendChild(r));
}));

/* ---------- shelf ---------- */
const shelf=$('#shelf');
$$('[data-shelf]').forEach(b=>b.addEventListener('click',()=>{ const c=$('.card',shelf); shelf.scrollBy({left:parseInt(b.dataset.shelf)*(c?c.offsetWidth+20:320)*1.5,behavior:rm?'auto':'smooth'}); }));
let sx=0, sl=0, sdown=false;
shelf.addEventListener('pointerdown',e=>{ if(e.pointerType==='touch') return; sdown=true; shelfDragged=false; sx=e.clientX; sl=shelf.scrollLeft; shelf.classList.add('drag'); });
addEventListener('pointermove',e=>{ if(!sdown) return; const dx=e.clientX-sx; if(Math.abs(dx)>6) shelfDragged=true; shelf.scrollLeft=sl-dx; });
addEventListener('pointerup',()=>{ if(!sdown) return; sdown=false; shelf.classList.remove('drag'); setTimeout(()=>shelfDragged=false,50); });

/* ---------- gallery filters ---------- */
$$('.gal-h .groups').forEach(g=>{
  const gal=g.closest('.gal-h').nextElementSibling;
  $$('button',g).forEach(b=>b.addEventListener('click',()=>{
    $$('button',g).forEach(x=>x.classList.toggle('on',x===b));
    const k=b.dataset.g; $$('.gi',gal).forEach(f=>f.classList.toggle('hide',k!=='*'&&f.dataset.g!==k));
  }));
});

/* ---------- shortlist ---------- */
const KEY=__SLUG__+'.shortlist';
const META={}; $$('section.dz').forEach(s=>{ META[s.id]={n:s.dataset.n,name:s.dataset.name,district:$('.run .c',s).textContent.trim()}; });
let sl_=[]; try{ sl_=JSON.parse(localStorage.getItem(KEY)||'[]').filter(id=>META[id]); }catch(e){ sl_=[]; }
function saveSl(){ try{ localStorage.setItem(KEY,JSON.stringify(sl_)); }catch(e){} }
function toggleStar(id,btn){
  const i=sl_.indexOf(id); if(i<0) sl_.push(id); else sl_.splice(i,1);
  sl_.sort((a,b)=>META[a].n.localeCompare(META[b].n)); saveSl(); renderSl();
  if(btn){ btn.classList.remove('pop'); void btn.offsetWidth; btn.classList.add('pop'); }
}
function renderSl(){
  $$('.star[data-id]').forEach(b=>{ const on=sl_.includes(b.dataset.id); b.classList.toggle('on',on); b.setAttribute('aria-pressed',on?'true':'false'); });
  $('#slcount').textContent=sl_.length?String(sl_.length):'';
  const list=$('#sllist'); list.innerHTML=sl_.map(id=>{ const m=META[id]; return '<li><span class="k">'+m.n+'</span><span>'+m.name+' · '+m.district+'</span><button type="button" class="rm" data-rm="'+id+'">Remove</button></li>'; }).join('');
  $('#slempty').hidden=sl_.length>0;
  let txt='Good day Sadiq. I have reviewed my portfolio.';
  if(sl_.length) txt+=' I would like to pursue:\n'+sl_.map(id=>META[id].n+' '+META[id].name+' ('+META[id].district+')').join('\n');
  txt+='\n— '+__SIGNOFF__;
  $('#slsend').href='https://wa.me/447931814601?text='+encodeURIComponent(txt);
}
renderSl();

/* ---------- lightbox ---------- */
const lb=$('#lb'), lbA=$('#lbA'), lbB=$('#lbB'), lbst=$('#lbst');
let lbList=[], lbI=0, lbActive=lbA, lbOpen=false, lbFocus=null, z={s:1,x:0,y:0};
function listFor(id,firstSrc,firstCap){
  const figs=$$('.gi[data-lb="'+id+'"]');
  let list=figs.map(f=>({src:M(R(f.dataset.src)),cap:f.dataset.cap,g:f.dataset.g}));
  if(firstSrc && !list.some(x=>x.src===firstSrc)) list.unshift({src:firstSrc,cap:firstCap,g:'Visualisation'});
  return list;
}
function openLb(el){
  const id=el.dataset.lb, sec=document.getElementById(id);
  const src=M(R(el.dataset.src)), cap=el.dataset.cap||($('.cap',el)?$('.cap',el).textContent:'');
  lbList=listFor(id,src,cap); if(!lbList.length) return;
  lbI=Math.max(0,lbList.findIndex(x=>x.src===src));
  $('#lbsite').textContent=(sec?sec.dataset.n+' · '+sec.dataset.name:'');
  lbFocus=document.activeElement; lbOpen=true; lb.classList.add('open'); lockScroll();
  lbA.classList.remove('on'); lbB.classList.remove('on'); lbA.removeAttribute('src'); lbB.removeAttribute('src'); lbActive=lbB;
  show(lbI); setTimeout(()=>$('#lbclose').focus(),50);
}
function resetZoom(){ z={s:1,x:0,y:0}; lb.classList.remove('zoomed'); [lbA,lbB].forEach(i=>i.style.transform=''); }
function applyZoom(){ lbActive.style.transform='translate('+z.x+'px,'+z.y+'px) scale('+z.s+')'; lb.classList.toggle('zoomed',z.s>1); }
function show(i){
  lbI=(i+lbList.length)%lbList.length; const it=lbList[lbI], myI=lbI;
  resetZoom();
  const next=lbActive===lbA?lbB:lbA, prev=lbActive;
  prev.classList.remove('on');
  const swap=()=>{ let done=false; const on=()=>{ if(done||lbI!==myI) return; done=true; next.classList.add('on'); lbActive=next; }; next.onload=on; next.onerror=on; next.alt=it.cap; next.src=it.src; if(next.complete&&next.naturalWidth) on(); else if(next.decode) next.decode().then(on).catch(()=>{}); };
  setTimeout(swap, rm?0:240);
  $('#lbcap').textContent=it.cap; $('#lbgroup').textContent=it.g; $('#lbct').textContent=String(lbI+1).padStart(2,'0')+' / '+String(lbList.length).padStart(2,'0');
  const pre=new Image(); pre.src=lbList[(lbI+1)%lbList.length].src;
}
function closeLb(){ if(!lbOpen) return; lbOpen=false; lb.classList.remove('open'); unlockScroll(); resetZoom(); if(lbFocus&&lbFocus.focus){ try{ lbFocus.focus({preventScroll:true}); }catch(e){} } }
document.addEventListener('click',e=>{ const t=e.target.closest('.gi, .plate.zoom'); if(t){ e.preventDefault(); openLb(t); } });
$('#lbclose').addEventListener('click',closeLb); $('#lbprev').addEventListener('click',()=>show(lbI-1)); $('#lbnext').addEventListener('click',()=>show(lbI+1));
$('#lbzoom').addEventListener('click',()=>{ if(z.s>1) resetZoom(); else { z.s=2.2; applyZoom(); } });
document.addEventListener('keydown',e=>{
  if(e.key==='Escape'){ if(lbOpen) closeLb(); else closeIndex(); }
  if(!lbOpen) return;
  if(e.key==='ArrowRight') show(lbI+1); if(e.key==='ArrowLeft') show(lbI-1);
});
let px=0, py=0, pdown=false, moved=false, zx=0, zy=0;
lb.addEventListener('touchmove',e=>{ if(lbOpen&&!e.target.closest('.leaflet-container')) e.preventDefault(); },{passive:false});
lbst.addEventListener('pointerdown',e=>{ if(e.target.closest('button')) return; pdown=true; moved=false; px=e.clientX; py=e.clientY; zx=z.x; zy=z.y; lbst.setPointerCapture(e.pointerId); });
lbst.addEventListener('pointermove',e=>{ if(!pdown) return; const dx=e.clientX-px, dy=e.clientY-py; if(Math.abs(dx)>4||Math.abs(dy)>4) moved=true; if(z.s>1){ z.x=zx+dx; z.y=zy+dy; applyZoom(); } });
lbst.addEventListener('pointerup',e=>{ if(!pdown) return; pdown=false; const dx=e.clientX-px;
  if(z.s>1) return; if(dx<-40) show(lbI+1); else if(dx>40) show(lbI-1); });
lbst.addEventListener('dblclick',e=>{ if(z.s>1) resetZoom(); else { const r=lbst.getBoundingClientRect(); z.s=2.2; z.x=(r.width/2-(e.clientX-r.left))*(z.s-1); z.y=(r.height/2-(e.clientY-r.top))*(z.s-1); applyZoom(); } });
lbst.addEventListener('wheel',e=>{ if(!lbOpen) return; e.preventDefault(); const s=Math.max(1,Math.min(4,z.s*(e.deltaY<0?1.12:0.89))); if(s===1){ resetZoom(); return; } z.s=s; applyZoom(); },{passive:false});


/* ---------- map (Leaflet, loaded when near; packed tiles in the preview) ---------- */
(function(){
  const wrap=$('#lmapwrap'); if(!wrap) return;
  const fb=$('#mapfb'), rowsEl=$('#mrows'), rows={}, markers={}; let map=null, booted=false, streets=null, aerial=null, route=null, cur=null;
  $$('.mrow',rowsEl).forEach(r=>rows[r.dataset.m]=r);
  const D=window.GARO_MAP||[], LM=window.GARO_LM||[], PACK=window.__TILES||null;
  const BLANK='data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7';
  function fail(){ fb.hidden=false; wrap.classList.add('failed'); }
  function loadScript(src,cb){ const el=document.createElement('script'); el.src=src; el.async=true; el.onload=cb; el.onerror=fail; document.head.appendChild(el); }
  function boot(){
    if(booted) return; booted=true;
    if(window.L){ try{ init(); }catch(e){ fail(); if(window.console) console.error(e); } return; }
    let pending=2; const done=()=>{ if(--pending===0){ if(window.L){ try{ init(); }catch(e){ fail(); if(window.console) console.error(e); } } else fail(); } };
    const css=document.createElement('link'); css.rel='stylesheet'; css.href='assets/leaflet/leaflet.css'; css.onload=done; css.onerror=fail; document.head.appendChild(css);
    loadScript('assets/leaflet/leaflet.js',done);
  }
  const lio=new IntersectionObserver(es=>{ if(es.some(e=>e.isIntersecting)){ boot(); lio.disconnect(); } },{rootMargin:'900px 0px'}); lio.observe(wrap);
  const coarse=matchMedia('(pointer:coarse)').matches;
  function init(){
    const maxZ=PACK?16:19;
    map=L.map('lmap',{zoomControl:false,scrollWheelZoom:false,dragging:!coarse,zoomSnap:.5,minZoom:PACK?11:5,maxZoom:maxZ,attributionControl:true});
    map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
    L.control.zoom({position:'topleft'}).addTo(map); L.control.scale({imperial:false,position:'bottomleft',maxWidth:130}).addTo(map);
    const OSM='&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors', ESRI='Imagery &copy; Esri, Maxar, Earthstar Geographics';
    if(PACK){
      const Packed=L.TileLayer.extend({getTileUrl:function(c){ return this.options.pack[c.z+'/'+c.x+'/'+c.y]||BLANK; }});
      streets=new Packed('',{pack:PACK.osm,maxZoom:maxZ,attribution:OSM+' · preview map, zoom limited'});
      aerial=PACK.esri?new Packed('',{pack:PACK.esri,maxZoom:maxZ,attribution:ESRI}):null;
    } else {
      streets=L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxNativeZoom:19,maxZoom:19,attribution:OSM});
      aerial=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:19,maxZoom:19,attribution:ESRI});
    }
    if(!aerial) $$('[data-layer]').forEach(b=>b.closest('.seg').hidden=true);
    streets.addTo(map);
    let tilesOk=false; streets.on('tileload',()=>{ tilesOk=true; wrap.classList.add('ready'); }); streets.on('tileerror',()=>{ if(!tilesOk&&!PACK) fail(); });
    setTimeout(()=>{ if(!tilesOk){ if(PACK) wrap.classList.add('ready'); else fail(); } },9000);
    map.on('click',()=>{ map.scrollWheelZoom.enable(); wrap.classList.add('wheel'); });
    map.on('zoomend',()=>wrap.classList.toggle('far',map.getZoom()<13.5)); wrap.classList.add('far');
    LM.forEach(l=>{
      L.marker(l.ll,{icon:L.divIcon({className:'lm-ref'+(l.dest?' dest':''),html:'<i></i><b>'+l.n+'</b>',iconSize:[0,0]}),interactive:true,keyboard:false,zIndexOffset:-100}).addTo(map).bindTooltip(l.n+' · '+l.s,{direction:'top',offset:[0,-8]});
    });
    D.forEach(x=>{
      if(!x.ll) return;
      const ap=x.approx?' ap':'';
      const m=L.marker(x.ll,{icon:L.divIcon({className:'lm-pin'+ap,html:'<i>'+x.n+'</i><b>'+x.name+'</b>',iconSize:[0,0]}),alt:x.name,riseOnHover:true,zIndexOffset:1000}).addTo(map);
      const note=x.approx==='nearest'?'Nearest pin available':x.approx==='street'?'Street-level pin':x.approx==='district'?'District only · exact pin to follow':'';
      const dist=x.route?'<div class="a">'+x.route.km+' km · '+x.route.min+' min to '+(x.city==='Lagos'?'the Eko Hotel':'the Central Business District')+'</div>':'';
      m.bindPopup('<div class="lm-pop"><div class="k">'+x.n+' · '+x.status+'</div><div class="n">'+x.name+'</div><div class="a">'+x.addr+(note?' · '+note:'')+'</div>'+dist+'<div class="p">'+x.price+'</div><div class="x"><a href="#'+x.id+'" data-go="'+x.id+'">Dossier</a><a href="'+x.gmaps+'" target="_blank" rel="noopener">Google Maps</a></div></div>',{maxWidth:300,closeButton:true,offset:[0,-6]});
      m.on('click',()=>select(x.id,false)); markers[x.id]=m;
    });
    fitCity('Abuja',true);
  }
  function drawRoute(x){
    if(route){ map.removeLayer(route); route=null; }
    if(!x||!x.route||!x.route.line) return;
    route=L.layerGroup([L.polyline(x.route.line,{color:'#0b0a08',weight:7,opacity:.55,lineJoin:'round'}),L.polyline(x.route.line,{color:'#e6cb92',weight:3,opacity:.95,lineJoin:'round',dashArray:'1 7',lineCap:'round'})]).addTo(map);
  }
  function fitCity(city,instant){
    let pts;
    if(city==='Maitama') pts=D.filter(x=>x.ll&&x.district==='Maitama').map(x=>x.ll);
    else pts=D.filter(x=>x.ll&&x.city===city).map(x=>x.ll).concat(LM.filter(l=>l.city===city&&l.dest).map(l=>l.ll));
    if(!pts.length) return;
    $$('[data-city]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.city===city?'true':'false'));
    if(pts.length===1){ instant?map.setView(pts[0],15):map.flyTo(pts[0],15,{duration:1.8}); return; }
    const b=L.latLngBounds(pts), o={padding:[44,44],maxZoom:PACK?15:16};
    instant||rm?map.fitBounds(b,o):map.flyToBounds(b,Object.assign({duration:1.6},o));
  }
  function select(id,fly){
    cur=id;
    for(const k in rows){ rows[k].setAttribute('aria-pressed',k===id?'true':'false'); rows[k].classList.toggle('on',k===id); const e=markers[k]&&markers[k].getElement(); if(e) e.classList.toggle('on',k===id); }
    const x=D.find(z=>z.id===id); if(!x||!map||!x.ll) return;
    const cityBtn=x.district==='Maitama'?'Maitama':x.city; $$('[data-city]').forEach(b=>b.setAttribute('aria-pressed',b.dataset.city===cityBtn?'true':'false'));
    drawRoute(x);
    const after=()=>markers[id].openPopup();
    if(fly&&!rm){ if(x.route&&x.route.line){ map.flyToBounds(L.latLngBounds(x.route.line),{padding:[60,60],maxZoom:PACK?15:16,duration:1.5}); } else map.flyTo(x.ll,x.approx==='district'?14:15,{duration:1.4}); map.once('moveend',after); }
    else { after(); }
    rows[id].scrollIntoView({block:'nearest',behavior:'smooth'});
  }
  rowsEl.addEventListener('click',e=>{ const r=e.target.closest('.mrow'); if(!r) return; if(!map){ go(r.dataset.m); return; } select(r.dataset.m,true); });
  $$('[data-layer]').forEach(b=>b.addEventListener('click',()=>{ if(!map||!aerial) return; const layer=b.dataset.layer; $$('[data-layer]').forEach(x=>x.setAttribute('aria-pressed',x===b?'true':'false')); wrap.classList.toggle('aerial',layer==='aerial'); if(layer==='aerial'){ map.removeLayer(streets); aerial.addTo(map); } else { map.removeLayer(aerial); streets.addTo(map); } }));
  $$('[data-city]').forEach(b=>b.addEventListener('click',()=>{ if(!map) return; drawRoute(null); map.closePopup(); for(const k in rows){ rows[k].setAttribute('aria-pressed','false'); rows[k].classList.remove('on'); const e=markers[k]&&markers[k].getElement(); if(e) e.classList.remove('on'); } fitCity(b.dataset.city,false); }));
})();

/* ---------- cursor ---------- */
const cur=$('#cur'), cur2=$('#cur2');
if(matchMedia('(pointer:fine)').matches && innerWidth>=900 && !rm){
  let mx=-100,my=-100,cx=-100,cy=-100,raf=null;
  const loop=()=>{ cx+=(mx-cx)*.18; cy+=(my-cy)*.18; cur2.style.left=cx+'px'; cur2.style.top=cy+'px'; raf=(Math.abs(mx-cx)+Math.abs(my-cy)>.2)?requestAnimationFrame(loop):null; };
  addEventListener('pointermove',e=>{ mx=e.clientX; my=e.clientY; cur.style.left=mx+'px'; cur.style.top=my+'px'; if(!raf) raf=requestAnimationFrame(loop); cur2.classList.toggle('big',!lbOpen&&!!e.target.closest('.gi, .plate.zoom, .card .pl')); },{passive:true});
  document.addEventListener('mouseleave',()=>{ cur.style.opacity='0'; cur2.style.opacity='0'; }); document.addEventListener('mouseenter',()=>{ cur.style.opacity='1'; cur2.style.opacity='1'; });
}
})();
"""

def build():
    parts = [chrome(), welcome(), brief(), shelf(), glance()]
    shade = "dark"; flip = False
    for s in SITES:
        parts.append(dossier(s, shade, flip))
        shade = "light" if shade == "dark" else "dark"
        if s["hero"][1] != "wide": flip = not flip
    parts.append(desk())
    content = "\n".join(parts)
    head = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The {esc(CLIENT_SURNAME)} Portfolio</title>
<meta name="description" content="A private portfolio of ten residential addresses in Abuja and Lagos, prepared for {esc(CLIENT)} by Mizan Qist Limited.">
<meta name="robots" content="noindex,nofollow">
<meta name="theme-color" content="#0b0a08">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gilda+Display&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,300;1,400&family=Instrument+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
</head>
<body>
'''
    js = JS.replace('__SLUG__', json.dumps(SLUG)).replace('__SIGNOFF__', json.dumps(CLIENT_SIGNOFF))
    tail = f'''
<script>window.GARO_MAP={json.dumps(map_data(), ensure_ascii=False)};window.GARO_LM={json.dumps(LANDMARKS, ensure_ascii=False)};</script>
<script>{js}</script>
</body>
</html>
'''
    page = head + content + tail
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f: f.write(page)
    # artifact variant: no document wrapper; title + style at the top
    art = f'<title>The {esc(CLIENT_SURNAME)} Portfolio</title>\n<style>{CSS}</style>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gilda+Display&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,300;1,400&family=Instrument+Sans:wght@400;500;600&display=swap">\n' + content + f'\n<script>window.GARO_MAP={json.dumps(map_data(), ensure_ascii=False)};window.GARO_LM={json.dumps(LANDMARKS, ensure_ascii=False)};</script>\n<script>{js}</script>\n'
    with open(os.path.join(ROOT, "tools", "artifact-src.html"), "w", encoding="utf-8") as f: f.write(art)
    print("index.html", len(page)//1024, "KB")

if __name__ == "__main__":
    build()
