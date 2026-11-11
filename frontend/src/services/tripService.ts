import api from "./api"

export interface DashboardTrip{
    id:string
    title:string
    origin:string
    destination:string
    image_url:string|null
    start_date:string
    end_date:string
    budget:string
    status:"scheduled" | "active" | "completed" | "cancelled"
    requires_payment:boolean
    created_at:string
}

interface PaginatedTripResponse{
    results:DashboardTrip[]
}

export const getDashboardTrips = async (): Promise<DashboardTrip[]> =>{
    const response = await api.get<DashboardTrip[] | PaginatedTripResponse>("trips/dashboard/")

    if(Array.isArray(response.data)){
        return response.data
    }

    return response.data.results
}