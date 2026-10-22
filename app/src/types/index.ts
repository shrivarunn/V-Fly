export type Itinerary = {id:string; origin:string; destination:string; operator:string; departure:string; arrival:string; duration:string; fare:number; availableSeats:number};
export type Passenger = {firstName:string; surname:string; email:string; phone:string};
export type SearchCriteria = {origin:string; destination:string; date:string; passengers:number};
