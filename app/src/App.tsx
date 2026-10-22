import {useEffect} from "react";
import {Route,Routes,useLocation,useNavigate} from "react-router-dom";
import Brand from "./components/Brand";
import HomePage from "./pages/HomePage";
import SearchResultsPage from "./pages/SearchResultsPage";
import PassengerPage from "./pages/PassengerPage";
import SeatSelectionPage from "./pages/SeatSelectionPage";
import TermsPage from "./pages/TermsPage";
import ReservationReviewPage from "./pages/ReservationReviewPage";
import {paths} from "./routes";
import {useSessionState} from "./hooks/useSessionState";
import type {Itinerary,Passenger,SearchCriteria} from "./types";
import "./styles/index.css";
export default function App(){
 const navigate=useNavigate(),location=useLocation();
 const [criteria,setCriteria]=useSessionState<SearchCriteria|null>("tt-criteria",null);
 const [item,setItem]=useSessionState<Itinerary|null>("tt-itinerary",null);
 const [passengers,setPassengers]=useSessionState<Passenger[]>("tt-passengers",[]);
 const [seats,setSeats]=useSessionState<string[]>("tt-seats",[]);
 useEffect(()=>{if(location.pathname!==paths.home&&!criteria&&location.pathname!==paths.review){navigate(paths.home,{replace:true});}},[location.pathname,criteria,navigate]);
 function startSearch(c:SearchCriteria){setCriteria(c);setItem(null);setPassengers([]);setSeats([]);navigate(paths.results);}
 function selectItinerary(i:Itinerary){setItem(i);setPassengers([]);setSeats([]);navigate(paths.passenger);}
 function edit(step:string){if(step==="home"){setItem(null);setPassengers([]);setSeats([]);navigate(paths.home);}else if(step==="passenger")navigate(paths.passenger);else if(step==="seats")navigate(paths.seats);else if(step==="terms")navigate(paths.terms);}
 return <div className="app-shell"><header className="site-header"><div className="header-inner"><Brand/><div className="header-right"><span className="demo-badge"><i></i> DEMO MODE</span><span className="header-divider"></span><span className="header-caption">Travel, thoughtfully.</span></div></div></header><main><Routes><Route path={paths.home} element={<HomePage onSearch={startSearch}/>}/><Route path={paths.results} element={<SearchResultsPage criteria={criteria} onBack={()=>navigate(paths.home)} onSelect={selectItinerary}/>}/><Route path={paths.passenger} element={<PassengerPage item={item} criteria={criteria} passengers={passengers} onBack={()=>navigate(paths.results)} onContinue={p=>{setPassengers(p);navigate(paths.seats);}}/>}/><Route path={paths.seats} element={<SeatSelectionPage item={item} criteria={criteria} selected={seats} onBack={()=>navigate(paths.passenger)} onContinue={s=>{setSeats(s);navigate(paths.terms);}}/>}/><Route path={paths.terms} element={<TermsPage onBack={()=>navigate(paths.seats)} onContinue={()=>navigate(paths.review)}/>}/><Route path={paths.review} element={<ReservationReviewPage item={item} criteria={criteria} passengers={passengers} seats={seats} onBack={()=>navigate(paths.terms)} onEdit={edit}/>}/><Route path="*" element={<HomePage onSearch={startSearch}/>}/></Routes></main><footer className="site-footer"><div><Brand/><p>Made for the journey, built for learning.</p></div><div className="footer-right"><span>Fictional itineraries · No real reservations</span><small>© 2026 V-Fly Academic Project</small></div></footer></div>
}
