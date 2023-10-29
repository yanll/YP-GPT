(self.webpackChunk_N_E=self.webpackChunk_N_E||[]).push([[265],{54681:function(e,t,l){(window.__NEXT_P=window.__NEXT_P||[]).push(["/knowledge",function(){return l(4223)}])},47207:function(e,t,l){"use strict";l.d(t,{Z:function(){return c}});var s=l(85893),a=l(27595),n=l(27329),i=l(68346);function c(e){let{type:t}=e;return"TEXT"===t?(0,s.jsx)(a.Z,{className:"text-[#2AA3FF] mr-2 !text-lg"}):"DOCUMENT"===t?(0,s.jsx)(n.Z,{className:"text-[#2AA3FF] mr-2 !text-lg"}):(0,s.jsx)(i.Z,{className:"text-[#2AA3FF] mr-2 !text-lg"})}},4223:function(e,t,l){"use strict";l.r(t),l.d(t,{default:function(){return es}});var s=l(85893),a=l(67294),n=l(24969),i=l(71577),c=l(12069),r=l(3363),o=l(46735),d=l(74627),m=l(40411),u=l(11163),x=l(25675),h=l.n(x),p=l(28058),_=l(31484),j=l(78346),f=l(83062),b=l(66309),g=l(85813),N=l(32983),Z=l(42075),w=l(96074),y=l(75081),k=l(31326),v=l(88008),T=l(27704),P=l(18754),S=l(92401),C=l(30381),F=l.n(C),D=l(59566),E=l(71230),I=l(15746),A=l(39479),V=l(44442),z=l(67421),O=l(31545),q=l(6321);let{TextArea:U}=D.default;function M(e){let{space:t,argumentsShow:l,setArgumentsShow:n}=e,{t:r}=(0,z.$G)(),[o,d]=(0,a.useState)(),[m,u]=(0,a.useState)(!1),x=async()=>{let[e,l]=await (0,S.Vx)((0,S.Tu)(t.name));d(l)};(0,a.useEffect)(()=>{x()},[t.name]);let h=[{key:"Embedding",label:(0,s.jsxs)("div",{children:[(0,s.jsx)(O.Z,{}),r("Embedding")]}),children:(0,s.jsxs)(E.Z,{gutter:24,children:[(0,s.jsx)(I.Z,{span:12,offset:0,children:(0,s.jsx)(A.Z.Item,{tooltip:r("the_top_k_vectors"),rules:[{required:!0}],label:r("topk"),name:["embedding","topk"],children:(0,s.jsx)(D.default,{className:"mb-5 h-12"})})}),(0,s.jsx)(I.Z,{span:12,children:(0,s.jsx)(A.Z.Item,{tooltip:r("Set_a_threshold_score"),rules:[{required:!0}],label:r("recall_score"),name:["embedding","recall_score"],children:(0,s.jsx)(D.default,{className:"mb-5  h-12",placeholder:r("Please_input_the_owner")})})}),(0,s.jsx)(I.Z,{span:12,children:(0,s.jsx)(A.Z.Item,{tooltip:r("Recall_Type"),rules:[{required:!0}],label:r("recall_type"),name:["embedding","recall_type"],children:(0,s.jsx)(D.default,{className:"mb-5  h-12"})})}),(0,s.jsx)(I.Z,{span:12,children:(0,s.jsx)(A.Z.Item,{tooltip:r("A_model_used"),rules:[{required:!0}],label:r("model"),name:["embedding","model"],children:(0,s.jsx)(D.default,{className:"mb-5  h-12"})})}),(0,s.jsx)(I.Z,{span:12,children:(0,s.jsx)(A.Z.Item,{tooltip:r("The_size_of_the_data_chunks"),rules:[{required:!0}],label:r("chunk_size"),name:["embedding","chunk_size"],children:(0,s.jsx)(D.default,{className:"mb-5  h-12"})})}),(0,s.jsx)(I.Z,{span:12,children:(0,s.jsx)(A.Z.Item,{tooltip:r("The_amount_of_overlap"),rules:[{required:!0}],label:r("chunk_overlap"),name:["embedding","chunk_overlap"],children:(0,s.jsx)(D.default,{className:"mb-5  h-12",placeholder:r("Please_input_the_description")})})})]})},{key:"Prompt",label:(0,s.jsxs)("div",{children:[(0,s.jsx)(q.Z,{}),r("Embedding")]}),children:(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(A.Z.Item,{tooltip:r("A_contextual_parameter"),label:r("scene"),name:["prompt","scene"],children:(0,s.jsx)(U,{rows:4,className:"mb-2"})}),(0,s.jsx)(A.Z.Item,{tooltip:r("structure_or_format"),label:r("template"),name:["prompt","template"],children:(0,s.jsx)(U,{rows:7,className:"mb-2"})}),(0,s.jsx)(A.Z.Item,{tooltip:r("The_maximum_number_of_tokens"),label:r("max_token"),name:["prompt","max_token"],children:(0,s.jsx)(D.default,{className:"mb-2"})})]})}],p=async e=>{u(!0);let[l,s,a]=await (0,S.Vx)((0,S.iH)(t.name,{argument:JSON.stringify(e)}));u(!1),(null==a?void 0:a.success)&&n(!1)};return(0,s.jsx)(c.default,{width:850,open:l,onCancel:()=>{n(!1)},footer:null,children:(0,s.jsx)(y.Z,{spinning:m,children:(0,s.jsxs)(A.Z,{size:"large",className:"mt-4",layout:"vertical",name:"basic",initialValues:{...o},autoComplete:"off",onFinish:p,children:[(0,s.jsx)(V.Z,{items:h}),(0,s.jsxs)("div",{className:"mt-3 mb-3",children:[(0,s.jsx)(i.ZP,{htmlType:"submit",type:"primary",className:"mr-6",children:r("Submit")}),(0,s.jsx)(i.ZP,{onClick:()=>{n(!1)},children:r("close")})]})]})})})}var G=l(47207);let{confirm:R}=c.default;function H(e){let{space:t}=e,{t:l}=(0,z.$G)(),c=(0,u.useRouter)(),[r,o]=(0,a.useState)(!1),[d,m]=(0,a.useState)([]),[x,h]=(0,a.useState)(!1),_=e=>{R({title:l("Tips"),icon:(0,s.jsx)(p.Z,{}),content:"".concat(l("Del_Document_Tips"),"?"),okText:"Yes",okType:"danger",cancelText:"No",async onOk(){await D(e)}})};async function j(){o(!0);let[e,l]=await (0,S.Vx)((0,S._Q)(t.name,{page:1,page_size:20}));o(!1),m(null==l?void 0:l.data)}let C=async(e,t)=>{await (0,S.Vx)((0,S.Hx)(e,{doc_ids:[t]}))},D=async l=>{await (0,S.Vx)((0,S.n3)(t.name,{doc_name:l.doc_name})),j(),e.onDeleteDoc()},E=()=>{e.onAddDoc(t.name)},I=(e,t)=>{let l;switch(e){case"TODO":l="gold";break;case"RUNNING":l="#2db7f5";break;case"FINISHED":l="#87d068";break;default:l="f50"}return(0,s.jsx)(f.Z,{title:t,children:(0,s.jsx)(b.Z,{color:l,children:e})})};return(0,a.useEffect)(()=>{j()},[t]),(0,s.jsxs)("div",{className:"collapse-container pt-2 px-4",children:[(0,s.jsxs)(Z.Z,{children:[(0,s.jsx)(i.ZP,{size:"middle",type:"primary",className:"flex items-center",icon:(0,s.jsx)(n.Z,{}),onClick:E,children:l("Add_Datasource")}),(0,s.jsx)(i.ZP,{size:"middle",className:"flex items-center mx-2",icon:(0,s.jsx)(P.Z,{}),onClick:()=>{h(!0)},children:"Arguments"})]}),(0,s.jsx)(w.Z,{}),(0,s.jsx)(y.Z,{spinning:r,children:(null==d?void 0:d.length)>0?(0,s.jsx)("div",{className:"max-h-96 mt-3 grid grid-cols-1 gap-x-6 gap-y-5 sm:grid-cols-2 lg:grid-cols-3 xl:gap-x-5 overflow-auto",children:d.map(e=>(0,s.jsxs)(g.Z,{className:" dark:bg-[#484848] relative  shrink-0 grow-0 cursor-pointer rounded-[10px] border border-gray-200 border-solid w-full",title:(0,s.jsx)(f.Z,{title:e.doc_name,children:(0,s.jsxs)("div",{className:"truncate ",children:[(0,s.jsx)(G.Z,{type:e.doc_type}),(0,s.jsx)("span",{children:e.doc_name})]})}),extra:(0,s.jsxs)("div",{className:"mx-3",children:[(0,s.jsx)(f.Z,{title:"detail",children:(0,s.jsx)(k.Z,{className:"mr-2 !text-lg",style:{color:"#1b7eff",fontSize:"20px"},onClick:()=>{c.push("/knowledge/chunk/?spaceName=".concat(t.name,"&id=").concat(e.id))}})}),(0,s.jsx)(f.Z,{title:"Sync",children:(0,s.jsx)(v.Z,{className:"mr-2 !text-lg",style:{color:"#1b7eff",fontSize:"20px"},onClick:()=>{C(t.name,e.id)}})}),(0,s.jsx)(f.Z,{title:"Delete",children:(0,s.jsx)(T.Z,{className:"text-[#ff1b2e] !text-lg",onClick:()=>{_(e)}})})]}),children:[(0,s.jsxs)("p",{className:"mt-2 font-semibold ",children:[l("Size"),":"]}),(0,s.jsxs)("p",{children:[e.chunk_size," chunks"]}),(0,s.jsxs)("p",{className:"mt-2 font-semibold ",children:[l("Last_Synch"),":"]}),(0,s.jsx)("p",{children:F()(e.last_sync).format("YYYY-MM-DD HH:MM:SS")}),(0,s.jsx)("p",{className:"mt-2 mb-2",children:I(e.status,e.result)})]},e.id))}):(0,s.jsx)(N.Z,{image:N.Z.PRESENTED_IMAGE_DEFAULT,children:(0,s.jsx)(i.ZP,{type:"primary",className:"flex items-center mx-auto",icon:(0,s.jsx)(n.Z,{}),onClick:E,children:"Create Now"})})}),(0,s.jsx)(M,{space:t,argumentsShow:x,setArgumentsShow:h})]})}var L=l(75957);let{confirm:Y}=c.default;function $(e){var t;let l=(0,u.useRouter)(),{t:a}=(0,z.$G)(),{space:n,getSpaces:c}=e,r=()=>{Y({title:a("Tips"),icon:(0,s.jsx)(p.Z,{}),content:"".concat(a("Del_Knowledge_Tips"),"?"),okText:"Yes",okType:"danger",cancelText:"No",async onOk(){await (0,S.Vx)((0,S.XK)({name:null==n?void 0:n.name})),c()}})},x=async e=>{e.stopPropagation();let[t,s]=await (0,S.Vx)((0,S.sW)({chat_mode:"chat_knowledge"}));(null==s?void 0:s.conv_uid)&&l.push("/chat?scene=chat_knowledge&id=".concat(null==s?void 0:s.conv_uid,"&db_param=").concat(n.name))};return(0,s.jsx)(o.ZP,{theme:{components:{Popover:{zIndexPopup:90}}},children:(0,s.jsx)(d.Z,{className:"dark:hover:border-white transition-all hover:shadow-md bg-[#FFFFFF] dark:bg-[#484848] cursor-pointer rounded-[10px] border border-gray-200 border-solid",placement:"bottom",trigger:"click",content:(0,s.jsx)(H,{space:n,onAddDoc:e.onAddDoc,onDeleteDoc:function(){c()}}),children:(0,s.jsxs)(m.Z,{className:"mr-4 mb-4 min-w-[200px] sm:w-60 lg:w-72",count:n.docs||0,children:[(0,s.jsxs)("div",{className:"flex justify-between mx-6 mt-3",children:[(0,s.jsxs)("div",{className:"text-lg font-bold text-black truncate",children:[(t=n.vector_type,(0,s.jsx)(h(),{className:"rounded-full w-8 h-8 border border-gray-200 object-contain bg-white inline-block",width:36,height:136,src:L.l3[t]||"/models/knowledge-default.jpg",alt:"llm"})),(0,s.jsx)("span",{className:"dark:text-white ml-2",children:null==n?void 0:n.name})]}),(0,s.jsx)(_.Z,{onClick:e=>{e.stopPropagation(),e.nativeEvent.stopImmediatePropagation(),r()},twoToneColor:"#CD2029",className:"!text-2xl"})]}),(0,s.jsxs)("div",{className:"text-sm mt-2  p-6 pt-2 h-40",children:[(0,s.jsxs)("p",{className:"font-semibold",children:[a("Owner"),":"]}),(0,s.jsx)("p",{className:" truncate",children:null==n?void 0:n.owner}),(0,s.jsxs)("p",{className:"font-semibold mt-2",children:[a("Description"),":"]}),(0,s.jsx)("p",{className:" line-clamp-2",children:null==n?void 0:n.desc}),(0,s.jsx)("p",{className:"font-semibold mt-2",children:"Last modify:"}),(0,s.jsx)("p",{className:" truncate",children:F()(n.gmt_modified).format("YYYY-MM-DD HH:MM:SS")})]}),(0,s.jsx)("div",{className:"flex justify-center",children:(0,s.jsx)(i.ZP,{size:"middle",onClick:x,className:"mr-4 dark:text-white mb-2",shape:"round",icon:(0,s.jsx)(j.Z,{}),children:a("Chat")})})]})})})}var X=l(31365),K=l(2453),W=l(72269),B=l(64082);let{Dragger:J}=X.default,{TextArea:Q}=D.default;function ee(e){let{handleStepChange:t,spaceName:l,docType:n}=e,{t:c}=(0,z.$G)(),[r]=A.Z.useForm(),[o,d]=(0,a.useState)(!1),m=async e=>{let s;let{synchChecked:a,docName:i,textSource:c,originFileObj:r,text:o,webPageUrl:m}=e;switch(d(!0),n){case"webPage":s=await (0,S.Vx)((0,S.H_)(l,{doc_name:i,content:m,doc_type:"URL"}));break;case"file":let x=new FormData;x.append("doc_name",i||r.file.name),x.append("doc_file",r.file),x.append("doc_type","DOCUMENT"),s=await (0,S.Vx)((0,S.iG)(l,x));break;default:s=await (0,S.Vx)((0,S.H_)(l,{doc_name:i,source:c,content:o,doc_type:"TEXT"}))}a&&(null==u||u(l,null==s?void 0:s[1])),d(!1),t({label:"finish"})},u=async(e,t)=>{await (0,S.Vx)((0,S.Hx)(e,{doc_ids:[t]}))},x=e=>{let{file:t,fileList:l}=e;r.getFieldsValue().docName||r.setFieldValue("docName",t.name),0===l.length&&r.setFieldValue("originFileObj",null)},h=()=>{let e=r.getFieldsValue().originFileObj;return!!e&&(K.ZP.warning(c("Limit_Upload_File_Count_Tips")),X.default.LIST_IGNORE)},p=()=>(0,s.jsxs)(s.Fragment,{children:[(0,s.jsx)(A.Z.Item,{label:"".concat(c("Text_Source"),":"),name:"textSource",rules:[{required:!0,message:c("Please_input_the_text_source")}],children:(0,s.jsx)(D.default,{className:"mb-5  h-12",placeholder:c("Please_input_the_text_source")})}),(0,s.jsx)(A.Z.Item,{label:"".concat(c("Text"),":"),name:"text",rules:[{required:!0,message:c("Please_input_the_description")}],children:(0,s.jsx)(Q,{rows:4})})]}),_=()=>(0,s.jsx)(s.Fragment,{children:(0,s.jsx)(A.Z.Item,{label:"".concat(c("Web_Page_URL"),":"),name:"webPageUrl",rules:[{required:!0,message:c("Please_input_the_owner")}],children:(0,s.jsx)(D.default,{className:"mb-5  h-12",placeholder:c("Please_input_the_Web_Page_URL")})})}),j=()=>(0,s.jsx)(s.Fragment,{children:(0,s.jsx)(A.Z.Item,{name:"originFileObj",rules:[{required:!0,message:c("Please_input_the_owner")}],children:(0,s.jsxs)(J,{onChange:x,beforeUpload:h,multiple:!1,accept:".pdf,.ppt,.pptx,.xls,.xlsx,.doc,.docx,.txt,.md",children:[(0,s.jsx)("p",{className:"ant-upload-drag-icon",children:(0,s.jsx)(B.Z,{})}),(0,s.jsx)("p",{style:{color:"rgb(22, 108, 255)",fontSize:"20px"},children:c("Select_or_Drop_file")}),(0,s.jsx)("p",{className:"ant-upload-hint",style:{color:"rgb(22, 108, 255)"},children:"PDF, PowerPoint, Excel, Word, Text, Markdown,"})]})})});return(0,s.jsx)(y.Z,{spinning:o,children:(0,s.jsxs)(A.Z,{form:r,size:"large",className:"mt-4",layout:"vertical",name:"basic",initialValues:{remember:!0},autoComplete:"off",onFinish:m,children:[(0,s.jsx)(A.Z.Item,{label:"".concat(c("Name"),":"),name:"docName",rules:[{required:!0,message:c("Please_input_the_name")}],children:(0,s.jsx)(D.default,{className:"mb-5 h-12",placeholder:c("Please_input_the_name")})}),(()=>{switch(n){case"webPage":return _();case"file":return j();default:return p()}})(),(0,s.jsx)(A.Z.Item,{label:"".concat(c("Synch"),":"),name:"synchChecked",initialValue:!0,children:(0,s.jsx)(W.Z,{className:"bg-slate-400",defaultChecked:!0})}),(0,s.jsxs)(A.Z.Item,{children:[(0,s.jsx)(i.ZP,{onClick:()=>{t({label:"back"})},className:"mr-4",children:"".concat(c("Back"))}),(0,s.jsx)(i.ZP,{type:"primary",htmlType:"submit",children:c("Finish")})]})]})})}function et(e){let{t}=(0,z.$G)(),{handleStepChange:l}=e,[n,c]=(0,a.useState)(!1),r=async e=>{let{spaceName:t,owner:s,description:a}=e;c(!0);let[n,i,r]=await (0,S.Vx)((0,S.be)({name:t,vector_type:"Chroma",owner:s,desc:a}));c(!1),(null==r?void 0:r.success)&&l({label:"forward",spaceName:t})};return(0,s.jsx)(y.Z,{spinning:n,children:(0,s.jsxs)(A.Z,{size:"large",className:"mt-4",layout:"vertical",name:"basic",initialValues:{remember:!0},autoComplete:"off",onFinish:r,children:[(0,s.jsx)(A.Z.Item,{label:t("Knowledge_Space_Name"),name:"spaceName",rules:[{required:!0,message:t("Please_input_the_name")},()=>({validator:(e,l)=>/[^\u4e00-\u9fa50-9a-zA-Z_-]/.test(l)?Promise.reject(Error(t("the_name_can_only_contain"))):Promise.resolve()})],children:(0,s.jsx)(D.default,{className:"mb-5 h-12",placeholder:t("Please_input_the_name")})}),(0,s.jsx)(A.Z.Item,{label:t("Owner"),name:"owner",rules:[{required:!0,message:t("Please_input_the_owner")}],children:(0,s.jsx)(D.default,{className:"mb-5  h-12",placeholder:t("Please_input_the_owner")})}),(0,s.jsx)(A.Z.Item,{label:t("Description"),name:"description",rules:[{required:!0,message:t("Please_input_the_description")}],children:(0,s.jsx)(D.default,{className:"mb-5  h-12",placeholder:t("Please_input_the_description")})}),(0,s.jsx)(A.Z.Item,{children:(0,s.jsx)(i.ZP,{type:"primary",htmlType:"submit",children:t("Next")})})]})})}function el(e){let{t}=(0,z.$G)(),{handleStepChange:l}=e,a=[{type:"text",title:t("Text"),subTitle:t("Fill your raw text"),iconType:"TEXT"},{type:"webPage",title:t("URL"),subTitle:t("Fetch_the_content_of_a_URL"),iconType:"WEBPAGE"},{type:"file",title:t("Document"),subTitle:t("Upload_a_document"),iconType:"DOCUMENT"}];return(0,s.jsx)(s.Fragment,{children:a.map((e,t)=>(0,s.jsxs)(g.Z,{className:"mt-4 mb-4 cursor-pointer",onClick:()=>{l({label:"forward",docType:e.type})},children:[(0,s.jsxs)("div",{className:"font-semibold",children:[(0,s.jsx)(G.Z,{type:e.iconType}),e.title]}),(0,s.jsx)("div",{children:e.subTitle})]},t))})}var es=()=>{let[e,t]=(0,a.useState)([]),[l,o]=(0,a.useState)(!1),[d,m]=(0,a.useState)(0),[u,x]=(0,a.useState)(""),[h,p]=(0,a.useState)(""),{t:_}=(0,z.$G)(),j=[{title:_("Knowledge_Space_Config")},{title:_("Choose_a_Datasource_type")},{title:_("Setup_the_Datasource")}];async function f(){let[e,l]=await (0,S.Vx)((0,S.Vm)());t(l)}(0,a.useEffect)(()=>{f()},[]);let b=e=>{let{label:t,spaceName:l,docType:s}=e;"finish"===t?(o(!1),f(),x(""),p("")):"forward"===t?(0===d&&f(),m(e=>e+1)):m(e=>e-1),l&&x(l),s&&p(s)};function g(e){x(e),m(1),o(!0)}return(0,s.jsxs)("div",{className:"bg-[#FAFAFA] dark:bg-[#212121] w-full h-full",children:[(0,s.jsxs)("div",{className:"page-body p-6 px-12 h-full overflow-auto",children:[(0,s.jsx)(i.ZP,{type:"primary",className:"flex items-center",icon:(0,s.jsx)(n.Z,{}),onClick:()=>{o(!0)},children:"Create"}),(0,s.jsx)("div",{className:"flex flex-wrap mt-4",children:null==e?void 0:e.map(e=>(0,s.jsx)($,{space:e,onAddDoc:g,getSpaces:f},e.id))})]}),(0,s.jsxs)(c.default,{title:"Add Knowledge",centered:!0,open:l,destroyOnClose:!0,onCancel:()=>{o(!1)},width:1e3,afterClose:()=>{m(0)},footer:null,children:[(0,s.jsx)(r.Z,{current:d,items:j}),0===d&&(0,s.jsx)(et,{handleStepChange:b}),1===d&&(0,s.jsx)(el,{handleStepChange:b}),2===d&&(0,s.jsx)(ee,{spaceName:u,docType:h,handleStepChange:b})]})]})}}},function(e){e.O(0,[885,44,479,442,365,813,411,63,774,888,179],function(){return e(e.s=54681)}),_N_E=e.O()}]);