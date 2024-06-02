<script setup lang="ts">
import {z} from "zod";
import {toTypedSchema} from "@vee-validate/zod";
import { Field, useForm } from 'vee-validate'

import { ref, reactive, computed, watch, onMounted } from 'vue';
import { useAppStore } from "~/stores/app";
import { storeToRefs } from "pinia";
import { useI18n } from 'vue-i18n';
import {useAuthStore} from "~/stores/auth";
const { t } = useI18n({ useScope: "local" });


const app = useAppStore();
const { seasonDatas, seasonLabels  } = storeToRefs(app);

const demoPie = reactive(useDemoPie())
const authStore = useAuthStore();


const fetchSeasonChart = app.fetchSeasonChart;
const fetchSeasonChartAdmin = app.fetchSeasonChartAdmin;
const fetchSeasonChartMng = app.fetchSeasonChartMng;


async function initializeData() {
  if (authStore.isAdmin) {
  await fetchSeasonChartAdmin()

  }
  if (authStore.isMng) {
  await fetchSeasonChartMng()

  }
  if (!authStore.isMng || authStore.isAdmin) {
  await fetchSeasonChart();

  }

}
// Initialize data on component mount
onMounted(async () => {
  await initializeData();
});



const VALIDATION_TEXT = {
  EMAIL_REQUIRED: t('emailRequired'),
  PASSWORD_REQUIRED: t('passwordRequired')
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
    labels: seasonLabels,
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

  const series = shallowRef(seasonDatas)

  return {
    type,
    height,
    options,
    series,
  }
}

const selectedYear = ref<number | null>(null);
const selectedSeason = ref<number | null>(null);
const fetchSeasonal = handleSubmit(async (values) => {
  const selectedValues = {
    year: selectedYear.value,
    month: selectedSeason.value,
  };
  console.log(selectedValues);
  await app.fetchSeasonChart(selectedYear.value, selectedSeason.value);
});

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
      <div class="flex justify-center mt-6">
        <form method="POST" class="items-center" style="max-width: 300px" @submit.prevent="fetchSeasonal" novalidate>
          <!-- Year selection -->
          <div class="mb-4">
            <BaseSelect
              v-model="selectedYear"
              shape="curved"
              placeholder="Select Year"
              icon="ri:community-fill"
              class="text-sm py-1 px-2"
            >
              <!-- Placeholder option -->
              <option disabled value="">{{ t('Select Year') }}</option>
              <!-- Options for year selection -->
              <option v-for="year in [2020, 2021, 2022, 2023, 2024, 2025]" :key="year" :value="year">{{ year }}</option>
            </BaseSelect>
          </div>

          <!-- Season selection -->
          <div class="mb-4">
            <BaseSelect
              v-model="selectedSeason"
              shape="curved"
              placeholder="Select Season"
              icon="ri:home-line"
              class="text-sm py-1 px-2"
            >
              <!-- Placeholder option -->
              <option disabled value="">{{ t('Select Season') }}</option>
              <!-- Options for season selection -->
              <option v-for="season in ['Spring', 'Summer', 'Fall','Winter']" :key="season" :value="season">{{ season }}</option>
            </BaseSelect>
          </div>

          <div class="ms-10 flex items-center gap-1 mt-5">
            <BaseButton
              type="submit"
              color="primary"
              class="w-24"
            >
              {{ t("Show") }}
            </BaseButton>
          </div>
        </form>
      </div>
    </BaseCard>
  </div></template>
