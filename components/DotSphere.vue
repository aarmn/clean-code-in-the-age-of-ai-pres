<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

/**
 * A slowly turning triangle-mesh sphere.
 * An icosphere (subdivided icosahedron) drawn as faintly lit faces, thin edges and
 * small vertex dots. A soft wave of light travels across the edges, so the mesh
 * gently pulses. Everything is shaded by depth: front bright, back faint.
 */
const props = withDefaults(defineProps<{
  size?: number
  /** Subdivision level: 1 = 80 faces, 2 = 320, 3 = 1280. */
  detail?: number
  /** Seconds per full turn. */
  period?: number
  /** Vertex dot radius in CSS pixels. */
  dotRadius?: number
  /** Optional surface displacement (fraction of the radius); 0 keeps a perfect sphere. */
  noise?: number
  /** A wave of light travelling across the edges. */
  pulse?: boolean
  /** Colour family: violet (part one) or cyan (Age of AI). */
  palette?: 'violet' | 'cyan'
}>(), {
  size: 360,
  detail: 3,
  period: 60,
  dotRadius: 1.1,
  noise: 0,
  pulse: true,
  palette: 'violet',
})

const canvas = ref<HTMLCanvasElement>()
let frame = 0
let visible = false
let observer: IntersectionObserver | undefined
const reduceMotion = typeof window !== 'undefined'
  && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

// ── Geometry ──────────────────────────────────────────────────────────
let verts: number[][] = []
let faces: number[][] = []
let edges: number[][] = []
let edgePhase: Float32Array = new Float32Array()

function normalize([x, y, z]: number[]) {
  const l = Math.hypot(x, y, z)
  return [x / l, y / l, z / l]
}

