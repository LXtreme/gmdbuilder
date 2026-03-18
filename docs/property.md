# Property Reference

Search all 500+ object property keys by name or key string. Click any row to copy the key to your clipboard.

<script setup>
import { ref, computed } from 'vue'
import propData from './propdata.json'

const query = ref('')

const results = computed(() => {
  const q = query.value.trim().toLowerCase()
  if (!q) return propData
  return propData.filter(entry =>
    entry.key.toLowerCase().includes(q) ||
    entry.names.some(n => n.toLowerCase().includes(q)) ||
    entry.type.toLowerCase().includes(q)
  )
})

const copied = ref('')

function copyKey(key) {
  navigator.clipboard?.writeText(key)
  copied.value = key
  setTimeout(() => { copied.value = '' }, 1200)
}
</script>

<input
  v-model="query"
  class="prop-search-input"
  placeholder="Search by name (DURATION, TARGET_ID…) or key (a10, a51…)"
  spellcheck="false"
  autocomplete="off"
/>

<div v-if="results.length === 0" class="prop-no-results">
  No properties match <strong>{{ query }}</strong>.
</div>

<table v-else class="prop-table">
  <thead>
    <tr>
      <th>Key</th>
      <th>Type</th>
      <th>Property names</th>
    </tr>
  </thead>
  <tbody>
    <tr
      v-for="entry in results"
      :key="entry.key"
      @click="copyKey(entry.key)"
      :title="copied === entry.key ? 'Copied!' : 'Click to copy key'"
      style="cursor: pointer"
    >
      <td>
        <span class="prop-key">
          {{ copied === entry.key ? '✓ copied' : entry.key }}
        </span>
      </td>
      <td><span class="prop-type">{{ entry.type }}</span></td>
      <td><span class="prop-names">{{ entry.names.join(', ') }}</span></td>
    </tr>
  </tbody>
</table>

<p style="margin-top: 1rem; font-size: 0.82rem; color: var(--vp-c-text-3)">
  Showing {{ results.length }} of {{ propData.length }} properties.
</p>