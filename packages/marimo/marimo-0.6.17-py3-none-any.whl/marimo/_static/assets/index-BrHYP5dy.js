import{iR as O,iP as e,iU as t,iT as n,iQ as a,iX as r,iV as l,j1 as o,iZ as s,jn as i,c6 as y}from"./index-CaER3GGA.js";function $(O){return 45==O||46==O||58==O||O>=65&&O<=90||95==O||O>=97&&O<=122||O>=161}let c=null,p=null,S=0;function g(O,e){let t=O.pos+e;if(p==O&&S==t)return c;for(;9==(n=O.peek(e))||10==n||13==n||32==n;)e++;var n;let a="";for(;;){let t=O.peek(e);if(!$(t))break;a+=String.fromCharCode(t),e++}return p=O,S=t,c=a||null}function u(O,e){this.name=O,this.parent=e,this.hash=e?e.hash:0;for(let t=0;t<O.length;t++)this.hash+=(this.hash<<4)+O.charCodeAt(t)+(O.charCodeAt(t)<<8)}const m=new O({start:null,shift:(O,e,t,n)=>1==e?new u(g(n,1)||"",O):O,reduce:(O,e)=>11==e&&O?O.parent:O,reuse(O,e,t,n){let a=e.type.id;return 1==a||13==a?new u(g(n,1)||"",O):O},hash:O=>O?O.hash:0,strict:!1}),f=new e(((O,e)=>{if(60==O.next)if(O.advance(),47==O.next){O.advance();let t=g(O,0);if(!t)return O.acceptToken(5);if(e.context&&t==e.context.name)return O.acceptToken(2);for(let n=e.context;n;n=n.parent)if(n.name==t)return O.acceptToken(3,-2);O.acceptToken(4)}else if(33!=O.next&&63!=O.next)return O.acceptToken(1)}),{contextual:!0});function d(O,t){return new e((e=>{let n=0,a=t.charCodeAt(0);O:for(;!(e.next<0);e.advance(),n++)if(e.next==a){for(let O=1;O<t.length;O++)if(e.peek(O)!=t.charCodeAt(O))continue O;break}n&&e.acceptToken(O)}))}const V=d(35,"--\x3e"),P=d(36,"?>"),T=d(37,"]]>"),h=t({Text:n.content,"StartTag StartCloseTag EndTag SelfCloseEndTag":n.angleBracket,TagName:n.tagName,"MismatchedCloseTag/Tagname":[n.tagName,n.invalid],AttributeName:n.attributeName,AttributeValue:n.attributeValue,Is:n.definitionOperator,"EntityReference CharacterReference":n.character,Comment:n.blockComment,ProcessingInst:n.processingInstruction,DoctypeDecl:n.documentMeta,Cdata:n.special(n.string)}),_=a.deserialize({version:14,states:",SOQOaOOOrOxO'#CfOzOpO'#CiO!tOaO'#CgOOOP'#Cg'#CgO!{OrO'#CrO#TOtO'#CsO#]OpO'#CtOOOP'#DS'#DSOOOP'#Cv'#CvQQOaOOOOOW'#Cw'#CwO#eOxO,59QOOOP,59Q,59QOOOO'#Cx'#CxO#mOpO,59TO#uO!bO,59TOOOP'#C{'#C{O$TOaO,59RO$[OpO'#CoOOOP,59R,59ROOOQ'#C|'#C|O$dOrO,59^OOOP,59^,59^OOOS'#C}'#C}O$lOtO,59_OOOP,59_,59_O$tOpO,59`O$|OpO,59`OOOP-E6t-E6tOOOW-E6u-E6uOOOP1G.l1G.lOOOO-E6v-E6vO%UO!bO1G.oO%UO!bO1G.oO%dOpO'#CkO%lO!bO'#CyO%zO!bO1G.oOOOP1G.o1G.oOOOP1G.w1G.wOOOP-E6y-E6yOOOP1G.m1G.mO&VOpO,59ZO&_OpO,59ZOOOQ-E6z-E6zOOOP1G.x1G.xOOOS-E6{-E6{OOOP1G.y1G.yO&gOpO1G.zO&gOpO1G.zOOOP1G.z1G.zO&oO!bO7+$ZO&}O!bO7+$ZOOOP7+$Z7+$ZOOOP7+$c7+$cO'YOpO,59VO'bOpO,59VO'jO!bO,59eOOOO-E6w-E6wO'xOpO1G.uO'xOpO1G.uOOOP1G.u1G.uO(QOpO7+$fOOOP7+$f7+$fO(YO!bO<<GuOOOP<<Gu<<GuOOOP<<G}<<G}O'bOpO1G.qO'bOpO1G.qO(eO#tO'#CnOOOO1G.q1G.qO(sOpO7+$aOOOP7+$a7+$aOOOP<<HQ<<HQOOOPAN=aAN=aOOOPAN=iAN=iO'bOpO7+$]OOOO7+$]7+$]OOOO'#Cz'#CzO({O#tO,59YOOOO,59Y,59YOOOP<<G{<<G{OOOO<<Gw<<GwOOOO-E6x-E6xOOOO1G.t1G.t",stateData:")Z~OPQOSVOTWOVWOWWOXWOiXOxPO}TO!PUO~OuZOw]O~O^`Oy^O~OPQOQcOSVOTWOVWOWWOXWOxPO}TO!PUO~ORdO~P!SOseO|gO~OthO!OjO~O^lOy^O~OuZOwoO~O^qOy^O~O[vO`sOdwOy^O~ORyO~P!SO^{Oy^O~OseO|}O~OthO!O!PO~O^!QOy^O~O[!SOy^O~O[!VO`sOd!WOy^O~Oa!YOy^O~Oy^O[mX`mXdmX~O[!VO`sOd!WO~O^!]Oy^O~O[!_Oy^O~O[!aOy^O~O[!cO`sOd!dOy^O~O[!cO`sOd!dO~Oa!eOy^O~Oy^Oz!gO~Oy^O[ma`madma~O[!jOy^O~O[!kOy^O~O[!lO`sOd!mO~OW!pOX!pOz!rO{!pO~O[!sOy^O~OW!pOX!pOz!vO{!pO~O",goto:"%[wPPPPPPPPPPxxP!OP!UPP!_!iP!oxxxP!u!{#R$Z$j$p$v$|PPPP%SXWORYbXRORYb_t`qru!T!U!bQ!h!YS!o!e!fR!t!nQdRRybXSORYbQYORmYQ[PRn[Q_QQkVjp_krz!R!T!X!Z!^!`!f!i!nQr`QzcQ!RlQ!TqQ!XsQ!ZtQ!^{Q!`!QQ!f!YQ!i!]R!n!eQu`S!UqrU![u!U!bR!b!TQ!q!gR!u!qQbRRxbQfTR|fQiUR!OiSXOYTaRb",nodeNames:"⚠ StartTag StartCloseTag MissingCloseTag StartCloseTag StartCloseTag Document Text EntityReference CharacterReference Cdata Element EndTag OpenTag TagName Attribute AttributeName Is AttributeValue CloseTag SelfCloseEndTag SelfClosingTag Comment ProcessingInst MismatchedCloseTag DoctypeDecl",maxTerm:47,context:m,nodeProps:[["closedBy",1,"SelfCloseEndTag EndTag",13,"CloseTag MissingCloseTag"],["openedBy",12,"StartTag StartCloseTag",19,"OpenTag",20,"StartTag"]],propSources:[h],skippedNodes:[0],repeatNodeCount:8,tokenData:"Jy~R!XOX$nXY&kYZ&kZ]$n]^&k^p$npq&kqr$nrs'ssv$nvw(Zw}$n}!O,^!O!P$n!P!Q.m!Q![$n![!]0V!]!^$n!^!_3h!_!`El!`!aF_!a!bGQ!b!c$n!c!}0V!}#P$n#P#QHj#Q#R$n#R#S0V#S#T$n#T#o0V#o%W$n%W%o0V%o%p$n%p&a0V&a&b$n&b1p0V1p4U$n4U4d0V4d4e$n4e$IS0V$IS$I`$n$I`$Ib0V$Ib$Kh$n$Kh%#t0V%#t&/x$n&/x&Et0V&Et&FV$n&FV;'S0V;'S;:j3b;:j;=`&e<%l?&r$n?&r?Ah0V?Ah?BY$n?BY?Mn0V?MnO$nX$uWVP{WOr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$nP%dTVPOv%_w!^%_!_;'S%_;'S;=`%s<%lO%_P%vP;=`<%l%_W&OT{WOr%ysv%yw;'S%y;'S;=`&_<%lO%yW&bP;=`<%l%yX&hP;=`<%l$n_&t_VP{WyUOX$nXY&kYZ&kZ]$n]^&k^p$npq&kqr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$nZ'zTzYVPOv%_w!^%_!_;'S%_;'S;=`%s<%lO%_~(^ast)c![!]*g!c!}*g#R#S*g#T#o*g%W%o*g%p&a*g&b1p*g4U4d*g4e$IS*g$I`$Ib*g$Kh%#t*g&/x&Et*g&FV;'S*g;'S;:j,W?&r?Ah*g?BY?Mn*g~)fQ!Q![)l#l#m)z~)oQ!Q![)l!]!^)u~)zOX~~)}R!Q![*W!c!i*W#T#Z*W~*ZS!Q![*W!]!^)u!c!i*W#T#Z*W~*jg}!O*g!O!P*g!Q![*g![!]*g!]!^,R!c!}*g#R#S*g#T#o*g$}%O*g%W%o*g%p&a*g&b1p*g1p4U*g4U4d*g4e$IS*g$I`$Ib*g$Je$Jg*g$Kh%#t*g&/x&Et*g&FV;'S*g;'S;:j,W?&r?Ah*g?BY?Mn*g~,WOW~~,ZP;=`<%l*gZ,eYVP{WOr$nrs%_sv$nw}$n}!O-T!O!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$nZ-[YVP{WOr$nrs%_sv$nw!^$n!^!_%y!_!`$n!`!a-z!a;'S$n;'S;=`&e<%lO$nZ.TW|QVP{WOr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$n].tYVP{WOr$nrs%_sv$nw!^$n!^!_%y!_!`$n!`!a/d!a;'S$n;'S;=`&e<%lO$n]/mWdSVP{WOr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$n_0b!O`S^QVP{WOr$nrs%_sv$nw}$n}!O0V!O!P0V!P!Q$n!Q![0V![!]0V!]!^$n!^!_%y!_!c$n!c!}0V!}#R$n#R#S0V#S#T$n#T#o0V#o$}$n$}%O0V%O%W$n%W%o0V%o%p$n%p&a0V&a&b$n&b1p0V1p4U0V4U4d0V4d4e$n4e$IS0V$IS$I`$n$I`$Ib0V$Ib$Je$n$Je$Jg0V$Jg$Kh$n$Kh%#t0V%#t&/x$n&/x&Et0V&Et&FV$n&FV;'S0V;'S;:j3b;:j;=`&e<%l?&r$n?&r?Ah0V?Ah?BY$n?BY?Mn0V?MnO$n_3eP;=`<%l0VX3mW{WOq%yqr4Vsv%yw!a%y!a!bEU!b;'S%y;'S;=`&_<%lO%yX4[]{WOr%ysv%yw}%y}!O5T!O!f%y!f!g6V!g!}%y!}#O;f#O#W%y#W#XAr#X;'S%y;'S;=`&_<%lO%yX5YV{WOr%ysv%yw}%y}!O5o!O;'S%y;'S;=`&_<%lO%yX5vT}P{WOr%ysv%yw;'S%y;'S;=`&_<%lO%yX6[V{WOr%ysv%yw!q%y!q!r6q!r;'S%y;'S;=`&_<%lO%yX6vV{WOr%ysv%yw!e%y!e!f7]!f;'S%y;'S;=`&_<%lO%yX7bV{WOr%ysv%yw!v%y!v!w7w!w;'S%y;'S;=`&_<%lO%yX7|V{WOr%ysv%yw!{%y!{!|8c!|;'S%y;'S;=`&_<%lO%yX8hV{WOr%ysv%yw!r%y!r!s8}!s;'S%y;'S;=`&_<%lO%yX9SV{WOr%ysv%yw!g%y!g!h9i!h;'S%y;'S;=`&_<%lO%yX9nX{WOr9irs:Zsv9ivw:Zw!`9i!`!a:x!a;'S9i;'S;=`;`<%lO9iP:^TO!`:Z!`!a:m!a;'S:Z;'S;=`:r<%lO:ZP:rOiPP:uP;=`<%l:ZX;PTiP{WOr%ysv%yw;'S%y;'S;=`&_<%lO%yX;cP;=`<%l9iX;kX{WOr%ysv%yw!e%y!e!f<W!f#V%y#V#W?f#W;'S%y;'S;=`&_<%lO%yX<]V{WOr%ysv%yw!f%y!f!g<r!g;'S%y;'S;=`&_<%lO%yX<wV{WOr%ysv%yw!c%y!c!d=^!d;'S%y;'S;=`&_<%lO%yX=cV{WOr%ysv%yw!v%y!v!w=x!w;'S%y;'S;=`&_<%lO%yX=}V{WOr%ysv%yw!c%y!c!d>d!d;'S%y;'S;=`&_<%lO%yX>iV{WOr%ysv%yw!}%y!}#O?O#O;'S%y;'S;=`&_<%lO%yX?VT{WxPOr%ysv%yw;'S%y;'S;=`&_<%lO%yX?kV{WOr%ysv%yw#W%y#W#X@Q#X;'S%y;'S;=`&_<%lO%yX@VV{WOr%ysv%yw#T%y#T#U@l#U;'S%y;'S;=`&_<%lO%yX@qV{WOr%ysv%yw#h%y#h#iAW#i;'S%y;'S;=`&_<%lO%yXA]V{WOr%ysv%yw#T%y#T#U>d#U;'S%y;'S;=`&_<%lO%yXAwV{WOr%ysv%yw#c%y#c#dB^#d;'S%y;'S;=`&_<%lO%yXBcV{WOr%ysv%yw#V%y#V#WBx#W;'S%y;'S;=`&_<%lO%yXB}V{WOr%ysv%yw#h%y#h#iCd#i;'S%y;'S;=`&_<%lO%yXCiV{WOr%ysv%yw#m%y#m#nDO#n;'S%y;'S;=`&_<%lO%yXDTV{WOr%ysv%yw#d%y#d#eDj#e;'S%y;'S;=`&_<%lO%yXDoV{WOr%ysv%yw#X%y#X#Y9i#Y;'S%y;'S;=`&_<%lO%yXE]T!PP{WOr%ysv%yw;'S%y;'S;=`&_<%lO%yZEuWaQVP{WOr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$n_FhW[UVP{WOr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$nZGXYVP{WOr$nrs%_sv$nw!^$n!^!_%y!_!`$n!`!aGw!a;'S$n;'S;=`&e<%lO$nZHQW!OQVP{WOr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$nZHqYVP{WOr$nrs%_sv$nw!^$n!^!_%y!_#P$n#P#QIa#Q;'S$n;'S;=`&e<%lO$nZIhYVP{WOr$nrs%_sv$nw!^$n!^!_%y!_!`$n!`!aJW!a;'S$n;'S;=`&e<%lO$nZJaWwQVP{WOr$nrs%_sv$nw!^$n!^!_%y!_;'S$n;'S;=`&e<%lO$n",tokenizers:[f,V,P,T,0,1,2,3],topRules:{Document:[0,6]},tokenPrec:0});function W(O,e){let t=e&&e.getChild("TagName");return t?O.sliceString(t.from,t.to):""}function b(O,e){let t=e&&e.firstChild;return t&&"OpenTag"==t.name?W(O,t):""}function v(O){for(let e=O&&O.parent;e;e=e.parent)if("Element"==e.name)return e;return null}class C{constructor(O,e,t){this.attrs=e,this.attrValues=t,this.children=[],this.name=O.name,this.completion=Object.assign(Object.assign({type:"type"},O.completion||{}),{label:this.name}),this.openCompletion=Object.assign(Object.assign({},this.completion),{label:"<"+this.name}),this.closeCompletion=Object.assign(Object.assign({},this.completion),{label:"</"+this.name+">",boost:2}),this.closeNameCompletion=Object.assign(Object.assign({},this.completion),{label:this.name+">"}),this.text=O.textContent?O.textContent.map((O=>({label:O,type:"text"}))):[]}}const w=/^[:\-\.\w\u00b7-\uffff]*$/;function x(O){return Object.assign(Object.assign({type:"property"},O.completion||{}),{label:O.name})}function X(O){return"string"==typeof O?{label:`"${O}"`,type:"constant"}:/^"/.test(O.label)?O:Object.assign(Object.assign({},O),{label:`"${O.label}"`})}function Q(O,e){let t=[],n=[],a=Object.create(null);for(let s of e){let O=x(s);t.push(O),s.global&&n.push(O),s.values&&(a[s.name]=s.values.map(X))}let r=[],l=[],o=Object.create(null);for(let s of O){let O=n,e=a;s.attributes&&(O=O.concat(s.attributes.map((O=>"string"==typeof O?t.find((e=>e.label==O))||{label:O,type:"property"}:(O.values&&(e==a&&(e=Object.create(e)),e[O.name]=O.values.map(X)),x(O))))));let i=new C(s,O,e);o[i.name]=i,r.push(i),s.top&&l.push(i)}l.length||(l=r);for(let s=0;s<r.length;s++){let e=O[s],t=r[s];if(e.children)for(let O of e.children)o[O]&&t.children.push(o[O]);else t.children=r}return O=>{var e;let{doc:t}=O.state,s=function(O,e){var t;let n=y(O).resolveInner(e,-1),a=null;for(let r=n;!a&&r.parent;r=r.parent)"OpenTag"!=r.name&&"CloseTag"!=r.name&&"SelfClosingTag"!=r.name&&"MismatchedCloseTag"!=r.name||(a=r);if(a&&(a.to>e||a.lastChild.type.isError)){let O=a.parent;if("TagName"==n.name)return"CloseTag"==a.name||"MismatchedCloseTag"==a.name?{type:"closeTag",from:n.from,context:O}:{type:"openTag",from:n.from,context:v(O)};if("AttributeName"==n.name)return{type:"attrName",from:n.from,context:a};if("AttributeValue"==n.name)return{type:"attrValue",from:n.from,context:a};let t=n==a||"Attribute"==n.name?n.childBefore(e):n;return"StartTag"==(null==t?void 0:t.name)?{type:"openTag",from:e,context:v(O)}:"StartCloseTag"==(null==t?void 0:t.name)&&t.to<=e?{type:"closeTag",from:e,context:O}:"Is"==(null==t?void 0:t.name)?{type:"attrValue",from:e,context:a}:t?{type:"attrName",from:e,context:a}:null}if("StartCloseTag"==n.name)return{type:"closeTag",from:e,context:n.parent};for(;n.parent&&n.to==e&&!(null===(t=n.lastChild)||void 0===t?void 0:t.type.isError);)n=n.parent;return"Element"==n.name||"Text"==n.name||"Document"==n.name?{type:"tag",from:e,context:"Element"==n.name?n:v(n)}:null}(O.state,O.pos);if(!s||"tag"==s.type&&!O.explicit)return null;let{type:i,from:$,context:c}=s;if("openTag"==i){let O=l,e=b(t,c);if(e){let t=o[e];O=(null==t?void 0:t.children)||r}return{from:$,options:O.map((O=>O.completion)),validFor:w}}if("closeTag"==i){let n=b(t,c);return n?{from:$,to:O.pos+(">"==t.sliceString(O.pos,O.pos+1)?1:0),options:[(null===(e=o[n])||void 0===e?void 0:e.closeNameCompletion)||{label:n+">",type:"type"}],validFor:w}:null}if("attrName"==i){let O=o[W(t,c)];return{from:$,options:(null==O?void 0:O.attrs)||n,validFor:w}}if("attrValue"==i){let e=function(O,e,t){let n=e&&e.getChildren("Attribute").find((O=>O.from<=t&&O.to>=t)),a=n&&n.getChild("AttributeName");return a?O.sliceString(a.from,a.to):""}(t,c,$);if(!e)return null;let n=o[W(t,c)],r=((null==n?void 0:n.attrValues)||a)[e];return r&&r.length?{from:$,to:O.pos+('"'==t.sliceString(O.pos,O.pos+1)?1:0),options:r,validFor:/^"[^"]*"?$/}:null}if("tag"==i){let e=b(t,c),n=o[e],a=[],s=c&&c.lastChild;!e||s&&"CloseTag"==s.name&&W(t,s)==e||a.push(n?n.closeCompletion:{label:"</"+e+">",type:"type",boost:2});let i=a.concat(((null==n?void 0:n.children)||(c?r:l)).map((O=>O.openCompletion)));if(c&&(null==n?void 0:n.text.length)){let e=c.firstChild;e.to>O.pos-20&&!/\S/.test(O.state.sliceDoc(e.to,O.pos))&&(i=i.concat(n.text))}return{from:$,options:i,validFor:/^<\/?[:\-\.\w\u00b7-\uffff]*$/}}return null}}const E=l.define({name:"xml",parser:_.configure({props:[o.add({Element(O){let e=/^\s*<\//.test(O.textAfter);return O.lineIndent(O.node.from)+(e?0:O.unit)},"OpenTag CloseTag SelfClosingTag":O=>O.column(O.node.from)+O.unit}),s.add({Element(O){let e=O.firstChild,t=O.lastChild;return e&&"OpenTag"==e.name?{from:e.to,to:"CloseTag"==t.name?t.from:O.to}:null}}),i.add({"OpenTag CloseTag":O=>O.getChild("TagName")})]}),languageData:{commentTokens:{block:{open:"\x3c!--",close:"--\x3e"}},indentOnInput:/^\s*<\/$/}});function G(O={}){return new r(E,E.data.of({autocomplete:Q(O.elements||[],O.attributes||[])}))}export{Q as completeFromSchema,G as xml,E as xmlLanguage};
