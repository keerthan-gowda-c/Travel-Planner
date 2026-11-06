export interface RegisterRequest{
    full_name: string
    username: string
    email: string
    password: string
}

export interface RegisterResponse{
    id: string
    username: string
    full_name: string
    email: string
}

export interface LoginRequest{
    email: string
    password: string
}

export interface LoginResponse{
    access:string
    refresh: string
}

export type SubscriptionPlan = "free" | "premium";

export type SubscriptionStatus = | "free" | "created" | "authenticated" | "active" | "pending" | "halted" | "cancelled" | "expired" | "failed" 

export interface UserSubscription {
    plan: SubscriptionPlan
    status: SubscriptionStatus
    billing_period: "weekly" | "monthly" | "";
}

export interface UserProfile {
    id:string
    username:string
    email:string
    full_name:string
    subscription: UserSubscription
}

export interface AuthResponse{
    message?: string
    access: string
    refresh: string
    user :{
        id: string  
        username: string
        email: string
        full_name: string

    }
}