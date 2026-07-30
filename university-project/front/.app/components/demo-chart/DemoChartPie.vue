<script setup lang="ts">
import { ref, reactive, computed, watch, onMounted } from 'vue';
import { useAppStore } from "~/stores/app";
import { storeToRefs } from "pinia";
import { useI18n } from 'vue-i18n';
import {useAuthStore} from "~/stores/auth";
const { t } = useI18n({ useScope: "local" });


const app = useAppStore();
const { seasonDatas, seasonLabels  } = storeToRefs(app);

const authStore = useAuthStore();

const now = new Date();
function currentSeason(d = now) {
  const m = d.getMonth() + 1, day = d.getDate();
  if ((m === 3 && day >= 21) || m === 4 || m === 5 || (m === 6 && day <= 20)) return 'Spring';
  if ((m === 6 && day >= 21) || m === 7 || m === 8 || (m === 9 && day <= 22)) return 'Summer';
  if ((m === 9 && day >= 23) || m === 10 || m === 11 || (m === 12 && day <= 20)) return 'Fall';
  return 'Winter';
}
const selectedYear = ref<number>(now.getFullYear());
const selectedSeason = ref<string>(currentSeason());

const SEASON_LABELS = {
  Spring: 'بهار',
  Summer: 'تابستان',
  Fall: 'پاییز',
  Winter: 'زمستان',
};

const yearOptions = computed(() =>
  Array.from({ length: 7 }, (_, index) => now.getFullYear() - 5 + index).map(year => ({
    value: year,
    label: gregorianYearToJalaliLabel(year),
  })),
);

const seasonOptions = computed(() =>
  Object.entries(SEASON_LABELS).map(([value, label]) => ({ value, label })),
);

async function loadSeasonal() {
  if (authStore.isAdmin) {
    await app.fetchSeasonChartAdmin(selectedYear.value, selectedSeason.value);
  } else if (authStore.isMng) {
    await app.fetchSeasonChartMng(selectedYear.value, selectedSeason.value);
  } else {
    await app.fetchSeasonChart(selectedYear.value, selectedSeason.value);
  }
}

// Initial load on mount.
onMounted(async () => {
  await loadSeasonal();
});

// Any change in the year or season selectors instantly refreshes the chart
// (no submit button needed).
watch([selectedYear, selectedSeason], async () => {
  await loadSeasonal();
});

const { primary, info, success, warning, danger } = useTailwindColors();
const demoPie = reactive({
  type: 'pie',
  height: 335,
  series: computed(() => seasonDatas.value ?? []),
  options: computed(() => ({
    chart: { toolbar: { show: false } },
    dataLabels: {
      style: { fontSize: '12px', weight: 500 },
    },
    colors: [primary.value, success.value, info.value, danger.value, warning.value],
    labels: seasonLabels.value ?? [],
    noData: {
      text: 'داده‌ای برای این بازه وجود ندارد',
      style: { fontSize: '14px' },
    },
    responsive: [
      {
        breakpoint: 480,
        options: {
          chart: { width: 315, toolbar: { show: false } },
          legend: { position: 'top' },
        },
      },
    ],
    legend: { position: 'right', horizontalAlign: 'center' },
  })),
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
        <span>مصرف فصلی</span>
      </BaseHeading>
      <AddonApexcharts v-bind="demoPie" />
      <div class="border-muted-200 dark:border-muted-700 mt-6 border-t pt-6">
        <div class="flex flex-col gap-4 sm:flex-row sm:items-end">
          <!-- Year selection -->
          <BaseSelect
            v-model="selectedYear"
            shape="curved"
            label="سال"
            icon="ph:calendar-blank-duotone"
            class="flex-1"
          >
            <option v-for="year in yearOptions" :key="year.value" :value="year.value">{{ year.label }}</option>
          </BaseSelect>

          <!-- Season selection -->
          <BaseSelect
            v-model="selectedSeason"
            shape="curved"
            label="فصل"
            icon="ph:sun-duotone"
            class="flex-1"
          >
            <option v-for="s in seasonOptions" :key="s.value" :value="s.value">{{ s.label }}</option>
          </BaseSelect>
        </div>
      </div>
    </BaseCard>
  </div></template>
