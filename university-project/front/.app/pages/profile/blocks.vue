<script setup lang="ts">
import {useAppStore} from "~/stores/app";
import {toTypedSchema} from "@vee-validate/zod";
import {Field, useForm} from 'vee-validate'
import {z} from 'zod'
import {storeToRefs} from "pinia";

const {t} = useI18n({useScope: "local"})
const demoAreaMulti = reactive(useDemoAreaMulti())
const router = useRouter()
// onBeforeUnmount(() => {
//     router.push('/dashboard')
//
//   }
// )


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
      categories: [
        '2018-09-19T00:00:00.000Z',
        '2018-09-20T01:30:00.000Z',
        '2018-09-22T02:30:00.000Z',
        '2018-09-25T03:30:00.000Z',
        '2018-10-5T04:30:00.000Z',
        '2018-10-10T05:30:00.000Z',
        '2018-10-19T06:30:00.000Z',
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
      name: 'iron',
      data: [31, 40, 28, 51, 42, 109, 100],
    },
    {
      name: 'heater',
      data: [11, 32, 45, 32, 34, 52, 41],
    },
  ])

  return {
    type,
    height,
    options,
    series,
  }
}

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
const app = useAppStore();
const {orders, categories24, values24} = storeToRefs(app);
const cate = ref(categories24)

const areaCustomers = reactive(useAreaCustomers())
const radialBarTeam = reactive(useRadialBarTeam())
const barProfit = reactive(useBarProfit())
const fetchselectedDevice = app.fetchselectedDevice;
const fetchOrders = app.fetchOrders;
const fetchApartment = app.fetchApartment;

const initializeData = async () => {
  await fetchApartment();
  await fetchselectedDevice();
  await fetchOrders();
};

onMounted(async () => {
    await initializeData();
  });

const VALIDATION_TEXT = {
  EMAIL_REQUIRED: t('emailRequired'), // Translate email required text
  PASSWORD_REQUIRED: t('passwordRequired'), // Translate password required text
}
const zodSchema = z.object({
  apartment: z.number(),
  area: z.string(),
  unit: z.string(),
})

type FormInput = z.infer<typeof zodSchema>;

const validationSchema = toTypedSchema(zodSchema)
const initialValues = computed<FormInput>(() => ({
  apartment: '',
  area: '',
  unit: '',
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
  await app.addBlock(values.apartment, values.area, values.unit);
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
      categories: cate,
      // categories: ['iron', 'heater'],

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
    // {
    //   name: 'AC',
    //   data: [44, 55, 57, 56, 61, 58, 63, 60, 66],
    // },
    {
      name: 'DC',
      data: values24,
      // data: [35, 41],
    },
    // {
    //   name: 'Free Cash Flow',
    //   data: [35, 41, 36, 26, 45, 48, 52, 53, 41],
    // },
  ])

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
                <span>Add Block</span>
              </BaseHeading>
            </div>
            <!-- Single input for device selection -->
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="apartment">
              <BaseSelect
                :model-value="field.value"
                :error="errorMessage"
                @update:model-value="handleChange"
                @blur="handleBlur"
                shape="curved"
                placeholder="Select Apartment"
                icon="ri:community-fill"
              >
                <!-- Options for device selection -->
                <option v-for="device in app.getApartment" :key="device.apartment_no" :value="device.apartment_no">{{
                    device.apartment_no
                  }}
                </option>
              </BaseSelect>
            </Field>
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="area">
              <BaseSelect
                :model-value="field.value"
                :error="errorMessage"
                @update:model-value="handleChange"
                @blur="handleBlur"
                shape="curved"
                placeholder="Select Area"
                icon="ri:home-line"
              >
                <!-- Options for device selection -->
                <option v-for="device in ['Small (80)','Medium (100)', 'Big (120)']" :key="device" :value="device">{{
                    device
                  }}
                </option>
              </BaseSelect>
            </Field>
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" class="mb-2" name="unit">
              <BaseInput
                :model-value="field.value"
                :error="errorMessage"
                @update:model-value="handleChange"
                @blur="handleBlur"
                shape="curved"
                placeholder="Unit"
                icon="ri:home-fill"
              />
            </Field>
            <!-- Other input fields -->
                       <div class="flex items-center gap-1 mt-5">
              <button type="submit" class="BaseButtonIcon" rounded="full" small>
                <BaseButtonIcon rounded="full" small>
                  <Icon name="ri:save-fill"/>
<!--                    Save-->
                </BaseButtonIcon>
<!-- <BaseButton-->
<!--            type="submit"-->
<!--            color="primary"-->
<!--            class="w-24"-->
<!--          >-->
<!--            {{ t("Save") }}-->
<!--          </BaseButton>-->
              </button>
              <!-- <button @click="deleteDevice" class="BaseButtonIcon" rounded="full" small>
                <Icon name="ri:delete-bin-fill"/>

              </button> -->
            </div>
          </BaseCard>
        </form>
      </div>

  </div>
</template>
