<script setup lang="ts">
definePageMeta({
  title: 'Activity',
  middleware: ['authenticated'],
  preview: {
    title: 'Personal dashboard v1',
    description: 'For personal usage and reports',
    categories: ['dashboards'],
    src: '/img/screens/dashboards-personal-1.png',
    srcDark: '/img/screens/dashboards-personal-1-dark.png',
    order: 1,
  },
})

const areaCustomers = reactive(useAreaCustomers())
const radialBarTeam = reactive(useRadialBarTeam())
const barProfit = reactive(useBarProfit())

function useAreaCustomers() {
  const {primary, info, success} = useTailwindColors()
  const type = 'area'
  const height = 258

  const options = {
    chart: {
      toolbar: {
        show: false,
      },
    },
    colors: [primary.value, info.value, success.value],
    title: {
      show: false,
      text: undefined,
      align: 'left',
    },
    legend: {
      show: true,
      position: 'top',
    },
    dataLabels: {
      enabled: false,
    },
    stroke: {
      width: [2, 2, 2],
      curve: 'smooth',
    },
    xaxis: {
      type: 'datetime',
      categories: [
        '2020-09-19T00:00:00.000Z',
        '2020-09-25T01:30:00.000Z',
        '2020-09-29T02:30:00.000Z',
        '2020-10-07T03:30:00.000Z',
        '2020-10-12T04:30:00.000Z',
        '2020-10-24T05:30:00.000Z',
        '2020-10-25T06:30:00.000Z',
      ],
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm',
      },
    },
  }

  const series = shallowRef([
    {
      name: 'Iron',
      data: [31, 40, 28, 51, 42, 109, 100],
    },
    {
      name: 'Refrigerator',
      data: [11, 32, 45, 32, 34, 52, 41],
    },
    {
      name: 'Oven',
      data: [78, 53, 36, 10, 14, 5, 2],
    },
  ])

  return {
    type,
    height,
    options,
    series,
  }
}

function useRadialBarTeam() {
  const {primary} = useTailwindColors()
  const type = 'radialBar'
  const height = 455

  const options = {
    title: {
      text: undefined,
    },
    chart: {
      sparkline: {
        enabled: true,
      },
      toolbar: {
        show: false,
      },
    },
    colors: [primary.value],
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: {
          background: '#e7e7e7',
          strokeWidth: '97%',
          margin: 5, // margin is in pixels
          dropShadow: {
            enabled: false,
            top: 2,
            left: 0,
            color: '#999',
            opacity: 1,
            blur: 2,
          },
        },
        hollow: {
          margin: 0,
          size: '40%',
        },
        dataLabels: {
          name: {
            show: false,
          },
          value: {
            offsetY: -2,
            fontSize: '22px',
          },
        },
      },
    },
    grid: {
      padding: {
        top: 80,
      },
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'light',
        shadeIntensity: 0.1,
        inverseColors: false,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 50, 53, 91],
      },
    },
    labels: ['Average Results'],
  }

  const series = shallowRef([76])

  return {
    type,
    height,
    options,
    series,
  }
}

function useBarProfit() {
  const {primary} = useTailwindColors()
  const type = 'bar'
  const height = 255

  const options = {
    chart: {
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      bar: {
        dataLabels: {
          position: 'top', // top, center, bottom
        },
      },
    },
    dataLabels: {
      enabled: true,
      formatter: function (val: string) {
        return val + '%'
      },
      offsetY: -20,
      style: {
        fontSize: '12px',
        colors: ['#304758'],
      },
    },
    xaxis: {
      categories: ['May', 'Jun', 'Jul', 'Aug', 'Sep'],
      position: 'top',
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      crosshairs: {
        fill: {
          type: 'gradient',
          gradient: {
            colorFrom: '#D8E3F0',
            colorTo: '#BED1E6',
            stops: [0, 100],
            opacityFrom: 0.4,
            opacityTo: 0.5,
          },
        },
      },
      tooltip: {
        enabled: true,
      },
    },
    yaxis: {
      axisBorder: {
        show: false,
      },
      axisTicks: {
        show: false,
      },
      labels: {
        show: false,
        formatter: function (val: string) {
          return val + '%'
        },
      },
    },
    colors: [primary.value],
    title: {
      text: undefined,
      align: 'left',
    },
  }

  const series = shallowRef([
    {
      name: 'Ratio',
      data: [2.3, 3.1, 4.0, 10.1, 4.0],
    },
  ])

  return {
    type,
    height,
    options,
    series,
  }
}
</script>

