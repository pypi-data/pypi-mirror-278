import{a as n}from"./array-DmjLdZ15.js";import{w as t,c as r}from"./path-qnb_ma6O.js";import{k as u}from"./step-CPXY0cSE.js";function o(n){return n[0]}function e(n){return n[1]}function f(f,l){var i=r(!0),c=null,a=u,p=null,s=t(h);function h(t){var r,u,o,e=(t=n(t)).length,h=!1;for(null==c&&(p=a(o=s())),r=0;r<=e;++r)!(r<e&&i(u=t[r],r,t))===h&&((h=!h)?p.lineStart():p.lineEnd()),h&&p.point(+f(u,r,t),+l(u,r,t));if(o)return p=null,o+""||null}return f="function"==typeof f?f:void 0===f?o:r(f),l="function"==typeof l?l:void 0===l?e:r(l),h.x=function(n){return arguments.length?(f="function"==typeof n?n:r(+n),h):f},h.y=function(n){return arguments.length?(l="function"==typeof n?n:r(+n),h):l},h.defined=function(n){return arguments.length?(i="function"==typeof n?n:r(!!n),h):i},h.curve=function(n){return arguments.length?(a=n,null!=c&&(p=a(c)),h):a},h.context=function(n){return arguments.length?(null==n?c=p=null:p=a(c=n),h):c},h}export{f as l,o as x,e as y};
