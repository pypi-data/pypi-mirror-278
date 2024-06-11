(window.webpackJsonpfeffery_utils_components=window.webpackJsonpfeffery_utils_components||[]).push([[29],{492:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var react__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(1),react__WEBPACK_IMPORTED_MODULE_0___default=__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__),_components_FefferyShortcutPanel_react__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(176),lodash__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(23),lodash__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(lodash__WEBPACK_IMPORTED_MODULE_2__),ninja_keys__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(906),_components_FefferyStyle_react__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(89);function _typeof(e){return(_typeof="function"==typeof Symbol&&"symbol"==typeof Symbol.iterator?function(e){return typeof e}:function(e){return e&&"function"==typeof Symbol&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e})(e)}function ownKeys(t,e){var n,i=Object.keys(t);return Object.getOwnPropertySymbols&&(n=Object.getOwnPropertySymbols(t),e&&(n=n.filter(function(e){return Object.getOwnPropertyDescriptor(t,e).enumerable})),i.push.apply(i,n)),i}function _objectSpread(t){for(var e=1;e<arguments.length;e++){var n=null!=arguments[e]?arguments[e]:{};e%2?ownKeys(Object(n),!0).forEach(function(e){_defineProperty(t,e,n[e])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):ownKeys(Object(n)).forEach(function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(n,e))})}return t}function _defineProperty(e,t,n){(t=_toPropertyKey(t))in e?Object.defineProperty(e,t,{value:n,enumerable:!0,configurable:!0,writable:!0}):e[t]=n}function _toPropertyKey(e){e=_toPrimitive(e,"string");return"symbol"==_typeof(e)?e:e+""}function _toPrimitive(e,t){if("object"!=_typeof(e)||!e)return e;var n=e[Symbol.toPrimitive];if(void 0===n)return("string"===t?String:Number)(e);n=n.call(e,t||"default");if("object"!=_typeof(n))return n;throw new TypeError("@@toPrimitive must return a primitive value.")}var footerHtmlEn=react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div",{class:"modal-footer",slot:"footer"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{class:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"enter"),"to select"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"})),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"})),"to navigate"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"esc"),"to close"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"backspace"),"move to parent")),footerHtmlZh=react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div",{className:"modal-footer",slot:"footer"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"enter"),"选择"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"})),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("svg",{xmlns:"http://www.w3.org/2000/svg",className:"ninja-examplekey",viewBox:"0 0 24 24"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M0 0h24v24H0V0z",fill:"none"}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("path",{d:"M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z"})),"上下切换"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"esc"),"关闭面板"),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"help"},react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("span",{className:"ninja-examplekey esc"},"backspace"),"回到上一级")),locale2footer=new Map([["en",footerHtmlEn],["zh",footerHtmlZh]]),locale2placeholder=new Map([["en","Type a command or search..."],["zh","输入指令或进行搜索..."]]),FefferyShortcutPanel=function FefferyShortcutPanel(props){var id=props.id,data=props.data,placeholder=props.placeholder,openHotkey=props.openHotkey,theme=props.theme,locale=props.locale,open=props.open,close=props.close,panelStyles=props.panelStyles,setProps=props.setProps,loading_state=props.loading_state,data=data.map(function(e){return Object(lodash__WEBPACK_IMPORTED_MODULE_2__.isString)(e.handler)||e.hasOwnProperty("children")?e:_objectSpread(_objectSpread({},e),{handler:function(){setProps({triggeredHotkey:{id:e.id,timestamp:Date.parse(new Date)}})}})}),ninjaKeys=Object(react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null);return Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){ninjaKeys.current&&ninjaKeys.current.addEventListener("change",function(e){setProps({searchValue:e.detail.search})})},[]),Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){ninjaKeys.current&&(ninjaKeys.current.data=data.map(function(item){return Object(lodash__WEBPACK_IMPORTED_MODULE_2__.isString)(item.handler)?_objectSpread(_objectSpread({},item),{handler:eval(item.handler)}):item}))},[data]),Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){ninjaKeys.current&&open&&(ninjaKeys.current.open(),setProps({open:!1}))},[open]),Object(react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){ninjaKeys.current&&close&&(ninjaKeys.current.close(),setProps({close:!1}))},[close]),panelStyles=_objectSpread(_objectSpread({},{width:"640px",overflowBackground:"rgba(255, 255, 255, 0.5)",textColor:"rgb(60, 65, 73)",fontSize:"16px",top:"20%",accentColor:"rgb(110, 94, 210)",secondaryBackgroundColor:"rgb(239, 241, 244)",secondaryTextColor:"rgb(107, 111, 118)",selectedBackground:"rgb(248, 249, 251)",actionsHeight:"300px",groupTextColor:"rgb(144, 149, 157)",zIndex:1}),panelStyles),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(react__WEBPACK_IMPORTED_MODULE_0___default.a.Fragment,null,react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_components_FefferyStyle_react__WEBPACK_IMPORTED_MODULE_4__.a,{rawStyle:"\nninja-keys {\n    --ninja-width: ".concat(panelStyles.width,";\n    --ninja-overflow-background: ").concat(panelStyles.overflowBackground,";\n    --ninja-text-color: ").concat(panelStyles.textColor,";\n    --ninja-font-size: ").concat(panelStyles.fontSize,";\n    --ninja-top: ").concat(panelStyles.top,";\n    --ninja-accent-color: ").concat(panelStyles.accentColor,";\n    --ninja-secondary-background-color: ").concat(panelStyles.secondaryBackgroundColor,";\n    --ninja-secondary-text-color: ").concat(panelStyles.secondaryTextColor,";\n    --ninja-selected-background: ").concat(panelStyles.selectedBackground,";\n    --ninja-actions-height: ").concat(panelStyles.actionsHeight,";\n    --ninja-group-text-color: ").concat(panelStyles.groupTextColor,";\n    --ninja-z-index: ").concat(panelStyles.zIndex,";\n}\n")}),react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("ninja-keys",{id:id,class:theme,ref:ninjaKeys,placeholder:placeholder||locale2placeholder.get(locale),openHotkey:openHotkey,hotKeysJoinedView:!0,hideBreadcrumbs:!0,"data-dash-is-loading":loading_state&&loading_state.is_loading||void 0},locale2footer.get(locale)))};__webpack_exports__.default=FefferyShortcutPanel,FefferyShortcutPanel.defaultProps=_components_FefferyShortcutPanel_react__WEBPACK_IMPORTED_MODULE_1__.b,FefferyShortcutPanel.propTypes=_components_FefferyShortcutPanel_react__WEBPACK_IMPORTED_MODULE_1__.c},906:function(T,R,e){"use strict";const B=window,L=B.ShadowRoot&&(void 0===B.ShadyCSS||B.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,I=Symbol(),K=new WeakMap;class N{constructor(e,t,n){if(this._$cssResult$=!0,n!==I)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;var t,n=this.t;return L&&void 0===e&&(t=void 0!==n&&1===n.length,void 0===(e=t?K.get(n):e))&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),t)&&K.set(n,e),e}toString(){return this.cssText}}const z=(i,...e)=>{e=1===i.length?i[0]:e.reduce((e,t,n)=>e+(()=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})()+i[n+1],i[0]);return new N(e,i,I)},W=L?e=>e:t=>{if(!(t instanceof CSSStyleSheet))return t;{let e="";for(const n of t.cssRules)e+=n.cssText;return t=e,new N("string"==typeof t?t:t+"",void 0,I)}};const V=window,q=V.trustedTypes,F=q?q.emptyScript:"",J=V.reactiveElementPolyfillSupport,G={toAttribute(e,t){switch(t){case Boolean:e=e?F:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let n=e;switch(t){case Boolean:n=null!==e;break;case Number:n=null===e?null:Number(e);break;case Object:case Array:try{n=JSON.parse(e)}catch(e){n=null}}return n}},Z=(e,t)=>t!==e&&(t==t||e==e),Q={attribute:!0,type:String,converter:G,reflect:!1,hasChanged:Z};class t extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this._$Eu()}static addInitializer(e){var t;this.finalize(),(null!=(t=this.h)?t:this.h=[]).push(e)}static get observedAttributes(){this.finalize();const n=[];return this.elementProperties.forEach((e,t)=>{e=this._$Ep(t,e);void 0!==e&&(this._$Ev.set(e,t),n.push(e))}),n}static createProperty(e,t=Q){var n;t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),t.noAccessor||this.prototype.hasOwnProperty(e)||(n="symbol"==typeof e?Symbol():"__"+e,void 0!==(n=this.getPropertyDescriptor(e,n,t))&&Object.defineProperty(this.prototype,e,n))}static getPropertyDescriptor(n,i,s){return{get(){return this[i]},set(e){var t=this[n];this[i]=e,this.requestUpdate(n,t,s)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||Q}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),void 0!==e.h&&(this.h=[...e.h]),this.elementProperties=new Map(e.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const n of t)this.createProperty(n,e[n])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){var t=[];if(Array.isArray(e)){var n=new Set(e.flat(1/0).reverse());for(const e of n)t.unshift(W(e))}else void 0!==e&&t.push(W(e));return t}static _$Ep(e,t){t=t.attribute;return!1===t?void 0:"string"==typeof t?t:"string"==typeof e?e.toLowerCase():void 0}_$Eu(){var e;this._$E_=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$Eg(),this.requestUpdate(),null!=(e=this.constructor.h)&&e.forEach(e=>e(this))}addController(e){var t;(null!=(t=this._$ES)?t:this._$ES=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&null!=(t=e.hostConnected)&&t.call(e)}removeController(e){var t;null!=(t=this._$ES)&&t.splice(this._$ES.indexOf(e)>>>0,1)}_$Eg(){this.constructor.elementProperties.forEach((e,t)=>{this.hasOwnProperty(t)&&(this._$Ei.set(t,this[t]),delete this[t])})}createRenderRoot(){var i,e,t=null!=(t=this.shadowRoot)?t:this.attachShadow(this.constructor.shadowRootOptions);return i=t,e=this.constructor.elementStyles,L?i.adoptedStyleSheets=e.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet):e.forEach(e=>{var t=document.createElement("style"),n=B.litNonce;void 0!==n&&t.setAttribute("nonce",n),t.textContent=e.cssText,i.appendChild(t)}),t}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null!=(e=this._$ES)&&e.forEach(e=>{var t;return null==(t=e.hostConnected)?void 0:t.call(e)})}enableUpdating(e){}disconnectedCallback(){var e;null!=(e=this._$ES)&&e.forEach(e=>{var t;return null==(t=e.hostDisconnected)?void 0:t.call(e)})}attributeChangedCallback(e,t,n){this._$AK(e,n)}_$EO(e,t,n=Q){var i,s=this.constructor._$Ep(e,n);void 0!==s&&!0===n.reflect&&(i=(void 0!==(null==(i=n.converter)?void 0:i.toAttribute)?n.converter:G).toAttribute(t,n.type),this._$El=e,null==i?this.removeAttribute(s):this.setAttribute(s,i),this._$El=null)}_$AK(e,t){var n=this.constructor,i=n._$Ev.get(e);if(void 0!==i&&this._$El!==i){const e=n.getPropertyOptions(i),s="function"==typeof e.converter?{fromAttribute:e.converter}:void 0!==(null==(n=e.converter)?void 0:n.fromAttribute)?e.converter:G;this._$El=i,this[i]=s.fromAttribute(t,e.type),this._$El=null}}requestUpdate(e,t,n){let i=!0;void 0!==e&&(((n=n||this.constructor.getPropertyOptions(e)).hasChanged||Z)(this[e],t)?(this._$AL.has(e)||this._$AL.set(e,t),!0===n.reflect&&this._$El!==e&&(void 0===this._$EC&&(this._$EC=new Map),this._$EC.set(e,n))):i=!1),!this.isUpdatePending&&i&&(this._$E_=this._$Ej())}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_}catch(e){Promise.reject(e)}var e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(this.isUpdatePending){this.hasUpdated,this._$Ei&&(this._$Ei.forEach((e,t)=>this[t]=e),this._$Ei=void 0);let e=!1;var n=this._$AL;try{(e=this.shouldUpdate(n))?(this.willUpdate(n),null!=(t=this._$ES)&&t.forEach(e=>{var t;return null==(t=e.hostUpdate)?void 0:t.call(e)}),this.update(n)):this._$Ek()}catch(t){throw e=!1,this._$Ek(),t}e&&this._$AE(n)}}willUpdate(e){}_$AE(e){var t;null!=(t=this._$ES)&&t.forEach(e=>{var t;return null==(t=e.hostUpdated)?void 0:t.call(e)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(e){return!0}update(e){void 0!==this._$EC&&(this._$EC.forEach((e,t)=>this._$EO(t,this[t],e)),this._$EC=void 0),this._$Ek()}updated(e){}firstUpdated(e){}}t.finalized=!0,t.elementProperties=new Map,t.elementStyles=[],t.shadowRootOptions={mode:"open"},null!=J&&J({ReactiveElement:t}),(null!=(n=V.reactiveElementVersions)?n:V.reactiveElementVersions=[]).push("1.6.3");const X=window,c=X.trustedTypes,Y=c?c.createPolicy("lit-html",{createHTML:e=>e}):void 0,p=`lit$${(Math.random()+"").slice(9)}$`,ee="?"+p,te=`<${ee}>`,l=document,h=()=>l.createComment(""),d=e=>null===e||"object"!=typeof e&&"function"!=typeof e,ne=Array.isArray,ie=e=>ne(e)||"function"==typeof(null==e?void 0:e[Symbol.iterator]),u=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,se=/-->/g,re=/>/g,_=RegExp(">|[ \t\n\f\r](?:([^\\s\"'>=/]+)([ \t\n\f\r]*=[ \t\n\f\r]*(?:[^ \t\n\f\r\"'`<>=]|(\"|')|))|$)","g"),oe=/'/g,ae=/"/g,le=/^(?:script|style|textarea|title)$/i,ce=n=>(e,...t)=>({_$litType$:n,strings:e,values:t}),r=ce(1),f=(ce(2),Symbol.for("lit-noChange")),v=Symbol.for("lit-nothing"),he=new WeakMap,y=l.createTreeWalker(l,129,null,!1);function de(e,t){if(Array.isArray(e)&&e.hasOwnProperty("raw"))return void 0!==Y?Y.createHTML(t):t;throw Error("invalid template strings array")}const pe=(r,e)=>{const o=r.length-1,a=[];let l,c=2===e?"<svg>":"",h=u;for(let s=0;s<o;s++){const o=r[s];let e,t,n=-1,i=0;for(;i<o.length&&(h.lastIndex=i,null!==(t=h.exec(o)));)i=h.lastIndex,h===u?"!--"===t[1]?h=se:void 0!==t[1]?h=re:void 0!==t[2]?(le.test(t[2])&&(l=RegExp("</"+t[2],"g")),h=_):void 0!==t[3]&&(h=_):h===_?">"===t[0]?(h=null!=l?l:u,n=-1):void 0===t[1]?n=-2:(n=h.lastIndex-t[2].length,e=t[1],h=void 0===t[3]?_:'"'===t[3]?ae:oe):h===ae||h===oe?h=_:h===se||h===re?h=u:(h=_,l=void 0);var d=h===_&&r[s+1].startsWith("/>")?" ":"";c+=h===u?o+te:0<=n?(a.push(e),o.slice(0,n)+"$lit$"+o.slice(n)+p+d):o+p+(-2===n?(a.push(void 0),s):d)}return[de(r,c+(r[o]||"<?>")+(2===e?"</svg>":"")),a]};class ue{constructor({strings:t,_$litType$:n},e){var i;this.parts=[];let s=0,r=0;var o=t.length-1,a=this.parts,[t,l]=pe(t,n);if(this.el=ue.createElement(t,e),y.currentNode=this.el.content,2===n){const t=this.el.content,n=t.firstChild;n.remove(),t.append(...n.childNodes)}for(;null!==(i=y.nextNode())&&a.length<o;){if(1===i.nodeType){if(i.hasAttributes()){const t=[];for(const n of i.getAttributeNames())if(n.endsWith("$lit$")||n.startsWith(p)){const e=l[r++];if(t.push(n),void 0!==e){const t=i.getAttribute(e.toLowerCase()+"$lit$").split(p),n=/([.?@])?(.*)/.exec(e);a.push({type:1,index:s,name:n[2],strings:t,ctor:"."===n[1]?ye:"?"===n[1]?ge:"@"===n[1]?$e:ve})}else a.push({type:6,index:s})}for(const n of t)i.removeAttribute(n)}if(le.test(i.tagName)){const t=i.textContent.split(p),n=t.length-1;if(0<n){i.textContent=c?c.emptyScript:"";for(let e=0;e<n;e++)i.append(t[e],h()),y.nextNode(),a.push({type:2,index:++s});i.append(t[n],h())}}}else if(8===i.nodeType)if(i.data===ee)a.push({type:2,index:s});else{let e=-1;for(;-1!==(e=i.data.indexOf(p,e+1));)a.push({type:7,index:s}),e+=p.length-1}s++}}static createElement(e,t){var n=l.createElement("template");return n.innerHTML=e,n}}function m(t,n,i=t,s){var r;if(n!==f){let e=void 0!==s?null==(o=i._$Co)?void 0:o[s]:i._$Cl;var o=d(n)?void 0:n._$litDirective$;(null==e?void 0:e.constructor)!==o&&(null!=(r=null==e?void 0:e._$AO)&&r.call(e,!1),void 0===o?e=void 0:(e=new o(t))._$AT(t,i,s),void 0!==s?(null!=(r=i._$Co)?r:i._$Co=[])[s]=e:i._$Cl=e),void 0!==e&&(n=m(t,e._$AS(t,n.values),e,s))}return n}class _e{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){var{el:{content:e},parts:n}=this._$AD,i=(null!=(i=null==t?void 0:t.creationScope)?i:l).importNode(e,!0);y.currentNode=i;let s=y.nextNode(),r=0,o=0,a=n[0];for(;void 0!==a;){if(r===a.index){let e;2===a.type?e=new fe(s,s.nextSibling,this,t):1===a.type?e=new a.ctor(s,a.name,a.strings,this,t):6===a.type&&(e=new be(s,this,t)),this._$AV.push(e),a=n[++o]}r!==(null==a?void 0:a.index)&&(s=y.nextNode(),r++)}return y.currentNode=l,i}v(e){let t=0;for(const n of this._$AV)void 0!==n&&(void 0!==n.strings?(n._$AI(e,n,t),t+=n.strings.length-2):n._$AI(e[t])),t++}}class fe{constructor(e,t,n,i){this.type=2,this._$AH=v,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=n,this.options=i,this._$Cp=null==(e=null==i?void 0:i.isConnected)||e}get _$AU(){var e;return null!=(e=null==(e=this._$AM)?void 0:e._$AU)?e:this._$Cp}get parentNode(){let e=this._$AA.parentNode;var t=this._$AM;return e=void 0!==t&&11===(null==e?void 0:e.nodeType)?t.parentNode:e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=m(this,e,t),d(e)?e===v||null==e||""===e?(this._$AH!==v&&this._$AR(),this._$AH=v):e!==this._$AH&&e!==f&&this._(e):void 0!==e._$litType$?this.g(e):void 0!==e.nodeType?this.$(e):ie(e)?this.T(e):this._(e)}k(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}$(e){this._$AH!==e&&(this._$AR(),this._$AH=this.k(e))}_(e){this._$AH!==v&&d(this._$AH)?this._$AA.nextSibling.data=e:this.$(l.createTextNode(e)),this._$AH=e}g(e){var t,{values:n,_$litType$:i}=e,i="number"==typeof i?this._$AC(e):(void 0===i.el&&(i.el=ue.createElement(de(i.h,i.h[0]),this.options)),i);if((null==(t=this._$AH)?void 0:t._$AD)===i)this._$AH.v(n);else{const e=new _e(i,this),t=e.u(this.options);e.v(n),this.$(t),this._$AH=e}}_$AC(e){let t=he.get(e.strings);return void 0===t&&he.set(e.strings,t=new ue(e)),t}T(e){ne(this._$AH)||(this._$AH=[],this._$AR());var t=this._$AH;let n,i=0;for(const s of e)i===t.length?t.push(n=new fe(this.k(h()),this.k(h()),this,this.options)):n=t[i],n._$AI(s),i++;i<t.length&&(this._$AR(n&&n._$AB.nextSibling,i),t.length=i)}_$AR(e=this._$AA.nextSibling,t){var n;for(null!=(n=this._$AP)&&n.call(this,!1,!0,t);e&&e!==this._$AB;){const t=e.nextSibling;e.remove(),e=t}}setConnected(e){var t;void 0===this._$AM&&(this._$Cp=e,null!=(t=this._$AP))&&t.call(this,e)}}class ve{constructor(e,t,n,i,s){this.type=1,this._$AH=v,this._$AN=void 0,this.element=e,this.name=t,this._$AM=i,this.options=s,2<n.length||""!==n[0]||""!==n[1]?(this._$AH=Array(n.length-1).fill(new String),this.strings=n):this._$AH=v}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(n,i=this,s,r){var o=this.strings;let a=!1;if(void 0===o)n=m(this,n,i,0),(a=!d(n)||n!==this._$AH&&n!==f)&&(this._$AH=n);else{const r=n;let e,t;for(n=o[0],e=0;e<o.length-1;e++)(t=m(this,r[s+e],i,e))===f&&(t=this._$AH[e]),a=a||!d(t)||t!==this._$AH[e],t===v?n=v:n!==v&&(n+=(null!=t?t:"")+o[e+1]),this._$AH[e]=t}a&&!r&&this.j(n)}j(e){e===v?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class ye extends ve{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===v?void 0:e}}const me=c?c.emptyScript:"";class ge extends ve{constructor(){super(...arguments),this.type=4}j(e){e&&e!==v?this.element.setAttribute(this.name,me):this.element.removeAttribute(this.name)}}class $e extends ve{constructor(e,t,n,i,s){super(e,t,n,i,s),this.type=5}_$AI(e,t=this){var n,i;(e=null!=(t=m(this,e,t,0))?t:v)!==f&&(t=this._$AH,n=e===v&&t!==v||e.capture!==t.capture||e.once!==t.once||e.passive!==t.passive,i=e!==v&&(t===v||n),n&&this.element.removeEventListener(this.name,this,t),i&&this.element.addEventListener(this.name,this,e),this._$AH=e)}handleEvent(e){var t;"function"==typeof this._$AH?this._$AH.call(null!=(t=null==(t=this.options)?void 0:t.host)?t:this.element,e):this._$AH.handleEvent(e)}}class be{constructor(e,t,n){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=n}get _$AU(){return this._$AM._$AU}_$AI(e){m(this,e)}}var n={O:"$lit$",P:p,A:ee,C:1,M:pe,L:_e,R:ie,D:m,I:fe,V:ve,H:ge,N:$e,U:ye,F:be},i=X.litHtmlPolyfillSupport;null!=i&&i(ue,fe),(null!=(i=X.litHtmlVersions)?i:X.litHtmlVersions=[]).push("2.8.0");class s extends t{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var e,t=super.createRenderRoot();return null==(e=this.renderOptions).renderBefore&&(e.renderBefore=t.firstChild),t}update(e){var t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=((e,t,n)=>{var i,s=null!=(s=null==n?void 0:n.renderBefore)?s:t;let r=s._$litPart$;if(void 0===r){const e=null!=(i=null==n?void 0:n.renderBefore)?i:null;s._$litPart$=r=new fe(t.insertBefore(h(),e),e,void 0,null!=n?n:{})}return r._$AI(e),r})(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null!=(e=this._$Do)&&e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null!=(e=this._$Do)&&e.setConnected(!1)}render(){return f}}s.finalized=!0,s._$litElement$=!0,null!=(i=globalThis.litElementHydrateSupport)&&i.call(globalThis,{LitElement:s});var i=globalThis.litElementPolyfillSupport;null!=i&&i({LitElement:s}),(null!=(i=globalThis.litElementVersions)?i:globalThis.litElementVersions=[]).push("3.3.3");const Ee=s=>e=>{var t,n,i;return"function"!=typeof e?(t=s,{kind:i,elements:n}=e,{kind:i,elements:n,finisher(e){customElements.define(t,e)}}):(i=e,customElements.define(s,i),i)};function o(s){return(e,t)=>{return void 0!==t?void e.constructor.createProperty(t,s):(n=s,"method"!==(i=e).kind||!i.descriptor||"value"in i.descriptor?{kind:"field",key:Symbol(),placement:"own",descriptor:{},originalKey:i.key,initializer(){"function"==typeof i.initializer&&(this[i.key]=i.initializer.call(this))},finisher(e){e.createProperty(i.key,n)}}:{...i,finisher(e){e.createProperty(i.key,n)}});var n,i}}function a(e){return o({...e,state:!0})}null!=(i=window.HTMLSlotElement)&&i.prototype.assignedElements;const Ae=2,we=t=>(...e)=>({_$litDirective$:t,values:e});class ke{constructor(e){}get _$AU(){return this._$AM._$AU}_$AT(e,t,n){this._$Ct=e,this._$AM=t,this._$Ci=n}_$AS(e,t){return this.update(e,t)}update(e,t){return this.render(...t)}}const xe=n["I"],Pe=e=>void 0===e.strings,je=()=>document.createComment(""),Oe=(t,n,i)=>{var s,r=t._$AA.parentNode,o=void 0===n?t._$AB:n._$AA;if(void 0===i){const n=r.insertBefore(je(),o),s=r.insertBefore(je(),o);i=new xe(n,s,t,t.options)}else{const n=i._$AB.nextSibling,a=i._$AM,e=a!==t;if(e){let e;null!=(s=i._$AQ)&&s.call(i,t),i._$AM=t,void 0!==i._$AP&&(e=t._$AU)!==a._$AU&&i._$AP(e)}if(n!==o||e){let e=i._$AA;for(;e!==n;){const n=e.nextSibling;r.insertBefore(e,o),e=n}}}return i},g=(e,t,n=e)=>(e._$AI(t,n),e),Se={},Ce=(e,t=Se)=>e._$AH=t,Me=e=>{var t;null!=(t=e._$AP)&&t.call(e,!1,!0);let n=e._$AA;for(var i=e._$AB.nextSibling;n!==i;){const e=n.nextSibling;n.remove(),n=e}},De=(t,n,i)=>{var s=new Map;for(let e=n;e<=i;e++)s.set(t[e],e);return s},Ue=we(class extends ke{constructor(e){if(super(e),e.type!==Ae)throw Error("repeat() can only be used in text expressions")}ct(e,t,n){let i;void 0===n?n=t:void 0!==t&&(i=t);var s=[],r=[];let o=0;for(const t of e)s[o]=i?i(t,o):o,r[o]=n(t,o),o++;return{values:r,keys:s}}render(e,t,n){return this.ct(e,t,n).values}update(e,[t,n,i]){var s=e._$AH,{values:r,keys:o}=this.ct(t,n,i);if(!Array.isArray(s))return this.ut=o,r;var a=null!=(t=this.ut)?t:this.ut=[],l=[];let c,h,d=0,p=s.length-1,u=0,_=r.length-1;for(;d<=p&&u<=_;)if(null===s[d])d++;else if(null===s[p])p--;else if(a[d]===o[u])l[u]=g(s[d],r[u]),d++,u++;else if(a[p]===o[_])l[_]=g(s[p],r[_]),p--,_--;else if(a[d]===o[_])l[_]=g(s[d],r[_]),Oe(e,l[_+1],s[d]),d++,_--;else if(a[p]===o[u])l[u]=g(s[p],r[u]),Oe(e,s[d],s[p]),p--,u++;else if(void 0===c&&(c=De(o,u,_),h=De(a,d,p)),c.has(a[d]))if(c.has(a[p])){const t=h.get(o[u]),n=void 0!==t?s[t]:null;if(null===n){const t=Oe(e,s[d]);g(t,r[u]),l[u]=t}else l[u]=g(n,r[u]),Oe(e,s[d],n),s[t]=null;u++}else Me(s[p]),p--;else Me(s[d]),d++;for(;u<=_;){const t=Oe(e,l[_+1]);g(t,r[u]),l[u++]=t}for(;d<=p;){const e=s[d++];null!==e&&Me(e)}return this.ut=o,Ce(e,l),f}}),He=we(class extends ke{constructor(e){if(super(e),3!==e.type&&1!==e.type&&4!==e.type)throw Error("The `live` directive is not allowed on child or event bindings");if(!Pe(e))throw Error("`live` bindings can only contain a single expression")}render(e){return e}update(e,[t]){if(t!==f&&t!==v){var n=e.element,i=e.name;if(3===e.type){if(t===n[i])return f}else if(4===e.type){if(!!t===n.hasAttribute(i))return f}else if(1===e.type&&n.getAttribute(i)===t+"")return f;Ce(e)}return t}}),Te=(e,t)=>{var n,i,s=e._$AN;if(void 0===s)return!1;for(const e of s)null!=(i=(n=e)._$AO)&&i.call(n,t,!1),Te(e,t);return!0},Re=e=>{let t,n;for(;void 0!==(t=e._$AM)&&((n=t._$AN).delete(e),e=t,0===(null==n?void 0:n.size)););},Be=n=>{for(let t;t=n._$AM;n=t){let e=t._$AN;if(void 0===e)t._$AN=e=new Set;else if(e.has(n))break;e.add(n),i=t,0,i.type==Ae&&(null==i._$AP&&(i._$AP=Ie),null==i._$AQ)&&(i._$AQ=Le)}var i};function Le(e){void 0!==this._$AN?(Re(this),this._$AM=e,Be(this)):this._$AM=e}function Ie(e,t=!1,n=0){var i=this._$AH,s=this._$AN;if(void 0!==s&&0!==s.size)if(t)if(Array.isArray(i))for(let e=n;e<i.length;e++)Te(i[e],!1),Re(i[e]);else null!=i&&(Te(i,!1),Re(i));else Te(this,e)}class Ke extends ke{constructor(){super(...arguments),this._$AN=void 0}_$AT(e,t,n){super._$AT(e,t,n),Be(this),this.isConnected=e._$AU}_$AO(e,t=!0){var n;e!==this.isConnected&&((this.isConnected=e)?null!=(n=this.reconnected)&&n.call(this):null!=(n=this.disconnected)&&n.call(this)),t&&(Te(this,e),Re(this))}setValue(e){var t;Pe(this._$Ct)?this._$Ct._$AI(e,this):((t=[...this._$Ct._$AH])[this._$Ci]=e,this._$Ct._$AI(t,this,0))}disconnected(){}reconnected(){}}const Ne=()=>new ze;class ze{}const We=new WeakMap,Ve=we(class extends Ke{render(e){return v}update(e,[t]){var n=t!==this.G;return n&&void 0!==this.G&&this.ot(void 0),!n&&this.rt===this.lt||(this.G=t,this.dt=null==(n=e.options)?void 0:n.host,this.ot(this.lt=e.element)),v}ot(t){if("function"==typeof this.G){var n=null!=(n=this.dt)?n:globalThis;let e=We.get(n);void 0===e&&(e=new WeakMap,We.set(n,e)),void 0!==e.get(this.G)&&this.G.call(this.dt,void 0),e.set(this.G,t),void 0!==t&&this.G.call(this.dt,t)}else this.G.value=t}get rt(){var e;return"function"==typeof this.G?null==(e=We.get(null!=(e=this.dt)?e:globalThis))?void 0:e.get(this.G):null==(e=this.G)?void 0:e.value}disconnected(){this.rt===this.lt&&this.ot(void 0)}reconnected(){this.ot(this.lt)}}),qe=we(class extends ke{constructor(e){if(super(e),1!==e.type||"class"!==e.name||2<(null==(e=e.strings)?void 0:e.length))throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.")}render(t){return" "+Object.keys(t).filter(e=>t[e]).join(" ")+" "}update(e,[t]){var n,i;if(void 0===this.it){this.it=new Set,void 0!==e.strings&&(this.nt=new Set(e.strings.join(" ").split(/\s/).filter(e=>""!==e)));for(const e in t)!t[e]||null!=(n=this.nt)&&n.has(e)||this.it.add(e);return this.render(t)}const s=e.element.classList;this.it.forEach(e=>{e in t||(s.remove(e),this.it.delete(e))});for(const e in t){const n=!!t[e];n===this.it.has(e)||null!=(i=this.nt)&&i.has(e)||(n?(s.add(e),this.it.add(e)):(s.remove(e),this.it.delete(e)))}return f}});i="undefined"!=typeof navigator&&0<navigator.userAgent.toLowerCase().indexOf("firefox");function Fe(e,t,n){e.addEventListener?e.addEventListener(t,n,!1):e.attachEvent&&e.attachEvent("on".concat(t),function(){n(window.event)})}function Je(e,t){for(var n=t.slice(0,t.length-1),i=0;i<n.length;i++)n[i]=e[n[i].toLowerCase()];return n}function Ge(e){for(var t=(e=(e="string"!=typeof e?"":e).replace(/\s/g,"")).split(","),n=t.lastIndexOf("");0<=n;)t[n-1]+=",",t.splice(n,1),n=t.lastIndexOf("");return t}for(var Ze={backspace:8,tab:9,clear:12,enter:13,return:13,esc:27,escape:27,space:32,left:37,up:38,right:39,down:40,del:46,delete:46,ins:45,insert:45,home:36,end:35,pageup:33,pagedown:34,capslock:20,num_0:96,num_1:97,num_2:98,num_3:99,num_4:100,num_5:101,num_6:102,num_7:103,num_8:104,num_9:105,num_multiply:106,num_add:107,num_enter:108,num_subtract:109,num_decimal:110,num_divide:111,"⇪":20,",":188,".":190,"/":191,"`":192,"-":i?173:189,"=":i?61:187,";":i?59:186,"'":222,"[":219,"]":221,"\\":220},$={"⇧":16,shift:16,"⌥":18,alt:18,option:18,"⌃":17,ctrl:17,control:17,"⌘":91,cmd:91,command:91},Qe={16:"shiftKey",18:"altKey",17:"ctrlKey",91:"metaKey",shiftKey:16,ctrlKey:17,altKey:18,metaKey:91},b={16:!1,18:!1,17:!1,91:!1},E={},Xe=1;Xe<20;Xe++)Ze["f".concat(Xe)]=111+Xe;var A=[],Ye="all",et=[],tt=function(e){return Ze[e.toLowerCase()]||$[e.toLowerCase()]||e.toUpperCase().charCodeAt(0)};function nt(e){Ye=e||"all"}function it(){return Ye||"all"}function st(e){var t=e.key,i=e.scope,s=e.method,o=void 0===(e=e.splitKey)?"+":e;Ge(t).forEach(function(e){var r,e=e.split(o),t=e.length,n=e[t-1],n="*"===n?"*":tt(n);E[n]&&(i=i||it(),r=1<t?Je($,e):[],E[n]=E[n].map(function(e){return s&&e.method!==s||e.scope!==i||!function(e){for(var t=e.length>=r.length?e:r,n=e.length>=r.length?r:e,i=!0,s=0;s<t.length;s++)-1===n.indexOf(t[s])&&(i=!1);return i}(e.mods)?e:{}}))})}function rt(e,t,n){var i;if(t.scope===n||"all"===t.scope){for(var s in i=0<t.mods.length,b)Object.prototype.hasOwnProperty.call(b,s)&&(!b[s]&&-1<t.mods.indexOf(+s)||b[s]&&-1===t.mods.indexOf(+s))&&(i=!1);(0!==t.mods.length||b[16]||b[18]||b[17]||b[91])&&!i&&"*"!==t.shortcut||!1===t.method(e,t)&&(e.preventDefault?e.preventDefault():e.returnValue=!1,e.stopPropagation&&e.stopPropagation(),e.cancelBubble)&&(e.cancelBubble=!0)}}function ot(n){var e=E["*"],t=n.keyCode||n.which||n.charCode;if(w.filter.call(this,n)){if(-1===A.indexOf(t=93!==t&&224!==t?t:91)&&229!==t&&A.push(t),["ctrlKey","altKey","shiftKey","metaKey"].forEach(function(e){var t=Qe[e];n[e]&&-1===A.indexOf(t)?A.push(t):!n[e]&&-1<A.indexOf(t)?A.splice(A.indexOf(t),1):"metaKey"!==e||!n[e]||3!==A.length||n.ctrlKey||n.shiftKey||n.altKey||(A=A.slice(A.indexOf(t)))}),t in b){for(var i in b[t]=!0,$)$[i]===t&&(w[i]=!0);if(!e)return}for(var s in b)Object.prototype.hasOwnProperty.call(b,s)&&(b[s]=n[Qe[s]]);n.getModifierState&&(!n.altKey||n.ctrlKey)&&n.getModifierState("AltGraph")&&(-1===A.indexOf(17)&&A.push(17),-1===A.indexOf(18)&&A.push(18),b[17]=!0,b[18]=!0);var r=it();if(e)for(var o=0;o<e.length;o++)e[o].scope===r&&("keydown"===n.type&&e[o].keydown||"keyup"===n.type&&e[o].keyup)&&rt(n,e[o],r);if(t in E)for(var a=0;a<E[t].length;a++)if(("keydown"===n.type&&E[t][a].keydown||"keyup"===n.type&&E[t][a].keyup)&&E[t][a].key){for(var l=E[t][a],c=l.splitKey,h=l.key.split(c),d=[],p=0;p<h.length;p++)d.push(tt(h[p]));d.sort().join("")===A.sort().join("")&&rt(n,l,r)}}}function w(e,t,n){A=[];var i=Ge(e),s=[],r="all",o=document,a=0,l=!1,c=!0,h="+";for(void 0===n&&"function"==typeof t&&(n=t),"[object Object]"===Object.prototype.toString.call(t)&&(t.scope&&(r=t.scope),t.element&&(o=t.element),t.keyup&&(l=t.keyup),void 0!==t.keydown&&(c=t.keydown),"string"==typeof t.splitKey)&&(h=t.splitKey),"string"==typeof t&&(r=t);a<i.length;a++)s=[],1<(e=i[a].split(h)).length&&(s=Je($,e)),(e="*"===(e=e[e.length-1])?"*":tt(e))in E||(E[e]=[]),E[e].push({keyup:l,keydown:c,scope:r,mods:s,shortcut:i[a],method:n,key:i[a],splitKey:h});void 0===o||(t=o,-1<et.indexOf(t))||!window||(et.push(o),Fe(o,"keydown",function(e){ot(e)}),Fe(window,"focus",function(){A=[]}),Fe(o,"keyup",function(e){ot(e);var t=e.keyCode||e.which||e.charCode,n=A.indexOf(t);if(0<=n&&A.splice(n,1),e.key&&"meta"===e.key.toLowerCase()&&A.splice(0,A.length),(t=93!==t&&224!==t?t:91)in b)for(var i in b[t]=!1,$)$[i]===t&&(w[i]=!1)}))}var at,lt,ct={setScope:nt,getScope:it,deleteScope:function(e,t){var n,i,s;for(s in e=e||it(),E)if(Object.prototype.hasOwnProperty.call(E,s))for(n=E[s],i=0;i<n.length;)n[i].scope===e?n.splice(i,1):i++;it()===e&&nt(t||"all")},getPressedKeyCodes:function(){return A.slice(0)},isPressed:function(e){return"string"==typeof e&&(e=tt(e)),-1!==A.indexOf(e)},filter:function(e){var e=e.target||e.srcElement,t=e.tagName,n=!0;return n=!e.isContentEditable&&("INPUT"!==t&&"TEXTAREA"!==t&&"SELECT"!==t||e.readOnly)?n:!1},unbind:function(e){if(e){if(Array.isArray(e))e.forEach(function(e){e.key&&st(e)});else if("object"==typeof e)e.key&&st(e);else if("string"==typeof e){for(var t=arguments.length,n=new Array(1<t?t-1:0),i=1;i<t;i++)n[i-1]=arguments[i];var s=n[0],r=n[1];"function"==typeof s&&(r=s,s=""),st({key:e,scope:s,method:r,splitKey:"+"})}}else Object.keys(E).forEach(function(e){return delete E[e]})}};for(at in ct)Object.prototype.hasOwnProperty.call(ct,at)&&(w[at]=ct[at]);"undefined"!=typeof window&&(lt=window.hotkeys,w.noConflict=function(e){return e&&window.hotkeys===w&&(window.hotkeys=lt),w},window.hotkeys=w);function ht(e,t,n,i){var s,r=arguments.length,o=r<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,n):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,n,i);else for(var a=e.length-1;0<=a;a--)(s=e[a])&&(o=(r<3?s(o):3<r?s(t,n,o):s(t,n))||o);return 3<r&&o&&Object.defineProperty(t,n,o),o}var k=w,n=class extends s{constructor(){super(...arguments),this.placeholder="",this.hideBreadcrumbs=!1,this.breadcrumbHome="Home",this.breadcrumbs=[],this._inputRef=Ne()}render(){let e="";if(!this.hideBreadcrumbs){var t=[];for(const e of this.breadcrumbs)t.push(r`<button
            tabindex="-1"
            @click=${()=>this.selectParent(e)}
            class="breadcrumb"
          >
            ${e}
          </button>`);e=r`<div class="breadcrumb-list">
        <button
          tabindex="-1"
          @click=${()=>this.selectParent()}
          class="breadcrumb"
        >
          ${this.breadcrumbHome}
        </button>
        ${t}
      </div>`}return r`
      ${e}
      <div part="ninja-input-wrapper" class="search-wrapper">
        <input
          part="ninja-input"
          type="text"
          id="search"
          spellcheck="false"
          autocomplete="off"
          @input="${this._handleInput}"
          ${Ve(this._inputRef)}
          placeholder="${this.placeholder}"
          class="search"
        />
      </div>
    `}setSearch(e){this._inputRef.value&&(this._inputRef.value.value=e)}focusSearch(){requestAnimationFrame(()=>this._inputRef.value.focus())}_handleInput(e){e=e.target;this.dispatchEvent(new CustomEvent("change",{detail:{search:e.value},bubbles:!1,composed:!1}))}selectParent(e){this.dispatchEvent(new CustomEvent("setParent",{detail:{parent:e},bubbles:!0,composed:!0}))}firstUpdated(){this.focusSearch()}_close(){this.dispatchEvent(new CustomEvent("close",{bubbles:!0,composed:!0}))}};n.styles=z`
    :host {
      flex: 1;
      position: relative;
    }
    .search {
      padding: 1.25em;
      flex-grow: 1;
      flex-shrink: 0;
      margin: 0px;
      border: none;
      appearance: none;
      font-size: 1.125em;
      background: transparent;
      caret-color: var(--ninja-accent-color);
      color: var(--ninja-text-color);
      outline: none;
      font-family: var(--ninja-font-family);
    }
    .search::placeholder {
      color: var(--ninja-placeholder-color);
    }
    .breadcrumb-list {
      padding: 1em 4em 0 1em;
      display: flex;
      flex-direction: row;
      align-items: stretch;
      justify-content: flex-start;
      flex: initial;
    }

    .breadcrumb {
      background: var(--ninja-secondary-background-color);
      text-align: center;
      line-height: 1.2em;
      border-radius: var(--ninja-key-border-radius);
      border: 0;
      cursor: pointer;
      padding: 0.1em 0.5em;
      color: var(--ninja-secondary-text-color);
      margin-right: 0.5em;
      outline: none;
      font-family: var(--ninja-font-family);
    }

    .search-wrapper {
      display: flex;
      border-bottom: var(--ninja-separate-border);
    }
  `,ht([o()],n.prototype,"placeholder",void 0),ht([o({type:Boolean})],n.prototype,"hideBreadcrumbs",void 0),ht([o()],n.prototype,"breadcrumbHome",void 0),ht([o({type:Array})],n.prototype,"breadcrumbs",void 0),ht([Ee("ninja-header")],n);class dt extends ke{constructor(e){if(super(e),this.et=v,e.type!==Ae)throw Error(this.constructor.directiveName+"() can only be used in child bindings")}render(e){if(e===v||null==e)return this.ft=void 0,this.et=e;if(e===f)return e;if("string"!=typeof e)throw Error(this.constructor.directiveName+"() called with a non-string value");return e===this.et?this.ft:(e=[this.et=e],this.ft={_$litType$:this.constructor.resultType,strings:e.raw=e,values:[]})}}dt.directiveName="unsafeHTML",dt.resultType=1;const pt=we(dt);i=e(2);const ut=window,_t=ut.ShadowRoot&&(void 0===ut.ShadyCSS||ut.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,ft=Symbol(),vt=new WeakMap;class yt{constructor(e,t,n){if(this._$cssResult$=!0,n!==ft)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=e,this.t=t}get styleSheet(){let e=this.o;var t,n=this.t;return _t&&void 0===e&&(t=void 0!==n&&1===n.length,void 0===(e=t?vt.get(n):e))&&((this.o=e=new CSSStyleSheet).replaceSync(this.cssText),t)&&vt.set(n,e),e}toString(){return this.cssText}}const mt=_t?e=>e:t=>{if(!(t instanceof CSSStyleSheet))return t;{let e="";for(const n of t.cssRules)e+=n.cssText;return t=e,new yt("string"==typeof t?t:t+"",void 0,ft)}},gt=window,$t=gt.trustedTypes,bt=$t?$t.emptyScript:"",Et=gt.reactiveElementPolyfillSupport,At={toAttribute(e,t){switch(t){case Boolean:e=e?bt:null;break;case Object:case Array:e=null==e?e:JSON.stringify(e)}return e},fromAttribute(e,t){let n=e;switch(t){case Boolean:n=null!==e;break;case Number:n=null===e?null:Number(e);break;case Object:case Array:try{n=JSON.parse(e)}catch(e){n=null}}return n}},wt=(e,t)=>t!==e&&(t==t||e==e),kt={attribute:!0,type:String,converter:At,reflect:!1,hasChanged:wt};class x extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this._$Eu()}static addInitializer(e){var t;this.finalize(),(null!=(t=this.h)?t:this.h=[]).push(e)}static get observedAttributes(){this.finalize();const n=[];return this.elementProperties.forEach((e,t)=>{e=this._$Ep(t,e);void 0!==e&&(this._$Ev.set(e,t),n.push(e))}),n}static createProperty(e,t=kt){var n;t.state&&(t.attribute=!1),this.finalize(),this.elementProperties.set(e,t),t.noAccessor||this.prototype.hasOwnProperty(e)||(n="symbol"==typeof e?Symbol():"__"+e,void 0!==(n=this.getPropertyDescriptor(e,n,t))&&Object.defineProperty(this.prototype,e,n))}static getPropertyDescriptor(n,i,s){return{get(){return this[i]},set(e){var t=this[n];this[i]=e,this.requestUpdate(n,t,s)},configurable:!0,enumerable:!0}}static getPropertyOptions(e){return this.elementProperties.get(e)||kt}static finalize(){if(this.hasOwnProperty("finalized"))return!1;this.finalized=!0;const e=Object.getPrototypeOf(this);if(e.finalize(),void 0!==e.h&&(this.h=[...e.h]),this.elementProperties=new Map(e.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const e=this.properties,t=[...Object.getOwnPropertyNames(e),...Object.getOwnPropertySymbols(e)];for(const n of t)this.createProperty(n,e[n])}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(e){var t=[];if(Array.isArray(e)){var n=new Set(e.flat(1/0).reverse());for(const e of n)t.unshift(mt(e))}else void 0!==e&&t.push(mt(e));return t}static _$Ep(e,t){t=t.attribute;return!1===t?void 0:"string"==typeof t?t:"string"==typeof e?e.toLowerCase():void 0}_$Eu(){var e;this._$E_=new Promise(e=>this.enableUpdating=e),this._$AL=new Map,this._$Eg(),this.requestUpdate(),null!=(e=this.constructor.h)&&e.forEach(e=>e(this))}addController(e){var t;(null!=(t=this._$ES)?t:this._$ES=[]).push(e),void 0!==this.renderRoot&&this.isConnected&&null!=(t=e.hostConnected)&&t.call(e)}removeController(e){var t;null!=(t=this._$ES)&&t.splice(this._$ES.indexOf(e)>>>0,1)}_$Eg(){this.constructor.elementProperties.forEach((e,t)=>{this.hasOwnProperty(t)&&(this._$Ei.set(t,this[t]),delete this[t])})}createRenderRoot(){var i,e,t=null!=(t=this.shadowRoot)?t:this.attachShadow(this.constructor.shadowRootOptions);return i=t,e=this.constructor.elementStyles,_t?i.adoptedStyleSheets=e.map(e=>e instanceof CSSStyleSheet?e:e.styleSheet):e.forEach(e=>{var t=document.createElement("style"),n=ut.litNonce;void 0!==n&&t.setAttribute("nonce",n),t.textContent=e.cssText,i.appendChild(t)}),t}connectedCallback(){var e;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null!=(e=this._$ES)&&e.forEach(e=>{var t;return null==(t=e.hostConnected)?void 0:t.call(e)})}enableUpdating(e){}disconnectedCallback(){var e;null!=(e=this._$ES)&&e.forEach(e=>{var t;return null==(t=e.hostDisconnected)?void 0:t.call(e)})}attributeChangedCallback(e,t,n){this._$AK(e,n)}_$EO(e,t,n=kt){var i,s=this.constructor._$Ep(e,n);void 0!==s&&!0===n.reflect&&(i=(void 0!==(null==(i=n.converter)?void 0:i.toAttribute)?n.converter:At).toAttribute(t,n.type),this._$El=e,null==i?this.removeAttribute(s):this.setAttribute(s,i),this._$El=null)}_$AK(e,t){var n=this.constructor,i=n._$Ev.get(e);if(void 0!==i&&this._$El!==i){const e=n.getPropertyOptions(i),s="function"==typeof e.converter?{fromAttribute:e.converter}:void 0!==(null==(n=e.converter)?void 0:n.fromAttribute)?e.converter:At;this._$El=i,this[i]=s.fromAttribute(t,e.type),this._$El=null}}requestUpdate(e,t,n){let i=!0;void 0!==e&&(((n=n||this.constructor.getPropertyOptions(e)).hasChanged||wt)(this[e],t)?(this._$AL.has(e)||this._$AL.set(e,t),!0===n.reflect&&this._$El!==e&&(void 0===this._$EC&&(this._$EC=new Map),this._$EC.set(e,n))):i=!1),!this.isUpdatePending&&i&&(this._$E_=this._$Ej())}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_}catch(e){Promise.reject(e)}var e=this.scheduleUpdate();return null!=e&&await e,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(this.isUpdatePending){this.hasUpdated,this._$Ei&&(this._$Ei.forEach((e,t)=>this[t]=e),this._$Ei=void 0);let e=!1;var n=this._$AL;try{(e=this.shouldUpdate(n))?(this.willUpdate(n),null!=(t=this._$ES)&&t.forEach(e=>{var t;return null==(t=e.hostUpdate)?void 0:t.call(e)}),this.update(n)):this._$Ek()}catch(t){throw e=!1,this._$Ek(),t}e&&this._$AE(n)}}willUpdate(e){}_$AE(e){var t;null!=(t=this._$ES)&&t.forEach(e=>{var t;return null==(t=e.hostUpdated)?void 0:t.call(e)}),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(e)),this.updated(e)}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(e){return!0}update(e){void 0!==this._$EC&&(this._$EC.forEach((e,t)=>this._$EO(t,this[t],e)),this._$EC=void 0),this._$Ek()}updated(e){}firstUpdated(e){}}x.finalized=!0,x.elementProperties=new Map,x.elementStyles=[],x.shadowRootOptions={mode:"open"},null!=Et&&Et({ReactiveElement:x}),(null!=(n=gt.reactiveElementVersions)?n:gt.reactiveElementVersions=[]).push("1.6.3");const xt=window,P=xt.trustedTypes,Pt=P?P.createPolicy("lit-html",{createHTML:e=>e}):void 0,j=`lit$${(Math.random()+"").slice(9)}$`,jt="?"+j,Ot=`<${jt}>`,O=document,St=()=>O.createComment(""),Ct=e=>null===e||"object"!=typeof e&&"function"!=typeof e,Mt=Array.isArray,Dt=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,Ut=/-->/g,Ht=/>/g,S=RegExp(">|[ \t\n\f\r](?:([^\\s\"'>=/]+)([ \t\n\f\r]*=[ \t\n\f\r]*(?:[^ \t\n\f\r\"'`<>=]|(\"|')|))|$)","g"),Tt=/'/g,Rt=/"/g,Bt=/^(?:script|style|textarea|title)$/i,Lt=n=>(e,...t)=>({_$litType$:n,strings:e,values:t}),It=Lt(1),C=(Lt(2),Symbol.for("lit-noChange")),M=Symbol.for("lit-nothing"),Kt=new WeakMap,D=O.createTreeWalker(O,129,null,!1);function Nt(e,t){if(Array.isArray(e)&&e.hasOwnProperty("raw"))return void 0!==Pt?Pt.createHTML(t):t;throw Error("invalid template strings array")}class zt{constructor({strings:t,_$litType$:n},e){var i;this.parts=[];let s=0,r=0;var o=t.length-1,a=this.parts,[t,l]=((r,e)=>{const o=r.length-1,a=[];let l,c=2===e?"<svg>":"",h=Dt;for(let s=0;s<o;s++){const o=r[s];let e,t,n=-1,i=0;for(;i<o.length&&(h.lastIndex=i,null!==(t=h.exec(o)));)i=h.lastIndex,h===Dt?"!--"===t[1]?h=Ut:void 0!==t[1]?h=Ht:void 0!==t[2]?(Bt.test(t[2])&&(l=RegExp("</"+t[2],"g")),h=S):void 0!==t[3]&&(h=S):h===S?">"===t[0]?(h=null!=l?l:Dt,n=-1):void 0===t[1]?n=-2:(n=h.lastIndex-t[2].length,e=t[1],h=void 0===t[3]?S:'"'===t[3]?Rt:Tt):h===Rt||h===Tt?h=S:h===Ut||h===Ht?h=Dt:(h=S,l=void 0);var d=h===S&&r[s+1].startsWith("/>")?" ":"";c+=h===Dt?o+Ot:0<=n?(a.push(e),o.slice(0,n)+"$lit$"+o.slice(n)+j+d):o+j+(-2===n?(a.push(void 0),s):d)}return[Nt(r,c+(r[o]||"<?>")+(2===e?"</svg>":"")),a]})(t,n);if(this.el=zt.createElement(t,e),D.currentNode=this.el.content,2===n){const t=this.el.content,n=t.firstChild;n.remove(),t.append(...n.childNodes)}for(;null!==(i=D.nextNode())&&a.length<o;){if(1===i.nodeType){if(i.hasAttributes()){const t=[];for(const n of i.getAttributeNames())if(n.endsWith("$lit$")||n.startsWith(j)){const e=l[r++];if(t.push(n),void 0!==e){const t=i.getAttribute(e.toLowerCase()+"$lit$").split(j),n=/([.?@])?(.*)/.exec(e);a.push({type:1,index:s,name:n[2],strings:t,ctor:"."===n[1]?Ft:"?"===n[1]?Gt:"@"===n[1]?Zt:qt})}else a.push({type:6,index:s})}for(const n of t)i.removeAttribute(n)}if(Bt.test(i.tagName)){const t=i.textContent.split(j),n=t.length-1;if(0<n){i.textContent=P?P.emptyScript:"";for(let e=0;e<n;e++)i.append(t[e],St()),D.nextNode(),a.push({type:2,index:++s});i.append(t[n],St())}}}else if(8===i.nodeType)if(i.data===jt)a.push({type:2,index:s});else{let e=-1;for(;-1!==(e=i.data.indexOf(j,e+1));)a.push({type:7,index:s}),e+=j.length-1}s++}}static createElement(e,t){var n=O.createElement("template");return n.innerHTML=e,n}}function U(t,n,i=t,s){var r;if(n!==C){let e=void 0!==s?null==(o=i._$Co)?void 0:o[s]:i._$Cl;var o=Ct(n)?void 0:n._$litDirective$;(null==e?void 0:e.constructor)!==o&&(null!=(r=null==e?void 0:e._$AO)&&r.call(e,!1),void 0===o?e=void 0:(e=new o(t))._$AT(t,i,s),void 0!==s?(null!=(r=i._$Co)?r:i._$Co=[])[s]=e:i._$Cl=e),void 0!==e&&(n=U(t,e._$AS(t,n.values),e,s))}return n}class Wt{constructor(e,t){this._$AV=[],this._$AN=void 0,this._$AD=e,this._$AM=t}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}u(t){var{el:{content:e},parts:n}=this._$AD,i=(null!=(i=null==t?void 0:t.creationScope)?i:O).importNode(e,!0);D.currentNode=i;let s=D.nextNode(),r=0,o=0,a=n[0];for(;void 0!==a;){if(r===a.index){let e;2===a.type?e=new Vt(s,s.nextSibling,this,t):1===a.type?e=new a.ctor(s,a.name,a.strings,this,t):6===a.type&&(e=new Qt(s,this,t)),this._$AV.push(e),a=n[++o]}r!==(null==a?void 0:a.index)&&(s=D.nextNode(),r++)}return D.currentNode=O,i}v(e){let t=0;for(const n of this._$AV)void 0!==n&&(void 0!==n.strings?(n._$AI(e,n,t),t+=n.strings.length-2):n._$AI(e[t])),t++}}class Vt{constructor(e,t,n,i){this.type=2,this._$AH=M,this._$AN=void 0,this._$AA=e,this._$AB=t,this._$AM=n,this.options=i,this._$Cp=null==(e=null==i?void 0:i.isConnected)||e}get _$AU(){var e;return null!=(e=null==(e=this._$AM)?void 0:e._$AU)?e:this._$Cp}get parentNode(){let e=this._$AA.parentNode;var t=this._$AM;return e=void 0!==t&&11===(null==e?void 0:e.nodeType)?t.parentNode:e}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(e,t=this){e=U(this,e,t),Ct(e)?e===M||null==e||""===e?(this._$AH!==M&&this._$AR(),this._$AH=M):e!==this._$AH&&e!==C&&this._(e):void 0!==e._$litType$?this.g(e):void 0!==e.nodeType?this.$(e):(t=e,Mt(t)||"function"==typeof(null==t?void 0:t[Symbol.iterator])?this.T(e):this._(e))}k(e){return this._$AA.parentNode.insertBefore(e,this._$AB)}$(e){this._$AH!==e&&(this._$AR(),this._$AH=this.k(e))}_(e){this._$AH!==M&&Ct(this._$AH)?this._$AA.nextSibling.data=e:this.$(O.createTextNode(e)),this._$AH=e}g(e){var t,{values:n,_$litType$:i}=e,i="number"==typeof i?this._$AC(e):(void 0===i.el&&(i.el=zt.createElement(Nt(i.h,i.h[0]),this.options)),i);if((null==(t=this._$AH)?void 0:t._$AD)===i)this._$AH.v(n);else{const e=new Wt(i,this),t=e.u(this.options);e.v(n),this.$(t),this._$AH=e}}_$AC(e){let t=Kt.get(e.strings);return void 0===t&&Kt.set(e.strings,t=new zt(e)),t}T(e){Mt(this._$AH)||(this._$AH=[],this._$AR());var t=this._$AH;let n,i=0;for(const s of e)i===t.length?t.push(n=new Vt(this.k(St()),this.k(St()),this,this.options)):n=t[i],n._$AI(s),i++;i<t.length&&(this._$AR(n&&n._$AB.nextSibling,i),t.length=i)}_$AR(e=this._$AA.nextSibling,t){var n;for(null!=(n=this._$AP)&&n.call(this,!1,!0,t);e&&e!==this._$AB;){const t=e.nextSibling;e.remove(),e=t}}setConnected(e){var t;void 0===this._$AM&&(this._$Cp=e,null!=(t=this._$AP))&&t.call(this,e)}}class qt{constructor(e,t,n,i,s){this.type=1,this._$AH=M,this._$AN=void 0,this.element=e,this.name=t,this._$AM=i,this.options=s,2<n.length||""!==n[0]||""!==n[1]?(this._$AH=Array(n.length-1).fill(new String),this.strings=n):this._$AH=M}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(n,i=this,s,r){var o=this.strings;let a=!1;if(void 0===o)n=U(this,n,i,0),(a=!Ct(n)||n!==this._$AH&&n!==C)&&(this._$AH=n);else{const r=n;let e,t;for(n=o[0],e=0;e<o.length-1;e++)(t=U(this,r[s+e],i,e))===C&&(t=this._$AH[e]),a=a||!Ct(t)||t!==this._$AH[e],t===M?n=M:n!==M&&(n+=(null!=t?t:"")+o[e+1]),this._$AH[e]=t}a&&!r&&this.j(n)}j(e){e===M?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=e?e:"")}}class Ft extends qt{constructor(){super(...arguments),this.type=3}j(e){this.element[this.name]=e===M?void 0:e}}const Jt=P?P.emptyScript:"";class Gt extends qt{constructor(){super(...arguments),this.type=4}j(e){e&&e!==M?this.element.setAttribute(this.name,Jt):this.element.removeAttribute(this.name)}}class Zt extends qt{constructor(e,t,n,i,s){super(e,t,n,i,s),this.type=5}_$AI(e,t=this){var n,i;(e=null!=(t=U(this,e,t,0))?t:M)!==C&&(t=this._$AH,n=e===M&&t!==M||e.capture!==t.capture||e.once!==t.once||e.passive!==t.passive,i=e!==M&&(t===M||n),n&&this.element.removeEventListener(this.name,this,t),i&&this.element.addEventListener(this.name,this,e),this._$AH=e)}handleEvent(e){var t;"function"==typeof this._$AH?this._$AH.call(null!=(t=null==(t=this.options)?void 0:t.host)?t:this.element,e):this._$AH.handleEvent(e)}}class Qt{constructor(e,t,n){this.element=e,this.type=6,this._$AN=void 0,this._$AM=t,this.options=n}get _$AU(){return this._$AM._$AU}_$AI(e){U(this,e)}}var e=xt.litHtmlPolyfillSupport;null!=e&&e(zt,Vt),(null!=(n=xt.litHtmlVersions)?n:xt.litHtmlVersions=[]).push("2.8.0");class Xt extends x{constructor(){super(...arguments),this.renderOptions={host:this},this._$Do=void 0}createRenderRoot(){var e,t=super.createRenderRoot();return null==(e=this.renderOptions).renderBefore&&(e.renderBefore=t.firstChild),t}update(e){var t=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(e),this._$Do=((e,t,n)=>{var i,s=null!=(s=null==n?void 0:n.renderBefore)?s:t;let r=s._$litPart$;if(void 0===r){const e=null!=(i=null==n?void 0:n.renderBefore)?i:null;s._$litPart$=r=new Vt(t.insertBefore(St(),e),e,void 0,null!=n?n:{})}return r._$AI(e),r})(t,this.renderRoot,this.renderOptions)}connectedCallback(){var e;super.connectedCallback(),null!=(e=this._$Do)&&e.setConnected(!0)}disconnectedCallback(){var e;super.disconnectedCallback(),null!=(e=this._$Do)&&e.setConnected(!1)}render(){return C}}Xt.finalized=!0,Xt._$litElement$=!0,null!=(e=globalThis.litElementHydrateSupport)&&e.call(globalThis,{LitElement:Xt});function Yt(e,t,n,i){var s,r=arguments.length,o=r<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,n):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,n,i);else for(var a=e.length-1;0<=a;a--)(s=e[a])&&(o=(r<3?s(o):3<r?s(t,n,o):s(t,n))||o);return 3<r&&o&&Object.defineProperty(t,n,o),o}n=globalThis.litElementPolyfillSupport,null!=n&&n({LitElement:Xt}),(null!=(e=globalThis.litElementVersions)?e:globalThis.litElementVersions=[]).push("3.3.3"),null!=(n=window.HTMLSlotElement)&&n.prototype.assignedElements,e=((i,...e)=>{e=1===i.length?i[0]:e.reduce((e,t,n)=>e+(()=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})()+i[n+1],i[0]);return new yt(e,i,ft)})`:host{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}`,n=class extends Xt{render(){return It`<span><slot></slot></span>`}},n.styles=[e],Object(i.c)([e=>{var t,n;return"function"!=typeof e?({kind:n,elements:t}=e,{kind:n,elements:t,finisher(e){customElements.define("mwc-icon",e)}}):(n=e,customElements.define("mwc-icon",n),n)}],n),e=class extends s{constructor(){super(),this.selected=!1,this.hotKeysJoinedView=!0,this.addEventListener("click",this.click)}ensureInView(){requestAnimationFrame(()=>this.scrollIntoView({block:"nearest"}))}click(){this.dispatchEvent(new CustomEvent("actionsSelected",{detail:this.action,bubbles:!0,composed:!0}))}updated(e){e.has("selected")&&this.selected&&this.ensureInView()}render(){let e,t;this.action.mdIcon?e=r`<mwc-icon part="ninja-icon" class="ninja-icon"
        >${this.action.mdIcon}</mwc-icon
      >`:this.action.icon&&(e=pt(this.action.icon||"")),this.action.hotkey&&(t=this.hotKeysJoinedView?this.action.hotkey.split(",").map(e=>{e=e.split("+"),e=r`${function*(t){if(void 0!==t){let e=-1;for(const n of t)-1<e&&(yield"+"),e++,yield n}}(e.map(e=>r`<kbd>${e}</kbd>`))}`;return r`<div class="ninja-hotkey ninja-hotkeys">
            ${e}
          </div>`}):this.action.hotkey.split(",").map(e=>{e=e.split("+").map(e=>r`<kbd class="ninja-hotkey">${e}</kbd>`);return r`<kbd class="ninja-hotkeys">${e}</kbd>`}));var n={selected:this.selected,"ninja-action":!0};return r`
      <div
        class="ninja-action"
        part="ninja-action ${this.selected?"ninja-selected":""}"
        class=${qe(n)}
      >
        ${e}
        <div class="ninja-title">${this.action.title}</div>
        ${t}
      </div>
    `}};e.styles=z`
    :host {
      display: flex;
      width: 100%;
    }
    .ninja-action {
      padding: 0.75em 1em;
      display: flex;
      border-left: 2px solid transparent;
      align-items: center;
      justify-content: start;
      outline: none;
      transition: color 0s ease 0s;
      width: 100%;
    }
    .ninja-action.selected {
      cursor: pointer;
      color: var(--ninja-selected-text-color);
      background-color: var(--ninja-selected-background);
      border-left: 2px solid var(--ninja-accent-color);
      outline: none;
    }
    .ninja-action.selected .ninja-icon {
      color: var(--ninja-selected-text-color);
    }
    .ninja-icon {
      font-size: var(--ninja-icon-size);
      max-width: var(--ninja-icon-size);
      max-height: var(--ninja-icon-size);
      margin-right: 1em;
      color: var(--ninja-icon-color);
      margin-right: 1em;
      position: relative;
    }

    .ninja-title {
      flex-shrink: 0.01;
      margin-right: 0.5em;
      flex-grow: 1;
      font-size: 0.8125em;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }
    .ninja-hotkeys {
      flex-shrink: 0;
      width: min-content;
      display: flex;
    }

    .ninja-hotkeys kbd {
      font-family: inherit;
    }
    .ninja-hotkey {
      background: var(--ninja-secondary-background-color);
      padding: 0.06em 0.25em;
      border-radius: var(--ninja-key-border-radius);
      text-transform: capitalize;
      color: var(--ninja-secondary-text-color);
      font-size: 0.75em;
      font-family: inherit;
    }

    .ninja-hotkey + .ninja-hotkey {
      margin-left: 0.5em;
    }
    .ninja-hotkeys + .ninja-hotkeys {
      margin-left: 1em;
    }
  `,Yt([o({type:Object})],e.prototype,"action",void 0),Yt([o({type:Boolean})],e.prototype,"selected",void 0),Yt([o({type:Boolean})],e.prototype,"hotKeysJoinedView",void 0),Yt([Ee("ninja-action")],e);const en=r` <div class="modal-footer" slot="footer">
  <span class="help">
    <svg
      version="1.0"
      class="ninja-examplekey"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 1280 1280"
    >
      <path
        d="M1013 376c0 73.4-.4 113.3-1.1 120.2a159.9 159.9 0 0 1-90.2 127.3c-20 9.6-36.7 14-59.2 15.5-7.1.5-121.9.9-255 1h-242l95.5-95.5 95.5-95.5-38.3-38.2-38.2-38.3-160 160c-88 88-160 160.4-160 161 0 .6 72 73 160 161l160 160 38.2-38.3 38.3-38.2-95.5-95.5-95.5-95.5h251.1c252.9 0 259.8-.1 281.4-3.6 72.1-11.8 136.9-54.1 178.5-116.4 8.6-12.9 22.6-40.5 28-55.4 4.4-12 10.7-36.1 13.1-50.6 1.6-9.6 1.8-21 2.1-132.8l.4-122.2H1013v110z"
      />
    </svg>

    to select
  </span>
  <span class="help">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="ninja-examplekey"
      viewBox="0 0 24 24"
    >
      <path d="M0 0h24v24H0V0z" fill="none" />
      <path
        d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"
      />
    </svg>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="ninja-examplekey"
      viewBox="0 0 24 24"
    >
      <path d="M0 0h24v24H0V0z" fill="none" />
      <path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z" />
    </svg>
    to navigate
  </span>
  <span class="help">
    <span class="ninja-examplekey esc">esc</span>
    to close
  </span>
  <span class="help">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="ninja-examplekey backspace"
      viewBox="0 0 20 20"
      fill="currentColor"
    >
      <path
        fill-rule="evenodd"
        d="M6.707 4.879A3 3 0 018.828 4H15a3 3 0 013 3v6a3 3 0 01-3 3H8.828a3 3 0 01-2.12-.879l-4.415-4.414a1 1 0 010-1.414l4.414-4.414zm4 2.414a1 1 0 00-1.414 1.414L10.586 10l-1.293 1.293a1 1 0 101.414 1.414L12 11.414l1.293 1.293a1 1 0 001.414-1.414L13.414 10l1.293-1.293a1 1 0 00-1.414-1.414L12 8.586l-1.293-1.293z"
        clip-rule="evenodd"
      />
    </svg>
    move to parent
  </span>
