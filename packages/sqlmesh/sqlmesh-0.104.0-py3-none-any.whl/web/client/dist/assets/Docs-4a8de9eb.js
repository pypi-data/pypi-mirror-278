import{r as i,j as e,P as k,i as v,c as x,d as q,Z as G,b as J,I as K,J as U,o as Z,a as b,a0 as _,s as h,K as W,E as D,B as L,g as C,h as F}from"./index-0556dabd.js";import{M as X,u as Y,L as ee,C as se,a as I}from"./context-4bbc2c1f.js";import{v as M,M as te,P as ae}from"./disclosure-f413270e.js";import le from"./ModelLineage-393ad5ba.js";import{S as O}from"./SplitPane-3126158d.js";import{r as N,T as ne}from"./Tab-2a507f7d.js";import{E as re}from"./file-208ba368.js";import"./_commonjs-dynamic-modules-302442b1.js";import"./Input-da5e8505.js";import"./editor-fd8b1606.js";import"./project-cc90bf2b.js";import"./SourceList-b301568f.js";import"./index-bad63c56.js";import"./transition-d6609a11.js";import"./ListboxShow-0ff5112b.js";import"./SearchList-f77620af.js";function ie({title:s,titleId:t,...r},n){return i.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 20 20",fill:"currentColor","aria-hidden":"true",ref:n,"aria-labelledby":t},r),s?i.createElement("title",{id:t},s):null,i.createElement("path",{d:"M3.28 2.22a.75.75 0 00-1.06 1.06L5.44 6.5H2.75a.75.75 0 000 1.5h4.5A.75.75 0 008 7.25v-4.5a.75.75 0 00-1.5 0v2.69L3.28 2.22zM13.5 2.75a.75.75 0 00-1.5 0v4.5c0 .414.336.75.75.75h4.5a.75.75 0 000-1.5h-2.69l3.22-3.22a.75.75 0 00-1.06-1.06L13.5 5.44V2.75zM3.28 17.78l3.22-3.22v2.69a.75.75 0 001.5 0v-4.5a.75.75 0 00-.75-.75h-4.5a.75.75 0 000 1.5h2.69l-3.22 3.22a.75.75 0 101.06 1.06zM13.5 14.56l3.22 3.22a.75.75 0 101.06-1.06l-3.22-3.22h2.69a.75.75 0 000-1.5h-4.5a.75.75 0 00-.75.75v4.5a.75.75 0 001.5 0v-2.69z"}))}const oe=i.forwardRef(ie),Q=oe;function ce({title:s,titleId:t,...r},n){return i.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 20 20",fill:"currentColor","aria-hidden":"true",ref:n,"aria-labelledby":t},r),s?i.createElement("title",{id:t},s):null,i.createElement("path",{d:"M13.28 7.78l3.22-3.22v2.69a.75.75 0 001.5 0v-4.5a.75.75 0 00-.75-.75h-4.5a.75.75 0 000 1.5h2.69l-3.22 3.22a.75.75 0 001.06 1.06zM2 17.25v-4.5a.75.75 0 011.5 0v2.69l3.22-3.22a.75.75 0 011.06 1.06L4.56 16.5h2.69a.75.75 0 010 1.5h-4.5a.747.747 0 01-.75-.75zM12.22 13.28l3.22 3.22h-2.69a.75.75 0 000 1.5h4.5a.747.747 0 00.75-.75v-4.5a.75.75 0 00-1.5 0v2.69l-3.22-3.22a.75.75 0 10-1.06 1.06zM3.5 4.56l3.22 3.22a.75.75 0 001.06-1.06L4.56 3.5h2.69a.75.75 0 000-1.5h-4.5a.75.75 0 00-.75.75v4.5a.75.75 0 001.5 0V4.56z"}))}const ue=i.forwardRef(ce),R=ue,S=function({model:t,withModel:r=!0,withDescription:n=!0,withColumns:o=!0,withCode:p=!0,withQuery:j=!0}){return e.jsxs(y,{className:"pt-2",children:[r&&e.jsx(E,{headline:"Model",defaultOpen:!0,children:e.jsxs("ul",{className:"w-full",children:[e.jsx(m,{name:"Path",value:t.path}),e.jsx(m,{name:"Name",title:t.displayName,value:k(t.displayName,50,25)}),e.jsx(m,{name:"Dialect",value:t.dialect}),e.jsx(m,{name:"Type",value:t.type}),Object.entries(t.details??{}).map(([u,f])=>e.jsx(m,{name:u.replaceAll("_"," "),value:f,isCapitalize:!0},u))]})}),n&&e.jsx(E,{headline:"Description",defaultOpen:!0,children:t.description??"No description"}),o&&e.jsx(E,{headline:"Columns",defaultOpen:!0,children:e.jsx(X,{nodeId:t.fqn,columns:t.columns,disabled:v(t.isModelSQL),withHandles:!1,withSource:!1,withDescription:!0,limit:10})})]})};function de({headline:s}){return e.jsx("div",{className:"text-md font-bold whitespace-nowrap w-full",id:s,children:e.jsx("h3",{className:"py-2",children:s})})}function xe(){return e.jsx(y,{className:"font-bold whitespace-nowrap",children:e.jsx("div",{className:"flex items-center justify-center w-full h-full",children:"Documentation Not Found"})})}function y({children:s,className:t}){return e.jsx("div",{className:x("w-full h-full rounded-xl",t),children:e.jsx("div",{className:"w-full h-full overflow-auto scrollbar scrollbar--vertical scrollbar--horizontal",children:s})})}function E({children:s,className:t,headline:r,defaultOpen:n=!1}){return e.jsx("div",{className:"px-1 text-neutral-500 dark:text-neutral-400",children:e.jsx(M,{defaultOpen:n,children:({open:o})=>e.jsxs(e.Fragment,{children:[e.jsxs(M.Button,{className:x("flex items-center justify-between rounded-lg text-left w-full hover:bg-neutral-5 px-3 mb-1 overflow-hidden",t),children:[e.jsx(de,{headline:r}),e.jsx("div",{children:o?e.jsx(te,{className:"w-4 text-neutral-50"}):e.jsx(ae,{className:"w-4 text-neutral-50"})})]}),e.jsx(M.Panel,{className:"pb-2 px-4 text-xs overflow-hidden",children:s})]})})})}function m({className:s,name:t,value:r,isHighlighted:n=!1,isCapitalize:o=!1,children:p,title:j}){return e.jsxs("li",{className:x("w-full border-b last:border-b-0 border-neutral-10 py-1 mb-1 text-neutral-500 dark:text-neutral-400",s),children:[q(r)?e.jsxs(e.Fragment,{children:[e.jsx("strong",{title:j,className:"mr-2 text-xs capitalize",children:t}),r.map((u,f)=>e.jsx("ul",{className:"w-full flex flex-col whitespace-nowrap p-1 m-1 rounded-md overflow-hidden",children:Object.entries(u).map(([c,g])=>e.jsxs("li",{className:"flex items-center justify-between text-xs border-b border-neutral-10 last:border-b-0 py-1",children:[e.jsxs("strong",{className:"mr-2",children:[c,":"]}),e.jsx("p",{className:"text-xs",children:A(g)})]},c))},f))]}):e.jsxs("div",{className:"flex justify-between text-xs whitespace-nowrap",children:[e.jsx("strong",{className:x("mr-2",o&&"capitalize",n&&"text-brand-500"),children:t}),e.jsx("p",{className:"text-xs rounded text-neutral-500 dark:text-neutral-400",children:A(r)})]}),e.jsx("p",{className:"text-xs ",children:p})]})}S.NotFound=xe;S.Container=y;const fe=S;function A(s){const t=new Date(s),r=G(s)&&!isNaN(t.getTime()),n=typeof s=="boolean";return n&&J(s)?"True":n&&v(s)?"False":r?K(t):String(s)}function Le(){const{modelName:s=""}=U(),t=Z(),r=b(a=>a.models),n=b(a=>a.lastSelectedModel),o=b(a=>a.setLastSelectedModel),[p,j]=i.useState([65,35]),[u,f]=i.useState([50,50]),[c,g]=i.useState(!1),[P,B]=i.useState(!1),{refetch:T,cancel:V,isFetching:$}=_(s),l=h(s)||s===(n==null?void 0:n.name)?n:r.get(encodeURI(s)),z=Y(l==null?void 0:l.path,a=>{w==null||w(a.name)});i.useEffect(()=>{if(!h(l))return T().then(({data:a})=>{l.update(a),o(l)}),()=>{V()}},[s,l==null?void 0:l.hash,l==null?void 0:l.path,l==null?void 0:l.name]);function w(a){const d=r.get(a);h(d)||t(D.DocsModels+"/"+d.name)}function H(a){console.log(a==null?void 0:a.message)}return e.jsx("div",{className:"flex overflow-auto w-full h-full",children:h(l)?e.jsx(W,{link:D.Docs,description:h(s)?void 0:`Model ${s} Does Not Exist`,message:"Back To Docs"}):e.jsx(ee,{showColumns:!0,handleClickModel:w,handleError:H,children:e.jsxs(O,{className:"flex h-full w-full",sizes:c||P?[100,0]:u,minSize:0,snapOffset:0,onDragEnd:a=>f(a),children:[e.jsx("div",{className:"flex flex-col h-full",children:e.jsxs(O,{direction:"vertical",sizes:c?[0,100]:P?[100,0]:p,minSize:0,snapOffset:0,className:"flex flex-col w-full h-full overflow-hidden",onDragEnd:a=>j(a),children:[e.jsxs("div",{className:"flex flex-col h-full relative overflow-hidden",children:[e.jsx(L,{className:x("absolute top-0 right-1 h-8 w-8 !px-0 !bg-light !text-neutral-500 shadow-xl z-10"),variant:C.Info,size:F.sm,onClick:a=>{a.stopPropagation(),B(d=>v(d))},children:c?e.jsx(Q,{className:"w-4 h-4"}):e.jsx(R,{className:"w-4 h-4"})}),e.jsx(se,{path:l.path,children:({file:a})=>e.jsxs(N.Group,{children:[e.jsx(ne,{list:["Source Code",l.isModelSQL&&"Compiled Query"].filter(Boolean),disabled:$,className:"justify-center"}),e.jsxs(N.Panels,{className:"h-full w-full overflow-hidden text-xs",children:[e.jsx(N.Panel,{unmount:!1,className:"w-full h-full",children:e.jsx(I,{content:a.content,type:a.extension,extensions:z})}),l.isModelSQL&&e.jsx(N.Panel,{unmount:!1,className:"w-full h-full",children:e.jsx(I,{type:re.SQL,content:l.sql??"",extensions:z})})]})]})})]}),e.jsxs("div",{className:"flex flex-col h-full relative overflow-hidden",children:[e.jsx(L,{className:x("absolute top-9 right-1 h-8 w-8 !px-0 !bg-light !text-neutral-500 shadow-xl z-10"),variant:C.Info,size:F.sm,onClick:a=>{a.stopPropagation(),g(d=>v(d))},children:c?e.jsx(Q,{className:"w-4 h-4"}):e.jsx(R,{className:"w-4 h-4"})}),e.jsx(le,{model:l})]})]})}),e.jsx("div",{className:"flex flex-col h-full",children:e.jsx(fe,{model:l,withQuery:l.isModelSQL})})]})})})}export{Le as default};
