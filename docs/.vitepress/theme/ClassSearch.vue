<script setup>
import { ref, computed } from 'vue'
import classData from '../../classdata.json'

// Pre-built lookup used by inheritanceChains — avoids rebuilding on every call.
const byName = Object.fromEntries(classData.map(c => [c.name, c]))

const query = ref('')
const expanded = ref(new Set())

function toggle(name) {
  const s = new Set(expanded.value)
  if (s.has(name)) s.delete(name)
  else s.add(name)
  expanded.value = s
}

function isExpanded(name) {
  return expanded.value.has(name)
}

function expandAll() {
  expanded.value = new Set(results.value.map(c => c.name))
}

function collapseAll() {
  expanded.value = new Set()
}

// ObjField is the base descriptor class — it appears in classdata.json because
// the AST parser picks up all classes, but it isn't a user-facing wrapper and
// should not appear in the search UI.
const BASE_CLASSES = new Set(['ObjField'])

const displayClasses = computed(() =>
  classData.filter(c => !BASE_CLASSES.has(c.name))
)

// Score a class against the query — higher = better match.
// Tier 0 (highest): class name
// Tier 1: property name
// Tier 2: property key (a<int>)
// Tier 3: method name / doc / class doc / property description
function scoreClass(cls, q) {
  if (cls.name.toLowerCase().includes(q)) return 0
  if (cls.props.some(p => p.name.toLowerCase().includes(q))) return 1
  if (cls.props.some(p => p.key && p.key.toLowerCase().includes(q))) return 2
  const descMatch =
    cls.doc.toLowerCase().includes(q) ||
    cls.props.some(p => p.doc.toLowerCase().includes(q)) ||
    cls.methods.some(m => m.name.toLowerCase().includes(q) || m.doc.toLowerCase().includes(q))
  if (descMatch) return 3
  return Infinity
}

const results = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return displayClasses.value

  return displayClasses.value
    .map(cls => ({ cls, score: scoreClass(cls, q) }))
    .filter(({ score }) => score < Infinity)
    .sort((a, b) => a.score - b.score)
    .map(({ cls }) => cls)
})

function highlight(text, q) {
  if (!q || !text) return text
  const escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return text.replace(new RegExp(`(${escaped})`, 'gi'), '<mark>$1</mark>')
}

function hl(text) {
  return highlight(text, query.value.trim().toLowerCase())
}

// Pre-computed inheritance chain for every class, keyed by class name.
// Avoids calling the chain builder on every render cycle in the template.
const inheritanceChains = computed(() => {
  const result = {}
  for (const cls of classData) {
    const chain = [cls.name]
    let current = cls
    while (current.bases && current.bases.length > 0) {
      const parentName = current.bases[0]
      chain.unshift(parentName)
      current = byName[parentName]
      if (!current) break
    }
    result[cls.name] = chain
  }
  return result
})
</script>

