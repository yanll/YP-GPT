(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[6366],{89301:function(e,t,l){(window.__NEXT_P=window.__NEXT_P||[]).push(["/app",function(){return l(99786)}])},91085:function(e,t,l){"use strict";var a=l(85893),n=l(32983),s=l(71577),r=l(67421);t.Z=function(e){let{error:t,description:l,refresh:i}=e,{t:o}=(0,r.$G)();return(0,a.jsx)(n.Z,{image:"/empty.png",imageStyle:{width:320,height:320,margin:"0 auto",maxWidth:"100%",maxHeight:"100%"},className:"flex items-center justify-center flex-col h-full w-full",description:t?(0,a.jsx)(s.ZP,{type:"primary",onClick:i,children:o("try_again")}):null!=l?l:o("no_data")})}},26892:function(e,t,l){"use strict";var a=l(85893),n=l(67294),s=l(66309),r=l(83062),i=l(94184),o=l.n(i),c=l(25675),d=l.n(c);t.Z=(0,n.memo)(function(e){let{icon:t,iconBorder:l=!0,title:i,desc:c,tags:u,children:m,disabled:p,operations:x,className:h,...f}=e,v=(0,n.useMemo)(()=>t?"string"==typeof t?(0,a.jsx)(d(),{className:o()("w-11 h-11 rounded-full mr-4 object-contain bg-white",{"border border-gray-200":l}),width:44,height:44,src:t,alt:i}):t:null,[t]),g=(0,n.useMemo)(()=>u&&u.length?(0,a.jsx)("div",{className:"flex items-center mt-1 flex-wrap",children:u.map((e,t)=>{var l;return"string"==typeof e?(0,a.jsx)(s.Z,{className:"text-xs",bordered:!1,color:"default",children:e},t):(0,a.jsx)(s.Z,{className:"text-xs",bordered:null!==(l=e.border)&&void 0!==l&&l,color:e.color,children:e.text},t)})}):null,[u]);return(0,a.jsxs)("div",{className:o()("group/card relative flex flex-col w-72 rounded justify-between text-black bg-white shadow-[0_8px_16px_-10px_rgba(100,100,100,.08)] hover:shadow-[0_14px_20px_-10px_rgba(100,100,100,.15)] dark:bg-[#232734] dark:text-white dark:hover:border-white transition-[transfrom_shadow] duration-300 hover:-translate-y-1 min-h-fit",{"grayscale cursor-no-drop":p,"cursor-pointer":!p&&!!f.onClick},h),...f,children:[(0,a.jsxs)("div",{className:"p-4",children:[(0,a.jsxs)("div",{className:"flex items-center",children:[v,(0,a.jsxs)("div",{className:"flex flex-col",children:[(0,a.jsx)("h2",{className:"text-sm font-semibold",children:i}),g]})]}),c&&(0,a.jsx)(r.Z,{title:c,children:(0,a.jsx)("p",{className:"mt-2 text-sm text-gray-500 font-normal line-clamp-2",children:c})})]}),(0,a.jsxs)("div",{children:[m,x&&!!x.length&&(0,a.jsx)("div",{className:"flex flex-wrap items-center justify-center border-t border-solid border-gray-100 dark:border-theme-dark",children:x.map((e,t)=>(0,a.jsx)(r.Z,{title:e.label,children:(0,a.jsxs)("div",{className:"relative flex flex-1 items-center justify-center h-11 text-gray-400 hover:text-blue-500 transition-colors duration-300 cursor-pointer",onClick:t=>{var l;t.stopPropagation(),null===(l=e.onClick)||void 0===l||l.call(e)},children:[e.children,t<x.length-1&&(0,a.jsx)("div",{className:"w-[1px] h-6 absolute top-2 right-0 bg-gray-100 rounded dark:bg-theme-dark"})]})},"operation-".concat(t)))})]})]})})},99743:function(e,t,l){"use strict";var a=l(85893);l(67294);var n=l(36851);t.Z=e=>{let{id:t,sourceX:l,sourceY:s,targetX:r,targetY:i,sourcePosition:o,targetPosition:c,style:d={},data:u,markerEnd:m}=e,[p,x,h]=(0,n.OQ)({sourceX:l,sourceY:s,sourcePosition:o,targetX:r,targetY:i,targetPosition:c}),f=(0,n._K)();return(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)(n.u5,{id:t,style:d,path:p,markerEnd:m}),(0,a.jsx)("foreignObject",{width:40,height:40,x:x-20,y:h-20,className:"bg-transparent w-10 h-10 relative",requiredExtensions:"http://www.w3.org/1999/xhtml",children:(0,a.jsx)("button",{className:"absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-5 h-5 rounded-full bg-stone-400 dark:bg-zinc-700 cursor-pointer text-sm",onClick:e=>{e.stopPropagation(),f.setEdges(f.getEdges().filter(e=>e.id!==t))},children:"\xd7"})})]})}},23391:function(e,t,l){"use strict";var a=l(85893);l(67294);var n=l(36851),s=l(59819),r=l(99743),i=l(67919);l(4583),t.Z=e=>{let{flowData:t,minZoom:l}=e,o=(0,i.z5)(t);return(0,a.jsx)(n.x$,{nodes:o.nodes,edges:o.edges,edgeTypes:{buttonedge:r.Z},fitView:!0,minZoom:l||.1,children:(0,a.jsx)(s.A,{color:"#aaa",gap:16})})}},99786:function(e,t,l){"use strict";l.r(t),l.d(t,{default:function(){return O}});var a=l(85893),n=l(39479),s=l(85418),r=l(42075),i=l(36147),o=l(75081),c=l(79531),d=l(51009),u=l(44442),m=l(67294),p=l(67421);function x(){return(0,a.jsx)("svg",{viewBox:"0 0 1024 1024",version:"1.1",xmlns:"http://www.w3.org/2000/svg","p-id":"5649",width:"1.5em",height:"1.5em",children:(0,a.jsx)("path",{d:"M810.666667 554.666667h-256v256h-85.333334v-256H213.333333v-85.333334h256V213.333333h85.333334v256h256v85.333334z","p-id":"5650",fill:"#bfbfbf"})})}var h=l(43893),f=l(71577),v=l(27704),g=l(85813),_=l(72269);function y(e){let{resourceTypeOptions:t,updateResourcesByIndex:l,index:n,resource:s}=e,{t:r}=(0,p.$G)(),[i,o]=(0,m.useState)(s.type||(null==t?void 0:t[0].label)),[u,x]=(0,m.useState)([]),[f,y]=(0,m.useState)({name:s.name,type:s.type,value:s.value,is_dynamic:s.is_dynamic||!1}),j=async()=>{let[e,t]=await (0,h.Vx)((0,h.RX)({type:i}));t?x(null==t?void 0:t.map(e=>({label:e,value:e}))):x([])},b=e=>{o(e)},w=(e,t)=>{f[t]=e,y(f),l(f,n)},N=()=>{l(null,n)};return(0,m.useEffect)(()=>{j(),w(f.type||i,"type")},[i]),(0,m.useEffect)(()=>{var e,t;w((null===(e=u[0])||void 0===e?void 0:e.label)||s.value,"value"),y({...f,value:(null===(t=u[0])||void 0===t?void 0:t.label)||s.value})},[u]),(0,a.jsx)(g.Z,{className:"mb-3 dark:bg-[#232734] border-gray-200",title:"".concat(r("resource")," ").concat(n+1),extra:(0,a.jsx)(v.Z,{className:"text-[#ff1b2e] !text-lg",onClick:()=>{N()}}),children:(0,a.jsxs)("div",{className:"flex-1",children:[(0,a.jsxs)("div",{className:"flex items-center  mb-6",children:[(0,a.jsxs)("div",{className:"font-bold mr-4 w-32 text-center",children:[(0,a.jsx)("span",{className:"text-[#ff4d4f] font-normal",children:"*"}),"\xa0",r("resource_name"),":"]}),(0,a.jsx)(c.default,{className:"w-1/3",required:!0,value:f.name,onInput:e=>{w(e.target.value,"name")}}),(0,a.jsxs)("div",{className:"flex items-center",children:[(0,a.jsx)("div",{className:"font-bold w-32 text-center",children:r("resource_dynamic")}),(0,a.jsx)(_.Z,{defaultChecked:s.is_dynamic||!1,style:{background:f.is_dynamic?"#1677ff":"#ccc"},onChange:e=>{w(e,"is_dynamic")}})]})]}),(0,a.jsxs)("div",{className:"flex mb-5  items-center",children:[(0,a.jsxs)("div",{className:"font-bold mr-4 w-32  text-center",children:[r("resource_type"),": "]}),(0,a.jsx)(d.default,{className:"w-1/3",options:t,value:f.type||(null==t?void 0:t[0]),onChange:e=>{w(e,"type"),b(e)}}),(0,a.jsxs)("div",{className:"font-bold w-32 text-center",children:[r("resource_value"),":"]}),(null==u?void 0:u.length)>0?(0,a.jsx)(d.default,{value:f.value,className:"flex-1",options:u,onChange:e=>{w(e,"value")}}):(0,a.jsx)(c.default,{className:"flex-1",value:f.value||s.value,onInput:e=>{w(e.target.value,"value")}})]})]})})}function j(e){var t;let{resourceTypes:l,updateDetailsByAgentKey:n,detail:s,editResources:r}=e,{t:i}=(0,p.$G)(),[o,u]=(0,m.useState)([...null!=r?r:[]]),[x,v]=(0,m.useState)({...s,resources:[]}),[g,_]=(0,m.useState)([]),[j,b]=(0,m.useState)([]),w=(e,t)=>{u(l=>{let a=[...l];return e?a.map((l,a)=>t===a?e:l):a.filter((e,l)=>t!==l)})},N=async()=>{let[e,t]=await (0,h.Vx)((0,h.Vd)());t&&_(null==t?void 0:t.map(e=>({label:e,value:e})))},k=async e=>{let[t,l]=await (0,h.Vx)((0,h.m9)(e));if(l){var a;b(null!==(a=l.map(e=>({label:e,value:e})))&&void 0!==a?a:[])}};(0,m.useEffect)(()=>{N(),k(s.llm_strategy)},[]),(0,m.useEffect)(()=>{C(o,"resources")},[o]);let C=(e,t)=>{let l={...x};l[t]=e,v(l),n(s.key,l)},Z=(0,m.useMemo)(()=>null==l?void 0:l.map(e=>({label:e,value:e})),[l]);return(0,a.jsxs)("div",{children:[(0,a.jsxs)("div",{className:"flex items-center mb-6 mt-6",children:[(0,a.jsxs)("div",{className:"mr-2 w-16 text-center",children:[i("Prompt"),":"]}),(0,a.jsx)(c.default,{required:!0,className:"mr-6 w-1/4",value:x.prompt_template,onChange:e=>{C(e.target.value,"prompt_template")}}),(0,a.jsxs)("div",{className:"mr-2",children:[i("LLM_strategy"),":"]}),(0,a.jsx)(d.default,{value:x.llm_strategy,options:g,className:"w-1/6 mr-6",onChange:e=>{C(e,"llm_strategy"),k(e)}}),j&&j.length>0&&(0,a.jsxs)(a.Fragment,{children:[(0,a.jsxs)("div",{className:"mr-2",children:[i("LLM_strategy_value"),":"]}),(0,a.jsx)(d.default,{value:(t=x.llm_strategy_value)?t.split(","):[],className:"w-1/4",mode:"multiple",options:j,onChange:e=>{if(!e||(null==e?void 0:e.length)===0)return C(null,"llm_strategy_value"),null;let t=e.reduce((e,t,l)=>0===l?t:"".concat(e,",").concat(t),"");C(t,"llm_strategy_value")}})]})]}),(0,a.jsx)("div",{className:"mb-3 text-lg font-bold",children:i("available_resources")}),o.map((e,t)=>(0,a.jsx)(y,{resource:e,index:t,updateResourcesByIndex:w,resourceTypeOptions:Z},t)),(0,a.jsx)(f.ZP,{type:"primary",className:"mt-2",size:"middle",onClick:()=>{u([...o,{name:"",type:"",introduce:"",value:"",is_dynamic:""}])},children:i("add_resource")})]})}var b=l(23391),w=l(41664),N=l.n(w),k=l(36609);function C(e){var t;let{onFlowsChange:l,teamContext:n}=e,[s,r]=(0,m.useState)(),[i,o]=(0,m.useState)(),[c,u]=(0,m.useState)(),p=async()=>{let[e,t]=await (0,h.Vx)((0,h.Wf)());if(t){var a;o(null==t?void 0:null===(a=t.items)||void 0===a?void 0:a.map(e=>({label:e.name,value:e.name}))),r(t.items),l(null==t?void 0:t.items[0])}};return(0,m.useEffect)(()=>{p()},[]),(0,m.useEffect)(()=>{u((null==s?void 0:s.find(e=>(null==n?void 0:n.name)===e.name))||(null==s?void 0:s[0]))},[n,s]),(0,a.jsxs)("div",{className:"w-full h-[300px]",children:[(0,a.jsx)("div",{className:"mr-24 mb-4 mt-2",children:"Flows:"}),(0,a.jsxs)("div",{className:"flex items-center mb-6",children:[(0,a.jsx)(d.default,{onChange:e=>{u(null==s?void 0:s.find(t=>e===t.name)),l(null==s?void 0:s.find(t=>e===t.name))},value:(null==c?void 0:c.name)||(null==i?void 0:null===(t=i[0])||void 0===t?void 0:t.value),className:"w-1/4",options:i}),(0,a.jsx)(N(),{href:"/flow/canvas/",className:"ml-6",children:(0,k.t)("edit_new_applications")}),(0,a.jsx)("div",{className:"text-gray-500 ml-16",children:null==c?void 0:c.description})]}),c&&(0,a.jsx)("div",{className:"w-full h-full border-[0.5px] border-dark-gray",children:(0,a.jsx)(b.Z,{flowData:null==c?void 0:c.flow_data})})]})}function Z(e){let{handleCancel:t,open:l,updateApps:f,type:v,app:g}=e,{t:_}=(0,p.$G)(),[y,b]=(0,m.useState)(!1),[w,N]=(0,m.useState)(),[k,Z]=(0,m.useState)(),[S,E]=(0,m.useState)([]),[V,T]=(0,m.useState)([]),[P,A]=(0,m.useState)([...(null==g?void 0:g.details)||[]]),[q,z]=(0,m.useState)(),[F,I]=(0,m.useState)(),[O,D]=(0,m.useState)(g.team_modal||"auto_plan"),[$]=n.Z.useForm(),G=[{value:"zh",label:_("Chinese")},{value:"en",label:_("English")}],H=async e=>{await (0,h.Vx)("add"===v?(0,h.L5)(e):(0,h.KT)(e)),await f()},K=async()=>{let e=g.details,[t,l]=await (0,h.Vx)((0,h.Q5)());(null==e?void 0:e.length)>0&&E(null==e?void 0:e.map(e=>({label:null==e?void 0:e.agent_name,children:(0,a.jsx)(j,{editResources:"edit"===v&&e.resources,detail:{key:null==e?void 0:e.agent_name,llm_strategy:null==e?void 0:e.llm_strategy,agent_name:null==e?void 0:e.agent_name,prompt_template:null==e?void 0:e.prompt_template,llm_strategy_value:null==e?void 0:e.llm_strategy_value},updateDetailsByAgentKey:R,resourceTypes:l}),key:null==e?void 0:e.agent_name})))},M=async()=>{let[e,t]=await (0,h.Vx)((0,h.lz)());if(!t)return null;let l=t.map(e=>({value:e,label:e}));Z(l)},B=async()=>{let[e,t]=await (0,h.Vx)((0,h.j8)());if(!t)return null;T(t.map(e=>({label:e.name,key:e.name,onClick:()=>{Q(e)},agent:e})).filter(e=>{var t,l;return g.details&&(null===(t=g.details)||void 0===t?void 0:t.length)!==0?null==g?void 0:null===(l=g.details)||void 0===l?void 0:l.every(t=>t.agent_name!==e.label):e}))},L=async()=>{let[e,t]=await (0,h.Vx)((0,h.Q5)());t&&I(t)};(0,m.useEffect)(()=>{M(),B(),L()},[]),(0,m.useEffect)(()=>{"edit"===v&&K()},[F]),(0,m.useEffect)(()=>{D(g.team_mode||"auto_plan")},[g]);let R=(e,t)=>{A(l=>l.map(l=>e===(l.agent_name||l.key)?t:l))},Q=async e=>{let t=e.name,[l,n]=await (0,h.Vx)((0,h.Q5)());N(t),A(e=>[...e,{key:t,name:"",llm_strategy:"priority"}]),E(e=>[...e,{label:t,children:(0,a.jsx)(j,{detail:{key:t,llm_strategy:"default",agent_name:t,prompt_template:"",llm_strategy_value:null},updateDetailsByAgentKey:R,resourceTypes:n}),key:t}]),T(t=>t.filter(t=>t.key!==e.name))},W=e=>{let t=w,l=-1;if(!S)return null;S.forEach((t,a)=>{t.key===e&&(l=a-1)});let a=S.filter(t=>t.key!==e);a.length&&t===e&&(t=l>=0?a[l].key:a[0].key),A(t=>null==t?void 0:t.filter(t=>(t.agent_name||t.key)!==e)),E(a),N(t),T(t=>[...t,{label:e,key:e,onClick:()=>{Q({name:e,describe:"",system_message:""})}}])},X=async()=>{let e=await $.validateFields();if(!e)return;b(!0);let l={...$.getFieldsValue()};if("edit"===v&&(l.app_code=g.app_code),"awel_layout"!==l.team_mode)l.details=P;else{let e={...q};delete e.flow_data,l.team_context=e}try{await H(l)}catch(e){return}b(!1),t()};return(0,a.jsx)("div",{children:(0,a.jsx)(i.default,{okText:_("Submit"),title:_("edit"===v?"edit_application":"add_application"),open:l,width:"65%",onCancel:t,onOk:X,destroyOnClose:!0,children:(0,a.jsx)(o.Z,{spinning:y,children:(0,a.jsxs)(n.Z,{form:$,preserve:!1,size:"large",className:"mt-4 max-h-[70vh] overflow-auto h-[90vh]",layout:"horizontal",labelAlign:"left",labelCol:{span:4},initialValues:{app_name:g.app_name,app_describe:g.app_describe,language:g.language||G[0].value,team_mode:g.team_mode||"auto_plan"},autoComplete:"off",onFinish:X,children:[(0,a.jsx)(n.Z.Item,{label:_("app_name"),name:"app_name",rules:[{required:!0,message:_("Please_input_the_name")}],children:(0,a.jsx)(c.default,{placeholder:_("Please_input_the_name")})}),(0,a.jsx)(n.Z.Item,{label:_("Description"),name:"app_describe",rules:[{required:!0,message:_("Please_input_the_description")}],children:(0,a.jsx)(c.default.TextArea,{rows:3,placeholder:_("Please_input_the_description")})}),(0,a.jsxs)("div",{className:"flex w-full",children:[(0,a.jsx)(n.Z.Item,{labelCol:{span:7},label:_("language"),name:"language",className:"w-1/2",rules:[{required:!0}],children:(0,a.jsx)(d.default,{className:"w-2/3 ml-4",placeholder:_("language_select_tips"),options:G})}),(0,a.jsx)(n.Z.Item,{label:_("team_modal"),name:"team_mode",className:"w-1/2",labelCol:{span:6},rules:[{required:!0}],children:(0,a.jsx)(d.default,{defaultValue:g.team_mode||"auto_plan",className:"ml-4 w-72",onChange:e=>{D(e)},placeholder:_("Please_input_the_work_modal"),options:k})})]}),"awel_layout"!==O?(0,a.jsxs)(a.Fragment,{children:[(0,a.jsx)("div",{className:"mb-5",children:_("Agents")}),(0,a.jsx)(u.Z,{addIcon:(0,a.jsx)(s.Z,{menu:{items:V},trigger:["click"],children:(0,a.jsx)("a",{className:"h-8 flex items-center",onClick:e=>e.preventDefault(),children:(0,a.jsx)(r.Z,{children:(0,a.jsx)(x,{})})})}),type:"editable-card",onChange:e=>{N(e)},activeKey:w,onEdit:(e,t)=>{"add"===t||W(e)},items:S})]}):(0,a.jsx)(C,{onFlowsChange:e=>{z(e)},teamContext:g.team_context})]})})})})}var S=l(28058),E=l(37017),V=l(90598),T=l(11163),P=l(41468),A=l(26892);let{confirm:q}=i.default;function z(e){let{updateApps:t,app:l,handleEdit:n,isCollected:s}=e,{model:r}=(0,m.useContext)(P.p),i=(0,T.useRouter)(),[o,c]=(0,m.useState)(l.is_collected),{setAgent:d}=(0,m.useContext)(P.p),{t:u}=(0,p.$G)(),x={en:u("English"),zh:u("Chinese")},f=()=>{q({title:u("Tips"),icon:(0,a.jsx)(S.Z,{}),content:"do you want delete the application?",okText:"Yes",okType:"danger",cancelText:"No",async onOk(){await (0,h.Vx)((0,h.Nl)({app_code:l.app_code})),t(s?{is_collected:s}:void 0)}})};(0,m.useEffect)(()=>{c(l.is_collected)},[l]);let g=async()=>{let[e]=await (0,h.Vx)("true"===o?(0,h.gD)({app_code:l.app_code}):(0,h.mo)({app_code:l.app_code}));e||(t(s?{is_collected:s}:void 0),c("true"===o?"false":"true"))},_=async()=>{null==d||d(l.app_code);let[,e]=await (0,h.Vx)((0,h.sW)({chat_mode:"chat_agent"}));e&&i.push("/chat/?scene=chat_agent&id=".concat(e.conv_uid).concat(r?"&model=".concat(r):""))};return(0,a.jsx)(A.Z,{title:l.app_name,icon:"/icons/node/vis.png",iconBorder:!1,desc:l.app_describe,tags:[{text:x[l.language],color:"default"},{text:l.team_mode,color:"default"}],onClick:()=>{n(l)},operations:[{label:u("Chat"),children:(0,a.jsx)(E.Z,{}),onClick:_},{label:u("collect"),children:(0,a.jsx)(V.Z,{className:"false"===l.is_collected?"text-gray-400":"text-yellow-400"}),onClick:g},{label:u("Delete"),children:(0,a.jsx)(v.Z,{}),onClick:()=>{f()}}]})}var F=l(24969),I=l(91085);function O(){let{t:e}=(0,p.$G)(),[t,l]=(0,m.useState)(!1),[n,s]=(0,m.useState)(!1),[r,i]=(0,m.useState)("app"),[c,d]=(0,m.useState)([]),[x,v]=(0,m.useState)(),[g,_]=(0,m.useState)("add"),y=()=>{_("add"),l(!0)},j=e=>{_("edit"),v(e),l(!0)},b=async function(){let e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};s(!0);let[t,l]=await (0,h.Vx)((0,h.yk)(e));if(t){s(!1);return}l&&(d(l||[]),s(!1))};(0,m.useEffect)(()=>{b()},[]);let w=t=>{let l=t.isCollected?c.every(e=>!e.is_collected):0===c.length;return(0,a.jsxs)("div",{children:[!t.isCollected&&(0,a.jsx)(f.ZP,{onClick:y,type:"primary",className:"mb-4",icon:(0,a.jsx)(F.Z,{}),children:e("create")}),l?(0,a.jsx)(I.Z,{}):(0,a.jsx)("div",{className:" w-full flex flex-wrap pb-0 gap-4",children:c.map((e,t)=>(0,a.jsx)(z,{handleEdit:j,app:e,updateApps:b,isCollected:"collected"===r},t))})]})},N=[{key:"app",label:e("App"),children:w({isCollected:!1})},{key:"collected",label:e("collected"),children:w({isCollected:!0})}];return(0,a.jsx)(a.Fragment,{children:(0,a.jsx)(o.Z,{spinning:n,children:(0,a.jsxs)("div",{className:"h-screen w-full p-4 md:p-6 overflow-y-auto",children:[(0,a.jsx)(u.Z,{defaultActiveKey:"app",items:N,onChange:e=>{i(e),"collected"===e?b({is_collected:!0}):b()}}),t&&(0,a.jsx)(Z,{app:"edit"===g?x:{},type:g,updateApps:b,open:t,handleCancel:()=>{l(!1)}})]})})})}},67919:function(e,t,l){"use strict";l.d(t,{Rv:function(){return r},VZ:function(){return a},Wf:function(){return n},z5:function(){return s}});let a=(e,t)=>{let l=0;return t.forEach(t=>{t.data.name===e.name&&l++}),"".concat(e.id,"_").concat(l)},n=e=>{let{nodes:t,edges:l,...a}=e,n=t.map(e=>{let{positionAbsolute:t,...l}=e;return{position_absolute:t,...l}}),s=l.map(e=>{let{sourceHandle:t,targetHandle:l,...a}=e;return{source_handle:t,target_handle:l,...a}});return{nodes:n,edges:s,...a}},s=e=>{let{nodes:t,edges:l,...a}=e,n=t.map(e=>{let{position_absolute:t,...l}=e;return{positionAbsolute:t,...l}}),s=l.map(e=>{let{source_handle:t,target_handle:l,...a}=e;return{sourceHandle:t,targetHandle:l,...a}});return{nodes:n,edges:s,...a}},r=e=>{let{nodes:t,edges:l}=e,a=[!0,t[0],""];e:for(let e=0;e<t.length;e++){let n=t[e].data,{inputs:s=[],parameters:r=[]}=n;for(let r=0;r<s.length;r++)if(!l.some(l=>l.targetHandle==="".concat(t[e].id,"|inputs|").concat(r))){a=[!1,t[e],"The input ".concat(s[r].type_name," of node ").concat(n.label," is required")];break e}for(let s=0;s<r.length;s++){let i=r[s];if(i.optional||"resource"!==i.category||l.some(l=>l.targetHandle==="".concat(t[e].id,"|parameters|").concat(s))){if(!i.optional&&"common"===i.category&&(void 0===i.value||null===i.value)){a=[!1,t[e],"The parameter ".concat(i.type_name," of node ").concat(n.label," is required")];break e}}else{a=[!1,t[e],"The parameter ".concat(i.type_name," of node ").concat(n.label," is required")];break e}}}return a}}},function(e){e.O(0,[8241,7113,5503,1009,9479,4442,5813,7434,9924,7958,9774,2888,179],function(){return e(e.s=89301)}),_N_E=e.O()}]);