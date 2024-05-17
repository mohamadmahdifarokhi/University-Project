<script setup lang="ts">
import '~/assets/css/apexcharts.css'
import { watch, ref, onMounted } from 'vue'

// Props definition
const props = defineProps<{
  type: string
  height: number
  width?: number
  series: any[]
  options?: Record<string, any>
}>()

const { LazyApexCharts, isLoaded } = useLazyApexCharts()
const target = ref(null)
const targetIsVisible = ref(false)
const chartKey = ref(0) // Key to force re-render

// Watch for changes in series and options props
watch(
  () => props.series,
  () => {
    // Increment the key to force re-render
    chartKey.value += 1
  },
  { deep: true }
)

watch(
  () => props.options,
  () => {
    // Increment the key to force re-render
    chartKey.value += 1
  },
  { deep: true }
)

// When the target is visible on viewport, load the chart
const { stop } = useIntersectionObserver(target, ([{ isIntersecting }]) => {
  if (isIntersecting) {
    targetIsVisible.value = isIntersecting
    stop()
  }
})

// Log the data for debugging purposes
onMounted(() => {
  console.log('Series:', props.series)
  console.log('Options:', props.options)
})

</script>

<template>
  <div ref="target">
    <BasePlaceload
      v-if="!isLoaded && !targetIsVisible"
      class="m-4 w-[calc(100%-32px)]"
      :style="{ height: `${height - 32}px` }"
    />
    <ClientOnly>
      <LazyApexCharts
        v-if="targetIsVisible"
        v-show="isLoaded"
        v-bind="props"
        :key="chartKey" <!-- Force re-render on key change -->
      />
      <BasePlaceload
        v-else
        class="m-4 w-[calc(100%-32px)]"
        :style="{ height: `${height - 32}px` }"
      />
    </ClientOnly>
  </div>
</template>

