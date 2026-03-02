<template>
  <view class="picker">
    <view class="preview" v-if="garment && previewUrl">
      <image :src="previewUrl" mode="aspectFill" class="img" />
      <view class="mask" @click="clear">
        <text>重选</text>
      </view>
    </view>
    <view class="upload-btn" v-else @click="chooseImage">
      <text class="upload-icon">+</text>
      <text class="upload-text">上传服饰平铺图</text>
      <text class="upload-tip">平铺、无褶皱、背景干净</text>
    </view>
  </view>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { uploadImage } from '../../api/index'

const props = defineProps({
  modelValue: { type: String, default: '' }
})
const emit = defineEmits(['update:modelValue'])

const garment = ref(props.modelValue)

watch(() => props.modelValue, (v) => { garment.value = v })
watch(garment, (v) => emit('update:modelValue', v))

const previewUrl = ref('')  // 本地预览（oss 不可直接展示，用上传前本地路径）

async function chooseImage() {
  const res = await uni.chooseImage({ count: 1, sizeType: ['compressed'] })
  const tempFilePath = res?.tempFilePaths?.[0] || res?.tempFiles?.[0]?.path
  if (!tempFilePath) return
  previewUrl.value = tempFilePath
  uni.showLoading({ title: '上传中' })
  try {
    const url = await uploadImage(tempFilePath)
    garment.value = url
  } catch (e) {
    garment.value = ''
    previewUrl.value = ''
    uni.showToast({ title: e.message || '上传失败', icon: 'none' })
  } finally {
    uni.hideLoading()
  }
}

function clear() {
  garment.value = ''
  previewUrl.value = ''
}
</script>

<style scoped>
.picker {
  min-height: 200rpx;
}
.preview {
  position: relative;
  width: 280rpx;
  height: 280rpx;
  border-radius: 12rpx;
  overflow: hidden;
}
.img {
  width: 100%;
  height: 100%;
}
.mask {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28rpx;
}
.upload-btn {
  width: 280rpx;
  height: 200rpx;
  border: 2rpx dashed #ccc;
  border-radius: 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.upload-icon {
  font-size: 48rpx;
  color: #999;
}
.upload-text {
  font-size: 28rpx;
  color: #666;
  margin-top: 8rpx;
}
.upload-tip {
  font-size: 22rpx;
  color: #999;
  margin-top: 4rpx;
}
</style>
