<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'

/**
 * A fixed-height window whose content slides up on a click, so a tall slide
 * can show its lower part while the title above stays in place. The top edge
 * fades, so content appears to slide under the title.
 * Give the slide `clicks: <at>` in its frontmatter so the click exists.
 */
const props = withDefaults(defineProps<{
  /** Click number that triggers the slide-up. */
  at?: number
  /** How far to move the content up, in px. */
  shift?: number
  /** Window height, in px. */
  height?: number
}>(), { at: 1, shift: 100, height: 330 })

const { $clicks } = useSlideContext()
const moved = computed(() => $clicks.value >= props.at)
</script>

<template>
  <div class="scroll-stage" :style="{ height: `${height}px` }">
    <div class="scroll-stage-inner" :style="{ transform: moved ? `translateY(-${shift}px)` : 'none' }">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.scroll-stage {
  overflow: hidden;
  padding-top: 14px;
  -webkit-mask-image: linear-gradient(to bottom, transparent 0, #000 14px);
  mask-image: linear-gradient(to bottom, transparent 0, #000 14px);
}
.scroll-stage-inner {
  transition: transform 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
