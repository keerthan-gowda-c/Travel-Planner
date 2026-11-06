import type { RecommendationRequest, RecommendationResponse } from "../types/recommendation";
import api from "./api";

export const getDestinationRecommendations = async(data: RecommendationRequest): Promise<RecommendationResponse> => {
    const response = await api.post<RecommendationResponse>("trips/recommend/", data)

    return response.data
}