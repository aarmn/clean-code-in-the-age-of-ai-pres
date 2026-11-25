<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

/**
 * A rotating sphere of dots drawn on a canvas.
 * Dots are spread evenly with a Fibonacci lattice, rotated in 3D,
 * projected with perspective and shaded by depth (front = bright, back = faint).
 */
const props = withDefaults(defineProps<{
  size?: number
  dots?: number
  /** Seconds per full turn. */
  period?: number
  /** Base dot radius in CSS pixels at the sphere's front. */
  dotRadius?: number
}>(), {
  size: 360,
  dots: 900,
  period: 26,
  dotRadius: 1.9,
})

const canvas = ref<HTMLCanvasElement>()
let frame = 0
let visible = false
let observer: IntersectionObserver | undefined
const reduceMotion = typeof window !== 'undefined'
  && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

// Precomputed unit-sphere points.
let points: Float32Array = new Float32Array()
function buildPoints() {
  const n = props.dots
  points = new Float32Array(n * 3)
  const golden = Math.PI * (3 - Math.sqrt(5))
  for (let i = 0; i < n; i++) {
    const y = 1 - (i / (n - 1)) * 2
    const r = Math.sqrt(1 - y * y)
    const theta = golden * i
    points[i * 3] = Math.cos(theta) * r
    points[i * 3 + 1] = y
    points[i * 3 + 2] = Math.sin(theta) * r
  }
}

// Violet (top) -> fuchsia (equator) -> indigo (bottom).
const STOPS: [number, number, number][] = [[196, 167, 255], [240, 171, 252], [129, 140, 248]]
function colorAt(y: number): [number, number, number] {
  const t = (1 - y) / 2 // 0 top, 1 bottom
  const [a, b, k] = t < 0.5 ? [STOPS[0], STOPS[1], t * 2] : [STOPS[1], STOPS[2], (t - 0.5) * 2]
  return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]
}

function draw(time: number) {
  const el = canvas.value
  if (!el)
    return
  const ctx = el.getContext('2d')
  if (!ctx)
    return
  const dpr = Math.min(3, (window.devicePixelRatio || 1) * 1.5)
  const px = Math.round(props.size * dpr)
  if (el.width !== px) {
    el.width = px
    el.height = px
  }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, props.size, props.size)

  const half = props.size / 2
  const radius = half * 0.82
  const yaw = (time / 1000) * (Math.PI * 2 / props.period)
  const tilt = 0.42
  const cy = Math.cos(yaw), sy = Math.sin(yaw)
  const ct = Math.cos(tilt), st = Math.sin(tilt)
  const camera = 3.2

  const n = props.dots
  const order: { x: number, y: number, z: number, oy: number }[] = Array.from({ length: n })
  for (let i = 0; i < n; i++) {
    const x0 = points[i * 3], y0 = points[i * 3 + 1], z0 = points[i * 3 + 2]
    // Rotate around Y (spin), then around X (tilt).
    const x1 = x0 * cy + z0 * sy
    const z1 = -x0 * sy + z0 * cy
    const y2 = y0 * ct - z1 * st
    const z2 = y0 * st + z1 * ct
    order[i] = { x: x1, y: y2, z: z2, oy: y0 }
  }
  order.sort((a, b) => a.z - b.z)

  for (const p of order) {
    const scale = camera / (camera - p.z)
    const sx = half + p.x * radius * scale
    const syy = half + p.y * radius * scale
    const depth = (p.z + 1) / 2 // 0 back, 1 front
    const [r, g, b] = colorAt(p.oy)
    ctx.fillStyle = `rgba(${r | 0},${g | 0},${b | 0},${0.12 + depth * 0.88})`
    ctx.beginPath()
    ctx.arc(sx, syy, props.dotRadius * scale * (0.45 + depth * 0.75), 0, Math.PI * 2)
    ctx.fill()
  }
}

function loop(time: number) {
  draw(time)
  if (visible && !reduceMotion)
    frame = requestAnimationFrame(loop)
}

function start() {
  cancelAnimationFrame(frame)
  frame = requestAnimationFrame(loop)
}

onMounted(() => {
  buildPoints()
  draw(performance.now())
  observer = new IntersectionObserver((entries) => {
    visible = entries.some(e => e.isIntersecting)
    if (visible)
      start()
    else
      cancelAnimationFrame(frame)
  })
  if (canvas.value)
    observer.observe(canvas.value)
})

watch(() => [props.dots, props.size], () => {
  buildPoints()
  draw(performance.now())
})

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  observer?.disconnect()
})
</script>

<template>
  <div class="dot-sphere" :style="{ width: `${size}px`, height: `${size}px` }" aria-hidden="true">
    <canvas ref="canvas" :style="{ width: `${size}px`, height: `${size}px` }" />
  </div>
</template>

<style scoped>
.dot-sphere {
  position: relative;
  flex: none;
}
.dot-sphere::before {
  content: "";
  position: absolute;
  inset: 12%;
  border-radius: 50%;
  background: radial-gradient(circle at 42% 38%, rgba(196, 167, 255, 0.22), rgba(139, 92, 246, 0.08) 45%, transparent 70%);
  filter: blur(18px);
}
canvas {
  position: relative;
  display: block;
}
</style>
