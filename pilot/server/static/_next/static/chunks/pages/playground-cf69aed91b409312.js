(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[311],{57838:function(e,t,n){"use strict";n.d(t,{Z:function(){return i}});var r=n(67294);function i(){let[,e]=r.useReducer(e=>e+1,0);return e}},96074:function(e,t,n){"use strict";n.d(t,{Z:function(){return m}});var r=n(94184),i=n.n(r),a=n(67294),o=n(53124),l=n(14747),s=n(67968),c=n(45503);let d=e=>{let{componentCls:t,sizePaddingEdgeHorizontal:n,colorSplit:r,lineWidth:i}=e;return{[t]:Object.assign(Object.assign({},(0,l.Wf)(e)),{borderBlockStart:`${i}px solid ${r}`,"&-vertical":{position:"relative",top:"-0.06em",display:"inline-block",height:"0.9em",margin:`0 ${e.dividerVerticalGutterMargin}px`,verticalAlign:"middle",borderTop:0,borderInlineStart:`${i}px solid ${r}`},"&-horizontal":{display:"flex",clear:"both",width:"100%",minWidth:"100%",margin:`${e.dividerHorizontalGutterMargin}px 0`},[`&-horizontal${t}-with-text`]:{display:"flex",alignItems:"center",margin:`${e.dividerHorizontalWithTextGutterMargin}px 0`,color:e.colorTextHeading,fontWeight:500,fontSize:e.fontSizeLG,whiteSpace:"nowrap",textAlign:"center",borderBlockStart:`0 ${r}`,"&::before, &::after":{position:"relative",width:"50%",borderBlockStart:`${i}px solid transparent`,borderBlockStartColor:"inherit",borderBlockEnd:0,transform:"translateY(50%)",content:"''"}},[`&-horizontal${t}-with-text-left`]:{"&::before":{width:"5%"},"&::after":{width:"95%"}},[`&-horizontal${t}-with-text-right`]:{"&::before":{width:"95%"},"&::after":{width:"5%"}},[`${t}-inner-text`]:{display:"inline-block",padding:"0 1em"},"&-dashed":{background:"none",borderColor:r,borderStyle:"dashed",borderWidth:`${i}px 0 0`},[`&-horizontal${t}-with-text${t}-dashed`]:{"&::before, &::after":{borderStyle:"dashed none none"}},[`&-vertical${t}-dashed`]:{borderInlineStartWidth:i,borderInlineEnd:0,borderBlockStart:0,borderBlockEnd:0},[`&-plain${t}-with-text`]:{color:e.colorText,fontWeight:"normal",fontSize:e.fontSize},[`&-horizontal${t}-with-text-left${t}-no-default-orientation-margin-left`]:{"&::before":{width:0},"&::after":{width:"100%"},[`${t}-inner-text`]:{paddingInlineStart:n}},[`&-horizontal${t}-with-text-right${t}-no-default-orientation-margin-right`]:{"&::before":{width:"100%"},"&::after":{width:0},[`${t}-inner-text`]:{paddingInlineEnd:n}}})}};var u=(0,s.Z)("Divider",e=>{let t=(0,c.TS)(e,{dividerVerticalGutterMargin:e.marginXS,dividerHorizontalWithTextGutterMargin:e.margin,dividerHorizontalGutterMargin:e.marginLG});return[d(t)]},{sizePaddingEdgeHorizontal:0}),h=function(e,t){var n={};for(var r in e)Object.prototype.hasOwnProperty.call(e,r)&&0>t.indexOf(r)&&(n[r]=e[r]);if(null!=e&&"function"==typeof Object.getOwnPropertySymbols)for(var i=0,r=Object.getOwnPropertySymbols(e);i<r.length;i++)0>t.indexOf(r[i])&&Object.prototype.propertyIsEnumerable.call(e,r[i])&&(n[r[i]]=e[r[i]]);return n},m=e=>{let{getPrefixCls:t,direction:n,divider:r}=a.useContext(o.E_),{prefixCls:l,type:s="horizontal",orientation:c="center",orientationMargin:d,className:m,rootClassName:f,children:p,dashed:x,plain:g,style:b}=e,v=h(e,["prefixCls","type","orientation","orientationMargin","className","rootClassName","children","dashed","plain","style"]),j=t("divider",l),[w,y]=u(j),$=c.length>0?`-${c}`:c,_=!!p,S="left"===c&&null!=d,N="right"===c&&null!=d,k=i()(j,null==r?void 0:r.className,y,`${j}-${s}`,{[`${j}-with-text`]:_,[`${j}-with-text${$}`]:_,[`${j}-dashed`]:!!x,[`${j}-plain`]:!!g,[`${j}-rtl`]:"rtl"===n,[`${j}-no-default-orientation-margin-left`]:S,[`${j}-no-default-orientation-margin-right`]:N},m,f),P=a.useMemo(()=>"number"==typeof d?d:/^\d+$/.test(d)?Number(d):d,[d]),O=Object.assign(Object.assign({},S&&{marginLeft:P}),N&&{marginRight:P});return w(a.createElement("div",Object.assign({className:k,style:Object.assign(Object.assign({},null==r?void 0:r.style),b)},v,{role:"separator"}),p&&"vertical"!==s&&a.createElement("span",{className:`${j}-inner-text`,style:O},p)))}},63746:function(e,t,n){(window.__NEXT_P=window.__NEXT_P||[]).push(["/playground",function(){return n(67183)}])},81799:function(e,t,n){"use strict";n.d(t,{A:function(){return u}});var r=n(85893),i=n(41468),a=n(51009),o=n(75957),l=n(25675),s=n.n(l),c=n(67294),d=n(67421);function u(e,t){var n;let{width:i,height:a}=t||{};return e?(0,r.jsx)(s(),{className:"rounded-full border border-gray-200 object-contain bg-white inline-block",width:i||24,height:a||24,src:(null===(n=o.Hf[e])||void 0===n?void 0:n.icon)||"/models/huggingface.svg",alt:"llm"}):null}t.Z=function(e){let{onChange:t}=e,{t:n}=(0,d.$G)(),{modelList:l,model:s}=(0,c.useContext)(i.p);return!l||l.length<=0?null:(0,r.jsx)(a.default,{value:s,placeholder:n("choose_model"),className:"w-52",onChange:e=>{null==t||t(e)},children:l.map(e=>{var t;return(0,r.jsx)(a.default.Option,{children:(0,r.jsxs)("div",{className:"flex items-center",children:[u(e),(0,r.jsx)("span",{className:"ml-2",children:(null===(t=o.Hf[e])||void 0===t?void 0:t.label)||e})]})},e)})})}},38954:function(e,t,n){"use strict";n.d(t,{Z:function(){return j}});var r=n(85893),i=n(27496),a=n(59566),o=n(71577),l=n(67294),s=n(2487),c=n(83062),d=n(2453),u=n(74627),h=n(39479),m=n(51009),f=n(58299),p=n(577),x=n(30119),g=n(67421);let b=e=>{let{data:t,loading:n,submit:i,close:a}=e,{t:o}=(0,g.$G)(),l=e=>()=>{i(e),a()};return(0,r.jsx)("div",{style:{maxHeight:400,overflow:"auto"},children:(0,r.jsx)(s.Z,{dataSource:null==t?void 0:t.data,loading:n,rowKey:e=>e.prompt_name,renderItem:e=>(0,r.jsx)(s.Z.Item,{onClick:l(e.content),children:(0,r.jsx)(c.Z,{title:e.content,children:(0,r.jsx)(s.Z.Item.Meta,{style:{cursor:"copy"},title:e.prompt_name,description:o("Prompt_Info_Scene")+"：".concat(e.chat_scene,"，")+o("Prompt_Info_Sub_Scene")+"：".concat(e.sub_chat_scene)})})},e.prompt_name)})})};var v=e=>{let{submit:t}=e,{t:n}=(0,g.$G)(),[i,a]=(0,l.useState)(!1),[o,s]=(0,l.useState)("common"),{data:v,loading:j}=(0,p.Z)(()=>(0,x.PR)("/prompt/list",{prompt_type:o}),{refreshDeps:[o],onError:e=>{d.ZP.error(null==e?void 0:e.message)}});return(0,r.jsx)(u.Z,{title:(0,r.jsx)(h.Z.Item,{label:"Prompt "+n("Type"),children:(0,r.jsx)(m.default,{style:{width:130},value:o,onChange:e=>{s(e)},options:[{label:n("Public")+" Prompts",value:"common"},{label:n("Private")+" Prompts",value:"private"}]})}),content:(0,r.jsx)(b,{data:v,loading:j,submit:t,close:()=>{a(!1)}}),placement:"topRight",trigger:"click",open:i,onOpenChange:e=>{a(e)},children:(0,r.jsx)(c.Z,{title:n("Click_Select")+" Prompt",children:(0,r.jsx)(f.Z,{className:"bottom-32"})})})},j=function(e){let{children:t,loading:n,onSubmit:s,...c}=e,[d,u]=(0,l.useState)("");return(0,r.jsxs)(r.Fragment,{children:[(0,r.jsx)(a.default.TextArea,{className:"flex-1",size:"large",value:d,autoSize:{minRows:1,maxRows:4},...c,onPressEnter:e=>{if(d.trim()&&13===e.keyCode){if(e.shiftKey){u(e=>e+"\n");return}s(d),setTimeout(()=>{u("")},0)}},onChange:e=>{if("number"==typeof c.maxLength){u(e.target.value.substring(0,c.maxLength));return}u(e.target.value)}}),(0,r.jsx)(o.ZP,{className:"ml-2 flex items-center justify-center",size:"large",type:"text",loading:n,icon:(0,r.jsx)(i.Z,{}),onClick:()=>{s(d)}}),(0,r.jsx)(v,{submit:e=>{u(d+e)}}),t]})}},67183:function(e,t,n){"use strict";n.r(t);var r=n(85893),i=n(577),a=n(67294),o=n(96074),l=n(75081),s=n(39332),c=n(25675),d=n.n(c),u=n(92401),h=n(81799),m=n(41468),f=n(38954),p=n(67421),x=n(75957);t.default=()=>{let e=(0,s.useRouter)(),{model:t,setModel:n}=(0,a.useContext)(m.p),{t:c}=(0,p.$G)(),[g,b]=(0,a.useState)(!1),[v,j]=(0,a.useState)(!1),{data:w=[]}=(0,i.Z)(async()=>{j(!0);let[,e]=await (0,u.Vx)((0,u.CU)());return j(!1),null!=e?e:[]}),y=async n=>{b(!0);let[,r]=await (0,u.Vx)((0,u.sW)({chat_mode:"chat_normal"}));r&&(localStorage.setItem(x.rU,JSON.stringify({id:r.conv_uid,message:n})),e.push("/chat/?scene=chat_normal&id=".concat(r.conv_uid).concat(t?"&model=".concat(t):""))),b(!1)},$=async n=>{let[,r]=await (0,u.Vx)((0,u.sW)({chat_mode:"chat_normal"}));r&&e.push("/chat?scene=".concat(n.chat_scene,"&id=").concat(r.conv_uid).concat(t?"&model=".concat(t):""))};return(0,r.jsxs)("div",{className:"mx-auto h-full justify-center flex max-w-3xl flex-col px-4",children:[(0,r.jsx)("div",{className:"my-0 mx-auto",children:(0,r.jsx)(d(),{src:"/LOGO.png",alt:"Revolutionizing Database Interactions with Private LLM Technology",width:856,height:160,className:"w-full",unoptimized:!0})}),(0,r.jsx)(o.Z,{className:"!text-[#878c93] !my-6",plain:!0,children:c("Quick_Start")}),(0,r.jsx)(l.Z,{spinning:v,children:(0,r.jsx)("div",{className:"flex flex-wrap -m-1 md:-m-3",children:w.map(e=>(0,r.jsx)("div",{className:"w-full sm:w-1/2 lg:w-1/3 p-1 md:p-3",children:(0,r.jsx)("div",{className:"cursor-pointer flex items-center justify-center w-full h-12 rounded font-semibold text-sm bg-[#E6F4FF] text-[#1677FE] dark:text-gray-100 dark:bg-[#4E4F56]",onClick:()=>{$(e)},children:e.scene_name})},e.chat_scene))})}),(0,r.jsx)("div",{className:"mt-8 mb-2",children:(0,r.jsx)(h.Z,{onChange:e=>{n(e)}})}),(0,r.jsx)("div",{className:"flex",children:(0,r.jsx)(f.Z,{loading:g,onSubmit:y})})]})}},30119:function(e,t,n){"use strict";n.d(t,{Tk:function(){return l},PR:function(){return s}});var r=n(2453),i=n(6154);let a=i.default.create({baseURL:"http://localhost:5000"});a.defaults.timeout=1e4,a.interceptors.response.use(e=>e.data,e=>Promise.reject(e)),n(96486);let o={"content-type":"application/json"},l=(e,t)=>{if(t){let n=Object.keys(t).filter(e=>void 0!==t[e]&&""!==t[e]).map(e=>"".concat(e,"=").concat(t[e])).join("&");n&&(e+="?".concat(n))}return a.get("/api"+e,{headers:o}).then(e=>e).catch(e=>{r.ZP.error(e),Promise.reject(e)})},s=(e,t)=>a.post(e,t,{headers:o}).then(e=>e).catch(e=>{r.ZP.error(e),Promise.reject(e)})}},function(e){e.O(0,[662,44,479,9,411,719,539,774,888,179],function(){return e(e.s=63746)}),_N_E=e.O()}]);