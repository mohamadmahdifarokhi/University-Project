function div(a,b){return Math.floor(a/b)}
function jalCal(jy){const breaks=[-61,9,38,199,426,686,756,818,1111,1181,1210,1635,2060,2097,2192,2262,2324,2394,2456,3178];const bl=breaks.length;const gy=jy+621;let leapJ=-14;let jp=breaks[0];let jm=0,jump=0,leap=0,n=0,i=1;for(;i<bl;i+=1){jm=breaks[i];jump=jm-jp;if(jy<jm)break;leapJ+=div(jump,33)*8+div(jump%33,4);jp=jm}n=jy-jp;leapJ+=div(n,33)*8+div((n%33)+3,4);if(jump%33===4&&jump-n===4)leapJ+=1;const leapG=div(gy,4)-div((div(gy,100)+1)*3,4)-150;const march=20+leapJ-leapG;if(jump-n<6)n=n-jump+div(jump+4,33)*33;leap=(((n+1)%33)-1)%4;if(leap===-1)leap=4;return{leap,gy,march}}
const r=jalCal(1405)
const out = ['jalCal(1405)='+JSON.stringify(r)]
import('fs').then(fs=>fs.writeFileSync('/home/mti/Desktop/University-Project/jt.out', out.join('\n')))
