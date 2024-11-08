<script setup>
defineProps({
  msg: {
    type: String,
    required: true
  }
})
</script>

<template>
  <div class="container rounded text-white bg-dark mt-1 pb-1">
      <h1 class="text-h3 text-height text-center">{{ msg }}</h1>
  </div>
</template>

