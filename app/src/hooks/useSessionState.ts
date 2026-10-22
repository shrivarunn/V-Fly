import {useEffect, useState} from "react";
export function useSessionState<T>(key:string, initial:T):[T,(value:T)=>void] {
 const [value,setValue] = useState<T>(()=>{try {const raw=sessionStorage.getItem(key); return raw ? JSON.parse(raw) as T : initial;} catch{return initial;}});
 useEffect(()=>{sessionStorage.setItem(key,JSON.stringify(value));},[key,value]);
 return [value,setValue];
}
