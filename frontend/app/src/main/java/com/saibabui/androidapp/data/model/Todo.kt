package com.saibabui.androidapp.data.model

import com.google.gson.annotations.SerializedName

/**
 * Todo data class matching the backend model
 */
data class Todo(
    @SerializedName("id")
    val id: Int? = null,
    
    @SerializedName("title")
    val title: String,
    
    @SerializedName("description")
    val description: String = "",
    
    @SerializedName("completed")
    val completed: Boolean = false
)
