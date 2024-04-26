<script setup lang="ts">
import {useAppStore} from "~/stores/app";
import {toTypedSchema} from "@vee-validate/zod";
import {Field, useForm} from 'vee-validate'
import {z} from 'zod'

const {t} = useI18n({useScope: "local"})

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

const areaCustomers = reactive(useAreaCustomers())
const radialBarTeam = reactive(useRadialBarTeam())
const barProfit = reactive(useBarProfit())
const fetchselectedDevice = app.fetchselectedDevice;
const initializeData = async () => {
  await fetchselectedDevice();
};
initializeData()
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
  console.log("Asdqwdqwdqwd", values)
  await app.addRecord(values.deviceId,values.start, values.end, values.consumption);
})

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
              <span>CONVERSION PERCENT</span>
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
              <span>SAVED ENERGY</span>
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
              <span>INVESTMENT & SAVING</span>
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
              <span>GREENHOUSE EMISSION SAVING</span>
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
              <span>EFFICIENCY</span>
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
                <span>Selected Products</span>
              </BaseHeading>
            </div>
            <div class="mb-2 space-y-5">
              <div v-for="device in app.getselectedDevice" class="flex items-center gap-2">
                <div class="flex items-center gap-2">
                  <div>
                    <BaseHeading
                      as="h4"
                      size="sm"
                      weight="medium"
                      lead="snug"
                      class="text-muted-800 dark:text-white"
                    >
                      <span>{{ device.name  }}</span>
                    </BaseHeading>
                  </div>
                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"
                         class="ms-auto flex items-center gap-1" :value="device.name" name="deviceId">
                    <BaseInput
                      :error="errorMessage"
                      @update:model-value="handleChange"
                      @blur="handleBlur"
                     type="hidden"
                      shape="curved"
                    />
                  </Field>

                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"
                         class="ms-auto flex items-center gap-1" name="start">
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
                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"
                         class="ms-auto flex items-center gap-1" name="end">
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
                  <Field v-slot="{ field, errorMessage, handleChange, handleBlur }"
                         class="ms-auto flex items-center gap-1" name="consumption">
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
                  <div class="ms-auto flex items-center gap-1">
                    <button type="submit" class="BaseButtonIcon" rounded="full" small>
                      <Icon name="ri:add-circle-fill"/>
                    </button>
                  </div>
                  <div class="ms-auto flex items-center gap-1">
                    <BaseButtonIcon rounded="full" small>
                      <Icon name="ri:delete-bin-7-fill"/>
                    </BaseButtonIcon>
                  </div>
                </div>
              </div>
            </div>
          </BaseCard>
        </form>
      </div>


    </div>
  </div>
</template>