function buildMesh(level: number) {
  const t = (1 + Math.sqrt(5)) / 2
  const v: number[][] = [
    [-1, t, 0], [1, t, 0], [-1, -t, 0], [1, -t, 0],
    [0, -1, t], [0, 1, t], [0, -1, -t], [0, 1, -t],
    [t, 0, -1], [t, 0, 1], [-t, 0, -1], [-t, 0, 1],
  ].map(normalize)
  let f: number[][] = [
    [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
    [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
    [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
    [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
  ]
  for (let l = 0; l < level; l++) {
    const cache = new Map<string, number>()
    const mid = (a: number, b: number) => {
      const key = a < b ? `${a}_${b}` : `${b}_${a}`
      let i = cache.get(key)
      if (i === undefined) {
        i = v.push(normalize([(v[a][0] + v[b][0]) / 2, (v[a][1] + v[b][1]) / 2, (v[a][2] + v[b][2]) / 2])) - 1
        cache.set(key, i)
      }
      return i
    }
    f = f.flatMap(([a, b, c]) => {
      const ab = mid(a, b), bc = mid(b, c), ca = mid(c, a)
      return [[a, ab, ca], [b, bc, ab], [c, ca, bc], [ab, bc, ca]]
    })
  }
  const seen = new Set<string>()
  const e: number[][] = []
  for (const [a, b, c] of f) {
    for (const [p, q] of [[a, b], [b, c], [c, a]]) {
      const key = p < q ? `${p}_${q}` : `${q}_${p}`
      if (!seen.has(key)) {
        seen.add(key)
        e.push([p, q])
      }
    }
  }
  // Each edge's place in the travelling light wave, fixed to the mesh so it turns with it.
  const phase = new Float32Array(e.length)
  e.forEach(([p, q], i) => {
    const mx = (v[p][0] + v[q][0]) / 2, my = (v[p][1] + v[q][1]) / 2, mz = (v[p][2] + v[q][2]) / 2
    phase[i] = (mx * 1.4 + my * 2.6 + mz * 0.8) * 2.1
  })
  verts = v
  faces = f
  edges = e
  edgePhase = phase
}

function wobble(x: number, y: number, z: number, s: number) {
  return 0.6 * Math.sin(2.6 * x + 0.4 * s) * Math.sin(2.9 * y + 0.3 * s + 1.3) * Math.sin(2.3 * z + 0.5 * s + 2.1)
    + 0.4 * Math.sin(4.1 * x + 3.7 * y + 0.6 * s)
}

// Palettes: back → middle → front, plus the colour of the travelling glow.
const PALETTES = {
  violet: { back: [88, 86, 214], mid: [167, 139, 250], front: [233, 190, 255], glow: [250, 205, 255] },
  cyan: { back: [14, 116, 144], mid: [34, 211, 238], front: [165, 243, 252], glow: [207, 250, 254] },
}
function mix(a: number[], b: number[], k: number) {
  return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]
}
function shade(d: number) {
  const p = PALETTES[props.palette]
  return d < 0.5 ? mix(p.back, p.mid, d * 2) : mix(p.mid, p.front, (d - 0.5) * 2)
}
const rgba = (c: number[], a: number) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a.toFixed(3)})`

// ── Drawing ───────────────────────────────────────────────────────────
const DEPTH_BANDS = 6
const GLOW_BANDS = 4

function draw(time: number) {
  const el = canvas.value
  const ctx = el?.getContext('2d')
  if (!el || !ctx)
    return
  const dpr = Math.min(2.5, (window.devicePixelRatio || 1) * 1.5)
  const px = Math.round(props.size * dpr)
  if (el.width !== px) {
    el.width = px
    el.height = px
  }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, props.size, props.size)

  const s = time / 1000
  const half = props.size / 2
  const R = half * 0.74
  const camera = 5
  const yaw = s * (Math.PI * 2 / props.period)
  const tilt = 0.36
  const cy = Math.cos(yaw), sy = Math.sin(yaw), ct = Math.cos(tilt), st = Math.sin(tilt)

  const n = verts.length
  const X = new Float32Array(n), Y = new Float32Array(n), Z = new Float32Array(n)
  const SX = new Float32Array(n), SY = new Float32Array(n), K = new Float32Array(n)
  for (let i = 0; i < n; i++) {
    const [vx, vy, vz] = verts[i]
    const r = props.noise ? 1 + props.noise * wobble(vx, vy, vz, s) : 1
    const x0 = vx * r, y0 = vy * r, z0 = vz * r
    const x1 = x0 * cy + z0 * sy
    const z1 = -x0 * sy + z0 * cy
    const y2 = y0 * ct - z1 * st
    const z2 = y0 * st + z1 * ct
    X[i] = x1; Y[i] = y2; Z[i] = z2
    const k = camera / (camera - z2)
    K[i] = k
    SX[i] = half + x1 * R * k
    SY[i] = half + y2 * R * k
  }

  // Faces: a faint, softly lit skin on the front half.
  const L = normalize([-0.45, -0.55, 0.7])
  const faceBands: number[][][] = Array.from({ length: 5 }, () => [])
  for (const f of faces) {
    const [a, b, c] = f
    const ux = X[b] - X[a], uy = Y[b] - Y[a], uz = Z[b] - Z[a]
    const vx = X[c] - X[a], vy = Y[c] - Y[a], vz = Z[c] - Z[a]
    let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx
    if (nx * (X[a] + X[b] + X[c]) + ny * (Y[a] + Y[b] + Y[c]) + nz * (Z[a] + Z[b] + Z[c]) < 0) {
      nx = -nx; ny = -ny; nz = -nz
    }
    const len = Math.hypot(nx, ny, nz) || 1
    if (nz / len <= 0.05)
      continue
    const light = Math.max(0, (nx * L[0] + ny * L[1] + nz * L[2]) / len)
    faceBands[Math.min(4, Math.floor(light * 5))].push(f)
  }
  faceBands.forEach((band, i) => {
    if (!band.length)
      return
    const lvl = (i + 0.5) / 5
    ctx.fillStyle = rgba(shade(0.4 + lvl * 0.6), 0.01 + lvl * 0.05)
    ctx.beginPath()
    for (const [a, b, c] of band) {
      ctx.moveTo(SX[a], SY[a])
      ctx.lineTo(SX[b], SY[b])
      ctx.lineTo(SX[c], SY[c])
      ctx.closePath()
    }
    ctx.fill()
  })

  // Edges: grouped by depth and by how lit they are by the travelling wave.
  const bands: number[][][] = Array.from({ length: DEPTH_BANDS * GLOW_BANDS }, () => [])
  edges.forEach((e, i) => {
    const d = ((Z[e[0]] + Z[e[1]]) / 2 + 1) / 2
    const wave = props.pulse ? Math.max(0, Math.sin(s * 0.9 - edgePhase[i])) ** 6 : 0
    const db = Math.max(0, Math.min(DEPTH_BANDS - 1, Math.floor(d * DEPTH_BANDS)))
    const gb = Math.min(GLOW_BANDS - 1, Math.floor(wave * GLOW_BANDS))
    bands[db * GLOW_BANDS + gb].push(e)
  })
  const lineScale = props.size / 500
  bands.forEach((band, i) => {
    if (!band.length)
      return
    const d = (Math.floor(i / GLOW_BANDS) + 0.5) / DEPTH_BANDS
    const g = (i % GLOW_BANDS) / (GLOW_BANDS - 1)
    const base = 0.025 + d * d * 0.17
    ctx.strokeStyle = rgba(mix(shade(d), PALETTES[props.palette].glow, g * 0.7), base * (1 + g * 1.6))
    ctx.lineWidth = Math.max(0.3, (0.3 + d * 0.45) * lineScale * (1 + g * 0.35))
    ctx.beginPath()
    for (const [a, b] of band) {
      ctx.moveTo(SX[a], SY[a])
      ctx.lineTo(SX[b], SY[b])
    }
    ctx.stroke()
  })

  // Vertex dots: small, front half only.
  for (let i = 0; i < n; i++) {
    const d = (Z[i] + 1) / 2
    if (d < 0.45)
      continue
    ctx.fillStyle = rgba(shade(d), 0.08 + (d - 0.45) * 0.9)
    ctx.beginPath()
    ctx.arc(SX[i], SY[i], props.dotRadius * K[i] * (0.45 + d * 0.55), 0, Math.PI * 2)
    ctx.fill()
  }
}

function loop(time: number) {
  draw(time)
  if (visible && !reduceMotion)
    frame = requestAnimationFrame(loop)
}

onMounted(() => {
  buildMesh(props.detail)
  draw(performance.now())
  observer = new IntersectionObserver((entries) => {
    visible = entries.some(e => e.isIntersecting)
    cancelAnimationFrame(frame)
    if (visible)
      frame = requestAnimationFrame(loop)
  })
  if (canvas.value)
    observer.observe(canvas.value)
})

watch(() => props.detail, (level) => {
  buildMesh(level)
  draw(performance.now())
})

onBeforeUnmount(() => {
  cancelAnimationFrame(frame)
  observer?.disconnect()
})
</script>

<template>
  <div class="dot-sphere" :class="palette" :style="{ width: `${size}px`, height: `${size}px` }" aria-hidden="true">
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
  inset: 14%;
  border-radius: 50%;
  background: radial-gradient(circle at 40% 36%, rgba(196, 167, 255, 0.16), rgba(139, 92, 246, 0.06) 50%, transparent 72%);
  filter: blur(26px);
}
.dot-sphere.cyan::before {
  background: radial-gradient(circle at 40% 36%, rgba(103, 232, 249, 0.16), rgba(6, 182, 212, 0.06) 50%, transparent 72%);
}
canvas {
  position: relative;
  display: block;
}
</style>
