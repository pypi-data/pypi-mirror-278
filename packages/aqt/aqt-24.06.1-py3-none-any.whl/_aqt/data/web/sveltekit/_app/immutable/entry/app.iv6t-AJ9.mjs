import{S as B,i as U,s as q,a as W,W as h,g as F,h as v,q as I,r as g,u as L,v as w,f as E,X as M,U as X,e as Y,c as Z,b as j,F as D,N as d,t as z,d as G,k as H,Y as J,V as O,Z as k,B as b,C as V,D as P,E as R}from"../chunks/Component.C0CSGRj9.mjs";import"../chunks/index.HrFqG6o2.mjs";const K="modulepreload",Q=function(a,e){return new URL(a,e).href},y={},m=function(e,n,i){let r=Promise.resolve();if(n&&n.length>0){const f=document.getElementsByTagName("link");r=Promise.all(n.map(t=>{if(t=Q(t,i),t in y)return;y[t]=!0;const o=t.endsWith(".css"),l=o?'[rel="stylesheet"]':"";if(!!i)for(let u=f.length-1;u>=0;u--){const p=f[u];if(p.href===t&&(!o||p.rel==="stylesheet"))return}else if(document.querySelector(`link[href="${t}"]${l}`))return;const s=document.createElement("link");if(s.rel=o?"stylesheet":K,o||(s.as="script",s.crossOrigin=""),s.href=t,document.head.appendChild(s),o)return new Promise((u,p)=>{s.addEventListener("load",u),s.addEventListener("error",()=>p(new Error(`Unable to preload CSS for ${t}`)))})}))}return r.then(()=>e()).catch(f=>{const t=new Event("vite:preloadError",{cancelable:!0});if(t.payload=f,window.dispatchEvent(t),!t.defaultPrevented)throw f})},oe={};function $(a){let e,n,i;var r=a[1][0];function f(t,o){return{props:{data:t[3],form:t[2]}}}return r&&(e=k(r,f(a)),a[12](e)),{c(){e&&b(e.$$.fragment),n=h()},l(t){e&&V(e.$$.fragment,t),n=h()},m(t,o){e&&P(e,t,o),v(t,n,o),i=!0},p(t,o){if(o&2&&r!==(r=t[1][0])){if(e){I();const l=e;g(l.$$.fragment,1,0,()=>{R(l,1)}),L()}r?(e=k(r,f(t)),t[12](e),b(e.$$.fragment),w(e.$$.fragment,1),P(e,n.parentNode,n)):e=null}else if(r){const l={};o&8&&(l.data=t[3]),o&4&&(l.form=t[2]),e.$set(l)}},i(t){i||(e&&w(e.$$.fragment,t),i=!0)},o(t){e&&g(e.$$.fragment,t),i=!1},d(t){t&&E(n),a[12](null),e&&R(e,t)}}}function x(a){let e,n,i;var r=a[1][0];function f(t,o){return{props:{data:t[3],$$slots:{default:[ee]},$$scope:{ctx:t}}}}return r&&(e=k(r,f(a)),a[11](e)),{c(){e&&b(e.$$.fragment),n=h()},l(t){e&&V(e.$$.fragment,t),n=h()},m(t,o){e&&P(e,t,o),v(t,n,o),i=!0},p(t,o){if(o&2&&r!==(r=t[1][0])){if(e){I();const l=e;g(l.$$.fragment,1,0,()=>{R(l,1)}),L()}r?(e=k(r,f(t)),t[11](e),b(e.$$.fragment),w(e.$$.fragment,1),P(e,n.parentNode,n)):e=null}else if(r){const l={};o&8&&(l.data=t[3]),o&8215&&(l.$$scope={dirty:o,ctx:t}),e.$set(l)}},i(t){i||(e&&w(e.$$.fragment,t),i=!0)},o(t){e&&g(e.$$.fragment,t),i=!1},d(t){t&&E(n),a[11](null),e&&R(e,t)}}}function ee(a){let e,n,i;var r=a[1][1];function f(t,o){return{props:{data:t[4],form:t[2]}}}return r&&(e=k(r,f(a)),a[10](e)),{c(){e&&b(e.$$.fragment),n=h()},l(t){e&&V(e.$$.fragment,t),n=h()},m(t,o){e&&P(e,t,o),v(t,n,o),i=!0},p(t,o){if(o&2&&r!==(r=t[1][1])){if(e){I();const l=e;g(l.$$.fragment,1,0,()=>{R(l,1)}),L()}r?(e=k(r,f(t)),t[10](e),b(e.$$.fragment),w(e.$$.fragment,1),P(e,n.parentNode,n)):e=null}else if(r){const l={};o&16&&(l.data=t[4]),o&4&&(l.form=t[2]),e.$set(l)}},i(t){i||(e&&w(e.$$.fragment,t),i=!0)},o(t){e&&g(e.$$.fragment,t),i=!1},d(t){t&&E(n),a[10](null),e&&R(e,t)}}}function T(a){let e,n=a[6]&&A(a);return{c(){e=Y("div"),n&&n.c(),this.h()},l(i){e=Z(i,"DIV",{id:!0,"aria-live":!0,"aria-atomic":!0,style:!0});var r=j(e);n&&n.l(r),r.forEach(E),this.h()},h(){D(e,"id","svelte-announcer"),D(e,"aria-live","assertive"),D(e,"aria-atomic","true"),d(e,"position","absolute"),d(e,"left","0"),d(e,"top","0"),d(e,"clip","rect(0 0 0 0)"),d(e,"clip-path","inset(50%)"),d(e,"overflow","hidden"),d(e,"white-space","nowrap"),d(e,"width","1px"),d(e,"height","1px")},m(i,r){v(i,e,r),n&&n.m(e,null)},p(i,r){i[6]?n?n.p(i,r):(n=A(i),n.c(),n.m(e,null)):n&&(n.d(1),n=null)},d(i){i&&E(e),n&&n.d()}}}function A(a){let e;return{c(){e=z(a[7])},l(n){e=G(n,a[7])},m(n,i){v(n,e,i)},p(n,i){i&128&&H(e,n[7])},d(n){n&&E(e)}}}function te(a){let e,n,i,r,f;const t=[x,$],o=[];function l(s,u){return s[1][1]?0:1}e=l(a),n=o[e]=t[e](a);let _=a[5]&&T(a);return{c(){n.c(),i=W(),_&&_.c(),r=h()},l(s){n.l(s),i=F(s),_&&_.l(s),r=h()},m(s,u){o[e].m(s,u),v(s,i,u),_&&_.m(s,u),v(s,r,u),f=!0},p(s,[u]){let p=e;e=l(s),e===p?o[e].p(s,u):(I(),g(o[p],1,1,()=>{o[p]=null}),L(),n=o[e],n?n.p(s,u):(n=o[e]=t[e](s),n.c()),w(n,1),n.m(i.parentNode,i)),s[5]?_?_.p(s,u):(_=T(s),_.c(),_.m(r.parentNode,r)):_&&(_.d(1),_=null)},i(s){f||(w(n),f=!0)},o(s){g(n),f=!1},d(s){s&&(E(i),E(r)),o[e].d(s),_&&_.d(s)}}}function ne(a,e,n){let{stores:i}=e,{page:r}=e,{constructors:f}=e,{components:t=[]}=e,{form:o}=e,{data_0:l=null}=e,{data_1:_=null}=e;M(i.page.notify);let s=!1,u=!1,p=null;X(()=>{const c=i.page.subscribe(()=>{s&&(n(6,u=!0),J().then(()=>{n(7,p=document.title||"untitled page")}))});return n(5,s=!0),c});function N(c){O[c?"unshift":"push"](()=>{t[1]=c,n(0,t)})}function S(c){O[c?"unshift":"push"](()=>{t[0]=c,n(0,t)})}function C(c){O[c?"unshift":"push"](()=>{t[0]=c,n(0,t)})}return a.$$set=c=>{"stores"in c&&n(8,i=c.stores),"page"in c&&n(9,r=c.page),"constructors"in c&&n(1,f=c.constructors),"components"in c&&n(0,t=c.components),"form"in c&&n(2,o=c.form),"data_0"in c&&n(3,l=c.data_0),"data_1"in c&&n(4,_=c.data_1)},a.$$.update=()=>{a.$$.dirty&768&&i.page.set(r)},[t,f,o,l,_,s,u,p,i,r,N,S,C]}class se extends B{constructor(e){super(),U(this,e,ne,te,q,{stores:8,page:9,constructors:1,components:0,form:2,data_0:3,data_1:4})}}const ae=[()=>m(()=>import("../nodes/0.84fQbphY.mjs"),__vite__mapDeps([0,1,2,3,4,5,6,7]),import.meta.url),()=>m(()=>import("../nodes/1.IiUzhS0v.mjs"),__vite__mapDeps([8,4,5,9,10,11]),import.meta.url),()=>m(()=>import("../nodes/2.j2J_cBth.mjs"),__vite__mapDeps([12,3,4,5,9,10,11,13,14,15,16,17,18,19,20]),import.meta.url),()=>m(()=>import("../nodes/3.qMjCZXZb.mjs"),__vite__mapDeps([21,3,17,11,4,22,23,24,5,6,25,26,27,28,18,29,30,13,14,15,16,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45]),import.meta.url),()=>m(()=>import("../nodes/4.x-cVHfPS.mjs"),__vite__mapDeps([46,3,4,5,17,47,26,36,37,13,14,19,48]),import.meta.url),()=>m(()=>import("../nodes/5.oN1PfiQ-.mjs"),__vite__mapDeps([49,3,1,2,11,4,50,23,24,5,6,25,17,26,27,28,22,18,29,13,14,15,16,33,34,35,51,30,52,53,36,37,54,55,56,57,31,32,42,43,44,58,19,59]),import.meta.url),()=>m(()=>import("../nodes/6.1ShaZYbK.mjs"),__vite__mapDeps([60,4,5,17,3,19,33,34,26,11,35,1,2,24,18,47,61,62]),import.meta.url),()=>m(()=>import("../nodes/7.DI0t1hMr.mjs"),__vite__mapDeps([63,4,3,17,64,18,5,13,14,11,2,25,26,27,52,53,65,56,23,24,6,28,66,67,34,68,50,36,37,15,16,69]),import.meta.url),()=>m(()=>import("../nodes/8.cABY1txO.mjs"),__vite__mapDeps([70,3,4,5,17,51,18,30,2,52,25,26,27,53,23,24,6,11,28,34,36,37,15,16,22,29,50,54,33,35,71,58,13,14,38,39,42,43,31,32,66,67,72]),import.meta.url),()=>m(()=>import("../nodes/9.rg2E1cnR.mjs"),__vite__mapDeps([73,3,17,11,4,50,23,24,5,6,25,26,27,28,22,18,29,15,16,71,58,34,13,14,38,39,42,43,31,32,33,35,52,2,53,66,67,72,61,36,37,51,30,54,65,56,68,74]),import.meta.url),()=>m(()=>import("../nodes/10.T7ZvzDGI.mjs"),__vite__mapDeps([75,4,5,3,71,58,34,26,11,13,14,17,25,27,38,39,42,43,31,32,18,15,16,33,35,52,2,53,66,67,72]),import.meta.url),()=>m(()=>import("../nodes/11.tn_OCWUn.mjs"),__vite__mapDeps([76,26,4,5,18,61,25,17,3,27,11,1,2,55,56,30,57,6,52,53,42,43,23,24,28,44,47,65,66,67,34,68,64,13,14,50,36,37,15,16,69,40,41,38,39,77]),import.meta.url)],le=[],ce={"/card-info/[cardId]":[2],"/change-notetype/[...notetypeIds]":[3],"/congrats":[4],"/deck-options/[deckId]":[5],"/graphs":[6],"/image-occlusion/[...imagePathOrNoteId]":[7],"/import-anki-package/[...path]":[8],"/import-csv/[...path]":[9],"/import-page/[...path]":[10],"/tmp":[11]},fe={handleError:({error:a})=>{console.error(a)},reroute:()=>{}};export{ce as dictionary,fe as hooks,oe as matchers,ae as nodes,se as root,le as server_loads};
function __vite__mapDeps(indexes) {
  if (!__vite__mapDeps.viteFileDeps) {
    __vite__mapDeps.viteFileDeps = ["../nodes/0.84fQbphY.mjs","../chunks/utils.zgoumLgx.mjs","../chunks/_commonjsHelpers.1J56E-h6.mjs","../chunks/backend.dXWO455a.mjs","../chunks/Component.C0CSGRj9.mjs","../chunks/index.HrFqG6o2.mjs","../chunks/context-keys.O6kwXuuk.mjs","../assets/0.IueIF_dt.css","../nodes/1.IiUzhS0v.mjs","../chunks/stores.PYsj3Zjm.mjs","../chunks/entry.9XUyJQvV.mjs","../chunks/index.YmSRfxF3.mjs","../nodes/2.j2J_cBth.mjs","../chunks/Container.gOvVoQ_U.mjs","../assets/Container.x45eSaz9.css","../chunks/Row.xEM4s8hj.mjs","../assets/Row.b7XJyprP.css","../chunks/ftl.IxHLS1AB.mjs","../chunks/each.AJyTDN0I.mjs","../chunks/time.dB5-GOAi.mjs","../assets/2.p-Cacfjz.css","../nodes/3.qMjCZXZb.mjs","../chunks/Select.c0X91UPX.mjs","../chunks/Badge.nHU7HYX0.mjs","../chunks/isObject.u1V2KUQz.mjs","../chunks/Shortcut.FTojhkHY.mjs","../chunks/runtime-require.2UnWAaTy.mjs","../assets/Shortcut.NgnNDWaX.css","../assets/Badge.ZOM94LPZ.css","../assets/Select.R71ltMjf.css","../chunks/helpers.Gx5FBjbA.mjs","../chunks/StickyContainer.oBu6HC1z.mjs","../assets/StickyContainer.DxeQbxYa.css","../chunks/TitledContainer._EA_hSs6.mjs","../chunks/theme.FGcaMnTR.mjs","../assets/TitledContainer.3T4Iyw2V.css","../chunks/Col.CsBfgooU.mjs","../assets/Col.qcAwB6Pe.css","../chunks/ButtonToolbar.590ag9iy.mjs","../assets/ButtonToolbar.2F6-K4-a.css","../chunks/ButtonGroup.UaERT0qk.mjs","../assets/ButtonGroup.uVxANZ_b.css","../chunks/LabelButton.S5BYDB1K.mjs","../assets/LabelButton.uoDNjQ14.css","../chunks/index.IuGsAnL9.mjs","../assets/3.J_BdeKS1.css","../nodes/4.x-cVHfPS.mjs","../chunks/bridgecommand._LcBipD7.mjs","../assets/4.B5ccZEdE.css","../nodes/5.oN1PfiQ-.mjs","../chunks/cloneDeep.nJG1jN9L.mjs","../chunks/EnumSelectorRow.9Z2Lf69F.mjs","../chunks/IconButton.JKr4FyHD.mjs","../assets/IconButton.S8sYsYVZ.css","../assets/EnumSelectorRow.tkFoEdPg.css","../chunks/functional.qOciT07A.mjs","../chunks/cross-browser.a5UeKJFq.mjs","../assets/functional.6WG_Obrt.css","../chunks/progress.RWW24KP_.mjs","../assets/5.wPUtG3YC.css","../nodes/6.1ShaZYbK.mjs","../chunks/await_block.QNQtley-.mjs","../assets/6.Qa4TP02F.css","../nodes/7.DI0t1hMr.mjs","../chunks/ImageOcclusionPage.bpnfpX-s.mjs","../chunks/TagEditor.Yqk0sR3q.mjs","../chunks/WithTooltip.tBPuR1Py.mjs","../assets/WithTooltip.Q8RzqOIi.css","../assets/TagEditor.nSBqd-vE.css","../assets/ImageOcclusionPage.6QQiO9Ct.css","../nodes/8.cABY1txO.mjs","../chunks/ImportPage.fyx3gl6J.mjs","../assets/ImportPage.MoxdtRNZ.css","../nodes/9.rg2E1cnR.mjs","../assets/9.-Zxjqsu7.css","../nodes/10.T7ZvzDGI.mjs","../nodes/11.tn_OCWUn.mjs","../assets/11.z-dvmZW1.css"]
  }
  return indexes.map((i) => __vite__mapDeps.viteFileDeps[i])
}
