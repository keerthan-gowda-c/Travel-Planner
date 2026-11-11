import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.API_BASE_URL,
    headers: { "Content-Type": "application/json" }
})

const refreshApi = axios.create({
    baseURL:import.meta.env.API_BASE_URL,
    headers:{"Content-Type": "applicaion/json"}
})

api.interceptors.request.use((config) => {
    const accessToken = localStorage.getItem("access_token");

    if (accessToken) {
        config.headers.Authorization = `Bearer ${accessToken}`
    }
    return config;
},
    (error) => Promise.reject(error)
)

api.interceptors.request.use((response)=>response, async(error) => {
    const originalRequest = error.config

    if(error.response?.status === 401 && originalRequest && !originalRequest._retry && !originalRequest.url?.includes("/token/refresh/")){
        originalRequest._retry = true
        const refreshToken = localStorage.getItem("refresh_token")

        if(!refreshToken){
            localStorage.removeItem("access_token")
            localStorage.removeItem("refresh_token")

            window.location.href = "/login"
            return Promise.reject(error)
        }

        try{
            const response = await refreshApi.post("token/refresh/",{refresh:refreshToken})
            const newAccessToken = response.data.access_token

            localStorage.setItem("access_token", newAccessToken)

            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`

            return api(originalRequest)
        } 
        catch (refreshError){
            localStorage.removeItem("access_token")
            localStorage.removeItem("refresh_token")

            window.location.href = "/login"
            return Promise.reject(refreshError)
        }
    }
    return Promise.reject(error)
})

export default api;