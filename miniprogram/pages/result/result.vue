<template>
  <view class="page">
    <view v-if="status === 'SUCCEEDED'" class="result">
      <image :src="resultUrl" mode="widthFix" class="result-img" />
      <view class="actions">
        <button @click="saveImage">保存图片</button>
      </view>
    </view>
    <view v-else-if="status === 'FAILED'" class="error">
      <text>{{ message || '生成失败' }}</text>
    </view>
    <view v-else class="loading">
      <text>生成中，请稍候...</text>
    </view>
  </view>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getTryonResult, getProxiedImageUrl } from '../../api/index'

const taskId = ref('')
const status = ref('PENDING')
const resultUrl = ref('')
const message = ref('')

onMounted(() => {
  const pages = getCurrentPages()
  const page = pages[pages.length - 1]
  taskId.value = page.options?.taskId || ''
  if (taskId.value) poll()
})

async function poll() {
  const maxAttempts = 60
  for (let i = 0; i < maxAttempts; i++) {
    const res = await getTryonResult(taskId.value)
    status.value = res.status
    if (res.status === 'SUCCEEDED') {
      resultUrl.value = getProxiedImageUrl(res.result_image_url) || ''
      return
    }
    if (res.status === 'FAILED') {
      message.value = res.message || '任务失败'
      return
    }
    await new Promise((r) => setTimeout(r, 2000))
  }
  status.value = 'FAILED'
  message.value = '超时，请返回重试'
}

function saveImage() {
  uni.downloadFile({
    url: resultUrl.value,
    success: (res) => {
      if (res.statusCode === 200) {
        uni.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success: () => uni.showToast({ title: '已保存' }),
          fail: () => uni.showToast({ title: '需授权相册', icon: 'none' })
        })
      }
    }
  })
}
</script>

<style scoped>
.page {
  padding: 32rpx;
  min-height: 100vh;
}
.result-img {
  width: 100%;
  border-radius: 12rpx;
}
.actions {
  margin-top: 32rpx;
}
.error, .loading {
  text-align: center;
  padding: 80rpx;
  color: #999;
}
</style>
