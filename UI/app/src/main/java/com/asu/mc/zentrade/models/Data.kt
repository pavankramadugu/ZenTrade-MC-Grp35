package com.asu.mc.zentrade.models

data class RecommendationsRequest(
    val frequency: String,
    val appetite: String,
    val countries: List<String>
)

data class RecommendationsResponse(
    val recommendations: List<String>
)