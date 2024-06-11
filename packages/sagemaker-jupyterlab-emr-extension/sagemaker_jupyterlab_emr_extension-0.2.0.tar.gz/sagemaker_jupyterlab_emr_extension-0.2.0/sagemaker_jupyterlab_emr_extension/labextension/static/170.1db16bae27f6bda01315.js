"use strict";(self.webpackChunk_amzn_sagemaker_jupyterlab_emr_extension=self.webpackChunk_amzn_sagemaker_jupyterlab_emr_extension||[]).push([[170],{9170:(e,t,n)=>{n.r(t),n.d(t,{default:()=>Tt});var r=n(6611),a=n(6029),s=n.n(a),o=n(4405),l=n(1837);const i="SelectedCell",c="HoveredCellClassname",d="SelectAuthContainer";var u;!function(e){e.emrConnect="sagemaker-studio:emr-connect"}(u||(u={}));const p={widgetTitle:"Connect to cluster",connectCommand:{label:"Connect",caption:"Connect to a cluster"},connectMessage:{errorTitle:"Error connecting to EMR cluster",successTitle:"Successfully connected to EMR cluster",errorDefaultMessage:"Error connecting to EMR cluster",successDefaultMessage:"Connected to EMR Cluster"},widgetConnected:"The notebook is connected to",defaultTooltip:"Select a cluster to connect to",widgetHeader:"Select a cluster to connect to. A code block will be added to the active cell and run automatically to establish the connection.",connectedWidgetHeader:"cluster. You can submit new jobs to run on the cluster.",connectButton:"Connect",learnMore:"Learn more",noResultsMatchingFilters:"There are no clusters matching the filter.",radioButtonLabels:{basicAccess:"Http basic authentication",noCredential:"No credential"},listClusterError:"Fail to list clusters, refresh the modal or try again later",noCluster:"No clusters are available",permissionError:"The IAM role SageMakerStudioClassicExecutionRole does not have permissions needed to list EMR clusters. Update the role with appropriate permissions and try again. Refer to the",selectCluster:"Select a cluster",selectAuthTitle:"Select credential type for ",clusterButtonLabel:"Cluster",expandCluster:{MasterNodes:"Master nodes",CoreNodes:"Core nodes",NotAvailable:"Not available",NoTags:"No tags",SparkHistoryServer:"Spark History Server",TezUI:"Tez UI",Overview:"Overview",Apps:"Apps",ApplicationUserInterface:"Application user Interface",Tags:"Tags"},presignedURL:{link:"Link",error:"Error: ",retry:"Retry",sparkUIError:"Spark UI Link is not available or time out. Please try ",sshTunnelLink:"SSH tunnel",or:" or ",viewTheGuide:"view the guide",clusterNotReady:"Cluster is not ready. Please try again later.",clusterNotConnected:"No active cluster connection. Please connect to a cluster and try again.",clusterNotCompatible:"EMR version 5.33+ or 6.3.0+ required for direct Spark UI links. Try a compatible cluster, use "}},m="Cancel",h=({handleClick:e,tooltip:t})=>s().createElement("div",{className:"EmrClusterContainer"},s().createElement(o.ToolbarButtonComponent,{className:"EmrClusterButton",tooltip:t,label:p.clusterButtonLabel,onClick:e,enabled:!0}));var g;!function(e){e.tab="Tab",e.enter="Enter",e.escape="Escape",e.arrowDown="ArrowDown"}(g||(g={}));var v=n(8278),E=n(9868),b=n(8564);const C={ModalBase:l.css`
  &.jp-Dialog {
    z-index: 1; /* Override default z-index so Dropdown menu is above the Modal */
  }
  .jp-Dialog-body {
    padding: var(--jp-padding-xl);
    .no-cluster-msg {
      padding: var(--jp-cell-collapser-min-height);
      margin: auto;
    }
  }
`,Header:l.css`
  width: 100%;
  display: contents;
  font-size: 0.5rem;
  h1 {
    margin: 0;
  }
`,HeaderButtons:l.css`
  display: flex;
  float: right;
`,ModalFooter:l.css`
  display: flex;
  justify-content: flex-end;
  background-color: var(--jp-layout-color2);
  padding: 12px 24px 12px 24px;
  button {
    margin: 5px;
  }
`,Footer:l.css`
  .jp-Dialog-footer {
    background-color: var(--jp-layout-color2);
    margin: 0;
  }
`,DismissButton:l.css`
  padding: 0;
  border: none;
  cursor: pointer;
`,DialogClassname:l.css`
  .jp-Dialog-content {
    width: 900px;
    max-width: none;
    max-height: none;
    padding: 0;
  }
  .jp-Dialog-header {
    padding: 24px 24px 12px 24px;
    background-color: var(--jp-layout-color2);
  }
  /* Hide jp footer so we can add custom footer with button controls. */
  .jp-Dialog-footer {
    display: none;
  }
`},f=({heading:e,headingId:t="modalHeading",className:n,shouldDisplayCloseButton:r=!1,onClickCloseButton:a,actionButtons:o})=>{let i=null,c=null;return r&&(i=s().createElement(v.z,{className:(0,l.cx)(C.DismissButton,"dismiss-button"),role:"button","aria-label":"close",onClick:a,"data-testid":"close-button"},s().createElement(E.closeIcon.react,{tag:"span"}))),o&&(c=o.map((e=>{const{className:t,component:n,onClick:r,label:a}=e;return n?s().createElement("div",{key:`${(0,b.v4)()}`},n):s().createElement(v.z,{className:t,type:"button",role:"button",onClick:r,"aria-label":a,key:`${(0,b.v4)()}`},a)}))),s().createElement("header",{className:(0,l.cx)(C.Header,n)},s().createElement("h1",{id:t},e),s().createElement("div",{className:(0,l.cx)(C.HeaderButtons,"header-btns")},c,i))};var x=n(1105);const w=({onCloseModal:e,onConnect:t,disabled:n})=>s().createElement("footer",{"data-analytics-type":"eventContext","data-analytics":"JupyterLab",className:C.ModalFooter},s().createElement(v.z,{"data-analytics-type":"eventDetail","data-analytics":"EMR-Modal-Footer-CancelButton",className:"jp-Dialog-button jp-mod-reject jp-mod-styled listcluster-cancel-btn",type:"button",onClick:e},m),s().createElement(v.z,{"data-analytics-type":"eventDetail","data-analytics":"EMR-Modal-Footer-ConnectButton",className:"jp-Dialog-button jp-mod-accept jp-mod-styled listcluster-connect-btn",type:"button",onClick:t,disabled:n},p.connectButton));class y{constructor(e="",t="",n="",r="",a="",s="",o=""){this.partition=e,this.service=t,this.region=n,this.accountId=r,this.resourceInfo=a,this.resourceType=s,this.resourceName=o}static getResourceInfo(e){const t=e.match(y.SPLIT_RESOURCE_INFO_REG_EXP);let n="",r="";return t&&(1===t.length?r=t[1]:(n=t[1],r=t[2])),{resourceType:n,resourceName:r}}static fromArnString(e){const t=e.match(y.ARN_REG_EXP);if(!t)throw new Error(`Invalid ARN format: ${e}`);const[,n,r,a,s,o]=t,{resourceType:l="",resourceName:i=""}=o?y.getResourceInfo(o):{};return new y(n,r,a,s,o,l,i)}static isValid(e){return!!e.match(y.ARN_REG_EXP)}static getArn(e,t,n,r,a,s){return`arn:${e}:${t}:${n}:${r}:${a}/${s}`}}y.ARN_REG_EXP=/^arn:(.*?):(.*?):(.*?):(.*?):(.*)$/,y.SPLIT_RESOURCE_INFO_REG_EXP=/^(.*?)[/:](.*)$/,y.VERSION_DELIMITER="/";const k=({cellData:e})=>{var t,n,r;const a=null===(t=e.status)||void 0===t?void 0:t.state;return"RUNNING"===(null===(n=e.status)||void 0===n?void 0:n.state)||"WAITING"===(null===(r=e.status)||void 0===r?void 0:r.state)?s().createElement("div",null,s().createElement("svg",{width:"10",height:"10"},s().createElement("circle",{cx:"5",cy:"5",r:"5",fill:"green"})),s().createElement("label",{htmlFor:"myInput"},"Running/Waiting")):s().createElement("div",null,s().createElement("label",{htmlFor:"myInput"},a))},I={name:"Name",id:"ID",status:"Status",creationTime:"Creation Time",createdOn:"Created On",accountId:"Account ID"};var T=n(2510),R=n(4321);l.css`
  height: 100%;
  position: relative;
`;const N=l.css`
  margin-right: 10px;
`,S=(l.css`
  ${N}
  svg {
    width: 6px;
  }
`,l.css`
  background-color: var(--jp-layout-color2);
  label: ${c};
  cursor: pointer;
`),M=l.css`
  background-color: var(--jp-layout-color3);
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Opera and Firefox */
  label: ${i};
`,A=l.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  padding: var(--jp-cell-padding);
  width: 100%;
  align-items: baseline;
  justify-content: start;
  /* box shadow */
  -moz-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  -webkit-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  /* Disable visuals for scroll */
  overflow-x: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  &::-webkit-scrollbar {
    display: none;
  }
`,U={borderTop:"var(--jp-border-width) solid var(--jp-border-color1)",borderBottom:"var(--jp-border-width) solid var(--jp-border-color1)",borderRight:"var(--jp-border-width) solid var(--jp-border-color1)",display:"flex",boxSizing:"border-box",marginRight:"0px",padding:"2.5px",fontWeight:"initial",textTransform:"capitalize",color:"var(--jp-ui-font-color2)"},j={display:"flex",flexDirection:"column",height:"max-content"},L=l.css`
  display: flex;
`,D={height:"max-content",display:"flex",overflow:"auto",padding:"var(--jp-cell-padding)"},P=({isSelected:e})=>e?s().createElement(E.caretDownIcon.react,{tag:"span"}):s().createElement(E.caretRightIcon.react,{tag:"span"}),_=({dataList:e,tableConfig:t,selectedId:n,expandedView:r,noResultsView:o,showIcon:i,isLoading:c,columnConfig:d,onRowSelect:u,...p})=>{const m=(0,a.useRef)(null),h=(0,a.useRef)(null),[g,v]=(0,a.useState)(-1),[E,b]=(0,a.useState)(0);(0,a.useEffect)((()=>{var e,t;b((null===(e=null==h?void 0:h.current)||void 0===e?void 0:e.clientHeight)||28),null===(t=m.current)||void 0===t||t.recomputeRowHeights()}),[n,c,t.width,t.height]);const C=({rowData:e,...t})=>e?(0,T.defaultTableCellDataGetter)({rowData:e,...t}):null;return s().createElement(T.Table,{...p,...t,headerStyle:U,ref:m,headerHeight:28,overscanRowCount:10,rowCount:e.length,rowData:e,noRowsRenderer:()=>o,rowHeight:({index:t})=>e[t].id&&e[t].id===n?E:28,rowRenderer:e=>{const{style:t,key:a,rowData:o,index:i,className:c}=e,d=n===o.id,u=g===i,p=(0,l.cx)(L,c,{[M]:d,[S]:!d&&u});return d?s().createElement("div",{key:a,ref:h,style:{...t,...j},onMouseEnter:()=>v(i),onMouseLeave:()=>v(-1),className:p},(0,R.Cx)({...e,style:{width:t.width,...D}}),s().createElement("div",{className:A},r)):s().createElement("div",{key:a,onMouseEnter:()=>v(i),onMouseLeave:()=>v(-1)},(0,R.Cx)({...e,className:p}))},onRowClick:({rowData:e})=>u(e),rowGetter:({index:t})=>e[t]},d.map((({dataKey:t,label:r,disableSort:a,cellRenderer:o})=>s().createElement(T.Column,{key:t,dataKey:t,label:r,flexGrow:1,width:150,disableSort:a,cellDataGetter:C,cellRenderer:t=>((t,r)=>{const{rowIndex:a,columnIndex:o}=t,l=e[a].id===n,c=0===o;let d=null;return r&&(d=r({row:e[a],rowIndex:a,columnIndex:o,onCellSizeChange:()=>null})),c&&i?s().createElement(s().Fragment,null,s().createElement(P,{isSelected:l})," ",d):d})(t,o)}))))},$=l.css`
  height: 100%;
  position: relative;
`,O=l.css`
  margin-right: 10px;
`,F=(l.css`
  ${O}
  svg {
    width: 6px;
  }
`,l.css`
  text-align: center;
  margin: 0;
  position: absolute;
  top: 50%;
  left: 50%;
  margin-right: -50%;
  transform: translate(-50%, -50%);
`),B=(l.css`
  background-color: var(--jp-layout-color2);
  label: ${c};
  cursor: pointer;
`,l.css`
  background-color: var(--jp-layout-color3);
  -webkit-touch-callout: none; /* iOS Safari */
  -webkit-user-select: none; /* Safari */
  -khtml-user-select: none; /* Konqueror HTML */
  -moz-user-select: none; /* Old versions of Firefox */
  -ms-user-select: none; /* Internet Explorer/Edge */
  user-select: none; /* Non-prefixed version, currently supported by Chrome, Opera and Firefox */
  label: ${i};
`,l.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  padding: var(--jp-cell-padding);
  width: 100%;
  align-items: baseline;
  justify-content: start;

  /* box shadow */
  -moz-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  -webkit-box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);
  box-shadow: inset 0 -15px 15px -15px var(--jp-layout-color3);

  /* Disable visuals for scroll */
  overflow-x: scroll;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
  &::-webkit-scrollbar {
    display: none;
  }
`,l.css`
  padding: 24px 24px 12px 24px;
`),z=l.css`
  .ReactVirtualized__Table__headerRow {
    display: flex;
  }
  .ReactVirtualized__Table__row {
    display: flex;
    font-size: 12px;
    align-items: center;
  }
`,H=l.css`
  width: 100%;
  display: flex;
  flex-direction: row;
`,G=l.css`
  flex-direction: column;
  margin: 0 32px 8px 8px;
  flex: 1 0 auto;
  width: 33%;
`,V=l.css`
  width: 20%;
`,W=l.css`
  margin-bottom: var(--jp-code-padding);
`,J=p.expandCluster,K=({clusterData:e})=>{const t=null==e?void 0:e.tags;return(null==t?void 0:t.length)?s().createElement(s().Fragment,null,t.map((e=>s().createElement("div",{className:W,key:null==e?void 0:e.key},null==e?void 0:e.key,": ",null==e?void 0:e.value)))):s().createElement("div",null,J.NoTags)},q=p.expandCluster;var X=n(9208),Y=n(759);const Z="/aws/sagemaker/api/emr/describe-cluster",Q=[200,201];var ee;!function(e){e.POST="POST",e.GET="GET",e.PUT="PUT"}(ee||(ee={}));const te=async(e,t,n)=>{const r=X.ServerConnection.makeSettings(),a=Y.URLExt.join(r.baseUrl,e);try{const e=await X.ServerConnection.makeRequest(a,{method:t,body:n},r);if(!Q.includes(e.status))throw a.includes("list-clusters")&&400===e.status?new Error("permission error"):new Error("Unable to fetch data");return e.json()}catch(e){return e}},ne=async e=>{if(void 0===e)throw new Error("Error describing persistent app UI: Invalid persistent app UI ID");const t={PersistentAppUIId:e},n=JSON.stringify(t);return await te("/aws/sagemaker/api/emr/describe-persistent-app-ui",ee.POST,n)},re=async e=>await new Promise((t=>setTimeout(t,e))),ae=async e=>{const t={ClusterId:e},n=JSON.stringify(t);return await te(Z,ee.POST,n)};var se,oe,le,ie,ce;!function(e){e.Bootstrapping="BOOTSTRAPPING",e.Running="RUNNING",e.Starting="STARTING",e.Terminated="TERMINATED",e.TerminatedWithErrors="TERMINATED_WITH_ERRORS",e.Terminating="TERMINATING",e.Undefined="UNDEFINED",e.Waiting="WAITING"}(se||(se={})),function(e){e.AllStepsCompleted="All_Steps_Completed",e.BootstrapFailure="Bootstrap_Failure",e.InstanceFailure="Instance_Failure",e.InstanceFleetTimeout="Instance_Fleet_Timeout",e.InternalError="Internal_Error",e.StepFailure="Step_Failure",e.UserRequest="User_Request",e.ValidationError="Validation_Error"}(oe||(oe={})),function(e){e[e.SHS=0]="SHS",e[e.TEZUI=1]="TEZUI",e[e.YTS=2]="YTS"}(le||(le={})),function(e){e.Success="Success",e.Fail="Fail"}(ie||(ie={})),function(e){e[e.Content=0]="Content",e[e.External=1]="External",e[e.Notebook=2]="Notebook"}(ce||(ce={}));const de="smsjp--icon-link-external",ue={link:l.css`
  a& {
    color: var(--jp-content-link-color);
    line-height: var(--jp-custom-ui-text-line-height);
    text-decoration: none;
    text-underline-offset: 1.5px;

    span.${de} {
      display: inline;
      svg {
        width: var(--jp-ui-font-size1);
        height: var(--jp-ui-font-size1);
        margin-left: var(--jp-ui-font-size1;
        transform: scale(calc(var(--jp-custom-ui-text-line-height) / 24));
      }
      path {
        fill: var(--jp-ui-font-color1);
      }
    }

    &.sm--content-link {
      text-decoration: underline;
    }

    &:hover:not([disabled]) {
      text-decoration: underline;
    }

    &:focus:not([disabled]),
    &:active:not([disabled]) {
      color: var(--jp-brand-color2);
      .${de} path {
        fill: var(--jp-ui-font-color1);
      }
    }

    &:focus:not([disabled]) {
      border: var(--jp-border-width) solid var(--jp-brand-color2);
    }

    &:active:not([disabled]) {
      text-decoration: underline;
    }

    &[disabled] {
      color: var(--jp-ui-font-color3);
      .${de} path {
        fill: var(--jp-ui-font-color1);
      }
    }
  }
`,externalIconClass:de};var pe;!function(e){e[e.Content=0]="Content",e[e.External=1]="External",e[e.Notebook=2]="Notebook"}(pe||(pe={}));const me=({children:e,className:t,disabled:n=!1,href:r,onClick:a,type:o=pe.Content,hideExternalIcon:i=!1,...c})=>{const d=o===pe.External,u={className:(0,l.cx)(ue.link,t,{"sm-emr-content":o===pe.Content}),href:r,onClick:n?void 0:a,target:d?"_blank":void 0,rel:d?"noopener noreferrer":void 0,...c},p=d&&!i?s().createElement("span",{className:ue.externalIconClass},s().createElement(E.launcherIcon.react,{tag:"span"})):null;return s().createElement("a",{role:"link",...u},e,p)},he=l.css`
  h2 {
    font-size: var(--jp-ui-font-size1);
    margin-top: 0;
  }
`,ge=l.css`
  .DataGrid-ContextMenu > div {
    overflow: hidden;
  }
  margin: 12px;
`,ve=l.css`
  padding-bottom: var(--jp-add-tag-extra-width);
`,Ee=l.css`
  background-color: var(--jp-layout-color2);
  display: flex;
  justify-content: flex-end;
  button {
    margin: 5px;
  }
`,be=l.css`
  text-align: center;
  vertical-align: middle;
`,Ce={ModalBase:he,ModalBody:ge,ModalFooter:Ee,ListTable:l.css`
  overflow: hidden;
`,NoHorizontalPadding:l.css`
  padding-left: 0;
  padding-right: 0;
`,RadioGroup:l.css`
  display: flex;
  justify-content: flex-start;
  li {
    margin-right: 20px;
  }
`,ModalHeader:ve,ModalMessage:be,AuthModal:l.css`
  min-height: none;
`,ListClusterModal:l.css`
  /* so the modal height remains the same visually during and after loading (this number can be changed) */
  min-height: 600px;
`,ConnectCluster:l.css`
  white-space: nowrap;
`,ClusterDescription:l.css`
  display: inline;
`,PresignedURL:l.css`
  line-height: normal;
`,ClusterListModalCrossAccountError:l.css`
  display: flex;
  flex-direction: column;
  padding: 0 0 10px 0;
`,GridWrapper:l.css`
  box-sizing: border-box;
  width: 100%;
  height: 100%;

  & .ReactVirtualized__Grid {
    /* important is required because react virtualized puts overflow style inline */
    overflow-x: hidden !important;
  }

  & .ReactVirtualized__Table__headerRow {
    display: flex;
  }

  & .ReactVirtualized__Table__row {
    display: flex;
    font-size: 12px;
    align-items: center;
  }
`,EmrExecutionRoleContainer:l.css`
  margin-top: 25px;
  width: 90%;
`,Dropdown:l.css`
  margin-top: var(--jp-cell-padding);
`,PresignedURLErrorText:l.css`
  color: var(--jp-error-color1);
`},fe="Invalid Cluster State",xe="Missing Cluster ID, are you connected to a cluster?",we="Unsupported cluster version",ye=({clusterId:e,accountId:t,applicationId:n,persistentAppUIType:r,label:o,onError:i})=>{const[c,d]=(0,a.useState)(!1),[u,m]=(0,a.useState)(!1),h=(0,a.useCallback)((e=>{m(!0),i(e)}),[i]),g=(0,a.useCallback)((e=>{if(!e)throw new Error("Error opening Spark UI: Invalid URL");null!==window.open(e,"_blank","noopener,noreferrer")&&(m(!1),i(null))}),[i]),v=(0,a.useCallback)(((e,t,n)=>{(async(e,t)=>{const n={ClusterId:e,OnClusterAppUIType:"ApplicationMaster",ApplicationId:t},r=JSON.stringify(n);return await te("/aws/sagemaker/api/emr/get-on-cluster-app-ui-presigned-url",ee.POST,r)})(e,n).then((e=>g(null==e?void 0:e.presignedURL))).catch((e=>h(e))).finally((()=>d(!1)))}),[h,g]),E=(0,a.useCallback)(((e,t,n,r)=>{(async e=>{if(void 0===e)throw new Error("Error describing persistent app UI: Invalid persistent app UI ID");const t={TargetResourceArn:e},n=JSON.stringify(t);return await te("/aws/sagemaker/api/emr/create-persistent-app-ui",ee.POST,n)})(e.clusterArn).then((e=>(async(e,t,n)=>{var r;const a=Date.now();let s,o=0;for(;o<=3e4;){const t=await ne(e),n=null===(r=null==t?void 0:t.persistentAppUI)||void 0===r?void 0:r.persistentAppUIStatus;if(n&&"ATTACHED"===n){s=t;break}await re(2e3),o=Date.now()-a}if(null==s)throw new Error("Error waiting for persistent app UI ready: Max attempts reached");return s})(null==e?void 0:e.persistentAppUIId))).then((e=>(async(e,t,n)=>{if(void 0===e)throw new Error("Error getting persistent app UI presigned URL: Invalid persistent app UI ID");const r={PersistentAppUIId:e,PersistentAppUIType:t},a=JSON.stringify(r);return await te("/aws/sagemaker/api/emr/get-persistent-app-ui-presigned-url",ee.POST,a)})(null==e?void 0:e.persistentAppUI.persistentAppUIId,r))).then((e=>g(null==e?void 0:e.presignedURL))).catch((e=>h(e))).finally((()=>d(!1)))}),[h,g]),b=(0,a.useCallback)(((e,t,n,r)=>async()=>{if(d(!0),!t)return d(!1),void h(xe);const a=await ae(t).catch((e=>h(e)));if(!a||!(null==a?void 0:a.cluster))return void d(!1);const s=null==a?void 0:a.cluster;if(s.releaseLabel)try{const e=s.releaseLabel.substr(4).split("."),t=+e[0],n=+e[1];if(t<5)return d(!1),void h(we);if(5===t&&n<33)return d(!1),void h(we);if(6===t&&n<3)return d(!1),void h(we)}catch(e){}switch(s.status.state){case se.Running:case se.Waiting:n?v(t,e,n):E(s,e,n,r);break;case se.Terminated:E(s,e,n,r);break;default:d(!1),h(fe)}}),[v,E,h]);return s().createElement(s().Fragment,null,c?s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})):s().createElement(me,{"data-analytics-type":"eventDetail","data-analytics":"EMR-Modal-PresignedUrl-Click",className:(0,l.cx)("PresignedURL",Ce.PresignedURL),onClick:b(t,e,n,r)},u?s().createElement("span",null,o&&o," ",s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText),onClick:b(t,e,n,r)},"(",p.presignedURL.retry,")")):o||p.presignedURL.link))},ke=l.css`
  cursor: pointer;
  & {
    color: var(--jp-content-link-color);
    text-decoration: none;
    text-underline-offset: 1.5px;
    text-decoration: underline;

    &:hover:not([disabled]) {
      text-decoration: underline;
    }

    &:focus:not([disabled]) {
      border: var(--jp-border-width) solid var(--jp-brand-color2);
    }

    &:active:not([disabled]) {
      text-decoration: underline;
    }

    &[disabled] {
      color: var(--jp-ui-font-color3);
    }
  }
`,Ie=l.css`
  display: flex;
`,Te=(l.css`
  margin-left: 10px;
`,l.css`
  margin-bottom: var(--jp-code-padding);
`),Re=p.expandCluster,Ne=({clusterId:e,accountId:t,setIsError:n})=>{const[r]=(0,a.useState)(!1);return s().createElement("div",{className:Ie},s().createElement("div",{className:(0,l.cx)("HistoryLink",ke)},s().createElement(ye,{clusterId:e,onError:e=>e,accountId:t,persistentAppUIType:"SHS",label:Re.SparkHistoryServer})),s().createElement(E.launcherIcon.react,{tag:"span"}),r&&s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})))},Se=p.expandCluster,Me=({clusterId:e,accountId:t,setIsError:n})=>{const[r]=s().useState(!1);return s().createElement("div",{className:Ie},s().createElement("div",{className:ke},s().createElement(ye,{clusterId:e,onError:e=>e,accountId:t,persistentAppUIType:"TEZ",label:Se.TezUI})),s().createElement(E.launcherIcon.react,{tag:"span"}),r&&s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})))},Ae=p.expandCluster,Ue=e=>{const{accountId:t,selectedClusterId:n}=e,[r,o]=(0,a.useState)(!1);return r?s().createElement("div",null,Ae.NotAvailable):s().createElement(s().Fragment,null,s().createElement("div",{className:Te},s().createElement(Ne,{clusterId:n,accountId:t,setIsError:o})),s().createElement("div",{className:Te},s().createElement(Me,{clusterId:n,accountId:t,setIsError:o})))},je=p.expandCluster,Le=({clusterArn:e,accountId:t,selectedClusterId:n,clusterData:r})=>{const o=r,[i,c]=(0,a.useState)();return(0,a.useEffect)((()=>{(async e=>{const t=JSON.stringify({ClusterId:e}),n=await te("/aws/sagemaker/api/emr/list-instance-groups",ee.POST,t);c(n)})(n)}),[n]),s().createElement("div",{"data-analytics-type":"eventContext","data-analytics":"JupyterLab",className:H},s().createElement("div",{className:G},s().createElement("h4",null,je.Overview),s().createElement("div",{className:W},(e=>{var t;const n=null===(t=null==e?void 0:e.instanceGroups)||void 0===t?void 0:t.find((e=>"MASTER"===(null==e?void 0:e.instanceGroupType)));if(n){const e=n.runningInstanceCount,t=n.instanceType;return`${q.MasterNodes}: ${e}, ${t}`}return`${q.MasterNodes}: ${q.NotAvailable}`})(i)),s().createElement("div",{className:W},(e=>{var t;const n=null===(t=null==e?void 0:e.instanceGroups)||void 0===t?void 0:t.find((e=>"CORE"===(null==e?void 0:e.instanceGroupType)));if(n){const e=n.runningInstanceCount,t=n.instanceType;return`${q.CoreNodes}: ${e}, ${t}`}return`${q.CoreNodes}: ${q.NotAvailable}`})(i)),s().createElement("div",{className:W},je.Apps,": ",(e=>{const t=null==e?void 0:e.applications;return(null==t?void 0:t.length)?t.map(((e,n)=>{const r=n===t.length-1?".":", ";return`${null==e?void 0:e.name} ${null==e?void 0:e.version}${r}`})):`${q.NotAvailable}`})(o))),s().createElement("div",{className:(0,l.cx)(G,V)},s().createElement("h4",null,je.ApplicationUserInterface),s().createElement(Ue,{selectedClusterId:n,accountId:t,clusterArn:e})),s().createElement("div",{className:G},s().createElement("h4",null,je.Tags),s().createElement(K,{clusterData:r})))},De=p,Pe=s().createElement("div",{className:$},s().createElement("p",{className:F},De.noResultsMatchingFilters)),_e=({clustersList:e,tableConfig:t,clusterManagementListConfig:n,selectedClusterId:r,clusterArn:a,accountId:o,onRowSelect:l,clusterDetails:i,...c})=>{const d=!i&&!1,u=i;return s().createElement(_,{...c,tableConfig:t,showIcon:!0,dataList:e,selectedId:r,columnConfig:n,isLoading:d,noResultsView:Pe,onRowSelect:l,expandedView:d?s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})):s().createElement(Le,{selectedClusterId:r,accountId:o||"",clusterArn:a,clusterData:u,instanceGroupData:void 0})})};n(7960);const $e=e=>Array.isArray(e)&&e.length>0,Oe=({onCloseModal:e,selectedCluster:t,notebookPanel:n,app:r,eventDetail:o})=>{const i=`${d}`,c=`${d}`,u=Je,[m,h]=(0,a.useState)("Basic_Access"),g=(0,a.useMemo)((()=>u(e,t,r,o,m,void 0,n)),[u,e,t,m,n,r,o]);return s().createElement("div",{className:(0,l.cx)(i,Ce.ModalBase,Ce.AuthModal),"data-analytics-type":"eventContext","data-analytics":"JupyterLab"},s().createElement("div",{className:(0,l.cx)(c,Ce.ModalBody)},s().createElement(x.FormControl,null,s().createElement(x.RadioGroup,{"aria-labelledby":"demo-radio-buttons-group-label",defaultValue:"Basic_Access",value:m,onChange:e=>{"Basic_Access"!==e.target.value&&"None"!==e.target.value||h(e.target.value)},name:"radio-buttons-group","data-testid":"radio-button-group",row:!0},s().createElement(x.FormControlLabel,{"data-analytics-type":"eventDetail","data-analytics":"EMR-Modal-SelectAuth-BasicAccess-Click",value:"Basic_Access",control:s().createElement(x.Radio,null),label:p.radioButtonLabels.basicAccess}),s().createElement(x.FormControlLabel,{"data-analytics-type":"eventDetail","data-analytics":"EMR-Modal-SelectAuth-None-Click",value:"None",control:s().createElement(x.Radio,null),label:p.radioButtonLabels.noCredential})))),s().createElement(w,{onCloseModal:e,onConnect:g,disabled:!1}))};class Fe{constructor(e,t,n,r,a){this.disposeDialog=e,this.selectedCluster=t,this.app=n,this.eventDetail=r,this.notebookPanel=a}render(){return s().createElement(Oe,{onCloseModal:this.disposeDialog,selectedCluster:this.selectedCluster,app:this.app,eventDetail:this.eventDetail,notebookPanel:this.notebookPanel})}}const Be=(e,t,n,r,a)=>new Fe(e,t,n,r,a),ze=(e,t,n)=>{t.execute(e,n)},He=e=>t=>n=>{ze(e,t,n)},Ge=Object.fromEntries(Object.entries(u).map((e=>{const t=e[0],n=e[1];return[t,(r=n,{id:r,createRegistryWrapper:He(r),execute:(e,t)=>ze(r,e,t)})];var r}))),Ve=e=>{var t,n;return(null===(t=e.kerberosAttributes)||void 0===t?void 0:t.kdcAdminPassword)?"Kerberos":(null===(n=e.configurations)||void 0===n?void 0:n.some((e=>{var t;return"ldap"===(null===(t=null==e?void 0:e.properties)||void 0===t?void 0:t.livyServerAuthType)})))?"Basic_Access":null},We=async(e,t,n)=>{let r={};const a=()=>r&&r.resolve();r=new o.Dialog({title:s().createElement(f,{heading:`${p.selectAuthTitle}"${e.name}"`,shouldDisplayCloseButton:!0,onClickCloseButton:a}),body:Be(a,e,t,n,void 0).render()}),r.addClass((0,l.cx)(C.ModalBase,C.Footer,C.DialogClassname)),r.launch()},Je=(e,t,n,r,a,s,o)=>()=>{if(!t||!n)return;const s=a||Ve(t);s?(e(),n.commands.execute(Ge.emrConnect.id,{clusterId:t.id,authType:s,language:"python"})):(e(),We(t,n,r)),window&&window.panorama&&window.panorama("trackCustomEvent",{eventType:"eventDetail",eventDetail:r,eventContext:"JupyterLab",timestamp:Date.now()})},Ke={width:850,height:500},qe=e=>{const{onCloseModal:t,header:n,app:r,eventDetail:o}=e,i=Je,[c,d]=(0,a.useState)([]),[u,m]=(0,a.useState)(!1),[h,g]=(0,a.useState)(""),[v,E]=(0,a.useState)(void 0),[b,C]=(0,a.useState)(),[,f]=(0,a.useState)(""),[T,R]=(0,a.useState)(!0),N=[{dataKey:"name",label:I.name,disableSort:!0,cellRenderer:({row:e})=>{var t,n;return((null===(t=e.name)||void 0===t?void 0:t.length)||0)>20?(null===(n=null==e?void 0:e.name)||void 0===n?void 0:n.slice(0,19))+"...":null==e?void 0:e.name}},{dataKey:"id",label:I.id,disableSort:!0,cellRenderer:({row:e})=>null==e?void 0:e.id},{dataKey:"status",label:I.status,disableSort:!0,cellRenderer:({row:e})=>s().createElement(k,{cellData:e})},{dataKey:"creationDateTime",label:I.creationTime,disableSort:!0,cellRenderer:({row:e})=>{var t;return null===(t=null==e?void 0:e.status)||void 0===t?void 0:t.timeline.creationDateTime.split("+")[0].split(".")[0]}},{dataKey:"clusterArn",label:I.accountId,disableSort:!0,cellRenderer:({row:e})=>{if(null==e?void 0:e.clusterArn)return y.fromArnString(e.clusterArn).accountId}}],S=async(e="")=>{try{m(!0);const t=JSON.stringify({ClusterStates:["RUNNING","WAITING"],...e&&{Marker:e}}),n=await te("/aws/sagemaker/api/emr/list-clusters",ee.POST,t);n&&n.clusters&&(d((e=>[...e,...n.clusters])),n&&n.Marker?S(n.Marker):m(!1)),$e(n)||(m(!1),g(n.message))}catch(e){m(!1),g(e.message)}};(0,a.useEffect)((()=>{S()}),[]),(0,a.useEffect)((()=>{b&&E((async e=>{const t=JSON.stringify({ClusterId:e}),n=await te(Z,ee.POST,t);E(n.cluster)})(b))}),[b]);const M=(0,a.useMemo)((()=>null==c?void 0:c.sort(((e,t)=>{const n=e.name,r=t.name;return null==n?void 0:n.localeCompare(r)}))),[c]),A=(0,a.useCallback)((e=>{const t=M.find((t=>t.id===e));let n="";const r=null==t?void 0:t.clusterArn;return r&&y.isValid(r)&&(n=y.fromArnString(r).accountId),n}),[M]),U=(0,a.useCallback)((e=>{const t=M.find((t=>t.id===e)),n=null==t?void 0:t.clusterArn;return n&&y.isValid(n)?n:""}),[M]),j=(0,a.useCallback)((e=>{const t=null==e?void 0:e.id;t&&t===b?(C(t),f(""),R(!0)):(C(t),f(A(t)),R(!1),window&&window.panorama&&window.panorama("trackCustomEvent",{eventType:"eventDetail",eventDetail:"EMR-Modal-ClusterRow",eventContext:"JupyterLab",timestamp:Date.now()}))}),[b,A]);return s().createElement(s().Fragment,null,h&&s().createElement("span",{className:"no-cluster-msg"},(e=>{const t=s().createElement("a",{href:"https://docs.aws.amazon.com/sagemaker/latest/dg/studio-notebooks-configure-discoverability-emr-cluster.html"},"documentation");return e.includes("permission error")?s().createElement("span",{className:"error-msg"},p.permissionError," ",t):s().createElement("span",{className:"error-msg"},e)})(h)),u?s().createElement("span",null,s().createElement(x.CircularProgress,{size:"1rem"})):$e(c)?s().createElement("div",{className:(0,l.cx)(B,"modal-body-container")},n,s().createElement(s().Fragment,null,s().createElement("div",{className:(0,l.cx)(z,"grid-wrapper")},s().createElement(_e,{clustersList:M,selectedClusterId:null!=b?b:"",clusterArn:U(null!=b?b:""),accountId:A(null!=b?b:""),tableConfig:Ke,clusterManagementListConfig:N,onRowSelect:j,clusterDetails:v})))):s().createElement("div",{className:"no-cluster-msg"},p.noCluster),s().createElement(w,{onCloseModal:t,onConnect:()=>{i(t,v,r,o,void 0,void 0,void 0)()},disabled:T}))};class Xe{constructor(e,t,n,r){this.disposeDialog=e,this.header=t,this.app=n,this.eventDetail=r}render(){return s().createElement(a.Suspense,{fallback:null},s().createElement(qe,{onCloseModal:this.disposeDialog,header:this.header,app:this.app,eventDetail:this.eventDetail,"data-testid":"list-cluster-view"}))}}const Ye=(e,t,n,r)=>new Xe(e,t,n,r);var Ze;!function(e){e["us-east-1"]="us-east-1",e["us-east-2"]="us-east-2",e["us-west-1"]="us-west-1",e["us-west-2"]="us-west-2",e["us-gov-west-1"]="us-gov-west-1",e["us-gov-east-1"]="us-gov-east-1",e["us-iso-east-1"]="us-iso-east-1",e["us-isob-east-1"]="us-isob-east-1",e["ca-central-1"]="ca-central-1",e["eu-west-1"]="eu-west-1",e["eu-west-2"]="eu-west-2",e["eu-west-3"]="eu-west-3",e["eu-central-1"]="eu-central-1",e["eu-north-1"]="eu-north-1",e["eu-south-1"]="eu-south-1",e["ap-east-1"]="ap-east-1",e["ap-south-1"]="ap-south-1",e["ap-southeast-1"]="ap-southeast-1",e["ap-southeast-2"]="ap-southeast-2",e["ap-southeast-3"]="ap-southeast-3",e["ap-northeast-3"]="ap-northeast-3",e["ap-northeast-1"]="ap-northeast-1",e["ap-northeast-2"]="ap-northeast-2",e["sa-east-1"]="sa-east-1",e["af-south-1"]="af-south-1",e["cn-north-1"]="cn-north-1",e["cn-northwest-1"]="cn-northwest-1",e["me-south-1"]="me-south-1"}(Ze||(Ze={}));const Qe=e=>(e=>e===Ze["cn-north-1"]||e===Ze["cn-northwest-1"])(e)?"https://docs.amazonaws.cn":"https://docs.aws.amazon.com",et=({clusterName:e})=>{const t=Qe(Ze["us-west-2"]);return s().createElement("div",{className:(0,l.cx)(Ce.ModalHeader,"list-cluster-modal-header")},(()=>{let t;if(e){const n=s().createElement("span",{className:Ce.ConnectCluster},e),r=`${p.widgetConnected} `,a=` ${p.connectedWidgetHeader} `;t=s().createElement("div",{className:(0,l.cx)(Ce.ClusterDescription,"list-cluster-description")},r,n,a)}else t=`${p.widgetHeader} `;return t})(),s().createElement(me,{href:`${t}/sagemaker/latest/dg/studio-notebooks-emr-cluster.html`,type:pe.External},p.learnMore))};class tt extends o.ReactWidget{constructor(e,t){super(),this.updateConnectedCluster=e=>{this._connectedCluster=e,this.update()},this.getToolTip=()=>this._connectedCluster?`${p.widgetConnected} ${this._connectedCluster.name} cluster`:p.defaultTooltip,this.clickHandler=async()=>{let e={};const t=()=>e&&e.resolve();e=new o.Dialog({title:s().createElement(f,{heading:p.widgetTitle,shouldDisplayCloseButton:!0,onClickCloseButton:t,className:"list-cluster-modal-header"}),body:Ye(t,this.listClusterHeader(),this._appContext,"EMR-Command-Connect").render()}),e.handleEvent=t=>{"keydown"===t.type&&(({keyboardEvent:e,onEscape:t,onShiftTab:n,onShiftEnter:r,onTab:a,onEnter:s})=>{const{key:o,shiftKey:l}=e;l?o===g.tab&&n?n():o===g.enter&&r&&r():o===g.tab&&a?a():o===g.enter&&s?s():o===g.escape&&t&&t()})({keyboardEvent:t,onEscape:()=>e.reject()})},e.addClass((0,l.cx)(C.ModalBase,C.Footer,C.DialogClassname)),e.launch()},this.listClusterHeader=()=>{var e;return s().createElement(et,{clusterName:null===(e=this._connectedCluster)||void 0===e?void 0:e.name})},this._selectedCluster=null,this._appContext=t,this._connectedCluster=null,this._kernelId=null}get kernelId(){return this._kernelId}get selectedCluster(){return this._selectedCluster}updateKernel(e){this._kernelId!==e&&(this._kernelId=e,this.kernelId&&this.update())}render(){return s().createElement(h,{handleClick:this.clickHandler,tooltip:this.getToolTip()})}}const nt=e=>null!=e;var rt=n(7704),at=n.n(rt);const st=e=>{const t=p.presignedURL.sshTunnelLink;return e?s().createElement(me,{href:e,type:pe.External,hideExternalIcon:!0},t):s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},t)},ot=()=>s().createElement(me,{href:"https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-ssh-tunnel.html",type:pe.External},p.presignedURL.viewTheGuide),lt=({sshTunnelLink:e,error:t})=>s().createElement(s().Fragment,null,(()=>{switch(t){case fe:return s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.clusterNotReady);case xe:return s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.clusterNotConnected);case we:return(e=>s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.clusterNotCompatible,st(e),p.presignedURL.or,ot()))(e);default:return(e=>s().createElement("span",null,s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},s().createElement("b",null,p.presignedURL.error),p.presignedURL.sparkUIError),st(e),s().createElement("span",{className:(0,l.cx)("PresignedURLErrorText",Ce.PresignedURLErrorText)},p.presignedURL.or),ot()))(e)}})()),it=(e,t)=>{var n;for(let r=0;r<e.childNodes.length;r++)if(null===(n=e.childNodes[r].textContent)||void 0===n?void 0:n.includes(t))return r;return-1},ct=e=>{try{let t=e.lastElementChild;for(;t;)e.removeChild(t),t=e.lastElementChild}catch(e){}},dt="YARN Application ID",ut="Spark UI",pt="--cluster-id",mt="--assumable-role-arn",ht="%info",gt="%configure",vt={childList:!0,subtree:!0};class Et{constructor(e){this.trackedPanels=new Set,this.trackedCells=new Set,this.notebookTracker=e,this.triggers=[bt,ht,gt],this.kernelChanged=!1,this.lastConnectedClusterId=null,this.lastConnectedAccountId=void 0}run(){this.notebookTracker.currentChanged.connect(((e,t)=>{t&&(this.isTrackedPanel(t)||(t.context.sessionContext.kernelChanged.connect(((e,t)=>{this.kernelChanged=!0})),t.context.sessionContext.iopubMessage.connect(((e,n)=>{!this.isTrackedPanel(t)||this.kernelChanged?(n?(this.trackPanel(t),this.handleExistingSparkWidgetsOnPanelLoad(t)):this.stopTrackingPanel(t),this.kernelChanged=!1):this.isTrackedPanel(t)&&this.checkMessageForEmrConnectAndInject(n,t)}))))}))}isTrackedCell(e){return this.trackedCells.has(e)}trackCell(e){this.trackedCells.add(e)}stopTrackingCell(e){this.trackedCells.delete(e)}isTrackedPanel(e){return this.trackedPanels.has(e)}trackPanel(e){this.trackedPanels.add(e)}stopTrackingPanel(e){this.trackedPanels.delete(e)}handleExistingSparkWidgetsOnPanelLoad(e){e.revealed.then((()=>{const t=new RegExp(this.triggers.join("|"));((e,t)=>{var n;const r=null===(n=null==e?void 0:e.content)||void 0===n?void 0:n.widgets;return null==r?void 0:r.filter((e=>{const n=e.model.sharedModel;return t.test(n.source)}))})(e,t).forEach((e=>{if(this.containsSparkMagicTable(e.outputArea.node)){const t=e.model.sharedModel,n=this.getClusterId(t.source),r=this.getAccountId(t.source);this.injectPresignedURL(e,n,r)}else this.injectPresignedURLOnTableRender(e)}))}))}checkMessageForEmrConnectAndInject(e,t){if("execute_input"!==e.header.msg_type)return;const n=e.content.code;var r;this.codeContainsTrigger(n)&&(r=n,t.content.widgets.filter((e=>e.model.sharedModel.source.includes(r)))).forEach((e=>{this.injectPresignedURLOnTableRender(e)}))}codeContainsTrigger(e){const t=this.triggers.filter((t=>e.includes(t)));return $e(t)}getParameterFromEmrConnectCommand(e,t){const n=e.split(" "),r=n.indexOf(t);if(!(-1===r||r+1>n.length-1))return n[r+1]}getClusterId(e){return e&&e.includes(pt)?this.getParameterFromEmrConnectCommand(e,pt)||null:this.lastConnectedClusterId}getAccountId(e){if(!e)return this.lastConnectedAccountId;if(e.includes(ht))return this.lastConnectedAccountId;if(e.includes(mt)){const t=this.getParameterFromEmrConnectCommand(e,mt);return void 0!==t?y.fromArnString(t).accountId:void 0}}getSparkMagicTableBodyNodes(e){const t=Array.from(e.getElementsByTagName("tbody"));return $e(t)?t.filter((e=>this.containsSparkMagicTable(e))):[]}containsSparkMagicTable(e){var t;return(null===(t=e.textContent)||void 0===t?void 0:t.includes(dt))&&e.textContent.includes(ut)}isSparkUIErrorRow(e){var t;return e instanceof HTMLTableRowElement&&(null===(t=e.textContent)||void 0===t?void 0:t.includes(p.presignedURL.error))||!1}injectSparkUIErrorIntoNextTableRow(e,t,n,r){var a;const o=this.isSparkUIErrorRow(t.nextSibling);if(null===r)return void(o&&(null===(a=t.nextSibling)||void 0===a||a.remove()));let l;if(o?(l=t.nextSibling,ct(l)):l=((e,t)=>{let n=1,r=!1;for(let a=1;a<e.childNodes.length;a++)if(e.childNodes[a].isSameNode(t)){n=a,r=!0;break}if(!r)return null;const a=n+1<e.childNodes.length?n+1:-1;return e.insertRow(a)})(e,t),!l)return;const i=l.insertCell(),c=t.childElementCount;i.setAttribute("colspan",c.toString()),i.style.textAlign="left",i.style.background="#212121";const d=s().createElement(lt,{sshTunnelLink:n,error:r});at().render(d,i)}injectPresignedURL(e,t,n){var r;const a=e.outputArea.node,o=e.model.sharedModel,l=this.getSparkMagicTableBodyNodes(a);if(!$e(l))return!1;if(o.source.includes(gt)&&l.length<2)return!1;for(let e=0;e<l.length;e++){const a=l[e],o=a.firstChild,i=it(o,ut),c=it(o,"Driver log"),d=it(o,dt),u=o.getElementsByTagName("th")[c];if(o.removeChild(u),-1===i||-1===d)break;for(let e=1;e<a.childNodes.length;e++){const o=a.childNodes[e],l=o.childNodes[i];o.childNodes[c].remove();const u=null===(r=l.getElementsByTagName("a")[0])||void 0===r?void 0:r.href;l.hasChildNodes()&&ct(l);const p=o.childNodes[d].textContent||void 0,m=document.createElement("div");l.appendChild(m);const h=s().createElement(ye,{clusterId:t,applicationId:p,onError:e=>this.injectSparkUIErrorIntoNextTableRow(a,o,u,e),accountId:n});at().render(h,m)}}return!0}injectPresignedURLOnTableRender(e){this.isTrackedCell(e)||(this.trackCell(e),new MutationObserver(((t,n)=>{for(const r of t)if("childList"===r.type)try{const t=e.model.sharedModel,r=this.getClusterId(t.source),a=this.getAccountId(t.source);if(this.injectPresignedURL(e,r,a)){this.stopTrackingCell(e),n.disconnect(),this.lastConnectedClusterId=r,this.lastConnectedAccountId=a;break}}catch(t){this.stopTrackingCell(e),n.disconnect()}})).observe(e.outputArea.node,vt))}}const bt="%sm_analytics emr connect",Ct=p,ft={id:"@sagemaker-studio:EmrCluster",autoStart:!0,optional:[r.INotebookTracker],activate:async(e,t)=>{null==t||new Et(t).run(),e.docRegistry.addWidgetExtension("Notebook",new xt(e)),e.commands.addCommand(Ge.emrConnect.id,{label:e=>Ct.connectCommand.label,isEnabled:()=>!0,isVisible:()=>!0,caption:()=>Ct.connectCommand.caption,execute:async t=>{try{const{clusterId:n,authType:a,language:s,crossAccountArn:o,executionRoleArn:l,notebookPanelToInjectCommandInto:i}=t,c="%load_ext sagemaker_studio_analytics_extension.magics",d=nt(s)?`--language ${s}`:"",u=nt(o)?`--assumable-role-arn ${o}`:"",p=nt(l)?`--emr-execution-role-arn ${l}`:"",m=`${c}\n${bt} --verify-certificate False --cluster-id ${n} --auth-type ${a} ${d} ${u} ${p}`,h=i||(e=>{const t=e.shell.widgets("main");let n=t.next().value;for(;n;){if(n.hasClass("jp-NotebookPanel")&&n.isVisible)return n;n=t.next().value}return null})(e);await(async(e,t,n=!0)=>new Promise((async(a,s)=>{if(t){const o=t.content,l=o.model,i=t.context.sessionContext,{metadata:c}=l.sharedModel.toJSON(),d={cell_type:"code",metadata:c,source:e},u=o.activeCell,p=u?o.activeCellIndex:0;if(l.sharedModel.insertCell(p,d),o.activeCellIndex=p,n)try{await r.NotebookActions.run(o,i)}catch(e){s(e)}const m=[];for(const e of u.outputArea.node.children)m.push(e.innerHTML);a({html:m,cell:u})}s("No notebook panel")})))(m,h)}catch(e){throw e.message,e}}})}};class xt{constructor(e){this.appContext=e}createNew(e,t){const n=(r=e.sessionContext,a=this.appContext,new tt(r,a));var r,a;return e.context.sessionContext.kernelChanged.connect((e=>{var t;const r=null===(t=e.session)||void 0===t?void 0:t.kernel;e.iopubMessage.connect(((e,t)=>{((e,t,n,r)=>{if(n)try{if(e.content.text){const{isConnSuccess:t,clusterId:a}=(e=>{let t,n=!1;if(e.content.text){const r=JSON.parse(e.content.text);if("sagemaker-analytics"!==r.namespace)return{};t=r.cluster_id,n=r.success}return{isConnSuccess:n,clusterId:t}})(e);t&&n.id===a&&r(n)}}catch(e){return}})(t,0,n.selectedCluster,n.updateConnectedCluster)})),r&&r.spec.then((e=>{e&&e.metadata&&n.updateKernel(r.id)})),n.updateKernel(null)})),e.toolbar.insertBefore("kernelName","emrCluster",n),n}}var wt=n(3891);const yt={errorTitle:"Unable to connect to EMR cluster",defaultErrorMessage:"Something went wrong when connecting to the EMR cluster.",invalidRequestErrorMessage:"A request to attach the EMR cluster to the notebook is invalid.",invalidClusterErrorMessage:"EMR cluster ID is invalid."};let kt=!1;const It=async e=>(0,o.showErrorMessage)(yt.errorTitle,{message:e}),Tt=[ft,{id:"@sagemaker-studio:DeepLinking",requires:[wt.IRouter],autoStart:!0,activate:async(e,t)=>{const{commands:n}=e,r="emrCluster:open-notebook-for-deeplinking";n.addCommand(r,{execute:()=>(async(e,t)=>{if(!kt)try{const{search:n}=e.current;if(!n)return void await It(yt.invalidRequestErrorMessage);t.restored.then((async()=>{const{clusterId:e}=Y.URLExt.queryStringToObject(n);if(!e)return void await It(yt.invalidRequestErrorMessage);const r=await ae(e);if(!r||!(null==r?void 0:r.cluster))return void await It(yt.invalidClusterErrorMessage);const a=await t.commands.execute("notebook:create-new");await new Promise((e=>{a.sessionContext.kernelChanged.connect(((t,n)=>{e(n)}))}));const s={name:r.cluster.name,id:r.cluster.id,status:{state:r.cluster.status},configurations:r.cluster.configurations,kerberosAttributes:r.cluster.kerberosAttributes},o=Ve(s);o?(await new Promise((e=>setTimeout(e,2e3))),await t.commands.execute(Ge.emrConnect.id,{clusterId:s.id,authType:o,language:"python"})):await We(s,t,"EMR-Attach-To-New-Notebook")}))}catch(e){return void await It(yt.defaultErrorMessage)}finally{kt=!0}})(t,e)}),t.register({command:r,pattern:new RegExp("[?]command=attach-emr-to-notebook"),rank:10})}}]}}]);