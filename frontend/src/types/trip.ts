export interface Trip {
    id: string;
    title: string;
    origin: string;
    destination: string;
    start_date: string;
    end_date: string;
    budget: number | string;
    image_url: string | null;
    status: "scheduled" | "active" | "completed" | "cancelled";
    requires_payment: boolean;
    created_at: string;
}

export interface TripCreateData {
    title: string;
    origin: string;
    destination: string;
    start_date: string;
    end_date: string;
    budget: number;
    image_url?: string | null;
}

export interface TripStop {
    id: string;
    name: string;
    arrival_date: string;
    order: number;
    notes: string;
}

export interface CreateTripStopData {
    name: string;
    arrival_date: string;
    notes: string;
}