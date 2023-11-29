package com.asu.mc.zentrade.helper

import com.asu.mc.zentrade.models.RecommendationsRequest
import com.asu.mc.zentrade.models.RecommendationsResponse
import retrofit2.Call
import retrofit2.http.Body
import retrofit2.http.POST

interface RecommendationsApiService {
    @POST("recommendations")
    fun getRecommendations(@Body request: RecommendationsRequest): Call<RecommendationsResponse>
}
