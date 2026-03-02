<template>
  <view class="page">
    <view class="section">
      <text class="label">选择模特</text>
      <model-picker v-model="personUrl" />
    </view>
    <view class="section">
      <text class="label">选择服饰</text>
      <garment-picker v-model="garmentUrl" />
    </view>
    <button
      class="btn-tryon"
      :disabled="!personUrl || !garmentUrl || loading"
      @click="onTryon"
    >
      {{ loading ? '生成中...' : '开始换衣' }}
    </button>
  </view>
</template>

<script setup>
import { ref } from 'vue'
import ModelPicker from '../../components/model-picker/model-picker.vue'
import GarmentPicker from '../../components/garment-picker/garment-picker.vue'
import { createTryon } from '../../api/index'

const personUrl = ref('')
const garmentUrl = ref('')
const loading = ref(false)

async function onTryon() {
  if (!personUrl.value || !garmentUrl.value) return
  loading.value = true
  try {
    const { task_id } = await createTryon(personUrl.value, garmentUrl.value)
    uni.navigateTo({
      url: `/pages/result/result?taskId=${task_id}`
    })
  } catch (e) {
    uni.showToast({ title: e.message || '创建失败', icon: 'none' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page {
  padding: 32rpx;
  min-height: 100vh;
}
.section {
  margin-bottom: 40rpx;
}
.label {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 16rpx;
}
.btn-tryon {
  margin-top: 48rpx;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: #fff;
  border-radius: 12rpx;
  font-size: 32rpx;
  height: 88rpx;
  line-height: 88rpx;
}
.btn-tryon[disabled] {
  opacity: 0.6;
}
</style>
