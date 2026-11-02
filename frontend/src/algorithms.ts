export type SortName = 'Bubble' | 'Selection' | 'Insertion' | 'Merge' | 'Quick';
export type Frame = { values: number[]; message: string; compare?: number[]; sorted?: number[]; line?: number };
export function traceSort(input: number[], kind: SortName): Frame[] {
  const a = [...input], frames: Frame[] = [{ values:[...a], message:'Start with the input array.' }];
  const push = (message:string, compare:number[]=[], sorted:number[]=[], line?:number) =>
    frames.push({ values:[...a], message, compare, sorted, line });
  if (kind === 'Bubble') {
    for (let i=0;i<a.length;i++) {
      let changed=false;
      for (let j=0;j<a.length-i-1;j++) {
        push(`Compare ${a[j]} and ${a[j+1]}.`,[j,j+1],Array.from({length:i},(_,k)=>a.length-1-k),3);
        if (a[j]>a[j+1]) { [a[j],a[j+1]]=[a[j+1],a[j]]; changed=true; push('They are out of order, so swap them.',[j,j+1],[],4); }
      }
      if (!changed) break;
    }
  } else if (kind === 'Selection') {
    for(let i=0;i<a.length;i++){ let m=i; for(let j=i+1;j<a.length;j++){push(`Compare ${a[j]} with minimum ${a[m]}.`,[m,j],[],3);if(a[j]<a[m])m=j;} if(m!==i){[a[i],a[m]]=[a[m],a[i]];push(`Move minimum ${a[i]} into position ${i}.`,[i,m],[],4);} }
  } else if (kind === 'Insertion') {
    for(let i=1;i<a.length;i++){const key=a[i];let j=i-1;while(j>=0&&a[j]>key){a[j+1]=a[j];push(`Shift ${a[j]} one position right.`,[j,j+1],[],4);j--;}a[j+1]=key;push(`Insert ${key} into its sorted position.`,[j+1],[],5);}
  } else if (kind === 'Merge') {
    const rec=(lo:number,hi:number):void=>{if(hi-lo<=1)return;const mid=Math.floor((lo+hi)/2);rec(lo,mid);rec(mid,hi);const merged=a.slice(lo,mid).concat(a.slice(mid,hi)).sort((x,y)=>x-y);for(let k=0;k<merged.length;k++)a[lo+k]=merged[k];push(`Merge the range from index ${lo} to ${hi-1}.`,Array.from({length:hi-lo},(_,k)=>lo+k),[],5);}; rec(0,a.length);
  } else {
    const rec=(lo:number,hi:number):void=>{if(lo>=hi)return;const pivot=a[hi];let i=lo;for(let j=lo;j<hi;j++){push(`Compare ${a[j]} with pivot ${pivot}.`,[j,hi],[],4);if(a[j]<=pivot){[a[i],a[j]]=[a[j],a[i]];i++;}}[a[i],a[hi]]=[a[hi],a[i]];push(`Place pivot ${pivot} at index ${i}.`,[i],[],6);rec(lo,i-1);rec(i+1,hi);};rec(0,a.length-1);
  }
  frames.push({values:[...a],message:'Sorted! Every value is in ascending order.',sorted:a.map((_,i)=>i)});
  return frames;
}
export function traceBinarySearch(input:number[], target:number) {
  const values=[...input].sort((a,b)=>a-b), frames:{values:number[];left:number;mid:number;right:number;message:string;found?:boolean}[]=[];
  let left=0,right=values.length-1,found=false;
  while(left<=right){const mid=Math.floor((left+right)/2);frames.push({values:[...values],left,mid,right,message:`Compare ${target} with ${values[mid]}.`});if(values[mid]===target){found=true;frames.push({values:[...values],left,mid,right,message:`Found ${target} at index ${mid}.`,found:true});break;}if(values[mid]<target)left=mid+1;else right=mid-1;}
  if(!found)frames.push({values:[...values],left,mid:-1,right,message:`${target} is not in the array.`,found:false});
  return frames;
}
export function uniqueSorted(values:number[]) { return values.filter((v,i)=>i===0||v!==values[i-1]); }
