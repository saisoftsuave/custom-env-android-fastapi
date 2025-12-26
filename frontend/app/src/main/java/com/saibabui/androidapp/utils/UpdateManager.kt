package com.saibabui.androidapp.utils

import android.app.DownloadManager
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.net.Uri
import android.os.Environment
import android.util.Log
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import com.saibabui.androidapp.BuildConfig
import com.saibabui.androidapp.data.api.GitHubClient
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File

class UpdateManager(private val context: Context) {

    suspend fun checkForUpdate(owner: String, repo: String): String? {
        return withContext(Dispatchers.IO) {
            try {
                val response = GitHubClient.api.getReleases(owner, repo)
                if (response.isSuccessful) {
                    Log.d("UpdateManager", "Response: ${response.body()}")
                    val releases = response.body()
                    val latestRelease = releases?.firstOrNull() ?: return@withContext null
                    val tagName = latestRelease.tagName
                    
                    // Parse "debug-42" -> 42
                    val remoteBuildId = tagName.replace(Regex("[^0-9]"), "").toIntOrNull() ?: 0
                    val currentBuildId = BuildConfig.BUILD_NUMBER
                    
                    Log.d("UpdateManager", "Current: $currentBuildId, Remote: $remoteBuildId")
                    
                    if (remoteBuildId > currentBuildId) {
                        // Return download URL of the first apk asset
                        return@withContext latestRelease.assets.find { it.name.endsWith(".apk") }?.downloadUrl
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
            return@withContext null
        }
    }

    fun downloadUpdate(url: String, onComplete: () -> Unit) {
        val request = DownloadManager.Request(Uri.parse(url))
            .setTitle("Todo App Update")
            .setDescription("Downloading latest version...")
            .setNotificationVisibility(DownloadManager.Request.VISIBILITY_HIDDEN) // Hide from notification bar for a cleaner feel
            .setDestinationInExternalFilesDir(context, Environment.DIRECTORY_DOWNLOADS, "update.apk")
            .setMimeType("application/vnd.android.package-archive")

        val manager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
        val downloadId = manager.enqueue(request)

        val receiver = object : BroadcastReceiver() {
            override fun onReceive(ctxt: Context?, intent: Intent?) {
                val id = intent?.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1)
                if (id == downloadId) {
                    onComplete()
                    context.unregisterReceiver(this)
                }
            }
        }
        ContextCompat.registerReceiver(
            context,
            receiver,
            IntentFilter(DownloadManager.ACTION_DOWNLOAD_COMPLETE),
            ContextCompat.RECEIVER_NOT_EXPORTED
        )
    }

    fun promptInstall() {
        val file = File(context.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), "update.apk")
        if (file.exists()) {
            val uri = FileProvider.getUriForFile(
                context,
                "${context.packageName}.fileprovider",
                file
            )
            val intent = Intent(Intent.ACTION_VIEW).apply {
                setDataAndType(uri, "application/vnd.android.package-archive")
                addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)
            }
            context.startActivity(intent)
        }
    }
}