<template>
  <div class="cls-toolbar">
    <input
      v-model="query"
      class="cls-search-input"
      placeholder="Search by class name, property, key (a51…), or description"
      spellcheck="false"
      autocomplete="off"
    />
    <div class="cls-toolbar-right">
      <span class="cls-count">{{ results.length }} / {{ displayClasses.length }} classes</span>
      <button class="cls-btn" @click="expandAll">Expand all</button>
      <button class="cls-btn" @click="collapseAll">Collapse all</button>
    </div>
  </div>

  <div v-if="results.length === 0" class="cls-no-results">
    No classes match <strong>{{ query }}</strong>.
  </div>

  <div class="cls-list">
    <div
      v-for="cls in results"
      :key="cls.name"
      class="cls-card"
    >
      <!-- Header row — always visible, click to toggle -->
      <div class="cls-header" @click="toggle(cls.name)">
        <div class="cls-header-left">
          <span class="cls-chevron">{{ isExpanded(cls.name) ? '▾' : '▸' }}</span>
          <span class="cls-name" v-html="hl(cls.name)" />
          <span class="cls-inheritance">
            <template v-for="(part, i) in inheritanceChains[cls.name]" :key="i">
              <span :class="part === cls.name ? 'cls-inherit-self' : 'cls-inherit-part'">{{ part }}</span>
              <span v-if="i < inheritanceChains[cls.name].length - 1" class="cls-inherit-arrow"> → </span>
            </template>
          </span>
        </div>
        <div class="cls-header-right">
          <span v-if="cls.methods.length" class="cls-badge cls-badge--method">
            {{ cls.methods.length }} method{{ cls.methods.length !== 1 ? 's' : '' }}
          </span>
          <span class="cls-badge cls-badge--prop">
            {{ cls.props.length }} prop{{ cls.props.length !== 1 ? 's' : '' }}
          </span>
        </div>
      </div>

      <!-- Class docstring -->
      <div v-if="cls.doc" class="cls-doc" v-html="hl(cls.doc)" />

      <!-- Expanded body -->
      <div v-if="isExpanded(cls.name)" class="cls-body">

        <!-- Methods -->
        <template v-if="cls.methods.length > 0">
          <div class="cls-section-title">Methods</div>
          <div
            v-for="m in cls.methods"
            :key="m.name"
            class="cls-method"
          >
            <code class="cls-method-sig" v-html="hl(m.sig)" />
            <p v-if="m.doc" class="cls-method-doc" v-html="hl(m.doc)" />
          </div>
        </template>

        <!-- Properties -->
        <template v-if="cls.props.length > 0">
          <div class="cls-section-title">Properties</div>
          <table class="cls-prop-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Key</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in cls.props" :key="p.name">
                <td><span class="cls-prop-name" v-html="hl(p.name)" /></td>
                <td><span class="cls-prop-type" v-html="hl(p.type)" /></td>
                <td>
                  <span v-if="p.key" class="cls-prop-key" v-html="hl(p.key)" />
                  <span v-else class="cls-no-key">—</span>
                </td>
                <td><span class="cls-prop-desc" v-html="hl(p.doc)" /></td>
              </tr>
            </tbody>
          </table>
        </template>

      </div>
    </div>
  </div>
</template>

<style scoped>
/* mark is injected via v-html so scoped hashing doesn't reach it.
   Target it through the stable wrapper class instead. */
.cls-list :deep(mark) {
  background: rgba(245, 197, 66, 0.15);
  color: inherit;
  border-radius: 2px;
  padding: 0 2px;
  text-decoration: underline;
  text-decoration-color: rgba(245, 197, 66, 0.45);
  text-underline-offset: 2px;
}

/* ── Toolbar ──────────────────────────────────────────────────────── */

.cls-toolbar {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  margin-bottom: 1.4rem;
}

.cls-search-input {
  width: 100%;
  padding: 0.6em 1em;
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-1);
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s;
}

.cls-search-input:focus {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 2px var(--vp-c-brand-soft);
}

.cls-toolbar-right {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.cls-count {
  font-size: 0.82rem;
  color: var(--vp-c-text-3);
  margin-right: auto;
}

.cls-btn {
  font-size: 0.8rem;
  padding: 0.25em 0.8em;
  border-radius: 6px;
  border: 1px solid var(--vp-c-divider);
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;
}

.cls-btn:hover {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
}

.cls-no-results {
  text-align: center;
  color: var(--vp-c-text-3);
  padding: 2rem;
}

/* ── Card ─────────────────────────────────────────────────────────── */

.cls-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.cls-card {
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s;
  background: var(--vp-c-bg);
}

.cls-card:hover {
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 1px var(--vp-c-brand-soft);
}

/* ── Header ───────────────────────────────────────────────────────── */

.cls-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.7rem 1rem;
  cursor: pointer;
  user-select: none;
  gap: 0.8rem;
}

