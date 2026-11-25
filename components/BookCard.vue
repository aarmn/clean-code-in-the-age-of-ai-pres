<script setup lang="ts">
import { ref } from 'vue'

/**
 * A book with its cover. The cover image comes from Open Library by ISBN;
 * if it can't load (offline, not found), a typographic cover shows instead.
 */
const props = defineProps<{
  title: string
  author: string
  isbn: string
  href: string
  /** Short note under the title, e.g. "Free online". */
  note?: string
}>()

const coverFailed = ref(false)
const coverUrl = `https://covers.openlibrary.org/b/isbn/${props.isbn}-M.jpg?default=false`
</script>

<template>
  <a class="book" :href="href" target="_blank" rel="noopener">
    <div class="book-cover">
      <div class="book-fallback">
        <span class="book-fallback-title">{{ title }}</span>
        <span class="book-fallback-author">{{ author }}</span>
      </div>
      <img v-if="!coverFailed" :src="coverUrl" :alt="`Cover of ${title}`" loading="eager" @error="coverFailed = true">
    </div>
    <div class="book-meta">
      <strong>{{ title }}</strong>
      <span>{{ author }}</span>
      <em v-if="note">{{ note }}</em>
    </div>
  </a>
</template>

<style scoped>
.book { display: flex; flex-direction: column; gap: 9px; color: inherit; text-decoration: none; min-width: 0; }
.book-cover {
  position: relative; aspect-ratio: 2 / 3; border-radius: 6px; overflow: hidden;
  border: 1px solid var(--line-strong); box-shadow: 0 10px 24px rgba(0, 0, 0, 0.45);
  background: linear-gradient(150deg, #2a1f47, #1a1230);
}
.book-cover img { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.book-fallback { position: absolute; inset: 0; display: flex; flex-direction: column; justify-content: space-between; padding: 10px; }
.book-fallback-title { font: 600 13px/1.15 var(--serif); color: var(--paper); }
.book-fallback-author { font: 9px var(--mono); color: var(--accent); letter-spacing: .06em; text-transform: uppercase; }
.book-meta { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.book-meta strong { font: 600 13px/1.2 var(--sans); color: var(--paper); }
.book-meta span { font-size: 11.5px; line-height: 1.3; color: var(--muted); }
.book-meta em { font: normal 10px var(--mono); color: var(--accent); letter-spacing: .05em; text-transform: uppercase; margin-top: 2px; }
.book:hover .book-cover { border-color: var(--accent); }
</style>
