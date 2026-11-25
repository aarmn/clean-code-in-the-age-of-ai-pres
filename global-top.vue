<script setup lang="ts">
/*
 * Footer drawn above every slide (global-top layer; global-bottom sits under the
 * opaque slide background and would be hidden).
 *
 * Labels come from slide frontmatter, so nothing depends on page numbers:
 *   part: classic | ai   -> on the slide where that part starts
 *   chapter: Patterns    -> on the first slide of a chapter
 *   footer: false        -> hide the footer on that slide (the cover)
 */
type Fm = Record<string, any>
interface Route { no: number, meta?: { slide?: { frontmatter?: Fm } } }

const PARTS: Record<string, string> = { classic: '01 / CLASSIC', ai: '02 / AGE OF AI' }

function fm(route?: Route): Fm {
  return route?.meta?.slide?.frontmatter ?? {}
}
function lastBefore(slides: Route[], no: number, key: string): string | undefined {
  for (let i = Math.min(no, slides.length) - 1; i >= 0; i--) {
    const value = fm(slides[i])[key]
    if (value !== undefined)
      return String(value)
  }
}
function label(slides: Route[], no: number): string {
  const part = lastBefore(slides, no, 'part')
  const chapter = lastBefore(slides, no, 'chapter')
  const partLabel = part ? PARTS[part] ?? part : 'CLEAN CODE IN THE AI AGE'
  return chapter && part ? `${partLabel}  ·  ${chapter.toUpperCase()}` : partLabel
}
function shown(slides: Route[], no: number): boolean {
  return fm(slides[no - 1]).footer !== false
}
function isAi(slides: Route[], no: number): boolean {
  return lastBefore(slides, no, 'part') === 'ai'
}
</script>

<template>
  <div v-if="shown($nav.slides, $nav.currentSlideNo)" class="deck-chrome" :class="{ 'is-ai': isAi($nav.slides, $nav.currentSlideNo) }" aria-hidden="true">
    <div class="deck-fade" />
    <div class="deck-foot">
      <span class="deck-foot-label">{{ label($nav.slides, $nav.currentSlideNo) }}</span>
      <span class="bar" />
      <span class="page">{{ String($nav.currentSlideNo).padStart(2, '0') }}</span>
      <DotSphere class="deck-foot-sphere" :size="58" :dots="260" :dot-radius="1.05" :period="18" />
    </div>
  </div>
</template>
