<template>
  <a-carousel autoplay>
    <slot/>
  </a-carousel>
</template>

<style scoped>
:deep(.slick-slide) {
  text-align: center;
  //height: 100%;
  //line-height: 160px;
  //background: #364d79;
  overflow: hidden;
}
:deep(.slick-slide h3) {
  color: #fff;
}


</style>
<script setup lang="ts">
</script>