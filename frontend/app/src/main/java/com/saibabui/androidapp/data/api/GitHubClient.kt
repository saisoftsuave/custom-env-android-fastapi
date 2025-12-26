package com.saibabui.androidapp.data.api

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object GitHubClient {
    private const val GITHUB_API_URL = "https://api.github.com/"

    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(GITHUB_API_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    val api: GitHubApiService by lazy {
        retrofit.create(GitHubApiService::class.java)
    }
}
