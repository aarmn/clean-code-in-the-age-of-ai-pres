<script setup lang="ts">
/**
 * A word whose letters slowly "morph around": an animated SVG turbulence
 * filter displaces the glyphs like liquid, while the colour drifts and the
 * font's SOFT/WONK axes change shape (not width).
 *
 * A hidden copy of the word holds the layout, and the animated copy floats
 * over it, so the line never re-wraps while the word moves.
 */
const id = `fuzzy-${Math.random().toString(36).slice(2, 9)}`
</script>

<template>
  <span class="fuzzy-word">
    <span class="fuzzy-ghost" aria-hidden="true"><slot /></span>
    <span class="fuzzy-live" :style="{ filter: `url(#${id})` }"><slot /></span>
    <svg class="fuzzy-defs" width="0" height="0" aria-hidden="true" focusable="false">
      <filter :id="id" x="-20%" y="-35%" width="140%" height="170%">
        <feTurbulence type="fractalNoise" baseFrequency="0.016 0.04" numOctaves="2" seed="7" result="noise">
          <animate attributeName="baseFrequency" dur="9s" repeatCount="indefinite"
                   values="0.012 0.03; 0.024 0.06; 0.016 0.045; 0.012 0.03" />
        </feTurbulence>
        <feDisplacementMap in="SourceGraphic" in2="noise" scale="9" xChannelSelector="R" yChannelSelector="G">
          <animate attributeName="scale" dur="6s" repeatCount="indefinite" values="4; 13; 7; 4" />
        </feDisplacementMap>
      </filter>
    </svg>
  </span>
</template>

<style scoped>
.fuzzy-word {
  position: relative;
  display: inline-block;
  font-style: italic;
  font-variation-settings: "SOFT" 50, "WONK" 0;
}
.fuzzy-ghost {
  visibility: hidden;
}
.fuzzy-live {
  position: absolute;
  left: 50%;
  top: 0;
  transform: translateX(-50%);
  white-space: nowrap;
  padding: 0 .08em;
  background: linear-gradient(90deg, #c4a7ff, #f0abfc, #7ee0f5, #c4a7ff);
  background-size: 300% 100%;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  animation: fuzzy-drift 8s ease-in-out infinite;
}
.fuzzy-defs {
  position: absolute;
  width: 0;
  height: 0;
}
@keyframes fuzzy-drift {
  0%, 100% { background-position: 0% 50%; font-variation-settings: "SOFT" 0, "WONK" 0; }
  50% { background-position: 100% 50%; font-variation-settings: "SOFT" 100, "WONK" 1; }
}
@media (prefers-reduced-motion: reduce) {
  .fuzzy-live { animation: none; filter: none !important; }
}
</style>
