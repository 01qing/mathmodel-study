import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {Workbook, SpreadsheetFile} from '@oai/artifact-tool';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const key=process.argv[2];
if(!['result11','result12','result21','result22'].includes(key))throw new Error('Specify result key');
const matrix=JSON.parse(await fs.readFile(path.join(root,'results',key+'_matrix.json'),'utf8'));
const wb=Workbook.create();const s=wb.worksheets.add('Sheet1');
// Values are the simulator's final states, as requested by the official template.
// Sparse block writes keep transit/outside cells genuinely empty and avoid formula dependencies.
for(let r=0;r<matrix.length;r++){
 const row=matrix[r];let c=0;
 while(c<row.length){
  while(c<row.length&&row[c]===null)c++;
  if(c===row.length)break;
  let end=c+1;while(end<row.length&&row[end]!==null)end++;
  s.getRangeByIndexes(r,c,1,end-c).values=[row.slice(c,end)];c=end;
 }
}
s.getRangeByIndexes(0,0,1,matrix[0].length).format={fill:'#E5E7EB',font:{name:'Arial',bold:true,size:10}};
s.getRangeByIndexes(1,0,matrix.length-1,1).format={fill:'#F3F4F6',font:{name:'Arial',bold:true,size:10}};
s.getRange('A1:T15').format.columnWidth=6;
s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);
wb.recalculate();
await fs.mkdir(path.join(root,'deliverables'),{recursive:true});
const xlsx=await SpreadsheetFile.exportXlsx(wb);await xlsx.save(path.join(root,'deliverables',key+'.xlsx'));
const preview=await wb.render({sheetName:'Sheet1',range:'A1:T15',scale:1.4,format:'png'});
await fs.writeFile(path.join(root,'deliverables',key+'_preview.png'),new Uint8Array(await preview.arrayBuffer()));
console.log(key,'exported',matrix.length,'rows',matrix[0].length,'columns');
