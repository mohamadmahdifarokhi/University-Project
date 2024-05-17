<script setup lang="ts">
import {useAppStore} from "~/stores/app";
import {toTypedSchema} from "@vee-validate/zod";
import {Field, useForm} from 'vee-validate'
import {z} from 'zod'
import {storeToRefs} from "pinia";

const {t} = useI18n({useScope: "local"})
const router = useRouter()
// onBeforeUnmount(() => {
//     router.push('/dashboard')
//
//   }
// )

const app = useAppStore();
const {orders, categories24, values24, categoriesMonth, valuesMonth} = storeToRefs(app);
const cate = ref(categories24)

const areaCustomers = reactive(useAreaCustomers())
const radialBarTeam = reactive(useRadialBarTeam())
const barProfit = reactive(useBarProfit())
const fetchselectedDevice = app.fetchselectedDevice;
const fetchOrders = app.fetchOrders;
const fetch24Records = app.fetch24Records;
const fetchMonthRecords = app.fetchMonthRecords;

const initializeData = async () => {
  await fetch24Records();
  await fetchMonthRecords();
  await fetchselectedDevice();
  await fetchOrders();
};

onMounted(() => {
   initializeData();
});



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


const VALIDATION_TEXT = {
  EMAIL_REQUIRED: t('emailRequired'), // Translate email required text
  PASSWORD_REQUIRED: t('passwordRequired'), // Translate password required text
}
const zodSchema = z.object({
  start: z.string(),
  end: z.string(),
  consumption: z.string(),
  deviceId: z.string(),
})

type FormInput = z.infer<typeof zodSchema>;

const validationSchema = toTypedSchema(zodSchema)
const initialValues = computed<FormInput>(() => ({
  start: '',
  end: '',
  consumption: '',
  deviceId: '',
}))
const {
  handleSubmit,
  isSubmitting,
  setFieldError,
  meta,
  values,
  errors,
  resetForm,
  setFieldValue,
  setErrors,
} = useForm({
  validationSchema,
  initialValues,
})

const addPowerRecord = handleSubmit(async (values) => {
  await app.addRecord(values.deviceId, values.start, values.end, values.consumption);
})


function deleteDevice(deviceId) {
  app.deleteDevice(deviceId)
}

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
        '2020-09-19T03:00:00.000Z',
        '2020-09-19T06:00:00.000Z',
        '2020-09-19T09:00:00.000Z',
        '2020-09-19T12:00:00.000Z',
        '2020-09-19T18:00:00.000Z',
        '2020-09-20T00:00:00.000Z',
        // '2020-09-25T01:30:00.000Z',
        // '2020-09-29T02:30:00.000Z',
        // '2020-10-07T03:30:00.000Z',
        // '2020-10-12T04:30:00.000Z',
        // '2020-10-24T05:30:00.000Z',
        // '2020-10-25T06:30:00.000Z',
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

const demoTimeline = reactive(useDemoTimeline())

function useDemoTimeline() {
  const {primary, info, success, warning, danger} = useTailwindColors()
  const type = 'rangeBar'
  const height = 280

  const options = {
    title: {
      text: '',
      align: 'left',
    },
    chart: {
      toolbar: {
        show: false,
      },
    },
    colors: [
      primary.value,
      info.value,
      success.value,
      warning.value,
      danger.value,
    ],
    plotOptions: {
      bar: {
        horizontal: true,
        distributed: true,
        dataLabels: {
          hideOverflowingLabels: false,
        },
      },
    },
    dataLabels: {
      enabled: true,
      formatter: function (val: string, opts: any) {
        const label = opts.w.globals.labels[opts.dataPointIndex]
        const a = val[0]
        const b = val[1]
        const diff = 0
        return label + ': ' + diff + (diff > 1 ? 'D' : 'd')
      },
      style: {
        colors: ['#f3f4f5', '#fff'],
        weight: 400,
      },
    },
    xaxis: {
      type: 'datetime',
    },
    yaxis: {
      show: false,
    },
    grid: {
      row: {
        colors: ['transparent'],
        opacity: 1,
      },
    },
  }

  const series = shallowRef([
    {
      data: [
        {
          x: 'Analysis',
          y: [
            new Date('2019-02-27').getTime(),
            new Date('2019-03-04').getTime(),
          ],
          fillColor: primary.value,
        },
        {
          x: 'Design',
          y: [
            new Date('2019-03-04').getTime(),
            new Date('2019-03-08').getTime(),
          ],
          fillColor: info.value,
        },
        {
          x: 'Coding',
          y: [
            new Date('2019-03-07').getTime(),
            new Date('2019-03-10').getTime(),
          ],
          fillColor: success.value,
        },
        {
          x: 'Testing',
          y: [
            new Date('2019-03-08').getTime(),
            new Date('2019-03-12').getTime(),
          ],
          fillColor: warning.value,
        },
        {
          x: 'Deployment',
          y: [
            new Date('2019-03-12').getTime(),
            new Date('2019-03-17').getTime(),
          ],
          fillColor: danger.value,
        },
      ],
    },
  ])

  return {
    type,
    height,
    options,
    series,
  }
}


