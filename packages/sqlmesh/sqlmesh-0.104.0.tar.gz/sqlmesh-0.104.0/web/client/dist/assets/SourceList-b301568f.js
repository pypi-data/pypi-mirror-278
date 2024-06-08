import{r as f,q as V,F as k,j as s,c as v,h as y,B as A,g as G,z as H,s as J}from"./index-0556dabd.js";import{I as F}from"./Input-da5e8505.js";import{u as K}from"./index-bad63c56.js";function W({items:c=[],keyId:d="id",keyName:N="",keyDescription:x="",to:L="",disabled:S=!1,withCounter:T=!0,withFilter:$=!0,types:a,className:B,isActive:m,listItem:h}){var I;const O=f.useRef(null),[r,q]=f.useState(""),j=f.useRef(null),[o,u]=f.useMemo(()=>{let t=-1;const e=[];return c.forEach((l,p)=>{const g=n(l[d]),w=n(l[x]),M=n(l[N]),Y=n(a==null?void 0:a[g]);(M.includes(r)||w.includes(r)||Y.includes(r))&&e.push(l),V(m)&&m(l[d])&&(t=p)}),[t,e]},[c,r,m]),i=K({count:u.length,getScrollElement:()=>j.current,estimateSize:()=>32+(x.length>0?16:0)}),b=({itemIndex:t,isSmoothScroll:e=!0})=>{i.scrollToIndex(t,{align:"center",behavior:e?"smooth":"auto"})},z=({itemIndex:t,range:e})=>V(e)&&(e.startIndex>t||(e==null?void 0:e.endIndex)<t),C=k(r)&&o>-1&&z({range:i.range,itemIndex:o});f.useEffect(()=>{o>-1&&z({range:i.range,itemIndex:o})&&b({itemIndex:o,isSmoothScroll:!1})},[o]);const E=i.getVirtualItems(),R=i.getTotalSize();return s.jsxs("div",{ref:O,className:v("flex flex-col w-full h-full text-sm text-neutral-600 dark:text-neutral-300",B),style:{contain:"strict"},children:[$&&s.jsxs("div",{className:"p-1 w-full flex justify-between",children:[s.jsx(F,{className:"w-full !m-0",size:y.sm,children:({className:t})=>s.jsx(F.Textfield,{className:v(t,"w-full"),value:r,placeholder:"Filter items",type:"search",onInput:e=>{q(e.target.value)}})}),T&&s.jsx("div",{className:"ml-1 px-3 bg-primary-10 text-primary-500 rounded-full text-xs flex items-center",children:u.length})]}),s.jsxs("div",{className:"w-full h-full relative p-1",children:[C&&s.jsx(A,{className:"absolute left-[50%] translate-x-[-50%] -top-2 z-10 text-ellipsis !block overflow-hidden no-wrap max-w-[90%] !border-neutral-20 shadow-md !bg-theme !hover:bg-theme text-neutral-500 dark:text-neutral-300 !focus:ring-2 !focus:ring-theme-500 !focus:ring-offset-2 !focus:ring-offset-theme-50 !focus:ring-opacity-50 !focus:outline-none !focus:ring-offset-transparent !focus:ring-offset-0 !focus:ring",onClick:()=>b({itemIndex:o}),size:y.sm,variant:G.Secondary,children:"Scroll to selected"}),s.jsx("div",{ref:j,className:"w-full h-full relative overflow-hidden overflow-y-auto hover:scrollbar scrollbar--horizontal scrollbar--vertical",style:{contain:"strict"},children:s.jsx("div",{className:"relative w-full",style:{height:R>0?`${R}px`:"100%"},children:s.jsxs("ul",{className:"w-full absolute top-0 left-0",style:{transform:`translateY(${((I=E[0])==null?void 0:I.start)??0}px)`},children:[H(u)&&s.jsx("li",{className:"px-2 py-0.5 text-center whitespace-nowrap overflow-ellipsis overflow-hidden",children:r.length>0?"No Results Found":"Empty List"},"not-found"),E.map(t=>{const e=u[t.index],l=n(e[d]),p=n(e[x]),g=n(e[N]),w=n(a==null?void 0:a[l]);return s.jsx("li",{"data-index":t.index,ref:i.measureElement,className:v("font-normal w-full",S&&"cursor-not-allowed"),tabIndex:l===r?-1:0,children:h==null?void 0:h({id:l,to:`${L}/${l}`,name:g,description:p,text:w,disabled:S,item:u[t.index]})},t.key)})]})})})]})]})}function n(c){return J(c)?"":String(c)}export{W as S};
