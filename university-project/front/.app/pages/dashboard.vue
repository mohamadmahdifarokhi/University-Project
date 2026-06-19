<script setup lang="ts">
import {ref, reactive, computed, watch, onMounted} from 'vue';
import {useAppStore} from "~/stores/app";
import {useAuthStore} from "@/stores/auth";
import {toTypedSchema} from "@vee-validate/zod";
import {Field, useForm} from 'vee-validate'
import {z} from 'zod'
import {storeToRefs} from "pinia";
import {useI18n} from 'vue-i18n';

const {t} = useI18n({useScope: "local"});
const router = useRouter();

const app = useAppStore();
const {categories24, values24, categoriesMonth, valuesMonth, cal8, graph4op, graph4Unop} = storeToRefs(app);
const cate = ref(categories24.value);
const authStore = useAuthStore();

const areaCustomers = reactive(useAreaCustomers());
const radialBarTeam = reactive(useRadialBarTeam());
const barProfit = reactive(useBarProfit());
const demoBarMulti = reactive(useDemoBarMulti());
const demoAreaMulti = reactive(useDemoAreaMulti());
const demoBarMulti3 = reactive(useDemoBarMulti3());

const fetchselectedDevice = app.fetchselectedDevice;
const fetchAvailablePeriods = app.fetchAvailablePeriods;
const fetch24Records = app.fetch24Records;
const fetchMonthRecords = app.fetchMonthRecords;
const fetch8 = app.fetch8;
const fetchGraph4 = app.fetchGraph4;
const powerConsumption = app.powerConsumption;

const fetch24RecordsAdmin = app.fetch24RecordsAdmin;
const fetchMonthRecordsAdmin = app.fetchMonthRecordsAdmin;
const fetchSeasonChartAdmin = app.fetchSeasonChartAdmin;
const fetchGraph4Admin = app.fetchGraph4Admin;


const fetch24RecordsMng = app.fetch24RecordsMng;
const fetchMonthRecordsMng = app.fetchMonthRecordsMng;
// const fetchSeasonChartMng = app.fetchSeasonChartMng;
const fetchGraph4Mng = app.fetchGraph4Mng;

async function initializeData() {
  console.log(authStore.isAdmin, "weifjwoief");
  console.log(authStore.isMng, "weifjwoief");

  if (authStore.isAdmin) {
    await fetch24RecordsAdmin();
    await fetchMonthRecordsAdmin();
    // await fetchSeasonChartAdmin();
    await fetchGraph4Admin();
  }
  if (authStore.isMng) {
    await fetch24RecordsMng();
    await fetchMonthRecordsMng();
    // await fetchSeasonChartMng();
    await fetchGraph4Mng();
  }
  if (!authStore.isMng && !authStore.isAdmin) {
    await fetchAvailablePeriods();
    // Default the monthly selector to the most recent period that has data.
    const months = app.availablePeriods?.months ?? [];
    if (months.length) {
      const last = months[months.length - 1];
      selectedYear.value = last.year;
      selectedMonth.value = last.month;
    }
    await fetch24Records();
    await fetchMonthRecords(selectedYear.value, selectedMonth.value);
    await fetchselectedDevice();
    await fetch8();
    await fetchGraph4();
    await powerConsumption();
  }
}

// Initialize data on component mount
onMounted(async () => {
  await initializeData();
});

// Watchers for reactive updates
watch([categories24, values24, categoriesMonth, valuesMonth, graph4op, graph4Unop], () => {
  // Update your charts here
  demoBarMulti.options.xaxis.categories = categories24.value;
  demoBarMulti.series[0].data = values24.value;
  demoAreaMulti.options.xaxis.categories = categoriesMonth.value;
  demoAreaMulti.series = valuesMonth.value;

  demoBarMulti3.series[0].data = graph4Unop.value;
  demoBarMulti3.series[1].data = graph4op.value;

}, {
  deep: true,
});
const now = new Date();
const isMonthlyLoading = ref(false);

const { availablePeriods } = storeToRefs(app);

// Only offer years/months that actually have data.
const yearOptions = computed(() =>
  (availablePeriods.value?.years ?? []).map((y) => ({
    value: y,
    label: gregorianYearToJalaliLabel(y),
  }))
);

const selectedYear = ref<number>(now.getFullYear());
const selectedMonth = ref<number>(now.getMonth() + 1);

const monthOptions = computed(() => {
  const months = (availablePeriods.value?.months ?? [])
    .filter((m) => m.year === selectedYear.value)
    .map((m) => ({ value: m.month, label: gregorianMonthToJalaliLabel(m.year, m.month) }));
  return months;
});

definePageMeta({
  title: 'داشبورد',
  middleware: ['authenticated'],
  preview: {
    title: 'Personal dashboard v1',
    description: 'For personal usage and reports',
    categories: ['dashboards'],
    src: '/img/screens/dashboards-personal-1.png',
    srcDark: '/img/screens/dashboards-personal-1-dark.png',
    order: 1,
  },
});

const VALIDATION_TEXT = {
  EMAIL_REQUIRED: t('emailRequired'),
  PASSWORD_REQUIRED: t('passwordRequired')
}

const zodSchema = z.object({
  start: z.string(),
  end: z.string(),
  deviceId: z.string(),
})

type FormInput = z.infer<typeof zodSchema>;

const validationSchema = toTypedSchema(zodSchema)
const initialValues = computed<FormInput>(() => ({
  start: '',
  end: '',
  deviceId: '',
}));

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
});

