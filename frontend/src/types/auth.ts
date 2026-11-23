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