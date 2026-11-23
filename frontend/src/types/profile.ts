export type SubscriptionPlan = "free" | "premium";

export type SubscriptionStatus = | "free" | "created" | "authenticated" | "active" | "pending" | "halted" | "cancelled" | "expired" | "failed" 

export interface UserSubscription {
    plan: SubscriptionPlan
    status: SubscriptionStatus
    billing_period: "weekly" | "monthly" | null;
}

export interface UserProfile {
    id:string
    username:string
    email:string
    full_name:string
    subscription: UserSubscription
}