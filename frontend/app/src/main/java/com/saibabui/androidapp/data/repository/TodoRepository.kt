package com.saibabui.androidapp.data.repository

import com.saibabui.androidapp.data.api.RetrofitClient
import com.saibabui.androidapp.data.model.Todo
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * Repository for Todo data operations
 */
class TodoRepository {
    
    private val apiService = RetrofitClient.todoApiService
    
    suspend fun getTodos(): Result<List<Todo>> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getTodos()
            if (response.isSuccessful) {
                Result.success(response.body() ?: emptyList())
            } else {
                Result.failure(Exception("Failed to fetch todos: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun getTodo(id: Int): Result<Todo> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.getTodo(id)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to fetch todo: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun createTodo(todo: Todo): Result<Todo> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.createTodo(todo)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to create todo: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun updateTodo(id: Int, todo: Todo): Result<Todo> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.updateTodo(id, todo)
            if (response.isSuccessful && response.body() != null) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("Failed to update todo: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
    
    suspend fun deleteTodo(id: Int): Result<Unit> = withContext(Dispatchers.IO) {
        try {
            val response = apiService.deleteTodo(id)
            if (response.isSuccessful) {
                Result.success(Unit)
            } else {
                Result.failure(Exception("Failed to delete todo: ${response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
