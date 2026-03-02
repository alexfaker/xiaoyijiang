<template>
  <view class="model-picker">
    <view class="tabs">
      <view
        v-for="t in tabs"
        :key="t.key"
        class="tab"
        :class="{ active: activeTab === t.key }"
        @click="activeTab = t.key"
      >
        {{ t.label }}
      </view>
    </view>
    <view class="content">
      <view v-if="activeTab === 'female'" class="preset-grid">
        <view
          v-for="(m, i) in femaleModels"
          :key="i"
          class="model-card"
          :class="{ active: model === m.url }"
          @click="selectPreset(m.url)"
        >
          <image :src="m.thumb" mode="aspectFill" class="thumb" />
          <view class="radio" :class="{ checked: model === m.url }" />
          <view class="card-info">
            <text class="card-name">{{ m.name }}</text>
            <text class="card-style">{{ m.style }}</text>
          </view>
        </view>
      </view>
      <view v-else-if="activeTab === 'male'" class="preset-grid">
        <view
          v-for="(m, i) in maleModels"
          :key="i"
          class="model-card"
          :class="{ active: model === m.url }"
          @click="selectPreset(m.url)"
        >
          <image :src="m.thumb" mode="aspectFill" class="thumb" />
          <view class="radio" :class="{ checked: model === m.url }" />
          <view class="card-info">
            <text class="card-name">{{ m.name }}</text>
            <text class="card-style">{{ m.style }}</text>
          </view>
        </view>
      </view>
      <view v-else class="custom-area">
        <view class="uploaded-preview" v-if="localPreviewPath">
          <image :src="localPreviewPath" mode="aspectFill" class="preview-img" />
          <view class="mask" @click="clearUploaded">
            <text>重选</text>
          </view>
        </view>
        <view class="upload-btn" v-else @click="chooseImage">
          <text class="upload-icon">+</text>
          <text class="upload-text">上传模特照</text>
          <text class="upload-tip">全身站立，标准姿势</text>
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
import { ref, watch } from 'vue'
import { uploadImage } from '../../api/index'

const props = defineProps({
  modelValue: { type: String, default: '' }
})
const emit = defineEmits(['update:modelValue'])

const model = ref(props.modelValue)
const localPreviewPath = ref('')
const activeTab = ref('female')

const tabs = [
  { key: 'female', label: '女模' },
  { key: 'male', label: '男模' },
  { key: 'custom', label: '自定义' }
]

// 女模：标准姿势站立、全身照（符合 API 要求：全身正面、光照良好）
const femaleModels = ref([
  { name: '柔妍', style: '优雅风', url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png', thumb: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png' },
])

// 男模：标准姿势站立、全身照
const maleModels = ref([
  { name: '俊宇', style: '休闲风', url: 'https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=600', thumb: 'https://images.pexels.com/photos/2379004/pexels-photo-2379004.jpeg?auto=compress&cs=tinysrgb&w=600' },
])

watch(() => props.modelValue, (v) => {
  model.value = v
  if (!v || !v.startsWith('oss://')) {
    localPreviewPath.value = ''
    if (femaleModels.value.some(m => m.url === v)) activeTab.value = 'female'
    else if (maleModels.value.some(m => m.url === v)) activeTab.value = 'male'
  } else {
    activeTab.value = 'custom'
  }
})
watch(model, (v) => emit('update:modelValue', v))

function selectPreset(url) {
  localPreviewPath.value = ''
  model.value = url
  if (femaleModels.value.some(m => m.url === url)) activeTab.value = 'female'
  else if (maleModels.value.some(m => m.url === url)) activeTab.value = 'male'
}

function clearUploaded() {
  localPreviewPath.value = ''
  model.value = ''
}

async function chooseImage() {
  const res = await uni.chooseImage({ count: 1, sizeType: ['compressed'] })
  const tempFilePath = res?.tempFilePaths?.[0] || res?.tempFiles?.[0]?.path
  if (!tempFilePath) return
  activeTab.value = 'custom'
  localPreviewPath.value = tempFilePath
  uni.showLoading({ title: '上传中' })
  try {
    const url = await uploadImage(tempFilePath)
    model.value = url
  } catch (e) {
    localPreviewPath.value = ''
    model.value = ''
    uni.showToast({ title: e.message || '上传失败', icon: 'none' })
  } finally {
    uni.hideLoading()
  }
}
</script>

<style scoped>
.model-picker {
  background: #fff;
  border-radius: 12rpx;
  overflow: hidden;
}
.tabs {
  display: flex;
  background: #f8f8f8;
  padding: 0 16rpx;
}
.tab {
  flex: 1;
  text-align: center;
  padding: 24rpx 0;
  font-size: 28rpx;
  color: #666;
}
.tab.active {
  color: #1989fa;
  font-weight: 600;
  border-bottom: 4rpx solid #1989fa;
}
.content {
  padding: 24rpx;
  min-height: 200rpx;
}
.preset-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}
.model-card {
  position: relative;
  width: 210rpx;
  height: 280rpx;
  border-radius: 12rpx;
  overflow: hidden;
  border: 4rpx solid transparent;
  background: #f5f5f5;
}
.model-card.active {
  border-color: #1989fa;
}
.thumb {
  width: 100%;
  height: 100%;
}
.radio {
  position: absolute;
  top: 16rpx;
  right: 16rpx;
  width: 36rpx;
  height: 36rpx;
  border-radius: 50%;
  border: 2rpx solid #ccc;
  background: #fff;
}
.radio.checked {
  border-color: #1989fa;
  background: #1989fa;
}
.card-info {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 12rpx;
  background: linear-gradient(transparent, rgba(0,0,0,0.6));
  color: #fff;
}
.card-name {
  display: block;
  font-size: 26rpx;
  font-weight: 600;
}
.card-style {
  font-size: 22rpx;
  opacity: 0.9;
}
.custom-area {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}
.uploaded-preview {
  position: relative;
  width: 210rpx;
  height: 280rpx;
  border-radius: 12rpx;
  overflow: hidden;
  border: 4rpx solid #1989fa;
}
.preview-img {
  width: 100%;
  height: 100%;
}
.uploaded-preview .mask {
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
  width: 210rpx;
  height: 280rpx;
  border: 2rpx dashed #ccc;
  border-radius: 12rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.upload-icon {
  font-size: 64rpx;
  color: #999;
}
.upload-text {
  font-size: 28rpx;
  color: #666;
  margin-top: 16rpx;
}
.upload-tip {
  font-size: 22rpx;
  color: #999;
  margin-top: 8rpx;
}
</style>
