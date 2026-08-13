<script lang="ts">
type DashboardLoadState = {
  key: string
  promise: Promise<void> | null
  completedAt: number
}

// Nuxt can briefly create the page twice while completing the login redirect.
// Keep the initial dashboard load shared at module scope so both instances do
// not issue the same set of expensive chart requests.
const dashboardLoadState: DashboardLoadState = {
  key: '',
  promise: null,
  completedAt: 0,
}

const DASHBOARD_LOAD_TTL = 3_000
</script>

<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue'
import { useAppStore } from '~/stores/app'
import { useAuthStore } from '@/stores/auth'
import { toTypedSchema } from '@vee-validate/zod'
import { Field, useForm } from 'vee-validate'
import { z } from 'zod'
import { storeToRefs } from 'pinia'
import { useI18n } from 'vue-i18n'
import { gregorianToJalaali, toJalaliDateTime } from '~/utils/jalali'

const { t } = useI18n({ useScope: 'local' })
const router = useRouter()

const app = useAppStore()
const { orders, categories24, values24, categoriesMonth, valuesMonth, cal8, graph4op, graph4Unop, peakHour, peakPower, battery } = storeToRefs(app)
const cate = ref(categories24.value)
const authStore = useAuthStore()
const dashboardLoading = ref(true)
const dashboardError = ref('')
const recordError = ref('')
const formatNumber = (value: any) => new Intl.NumberFormat('fa-IR').format(Number(value ?? 0))
const formatIranianDate = (value: any) => toJalaliDateTime(value) || '—'
const toPersianDigits = (value: unknown) => String(value ?? '').replace(/\d/g, digit => '۰۱۲۳۴۵۶۷۸۹'[Number(digit)])
const formatPeakHour = (value: any) => {
  const match = String(value ?? '').match(/^(\d{1,2}):(\d{2})$/)
  if (!match) return '—'
  const hour = Number(match[1])
  const minute = Number(match[2])
  if (hour > 23 || minute > 59) return '—'
  const period = hour < 12 ? 'صبح' : hour < 18 ? 'بعدازظهر' : 'شب'
  return `${toPersianDigits(`${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')}`)} ${period}`
}
const batteryStoredEnergy = computed(() => Number(battery.value?.saved_energy ?? 0))
const dashboardEmpty = computed(() => !categories24.value?.length && !categoriesMonth.value?.length && !orders.value?.length && !Object.keys(cal8.value || {}).length)

const areaCustomers = reactive(useAreaCustomers())
const radialBarTeam = reactive(useRadialBarTeam())
const barProfit = reactive(useBarProfit())
const dailyConsumptionChart = reactive(useDailyConsumptionChart())
const monthlyConsumptionChart = reactive(useMonthlyConsumptionChart())
const optimizationChart = reactive(useOptimizationChart())
const monthlyChartVersion = ref(0)

const fetchselectedDevice = app.fetchselectedDevice
const fetchOrders = app.fetchOrders
const fetch24Records = app.fetch24Records
const fetchMonthRecords = app.fetchMonthRecords
const fetch8 = app.fetch8
const fetchGraph4 = app.fetchGraph4
const powerConsumption = app.powerConsumption
const fetchBattery = app.fetchBattery

const fetch24RecordsAdmin = app.fetch24RecordsAdmin
const fetchMonthRecordsAdmin = app.fetchMonthRecordsAdmin
const fetchSeasonChartAdmin = app.fetchSeasonChartAdmin
const fetchGraph4Admin = app.fetchGraph4Admin

const fetch24RecordsMng = app.fetch24RecordsMng
const fetchMonthRecordsMng = app.fetchMonthRecordsMng
// const fetchSeasonChartMng = app.fetchSeasonChartMng;
const fetchGraph4Mng = app.fetchGraph4Mng

async function initializeData(force = false) {
  dashboardLoading.value = true
  dashboardError.value = ''

  await authStore.checkAccessToken()

  const sessionKey = useCookie('email').value || useCookie('access_token').value || 'session'
  const loadKey = `${sessionKey}:${authStore.isAdmin ? 'admin' : authStore.isMng ? 'manager' : 'user'}:${selectedYear.value}:${selectedMonth.value}`
  const cacheIsFresh = dashboardLoadState.key === loadKey
    && Date.now() - dashboardLoadState.completedAt < DASHBOARD_LOAD_TTL

  if (!force && dashboardLoadState.key === loadKey) {
    if (dashboardLoadState.promise) {
      await dashboardLoadState.promise
      dashboardLoading.value = false
      return
    }

    if (cacheIsFresh) {
      dashboardLoading.value = false
      return
    }
  }

  const loadPromise = (async () => {
    try {
      if (authStore.isAdmin) {
        await Promise.all([fetch24RecordsAdmin(), fetchMonthRecordsAdmin(selectedYear.value, selectedMonth.value), fetchGraph4Admin(), powerConsumption()])
      }
      else if (authStore.isMng) {
        await Promise.all([fetch24RecordsMng(), fetchMonthRecordsMng(selectedYear.value, selectedMonth.value), fetchGraph4Mng(), powerConsumption()])
      }
      else {
        await Promise.all([fetch24Records(), fetchMonthRecords(selectedYear.value, selectedMonth.value), fetchselectedDevice(), fetchOrders(1, 5), fetch8(), fetchGraph4(), fetchBattery(), powerConsumption()])
      }
    }
    catch {
      dashboardError.value = 'اطلاعات داشبورد دریافت نشد. اتصال سرویس انرژی را بررسی کنید.'
    }
    finally {
      dashboardLoading.value = false
    }
  })()

  dashboardLoadState.key = loadKey
  dashboardLoadState.promise = loadPromise
  try {
    await loadPromise
    dashboardLoadState.completedAt = Date.now()
  }
  finally {
    if (dashboardLoadState.promise === loadPromise) {
      dashboardLoadState.promise = null
    }
  }
}

// Initialize data on component mount
onMounted(async () => {
  await initializeData()
})

// Watchers for reactive updates
watch([categories24, values24, graph4op, graph4Unop], () => {
  dailyConsumptionChart.options.xaxis.categories = categories24.value
  dailyConsumptionChart.series[0].data = values24.value
  optimizationChart.series[0].data = graph4Unop.value
  optimizationChart.series[1].data = graph4op.value
}, {
  deep: true,
})

watch([categoriesMonth, valuesMonth], () => {
  monthlyConsumptionChart.options.xaxis.categories = categoriesMonth.value
  monthlyConsumptionChart.series = valuesMonth.value
  monthlyChartVersion.value += 1
}, {
  deep: true,
})
const now = new Date()
const currentJalali = gregorianToJalaali(now.getFullYear(), now.getMonth() + 1, now.getDate())
const selectedYear = ref<number>(currentJalali.jy)
const selectedMonth = ref<number>(currentJalali.jm)
const isMonthlyLoading = ref(false)
const yearOptions = Array.from({ length: 7 }, (_, index) => currentJalali.jy - 5 + index)
const monthOptions = [
  { value: 1, label: 'فروردین' }, { value: 2, label: 'اردیبهشت' }, { value: 3, label: 'خرداد' },
  { value: 4, label: 'تیر' }, { value: 5, label: 'مرداد' }, { value: 6, label: 'شهریور' },
  { value: 7, label: 'مهر' }, { value: 8, label: 'آبان' }, { value: 9, label: 'آذر' },
  { value: 10, label: 'دی' }, { value: 11, label: 'بهمن' }, { value: 12, label: 'اسفند' },
]
definePageMeta({
  title: 'داشبورد',
  middleware: ['authenticated'],
})

const VALIDATION_TEXT = {
  EMAIL_REQUIRED: t('emailRequired'),
  PASSWORD_REQUIRED: t('passwordRequired'),
}

const zodSchema = z.object({
  start: z.string().min(1, 'تاریخ شروع را انتخاب کنید'),
  end: z.string().min(1, 'تاریخ پایان را انتخاب کنید'),
  deviceId: z.string().min(1, 'دستگاه را انتخاب کنید'),
}).superRefine((values, context) => {
  if (!values.start || !values.end) return
  const start = new Date(values.start).getTime()
  const end = new Date(values.end).getTime()
  if (!Number.isFinite(start) || !Number.isFinite(end)) return
  if (end <= start) {
    context.addIssue({
      code: z.ZodIssueCode.custom,
      path: ['end'],
      message: 'زمان پایان باید بعد از زمان شروع باشد',
    })
  }
})

type FormInput = z.infer<typeof zodSchema>

const validationSchema = toTypedSchema(zodSchema)
const initialValues = computed<FormInput>(() => ({
  start: '',
  end: '',
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

const addPowerRecord = handleSubmit(async (formValues) => {
  recordError.value = ''
  try {
    await app.addRecord(formValues.deviceId, formValues.start, formValues.end)
    resetForm()
    await Promise.all([
      fetch24Records(),
      fetchMonthly(),
      fetch8(),
      fetchGraph4(),
      powerConsumption(),
    ])
  }
  catch (error: any) {
    recordError.value = error?.response?.data?.detail || 'ثبت سابقه مصرف انجام نشد.'
  }
})
const fetchMonthly = async () => {
  isMonthlyLoading.value = true
  try {
    if (authStore.isAdmin) {
      await app.fetchMonthRecordsAdmin(selectedYear.value, selectedMonth.value)
    }
    else if (authStore.isMng) {
      await app.fetchMonthRecordsMng(selectedYear.value, selectedMonth.value)
    }
    else {
      await app.fetchMonthRecords(selectedYear.value, selectedMonth.value)
    }
  }
  finally {
    isMonthlyLoading.value = false
  }
}

watch([selectedYear, selectedMonth], () => {
  void fetchMonthly()
})

function deleteDevice(deviceId) {
  app.deleteDevice(deviceId)
}

function useAreaCustomers() {
  const { primary, info, success } = useTailwindColors()
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
      name: 'اتو',
      data: [31, 40, 28, 51, 42, 109, 100],
    },
    {
      name: 'یخچال',
      data: [11, 32, 45, 32, 34, 52, 41],
    },
    {
      name: 'فر برقی',
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
  const { primary } = useTailwindColors()
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
          margin: 5,
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
  const { primary } = useTailwindColors()
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
          position: 'top',
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
      categories: ['اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور'],
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
      name: 'نسبت بهره‌وری',
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

function useDemoTimeline() {
  const { primary, info, success, warning, danger } = useTailwindColors()
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

function useDailyConsumptionChart() {
  const { primary, info, success, warning } = useTailwindColors()
  const type = 'bar'
  const height = 280

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
            })
          })
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
      enabled: true,
      formatter: function (val) {
        return val.toFixed(2)
      },
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
        text: 'مصرف (وات‌ساعت)',
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
  }

  const series = shallowRef([
    {
      name: 'جریان مستقیم',
      data: values24.value.map(value => parseFloat(value.toFixed(2))),
    },
  ])

  return {
    type,
    height,
    options,
    series,
  }
}

function useMonthlyConsumptionChart() {
  const { primary, info, success } = useTailwindColors()
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
      // Categories are already formatted as Persian dates in the store.
      // They must stay categorical; ApexCharts cannot parse Jalali text as a
      // native JavaScript datetime.
      type: 'category',
      categories: categoriesMonth.value,
    },
    tooltip: {
      x: { formatter: value => value },
    },
  }

  // Formatting the series data to 2 decimal places
  const formattedSeries = valuesMonth.value.map(series => ({
    name: series.name,
    data: series.data.map(value => parseFloat(value.toFixed(2))),
  }))

  const series = shallowRef(formattedSeries)

  return {
    type,
    height,
    options,
    series,
  }
}