<template>
  <div>
    <!-- Header -->
    <!--    <div class="mb-8 flex flex-col justify-between md:flex-row md:items-center">-->
    <!--      <div-->
    <!--        class="ltablet:max-w-full flex max-w-[425px] flex-col items-center gap-4 text-center md:flex-row md:text-left lg:max-w-full"-->
    <!--      >-->
    <!--        <BaseAvatar src="/img/avatars/2.svg" size="lg" />-->
    <!--        <div>-->
    <!--          <BaseHeading-->
    <!--            as="h2"-->
    <!--            size="xl"-->
    <!--            weight="light"-->
    <!--            lead="tight"-->
    <!--            class="text-muted-800 dark:text-white"-->
    <!--          >-->
    <!--            <span>Welcome back, Maya</span>-->
    <!--          </BaseHeading>-->
    <!--          <BaseParagraph>-->
    <!--            <span class="text-muted-500">-->
    <!--              Happy to see you again on your dashboard.-->
    <!--            </span>-->
    <!--          </BaseParagraph>-->
    <!--        </div>-->
    <!--      </div>-->
    <!--      <div-->
    <!--        class="mt-4 flex items-center justify-center gap-2 md:mt-0 md:justify-start"-->
    <!--      >-->
    <!--        <BaseButton>-->
    <!--          <span>View Reports</span>-->
    <!--        </BaseButton>-->
    <!--        <BaseButton color="primary">-->
    <!--          <span>Manage Store</span>-->
    <!--        </BaseButton>-->
    <!--      </div>-->
    <!--    </div>-->
    <!-- Grid -->
    <div class="grid grid-cols-12 gap-6">
      <!-- Quick stats -->
      <!--      <div class="ltablet:col-span-6 col-span-12 lg:col-span-6">-->
      <!--        <BaseCard class="p-6">-->
      <!--          <div class="mb-6">-->
      <!--            <BaseHeading-->
      <!--              as="h3"-->
      <!--              size="md"-->
      <!--              weight="semibold"-->
      <!--              lead="tight"-->
      <!--              class="text-muted-800 dark:text-white"-->
      <!--            >-->
      <!--              <span>Your Quick Stats</span>-->
      <!--            </BaseHeading>-->
      <!--          </div>-->
      <!--          <div class="grid gap-4 md:grid-cols-2">-->
      <!--            &lt;!&ndash; Grid item &ndash;&gt;-->
      <!--            <div-->
      <!--              class="bg-muted-100/80 dark:bg-muted-700 flex items-center gap-2 rounded-md px-5 py-10"-->
      <!--            >-->
      <!--              <BaseIconBox-->
      <!--                size="md"-->
      <!--                class="bg-primary-100 text-primary-500 dark:bg-primary-500/20 dark:text-primary-400 dark:border-primary-500 dark:border-2"-->
      <!--                rounded="full"-->
      <!--                color="none"-->
      <!--              >-->
      <!--                <Icon name="ph:nut-duotone" class="size-5" />-->
      <!--              </BaseIconBox>-->
      <!--              <div>-->
      <!--                <BaseHeading-->
      <!--                  as="h2"-->
      <!--                  size="md"-->
      <!--                  weight="semibold"-->
      <!--                  lead="tight"-->
      <!--                  class="text-muted-800 dark:text-white"-->
      <!--                >-->
      <!--                  <span>2,870</span>-->
      <!--                </BaseHeading>-->
      <!--                <BaseParagraph size="sm">-->
      <!--                  <span class="text-muted-500 dark:text-muted-400">-->
      <!--                    Sales this month-->
      <!--                  </span>-->
      <!--                </BaseParagraph>-->
      <!--              </div>-->
      <!--            </div>-->
      <!--            &lt;!&ndash; Grid item &ndash;&gt;-->
      <!--            <div-->
      <!--              class="bg-muted-100/80 dark:bg-muted-700 flex items-center gap-2 rounded-md px-5 py-10"-->
      <!--            >-->
      <!--              <BaseIconBox-->
      <!--                size="md"-->
      <!--                class="bg-amber-100 text-amber-500 dark:border-2 dark:border-amber-500 dark:bg-amber-500/20 dark:text-amber-400"-->
      <!--                rounded="full"-->
      <!--                color="none"-->
      <!--              >-->
      <!--                <Icon name="ph:handshake-duotone" class="size-5" />-->
      <!--              </BaseIconBox>-->
      <!--              <div>-->
      <!--                <BaseHeading-->
      <!--                  as="h2"-->
      <!--                  size="md"-->
      <!--                  weight="semibold"-->
      <!--                  lead="tight"-->
      <!--                  class="text-muted-800 dark:text-white"-->
      <!--                >-->
      <!--                  <span>159</span>-->
      <!--                </BaseHeading>-->
      <!--                <BaseParagraph size="sm">-->
      <!--                  <span class="text-muted-500 dark:text-muted-400">-->
      <!--                    New users-->
      <!--                  </span>-->
      <!--                </BaseParagraph>-->
      <!--              </div>-->
      <!--            </div>-->
      <!--            &lt;!&ndash; Grid item &ndash;&gt;-->
      <!--            <div-->
      <!--              class="bg-muted-100/80 dark:bg-muted-700 flex items-center gap-2 rounded-md px-5 py-10"-->
      <!--            >-->
      <!--              <BaseIconBox-->
      <!--                size="md"-->
      <!--                class="bg-green-100 text-green-500 dark:border-2 dark:border-green-500 dark:bg-green-500/20 dark:text-green-400"-->
      <!--                rounded="full"-->
      <!--                color="none"-->
      <!--              >-->
      <!--                <Icon name="ph:sketch-logo-duotone" class="size-5" />-->
      <!--              </BaseIconBox>-->
      <!--              <div>-->
      <!--                <BaseHeading-->
      <!--                  as="h2"-->
      <!--                  size="md"-->
      <!--                  weight="semibold"-->
      <!--                  lead="tight"-->
      <!--                  class="text-muted-800 dark:text-white"-->
      <!--                >-->
      <!--                  <span>$429.18</span>-->
      <!--                </BaseHeading>-->
      <!--                <BaseParagraph size="sm">-->
      <!--                  <span class="text-muted-500 dark:text-muted-400">-->
      <!--                    Earned today-->
      <!--                  </span>-->
      <!--                </BaseParagraph>-->
      <!--              </div>-->
      <!--            </div>-->
      <!--            &lt;!&ndash; Grid item &ndash;&gt;-->
      <!--            <div-->
      <!--              class="bg-muted-100/80 dark:bg-muted-700 flex items-center gap-2 rounded-md px-5 py-10"-->
      <!--            >-->
      <!--              <BaseIconBox-->
      <!--                size="md"-->
      <!--                class="bg-indigo-100 text-indigo-500 dark:border-2 dark:border-indigo-500 dark:bg-indigo-500/20 dark:text-indigo-400"-->
      <!--                rounded="full"-->
      <!--                color="none"-->
      <!--              >-->
      <!--                <Icon name="ph:bank-duotone" class="size-5" />-->
      <!--              </BaseIconBox>-->
      <!--              <div>-->
      <!--                <BaseHeading-->
      <!--                  as="h2"-->
      <!--                  size="md"-->
      <!--                  weight="semibold"-->
      <!--                  lead="tight"-->
      <!--                  class="text-muted-800 dark:text-white"-->
      <!--                >-->
      <!--                  <span>$6816.32</span>-->
      <!--                </BaseHeading>-->
      <!--                <BaseParagraph size="sm">-->
      <!--                  <span class="text-muted-500 dark:text-muted-400">-->
      <!--                    Total balance-->
      <!--                  </span>-->
      <!--                </BaseParagraph>-->
      <!--              </div>-->
      <!--            </div>-->
      <!--          </div>-->
      <!--        </BaseCard>-->
      <!--      </div>-->
      <div class="col-span-12 md:col-span-4">
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>Saved Energy</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-success-100 text-success-500 dark:bg-success-500/20 dark:text-success-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <Icon name="ri:battery-saver-fill" class="size-6"/>
            </BaseIconBox>
          </div>
          <div class="mb-2">
            <BaseHeading
              as="h4"
              size="3xl"
              weight="bold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>7,549</span>
            </BaseHeading>
          </div>
          <div
            class="text-success-500 flex items-center gap-1 font-sans text-sm"
          >
            <!--            <span>+7.8%</span>-->
            <!--            <Icon name="lucide:trending-up" class="size-5"/>-->
            <!--            <span class="text-muted-400 text-xs">since last month</span>-->
          </div>
        </BaseCard>
      </div>
      <!-- Stat tile -->
      <div class="col-span-12 md:col-span-4">
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>Sold Energy</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-yellow-500 dark:border-2 dark:border-yellow-500 dark:bg-yellow-500/20 dark:text-yellow-400"
              rounded="full"
              color="none"
            >
              <Icon name="ri:money-dollar-circle-fill" class="size-6"/>
            </BaseIconBox>
          </div>
          <div class="mb-2">
            <BaseHeading
              as="h4"
              size="3xl"
              weight="bold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>1,611</span>
            </BaseHeading>
          </div>
          <div
            class="text-danger-500 flex items-center gap-1 font-sans text-sm"
          >
            <!--            <span>-2.7%</span>-->
            <!--            <Icon name="lucide:trending-down" class="size-5"/>-->
            <!--            <span class="text-muted-400 text-xs">going down</span>-->
          </div>
        </BaseCard>
      </div>
      <!-- Stat tile -->
      <div class="col-span-12 md:col-span-4">
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>Remain Energy</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-primary-100 text-primary-500 dark:bg-primary-500/20 dark:text-primary-400 dark:border-primary-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <Icon name="ri:leaf-fill" class="size-6"/>

              <!--              <Icon name="ph:megaphone-simple-duotone" class="size-5"/>-->
            </BaseIconBox>
          </div>
          <div class="mb-2">
            <BaseHeading
              as="h4"
              size="3xl"
              weight="bold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>862</span>
            </BaseHeading>
          </div>
          <div
            class="text-success-500 flex items-center gap-1 font-sans text-sm"
          >
            <!--            <span>+4.5%</span>-->
            <!--            <Icon name="lucide:trending-up" class="size-5"/>-->
            <!--            <span class="text-muted-400 text-xs">going up</span>-->
          </div>
        </BaseCard>
      </div>
      <!-- Area Chart card -->
      <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">
        <BaseCard class="p-6">
          <!-- Title -->
          <div class="mb-6">
            <BaseHeading
              as="h3"
              size="md"
              weight="semibold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>Products</span>
            </BaseHeading>
          </div>
          <AddonApexcharts v-bind="areaCustomers" class="-ms-4"/>
        </BaseCard>
      </div>
      <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">
        <BaseCard class="p-6">
          <!-- Title -->
          <div class="mb-6">
            <BaseHeading
              as="h3"
              size="md"
              weight="semibold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>AC To DC</span>
            </BaseHeading>
          </div>
          <AddonApexcharts v-bind="areaCustomers" class="-ms-4"/>
        </BaseCard>
      </div>
      <!-- CTA card -->
      <!--      <div-->
      <!--        class="ptablet:col-span-6 ltablet:col-span-4 col-span-12 lg:col-span-4"-->
      <!--      >-->
      <!--        <BaseCard-->
      <!--          class="from-primary-600 to-primary-700 relative flex h-full items-center justify-center bg-gradient-to-br p-6"-->
      <!--        >-->
      <!--          <div class="relative z-20 flex flex-col gap-3 py-10 text-center">-->
      <!--            <BaseHeading-->
      <!--              as="h4"-->
      <!--              size="lg"-->
      <!--              weight="semibold"-->
      <!--              lead="tight"-->
      <!--              class="text-white"-->
      <!--            >-->
      <!--              <span>Hey Maya, you're doing great.</span>-->
      <!--            </BaseHeading>-->
      <!--            <BaseParagraph size="md" class="mx-auto max-w-[280px]">-->
      <!--              <span class="text-white/80">-->
      <!--                Start using our team and project management tools-->
      <!--              </span>-->
      <!--            </BaseParagraph>-->
      <!--            <NuxtLink-->
      <!--              class="font-sans text-white underline-offset-4 hover:underline"-->
      <!--              to="#"-->
      <!--            >-->
      <!--              Learn More-->
      <!--            </NuxtLink>-->
      <!--          </div>-->
      <!--          <div-->
      <!--            class="absolute bottom-4 end-4 z-10 flex size-14 items-center justify-center"-->
      <!--          >-->
      <!--            <Icon-->
      <!--              name="ph:crown-duotone"-->
      <!--              class="text-primary-900/50 size-14"-->
      <!--            />-->
      <!--          </div>-->
      <!--        </BaseCard>-->
      <!--      </div>-->
      <!-- Radial Bar card -->
      <!--      <div-->
      <!--        class="ptablet:col-span-6 ltablet:col-span-4 col-span-12 lg:col-span-4"-->
      <!--      >-->
      <!--        <BaseCard class="relative p-6">-->
      <!--          <div class="mb-6">-->
      <!--            <BaseHeading-->
      <!--              as="h3"-->
      <!--              size="md"-->
      <!--              weight="semibold"-->
      <!--              lead="tight"-->
      <!--              class="text-muted-800 dark:text-white"-->
      <!--            >-->
      <!--              <span>Team Efficiency</span>-->
      <!--            </BaseHeading>-->
      <!--          </div>-->
      <!--          <div-->
      <!--            class="absolute inset-x-0 top-24 flex items-center justify-center gap-4"-->
      <!--          >-->
      <!--            <BaseAvatar src="/img/avatars/4.svg" />-->
      <!--            <BaseAvatar-->
      <!--              text="H"-->
      <!--              class="bg-yellow-100 text-yellow-500 dark:bg-yellow-500 dark:text-white"-->
      <!--            />-->
      <!--            <BaseAvatar src="/img/avatars/3.svg" />-->
      <!--          </div>-->
      <!--          <AddonApexcharts v-bind="radialBarTeam" />-->
      <!--        </BaseCard>-->
      <!--      </div>-->
      <!-- Bar chart card -->
      <!--      <div class="ltablet:col-span-4 col-span-12 lg:col-span-4">-->
      <!--        <BaseCard class="relative p-6">-->
      <!--          <div class="mb-6">-->
      <!--            <BaseHeading-->
      <!--              as="h3"-->
      <!--              size="md"-->
      <!--              weight="semibold"-->
      <!--              lead="tight"-->
      <!--              class="text-muted-800 dark:text-white"-->
      <!--            >-->
      <!--              <span>Profit Evolution</span>-->
      <!--            </BaseHeading>-->
      <!--          </div>-->
      <!--          <AddonApexcharts v-bind="barProfit" />-->
      <!--        </BaseCard>-->
      <!--      </div>-->

      <div class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">
        <BaseCard rounded="lg" class="p-6">
          <div class="mb-6 flex items-center justify-between">
            <BaseHeading
              as="h3"
              size="md"
              weight="semibold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>Selected Products</span>
            </BaseHeading>
            <!--            <NuxtLink-->
            <!--              to="#"-->
            <!--              class="bg-muted-100 hover:bg-muted-200 dark:bg-muted-700 dark:hover:bg-muted-900 text-primary-500 rounded-lg px-4 py-2 font-sans text-sm font-medium underline-offset-4 transition-colors duration-300 hover:underline"-->
            <!--            >-->
            <!--              View All-->
            <!--            </NuxtLink>-->
          </div>
          <div class="mb-2 space-y-5">
            <!-- List item -->
            <div class="flex items-center gap-2">
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-blue-800 text-white shadow-xl shadow-blue-500/20 dark:shadow-blue-800/20"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa6-brands:linkedin-in" class="size-3"/>-->
<!--              </BaseIconBox>-->
              <div>
                <BaseHeading
                  as="h4"
                  size="sm"
                  weight="medium"
                  lead="snug"
                  class="text-muted-800 dark:text-white"
                >
                  <span>Iron</span>
                </BaseHeading>

              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              type="date"

              shape="curved"
              placeholder="Start Date"
              icon="ri:calendar-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              type="date"

              shape="curved"
              placeholder="End Date"
              icon="ri:calendar-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              shape="curved"
              placeholder="Consumption"
              icon="ri:lightbulb-flash-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:add-circle-fill"/>
                </BaseButtonIcon>
              </div>
              <div class="ms-auto flex items-center gap-1">
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:delete-bin-7-fill"/>
                </BaseButtonIcon>
              </div>
            </div>
            <!-- List item -->
            <div class="flex items-center gap-2">
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-muted-900 dark:bg-muted-100 dark:text-muted-800 text-white"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa6-brands:github" class="size-3"/>-->
<!--              </BaseIconBox>-->
              <div>
                <BaseHeading
                  as="h4"
                  size="sm"
                  weight="medium"
                  lead="snug"
                  class="text-muted-800 dark:text-white"
                >
                  <span>Refrigerator</span>
                </BaseHeading>
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Github Inc.</span>-->
<!--                </BaseParagraph>-->
              </div>
                            <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              type="date"

              shape="curved"
              placeholder="Start Date"
              icon="ri:calendar-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              type="date"

              shape="curved"
              placeholder="End Date"
              icon="ri:calendar-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              shape="curved"
              placeholder="Consumption"
              icon="ri:lightbulb-flash-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:add-circle-fill"/>
                </BaseButtonIcon>
              </div>
              <div class="ms-auto flex items-center gap-1">
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:delete-bin-7-fill"/>
                </BaseButtonIcon>
                <!--                <Icon-->
                <!--                  name="ph:check-circle-duotone"-->
                <!--                  class="text-success-500 size-4"-->
                <!--                />-->
                <!--                <span-->
                <!--                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"-->
                <!--                >-->
                <!--                  $1,478.32-->
                <!--                </span>-->
              </div>

            </div>
            <!-- List item -->
            <div class="flex items-center gap-2">
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-rose-500 text-white shadow-xl shadow-rose-500/20 dark:shadow-rose-800/20"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa6-brands:invision" class="size-4"/>-->
<!--              </BaseIconBox>-->
              <div>
                <BaseHeading
                  as="h4"
                  size="sm"
                  weight="medium"
                  lead="snug"
                  class="text-muted-800 dark:text-white"
                >
                  <span>Oven</span>
                </BaseHeading>
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Invision Corp.</span>-->
<!--                </BaseParagraph>-->
              </div>
                            <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              type="date"

              shape="curved"
              placeholder="Start Date"
              icon="ri:calendar-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              type="date"

              shape="curved"
              placeholder="End Date"
              icon="ri:calendar-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseInput
              shape="curved"
              placeholder="Consumption"
              icon="ri:lightbulb-flash-fill"
            />
              </div>
              <div class="ms-auto flex items-center gap-1">
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:add-circle-fill"/>
                </BaseButtonIcon>
              </div>
              <div class="ms-auto flex items-center gap-1">
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:delete-bin-7-fill"/>
                </BaseButtonIcon>
                <!--                <Icon-->
                <!--                  name="ph:check-circle-duotone"-->
                <!--                  class="text-success-500 size-4"-->
                <!--                />-->
                <!--                <span-->
                <!--                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"-->
                <!--                >-->
                <!--                  $1,478.32-->
                <!--                </span>-->
              </div>

            </div>

          </div>
        </BaseCard>
      </div>


    </div>
  </div>
</template>
