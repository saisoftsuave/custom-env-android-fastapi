package com.saibabui.androidapp.ui.todo

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.saibabui.androidapp.data.model.Todo
import com.saibabui.androidapp.data.repository.TodoRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * UI State for Todo list screen
 */
data class TodoUiState(
    val todos: List<Todo> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val showAddDialog: Boolean = false,
    val editingTodo: Todo? = null
)

/**
 * ViewModel for Todo management
 */
class TodoViewModel : ViewModel() {
    
    private val repository = TodoRepository()
    
    private val _uiState = MutableStateFlow(TodoUiState())
    val uiState: StateFlow<TodoUiState> = _uiState.asStateFlow()
    
    init {
        loadTodos()
    }
    
    fun loadTodos() {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, error = null)
            repository.getTodos()
                .onSuccess { todos ->
                    _uiState.value = _uiState.value.copy(
                        todos = todos,
                        isLoading = false
                    )
                }
                .onFailure { exception ->
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = exception.message ?: "Unknown error"
                    )
                }
        }
    }
    
    fun createTodo(title: String, description: String) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            val todo = Todo(title = title, description = description)
            repository.createTodo(todo)
                .onSuccess {
                    _uiState.value = _uiState.value.copy(showAddDialog = false)
                    loadTodos()
                }
                .onFailure { exception ->
                    _uiState.value = _uiState.value.copy(
                        isLoading = false,
                        error = exception.message
                    )
                }
        }
    }
    
    fun updateTodo(todo: Todo) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            todo.id?.let { id ->
                repository.updateTodo(id, todo)
                    .onSuccess {
                        _uiState.value = _uiState.value.copy(editingTodo = null)
                        loadTodos()
                    }
                    .onFailure { exception ->
                        _uiState.value = _uiState.value.copy(
                            isLoading = false,
                            error = exception.message
                        )
                    }
            }
        }
    }
    
    fun toggleTodoCompleted(todo: Todo) {
        val updatedTodo = todo.copy(completed = !todo.completed)
        updateTodo(updatedTodo)
    }
    
    fun deleteTodo(todo: Todo) {
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true)
            todo.id?.let { id ->
                repository.deleteTodo(id)
                    .onSuccess {
                        loadTodos()
                    }
                    .onFailure { exception ->
                        _uiState.value = _uiState.value.copy(
                            isLoading = false,
                            error = exception.message
                        )
                    }
            }
        }
    }
    
    fun showAddDialog() {
        _uiState.value = _uiState.value.copy(showAddDialog = true)
    }
    
    fun hideAddDialog() {
        _uiState.value = _uiState.value.copy(showAddDialog = false)
    }
    
    fun showEditDialog(todo: Todo) {
        _uiState.value = _uiState.value.copy(editingTodo = todo)
    }
    
    fun hideEditDialog() {
        _uiState.value = _uiState.value.copy(editingTodo = null)
    }
    
    fun clearError() {
        _uiState.value = _uiState.value.copy(error = null)
    }
}
