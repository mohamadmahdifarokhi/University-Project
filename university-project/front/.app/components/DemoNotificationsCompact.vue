<script setup lang="ts">
import { onMounted, ref, computed, watch } from "vue";
import { storeToRefs } from "pinia";
import { useAppStore } from "~/stores/app";
import { useRuntimeConfig, useRoute, useRouter, useFetch } from "#imports";

const app = useAppStore();
const { battery } = storeToRefs(app);
const fetchBattery = app.fetchBattery;

async function addOrder(user_id: number, solar_panel_id: number, amount: number, fee: number) {
  app.addOrder(user_id, solar_panel_id, amount, fee);
}

const config = useRuntimeConfig();
if (import.meta.env.DEV && !config.public.mapboxToken) {
  console.warn(
    'NUXT_PUBLIC_MAPBOX_TOKEN environment variable is not defined, mapbox features are disabled',
  );
}

const route = useRoute();
const router = useRouter();
const page = computed(() => parseInt((route.query.page as string) ?? '1'));
const filter = ref('');
const perPage = ref(10);

watch([filter, perPage], () => {
  router.push({
    query: {
      page: undefined,
    },
  });
});

const query = computed(() => {
  return {
    filter: filter.value,
    perPage: perPage.value,
    page: page.value,
  };
});

const { data, pending, error, refresh } = await useFetch(
  '/api/company/members/',
  {
    query,
  },
);

const selected = ref<number[]>([]);

const isAllVisibleSelected = computed(() => {
  return selected.value.length === data.value?.data.length;
});

function toggleAllVisibleSelection() {
  if (isAllVisibleSelected.value) {
    selected.value = [];
  } else {
    selected.value = data.value?.data.map(item => item.id) ?? [];
  }
}

const initializeData = async () => {
  await fetchBattery();
};

onBeforeMount(async () => {
  await initializeData();
});

function createBattery() {
  // Logic to create a battery, e.g., calling an API or updating the store

  app.addBattery(0,0)
  window.location.reload();

}
</script>

<template>
  <div>
    <div class="mb-4 flex items-center justify-between">
      <BaseHeading
        v-if="battery"
        as="h3"
        size="sm"
        weight="semibold"
        lead="tight"
        class="text-muted-800 dark:text-white"
      >
        <span>Battery Status (kw/h)</span>
      </BaseHeading>
    </div>
    <div>
      <ul class="space-y-3" v-if="battery">
        <li>
          <NuxtLink class="group flex items-center justify-between">
            <BaseParagraph size="sm">
              <span
                class="text-muted-500 dark:text-muted-400 group-hover:text-primary-500 transition-colors duration-300"
              >
                Saved Energy
              </span>
            </BaseParagraph>
            <div
              class="bg-muted-200 dark:bg-muted-700 text-muted-500 dark:text-muted-200 flex size-7 items-center justify-center rounded-full text-xs"
            >
              <span>{{ battery.saved_energy }}</span>
            </div>
          </NuxtLink>
        </li>
        <li>
          <NuxtLink class="group flex items-center justify-between">
            <BaseParagraph size="sm">
              <span
                class="text-muted-500 dark:text-muted-400 group-hover:text-primary-500 transition-colors duration-300"
              >
                Sold Energy
              </span>
            </BaseParagraph>
            <div
              class="bg-muted-200 dark:bg-muted-700 text-muted-500 dark:text-muted-200 flex size-7 items-center justify-center rounded-full text-xs"
            >
              <span>{{ battery.sold_energy }}</span>
            </div>
          </NuxtLink>
        </li>
      </ul>
      <div v-else>
        <button @click="createBattery" class="btn btn-primary">Create Battery</button>
      </div>
    </div>
  </div>
</template>
