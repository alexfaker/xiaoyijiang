<script setup lang="ts">
// 应用根组件
</script>

<template>
  <view>
    <page-meta :page-style="'overflow:' + (overflow ? 'hidden' : 'visible')" />
  </view>
</template>

<script lang="ts">
export default {
  data() {
    return { overflow: false }
  }
}
</script>

<style>
page {
  background-color: #f5f5f5;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
