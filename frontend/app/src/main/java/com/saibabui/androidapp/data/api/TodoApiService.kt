package com.saibabui.androidapp.data.api

import com.saibabui.androidapp.data.model.Todo
import retrofit2.Response
import retrofit2.http.*

/**
 * Retrofit API service interface for Todo operations
 */
interface TodoApiService {
    
    @GET("todos/")
    suspend fun getTodos(): Response<List<Todo>>
    
    @GET("todos/{id}")
    suspend fun getTodo(@Path("id") id: Int): Response<Todo>
    
    @POST("todos/")
    suspend fun createTodo(@Body todo: Todo): Response<Todo>
    
    @PUT("todos/{id}")
    suspend fun updateTodo(@Path("id") id: Int, @Body todo: Todo): Response<Todo>
    
    @DELETE("todos/{id}")
    suspend fun deleteTodo(@Path("id") id: Int): Response<Map<String, String>>
    
    @GET("health")
    suspend fun healthCheck(): Response<Map<String, String>>
}
