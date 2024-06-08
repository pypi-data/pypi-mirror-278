import{j as s}from"./@tanstack-CEbkxrhX.js";const a={uppercase:"Password must contain at least one uppercase letter",lowercase:"Password must contain at least one lowercase letter",number:"Password must contain at least one number",special:"Password must contain at least one special character",length:"Password must be at least 8 characters"};function l({errors:c,val:t}){const e=n(c||{});function r(o){return t?e.includes(o)?"text-theme-text-error":"text-theme-text-success":"text-theme-text-secondary"}return s.jsxs("div",{className:"space-y-1 rounded-md border border-theme-border-moderate bg-theme-surface-secondary px-5 py-3 text-text-xs text-theme-text-secondary",children:[s.jsx("p",{className:"text-text-sm text-theme-text-primary",children:"Password criteria"}),s.jsxs("div",{children:[s.jsx("p",{className:r(a.length),children:"Minimum 8 characters"}),s.jsx("p",{className:r(a.number),children:"Must Contain one Numeric value"}),s.jsx("p",{className:r(a.uppercase),children:"Must include upper cases"}),s.jsx("p",{className:r(a.lowercase),children:"Must include lower cases"}),s.jsx("p",{className:r(a.special),children:"Must include one special character (!,@,#...)"})]})]})}function n(c){const t=[];return Object.values(c).forEach(e=>{typeof e=="string"?t.push(e):Array.isArray(e)?t.push(...e):typeof e=="object"&&e!==null&&t.push(...n(e))}),t}export{l as P};
