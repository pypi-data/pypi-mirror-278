import{j as e,c as f}from"./@tanstack-CEbkxrhX.js";import{u as c,S as y,a as v,b as j}from"./SuccessStep-BHhPYxz9.js";import{A as h,P as U,a as C}from"./AwarenessChannel-DDpU6zHx.js";import{r as l}from"./@radix-C9DBgJhe.js";import{f as b,ao as w,aA as A,i as _,am as P,S as E}from"./index-BhYPVFKa.js";import"./UpdatePasswordSchemas-4FyPPBY9.js";import"./check-circle-BVvhm5dy.js";import"./url-ZKNs861m.js";import"./@react-router-DYovave8.js";import"./zod-DrZvVLjd.js";import"./index.esm-F7nqy9zY.js";import"./file-text-CbVERUON.js";import"./play-circle-DK5QMJyp.js";import"./@reactflow-CegZ5GV3.js";const S=l.createContext(null);function g({children:r,initialUser:n}){const[a,t]=l.useState(n||{});return e.jsx(S.Provider,{value:{user:a,setUser:t},children:r})}function d(){const r=l.useContext(S);if(r===null)throw new Error("useSurveyUserContext must be used within an SurveyUserProvider");return r}function F({user:r}){var u,i;const{setSurveyStep:n}=c(),{setUser:a}=d();function t({fullName:s,getUpdates:o,email:m}){a(p=>({...p,...m?{email:m}:{email:null},full_name:s,email_opted_in:o})),n(2)}return e.jsx(h,{email:(u=r.metadata)==null?void 0:u.email,fullName:(i=r.body)==null?void 0:i.full_name,submitHandler:t})}function D({user:r}){const{setSurveyStep:n}=c(),{setUser:a}=d();function t({amountProductionModels:u,primaryUse:i}){const s={models_production:u,primary_use:i};a(o=>({...o,user_metadata:{...o.user_metadata,...s}})),n(3)}return e.jsx(U,{user:r,submitHandler:t})}function H(){const{user:r}=d(),{setSurveyStep:n}=c(),{toast:a}=b(),t=f(),{mutate:u}=w({onSuccess:async()=>{await t.invalidateQueries({queryKey:A()}),n(s=>s+1)},onError:s=>{s instanceof Error&&a({status:"error",emphasis:"subtle",icon:e.jsx(_,{className:"h-5 w-5 shrink-0 fill-error-700"}),description:s.message,rounded:!0})}});function i({other:s,channels:o,otherVal:m}){const x={awareness_channels:s?[...o,m]:o};u({...r,user_metadata:{...r.user_metadata,...x}})}return e.jsx(C,{submitHandler:i})}function M(){const{data:r,isPending:n,isError:a}=P({throwOnError:!0}),{surveyStep:t}=c();return a?null:n?e.jsx(E,{className:"h-[300px]"}):e.jsx(e.Fragment,{children:e.jsxs(g,{children:[e.jsx(y,{stepAmount:3}),t===1&&e.jsx(F,{user:r}),t===2&&e.jsx(D,{user:r}),t===3&&e.jsx(H,{}),t===4&&e.jsx(v,{subHeader:"Your ZenML account is now updated",displayBody:!1,username:r.name})]})})}function G(){return e.jsx("div",{children:e.jsx(j,{children:e.jsx(M,{})})})}export{G as default};
