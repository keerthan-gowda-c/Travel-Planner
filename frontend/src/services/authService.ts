import type { LoginRequest, LoginResponse, RegisterRequest, RegisterResponse, UserProfile } from "../types/auth";
import api from "./api";

export const registerUser = async (data:RegisterRequest):Promise<RegisterResponse> => {
    const response = await api.post<RegisterResponse>("users/register/",data)
    return response.data
}

export const loginUser = async (data:LoginRequest):Promise<LoginResponse> => {
    const response = await api.post<LoginResponse>("token/", data)
    return response.data
}

export const getUserProfile = async(): Promise<UserProfile> => {
    const response = await api.get<UserProfile>("users/profile/")
    return response.data
}