const demoBarMulti = reactive(useDemoBarMulti())
const demoBarMulti3 = reactive(useDemoBarMulti3())

function useDemoBarMulti() {
  const { primary, info, success, warning } = useTailwindColors();
  const type = 'bar';
  const height = 280;

  const options = {
    chart: {
      toolbar: {
        show: false,
      },
      events: {
        mounted: function (chartContext, config) {
          window.addEventListener('resize', () => {
            chartContext.updateOptions({
              chart: {
                width: '100%',
              },
            });
          });
        },
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        endingShape: 'rounded',
      },
    },
    colors: [primary.value, success.value, info.value, warning.value],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['transparent'],
    },
    xaxis: {
      categories: categories24.value,
    },
    yaxis: {
      title: {
        text: 'Consumption (kw/h)',
      },
    },
    fill: {
      opacity: 1,
    },
    legend: {
      position: 'top',
      horizontalAlign: 'center',
    },
    title: {
      text: '',
      align: 'left',
    },
  };

  const series = shallowRef([
    {
      name: 'DC',
      data: values24.value,
    },
  ]);

  return {
    type,
    height,
    options,
    series,
  };
}
const demoAreaMulti = reactive(useDemoAreaMulti())

function useDemoAreaMulti() {
  const {primary, info, success} = useTailwindColors()
  const type = 'area'
  const height = 280

  const options = {
    chart: {
      toolbar: {
        show: false,
      },
    },
    colors: [primary.value, info.value, success.value],
    title: {
      text: '',
      align: 'left',
    },
    legend: {
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
      categories: categoriesMonth,
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm',
      },
    },
  }

  const series = shallowRef(valuesMonth)

  return {
    type,
    height,
    options,
    series,
  }
}