.cls-header:hover {
  background: var(--vp-c-bg-soft);
}

.cls-header-left {
  display: flex;
  align-items: center;
  gap: 0.55rem;
  flex-wrap: wrap;
  min-width: 0;
}

.cls-header-right {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-shrink: 0;
}

.cls-chevron {
  color: var(--vp-c-brand-1);
  font-size: 0.85rem;
  width: 1em;
  flex-shrink: 0;
}

.cls-name {
  font-family: var(--vp-font-family-mono);
  font-weight: 700;
  font-size: 1rem;
  color: var(--vp-c-brand-1);
}

.cls-inheritance {
  font-size: 0.78rem;
  color: var(--vp-c-text-3);
}

.cls-inherit-part {
  color: var(--vp-c-text-3);
}

.cls-inherit-self {
  color: var(--vp-c-accent);
  font-weight: 600;
}

.cls-inherit-arrow {
  opacity: 0.5;
}

.cls-badge {
  font-size: 0.72rem;
  padding: 0.18em 0.55em;
  border-radius: 99px;
  font-weight: 600;
  white-space: nowrap;
}

.cls-badge--prop {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-2);
}

.cls-badge--method {
  background: var(--vp-c-accent-soft);
  color: var(--vp-c-accent);
}

/* ── Docstring ────────────────────────────────────────────────────── */

.cls-doc {
  padding: 0.5rem 1rem 0.6rem 2.55rem;
  font-size: 0.87rem;
  color: var(--vp-c-text-2);
  border-top: 1px solid var(--vp-c-divider);
}

/* ── Expanded body ────────────────────────────────────────────────── */

.cls-body {
  border-top: 1px solid var(--vp-c-divider);
  padding: 0.8rem 1rem 1rem;
}

.cls-section-title {
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--vp-c-text-3);
  margin: 1rem 0 0.5rem;
}

.cls-section-title:first-child {
  margin-top: 0;
}

/* ── Methods ──────────────────────────────────────────────────────── */

.cls-method {
  margin-bottom: 0.8rem;
  padding: 0.55rem 0.8rem;
  border-radius: 8px;
  background: var(--vp-c-bg-soft);
  border: 1px solid var(--vp-c-divider);
}

.cls-method-sig {
  display: block;
  font-family: var(--vp-font-family-mono);
  font-size: 0.85rem;
  color: var(--vp-c-accent);
  background: transparent;
  padding: 0;
  white-space: pre-wrap;
  word-break: break-all;
}

.cls-method-doc {
  margin: 0.4rem 0 0;
  font-size: 0.85rem;
  color: var(--vp-c-text-2);
}

/* ── Properties table ─────────────────────────────────────────────── */

.cls-prop-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
}

.cls-prop-table th {
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-brand-1);
  font-weight: 600;
  padding: 0.55em 0.9em;
  text-align: left;
  position: sticky;
  top: 0;
  z-index: 1;
}

.cls-prop-table td {
  padding: 0.45em 0.9em;
  border-top: 1px solid var(--vp-c-divider);
  vertical-align: top;
}

.cls-prop-table tr:hover td {
  background: var(--vp-c-bg-soft);
}

.cls-prop-name {
  font-family: var(--vp-font-family-mono);
  color: var(--vp-c-text-1);
  font-weight: 500;
}

.cls-prop-type {
  font-family: var(--vp-font-family-mono);
  color: var(--vp-c-brand-1);
  font-size: 0.82rem;
}

.cls-prop-key {
  font-family: var(--vp-font-family-mono);
  color: var(--vp-c-accent);
  font-weight: 500;
}

.cls-prop-desc {
  color: var(--vp-c-text-2);
  font-size: 0.85rem;
}

.cls-no-key {
  color: var(--vp-c-text-3);
}

.cls-empty {
  color: var(--vp-c-text-3);
  font-size: 0.85rem;
  font-style: italic;
  padding: 0.4rem 0;
}
</style>