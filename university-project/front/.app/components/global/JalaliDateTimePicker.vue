<script setup lang="ts">
import { ref, computed, watch } from 'vue'

const props = defineProps<{
  modelValue?: string
  placeholder?: string
  error?: string
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const now = new Date()
const initJ = gregorianToJalaali(now.getFullYear(), now.getMonth() + 1, now.getDate())

const jYear = ref<number>(initJ.jy)
const jMonth = ref<number>(initJ.jm)
const jDay = ref<number>(initJ.jd)
const hour = ref<number>(now.getHours())
const minute = ref<number>(0)

// Reasonable year range around the current Jalali year.
const years = computed(() => {
  const list: number[] = []
  for (let y = initJ.jy - 3; y <= initJ.jy + 1; y += 1) list.push(y)
  return list
})

const days = computed(() => {
  const len = jalaliMonthLength(jYear.value, jMonth.value)
  return Array.from({ length: len }, (_, i) => i + 1)
})

const hours = Array.from({ length: 24 }, (_, i) => i)
const minutes = [0, 15, 30, 45]

// Keep day in range when month/year changes.
watch([jYear, jMonth], () => {
  const len = jalaliMonthLength(jYear.value, jMonth.value)
  if (jDay.value > len) jDay.value = len
})

// Emit an ISO-like local datetime string ("YYYY-MM-DDTHH:mm") that the
// backend understands, converted from the chosen Jalali date.
function emitValue() {
  const g = jalaaliToGregorian(jYear.value, jMonth.value, jDay.value)
  const pad = (n: number) => String(n).padStart(2, '0')
  const iso = `${g.gy}-${pad(g.gm)}-${pad(g.gd)}T${pad(hour.value)}:${pad(minute.value)}`
  emit('update:modelValue', iso)
}

watch([jYear, jMonth, jDay, hour, minute], emitValue, { immediate: true })

const monthLabels = JALALI_MONTHS
</script>

<template>
  <div>
    <p v-if="placeholder" class="text-muted-400 mb-1 text-xs">{{ placeholder }}</p>
    <div class="flex flex-wrap gap-2">
      <BaseSelect v-model.number="jYear" shape="curved" class="min-w-[90px] flex-1">
        <option v-for="y in years" :key="y" :value="y">{{ toPersianDigits(y) }}</option>
      </BaseSelect>
      <BaseSelect v-model.number="jMonth" shape="curved" class="min-w-[110px] flex-1">
        <option v-for="(m, idx) in monthLabels" :key="idx" :value="idx + 1">{{ m }}</option>
      </BaseSelect>
      <BaseSelect v-model.number="jDay" shape="curved" class="min-w-[80px] flex-1">
        <option v-for="d in days" :key="d" :value="d">{{ toPersianDigits(d) }}</option>
      </BaseSelect>
      <BaseSelect v-model.number="hour" shape="curved" class="min-w-[80px] flex-1">
        <option v-for="hh in hours" :key="hh" :value="hh">{{ toPersianDigits(hh) }}</option>
      </BaseSelect>
      <BaseSelect v-model.number="minute" shape="curved" class="min-w-[80px] flex-1">
        <option v-for="mm in minutes" :key="mm" :value="mm">{{ toPersianDigits(mm) }}</option>
      </BaseSelect>
    </div>
    <p v-if="error" class="text-danger-500 mt-1 text-xs">{{ error }}</p>
  </div>
</template>
