<script setup lang="ts">
import { computed } from 'vue'
import { encode } from 'uqr'

/** QR code rendered locally as SVG (no network). Colors come from CSS. */
const props = withDefaults(defineProps<{ url: string, size?: number }>(), { size: 96 })

const qr = computed(() => {
  const { data, size } = encode(props.url, { ecc: 'M', border: 0 })
  let d = ''
  data.forEach((row, y) => row.forEach((on, x) => {
    if (on)
      d += `M${x} ${y}h1v1h-1z`
  }))
  return { d, size }
})
</script>

<template>
  <a class="qr-code" :href="url" target="_blank" rel="noopener" :aria-label="`QR code for ${url}`">
    <svg :width="size" :height="size" :viewBox="`-2 -2 ${qr.size + 4} ${qr.size + 4}`" shape-rendering="crispEdges">
      <rect x="-2" y="-2" :width="qr.size + 4" :height="qr.size + 4" rx="1.5" class="qr-bg" />
      <path :d="qr.d" class="qr-fg" />
    </svg>
  </a>
</template>

<style scoped>
.qr-code { display: inline-block; line-height: 0; }
.qr-bg { fill: #f4f0ff; }
.qr-fg { fill: #160f26; }
</style>