</div>`,tn=z`
  :host {
    --ninja-width: 640px;
    --ninja-backdrop-filter: none;
    --ninja-overflow-background: rgba(255, 255, 255, 0.5);
    --ninja-text-color: rgb(60, 65, 73);
    --ninja-font-size: 16px;
    --ninja-top: 20%;

    --ninja-key-border-radius: 0.25em;
    --ninja-accent-color: rgb(110, 94, 210);
    --ninja-secondary-background-color: rgb(239, 241, 244);
    --ninja-secondary-text-color: rgb(107, 111, 118);

    --ninja-selected-background: rgb(248, 249, 251);

    --ninja-icon-color: var(--ninja-secondary-text-color);
    --ninja-icon-size: 1.2em;
    --ninja-separate-border: 1px solid var(--ninja-secondary-background-color);

    --ninja-modal-background: #fff;
    --ninja-modal-shadow: rgb(0 0 0 / 50%) 0px 16px 70px;

    --ninja-actions-height: 300px;
    --ninja-group-text-color: rgb(144, 149, 157);

    --ninja-footer-background: rgba(242, 242, 242, 0.4);

    --ninja-placeholder-color: #8e8e8e;

    font-size: var(--ninja-font-size);

    --ninja-z-index: 1;
  }

  :host(.dark) {
    --ninja-backdrop-filter: none;
    --ninja-overflow-background: rgba(0, 0, 0, 0.7);
    --ninja-text-color: #7d7d7d;

    --ninja-modal-background: rgba(17, 17, 17, 0.85);
    --ninja-accent-color: rgb(110, 94, 210);
    --ninja-secondary-background-color: rgba(51, 51, 51, 0.44);
    --ninja-secondary-text-color: #888;

    --ninja-selected-text-color: #eaeaea;
    --ninja-selected-background: rgba(51, 51, 51, 0.44);

    --ninja-icon-color: var(--ninja-secondary-text-color);
    --ninja-separate-border: 1px solid var(--ninja-secondary-background-color);

    --ninja-modal-shadow: 0 16px 70px rgba(0, 0, 0, 0.2);

    --ninja-group-text-color: rgb(144, 149, 157);

    --ninja-footer-background: rgba(30, 30, 30, 85%);
  }

  .modal {
    display: none;
    position: fixed;
    z-index: var(--ninja-z-index);
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background: var(--ninja-overflow-background);
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    -webkit-backdrop-filter: var(--ninja-backdrop-filter);
    backdrop-filter: var(--ninja-backdrop-filter);
    text-align: left;
    color: var(--ninja-text-color);
    font-family: var(--ninja-font-family);
  }
  .modal.visible {
    display: block;
  }

  .modal-content {
    position: relative;
    top: var(--ninja-top);
    margin: auto;
    padding: 0;
    display: flex;
    flex-direction: column;
    flex-shrink: 1;
    -webkit-box-flex: 1;
    flex-grow: 1;
    min-width: 0px;
    will-change: transform;
    background: var(--ninja-modal-background);
    border-radius: 0.5em;
    box-shadow: var(--ninja-modal-shadow);
    max-width: var(--ninja-width);
    overflow: hidden;
  }

  .bump {
    animation: zoom-in-zoom-out 0.2s ease;
  }

  @keyframes zoom-in-zoom-out {
    0% {
      transform: scale(0.99);
    }
    50% {
      transform: scale(1.01, 1.01);
    }
    100% {
      transform: scale(1, 1);
    }
  }

  .ninja-github {
    color: var(--ninja-keys-text-color);
    font-weight: normal;
    text-decoration: none;
  }

  .actions-list {
    max-height: var(--ninja-actions-height);
    overflow: auto;
    scroll-behavior: smooth;
    position: relative;
    margin: 0;
    padding: 0.5em 0;
    list-style: none;
    scroll-behavior: smooth;
  }

  .group-header {
    height: 1.375em;
    line-height: 1.375em;
    padding-left: 1.25em;
    padding-top: 0.5em;
    text-overflow: ellipsis;
    white-space: nowrap;
    overflow: hidden;
    font-size: 0.75em;
    line-height: 1em;
    color: var(--ninja-group-text-color);
    margin: 1px 0;
  }

  .modal-footer {
    background: var(--ninja-footer-background);
    padding: 0.5em 1em;
    display: flex;
    /* font-size: 0.75em; */
    border-top: var(--ninja-separate-border);
    color: var(--ninja-secondary-text-color);
  }

  .modal-footer .help {
    display: flex;
    margin-right: 1em;
    align-items: center;
    font-size: 0.75em;
  }

  .ninja-examplekey {
    background: var(--ninja-secondary-background-color);
    padding: 0.06em 0.25em;
    border-radius: var(--ninja-key-border-radius);
    color: var(--ninja-secondary-text-color);
    width: 1em;
    height: 1em;
    margin-right: 0.5em;
    font-size: 1.25em;
    fill: currentColor;
  }
  .ninja-examplekey.esc {
    width: auto;
    height: auto;
    font-size: 1.1em;
  }
  .ninja-examplekey.backspace {
    opacity: 0.7;
  }
