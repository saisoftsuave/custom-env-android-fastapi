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
                    val releases = response.body() ?: return@withContext null
                    
                    // Filter and map to include build ID for sorting
                    val releaseData = releases.mapNotNull { release ->
                        val id = release.tagName.replace(Regex("[^0-9]"), "").toIntOrNull() ?: 0
                        if (id > 0) release to id else null
                    }.sortedByDescending { it.second }

                    val (latestRelease, remoteBuildId) = releaseData.firstOrNull() ?: return@withContext null
                    val currentBuildId = BuildConfig.BUILD_NUMBER
                    
                    Log.d("UpdateManager", "Build Check - Local: $currentBuildId, Remote (Latest): $remoteBuildId")
                    
                    if (remoteBuildId > currentBuildId) {
                        val apkAsset = latestRelease.assets.find { it.name.endsWith(".apk") }
                        Log.d("UpdateManager", "New version found! URL: ${apkAsset?.downloadUrl}")
                        return@withContext apkAsset?.downloadUrl
                    } else {
                        Log.d("UpdateManager", "App is up to date (or local version is ahead).")
                    }
                }
            } catch (e: Exception) {
                Log.e("UpdateManager", "Error checking for update", e)
            }
            return@withContext null
        }
    }

    fun downloadUpdate(url: String, onComplete: () -> Unit) {
        val destinationFile = File(context.getExternalFilesDir(Environment.DIRECTORY_DOWNLOADS), "update.apk")
        if (destinationFile.exists()) {
            destinationFile.delete()
            Log.d("UpdateManager", "Deleted existing update.apk before new download")
        }

        val request = DownloadManager.Request(Uri.parse(url))
            .setTitle("Todo App Update")
            .setDescription("Downloading latest version...")
            .setNotificationVisibility(DownloadManager.Request.VISIBILITY_VISIBLE)
            .setDestinationInExternalFilesDir(context, Environment.DIRECTORY_DOWNLOADS, "update.apk")
            .setMimeType("application/vnd.android.package-archive")

        val manager = context.getSystemService(Context.DOWNLOAD_SERVICE) as DownloadManager
        val downloadId = manager.enqueue(request)
        Log.d("UpdateManager", "Enqueued download ID: $downloadId")

        val receiver = object : BroadcastReceiver() {
            override fun onReceive(ctxt: Context?, intent: Intent?) {
                val id = intent?.getLongExtra(DownloadManager.EXTRA_DOWNLOAD_ID, -1)
                if (id == downloadId) {
                    Log.d("UpdateManager", "Download complete!")
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
