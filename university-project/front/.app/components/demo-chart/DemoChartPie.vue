<script setup lang="ts">
const demoPie = reactive(useDemoPie())

function useDemoPie() {
  const { primary, info, success, warning, danger } = useTailwindColors()
  const height = 335
  const type = 'pie'

  const options = {
    dataLabels: {
      style: {
        fontSize: '12px',
        weight: 500,
      },
    },
    colors: [primary.value, success.value, info.value, danger.value],
    labels: ['Spring' , 'Autumn', 'Fall','Winter'],
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: {
            width: 315,
            toolbar: {
              show: false,
            },
          },
          legend: {
            position: 'top',
          },
        },
      },
    ],
    legend: {
      position: 'right',
      horizontalAlign: 'center',
    },
  }

  const series = shallowRef([50, 20, 10, 20])

  return {
    type,
    height,
    options,
    series,
  }
}
</script>

<template>
  <div class="relative">
    <BaseCard class="p-6">
      <BaseHeading
          as="h3"
          size="md"
          weight="semibold"
          lead="tight"
          class="text-muted-800 dark:text-white"
        >
          <span>Seasonal Consumption</span>
        </BaseHeading>
      <AddonApexcharts v-bind="demoPie" />
    </BaseCard>
  </div>
</template>