function useDemoBarMulti3() {
  const {primary, info, success, warning} = useTailwindColors()
  const type = 'bar'
  const height = 280

  const options = {
    chart: {
      toolbar: {
        show: false,
      },
    },
    plotOptions: {
      bar: {
        horizontal: false,
        columnWidth: '55%',
        endingShape: 'rounded',
      },
    },
    colors: [primary.value, success.value, info.value, warning.value],
    dataLabels: {
      enabled: false,
    },
    stroke: {
      show: true,
      width: 2,
      colors: ['transparent'],
    },
    xaxis: {
      categories: [
        'Spring', 'Autumn', 'Fall', 'Winter'
      ],

    },
    yaxis: {
      title: {
        text: 'Consumption (kw/h)',
      },
    },
    fill: {
      opacity: 1,
    },
    legend: {
      position: 'top',
      horizontalAlign: 'center',
    },
    title: {
      text: '',
      align: 'left',
    },
    // tooltip: {
    //   y: {
    //     formatter: asKDollar,
    //   },
    // },
  }

  const series = shallowRef([
    {
      name: 'non-optimized',
      data: [44, 55, 57, 56],
    },
    {
      name: 'optimized',
      data: [35, 41, 36, 26],
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
      <!--                class="bg-primary-100 text-primary-500 dark:bg-primary-500/20 dark:text-primary-400 dark:border-success-500 dark:border-2"-->
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
              <span>CONVERSION PERCENT (%)</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/exchange-line.png"
                alt=""
              >
              <!--              <Icon name="ri:battery-saver-fill" class="size-6"/>-->
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
              <span>SAVED ENERGY (kwh/day)</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/battery-saver-line.png"
                alt=""
              >
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
              <span>INVESTMENT & SAVING (€)</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/wallet-3-line.png"
                alt=""
              >
              <!--              <Icon name="ri:leaf-fill" class="size-6"/>-->

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
              <span>812</span>
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
              <span>GREENHOUSE EMISSION SAVING (CO2/kwh)</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/battery-saver-line.png"
                alt=""
              >
              <!--              <Icon name="ri:leaf-fill" class="size-6"/>-->

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
              <span>POWER DIVIDED BY AC-DC</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/supabase-fill.png"
                alt=""
              >
              <!--              <Icon name="ri:leaf-fill" class="size-6"/>-->

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
              <span>270</span>
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
              <span>EFFICIENCY (%)</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/speed-up-line.svg"
                alt=""
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
              <span>832</span>
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

      <div class="col-span-12 md:col-span-6">
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>PV GENERATION (kwh)</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/flashlight-line.png"
                alt=""
              >
              <!--              <Icon name="ri:leaf-fill" class="size-6"/>-->

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
              <span>262</span>
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
      <div class="col-span-12 md:col-span-6">
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>STORAGE CAPACITY (kwh)</span>
            </BaseHeading>
            <BaseIconBox
              size="xs"
              class="bg-yellow-100 text-primary-500 dark:bg-yellow-100 dark:text-primary-400 dark:border-success-500 dark:border-2"
              rounded="full"
              color="none"
            >
              <img
                class="size-10 h-7 w-8"
                src="/img/database-line.png"
                alt=""
              >
              <!--              <Icon name="ri:leaf-fill" class="size-6"/>-->

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
              <span>762</span>
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

      <!--  <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">-->
      <!--    <BaseCard class="p-6">-->
      <!--      &lt;!&ndash; Title &ndash;&gt;-->
      <!--      <div class="mb-6">-->
      <!--        <BaseHeading-->
      <!--          as="h3"-->
      <!--          size="md"-->
      <!--          weight="semibold"-->
      <!--          lead="tight"-->
      <!--          class="text-muted-800 dark:text-white"-->
      <!--        >-->
      <!--          <span>Timeline Chart</span>-->
      <!--        </BaseHeading>-->
      <!--      </div>-->
      <!--      <AddonApexcharts v-bind="demoTimeline" />-->
      <!--    </BaseCard>-->
      <!--  </div>-->
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
              <span>Daily Consumption</span>
            </BaseHeading>
          </div>
          <AddonApexcharts v-bind="demoBarMulti"/>
        </BaseCard>
      </div>


<div class="ltablet:col-span-12 col-span-12 lg:col-span-12">
  <div class="relative">
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
          <span>Monthly Consumption</span>
        </BaseHeading>
      </div>

      <AddonApexcharts v-bind="demoAreaMulti" />

      <div class="flex justify-center mt-6">
        <form method="POST" class="items-center" style="max-width: 300px" action="" @submit.prevent="addPowerRecord" novalidate>
          <!-- Apartment selection -->
          <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-4" name="apartment">
            <BaseSelect
              :model-value="field.value"
              :error="errorMessage"
              @update:model-value="handleChange"
              @blur="handleBlur"
              shape="curved"
              placeholder="Select Apartment"
              icon="ri:community-fill"
              class="text-sm py-1 px-2"
            >
              <!-- Options for apartment selection -->
              <option v-for="year in [2020, 2021, 2022, 2023, 2024]" :key="year" :value="year">{{ year }}</option>
            </BaseSelect>
          </Field>

          <!-- Area selection -->
          <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-4" name="area">
            <BaseSelect
              :model-value="field.value"
              :error="errorMessage"
              @update:model-value="handleChange"
              @blur="handleBlur"
              shape="curved"
              placeholder="Select Area"
              icon="ri:home-line"
              class="text-sm py-1 px-2"
            >
              <!-- Options for area selection -->
              <option v-for="area in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]" :key="area" :value="area">{{ area }}</option>
            </BaseSelect>
          </Field>

          <div class="ms-10 flex items-center gap-1 mt-5">
            <button type="submit" class="BaseButtonIcon" rounded="full" small>
<!--              <BaseButtonIcon rounded="full" small>-->
<!--                Show-->
<!--              </BaseButtonIcon>-->
              <BaseButton
            color="primary"
            class="w-24"
          >
            {{ t("Save") }}
          </BaseButton>
            </button>
          </div>
        </form>
      </div>
    </BaseCard>
  </div>
</div>


      <div class="ltablet:col-span-6 col-span-6 lg:col-span-6">

        <DemoChartPie/>

      </div>
      <div class="ltablet:col-span-6 col-span-6 lg:col-span-6">

        <BaseCard class="p-14 py-30" rounded="lg">
          <!-- Title -->
          <div class="mb-8 flex items-center justify-between">
            <BaseHeading
              as="h3"
              size="md"
              weight="semibold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>Max Power Consumption</span>
            </BaseHeading>
            <!--          <NuxtLink-->
            <!--            to="#"-->
            <!--            class="bg-muted-100 hover:bg-muted-200 dark:bg-muted-700 dark:hover:bg-muted-900 text-primary-500 rounded-lg px-4 py-2 font-sans text-sm font-medium underline-offset-4 transition-colors duration-300 hover:underline"-->
            <!--          >-->
            <!--            View All-->
            <!--          </NuxtLink>-->
          </div>
          <DemoTrendingSkills/>
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
              <span>Seasonal Comparison</span>
            </BaseHeading>
          </div>
          <AddonApexcharts v-bind="demoBarMulti3"/>
        </BaseCard>
      </div>


      <!--       Area Chart card-->
      <!--      <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">-->
      <!--        <BaseCard class="p-6">-->
      <!--          &lt;!&ndash; Title &ndash;&gt;-->
      <!--          <div class="mb-6">-->
      <!--            <BaseHeading-->
      <!--              as="h3"-->
      <!--              size="md"-->
      <!--              weight="semibold"-->
      <!--              lead="tight"-->
      <!--              class="text-muted-800 dark:text-white"-->
      <!--            >-->
      <!--              <span>List Of Appliance</span>-->
      <!--            </BaseHeading>-->
      <!--          </div>-->
      <!--          <AddonApexcharts v-bind="areaCustomers" class="-ms-4"/>-->
      <!--        </BaseCard>-->
      <!--      </div>-->
      <!--      <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">-->
      <!--        <BaseCard class="p-6">-->
      <!--          &lt;!&ndash; Title &ndash;&gt;-->
      <!--          <div class="mb-6">-->
      <!--            <BaseHeading-->
      <!--              as="h3"-->
      <!--              size="md"-->
      <!--              weight="semibold"-->
      <!--              lead="tight"-->
      <!--              class="text-muted-800 dark:text-white"-->
      <!--            >-->
      <!--              <span>AC To DC</span>-->
      <!--            </BaseHeading>-->
      <!--          </div>-->
      <!--          <AddonApexcharts v-bind="areaCustomers" class="-ms-4"/>-->
      <!--        </BaseCard>-->
      <!--      </div>-->


      <!--      <div class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">-->
      <!--        <form method="POST" action="" @submit.prevent="addPowerRecord" novalidate>-->
      <!--          <BaseCard rounded="lg" class="p-6">-->
      <!--            <div class="mb-6 flex items-center justify-between">-->
      <!--              <BaseHeading-->
      <!--                as="h3"-->
      <!--                size="md"-->
      <!--                weight="semibold"-->
      <!--                lead="tight"-->
      <!--                class="text-muted-800 dark:text-white"-->
      <!--              >-->
      <!--                <span>Selected Products</span>-->
      <!--              </BaseHeading>-->
      <!--            </div>-->
      <!--            <div class="mb-2 space-y-5">-->
      <!--              <div v-for="device in app.getselectedDevice" :key="device.id"-->
      <!--                   class="flex flex-col md:flex-row items-center md:items-start gap-2">-->

      <!--                <div class="flex items-center gap-2 md:w-1/4">-->
      <!--                  <BaseHeading-->
      <!--                    as="h4"-->
      <!--                    size="sm"-->
      <!--                    weight="medium"-->
      <!--                    lead="snug"-->
      <!--                    class="text-muted-800 dark:text-white"-->
      <!--                  >-->
      <!--                    <span>{{ device.name }}</span>-->
      <!--                    <BaseTag-->
      <!--                      color="success"-->
      <!--                      variant="pastel"-->
      <!--                      rounded="full"-->
      <!--                      size="sm"-->
      <!--                      class="font-medium ms-3"-->
      <!--                    >-->
      <!--                      ON-->
      <!--                    </BaseTag>-->
      <!--                  </BaseHeading>-->
      <!--                </div>-->
      <!--                <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="flex-1 md:w-1/4"-->
      <!--                       :value="device.name" name="deviceId">-->
      <!--                  <BaseInput-->
      <!--                    :error="errorMessage"-->
      <!--                    @update:model-value="handleChange"-->
      <!--                    @blur="handleBlur"-->
      <!--                    type="hidden"-->
      <!--                    shape="curved"-->
      <!--                  />-->
      <!--                </Field>-->
      <!--                <Field  v-slot="{ field, errorMessage, handleChange, handleBlur }" class="flex-1 md:w-1/4" name="start">-->
      <!--                  <BaseInput-->
      <!--                    :model-value="field.value"-->
      <!--                    :error="errorMessage"-->
      <!--                    @update:model-value="handleChange"-->
      <!--                    @blur="handleBlur"-->
      <!--                    type="datetime-local"-->
      <!--                    shape="curved"-->
      <!--                    placeholder="Start Date"-->
      <!--                    icon="ri:calendar-fill"-->
      <!--                  />-->
      <!--                </Field>-->
      <!--                <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="flex-1 md:w-1/4" name="end">-->
      <!--                  <BaseInput-->
      <!--                    :model-value="field.value"-->
      <!--                    :error="errorMessage"-->
      <!--                    @update:model-value="handleChange"-->
      <!--                    @blur="handleBlur"-->
      <!--                    type="datetime-local"-->
      <!--                    shape="curved"-->
      <!--                    placeholder="End Date"-->
      <!--                    icon="ri:calendar-fill"-->
      <!--                  />-->
      <!--                </Field>-->
      <!--                <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="flex-1 md:w-1/4"-->
      <!--                       name="consumption">-->
      <!--                  <BaseInput-->
      <!--                    :model-value="field.value"-->
      <!--                    :error="errorMessage"-->
      <!--                    @update:model-value="handleChange"-->
      <!--                    @blur="handleBlur"-->
      <!--                    shape="curved"-->
      <!--                    placeholder="Consumption"-->
      <!--                    icon="ri:lightbulb-flash-fill"-->
      <!--                  />-->
      <!--                </Field>-->
      <!--                &lt;!&ndash;          <div class="flex items-center gap-1">&ndash;&gt;-->

      <!--                &lt;!&ndash;          </div>&ndash;&gt;-->
      <!--                <div class="flex items-center gap-1 mt-3">-->
      <!--                  <button type="submit" class="BaseButtonIcon" rounded="full" small>-->
      <!--                    <Icon name="ri:add-circle-fill"/>-->
      <!--                  </button>-->
      <!--                  <BaseButtonIcon rounded="full" small class="ms-3">-->
      <!--                    <Icon name="ri:delete-bin-7-fill"/>-->
      <!--                  </BaseButtonIcon>-->
      <!--                </div>-->
      <!--              </div>-->
      <!--            </div>-->
      <!--          </BaseCard>-->
      <!--        </form>-->
      <!--      </div>-->


      <div class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">
        <form method="POST" action="" @submit.prevent="addPowerRecord" novalidate>
          <BaseCard rounded="lg" class="p-6">
            <div class="mb-6 flex items-center justify-between">
              <BaseHeading
                as="h3"
                size="md"
                weight="semibold"
                lead="tight"
                class="text-muted-800 dark:text-white"
              >
                <span>Add Product Record</span>
              </BaseHeading>
            </div>
            <!-- Single input for device selection -->
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="deviceId">
              <BaseSelect
                :model-value="field.value"
                :error="errorMessage"
                @update:model-value="handleChange"
                @blur="handleBlur"
                shape="curved"
                placeholder="Select Device"
                icon="ri:device-fill"
              >
                <!-- Options for device selection -->
                <option v-for="device in app.getselectedDevice" :key="device.name" :value="device.name">{{
                    device.name
                  }}
                </option>
              </BaseSelect>
            </Field>
            <!-- Other input fields -->
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="start">
              <BaseInput
                :model-value="field.value"
                :error="errorMessage"
                @update:model-value="handleChange"
                @blur="handleBlur"
                type="datetime-local"
                shape="curved"
                placeholder="Start Date"
                icon="ri:calendar-fill"
              />
            </Field>
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="end">
              <BaseInput
                :model-value="field.value"
                :error="errorMessage"
                @update:model-value="handleChange"
                @blur="handleBlur"
                type="datetime-local"
                shape="curved"
                placeholder="End Date"
                icon="ri:calendar-fill"
              />
            </Field>
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="consumption">
              <BaseInput
                :model-value="field.value"
                :error="errorMessage"
                @update:model-value="handleChange"
                @blur="handleBlur"
                shape="curved"
                placeholder="Consumption"
                icon="ri:lightbulb-flash-fill"
              />
            </Field>
            <div class="flex items-center gap-1 mt-5">
              <button type="submit" class="BaseButtonIcon" rounded="full" small>
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:add-circle-fill"/>

                </BaseButtonIcon>

              </button>
              <!-- <button @click="deleteDevice" class="BaseButtonIcon" rounded="full" small>
                <Icon name="ri:delete-bin-fill"/>

              </button> -->
            </div>
          </BaseCard>
        </form>
      </div>

      <!-- Create a section to loop through devices -->
      <div class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">
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
        </div>
        <!-- Loop through devices -->
        <div v-for="device in app.getselectedDevice" :key="device.name">
          <div class="ltablet:col-span-4 col-span-4 md:col-span-4 lg:col-span-4">

            <BaseCard rounded="lg" class="p-6 mt-3">

              <span> {{ device.name }}</span>
              <button @click="deleteDevice(device.id)" class="BaseButtonIcon ms-5" rounded="full" small>
                <Icon name="ri:delete-bin-fill"/>
              </button>

              <!-- Button to delete device -->

            </BaseCard>
          </div>
        </div>
      </div>

      <!--      <div class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">-->
      <!--        <form method="POST" action="" @submit.prevent="addPowerRecord" novalidate>-->
      <!--          <BaseCard rounded="lg" class="p-6">-->
      <!--            <div class="mb-6 flex items-center justify-between">-->
      <!--              <BaseHeading-->
      <!--                as="h3"-->
      <!--                size="md"-->
      <!--                weight="semibold"-->
      <!--                lead="tight"-->
      <!--                class="text-muted-800 dark:text-white"-->
      <!--              >-->
      <!--                <span>Selected Products</span>-->
      <!--              </BaseHeading>-->
      <!--            </div>-->
      <!--            <div class="mb-2 space-y-5">-->
      <!--              <div v-for="device in app.getselectedDevice" class="flex items-center gap-2">-->
      <!--                <div class="flex items-center gap-2 justify-between">-->
      <!--                  <div>-->
      <!--                    <BaseHeading-->
      <!--                      as="h4"-->
      <!--                      size="sm"-->
      <!--                      weight="medium"-->
      <!--                      lead="snug"-->
      <!--                      class="text-muted-800 dark:text-white"-->
      <!--                    >-->
      <!--                      <span>{{ device.name  }}</span>-->
      <!--                      <BaseTag-->
      <!--                    color="success"-->
      <!--                    variant="pastel"-->
      <!--                    rounded="full"-->
      <!--                    size="sm"-->
      <!--                    class="font-medium ms-3"-->
      <!--                  >-->
      <!--                    ON-->
      <!--                  </BaseTag>-->
      <!--                    </BaseHeading>-->

      <!--                  </div>-->
      <!--                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"-->
      <!--                         class="ms-auto flex items-center gap-1" :value="device.name" name="deviceId">-->
      <!--                    <BaseInput-->
      <!--                      :error="errorMessage"-->
      <!--                      @update:model-value="handleChange"-->
      <!--                      @blur="handleBlur"-->
      <!--                     type="hidden"-->
      <!--                      shape="curved"-->
      <!--                    />-->
      <!--                  </Field>-->

      <!--                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"-->
      <!--                         class="ms-auto flex items-center gap-1" name="start">-->
      <!--                    <BaseInput-->
      <!--                      :model-value="field.value"-->
      <!--                      :error="errorMessage"-->
      <!--                      @update:model-value="handleChange"-->
      <!--                      @blur="handleBlur"-->
      <!--                      type="datetime-local"-->
      <!--                      shape="curved"-->
      <!--                      placeholder="Start Date"-->
      <!--                      icon="ri:calendar-fill"-->
      <!--                    />-->
      <!--                  </Field>-->
      <!--                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"-->
      <!--                         class="ms-auto flex items-center gap-1" name="end">-->
      <!--                    <BaseInput-->
      <!--                      :model-value="field.value"-->
      <!--                      :error="errorMessage"-->
      <!--                      @update:model-value="handleChange"-->
      <!--                      @blur="handleBlur"-->
      <!--                      type="datetime-local"-->
      <!--                      shape="curved"-->
      <!--                      placeholder="End Date"-->
      <!--                      icon="ri:calendar-fill"-->
      <!--                    />-->
      <!--                  </Field>-->
      <!--                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"-->
      <!--                         class="ms-auto flex items-center gap-1" name="consumption">-->
      <!--                    <BaseInput-->
      <!--                      :model-value="field.value"-->
      <!--                      :error="errorMessage"-->
      <!--                      @update:model-value="handleChange"-->
      <!--                      @blur="handleBlur"-->
      <!--                      shape="curved"-->
      <!--                      placeholder="Consumption"-->
      <!--                      icon="ri:lightbulb-flash-fill"-->

      <!--                    />-->
      <!--                  </Field>-->
      <!--                  <div class="ms-auto flex items-center gap-1">-->
      <!--                    <button type="submit" class="BaseButtonIcon" rounded="full" small>-->
      <!--                      <Icon name="ri:add-circle-fill"/>-->
      <!--                    </button>-->
      <!--                  </div>-->
      <!--                  <div class="ms-auto flex items-center gap-1">-->
      <!--                    <BaseButtonIcon rounded="full" small>-->
      <!--                      <Icon name="ri:delete-bin-7-fill"/>-->
      <!--                    </BaseButtonIcon>-->
      <!--                  </div>-->
      <!--                </div>-->
      <!--              </div>-->
      <!--            </div>-->
      <!--          </BaseCard>-->
      <!--        </form>-->
      <!--      </div>-->


    </div>


    <div class="ltablet:col-span-6 col-span-6 md:col-span-6 lg:col-span-6">
      <BaseHeading
        as="h3"
        size="md"
        weight="semibold"
        lead="tight"
        class="text-muted-800 dark:text-white mt-10 my-5"
      >
        <span>Latest order</span>
      </BaseHeading>
      <div class="space-y-2 pt-6">
        <TransitionGroup
          enter-active-class="transform-gpu"
          enter-from-class="opacity-0 -translate-x-full"
          enter-to-class="opacity-100 translate-x-0"
          leave-active-class="absolute transform-gpu"
          leave-from-class="opacity-100 translate-x-0"
          leave-to-class="opacity-0 -translate-x-full"
        >

          <DemoFlexTableRow
            v-for="(item, index) in orders"
            :key="index"
            rounded="sm"
          >
            <template #start>
              <DemoFlexTableStart
                label="Buyer"
                :hide-label="index > 0"
                :title="item.user_id"
              />
              <DemoFlexTableStart
                label="Amount"
                :hide-label="index > 0"
                :title="item.amount"
                class="ms-20"

              />
              <DemoFlexTableStart
                label="Fee"
                :hide-label="index > 0"
                :title="item.fee"
                class="ms-20"

              />
            </template>

            <template #end>
              <DemoFlexTableCell
                label="Create"
                :hide-label="index > 0"
                tablet-hidden
                class="w-full sm:w-36"
              >
                  <span
                    class="text-muted-500 dark:text-muted-400 font-sans text-sm"
                  >
                    {{ item.created_at }}
                  </span>
              </DemoFlexTableCell>
              <DemoFlexTableCell
                label="Price"
                :hide-label="index > 0"
                class="w-full sm:w-32"
              >
                <div
                  class="flex w-full items-center justify-end gap-1 sm:justify-center"
                >

                    <span
                      class="text-muted-500 dark:text-muted-400 font-sans text-sm"
                    >
                      20
                    </span>
                </div>
              </DemoFlexTableCell>

            </template>
          </DemoFlexTableRow>
        </TransitionGroup>

        <!--          <div v-if="!pending && data?.data.length !== 0" class="pt-6">-->
        <!--            <BasePagination-->
        <!--              :total-items="data?.total ?? 0"-->
        <!--              :item-per-page="perPage"-->
        <!--              :current-page="page"-->
        <!--              rounded="full"-->
        <!--            />-->
        <!--          </div>-->
      </div>

    </div>


  </div>
</template>
