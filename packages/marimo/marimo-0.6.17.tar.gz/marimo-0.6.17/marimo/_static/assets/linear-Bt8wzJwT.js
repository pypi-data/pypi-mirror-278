import{w as n,i as r,c as t,a as e,b as a}from"./timer-Di1g2zcK.js";import{hp as i,gR as u,hT as o,hx as f,jR as c,jS as s,jT as l,jU as h,hy as p,hw as m,jV as g}from"./index-CaER3GGA.js";import{i as v}from"./init-DLRA0X12.js";function y(n){return null===n?NaN:+n}function*M(n,r){if(void 0===r)for(let t of n)null!=t&&(t=+t)>=t&&(yield t);else{let t=-1;for(let e of n)null!=(e=r(e,++t,n))&&(e=+e)>=e&&(yield e)}}const N=i(u),w=N.right,b=N.left;function d(n,r){r||(r=[]);var t,e=n?Math.min(r.length,n.length):0,a=r.slice();return function(i){for(t=0;t<e;++t)a[t]=n[t]*(1-i)+r[t]*i;return a}}function j(n){return ArrayBuffer.isView(n)&&!(n instanceof DataView)}function A(n,r){return(j(r)?d:k)(n,r)}function k(n,r){var t,e=r?r.length:0,a=n?Math.min(e,n.length):0,i=new Array(a),u=new Array(e);for(t=0;t<a;++t)i[t]=R(n[t],r[t]);for(;t<e;++t)u[t]=r[t];return function(n){for(t=0;t<a;++t)u[t]=i[t](n);return u}}function x(n,r){var t=new Date;return n=+n,r=+r,function(e){return t.setTime(n*(1-e)+r*e),t}}function D(n,r){var t,e={},a={};for(t in null!==n&&"object"==typeof n||(n={}),null!==r&&"object"==typeof r||(r={}),r)t in n?e[t]=R(n[t],r[t]):a[t]=r[t];return function(n){for(t in e)a[t]=e[t](n);return a}}function R(i,u){var o,f=typeof u;return null==u||"boolean"===f?n(u):("number"===f?r:"string"===f?(o=t(u))?(u=o,e):a:u instanceof t?e:u instanceof Date?x:j(u)?d:Array.isArray(u)?k:"function"!=typeof u.valueOf&&"function"!=typeof u.toString||isNaN(u)?D:r)(i,u)}function T(n,r){return n=+n,r=+r,function(t){return Math.round(n*(1-t)+r*t)}}function V(n){return+n}i(y).center;var S=[0,1];function q(n){return n}function B(n,r){return(r-=n=+n)?function(t){return(t-n)/r}:(t=isNaN(r)?NaN:.5,function(){return t});var t}function F(n,r,t){var e=n[0],a=n[1],i=r[0],u=r[1];return a<e?(e=B(a,e),i=t(u,i)):(e=B(e,a),i=t(i,u)),function(n){return i(e(n))}}function O(n,r,t){var e=Math.min(n.length,r.length)-1,a=new Array(e),i=new Array(e),u=-1;for(n[e]<n[0]&&(n=n.slice().reverse(),r=r.slice().reverse());++u<e;)a[u]=B(n[u],n[u+1]),i[u]=t(r[u],r[u+1]);return function(r){var t=w(n,r,1,e)-1;return i[t](a[t](r))}}function U(n,r){return r.domain(n.domain()).range(n.range()).interpolate(n.interpolate()).clamp(n.clamp()).unknown(n.unknown())}function _(){var n,t,e,a,i,u,o=S,f=S,c=R,s=q;function l(){var n,r,t,e=Math.min(o.length,f.length);return s!==q&&(n=o[0],r=o[e-1],n>r&&(t=n,n=r,r=t),s=function(t){return Math.max(n,Math.min(r,t))}),a=e>2?O:F,i=u=null,h}function h(r){return null==r||isNaN(r=+r)?e:(i||(i=a(o.map(n),f,c)))(n(s(r)))}return h.invert=function(e){return s(t((u||(u=a(f,o.map(n),r)))(e)))},h.domain=function(n){return arguments.length?(o=Array.from(n,V),l()):o.slice()},h.range=function(n){return arguments.length?(f=Array.from(n),l()):f.slice()},h.rangeRound=function(n){return f=Array.from(n),c=T,l()},h.clamp=function(n){return arguments.length?(s=!!n||q,l()):s!==q},h.interpolate=function(n){return arguments.length?(c=n,l()):c},h.unknown=function(n){return arguments.length?(e=n,h):e},function(r,e){return n=r,t=e,l()}}function z(){return _()(q,q)}function C(n,r,t,e){var a,i=o(n,r,t);switch((e=f(null==e?",f":e)).type){case"s":var u=Math.max(Math.abs(n),Math.abs(r));return null!=e.precision||isNaN(a=l(i,u))||(e.precision=a),h(e,u);case"":case"e":case"g":case"p":case"r":null!=e.precision||isNaN(a=s(i,Math.max(Math.abs(n),Math.abs(r))))||(e.precision=a-("e"===e.type));break;case"f":case"%":null!=e.precision||isNaN(a=c(i))||(e.precision=a-2*("%"===e.type))}return p(e)}function E(n){var r=n.domain;return n.ticks=function(n){var t=r();return m(t[0],t[t.length-1],null==n?10:n)},n.tickFormat=function(n,t){var e=r();return C(e[0],e[e.length-1],null==n?10:n,t)},n.nice=function(t){null==t&&(t=10);var e,a,i=r(),u=0,o=i.length-1,f=i[u],c=i[o],s=10;for(c<f&&(a=f,f=c,c=a,a=u,u=o,o=a);s-- >0;){if((a=g(f,c,t))===e)return i[u]=f,i[o]=c,r(i);if(a>0)f=Math.floor(f/a)*a,c=Math.ceil(c/a)*a;else{if(!(a<0))break;f=Math.ceil(f*a)/a,c=Math.floor(c*a)/a}e=a}return n},n}function G(){var n=z();return n.copy=function(){return U(n,G())},v.apply(n,arguments),E(n)}export{y as a,A as b,d as c,x as d,T as e,V as f,U as g,q as h,R as i,w as j,G as k,E as l,C as m,M as n,D as o,b as p,z as q,_ as t};
