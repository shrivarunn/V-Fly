import {ArrowRight,Clock,MapPin} from "lucide-react";
import type {Itinerary} from "../types";
import {money} from "../lib/format";
export default function ItineraryCard({item,onSelect}:{item:Itinerary;onSelect:(item:Itinerary)=>void}){
 const sold=item.availableSeats===0;
 return <article className="itinerary-card" data-testid="itinerary-card" data-itinerary-id={item.id} id={`itinerary-${item.id}`}>
  <div className="operator"><span className="operator-icon"><MapPin size={18}/></span><div><strong>{item.operator}</strong><small>{item.id}</small></div><span className={`availability ${sold?"sold":""}`} data-testid="itinerary-availability">{sold?"Sold out":`${item.availableSeats} seats left`}</span></div>
  <div className="journey"><div><strong data-testid="itinerary-departure-time">{item.departure}</strong><small>{item.origin}</small></div><div className="journey-line"><span>{item.duration}</span><div></div><ArrowRight size={16}/></div><div><strong>{item.arrival}</strong><small>{item.destination}</small></div><div className="fare"><small>From</small><strong data-testid="itinerary-fare" data-fare={item.fare}>{money(item.fare)}</strong><button className="button primary small" data-testid="select-itinerary-button" disabled={sold} onClick={()=>onSelect(item)} aria-label={`Select ${item.id}`}>{sold?"Unavailable":"Select"}</button></div></div>
 </article>
}
