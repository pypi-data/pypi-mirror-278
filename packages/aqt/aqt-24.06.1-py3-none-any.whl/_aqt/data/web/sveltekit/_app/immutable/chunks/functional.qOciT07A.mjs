var me=Object.defineProperty;var de=(n,e,s)=>e in n?me(n,e,{enumerable:!0,configurable:!0,writable:!0,value:s}):n[e]=s;var U=(n,e,s)=>(de(n,typeof e!="symbol"?e+"":e,s),s);import{_ as he,a5 as _e,a6 as pe,S as X,i as Y,s as Z,I as z,e as x,a as $,c as ee,b as te,g as ne,f as E,F as v,h as C,j as ge,a7 as Ee,J as se,K as oe,L as re,q as N,u as T,v as _,r as g,l as le,Z as w,W as P,B as A,C as ie,D,E as L,a8 as Ie}from"./Component.C0CSGRj9.mjs";import{e as G,u as ye,o as Se}from"./each.AJyTDN0I.mjs";import{g as K,a as j}from"./Shortcut.FTojhkHY.mjs";import"./index.HrFqG6o2.mjs";import{g as be}from"./cross-browser.a5UeKJFq.mjs";import{r as Ce}from"./helpers.Gx5FBjbA.mjs";import{w as R}from"./index.YmSRfxF3.mjs";function O(n,e){let s,t;if(e instanceof Element){if(s=e,t=Array.prototype.indexOf.call(n,s),t<0)return null}else if(typeof e=="string"){const o=n.namedItem(e);if(!o||(s=o,t=Array.prototype.indexOf.call(n,s),t<0))return null}else if(e<0){t=n.length+e;const o=n.item(t);if(!o)return null;s=o}else{t=e;const o=n.item(t);if(!o)return null;s=o}return[s,t]}class Pe{constructor(e){U(this,"parent");this.parent=e}insertElement(e,s){const t=O(this.parent.children,s);if(!t)return-1;const[o,i]=t;return this.parent.insertBefore(e,o[0]),i}appendElement(e,s){const t=O(this.parent.children,s);if(!t)return-1;const[o,i]=t,m=o.nextElementSibling??null;return this.parent.insertBefore(e,m),i+1}updateElement(e,s){const t=O(this.parent.children,s);return t?(e(...t),!0):!1}}function ve(n){return new Pe(n)}function k(n){return n.nodeType===Node.ELEMENT_NODE}function tt(n){return n.nodeType===Node.TEXT_NODE}function nt(n){return n.nodeType===Node.COMMENT_NODE}const we=["ADDRESS","ARTICLE","ASIDE","BLOCKQUOTE","DETAILS","DIALOG","DD","DIV","DL","DT","FIELDSET","FIGCAPTION","FIGURE","FOOTER","FORM","H1","H2","H3","H4","H5","H6","HEADER","HGROUP","HR","LI","MAIN","NAV","OL","P","PRE","SECTION","TABLE","UL"];function Ae(n){return n.hasAttribute("block")&&n.getAttribute("block")!=="false"}function De(n){return we.includes(n.tagName)||Ae(n)}const Le=["AREA","BASE","BR","COL","EMBED","HR","IMG","INPUT","LINK","META","PARAM","SOURCE","TRACK","WBR"];function st(n){return Le.includes(n.tagName)}function Ne(n){for(const e of n.childNodes)if(k(e)&&De(e)||!Ne(e))return!1;return!0}function ot(n){const e=document.createElement("div");return e.appendChild(n),e.innerHTML}const Te=n=>e=>{var i;const s=(i=be(e))==null?void 0:i.anchorNode;if(!s)return null;let t=null,o=k(s)?s:s.parentElement;for(;o;)t=t||(n(o)?o:null),o=o.parentElement;return t},He=n=>window.getComputedStyle(n).display==="list-item",rt=Te(He);function V(){let n;return[new Promise(s=>n=s),n]}function Oe(n){function e(t){he(n,t)}return[{get(){return _e(n)},available(){return pe(n)}},e]}function Re(n,e,s,t){const o=R([]);o.subscribe(e);function i(d,h){o.update(S=>(S.splice(d,0,h),S))}const[m,a]=V(),l=m.then(ve),r=R([]);async function f(d,h){const[S,M]=V(),b=await l,y=n();function ae(p){return!d.id||p.id===d.id}async function ce(p,ue){for(const fe of p)for(const H of fe.addedNodes){if(!k(H)||!ae(H))continue;const F=h(H,b);return F>=0&&i(F,y),M(void 0),ue.disconnect()}}new MutationObserver(ce).observe(b.parent,{childList:!0});const B={component:d,hostProps:y};return r.update(p=>(p.push(B),p)),await S,{destroy(){r.update(p=>(Ce(p,B),p))}}}async function I(d,h){return(await l).updateElement((M,b)=>{o.update(y=>(y[b]=d(y[b]),y))},h)}const c=t({addComponent:f,updateProps:I});function u(){const d=n();return o.update(h=>(h.push(d),h)),d}return s({getProps:u}),{dynamicSlotted:r,resolveSlotContainer:a,slotsInterface:c}}function ke(){return{detach:R(!1)}}function Me({addComponent:n,updateProps:e}){function s(a,l=0){return n(a,(r,f)=>f.insertElement(r,l))}function t(a,l=-1){return n(a,(r,f)=>f.appendElement(r,l))}function o(a){return e(l=>(l.detach.set(!1),l),a)}function i(a){return e(l=>(l.detach.set(!0),l),a)}function m(a){return e(l=>(l.detach.update(r=>!r),l),a)}return{insert:s,append:t,show:o,hide:i,toggle:m}}const Be=Symbol("dynamicSlotting"),[W,Fe]=Oe(Be);function q(n,e,s){const t=n.slice();return t[12]=e[s].component,t[13]=e[s].hostProps,t}function Ue(n){let e,s,t;const o=[n[12].props];var i=n[12].component;function m(a,l){let r={};if(l!==void 0&&l&2)r=K(o,[j(a[12].props)]);else for(let f=0;f<o.length;f+=1)r=Ie(r,o[f]);return{props:r}}return i&&(e=w(i,m(n))),{c(){e&&A(e.$$.fragment),s=$()},l(a){e&&ie(e.$$.fragment,a),s=ne(a)},m(a,l){e&&D(e,a,l),C(a,s,l),t=!0},p(a,l){if(l&2&&i!==(i=a[12].component)){if(e){N();const r=e;g(r.$$.fragment,1,0,()=>{L(r,1)}),T()}i?(e=w(i,m(a,l)),A(e.$$.fragment),_(e.$$.fragment,1),D(e,s.parentNode,s)):e=null}else if(i){const r=l&2?K(o,[j(a[12].props)]):{};e.$set(r)}},i(a){t||(e&&_(e.$$.fragment,a),t=!0)},o(a){e&&g(e.$$.fragment,a),t=!1},d(a){a&&E(s),e&&L(e,a)}}}function J(n,e){let s,t,o,i;var m=e[0];function a(l,r){return{props:{id:l[12].id,hostProps:l[13],$$slots:{default:[Ue]},$$scope:{ctx:l}}}}return m&&(t=w(m,a(e))),{key:n,first:null,c(){s=P(),t&&A(t.$$.fragment),o=P(),this.h()},l(l){s=P(),t&&ie(t.$$.fragment,l),o=P(),this.h()},h(){this.first=s},m(l,r){C(l,s,r),t&&D(t,l,r),C(l,o,r),i=!0},p(l,r){if(e=l,r&1&&m!==(m=e[0])){if(t){N();const f=t;g(f.$$.fragment,1,0,()=>{L(f,1)}),T()}m?(t=w(m,a(e)),A(t.$$.fragment),_(t.$$.fragment,1),D(t,o.parentNode,o)):t=null}else if(m){const f={};r&2&&(f.id=e[12].id),r&2&&(f.hostProps=e[13]),r&1026&&(f.$$scope={dirty:r,ctx:e}),t.$set(f)}},i(l){i||(t&&_(t.$$.fragment,l),i=!0)},o(l){t&&g(t.$$.fragment,l),i=!1},d(l){l&&(E(s),E(o)),t&&L(t,l)}}}function Ge(n){let e,s,t=[],o=new Map,i,m,a;const l=n[9].default,r=z(l,n,n[10],null);let f=G(n[1]);const I=c=>c[12].id;for(let c=0;c<f.length;c+=1){let u=q(n,f,c),d=I(u);o.set(d,t[c]=J(d,u))}return{c(){e=x("div"),r&&r.c(),s=$();for(let c=0;c<t.length;c+=1)t[c].c();this.h()},l(c){e=ee(c,"DIV",{class:!0});var u=te(e);r&&r.l(u),s=ne(u);for(let d=0;d<t.length;d+=1)t[d].l(u);u.forEach(E),this.h()},h(){v(e,"class","dynamically-slottable svelte-8in7my")},m(c,u){C(c,e,u),r&&r.m(e,null),ge(e,s);for(let d=0;d<t.length;d+=1)t[d]&&t[d].m(e,null);i=!0,m||(a=Ee(n[2].call(null,e)),m=!0)},p(c,[u]){r&&r.p&&(!i||u&1024)&&se(r,l,c,c[10],i?re(l,c[10],u,null):oe(c[10]),null),u&3&&(f=G(c[1]),N(),t=ye(t,u,I,1,c,f,o,e,Se,J,null,q),T())},i(c){if(!i){_(r,c);for(let u=0;u<f.length;u+=1)_(t[u]);i=!0}},o(c){g(r,c);for(let u=0;u<t.length;u+=1)g(t[u]);i=!1},d(c){c&&E(e),r&&r.d(c);for(let u=0;u<t.length;u+=1)t[u].d();m=!1,a()}}}function Ke(n){return n}function je(n,e,s){let t,{$$slots:o={},$$scope:i}=e,{slotHost:m}=e,{createProps:a=ke}=e,{updatePropsList:l=Ke}=e,{setSlotHostContext:r=Fe}=e,{createInterface:f=Me}=e;const{slotsInterface:I,resolveSlotContainer:c,dynamicSlotted:u}=Re(a,l,r,f);le(n,u,h=>s(1,t=h));let{api:d}=e;return Object.assign(d,I),n.$$set=h=>{"slotHost"in h&&s(0,m=h.slotHost),"createProps"in h&&s(4,a=h.createProps),"updatePropsList"in h&&s(5,l=h.updatePropsList),"setSlotHostContext"in h&&s(6,r=h.setSlotHostContext),"createInterface"in h&&s(7,f=h.createInterface),"api"in h&&s(8,d=h.api),"$$scope"in h&&s(10,i=h.$$scope)},[m,t,c,u,a,l,r,f,d,o,i]}class lt extends X{constructor(e){super(),Y(this,e,je,Ge,Z,{slotHost:0,createProps:4,updatePropsList:5,setSlotHostContext:6,createInterface:7,api:8})}}function Q(n){let e;const s=n[5].default,t=z(s,n,n[4],null);return{c(){t&&t.c()},l(o){t&&t.l(o)},m(o,i){t&&t.m(o,i),e=!0},p(o,i){t&&t.p&&(!e||i&16)&&se(t,s,o,o[4],e?re(s,o[4],i,null):oe(o[4]),null)},i(o){e||(_(t,o),e=!0)},o(o){g(t,o),e=!1},d(o){t&&t.d(o)}}}function Ve(n){let e,s,t=!n[1]&&Q(n);return{c(){e=x("div"),t&&t.c(),this.h()},l(o){e=ee(o,"DIV",{class:!0,id:!0});var i=te(e);t&&t.l(i),i.forEach(E),this.h()},h(){v(e,"class","item svelte-u5rx4p"),v(e,"id",n[0])},m(o,i){C(o,e,i),t&&t.m(e,null),s=!0},p(o,[i]){o[1]?t&&(N(),g(t,1,1,()=>{t=null}),T()):t?(t.p(o,i),i&2&&_(t,1)):(t=Q(o),t.c(),_(t,1),t.m(e,null)),(!s||i&1)&&v(e,"id",o[0])},i(o){s||(_(t),s=!0)},o(o){g(t),s=!1},d(o){o&&E(e),t&&t.d()}}}function We(n,e,s){let t,{$$slots:o={},$$scope:i}=e,{id:m=void 0}=e,{hostProps:a=void 0}=e;W.available()||console.log("Item: should always have a slotHostContext");const{detach:l}=a??W.get().getProps();return le(n,l,r=>s(1,t=r)),n.$$set=r=>{"id"in r&&s(0,m=r.id),"hostProps"in r&&s(3,a=r.hostProps),"$$scope"in r&&s(4,i=r.$$scope)},[m,t,l,a,i,o]}class it extends X{constructor(e){super(),Y(this,e,We,Ve,Z,{id:0,hostProps:3})}}function at(){}async function ct(){}function ut(n){return!!n}export{we as B,lt as D,it as I,k as a,tt as b,nt as c,De as d,st as e,Oe as f,ct as g,Ae as h,ot as i,Ne as j,rt as k,at as n,V as p,ut as t};
