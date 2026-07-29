const fs=require('fs')
try {
function div(a,b){return Math.floor(a/b)}
function g2d(gy,gm,gd){let d=div((gy+div(gm-8,6)+100100)*1461,4)+div(153*((gm+9)%12)+2,5)+gd-34840408;d=d-div(div(gy+100100+div(gm-8,6),100)*3,4)+752;return d}
function d2g(jdn){let j=4*jdn+139361631;j=j+div(div(4*jdn+183187720,146097)*3,4)*4-3908;const i=div(j%1461,4)*5+308;const gd=div(i%153,5)+1;const gm=(div(i,153)%12)+1;const gy=div(j,1461)-100100+div(8-gm,6);return{gy,gm,gd}}
const a=g2d(2025,3,21)
fs.writeFileSync(__dirname+'/dbg.out','g2d='+a+' d2g='+JSON.stringify(d2g(a)))
} catch(e){ fs.writeFileSync(__dirname+'/dbg.out','ERR:'+e.message) }
