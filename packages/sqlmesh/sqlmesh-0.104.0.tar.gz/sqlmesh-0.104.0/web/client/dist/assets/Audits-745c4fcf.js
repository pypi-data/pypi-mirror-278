import{t as n,j as s,E as e,D as f,B as c,h as d,g as p,O as x}from"./index-0556dabd.js";import{P as j}from"./Page-ae43d5d2.js";import{u as h}from"./project-cc90bf2b.js";import{S as v}from"./SourceList-b301568f.js";import{S as A}from"./SourceListItem-34339f00.js";import"./SplitPane-3126158d.js";import"./file-208ba368.js";import"./Input-da5e8505.js";import"./index-bad63c56.js";function R(){const{pathname:a}=n(),i=h(t=>t.files),r=Array.from(i.values()).filter(t=>t.path.endsWith("audits"));return s.jsx(j,{sidebar:s.jsxs("div",{className:"flex flex-col w-full h-full",children:[s.jsx(v,{keyId:"basename",keyName:"basename",to:e.Audits,items:r,isActive:t=>`${e.Audits}/${t}`===a,className:"h-full",listItem:({to:t,name:o,description:m,text:l,disabled:u=!1})=>s.jsx(A,{to:t,name:o,text:l,description:m,disabled:u})}),s.jsx(f,{}),s.jsx("div",{className:"py-1 px-1 flex justify-end",children:s.jsx(c,{size:d.sm,variant:p.Neutral,children:"Run All"})})]}),content:s.jsx(x,{})})}export{R as default};
