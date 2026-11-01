export function validFilter(f){return typeof f==='string'&&f.length>0&&f.length<=200&&!f.includes('\0')&&f.split('/').every((x,i,a)=>(!x.includes('#')||(x==='#'&&i===a.length-1))&&(!x.includes('+')||x==='+'));}
export function matches(f,t){if(!validFilter(f))return false;if(t.startsWith('$')&&!f.startsWith('$'))return false;const a=f.split('/'),b=t.split('/');for(let i=0;i<a.length;i++){if(a[i]==='#')return true;if(i>=b.length||(a[i]!=='+'&&a[i]!==b[i]))return false;}return a.length===b.length;}
export function validateMetrics(m){return m&&['cpu','ram','disk'].every(k=>typeof m[k]==='number'&&Number.isFinite(m[k])&&m[k]>=0&&m[k]<=100);}
export function roomPrefix(r){if(!/^[A-Za-z0-9_-]{6,40}$/.test(r))throw Error('Mã phòng cần 6–40 chữ, số, dấu _ hoặc -.');return `pcmon/v1/${r}`;}
export function csvCell(x){let s=String(x??'');if(/^[=+@-]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';}
