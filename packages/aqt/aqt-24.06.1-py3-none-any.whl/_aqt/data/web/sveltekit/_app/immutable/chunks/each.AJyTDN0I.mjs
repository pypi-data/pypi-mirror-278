import{r as C,y as E,v as K}from"./Component.C0CSGRj9.mjs";function B(e){return(e==null?void 0:e.length)!==void 0?e:Array.from(e)}function j(e,t){e.d(1),t.delete(e.key)}function q(e,t){C(e,1,1,()=>{t.delete(e.key)})}function D(e,t){e.f(),j(e,t)}function F(e,t){e.f(),q(e,t)}function G(e,t,y,_,h,d,s,l,g,S,p,A){let c=e.length,o=d.length,f=c;const v={};for(;f--;)v[e[f].key]=f;const u=[],k=new Map,m=new Map,M=[];for(f=o;f--;){const n=A(h,d,f),i=y(n);let a=s.get(i);a?_&&M.push(()=>a.p(n,t)):(a=S(i,n),a.c()),k.set(i,u[f]=a),i in v&&m.set(i,Math.abs(f-v[i]))}const $=new Set,r=new Set;function x(n){K(n,1),n.m(l,p),s.set(n.key,n),p=n.first,o--}for(;c&&o;){const n=u[o-1],i=e[c-1],a=n.key,w=i.key;n===i?(p=n.first,c--,o--):k.has(w)?!s.has(a)||$.has(a)?x(n):r.has(w)?c--:m.get(a)>m.get(w)?(r.add(a),x(n)):($.add(w),c--):(g(i,s),c--)}for(;c--;){const n=e[c];k.has(n.key)||g(n,s)}for(;o;)x(u[o-1]);return E(M),u}function H(e,t,y,_){const h=new Map;for(let d=0;d<t.length;d++){const s=_(y(e,t,d));if(h.has(s)){let l="";try{l=`with value '${String(s)}' `}catch{}throw new Error(`Cannot have duplicate keys in a keyed each: Keys at index ${h.get(s)} and ${d} ${l}are duplicates`)}h.set(s,d)}}export{F as a,j as d,B as e,D as f,q as o,G as u,H as v};
