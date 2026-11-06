export interface Trip {
    id: string;
    title: string;
    origin: string;
    destination: string;
    start_date: string;
    end_date: string;
    budget: number;
    image_url: string | null;
    status: "scheduled" | "active" | "completed" | "cancelled";
    requires_payment: boolean;
    created_at: string;
}

export interface TripCreateData {
    title: string;
    origin: string;
    start_date: string;
    end_date: string;
    budget: number;
    image_url?: string | null;
}