const addPowerRecord = handleSubmit(async (values) => {
  console.log('lllll')
  await app.addRecord(values.deviceId, values.start, values.end);
});
const fetchMonthly = async () => {
  isMonthlyLoading.value = true;
  try {
    await app.fetchMonthRecords(selectedYear.value, selectedMonth.value);
  } finally {
    isMonthlyLoading.value = false;
  }
};

// When the year changes, make sure the selected month is valid for it.
watch(selectedYear, () => {
  const months = monthOptions.value;
  if (months.length && !months.some((m) => m.value === selectedMonth.value)) {
    selectedMonth.value = months[months.length - 1].value;
  }
});

// Any change in the year or month selectors instantly refreshes the chart
// (no submit button needed).
watch([selectedYear, selectedMonth], async () => {
  await fetchMonthly();
});

function deleteDevice(deviceId) {
  app.deleteDevice(deviceId);
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

function useDemoBarMulti() {
  const {primary, info, success, warning} = useTailwindColors();
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
      enabled: true,
      formatter: function (val) {
        return val.toFixed(2);
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
  };

  const series = shallowRef([
    {
      name: 'DC',
      data: values24.value.map(value => parseFloat(value.toFixed(2))),
    },
  ]);

  return {
    type,
    height,
    options,
    series,
  };
}

function useDemoAreaMulti() {
  const {primary, info, success} = useTailwindColors();
  const type = 'area';
  const height = 280;

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
      categories: categoriesMonth.value,
      labels: {
        formatter: function (val: any) {
          try {
            return toJalaliDate(val);
          } catch (e) {
            return val;
          }
        },
      },
    },
    tooltip: {
      x: {
        formatter: function (val: any) {
          try {
            return toJalaliDate(val);
          } catch (e) {
            return val;
          }
        },
      },
    },
  };

  // Formatting the series data to 2 decimal places
  const formattedSeries = valuesMonth.value.map(series => ({
    name: series.name,
    data: series.data.map(value => parseFloat(value.toFixed(2)))
  }));

  const series = shallowRef(formattedSeries);

  return {
    type,
    height,
    options,
    series,
  };
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
      categories: [
        'بهار', 'تابستان', 'پاییز', 'زمستان'
      ],
    },
    yaxis: {
      title: {
        text: 'هزینه (تومان)',
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

    <div class="grid grid-cols-12 gap-6">

      <div v-if="!authStore.isAdmin && !authStore.isMng" class="col-span-12 md:col-span-4">
        <BaseCard class="p-4">
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
              <span>{{ cal8['conversion_per'] }}</span>
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
        <BaseCard class="p-4">
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
              <span>0</span>
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
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>میانگین سالانه سرمایه‌گذاری و صرفه‌جویی (یورو)</span>
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
              <span>{{ cal8['investment'] }}</span>
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
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>کاهش انتشار گازهای گلخانه‌ای (گرم CO2/کیلووات‌ساعت در روز)</span>
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
              <span>{{ cal8['gr_em_sa'] }}</span>
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
        <BaseCard class="p-4">
          <div class="mb-1 flex items-center justify-between">
            <BaseHeading
              as="h5"
              size="sm"
              weight="medium"
              lead="tight"
              class="text-muted-500 dark:text-muted-400"
            >
              <span>توان تقسیم‌شده بر AC-DC</span>
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
              <span>{{ cal8['power_divided_by_ac_dc'] }}</span>
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
        <BaseCard class="p-4">
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
              <span>{{ cal8['efficiency'] }}%</span>
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
        <BaseCard class="p-4">
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
              <span>{{ cal8['pv_gen'] }}</span>
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
        <BaseCard class="p-4">
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
              <span>{{ cal8['st_ca'] }}%</span>
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
              <span>مصرف روزانه</span>
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
                <span>مصرف ماهانه (وات‌ساعت)</span>
              </BaseHeading>
            </div>

            <AddonApexcharts v-bind="demoAreaMulti"/>

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
                    <option v-for="y in yearOptions" :key="y.value" :value="y.value">{{ y.label }}</option>
                  </BaseSelect>

                  <!-- Month selection -->
                  <BaseSelect
                    v-model="selectedMonth"
                    shape="curved"
                    label="ماه"
                    icon="ph:calendar-check-duotone"
                    class="flex-1"
                  >
                    <option v-for="m in monthOptions" :key="m.value" :value="m.value">{{ m.label }}</option>
                  </BaseSelect>
                </div>
              </div>
            </div>
          </BaseCard>
        </div>
      </div>


      <div class="ltablet:col-span-12 col-span-12 lg:col-span-6">

        <DemoChartPie/>

      </div>
      <div class="ltablet:col-span-12 col-span-12 lg:col-span-6">

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
              <span>حداکثر مصرف توان</span>
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
              <span>مقایسه فصلی</span>
            </BaseHeading>
          </div>
          <AddonApexcharts v-bind="demoBarMulti3"/>
        </BaseCard>
      </div>


      <div v-if="!authStore.isAdmin && !authStore.isMng" class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">
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
                <span>افزودن رکورد مصرف</span>
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
                placeholder="انتخاب دستگاه"
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
                placeholder="تاریخ شروع"
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
                placeholder="تاریخ پایان"
                icon="ri:calendar-fill"
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
      <div v-if="!authStore.isAdmin && !authStore.isMng" class="ltablet:col-span-12 col-span-12 md:col-span-12 lg:col-span-12">
        <div class="mb-6 flex items-center justify-between">
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


    </div>


  </div>
</template>
