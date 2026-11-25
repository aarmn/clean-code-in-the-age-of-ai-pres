<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'

/**
 * A slowly turning triangle-mesh sphere.
 * An icosphere (subdivided icosahedron) whose vertices breathe with smooth noise,
 * drawn as softly lit faces, glowing edges and vertex dots. Optional orbit rings
 * of particles circle it. Everything is shaded by depth: front bright, back faint.
 */
const props = withDefaults(defineProps<{
  size?: number
  /** Subdivision level: 1 = 80 faces, 2 = 320, 3 = 1280. */
  detail?: number
  /** Seconds per full turn. */
  period?: number
  /** Vertex dot radius in CSS pixels. */
  dotRadius?: number
  /** How far the noise pushes vertices in and out (fraction of the radius). */
  noise?: number
  /** Draw orbiting particle rings. */
  rings?: boolean
}>(), {
  size: 360,
  detail: 3,
  period: 30,
  dotRadius: 1.4,
  noise: 0.07,
  rings: false,
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
  verts = v
  faces = f
  edges = e
}

function normalize([x, y, z]: number[]) {
  const l = Math.hypot(x, y, z)
  return [x / l, y / l, z / l]
}

/** Smooth, cheap 3D noise in [-1, 1], animated by s (seconds). */
function wobble(x: number, y: number, z: number, s: number) {
  return 0.55 * Math.sin(2.6 * x + 0.9 * s) * Math.sin(2.9 * y + 0.7 * s + 1.3) * Math.sin(2.3 * z + 1.1 * s + 2.1)
    + 0.30 * Math.sin(4.7 * x + 3.9 * y + 1.6 * s)
    + 0.15 * Math.sin(6.1 * z - 4.3 * x + 2.3 * s)
}

// Palette: indigo (back) → violet → fuchsia (front).
const BACK = [99, 102, 241]
const MIDC = [167, 139, 250]
const FRONT = [240, 171, 252]
function shade(d: number): number[] {
  const [a, b, k] = d < 0.5 ? [BACK, MIDC, d * 2] : [MIDC, FRONT, (d - 0.5) * 2]
  return [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k]
}
const rgba = (c: number[], a: number) => `rgba(${c[0] | 0},${c[1] | 0},${c[2] | 0},${a.toFixed(3)})`

// ── Drawing ───────────────────────────────────────────────────────────
const BANDS = 8
function draw(time: number) {
  const el = canvas.value
  const ctx = el?.getContext('2d')
  if (!el || !ctx)
    return
  const dpr = Math.min(3, (window.devicePixelRatio || 1) * 1.5)
  const px = Math.round(props.size * dpr)
  if (el.width !== px) {
    el.width = px
    el.height = px
  }
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, props.size, props.size)

  const s = time / 1000
  const half = props.size / 2
  const R = half * (props.rings ? 0.6 : 0.74)
  const camera = 5
  const yaw = s * (Math.PI * 2 / props.period)
  const tilt = 0.38
  const cy = Math.cos(yaw), sy = Math.sin(yaw), ct = Math.cos(tilt), st = Math.sin(tilt)

  // Transform vertices: noise displacement, then spin (Y) and tilt (X).
  const n = verts.length
  const X = new Float32Array(n), Y = new Float32Array(n), Z = new Float32Array(n)
  const SX = new Float32Array(n), SY = new Float32Array(n), K = new Float32Array(n)
  for (let i = 0; i < n; i++) {
    const [vx, vy, vz] = verts[i]
    const r = 1 + props.noise * wobble(vx, vy, vz, s)
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

  // Faces: shade front-facing triangles by a soft light from the upper left.
  const L = normalize([-0.45, -0.55, 0.7])
  const faceBands: number[][][] = Array.from({ length: BANDS }, () => [])
  for (const f of faces) {
    const [a, b, c] = f
    const ux = X[b] - X[a], uy = Y[b] - Y[a], uz = Z[b] - Z[a]
    const vx = X[c] - X[a], vy = Y[c] - Y[a], vz = Z[c] - Z[a]
    let nx = uy * vz - uz * vy, ny = uz * vx - ux * vz, nz = ux * vy - uy * vx
    const mx = X[a] + X[b] + X[c], my = Y[a] + Y[b] + Y[c], mz = Z[a] + Z[b] + Z[c]
    if (nx * mx + ny * my + nz * mz < 0) { nx = -nx; ny = -ny; nz = -nz }
    const len = Math.hypot(nx, ny, nz) || 1
    if (nz / len <= 0.02)
      continue
    const light = Math.max(0, (nx * L[0] + ny * L[1] + nz * L[2]) / len)
    faceBands[Math.min(BANDS - 1, Math.floor(light * BANDS))].push(f)
  }
  faceBands.forEach((band, i) => {
    if (!band.length)
      return
    const lvl = (i + 0.5) / BANDS
    ctx.fillStyle = rgba(shade(0.35 + lvl * 0.65), 0.025 + lvl * 0.13)
    ctx.beginPath()
    for (const [a, b, c] of band) {
      ctx.moveTo(SX[a], SY[a])
      ctx.lineTo(SX[b], SY[b])
      ctx.lineTo(SX[c], SY[c])
      ctx.closePath()
    }
    ctx.fill()
  })

  // Edges, grouped by depth so each band is a single stroke.
  const edgeBands: number[][][] = Array.from({ length: BANDS }, () => [])
  for (const e of edges) {
    const d = ((Z[e[0]] + Z[e[1]]) / 2 + 1) / 2
    edgeBands[Math.max(0, Math.min(BANDS - 1, Math.floor(d * BANDS)))].push(e)
  }
  const lineScale = props.size / 400
  edgeBands.forEach((band, i) => {
    if (!band.length)
      return
    const d = (i + 0.5) / BANDS
    ctx.strokeStyle = rgba(shade(d), 0.05 + d * d * 0.55)
    ctx.lineWidth = Math.max(0.35, (0.35 + d * 0.75) * lineScale)
    ctx.beginPath()
    for (const [a, b] of band) {
      ctx.moveTo(SX[a], SY[a])
      ctx.lineTo(SX[b], SY[b])
    }
    ctx.stroke()
  })

  // Vertex dots, front ones brighter and larger.
  for (let i = 0; i < n; i++) {
    const d = (Z[i] + 1) / 2
    if (d < 0.35)
      continue
    ctx.fillStyle = rgba(shade(d), 0.15 + d * 0.85)
    ctx.beginPath()
    ctx.arc(SX[i], SY[i], props.dotRadius * K[i] * (0.4 + d * 0.8), 0, Math.PI * 2)
    ctx.fill()
  }

  if (props.rings)
    drawRings(ctx, s, half, R, camera)
}

function drawRings(ctx: CanvasRenderingContext2D, s: number, half: number, R: number, camera: number) {
  const rings = [
    { count: 120, radius: 1.34, tiltX: 1.18, tiltZ: 0.32, speed: 0.22, size: 1.15 },
    { count: 80, radius: 1.52, tiltX: 1.42, tiltZ: -0.5, speed: -0.14, size: 0.9 },
  ]
  for (const ring of rings) {
    const cx = Math.cos(ring.tiltX), sx = Math.sin(ring.tiltX)
    const cz = Math.cos(ring.tiltZ), sz = Math.sin(ring.tiltZ)
    for (let i = 0; i < ring.count; i++) {
      const a = (i / ring.count) * Math.PI * 2 + s * ring.speed
      const jitter = 1 + 0.03 * Math.sin(i * 12.9898 + s * 0.8)
      let x = Math.cos(a) * ring.radius * jitter
      let y = 0
      let z = Math.sin(a) * ring.radius * jitter
      const y1 = y * cx - z * sx
      const z1 = y * sx + z * cx
      y = y1; z = z1
      const x2 = x * cz - y * sz
      const y2 = x * sz + y * cz
      x = x2; y = y2
      const k = camera / (camera - z)
      const px = half + x * R * k
      const py = half + y * R * k
      // Dim particles that pass behind the sphere.
      const behind = z < 0 && Math.hypot(x, y) < 1.05
      const d = (z / ring.radius + 1) / 2
      const alpha = behind ? 0.06 : 0.2 + d * 0.7
      ctx.fillStyle = rgba(shade(0.4 + d * 0.6), alpha)
      ctx.beginPath()
      ctx.arc(px, py, ring.size * k * (0.5 + d * 0.7), 0, Math.PI * 2)
      ctx.fill()
    }
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
  inset: 18%;
  border-radius: 50%;
  background: radial-gradient(circle at 42% 38%, rgba(196, 167, 255, 0.22), rgba(139, 92, 246, 0.08) 45%, transparent 70%);
  filter: blur(22px);
}
canvas {
  position: relative;
  display: block;
}
</style>
