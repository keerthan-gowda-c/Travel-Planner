export type TravelMode = "train" | "bus" | "car" | "flight" 

export interface RecommendationRequest{
    origin : string
    start_date: string
    end_date: string
    budget: number
    travel_mode: TravelMode
}

export interface RecommendedDestination{
    name: string
    state: string
    region: string
    travel_mode: TravelMode
    distance_km: number
    travel_cost: number
    stay_cost: number
    food_cost: number
    activities_cost: number
    estimated_cost: number
    remaining_budget: number
}

export interface RecommendationResponse{
    origin: string;
    recommendations: RecommendedDestination[];
}