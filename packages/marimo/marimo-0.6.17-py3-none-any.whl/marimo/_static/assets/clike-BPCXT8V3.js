function e(e,t,n,r,a,o){this.indented=e,this.column=t,this.type=n,this.info=r,this.align=a,this.prev=o}function t(t,n,r,a){var o=t.indented;return t.context&&"statement"==t.context.type&&"statement"!=r&&(o=t.context.indented),t.context=new e(o,n,r,a,null,t.context)}function n(e){var t=e.context.type;return")"!=t&&"]"!=t&&"}"!=t||(e.indented=e.context.indented),e.context=e.context.prev}function r(e,t,n){return"variable"==t.prevToken||"type"==t.prevToken||(!!/\S(?:[^- ]>|[*\]])\s*$|\*$/.test(e.string.slice(0,n))||(!(!t.typeAtEndOfLine||e.column()!=e.indentation())||void 0))}function a(e){for(;;){if(!e||"top"==e.type)return!0;if("}"==e.type&&"namespace"!=e.prev.info)return!1;e=e.prev}}function o(o){var i,s,c=o.statementIndentUnit,u=o.dontAlignCalls,d=o.keywords||{},f=o.types||{},p=o.builtin||{},m=o.blockKeywords||{},h=o.defKeywords||{},y=o.atoms||{},g=o.hooks||{},k=o.multiLineStrings,b=!1!==o.indentStatements,v=!1!==o.indentSwitch,w=o.namespaceSeparator,_=o.isPunctuationChar||/[\[\]{}\(\),;\:\.]/,x=o.numberStart||/[\d\.]/,S=o.number||/^(?:0x[a-f\d]+|0b[01]+|(?:\d+\.?\d*|\.\d+)(?:e[-+]?\d+)?)(u|ll?|l|f)?/i,T=o.isOperatorChar||/[+\-*&%=<>!?|\/]/,N=o.isIdentifierChar||/[\w\$_\xa1-\uffff]/,I=o.isReservedIdentifier||!1;function D(e,t){var n,r=e.next();if(g[r]){var a=g[r](e,t);if(!1!==a)return a}if('"'==r||"'"==r)return t.tokenize=(n=r,function(e,t){for(var r,a=!1,o=!1;null!=(r=e.next());){if(r==n&&!a){o=!0;break}a=!a&&"\\"==r}return(o||!a&&!k)&&(t.tokenize=null),"string"}),t.tokenize(e,t);if(x.test(r)){if(e.backUp(1),e.match(S))return"number";e.next()}if(_.test(r))return i=r,null;if("/"==r){if(e.eat("*"))return t.tokenize=C,C(e,t);if(e.eat("/"))return e.skipToEnd(),"comment"}if(T.test(r)){for(;!e.match(/^\/[\/*]/,!1)&&e.eat(T););return"operator"}if(e.eatWhile(N),w)for(;e.match(w);)e.eatWhile(N);var o=e.current();return l(d,o)?(l(m,o)&&(i="newstatement"),l(h,o)&&(s=!0),"keyword"):l(f,o)?"type":l(p,o)||I&&I(o)?(l(m,o)&&(i="newstatement"),"builtin"):l(y,o)?"atom":"variable"}function C(e,t){for(var n,r=!1;n=e.next();){if("/"==n&&r){t.tokenize=null;break}r="*"==n}return"comment"}function z(e,t){o.typeFirstDefinitions&&e.eol()&&a(t.context)&&(t.typeAtEndOfLine=r(e,t,e.pos))}return{name:o.name,startState:function(t){return{tokenize:null,context:new e(-t,0,"top",null,!1),indented:0,startOfLine:!0,prevToken:null}},token:function(e,l){var c=l.context;if(e.sol()&&(null==c.align&&(c.align=!1),l.indented=e.indentation(),l.startOfLine=!0),e.eatSpace())return z(e,l),null;i=s=null;var u=(l.tokenize||D)(e,l);if("comment"==u||"meta"==u)return u;if(null==c.align&&(c.align=!0),";"==i||":"==i||","==i&&e.match(/^\s*(?:\/\/.*)?$/,!1))for(;"statement"==l.context.type;)n(l);else if("{"==i)t(l,e.column(),"}");else if("["==i)t(l,e.column(),"]");else if("("==i)t(l,e.column(),")");else if("}"==i){for(;"statement"==c.type;)c=n(l);for("}"==c.type&&(c=n(l));"statement"==c.type;)c=n(l)}else i==c.type?n(l):b&&(("}"==c.type||"top"==c.type)&&";"!=i||"statement"==c.type&&"newstatement"==i)&&t(l,e.column(),"statement",e.current());if("variable"==u&&("def"==l.prevToken||o.typeFirstDefinitions&&r(e,l,e.start)&&a(l.context)&&e.match(/^\s*\(/,!1))&&(u="def"),g.token){var d=g.token(e,l,u);void 0!==d&&(u=d)}return"def"==u&&!1===o.styleDefs&&(u="variable"),l.startOfLine=!1,l.prevToken=s?"def":u||i,z(e,l),u},indent:function(e,t,n){if(e.tokenize!=D&&null!=e.tokenize||e.typeAtEndOfLine&&a(e.context))return null;var r=e.context,i=t&&t.charAt(0),l=i==r.type;if("statement"==r.type&&"}"==i&&(r=r.prev),o.dontIndentStatements)for(;"statement"==r.type&&o.dontIndentStatements.test(r.info);)r=r.prev;if(g.indent){var s=g.indent(e,r,t,n.unit);if("number"==typeof s)return s}var d=r.prev&&"switch"==r.prev.info;if(o.allmanIndentation&&/[{(]/.test(i)){for(;"top"!=r.type&&"}"!=r.type;)r=r.prev;return r.indented}return"statement"==r.type?r.indented+("{"==i?0:c||n.unit):!r.align||u&&")"==r.type?")"!=r.type||l?r.indented+(l?0:n.unit)+(l||!d||/^(?:case|default)\b/.test(t)?0:n.unit):r.indented+(c||n.unit):r.column+(l?0:1)},languageData:{indentOnInput:v?/^\s*(?:case .*?:|default:|\{\}?|\})$/:/^\s*[{}]$/,commentTokens:{line:"//",block:{open:"/*",close:"*/"}},autocomplete:Object.keys(d).concat(Object.keys(f)).concat(Object.keys(p)).concat(Object.keys(y)),...o.languageData}}}function i(e){for(var t={},n=e.split(" "),r=0;r<n.length;++r)t[n[r]]=!0;return t}function l(e,t){return"function"==typeof e?e(t):e.propertyIsEnumerable(t)}var s="auto if break case register continue return default do sizeof static else struct switch extern typedef union for goto while enum const volatile inline restrict asm fortran",c="alignas alignof and and_eq audit axiom bitand bitor catch class compl concept constexpr const_cast decltype delete dynamic_cast explicit export final friend import module mutable namespace new noexcept not not_eq operator or or_eq override private protected public reinterpret_cast requires static_assert static_cast template this thread_local throw try typeid typename using virtual xor xor_eq",u="bycopy byref in inout oneway out self super atomic nonatomic retain copy readwrite readonly strong weak assign typeof nullable nonnull null_resettable _cmd @interface @implementation @end @protocol @encode @property @synthesize @dynamic @class @public @package @private @protected @required @optional @try @catch @finally @import @selector @encode @defs @synchronized @autoreleasepool @compatibility_alias @available",d="FOUNDATION_EXPORT FOUNDATION_EXTERN NS_INLINE NS_FORMAT_FUNCTION  NS_RETURNS_RETAINEDNS_ERROR_ENUM NS_RETURNS_NOT_RETAINED NS_RETURNS_INNER_POINTER NS_DESIGNATED_INITIALIZER NS_ENUM NS_OPTIONS NS_REQUIRES_NIL_TERMINATION NS_ASSUME_NONNULL_BEGIN NS_ASSUME_NONNULL_END NS_SWIFT_NAME NS_REFINED_FOR_SWIFT",f=i("int long char short double float unsigned signed void bool"),p=i("SEL instancetype id Class Protocol BOOL");function m(e){return l(f,e)||/.+_t$/.test(e)}function h(e){return m(e)||l(p,e)}var y="case do else for if switch while struct enum union",g="struct enum union";function k(e,t){if(!t.startOfLine)return!1;for(var n,r=null;n=e.peek();){if("\\"==n&&e.match(/^.$/)){r=k;break}if("/"==n&&e.match(/^\/[\/\*]/,!1))break;e.next()}return t.tokenize=r,"meta"}function b(e,t){return"type"==t.prevToken&&"type"}function v(e){return!(!e||e.length<2)&&("_"==e[0]&&("_"==e[1]||e[1]!==e[1].toLowerCase()))}function w(e){return e.eatWhile(/[\w\.']/),"number"}function _(e,t){if(e.backUp(1),e.match(/^(?:R|u8R|uR|UR|LR)/)){var n=e.match(/^"([^\s\\()]{0,16})\(/);return!!n&&(t.cpp11RawStringDelim=n[1],t.tokenize=T,T(e,t))}return e.match(/^(?:u8|u|U|L)/)?!!e.match(/^["']/,!1)&&"string":(e.next(),!1)}function x(e){var t=/(\w+)::~?(\w+)$/.exec(e);return t&&t[1]==t[2]}function S(e,t){for(var n;null!=(n=e.next());)if('"'==n&&!e.eat('"')){t.tokenize=null;break}return"string"}function T(e,t){var n=t.cpp11RawStringDelim.replace(/[^\w\s]/g,"\\$&");return e.match(new RegExp(".*?\\)"+n+'"'))?t.tokenize=null:e.skipToEnd(),"string"}const N=o({name:"c",keywords:i(s),types:m,blockKeywords:i(y),defKeywords:i(g),typeFirstDefinitions:!0,atoms:i("NULL true false"),isReservedIdentifier:v,hooks:{"#":k,"*":b}}),I=o({name:"cpp",keywords:i(s+" "+c),types:m,blockKeywords:i(y+" class try catch"),defKeywords:i(g+" class namespace"),typeFirstDefinitions:!0,atoms:i("true false NULL nullptr"),dontIndentStatements:/^template$/,isIdentifierChar:/[\w\$_~\xa1-\uffff]/,isReservedIdentifier:v,hooks:{"#":k,"*":b,u:_,U:_,L:_,R:_,0:w,1:w,2:w,3:w,4:w,5:w,6:w,7:w,8:w,9:w,token:function(e,t,n){if("variable"==n&&"("==e.peek()&&(";"==t.prevToken||null==t.prevToken||"}"==t.prevToken)&&x(e.current()))return"def"}},namespaceSeparator:"::"}),D=o({name:"java",keywords:i("abstract assert break case catch class const continue default do else enum extends final finally for goto if implements import instanceof interface native new package private protected public return static strictfp super switch synchronized this throw throws transient try volatile while @interface"),types:i("var byte short int long float double boolean char void Boolean Byte Character Double Float Integer Long Number Object Short String StringBuffer StringBuilder Void"),blockKeywords:i("catch class do else finally for if switch try while"),defKeywords:i("class interface enum @interface"),typeFirstDefinitions:!0,atoms:i("true false null"),number:/^(?:0x[a-f\d_]+|0b[01_]+|(?:[\d_]+\.?\d*|\.\d+)(?:e[-+]?[\d_]+)?)(u|ll?|l|f)?/i,hooks:{"@":function(e){return!e.match("interface",!1)&&(e.eatWhile(/[\w\$_]/),"meta")},'"':function(e,t){return!!e.match(/""$/)&&(t.tokenize=z,t.tokenize(e,t))}}}),C=o({name:"csharp",keywords:i("abstract as async await base break case catch checked class const continue default delegate do else enum event explicit extern finally fixed for foreach goto if implicit in init interface internal is lock namespace new operator out override params private protected public readonly record ref required return sealed sizeof stackalloc static struct switch this throw try typeof unchecked unsafe using virtual void volatile while add alias ascending descending dynamic from get global group into join let orderby partial remove select set value var yield"),types:i("Action Boolean Byte Char DateTime DateTimeOffset Decimal Double Func Guid Int16 Int32 Int64 Object SByte Single String Task TimeSpan UInt16 UInt32 UInt64 bool byte char decimal double short int long object sbyte float string ushort uint ulong"),blockKeywords:i("catch class do else finally for foreach if struct switch try while"),defKeywords:i("class interface namespace record struct var"),typeFirstDefinitions:!0,atoms:i("true false null"),hooks:{"@":function(e,t){return e.eat('"')?(t.tokenize=S,S(e,t)):(e.eatWhile(/[\w\$_]/),"meta")}}});function z(e,t){for(var n=!1;!e.eol();){if(!n&&e.match('"""')){t.tokenize=null;break}n="\\"==e.next()&&!n}return"string"}function L(e){return function(t,n){for(var r;r=t.next();){if("*"==r&&t.eat("/")){if(1==e){n.tokenize=null;break}return n.tokenize=L(e-1),n.tokenize(t,n)}if("/"==r&&t.eat("*"))return n.tokenize=L(e+1),n.tokenize(t,n)}return"comment"}}const M=o({name:"scala",keywords:i("abstract case catch class def do else extends final finally for forSome if implicit import lazy match new null object override package private protected return sealed super this throw trait try type val var while with yield _ assert assume require print println printf readLine readBoolean readByte readShort readChar readInt readLong readFloat readDouble"),types:i("AnyVal App Application Array BufferedIterator BigDecimal BigInt Char Console Either Enumeration Equiv Error Exception Fractional Function IndexedSeq Int Integral Iterable Iterator List Map Numeric Nil NotNull Option Ordered Ordering PartialFunction PartialOrdering Product Proxy Range Responder Seq Serializable Set Specializable Stream StringBuilder StringContext Symbol Throwable Traversable TraversableOnce Tuple Unit Vector Boolean Byte Character CharSequence Class ClassLoader Cloneable Comparable Compiler Double Exception Float Integer Long Math Number Object Package Pair Process Runtime Runnable SecurityManager Short StackTraceElement StrictMath String StringBuffer System Thread ThreadGroup ThreadLocal Throwable Triple Void"),multiLineStrings:!0,blockKeywords:i("catch class enum do else finally for forSome if match switch try while"),defKeywords:i("class enum def object package trait type val var"),atoms:i("true false null"),indentStatements:!1,indentSwitch:!1,isOperatorChar:/[+\-*&%=<>!?|\/#:@]/,hooks:{"@":function(e){return e.eatWhile(/[\w\$_]/),"meta"},'"':function(e,t){return!!e.match('""')&&(t.tokenize=z,t.tokenize(e,t))},"'":function(e){return e.match(/^(\\[^'\s]+|[^\\'])'/)?"character":(e.eatWhile(/[\w\$_\xa1-\uffff]/),"atom")},"=":function(t,n){var r=n.context;return!("}"!=r.type||!r.align||!t.eat(">"))&&(n.context=new e(r.indented,r.column,r.type,r.info,null,r.prev),"operator")},"/":function(e,t){return!!e.eat("*")&&(t.tokenize=L(1),t.tokenize(e,t))}},languageData:{closeBrackets:{brackets:["(","[","{","'",'"','"""']}}});const E=o({name:"kotlin",keywords:i("package as typealias class interface this super val operator var fun for is in This throw return annotation break continue object if else while do try when !in !is as? file import where by get set abstract enum open inner override private public internal protected catch finally out final vararg reified dynamic companion constructor init sealed field property receiver param sparam lateinit data inline noinline tailrec external annotation crossinline const operator infix suspend actual expect setparam"),types:i("Boolean Byte Character CharSequence Class ClassLoader Cloneable Comparable Compiler Double Exception Float Integer Long Math Number Object Package Pair Process Runtime Runnable SecurityManager Short StackTraceElement StrictMath String StringBuffer System Thread ThreadGroup ThreadLocal Throwable Triple Void Annotation Any BooleanArray ByteArray Char CharArray DeprecationLevel DoubleArray Enum FloatArray Function Int IntArray Lazy LazyThreadSafetyMode LongArray Nothing ShortArray Unit"),intendSwitch:!1,indentStatements:!1,multiLineStrings:!0,number:/^(?:0x[a-f\d_]+|0b[01_]+|(?:[\d_]+(\.\d+)?|\.\d+)(?:e[-+]?[\d_]+)?)(u|ll?|l|f)?/i,blockKeywords:i("catch class do else finally for if where try while enum"),defKeywords:i("class val var object interface fun"),atoms:i("true false null this"),hooks:{"@":function(e){return e.eatWhile(/[\w\$_]/),"meta"},"*":function(e,t){return"."==t.prevToken?"variable":"operator"},'"':function(e,t){var n;return t.tokenize=(n=e.match('""'),function(e,t){for(var r,a=!1,o=!1;!e.eol();){if(!n&&!a&&e.match('"')){o=!0;break}if(n&&e.match('"""')){o=!0;break}r=e.next(),!a&&"$"==r&&e.match("{")&&e.skipTo("}"),a=!a&&"\\"==r&&!n}return!o&&n||(t.tokenize=null),"string"}),t.tokenize(e,t)},"/":function(e,t){return!!e.eat("*")&&(t.tokenize=L(1),t.tokenize(e,t))},indent:function(e,t,n,r){var a=n&&n.charAt(0);return"}"!=e.prevToken&&")"!=e.prevToken||""!=n?"operator"==e.prevToken&&"}"!=n&&"}"!=e.context.type||"variable"==e.prevToken&&"."==a||("}"==e.prevToken||")"==e.prevToken)&&"."==a?2*r+t.indented:t.align&&"}"==t.type?t.indented+(e.context.type==(n||"").charAt(0)?0:r):void 0:e.indented}},languageData:{closeBrackets:{brackets:["(","[","{","'",'"','"""']}}}),F=o({name:"shader",keywords:i("sampler1D sampler2D sampler3D samplerCube sampler1DShadow sampler2DShadow const attribute uniform varying break continue discard return for while do if else struct in out inout"),types:i("float int bool void vec2 vec3 vec4 ivec2 ivec3 ivec4 bvec2 bvec3 bvec4 mat2 mat3 mat4"),blockKeywords:i("for while do if else struct"),builtin:i("radians degrees sin cos tan asin acos atan pow exp log exp2 sqrt inversesqrt abs sign floor ceil fract mod min max clamp mix step smoothstep length distance dot cross normalize ftransform faceforward reflect refract matrixCompMult lessThan lessThanEqual greaterThan greaterThanEqual equal notEqual any all not texture1D texture1DProj texture1DLod texture1DProjLod texture2D texture2DProj texture2DLod texture2DProjLod texture3D texture3DProj texture3DLod texture3DProjLod textureCube textureCubeLod shadow1D shadow2D shadow1DProj shadow2DProj shadow1DLod shadow2DLod shadow1DProjLod shadow2DProjLod dFdx dFdy fwidth noise1 noise2 noise3 noise4"),atoms:i("true false gl_FragColor gl_SecondaryColor gl_Normal gl_Vertex gl_MultiTexCoord0 gl_MultiTexCoord1 gl_MultiTexCoord2 gl_MultiTexCoord3 gl_MultiTexCoord4 gl_MultiTexCoord5 gl_MultiTexCoord6 gl_MultiTexCoord7 gl_FogCoord gl_PointCoord gl_Position gl_PointSize gl_ClipVertex gl_FrontColor gl_BackColor gl_FrontSecondaryColor gl_BackSecondaryColor gl_TexCoord gl_FogFragCoord gl_FragCoord gl_FrontFacing gl_FragData gl_FragDepth gl_ModelViewMatrix gl_ProjectionMatrix gl_ModelViewProjectionMatrix gl_TextureMatrix gl_NormalMatrix gl_ModelViewMatrixInverse gl_ProjectionMatrixInverse gl_ModelViewProjectionMatrixInverse gl_TextureMatrixTranspose gl_ModelViewMatrixInverseTranspose gl_ProjectionMatrixInverseTranspose gl_ModelViewProjectionMatrixInverseTranspose gl_TextureMatrixInverseTranspose gl_NormalScale gl_DepthRange gl_ClipPlane gl_Point gl_FrontMaterial gl_BackMaterial gl_LightSource gl_LightModel gl_FrontLightModelProduct gl_BackLightModelProduct gl_TextureColor gl_EyePlaneS gl_EyePlaneT gl_EyePlaneR gl_EyePlaneQ gl_FogParameters gl_MaxLights gl_MaxClipPlanes gl_MaxTextureUnits gl_MaxTextureCoords gl_MaxVertexAttribs gl_MaxVertexUniformComponents gl_MaxVaryingFloats gl_MaxVertexTextureImageUnits gl_MaxTextureImageUnits gl_MaxFragmentUniformComponents gl_MaxCombineTextureImageUnits gl_MaxDrawBuffers"),indentSwitch:!1,hooks:{"#":k}}),P=o({name:"nesc",keywords:i(s+" as atomic async call command component components configuration event generic implementation includes interface module new norace nx_struct nx_union post provides signal task uses abstract extends"),types:m,blockKeywords:i(y),atoms:i("null true false"),hooks:{"#":k}}),R=o({name:"objectivec",keywords:i(s+" "+u),types:h,builtin:i(d),blockKeywords:i(y+" @synthesize @try @catch @finally @autoreleasepool @synchronized"),defKeywords:i(g+" @interface @implementation @protocol @class"),dontIndentStatements:/^@.*$/,typeFirstDefinitions:!0,atoms:i("YES NO NULL Nil nil true false nullptr"),isReservedIdentifier:v,hooks:{"#":k,"*":b}}),O=o({name:"objectivecpp",keywords:i(s+" "+u+" "+c),types:h,builtin:i(d),blockKeywords:i(y+" @synthesize @try @catch @finally @autoreleasepool @synchronized class try catch"),defKeywords:i(g+" @interface @implementation @protocol @class class namespace"),dontIndentStatements:/^@.*$|^template$/,typeFirstDefinitions:!0,atoms:i("YES NO NULL Nil nil true false nullptr"),isReservedIdentifier:v,hooks:{"#":k,"*":b,u:_,U:_,L:_,R:_,0:w,1:w,2:w,3:w,4:w,5:w,6:w,7:w,8:w,9:w,token:function(e,t,n){if("variable"==n&&"("==e.peek()&&(";"==t.prevToken||null==t.prevToken||"}"==t.prevToken)&&x(e.current()))return"def"}},namespaceSeparator:"::"}),A=o({name:"squirrel",keywords:i("base break clone continue const default delete enum extends function in class foreach local resume return this throw typeof yield constructor instanceof static"),types:m,blockKeywords:i("case catch class else for foreach if switch try while"),defKeywords:i("function local class"),typeFirstDefinitions:!0,atoms:i("true false null"),hooks:{"#":k}});var j=null;function U(e){return function(t,n){for(var r,a=!1,o=!1;!t.eol();){if(!a&&t.match('"')&&("single"==e||t.match('""'))){o=!0;break}if(!a&&t.match("``")){j=U(e),o=!0;break}r=t.next(),a="single"==e&&!a&&"\\"==r}return o&&(n.tokenize=null),"string"}}const $=o({name:"ceylon",keywords:i("abstracts alias assembly assert assign break case catch class continue dynamic else exists extends finally for function given if import in interface is let module new nonempty object of out outer package return satisfies super switch then this throw try value void while"),types:function(e){var t=e.charAt(0);return t===t.toUpperCase()&&t!==t.toLowerCase()},blockKeywords:i("case catch class dynamic else finally for function if interface module new object switch try while"),defKeywords:i("class dynamic function interface module object package value"),builtin:i("abstract actual aliased annotation by default deprecated doc final formal late license native optional sealed see serializable shared suppressWarnings tagged throws variable"),isPunctuationChar:/[\[\]{}\(\),;\:\.`]/,isOperatorChar:/[+\-*&%=<>!?|^~:\/]/,numberStart:/[\d#$]/,number:/^(?:#[\da-fA-F_]+|\$[01_]+|[\d_]+[kMGTPmunpf]?|[\d_]+\.[\d_]+(?:[eE][-+]?\d+|[kMGTPmunpf]|)|)/i,multiLineStrings:!0,typeFirstDefinitions:!0,atoms:i("true false null larger smaller equal empty finished"),indentSwitch:!1,styleDefs:!1,hooks:{"@":function(e){return e.eatWhile(/[\w\$_]/),"meta"},'"':function(e,t){return t.tokenize=U(e.match('""')?"triple":"single"),t.tokenize(e,t)},"`":function(e,t){return!(!j||!e.match("`"))&&(t.tokenize=j,j=null,t.tokenize(e,t))},"'":function(e){return e.match(/^(\\[^'\s]+|[^\\'])'/)?"string.special":(e.eatWhile(/[\w\$_\xa1-\uffff]/),"atom")},token:function(e,t,n){if(("variable"==n||"type"==n)&&"."==t.prevToken)return"variableName.special"}},languageData:{closeBrackets:{brackets:["(","[","{","'",'"','"""']}}});function B(e){(e.interpolationStack||(e.interpolationStack=[])).push(e.tokenize)}function K(e){return(e.interpolationStack||(e.interpolationStack=[])).pop()}function q(e,t,n,r){var a=!1;if(t.eat(e)){if(!t.eat(e))return"string";a=!0}function o(t,n){for(var o=!1;!t.eol();){if(!r&&!o&&"$"==t.peek())return B(n),n.tokenize=V,"string";var i=t.next();if(i==e&&!o&&(!a||t.match(e+e))){n.tokenize=null;break}o=!r&&!o&&"\\"==i}return"string"}return n.tokenize=o,o(t,n)}function V(e,t){return e.eat("$"),e.eat("{")?t.tokenize=null:t.tokenize=W,null}function W(e,t){return e.eatWhile(/[\w_]/),t.tokenize=K(t),"variable"}const G=o({name:"dart",keywords:i("this super static final const abstract class extends external factory implements mixin get native set typedef with enum throw rethrow assert break case continue default in return new deferred async await covariant try catch finally do else for if switch while import library export part of show hide is as extension on yield late required sealed base interface when inline"),blockKeywords:i("try catch finally do else for if switch while"),builtin:i("void bool num int double dynamic var String Null Never"),atoms:i("true false null"),hooks:{"@":function(e){return e.eatWhile(/[\w\$_\.]/),"meta"},"'":function(e,t){return q("'",e,t,!1)},'"':function(e,t){return q('"',e,t,!1)},r:function(e,t){var n=e.peek();return("'"==n||'"'==n)&&q(e.next(),e,t,!0)},"}":function(e,t){return function(e){return e.interpolationStack?e.interpolationStack.length:0}(t)>0&&(t.tokenize=K(t),null)},"/":function(e,t){return!!e.eat("*")&&(t.tokenize=L(1),t.tokenize(e,t))},token:function(e,t,n){if("variable"==n&&RegExp("^[_$]*[A-Z][a-zA-Z0-9_$]*$","g").test(e.current()))return"type"}}});export{N as c,$ as ceylon,o as clike,I as cpp,C as csharp,G as dart,D as java,E as kotlin,P as nesC,R as objectiveC,O as objectiveCpp,M as scala,F as shader,A as squirrel};
