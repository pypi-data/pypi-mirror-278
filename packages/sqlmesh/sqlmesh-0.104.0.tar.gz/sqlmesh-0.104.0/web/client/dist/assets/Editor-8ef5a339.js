import{r as f,d as oe,j as e,c as h,q as E,s as A,b as Ie,i as P,a as T,h as w,F as q,B as F,g as _,ad as ze,D as V,S as Z,I as le,a1 as ve,a2 as Ae,a3 as Qe,ae as Ee,_ as Oe,u as Te,o as Be,E as We,n as He,A as z,z as $e,a4 as Ge,af as Ve}from"./index-0556dabd.js";import{u as G,M as qe}from"./project-cc90bf2b.js";import{S as be}from"./SplitPane-3126158d.js";import{E as $,M as Ue}from"./file-208ba368.js";import{u as j}from"./editor-fd8b1606.js";import{I as b}from"./Input-da5e8505.js";import{X as Ye,L as Xe}from"./ListboxShow-0ff5112b.js";import{B as we}from"./Banner-9c0a1d8a.js";import{r as D,T as de}from"./Tab-2a507f7d.js";import{g as ue,G as Je,F as Ze,T as Ke}from"./help-9ac13e33.js";import{M as es,u as Se,a as ie,b as ss,c as ts,C as ls}from"./context-4bbc2c1f.js";import{v as ne,M as ns,P as rs}from"./disclosure-f413270e.js";import{D as as}from"./ReportErrors-72b6ab0c.js";import"./transition-d6609a11.js";import"./index-bad63c56.js";import"./_commonjs-dynamic-modules-302442b1.js";import"./SourceList-b301568f.js";import"./pluralize-980f5fb9.js";function os({title:s,titleId:t,...l},a){return f.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor","aria-hidden":"true",ref:a,"aria-labelledby":t},l),s?f.createElement("title",{id:t},s):null,f.createElement("path",{fillRule:"evenodd",d:"M3 6.75A.75.75 0 013.75 6h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 6.75zM3 12a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75A.75.75 0 013 12zm0 5.25a.75.75 0 01.75-.75h16.5a.75.75 0 010 1.5H3.75a.75.75 0 01-.75-.75z",clipRule:"evenodd"}))}const is=f.forwardRef(os),Ce=is;function cs({title:s,titleId:t,...l},a){return f.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor","aria-hidden":"true",ref:a,"aria-labelledby":t},l),s?f.createElement("title",{id:t},s):null,f.createElement("path",{fillRule:"evenodd",d:"M12 3.75a.75.75 0 01.75.75v6.75h6.75a.75.75 0 010 1.5h-6.75v6.75a.75.75 0 01-1.5 0v-6.75H4.5a.75.75 0 010-1.5h6.75V4.5a.75.75 0 01.75-.75z",clipRule:"evenodd"}))}const ds=f.forwardRef(cs),us=ds;function ms({title:s,titleId:t,...l},a){return f.createElement("svg",Object.assign({xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 24 24",fill:"currentColor","aria-hidden":"true",ref:a,"aria-labelledby":t},l),s?f.createElement("title",{id:t},s):null,f.createElement("path",{d:"M15 3.75H9v16.5h6V3.75zM16.5 20.25h3.375c1.035 0 1.875-.84 1.875-1.875V5.625c0-1.036-.84-1.875-1.875-1.875H16.5v16.5zM4.125 3.75H7.5v16.5H4.125a1.875 1.875 0 01-1.875-1.875V5.625c0-1.036.84-1.875 1.875-1.875z"}))}const fs=f.forwardRef(ms),xs=fs;function hs(s){switch(s){case $.SQL:return"SQL";case $.PY:return"Python";case $.YAML:case $.YML:return"YAML";default:return"Plain Text"}}function ps(s,t){return s.file.extension===$.SQL&&s.file.isLocal&&oe(t)}const L=function({text:t,children:l,className:a}){return e.jsxs("small",{className:h("font-bold whitespace-nowrap text-xs",a),children:[E(t)&&e.jsxs("span",{children:[t,": "]}),l]})};function gs({text:s,className:t}){return e.jsx("span",{className:h("font-normal",t),children:s})}function js({ok:s,className:t}){return e.jsx("span",{className:h("inline-block w-2 h-2 rounded-full",A(s)&&"bg-warning-500",Ie(s)&&"bg-success-500",P(s)&&"bg-danger-500",t)})}L.Text=gs;L.Light=js;const I={Model:"model",Test:"test",Audit:"audit",Macro:"macro",Hook:"hook",Log:"log",Config:"config",Seed:"seed",Metric:"metric",Schema:"schema",Unknown:"unknown"};function vs({tab:s}){const t=T(d=>d.isModel),l=j(d=>d.engine),a=j(d=>d.dialects),u=j(d=>d.refreshTab);f.useEffect(()=>{var c;const d=(c=a[0])==null?void 0:c.dialect_name;A(s.dialect)&&E(d)&&o(d)},[a,s]);function o(d){s.dialect=d,u(s),l.postMessage({topic:"dialect",payload:s.dialect})}return e.jsxs("div",{className:"flex w-full items-center px-2 min-h-[2rem]",children:[s.file.isRemote&&e.jsx(L,{className:"mr-2",text:"Saved",children:e.jsx(L.Light,{ok:P(s.file.isChanged)})}),s.file.isRemote&&s.file.isSQL&&e.jsx(L,{className:"mr-2",text:"Formatted",children:e.jsx(L.Light,{ok:s.file.isFormatted})}),e.jsx(L,{className:"mr-2",text:"Language",children:e.jsx(L.Text,{text:hs(s.file.extension)})}),ps(s,a)&&e.jsx(L,{className:"mr-2",text:"Dialect",children:e.jsx(b,{size:w.sm,children:({className:d,size:c})=>e.jsx(b.Selector,{className:d,size:c,list:a.map(x=>({text:x.dialect_title,value:q(x.dialect_name)?"sqlglot":x.dialect_name})),onChange:x=>{o(x)},value:s.dialect})})}),t(s.file.path)&&!q(s.dialect)&&e.jsx(L,{className:"mr-2",text:"Dialect",children:e.jsx(L.Text,{text:s.dialect})}),e.jsx(L,{className:"mr-2",text:"SQLMesh Type",children:e.jsx(L.Text,{text:bs(s.file.path)})})]})}function bs(s){return q(s)?I.Unknown:s.startsWith("models")?I.Model:s.startsWith("tests")?I.Test:s.startsWith("logs")?I.Log:s.startsWith("macros")?I.Macro:s.startsWith("hooks")?I.Hook:s.startsWith("seeds")?I.Seed:s.startsWith("metrics")?I.Metric:["config.yaml","config.yml","config.py"].includes(s)?I.Config:["external_models.yaml","schema.yaml"].includes(s)?I.Schema:I.Unknown}function ws(){const s=T(r=>r.modules),t=T(r=>r.models),l=T(r=>r.lastSelectedModel),a=T(r=>r.setLastSelectedModel),u=G(r=>r.files),o=G(r=>r.selectedFile),d=G(r=>r.setSelectedFile),c=j(r=>r.tab),x=j(r=>r.tabs),n=j(r=>r.replaceTab),i=j(r=>r.createTab),N=j(r=>r.selectTab),k=j(r=>r.addTab),[p,y]=f.useMemo(()=>{const r=[],v=[];return x.forEach(S=>{S.file.isLocal&&r.push(S),S.file.isRemote&&v.push(S)}),[r,v]},[x]);f.useEffect(()=>{if(A(o)||(c==null?void 0:c.file)===o||o instanceof qe||P(s.hasFiles))return;a(t.get(o.path));const r=i(o);E(c)&&c.file instanceof Ue&&P(c.file.isChanged)&&c.file.isRemote&&P(x.has(o))?n(c,r):k(r),N(r)},[o]),f.useEffect(()=>{if(A(l))return;const r=u.get(l.path);A(r)||d(r)},[l]);function R(){const r=i();k(r),N(r),d(r.file)}return e.jsxs("div",{className:"flex items-center",children:[e.jsx(F,{className:"h-6 m-0 ml-1 mr-2 border-none",variant:_.Alternative,size:w.sm,onClick:r=>{r.stopPropagation(),R()},children:e.jsx(us,{className:"inline-block w-3 h-4"})}),e.jsxs("ul",{className:"w-full whitespace-nowrap min-h-[2rem] max-h-[2rem] overflow-hidden overflow-x-auto hover:scrollbar scrollbar--horizontal",children:[p.map((r,v)=>e.jsx(Ne,{tab:r,title:`Custom SQL ${v+1}`},r.id)),y.map(r=>e.jsx(Ne,{tab:r,title:r.file.name},r.id))]})]})}function Ne({tab:s,title:t}){const l=f.useRef(null),a=T(i=>i.addConfirmation),u=G(i=>i.setSelectedFile),o=j(i=>i.tab),d=j(i=>i.selectTab),c=j(i=>i.closeTab);f.useEffect(()=>{A(s)||(s.el=l.current??void 0,(o==null?void 0:o.id)===s.id&&setTimeout(()=>{var i;(i=s==null?void 0:s.el)==null||i.scrollIntoView({behavior:"smooth",inline:"center"})},300))},[l,s,o]);function x(){s.file.isChanged?a({headline:"Closing Tab",description:"All unsaved changes will be lost. Do you want to close the tab anyway?",yesText:"Yes, Close Tab",noText:"No, Cancel",action:()=>{c(s.file)}}):c(s.file)}const n=s.file.id===(o==null?void 0:o.file.id);return e.jsx("li",{ref:l,className:h("inline-block py-1 pr-2 last-child:pr-0 overflow-hidden text-center overflow-ellipsis cursor-pointer"),onClick:i=>{i.stopPropagation(),d(s),u(s.file)},children:e.jsxs("span",{className:h("flex border-2 justify-between items-center pl-1 pr-1 py-[0.125rem] min-w-[8rem] rounded-md group border-transparent border-r border-r-theme-darker dark:border-r-theme-lighter",n?"bg-neutral-200 border-neutral-200 text-neutral-900 dark:bg-dark-lighter dark:border-dark-lighter dark:text-primary-500":"bg-trasparent hover:bg-theme-darker dark:hover:bg-theme-lighter"),children:[e.jsx("small",{className:"text-xs",children:t}),e.jsx("small",{className:h("group-hover:hidden text-xs inline-block ml-3 mr-1 w-2 h-2 rounded-full",s.file.isChanged?"bg-warning-500":"bg-transparent")}),e.jsx(Ye,{className:"hidden group-hover:inline-block text-neutral-600 dark:text-neutral-100 w-4 h-4 ml-2 mr-0 cursor-pointer",onClick:i=>{i.stopPropagation(),x()}})]})})}const ye=24*60*60*1e3,Ns=1e3,J=50;function ys({tab:s,isOpen:t=!0,toggle:l}){const a=T(d=>d.models),u=T(d=>d.isModel),o=f.useMemo(()=>a.get(s.file.path),[s,a]);return e.jsx("div",{className:h("flex flex-col w-full h-full items-center overflow-hidden"),children:u(s.file.path)?E(o)&&e.jsx(Es,{tab:s,model:o,isOpen:t,toggle:l}):e.jsx(Ts,{tab:s,isOpen:t,toggle:l})})}function Es({tab:s,model:t,isOpen:l=!0,toggle:a}){const u=T(c=>c.environment),o=T(c=>c.environments),d=Array.from(o).filter(({isRemote:c})=>c).map(({name:c})=>({text:c,value:c}));return e.jsxs(D.Group,{children:[e.jsxs("div",{className:"flex w-full items-center",children:[e.jsx(F,{className:h("h-6 w-6 !px-0 border-none bg-neutral-10 dark:bg-neutral-20",l?"text-secondary-500 dark:text-secondary-300":"text-neutral-500 dark:text-neutral-300"),variant:_.Info,size:w.sm,onClick:c=>{c.stopPropagation(),a==null||a()},children:e.jsx(Ce,{className:"w-4 h-4"})}),l&&e.jsx(de,{className:"flex justify-center items-center",list:["Evaluate","Columns",d.length>1&&u.isRemote&&"Diff"].filter(Boolean)})]}),l&&e.jsxs(D.Panels,{className:"h-full w-full overflow-hidden",children:[e.jsx(D.Panel,{unmount:!1,className:h("flex flex-col w-full h-full relative overflow-hidden","ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2"),children:e.jsx(Ps,{model:t})}),e.jsx(D.Panel,{unmount:!1,className:"text-xs w-full h-full ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2 px-2",children:e.jsx(es,{nodeId:t.fqn,columns:t.columns,disabled:P(t.isModelSQL),withHandles:!1,withSource:!1,withDescription:!0,limit:10})}),d.length>1&&u.isRemote&&e.jsx(D.Panel,{unmount:!1,className:h("flex flex-col w-full h-full relative overflow-hidden","ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2"),children:e.jsx(ks,{tab:s,model:t,list:d.filter(({value:c})=>u.name!==c),target:{text:u.name,value:u.name}})})]})]})}function Ts({tab:s,isOpen:t=!0,toggle:l}){return e.jsxs(D.Group,{children:[e.jsxs("div",{className:"flex w-full items-center",children:[e.jsx(F,{className:h("h-6 w-6 !px-0 border-none bg-neutral-10 dark:bg-neutral-20",t?"text-secondary-500 dark:text-secondary-300":"text-neutral-500 dark:text-neutral-300"),variant:_.Info,size:w.sm,onClick:a=>{a.stopPropagation(),l==null||l()},children:e.jsx(Ce,{className:"w-4 h-4"})}),t&&e.jsx(de,{className:"flex justify-center items-center",list:["Run Query","Diff"]})]}),t&&e.jsxs(D.Panels,{className:"h-full w-full overflow-hidden",children:[e.jsx(D.Panel,{unmount:!1,className:h("flex flex-col w-full h-full relative overflow-hidden","ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2"),children:e.jsx(Cs,{tab:s})}),e.jsx(D.Panel,{unmount:!1,className:h("flex flex-col w-full h-full relative overflow-hidden","ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2"),children:e.jsx(Ds,{})})]})]})}function Ss({children:s}){return e.jsx("fieldset",{className:"flex my-3",children:s})}function K({children:s}){return e.jsx("div",{className:"flex w-full h-full py-1 overflow-hidden overflow-y-auto hover:scrollbar scrollbar--vertical",children:s})}function ee({children:s}){return e.jsx("div",{className:"flex w-full py-1 px-1 justify-end",children:s})}function Cs({tab:s}){const t=j(x=>x.setPreviewQuery),l=j(x=>x.setPreviewTable),a=j(x=>x.engine),{refetch:u,isFetching:o,cancel:d}=ze({sql:s.file.content});f.useEffect(()=>()=>{d()},[]);function c(){l(void 0),t(s.file.content),u().then(({data:x})=>{l(ue(x))})}return e.jsxs(e.Fragment,{children:[e.jsx(K,{}),e.jsx(V,{}),e.jsxs(ee,{children:[e.jsx(F,{size:w.sm,variant:_.Alternative,onClick:x=>{x.stopPropagation(),a.postMessage({topic:"format",payload:{sql:s.file.content}})},children:"Format"}),o?e.jsxs("div",{className:"flex items-center",children:[e.jsx(Z,{className:"w-3"}),e.jsx("small",{className:"text-xs text-neutral-400 block mx-2",children:"Running Query..."}),e.jsx(F,{size:w.sm,variant:_.Danger,onClick:x=>{x.stopPropagation(),d()},children:"Cancel"})]}):e.jsx(F,{size:w.sm,variant:_.Alternative,disabled:o,onClick:x=>{x.stopPropagation(),c()},children:"Run Query"})]})]})}function Ps({model:s}){const t=T(p=>p.environment),l=T(p=>p.isModel),a=j(p=>p.setPreviewQuery),u=j(p=>p.setPreviewTable),[o,d]=f.useState({model:s.displayName,start:le(ve(Date.now()-ye)),end:le(new Date),execution_time:le(ve(Date.now()-ye)),limit:1e3}),{refetch:c}=Ae(o),{refetch:x,isFetching:n,cancel:i}=Qe(o),N=l(s.path)&&Object.values(o).every(Boolean);f.useEffect(()=>()=>{i()},[]);function k(){a(void 0),u(void 0),c().then(({data:p})=>{a(p==null?void 0:p.sql)}),x().then(({data:p})=>{u(ue(p))})}return e.jsxs(e.Fragment,{children:[e.jsx(K,{children:e.jsxs("form",{className:"w-full",children:[P(N)&&e.jsx(Ss,{children:e.jsx(we,{variant:_.Warning,children:e.jsxs(we.Description,{className:"w-full mr-2 text-sm",children:["Please fill out all fields to ",e.jsx("b",{children:"evaluate the model"}),"."]})})}),e.jsxs("fieldset",{className:"px-2 w-full text-neutral-500",children:[e.jsx(b,{className:"w-full mx-0",label:"Start Date",size:w.sm,children:({className:p})=>e.jsx(b.Textfield,{className:h(p,"w-full"),placeholder:"02/11/2023",value:o.start,onInput:y=>{y.stopPropagation(),d({...o,start:y.target.value??""})}})}),e.jsx(b,{className:"w-full mx-0",label:"End Date",size:w.sm,children:({className:p})=>e.jsx(b.Textfield,{className:h(p,"w-full"),placeholder:"02/13/2023",value:o.end,onInput:y=>{y.stopPropagation(),d({...o,end:y.target.value??""})}})}),e.jsx(b,{className:"w-full mx-0",label:"Execution Time",size:w.sm,children:({className:p})=>e.jsx(b.Textfield,{className:h(p,"w-full"),placeholder:"02/13/2023",value:o.execution_time,onInput:y=>{y.stopPropagation(),d({...o,execution_time:y.target.value??""})}})}),E(o.limit)&&e.jsx(b,{className:"w-full mx-0",label:"Limit",size:w.sm,children:({className:p})=>e.jsx(b.Textfield,{className:h(p,"w-full"),type:"number",placeholder:"1000",value:o.limit,onInput:y=>{y.stopPropagation(),d({...o,limit:y.target.valueAsNumber??Ns})}})})]})]})}),e.jsx(V,{}),e.jsx(ee,{children:e.jsx("div",{className:"flex w-full justify-end",children:l(s.path)&&n?e.jsxs("div",{className:"flex items-center",children:[e.jsx(Z,{className:"w-3"}),e.jsx("small",{className:"text-xs text-neutral-400 block mx-2",children:"Evaluating..."}),e.jsx(F,{size:w.sm,variant:_.Danger,onClick:p=>{p.stopPropagation(),i()},children:"Cancel"})]}):e.jsx(F,{size:w.sm,variant:_.Alternative,disabled:P(N)||n||t.isInitialProd,onClick:p=>{p.stopPropagation(),k()},children:"Evaluate"})})})]})}function ks({tab:s,model:t,list:l,target:a}){const u=T(g=>g.isModel),o=j(g=>g.setPreviewDiff),[d,c]=f.useState(l[0].value),[x,n]=f.useState(J),[i,N]=f.useState(""),[k,p]=f.useState(""),{refetch:y,isFetching:R,cancel:r}=Ee({source:d,target:a.value,model_or_snapshot:t.name,limit:x,on:i,where:k}),v=f.useCallback(()=>{o(void 0),y().then(({data:g})=>{o(g)})},[t.name,t.hash]);f.useEffect(()=>()=>{r()},[]),f.useEffect(()=>{c(l[0].value)},[l]);const S=u(s.file.path)&&[d,a,x].every(Boolean);return e.jsxs(e.Fragment,{children:[e.jsx(K,{children:e.jsx("form",{className:"w-full",children:e.jsxs("fieldset",{className:"px-2 w-full text-neutral-500",children:[e.jsx(b,{className:"w-full mx-0",label:"Source",disabled:l.length<2,size:w.sm,children:({disabled:g,className:M})=>e.jsx(b.Selector,{className:h(M,"w-full"),list:l,value:d,disabled:g,onChange:c})}),e.jsx(b,{className:"w-full mx-0",label:"Target",disabled:!0,children:({disabled:g,className:M})=>e.jsx(b.Textfield,{className:h(M,"w-full"),disabled:g,value:a.value})}),e.jsx(b,{className:"w-full mx-0",label:"Limit",size:w.sm,children:({className:g})=>e.jsx(b.Textfield,{className:h(g,"w-full"),type:"number",placeholder:"1000",value:x,onInput:M=>{M.stopPropagation(),n(M.target.valueAsNumber??J)}})}),e.jsx(b,{className:"w-full mx-0",label:"ON",size:w.sm,children:({className:g})=>e.jsx(b.Textfield,{className:h(g,"w-full"),placeholder:"s.id = t.id",value:i,onInput:M=>{M.stopPropagation(),N(M.target.value)}})}),e.jsx(b,{className:"w-full mx-0",label:"WHERE",size:w.sm,children:({className:g})=>e.jsx(b.Textfield,{className:h(g,"w-full"),placeholder:"id > 10",value:k,onInput:M=>{M.stopPropagation(),p(M.target.value)}})})]})})}),e.jsx(V,{}),e.jsx(ee,{children:e.jsx("div",{className:"flex w-full justify-end items-center px-2",children:R?e.jsxs("div",{className:"flex items-center",children:[e.jsx(Z,{className:"w-3"}),e.jsx("small",{className:"text-xs text-neutral-400 block mx-2",children:"Getting Diff..."}),e.jsx(F,{size:w.sm,variant:_.Danger,onClick:g=>{g.stopPropagation(),r()},children:"Cancel"})]}):e.jsx(F,{className:"ml-2",size:w.sm,variant:_.Alternative,disabled:P(S)||R,onClick:g=>{g.stopPropagation(),v()},children:"Get Diff"})})})]})}function Ds(){const s=j(r=>r.setPreviewDiff),[t,l]=f.useState(""),[a,u]=f.useState(""),[o,d]=f.useState(J),[c,x]=f.useState(""),[n,i]=f.useState(""),{refetch:N,isFetching:k,cancel:p}=Ee({source:t,target:a,limit:o,on:c,where:n});f.useEffect(()=>()=>{p()},[]);function y(){s(void 0),N().then(({data:r})=>{s(r)})}const R=[t,a,o,c].every(Boolean);return e.jsxs(e.Fragment,{children:[e.jsx(K,{children:e.jsx("form",{className:"w-full",children:e.jsxs("fieldset",{className:"px-2 w-full text-neutral-500",children:[e.jsx(b,{className:"w-full mx-0",label:"Source",size:w.sm,children:({className:r})=>e.jsx(b.Textfield,{className:h(r,"w-full"),placeholder:"exp.tst_model__dev",value:t,onInput:v=>{v.stopPropagation(),l(v.target.value)}})}),e.jsx(b,{className:"w-full mx-0",label:"Target",size:w.sm,children:({className:r})=>e.jsx(b.Textfield,{className:h(r,"w-full"),placeholder:"exp.tst_snapshot__1353336088",value:a,onInput:v=>{v.stopPropagation(),u(v.target.value)}})}),e.jsx(b,{className:"w-full mx-0",label:"Limit",size:w.sm,children:({className:r})=>e.jsx(b.Textfield,{className:h(r,"w-full"),type:"number",placeholder:"1000",value:o,onInput:v=>{v.stopPropagation(),d(v.target.valueAsNumber??J)}})}),e.jsx(b,{className:"w-full mx-0",label:"ON",size:w.sm,children:({className:r})=>e.jsx(b.Textfield,{className:h(r,"w-full"),placeholder:"s.id = t.id",value:c,onInput:v=>{v.stopPropagation(),x(v.target.value)}})}),e.jsx(b,{className:"w-full mx-0",label:"WHERE",size:w.sm,children:({className:r})=>e.jsx(b.Textfield,{className:h(r,"w-full"),placeholder:"id > 10",value:n,onInput:v=>{v.stopPropagation(),i(v.target.value)}})})]})})}),e.jsx(V,{}),e.jsx(ee,{children:k?e.jsxs("div",{className:"flex items-center",children:[e.jsx(Z,{className:"w-3"}),e.jsx("small",{className:"text-xs text-neutral-400 block mx-2",children:"Getting Diff..."}),e.jsx(F,{size:w.sm,variant:_.Danger,onClick:r=>{r.stopPropagation(),p()},children:"Cancel"})]}):e.jsx(F,{className:"ml-2",size:w.sm,variant:_.Alternative,disabled:P(R)||k,onClick:r=>{r.stopPropagation(),y()},children:"Get Diff"})})]})}const U="s__",Y="t__",me="NULL";function Ms({source_schema:s,target_schema:t},l,a){const u=Array.from(new Set(a.flat())),o=Object.keys(s),d=Object.keys(t),x=Array.from(new Set(o.concat(d))).filter(N=>o.includes(N)&&d.includes(N)),n=o.filter(N=>!d.includes(N)),i=d.filter(N=>!o.includes(N));return{all:Array.from(new Set([u,l.modifiedColumns&&x,l.addedColumns&&i,l.removedColumns&&n].filter(Boolean).flat())),added:i.length,deleted:n.length,modified:x.length-u.length}}function _s(s,t,l){const a=Object.values(s.row_diff.sample)[0]??{},u=[],o=[],d=[];return Object.keys(a).forEach(c=>{H(s,c,l)?o.push(c):W(s,c,l)?u.push(c):d.push(c)}),{all:[t.modifiedRows&&d,t.addedRows&&o,t.removedRows&&u].filter(Boolean).flat(),added:o.length,deleted:u.length,modified:d.length}}function ce(s,t,l){const a=Q(s,U,t,l),u=Q(s,Y,t,l);return a!==u}function W(s,t,l){return l.every(([a,u])=>{const o=Q(s,U,a,t),d=Q(s,Y,u,t);return E(o)&&A(d)})}function H(s,t,l){return l.every(([a,u])=>{const o=Q(s,U,a,t),d=Q(s,Y,u,t);return A(o)&&E(d)})}function re(s,t,l,a){return l in s.schema_diff.added||l in s.schema_diff.removed?!1:t.some(u=>P(H(s,u,a))&&P(W(s,u,a))&&ce(s,l,u))}function Q(s,t,l,a){var u;return(u=s.row_diff.sample[`${t}${l}`])==null?void 0:u[a]}function Ls(s,t,l){return Q(s,U,t,l)??me}function Fs(s,t,l){return Q(s,Y,t,l)??me}function Rs({diff:s}){const[t,l]=f.useState({modifiedRows:!0,addedRows:!0,removedRows:!0,modifiedColumns:!0,addedColumns:!0,removedColumns:!0}),a=Ms(s.schema_diff,t,s.on),u=_s(s,t,s.on),o=t.addedRows&&!t.removedRows&&!t.modifiedRows,d=!t.addedRows&&t.removedRows&&!t.modifiedRows,c=Array.from(new Set(s.on.flat())),x=Object.values(s.row_diff.sample).some(n=>Object.keys(n).length>0);return e.jsxs("div",{className:"px-2 h-full flex flex-col rounded-lg",children:[x&&e.jsxs(e.Fragment,{children:[e.jsx(As,{diff:s,rows:u,columns:a}),e.jsx("div",{className:"mt-2 mb-1 flex rounded-lg items-center",children:e.jsx("div",{className:"w-full flex justify-end items-center",children:e.jsx(Xe,{options:Object.keys(t).reduce((n,i)=>(n[i]=N=>l(k=>({...k,[i]:N})),n),{}),value:Object.keys(t).map(n=>P(t[n])?void 0:n).filter(Boolean)})})})]}),e.jsx("div",{className:"overflow-auto h-full hover:scrollbar scrollbar--horizontal scrollbar--vertical",children:e.jsxs("table",{cellPadding:0,cellSpacing:0,className:"w-full text-xs text-neutral-600 dark:text-neutral-200 font-normal border-separate",children:[e.jsx("thead",{className:"sticky bg-theme top-0 z-10",children:e.jsx("tr",{children:a.all.map(n=>e.jsx("th",{colSpan:re(s,u.all,n,s.on)?2:1,className:h("text-left whitespace-nowrap py-1 px-2 font-bold",n in s.schema_diff.added?"border-t-2 border-l-2 border-r-2 border-success-500":n in s.schema_diff.removed?"border-t-2 border-l-2 border-r-2 border-danger-500":c.includes(n)?"border-brand-500 border-l-2 border-t-2 border-r-2":"border-r border-b border-neutral-100 dark:border-neutral-700 last:border-r-0",c.includes(n)?"bg-brand-10":"bg-neutral-5"),children:e.jsxs("div",{className:"flex justify-between",children:[e.jsxs("div",{className:"mr-2",children:[e.jsx("span",{children:n})," ",e.jsxs("small",{className:"text-neutral-500 font-medium",children:["(",s.schema_diff.source_schema[n]??s.schema_diff.target_schema[n],")"]})]}),P(c.includes(n))&&e.jsx("div",{className:"ml-2",children:e.jsxs("small",{className:"inline-block bg-neutral-10 px-2 py-0.5 rounded-full",children:[Math.round(u.all.filter(i=>ce(s,n,i)).length/u.all.length*100),"%"]})})]})},n))})}),e.jsx("tbody",{children:oe(u.all)?u.all.map(n=>e.jsx("tr",{children:a.all.map(i=>re(s,u.all,i,s.on)?e.jsxs(e.Fragment,{children:[e.jsx("td",{className:h("p-1 border-r border-b border-neutral-100 dark:border-neutral-700 last:border-r-0",H(s,n,s.on)&&"bg-success-10 text-success-500",W(s,n,s.on)&&"bg-danger-5 text-danger-500"),children:e.jsx("div",{className:h("px-2 py-1 whitespace-nowrap font-bold rounded-md ",H(s,n,s.on)&&"bg-success-10 text-success-500",W(s,n,s.on)&&"bg-danger-5 text-danger-500"),children:Ls(s,i,n)})},`${n}-${i}-source`),e.jsx("td",{className:h("p-1 border-r border-b border-neutral-100 dark:border-neutral-700 last:border-r-0",H(s,n,s.on)&&"bg-success-10 text-success-500",W(s,n,s.on)&&"bg-danger-5 text-danger-500"),children:e.jsx("div",{className:h("px-2 py-1 whitespace-nowrap font-bold rounded-md",ce(s,i,n)&&"bg-primary-10 text-primary-500",H(s,n,s.on)&&"!bg-success-10 !text-success-500",W(s,n,s.on)&&"!bg-danger-5 !text-danger-500"),children:Fs(s,i,n)})},`${n}-${i}-target`)]}):e.jsx("td",{className:h("p-1",i in s.schema_diff.added?"bg-success-10 border-l-2 border-r-2 border-success-500 text-success-500 font-bold":i in s.schema_diff.removed?"bg-danger-5 border-l-2 border-r-2 border-danger-500 !text-danger-500 font-bold":c.includes(i)?"border-brand-500 border-l-2 border-r-2":"border-r border-b border-neutral-100 dark:border-neutral-700 last:border-r-0",W(s,n,s.on)&&"!bg-danger-5 text-danger-500 font-bold",H(s,n,s.on)&&"bg-success-10 text-success-500 font-bold"),children:e.jsx("div",{className:h("px-2 py-1 whitespace-nowrap rounded-md",(i in s.schema_diff.added||H(s,n,s.on))&&"bg-success-10 text-success-500 font-bold",(i in s.schema_diff.removed||W(s,n,s.on))&&"!bg-danger-5 !text-danger-500 font-bold"),children:Q(s,U,i,n)??Q(s,Y,i,n)??me})},`${n}-${i}`))},n)):e.jsx(Je,{columns:a.all.length>0?a.all.length:void 0})}),oe(u.all)&&e.jsx("tfoot",{className:"sticky bg-theme bottom-0",children:e.jsx("tr",{children:a.all.map(n=>re(s,u.all,n,s.on)?e.jsxs(e.Fragment,{children:[e.jsx("th",{className:h("text-left whitespace-nowrap px-2 py-1 border-r border-t border-neutral-100 dark:border-neutral-700 last:border-r-0",c.includes(n)?"bg-brand-10":"bg-neutral-10"),children:"Source"},`${n}-source`),e.jsx("th",{className:h("text-left whitespace-nowrap px-2 py-1 border-r border-t border-neutral-100 dark:border-neutral-700 last:border-r-0",c.includes(n)?"bg-brand-10":"bg-primary-10"),children:"Target"},`${n}-target`)]}):e.jsxs("th",{className:h("text-left whitespace-nowrap px-2 py-1 font-bold",n in s.schema_diff.added?"border-b-2 border-l-2 border-r-2 border-success-500":n in s.schema_diff.removed?"border-b-2 border-l-2 border-r-2 border-danger-500":c.includes(n)?"border-brand-500 border-l-2 border-b-2 border-r-2":"border-r border-t border-neutral-100 dark:border-neutral-700 last:border-r-0",c.includes(n)?"bg-brand-10":"bg-neutral-10"),children:[(n in s.schema_diff.removed||d)&&e.jsx("span",{children:"Source"}),(n in s.schema_diff.added||o)&&e.jsx("span",{children:"Target"})]},n))})})]})}),e.jsxs("div",{className:"flex justify-between items-center px-2 mt-2",children:[e.jsx(Ze,{count:u.all.length}),e.jsx(Is,{})]})]})}function Is(){const s=[["Grain","bg-brand-500"],["Changed","bg-primary-500"],["Added","bg-success-500"],["Deleted","bg-danger-500"]];return e.jsx("div",{className:"flex text-xs",children:s.map(([t="",l])=>e.jsx(zs,{text:t,className:l},t))})}function zs({text:s,className:t}){return e.jsxs("div",{className:"flex ml-2 items-center",children:[e.jsx("span",{className:h("inline-block w-3 h-3 mr-2 rounded-full",t)}),e.jsx("small",{className:"text-neutral-600 dark:text-neutral-400",children:s})]})}function As({diff:s,rows:t,columns:l}){return e.jsx(ne,{defaultOpen:!1,children:({open:a})=>e.jsxs(e.Fragment,{children:[e.jsxs(ne.Button,{className:"flex items-center w-full justify-between rounded-lg text-left text-sm px-4 pt-3 pb-2 bg-neutral-10 hover:bg-theme-darker dark:hover:bg-theme-lighter text-neutral-600 dark:text-neutral-400",children:[e.jsx("h2",{className:"whitespace-nowrap text-xl font-bold mb-1",children:"Stats"}),a?e.jsx(ns,{className:"h-6 w-6 text-primary-500"}):e.jsx(rs,{className:"h-6 w-6 text-primary-500"})]}),e.jsx(ne.Panel,{className:"px-4 pb-2 text-sm text-neutral-500",children:e.jsxs("div",{className:"p-2 grid grid-cols-3 gap-4 mb-3",children:[e.jsx(ae,{text:"Row Count Change",children:e.jsxs("p",{className:"text-6xl font-light text-primary-500 mt-3",children:[Math.round(Math.abs(s.row_diff.count_pct_change)),e.jsx("small",{className:"text-sm",children:"%"})]})}),e.jsxs(ae,{text:"Column Count Change",count:t.all.length,children:[e.jsx("p",{className:"text-center text-6xl font-light text-primary-500 mt-3",children:t.modified}),e.jsx("p",{className:"text-center text-6xl font-light text-success-500 mt-3",children:t.added}),e.jsx("p",{className:"text-center text-6xl font-light text-danger-500 mt-3",children:t.deleted})]}),e.jsxs(ae,{text:"Column Changes",count:l.all.length,children:[e.jsx("p",{className:"text-center text-6xl font-light text-primary-500 mt-3",children:l.modified}),e.jsx("p",{className:"text-center text-6xl font-light text-success-500 mt-3",children:l.added}),e.jsx("p",{className:"text-center text-6xl font-light text-danger-500 mt-3",children:l.deleted})]})]})})]})})}function ae({text:s,children:t,className:l,count:a}){return e.jsxs("div",{className:h("rounded-xl overflow-hidden px-3 py-6 bg-primary-10",l),children:[e.jsxs("div",{className:"flex justify-between",children:[e.jsx("h3",{className:"text-neutral-500 dark:text-neutral-300 text-sm font-bold",children:s}),E(a)&&e.jsx("div",{children:e.jsx("small",{className:"inline-block px-2 py-0.5 bg-neutral-10 rounded-full",children:a})})]}),e.jsx("div",{className:"grid grid-cols-3 gap-2",children:t})]})}const Qs=f.lazy(async()=>await Oe(()=>import("./ModelLineage-393ad5ba.js"),["assets/ModelLineage-393ad5ba.js","assets/index-0556dabd.js","assets/index-daa9e59b.css","assets/context-4bbc2c1f.js","assets/_commonjs-dynamic-modules-302442b1.js","assets/Input-da5e8505.js","assets/editor-fd8b1606.js","assets/file-208ba368.js","assets/project-cc90bf2b.js","assets/SourceList-b301568f.js","assets/index-bad63c56.js","assets/transition-d6609a11.js","assets/context-595521ee.css","assets/ListboxShow-0ff5112b.js","assets/SearchList-f77620af.js"])),B={Query:"Query",Table:"Data Preview",Console:"Logs",Lineage:"Lineage",Diff:"Diff",Errors:"Errors"};function Os({tab:s,className:t}){const{errors:l,removeError:a}=Te(),u=Be(),o=T(g=>g.models),d=T(g=>g.isModel),c=j(g=>g.direction),x=j(g=>g.previewQuery),n=j(g=>g.previewTable),i=j(g=>g.previewDiff),N=j(g=>g.setDirection),[k,p]=f.useState(-1),y=Se(s.file.path,g=>{u(`${We.DocsModels}/${g.name}`)}),R=o.get(s.file.path),r=P(s.file.isEmpty)&&E(R)&&d(s.file.path),v=l.size>0,S=f.useMemo(()=>[E(n)&&B.Table,E(x)&&s.file.isRemote&&B.Query,r&&B.Lineage,E(i)&&B.Diff,v&&B.Errors].filter(Boolean),[s.id,n,x,i,r,l,v]);return f.useEffect(()=>{E(n)?p(S.indexOf(B.Table)):p(0)},[n]),f.useEffect(()=>{E(i)?p(S.indexOf(B.Diff)):p(0)},[i]),f.useEffect(()=>{E(r)?p(S.indexOf(B.Lineage)):p(0)},[r]),f.useEffect(()=>{p(v?S.indexOf(B.Errors):0)},[v]),f.useEffect(()=>{for(const g of l)He([z.Fetchdf,z.EvaluateModel,z.RenderQuery,z.ColumnLineage,z.ModelLineage,z.TableDiff,z.Table,z.SaveFile],g.key)&&a(g)},[n,i,x,r]),e.jsx("div",{className:h("w-full h-full flex flex-col text-prose overflow-auto hover:scrollbar scrollbar--vertical",t),children:$e(S)?e.jsx("div",{className:"flex justify-center items-center w-full h-full",children:e.jsx("h3",{className:"text-md",children:"No Data To Preview"})}):e.jsxs(D.Group,{onChange:p,selectedIndex:k,children:[e.jsx(de,{list:S,children:e.jsx("div",{className:"ml-2",children:e.jsx(F,{className:"!m-0 !py-0.5 px-[0.25rem] border-none",variant:_.Alternative,size:w.sm,onClick:()=>{N(c==="horizontal"?"vertical":"horizontal")},children:e.jsx(xs,{"aria-label":c==="horizontal"?"Use vertical layout":"Use horizontal layout",className:"text-primary-500 w-5"})})})},S.join("-")),e.jsxs(D.Panels,{className:"h-full w-full overflow-hidden",children:[E(n)&&e.jsx(D.Panel,{unmount:!1,className:h("w-full h-full pt-4 relative px-2","ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2"),children:e.jsx(Ke,{data:n})}),E(x)&&s.file.isRemote&&e.jsx(D.Panel,{unmount:!1,className:"w-full h-full ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2 p-2",children:e.jsx("div",{className:"w-full h-full p-2 bg-primary-10 rounded-lg overflow-auto hover:scrollbar scrollbar--horizontal scrollbar--vertical",children:e.jsx(ie,{type:$.SQL,content:x??"",extensions:y,className:"text-xs"})})}),r&&e.jsx(D.Panel,{unmount:!1,className:h("w-full h-full ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2"),children:e.jsx(f.Suspense,{fallback:e.jsx(Ge,{children:"Loading Model page..."}),children:e.jsx(Qs,{model:R})})}),E(i==null?void 0:i.row_diff)&&e.jsx(D.Panel,{unmount:!1,className:h("w-full h-full ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2 py-2"),children:e.jsx(Rs,{diff:i},s.id)}),v&&e.jsx(D.Panel,{unmount:!1,className:"w-full h-full ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2 py-2",children:e.jsx("ul",{className:"w-full h-full p-2 overflow-auto hover:scrollbar scrollbar--vertical scrollbar--horizontal",children:Array.from(l).reverse().map(g=>e.jsx("li",{className:"bg-danger-10 mb-4 last:m-0 p-2 rounded-md",children:e.jsx(as,{scope:g.key,error:g})},g.id))})})]})]},s.id)})}function fe(){const s=j(t=>t.tab);return e.jsxs("div",{className:"w-full h-full flex flex-col overflow-hidden",children:[e.jsx(ws,{}),e.jsx(V,{}),A(s)?e.jsx(xe,{}):e.jsx(Pe,{tab:s})]})}function xe(){return e.jsx("div",{className:"flex justify-center items-center w-full h-full",children:e.jsx("div",{className:"p-4 text-center text-theme-darker dark:text-theme-lighter",children:e.jsx("h2",{className:"text-3xl",children:"Select File or Add New SQL Tab"})})})}function Pe({tab:s}){const{errors:t,addError:l,removeError:a}=Te(),u=T(m=>m.environment),o=T(m=>m.models),d=T(m=>m.isModel),c=G(m=>m.files),x=G(m=>m.selectedFile),n=G(m=>m.setSelectedFile),i=j(m=>m.direction),N=j(m=>m.engine),k=j(m=>m.previewTable),p=j(m=>m.previewDiff),y=j(m=>m.refreshTab),R=j(m=>m.updateStoredTabsIds),r=j(m=>m.setPreviewQuery),v=j(m=>m.setPreviewTable),S=j(m=>m.setPreviewDiff),g=j(m=>m.setDialects),{setManuallySelectedColumn:M}=ss(),ke=f.useCallback(function(m){n(c.get(m.path))},[c]),De=f.useCallback(function(m,C){M([m,C])},[]),se=ts(),he=Se(s.file.path,ke,De),[pe,te]=f.useState(!1),Me=f.useMemo(()=>[...se,{key:"Shift-Mod-Enter",preventDefault:!0,run(m){const C=m.state.doc.toString();v(void 0),r(C);for(const O of t)O.key===z.Fetchdf&&a(O);return Ve({sql:C}).then(O=>{v(ue(O))}).catch(O=>{l(z.Fetchdf,{...O,errorKey:z.Fetchdf,trigger:"Editor -> customSQLKeymaps",message:O.message,timestamp:Date.now(),origin:"useQueryTimeout"})}),!0}}],[se,t]),ge=f.useCallback(m=>{if(m.data.topic==="dialects"){const C=o.get(s.file.path);s.dialect=(C==null?void 0:C.dialect)??"",g(m.data.payload),y(s)}if(m.data.topic==="format"){if(q(m.data.payload))return;s.file.content=m.data.payload,y(s)}},[s.id]),je=f.useCallback(function(C){s.file.content=C,y(s)},[s.id]);f.useEffect(()=>(N.addEventListener("message",ge),te(!1),A(x)&&n(s==null?void 0:s.file),()=>{N.removeEventListener("message",ge)}),[s.id]),f.useEffect(()=>{r(void 0),v(void 0),S(void 0),R()},[s.id,s.file.fingerprint]),f.useEffect(()=>{S(void 0)},[u]);function _e(){const m=o.get(s.file.path),C=P(s.file.isEmpty)&&E(m)&&d(s.file.path);return t.size>0||[k,p].some(Boolean)||C?[70,30]:[100,0]}function Le(){const m=o.get(s==null?void 0:s.file.path);return pe&&(E(m)&&d(s.file.path)||s.file.isLocal)&&P(q(s.file.content))?[70,30]:[100,0]}const X=32,Fe=2;return e.jsxs(be,{className:h("w-full h-full overflow-hidden",i==="vertical"?"flex flex-col":"flex"),sizes:_e(),direction:i,minSize:[X,0],snapOffset:0,children:[e.jsxs("div",{className:h("flex flex-col",i==="vertical"?"w-full ":"h-full"),children:[e.jsxs(be,{className:"flex h-full overflow-hidden",sizes:Le(),minSize:X,snapOffset:X,handleDrag:(m,C)=>{const Re=C.parent.getBoundingClientRect().width*(m[1]??0)/100;te(Re>=X+Fe)},children:[e.jsxs("div",{className:"flex flex-col h-full",children:[s.file.isLocal&&e.jsx(ie,{type:$.SQL,dialect:s.dialect,keymaps:Me,content:s.file.content,extensions:he,onChange:je}),s.file.isRemote&&e.jsx(ls,{keymaps:se,path:s.file.path,children:({file:m,keymaps:C})=>e.jsx(ie,{type:m.extension,dialect:s.dialect,extensions:he,keymaps:C,content:m.content,onChange:je})})]}),e.jsx("div",{className:"flex flex-col h-full",children:e.jsx(ys,{tab:s,toggle:()=>te(m=>!m),isOpen:pe})})]},s.id),e.jsx(V,{}),e.jsx(vs,{tab:s},s.file.fingerprint)]}),e.jsx(Os,{tab:s,className:h(i==="vertical"?"flex flex-col":"flex")})]},i)}fe.Empty=xe;fe.Loading=xe;fe.Main=Pe;export{fe as default};