`;function H(e,t,n,i){var s,r=arguments.length,o=r<3?t:null===i?i=Object.getOwnPropertyDescriptor(t,n):i;if("object"==typeof Reflect&&"function"==typeof Reflect.decorate)o=Reflect.decorate(e,t,n,i);else for(var a=e.length-1;0<=a;a--)(s=e[a])&&(o=(r<3?s(o):3<r?s(t,n,o):s(t,n))||o);return 3<r&&o&&Object.defineProperty(t,n,o),o}i=class extends s{constructor(){super(...arguments),this.placeholder="Type a command or search...",this.disableHotkeys=!1,this.hideBreadcrumbs=!1,this.openHotkey="cmd+k,ctrl+k",this.navigationUpHotkey="up,shift+tab",this.navigationDownHotkey="down,tab",this.closeHotkey="esc",this.goBackHotkey="backspace",this.selectHotkey="enter",this.hotKeysJoinedView=!1,this.noAutoLoadMdIcons=!1,this.data=[],this.visible=!1,this._bump=!0,this._actionMatches=[],this._search="",this._flatData=[],this._headerRef=Ne()}open(e={}){this._bump=!0,this.visible=!0,this._headerRef.value.focusSearch(),0<this._actionMatches.length&&(this._selected=this._actionMatches[0]),this.setParent(e.parent)}close(){this._bump=!1,this.visible=!1}setParent(e){this._currentRoot=e||void 0,this._selected=void 0,this._search="",this._headerRef.value.setSearch("")}get breadcrumbs(){var e,t=[];let n=null==(e=this._selected)?void 0:e.parent;if(n)for(t.push(n);n;){const e=this._flatData.find(e=>e.id===n);null!=e&&e.parent&&t.push(e.parent),n=e?e.parent:void 0}return t.reverse()}connectedCallback(){super.connectedCallback(),this.noAutoLoadMdIcons||document.fonts.load("24px Material Icons","apps").then(()=>{}),this._registerInternalHotkeys()}disconnectedCallback(){super.disconnectedCallback(),this._unregisterInternalHotkeys()}_flattern(e,i){let s=[];return(e=e||[]).map(e=>{var t=e.children&&e.children.some(e=>"string"==typeof e),n={...e,parent:e.parent||i};return t||(n.children&&n.children.length&&(i=e.id,s=[...s,...n.children]),n.children=n.children?n.children.map(e=>e.id):[]),n}).concat(s.length?this._flattern(s,i):s)}update(e){e.has("data")&&!this.disableHotkeys&&(this._flatData=this._flattern(this.data),this._flatData.filter(e=>!!e.hotkey).forEach(t=>{k(t.hotkey,e=>{e.preventDefault(),t.handler&&t.handler(t)})})),super.update(e)}_registerInternalHotkeys(){this.openHotkey&&k(this.openHotkey,e=>{e.preventDefault(),this.visible?this.close():this.open()}),this.selectHotkey&&k(this.selectHotkey,e=>{this.visible&&(e.preventDefault(),this._actionSelected(this._actionMatches[this._selectedIndex]))}),this.goBackHotkey&&k(this.goBackHotkey,e=>{!this.visible||this._search||(e.preventDefault(),this._goBack())}),this.navigationDownHotkey&&k(this.navigationDownHotkey,e=>{this.visible&&(e.preventDefault(),this._selectedIndex>=this._actionMatches.length-1?this._selected=this._actionMatches[0]:this._selected=this._actionMatches[this._selectedIndex+1])}),this.navigationUpHotkey&&k(this.navigationUpHotkey,e=>{this.visible&&(e.preventDefault(),0===this._selectedIndex?this._selected=this._actionMatches[this._actionMatches.length-1]:this._selected=this._actionMatches[this._selectedIndex-1])}),this.closeHotkey&&k(this.closeHotkey,()=>{this.visible&&this.close()})}_unregisterInternalHotkeys(){this.openHotkey&&k.unbind(this.openHotkey),this.selectHotkey&&k.unbind(this.selectHotkey),this.goBackHotkey&&k.unbind(this.goBackHotkey),this.navigationDownHotkey&&k.unbind(this.navigationDownHotkey),this.navigationUpHotkey&&k.unbind(this.navigationUpHotkey),this.closeHotkey&&k.unbind(this.closeHotkey)}_actionFocused(e,t){this._selected=e,t.target.ensureInView()}_onTransitionEnd(){this._bump=!1}_goBack(){var e=1<this.breadcrumbs.length?this.breadcrumbs[this.breadcrumbs.length-2]:void 0;this.setParent(e)}render(){var e={bump:this._bump,"modal-content":!0},t={visible:this.visible,modal:!0},n=this._flatData.filter(e=>{var t=new RegExp(this._search,"gi"),n=e.title.match(t)||(null==(n=e.keywords)?void 0:n.match(t));return(!this._currentRoot&&this._search||e.parent===this._currentRoot)&&n}).reduce((e,t)=>e.set(t.section,[...e.get(t.section)||[],t]),new Map);this._actionMatches=[...n.values()].flat(),0<this._actionMatches.length&&-1===this._selectedIndex&&(this._selected=this._actionMatches[0]),0===this._actionMatches.length&&(this._selected=void 0);const i=e=>r` ${Ue(e,e=>e.id,t=>{var e;return r`<ninja-action
            exportparts="ninja-action,ninja-selected,ninja-icon"
            .selected=${He(t.id===(null==(e=this._selected)?void 0:e.id))}
            .hotKeysJoinedView=${this.hotKeysJoinedView}
            @mouseover=${e=>this._actionFocused(t,e)}
            @actionsSelected=${e=>this._actionSelected(e.detail)}
            .action=${t}
          ></ninja-action>`})}`,s=[];return n.forEach((e,t)=>{t=t?r`<div class="group-header">${t}</div>`:void 0;s.push(r`${t}${i(e)}`)}),r`
      <div @click=${this._overlayClick} class=${qe(t)}>
        <div class=${qe(e)} @animationend=${this._onTransitionEnd}>
          <ninja-header
            exportparts="ninja-input,ninja-input-wrapper"
            ${Ve(this._headerRef)}
            .placeholder=${this.placeholder}
            .hideBreadcrumbs=${this.hideBreadcrumbs}
            .breadcrumbs=${this.breadcrumbs}
            @change=${this._handleInput}
            @setParent=${e=>this.setParent(e.detail.parent)}
            @close=${this.close}
          >
          </ninja-header>
          <div class="modal-body">
            <div class="actions-list" part="actions-list">${s}</div>
          </div>
          <slot name="footer"> ${en} </slot>
        </div>
      </div>
    `}get _selectedIndex(){return this._selected?this._actionMatches.indexOf(this._selected):-1}_actionSelected(e){var t;if(this.dispatchEvent(new CustomEvent("selected",{detail:{search:this._search,action:e},bubbles:!0,composed:!0})),e){if(e.children&&0<(null==(t=e.children)?void 0:t.length)&&(this._currentRoot=e.id,this._search=""),this._headerRef.value.setSearch(""),this._headerRef.value.focusSearch(),e.handler){const t=e.handler(e);null!=t&&t.keepOpen||this.close()}this._bump=!0}}async _handleInput(e){this._search=e.detail.search,await this.updateComplete,this.dispatchEvent(new CustomEvent("change",{detail:{search:this._search,actions:this._actionMatches},bubbles:!0,composed:!0}))}_overlayClick(e){null!=(e=e.target)&&e.classList.contains("modal")&&this.close()}};i.styles=[tn],H([o({type:String})],i.prototype,"placeholder",void 0),H([o({type:Boolean})],i.prototype,"disableHotkeys",void 0),H([o({type:Boolean})],i.prototype,"hideBreadcrumbs",void 0),H([o()],i.prototype,"openHotkey",void 0),H([o()],i.prototype,"navigationUpHotkey",void 0),H([o()],i.prototype,"navigationDownHotkey",void 0),H([o()],i.prototype,"closeHotkey",void 0),H([o()],i.prototype,"goBackHotkey",void 0),H([o()],i.prototype,"selectHotkey",void 0),H([o({type:Boolean})],i.prototype,"hotKeysJoinedView",void 0),H([o({type:Boolean})],i.prototype,"noAutoLoadMdIcons",void 0),H([o({type:Array,hasChanged:()=>!0})],i.prototype,"data",void 0),H([a()],i.prototype,"visible",void 0),H([a()],i.prototype,"_bump",void 0),H([a()],i.prototype,"_actionMatches",void 0),H([a()],i.prototype,"_search",void 0),H([a()],i.prototype,"_currentRoot",void 0),H([a()],i.prototype,"_flatData",void 0),H([a()],i.prototype,"breadcrumbs",null),H([a()],i.prototype,"_selected",void 0),H([Ee("ninja-keys")],i)}}]);