function useOptimizationChart() {
  const { primary, info, success, warning } = useTailwindColors()
  const type = 'bar'
  const height = 280

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
            })
          })
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
      categories: [
        'بهار', 'تابستان', 'پاییز', 'زمستان',
      ],
    },
    yaxis: {
      title: {
        text: 'هزینه (تومان)',
      },
      labels: {
        formatter: (value: any) => new Intl.NumberFormat('fa-IR').format(Number(value ?? 0)),
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
  }

  const series = shallowRef([
    {
      name: 'بهینه‌نشده',
      data: graph4Unop.value,
    },
    {
      name: 'بهینه‌شده',
      data: graph4op.value,
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
    <header class="mb-6 flex flex-wrap items-end justify-between gap-4" data-tour="dashboard-overview">
      <div>
        <BaseHeading as="h1" size="2xl">
          مرکز عملیات انرژی
        </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
          نمای یکپارچه تولید، ذخیره، مصرف و تبادل ریزشبکه دانشگاه
        </BaseParagraph>
      </div>
      <div class="flex flex-wrap gap-2">
        <BaseTag color="warning" variant="pastel">
          تولید خورشیدی
        </BaseTag><BaseTag color="success" variant="pastel">
          ذخیره باتری
        </BaseTag><BaseTag color="primary" variant="pastel">
          مصرف ساختمان
        </BaseTag><BaseTag color="info" variant="pastel">
          تبادل انرژی
        </BaseTag>
      </div>
    </header>

    <BaseCard v-if="dashboardLoading" class="p-12 text-center">
      <Icon name="svg-spinners:ring-resize" class="text-primary-500 mx-auto size-9" /><p class="mt-3">
        در حال همگام‌سازی داده‌های انرژی…
      </p>
    </BaseCard>
    <BaseMessage v-else-if="dashboardError" type="danger">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span>{{ dashboardError }}</span><BaseButton size="sm" @click="initializeData(true)">
          تلاش دوباره
        </BaseButton>
      </div>
    </BaseMessage>
    <BaseCard v-else-if="dashboardEmpty" class="p-12 text-center">
      <Icon name="ph:sun-horizon-duotone" class="text-warning-500 mx-auto size-14" /><BaseHeading class="mt-3">
        داده انرژی هنوز آماده نیست
      </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
        پس از ثبت ساختمان و سوابق مصرف، شاخص‌های عملیاتی اینجا نمایش داده می‌شوند.
      </BaseParagraph><BaseButton
        to="/profile/blocks"
        color="primary"
        class="mt-5"
      >
        ثبت منابع انرژی
      </BaseButton>
    </BaseCard>

    <template v-else>
      <div class="grid grid-cols-12 gap-6">
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-4">
          <BaseCard class="p-4" data-tour="metric-conversion">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>درصد تبدیل (٪)</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/conversion.png"
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
                <span>{{ formatNumber(cal8['conversion_per']) }}</span>
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
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-4">
          <BaseCard class="p-4" data-tour="metric-battery">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>انرژی ذخیره‌شده در باتری (وات/روز)</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/battery-storage.png"
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
                <span>{{ formatNumber(batteryStoredEnergy) }}</span>
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
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-4">
          <BaseCard class="p-4" data-tour="metric-investment">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>میانگین سالانه سرمایه‌گذاری و صرفه‌جویی (تومان)</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/investment.png"
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
                <span>{{ formatNumber(cal8['investment']) }}</span>
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
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-4">
          <BaseCard class="p-4" data-tour="metric-emissions">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>کاهش انتشار گازهای گلخانه‌ای (گرم دی‌اکسیدکربن/کیلووات‌ساعت در روز)</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/emissions.png"
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
                <span>{{ formatNumber(cal8['gr_em_sa']) }}</span>
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
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-4">
          <BaseCard class="p-4" data-tour="metric-ac-dc">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>نسبت توان متناوب و مستقیم</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/ac-dc.png"
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
                <span>{{ formatNumber(cal8['power_divided_by_ac_dc']) }}</span>
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
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-4">
          <BaseCard class="p-4" data-tour="metric-efficiency">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>بازده (٪)</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/efficiency.png"
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
                <span>{{ formatNumber(cal8['efficiency']) }}٪</span>
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

        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-6">
          <BaseCard class="p-4" data-tour="metric-solar">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>تولید پنل خورشیدی (وات)</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/solar-generation.png"
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
                <span>{{ formatNumber(cal8['pv_gen']) }}</span>
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
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-6">
          <BaseCard class="p-4" data-tour="metric-charge">
            <div class="mb-1 flex items-center justify-between">
              <BaseHeading
                as="h5"
                size="sm"
                weight="medium"
                lead="tight"
                class="text-muted-500 dark:text-muted-400"
              >
                <span>وضعیت شارژ (٪)</span>
              </BaseHeading>
              <BaseIconBox
                size="xs"
                class="text-primary-500 dark:text-primary-400 bg-transparent"
                rounded="full"
                color="none"
              >
                <img
                  class="size-9 object-contain"
                  src="/img/dashboard-icons/charge-status.png"
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
                <span>{{ formatNumber(cal8['st_ca']) }}٪</span>
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

        <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">
          <BaseCard class="p-6" data-tour="daily-chart">
            <!-- Title -->
            <div class="mb-6">
              <BaseHeading
                as="h3"
                size="md"
                weight="semibold"
                lead="tight"
                class="text-muted-800 dark:text-white"
              >
                <span>مصرف روزانه</span>
              </BaseHeading>
            </div>
            <AddonApexcharts v-bind="dailyConsumptionChart" />
          </BaseCard>
        </div>

        <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">
          <div class="relative">
            <BaseCard class="p-6" data-tour="monthly-chart">
              <!-- Title -->
              <div class="mb-6">
                <BaseHeading
                  as="h3"
                  size="md"
                  weight="semibold"
                  lead="tight"
                  class="text-muted-800 dark:text-white"
                >
                  <span>مصرف ماهانه (وات‌ساعت)</span>
                </BaseHeading>
              </div>

              <AddonApexcharts
                v-bind="monthlyConsumptionChart"
                :refresh-key="monthlyChartVersion"
              />

              <div class="border-muted-200 dark:border-muted-700 mt-6 flex justify-center border-t pt-6">
                <div class="w-full max-w-md">
                  <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
                    <!-- Year selection -->
                    <BaseSelect
                      v-model="selectedYear"
                      shape="curved"
                      label="سال"
                      icon="ph:calendar-blank-duotone"
                      class="flex-1"
                    >
                      <option
                        v-for="year in yearOptions"
                        :key="year"
                        :value="year"
                      >
                        {{ toPersianDigits(year) }}
                      </option>
                    </BaseSelect>

                    <!-- Month selection -->
                    <BaseSelect
                      v-model="selectedMonth"
                      shape="curved"
                      label="ماه"
                      icon="ph:calendar-check-duotone"
                      class="flex-1"
                    >
                      <option
                        v-for="m in monthOptions"
                        :key="m.value"
                        :value="m.value"
                      >
                        {{ m.label }}
                      </option>
                    </BaseSelect>

                  </div>
                  <BaseProgress
                    v-if="isMonthlyLoading"
                    size="xs"
                    class="mt-3"
                  />
                </div>
              </div>
            </BaseCard>
          </div>
        </div>

        <div class="ltablet:col-span-12 col-span-12 lg:col-span-6">
          <div data-tour="season-summary">
            <EnergySeasonSummary />
          </div>
        </div>
        <div class="ltablet:col-span-12 col-span-12 lg:col-span-6">
          <BaseCard class="py-30 p-14" rounded="lg" data-tour="peak-power">
            <!-- Title -->
            <div class="mb-8 flex items-center justify-between">
              <BaseHeading
                as="h3"
                size="md"
                weight="semibold"
                lead="tight"
                class="text-muted-800 dark:text-white"
              >
                <span>حداکثر مصرف توان</span>
              </BaseHeading>
            <!--          <NuxtLink-->
            <!--            to="#"-->
            <!--            class="bg-muted-100 hover:bg-muted-200 dark:bg-muted-700 dark:hover:bg-muted-900 text-primary-500 rounded-lg px-4 py-2 font-sans text-sm font-medium underline-offset-4 transition-colors duration-300 hover:underline"-->
            <!--          >-->
            <!--            View All-->
            <!--          </NuxtLink>-->
            </div>
            <div class="space-y-5">
              <div class="flex items-center gap-3">
                <Icon name="ri:time-fill" class="text-warning-500 size-6" /><div>
                  <BaseHeading size="sm">
                    ساعت اوج مصرف
                  </BaseHeading><BaseParagraph class="text-muted-500">
                    {{ formatPeakHour(peakHour) }}
                  </BaseParagraph>
                </div>
              </div><div class="flex items-center gap-3">
                <Icon name="ri:flashlight-fill" class="text-primary-500 size-6" /><div>
                  <BaseHeading size="sm">
                    بیشینه توان مصرفی
                  </BaseHeading><BaseParagraph class="text-muted-500">
                    {{ peakPower ? formatNumber(peakPower) : '—' }} وات
                  </BaseParagraph>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>

        <div class="ltablet:col-span-12 col-span-12 lg:col-span-12">
          <BaseCard class="p-6" data-tour="season-comparison">
            <!-- Title -->
            <div class="mb-6">
              <BaseHeading
                as="h3"
                size="md"
                weight="semibold"
                lead="tight"
                class="text-muted-800 dark:text-white"
              >
                <span>مقایسه فصلی</span>
              </BaseHeading>
            </div>
            <AddonApexcharts v-bind="optimizationChart" />
          </BaseCard>
        </div>

        <div v-if="!authStore.isAdmin && !authStore.isMng" class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">
          <form
            method="POST"
            action=""
            novalidate
            @submit.prevent="addPowerRecord"
          >
            <BaseCard rounded="lg" class="p-6" data-tour="add-record">
              <BaseMessage v-if="recordError" type="danger" class="mb-4">
                {{ recordError }}
              </BaseMessage>
              <div class="mb-6 flex items-center justify-between">
                <BaseHeading
                  as="h3"
                  size="md"
                  weight="semibold"
                  lead="tight"
                  class="text-muted-800 dark:text-white"
                >
                  <span>افزودن رکورد مصرف</span>
                </BaseHeading>
              </div>
              <!-- Single input for device selection -->
              <Field
                v-slot="{ field, errorMessage, handleChange, handleBlur }"
                class="mb-2"
                name="deviceId"
              >
                <BaseSelect
                  :model-value="field.value"
                  :error="errorMessage"
                  shape="curved"
                  placeholder="انتخاب دستگاه"
                  icon="ri:device-fill"
                  @update:model-value="handleChange"
                  @blur="handleBlur"
                >
                  <!-- Options for device selection -->
                  <option
                    v-for="device in app.getselectedDevice"
                    :key="device.name"
                    :value="device.name"
                  >
                    {{
                      device.name
                    }}
                  </option>
                </BaseSelect>
              </Field>
              <!-- Other input fields -->
              <Field
                v-slot="{ field, errorMessage, handleChange }"
                class="mb-2"
                name="start"
              >
                <JalaliDateTimePicker
                  :model-value="field.value"
                  :error="errorMessage"
                  placeholder="تاریخ و زمان شروع"
                  @update:model-value="handleChange"
                />
              </Field>
              <Field
                v-slot="{ field, errorMessage, handleChange }"
                class="mb-2"
                name="end"
              >
                <JalaliDateTimePicker
                  :model-value="field.value"
                  :error="errorMessage"
                  placeholder="تاریخ و زمان پایان"
                  @update:model-value="handleChange"
                />
              </Field>
              <!--            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="consumption">-->
              <!--              <BaseInput-->
              <!--                :model-value="field.value"-->
              <!--                :error="errorMessage"-->
              <!--                @update:model-value="handleChange"-->
              <!--                @blur="handleBlur"-->
              <!--                shape="curved"-->
              <!--                placeholder="Consumption"-->
              <!--                icon="ri:lightbulb-flash-fill"-->
              <!--              />-->
              <!--            </Field>-->
              <div class="mt-5 flex items-center gap-1">
                <button
                  type="submit"
                  class="BaseButtonIcon"
                  rounded="full"
                  small
                >
                  <BaseButtonIcon rounded="full" small>
                    <Icon name="ri:add-circle-fill" />
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
        <div v-if="!authStore.isAdmin && !authStore.isMng" class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">
          <div class="mb-6 flex items-center justify-between" data-tour="selected-devices">
            <BaseHeading
              as="h3"
              size="md"
              weight="semibold"
              lead="tight"
              class="text-muted-800 dark:text-white"
            >
              <span>دستگاه‌های انتخاب‌شده</span>
            </BaseHeading>
          </div>
          <!-- Loop through devices -->
          <div v-for="device in app.getselectedDevice" :key="device.name">
            <div class="ltablet:col-span-4 col-span-4 md:col-span-4 lg:col-span-4">
              <BaseCard rounded="lg" class="mt-3 p-6">
                <span> {{ device.name }}</span>
                <button
                  class="BaseButtonIcon ms-5"
                  rounded="full"
                  small
                  @click="deleteDevice(device.id)"
                >
                  <Icon name="ri:delete-bin-fill" />
                </button>

              <!-- Button to delete device -->
              </BaseCard>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!authStore.isAdmin && !authStore.isMng" class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12" data-tour="latest-orders">
        <div class="my-5 mt-10 flex items-center justify-between gap-3">
          <BaseHeading
            as="h3"
            size="md"
            weight="semibold"
            lead="tight"
            class="text-muted-800 dark:text-white"
          >
            <span>آخرین سفارش‌ها</span>
          </BaseHeading>
          <BaseTag v-if="orders.length" color="primary" variant="pastel">
            {{ formatNumber(orders.length) }} مورد
          </BaseTag>
        </div>
        <TransitionGroup
          tag="div"
          class="space-y-3"
          enter-active-class="transform-gpu transition-all duration-300"
          enter-from-class="opacity-0 -translate-y-2"
          enter-to-class="opacity-100 translate-y-0"
          leave-active-class="absolute transform-gpu transition-all duration-300"
          leave-from-class="opacity-100 translate-y-0"
          leave-to-class="opacity-0 -translate-y-2"
        >
          <BaseCard
            v-for="(item, index) in orders"
            :key="item.id || item._id || `${item.created_at}-${index}`"
            rounded="sm"
            class="p-4 sm:p-5"
          >
            <div class="mb-4 flex items-center justify-between gap-3 border-b border-muted-200 pb-3 dark:border-muted-700">
              <span class="text-muted-500 dark:text-muted-400 text-xs font-medium">
                سفارش {{ formatNumber(index + 1) }}
              </span>
              <span class="text-muted-400 dark:text-muted-500 text-xs">
                {{ formatIranianDate(item.created_at) }}
              </span>
            </div>
            <div class="flex flex-col divide-y divide-muted-200 dark:divide-muted-700">
              <div class="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0">
                <span class="text-muted-500 dark:text-muted-400 text-sm">خریدار</span>
                <span class="text-muted-800 dark:text-white text-end text-sm font-semibold">
                  {{ item.buyer_name || 'کاربر ناشناس' }}
                </span>
              </div>
              <div class="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0">
                <span class="text-muted-500 dark:text-muted-400 text-sm">مقدار انرژی</span>
                <span class="text-muted-800 dark:text-white text-end text-sm font-semibold">
                  {{ formatNumber(item.amount) }} کیلووات‌ساعت
                </span>
              </div>
              <div class="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0">
                <span class="text-muted-500 dark:text-muted-400 text-sm">کارمزد</span>
                <span class="text-muted-800 dark:text-white text-end text-sm font-semibold">
                  {{ formatNumber(item.fee) }} تومان
                </span>
              </div>
              <div class="flex items-center justify-between gap-4 py-3 first:pt-0 last:pb-0">
                <span class="text-muted-500 dark:text-muted-400 text-sm">قیمت نهایی</span>
                <span class="text-primary-600 dark:text-primary-400 text-end text-sm font-bold">
                  {{ formatNumber(item.fee) }} تومان
                </span>
              </div>
            </div>
          </BaseCard>
        </TransitionGroup>
        <BaseCard v-if="!orders.length" class="p-6 text-center">
          <BaseParagraph class="text-muted-500">
            هنوز سفارشی برای نمایش وجود ندارد.
          </BaseParagraph>
        </BaseCard>
      </div>
    </template>
  </div>
</template>
