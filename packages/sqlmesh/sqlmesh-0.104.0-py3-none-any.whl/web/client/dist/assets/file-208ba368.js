var a=Object.defineProperty;var u=(n,t,e)=>t in n?a(n,t,{enumerable:!0,configurable:!0,writable:!0,value:e}):n[t]=e;var s=(n,t,e)=>(u(n,typeof t!="symbol"?t+"":t,e),e);import{X as d,F as r,a5 as c,i as p,s as _}from"./index-0556dabd.js";class g extends d{constructor(e,h){super(e!=null&&e.isModel?e.initial:{...e,name:(e==null?void 0:e.name)??"",path:(e==null?void 0:e.path)??""});s(this,"_path");s(this,"_name");s(this,"parent");s(this,"remove",!1);this._path=(e==null?void 0:e.path)??this.initial.path,this._name=(e==null?void 0:e.name)??this.initial.name,this.parent=h}get id(){return r(this.path)?this.initial.id:this.path}get name(){return this._name}get path(){return this._path}get isUntitled(){return this.name===""}get isLocal(){return this.path===""}get isRemote(){return this.path!==""}get withParent(){var e;return!!((e=this.parent)!=null&&e.isModel)}copyName(){return`Copy of ${this.name}__${c()}`}rename(e){this.isRemote&&(this._path=this._path.replace(this.name,e)),this._name=e}static findArtifactByPath(e,h){return e.path===h?e:e.allArtifacts.find(m=>m.path===h)}}const o={SQL:".sql",PY:".py",CSV:".csv",YAML:".yaml",YML:".yml",None:""};class y extends g{constructor(e,h){super(e!=null&&e.isModel?e.initial:{...e,extension:(e==null?void 0:e.extension)??o.SQL,content:(e==null?void 0:e.content)??""},h);s(this,"_content","");s(this,"content");s(this,"extension");s(this,"isFormatted");this.extension=(e==null?void 0:e.extension)??this.initial.extension??"",this._content=this.content=(e==null?void 0:e.content)??this.initial.content??"",this.isFormatted=e==null?void 0:e.isFormatted}get basename(){return this.name.replace(this.extension,"")}get isSynced(){return p(r(this._content))}get isEmpty(){return r(this.content)}get isChanged(){return this.content!==this._content}get isSQL(){return this.extension===o.SQL}get fingerprint(){return this._content+this.name+this.path}removeChanges(){this.content=this._content}copyName(){return`Copy of ${this.name.split(this.extension)[0]??""}__${c()}${this.extension}`}updateContent(e=""){(this.isSynced||p(this.isChanged))&&(this.content=e),this._content=e}update(e){_(e)?this.updateContent(""):(this.extension=e.extension??o.None,this.updateContent(e.content??""))}}export{o as E,y as M,g as a};
