<script setup lang="ts">
import {onMounted} from "vue";
import {storeToRefs} from "pinia";
import {useAppStore} from "~/stores/app";
const app = useAppStore();

function addOrder(user_id, solar_panel_id, amount, fee) {
  app.addOrder(user_id, solar_panel_id, amount, fee)
}
const config = useRuntimeConfig()
if (import.meta.dev && !config.public.mapboxToken) {
  console.warn(
    'NUXT_PUBLIC_MAPBOX_TOKEN environment variable is not defined, mapbox features are disabled',
  )
}
const route = useRoute()
const router = useRouter()
const page = computed(() => parseInt((route.query.page as string) ?? '1'))
const amount = 0
const filter = ref('')
const perPage = ref(10)

watch([filter, perPage], () => {
  router.push({
    query: {
      page: undefined,
    },
  })
})

const query = computed(() => {
  return {
    filter: filter.value,
    perPage: perPage.value,
    page: page.value,
  }
})

const { data, pending, error, refresh } = await useFetch(
  '/api/company/members/',
  {
    query,
  },
)

const selected = ref<number[]>([])

const isAllVisibleSelected = computed(() => {
  return selected.value.length === data.value?.data.length
})

function toggleAllVisibleSelection() {
  if (isAllVisibleSelected.value) {
    selected.value = []
  }
  else {
    selected.value = data.value?.data.map(item => item.id) ?? []
  }
}

const {battery} = storeToRefs(app);

const fetchBattery = app.fetchBattery;


const initializeData = async () => {
  await fetchBattery();
}
onMounted(async () => {
    await initializeData();
  });

</script>

<template>
  <div>
    <div class="mb-4 flex items-center justify-between">
      <BaseHeading
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
      <ul class="space-y-3">
        <li>
          <NuxtLink to="#" class="group flex items-center justify-between">
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
              <span>{{ battery['saved_energy'] }}</span>
            </div>
          </NuxtLink>
        </li>
        <li>
          <NuxtLink to="#" class="group flex items-center justify-between">
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
              <span>{{ battery['sold_energy'] }}</span>
            </div>
          </NuxtLink>
        </li>
        <li>
<!--          <NuxtLink to="#" class="group flex items-center justify-between">-->
<!--            <BaseParagraph size="sm">-->
<!--              <span-->
<!--                class="text-muted-500 dark:text-muted-400 group-hover:text-primary-500 transition-colors duration-300"-->
<!--              >-->
<!--                Family-->
<!--              </span>-->
<!--            </BaseParagraph>-->
<!--            <div-->
<!--              class="bg-muted-200 dark:bg-muted-700 text-muted-500 dark:text-muted-200 flex size-7 items-center justify-center rounded-full text-xs"-->
<!--            >-->
<!--              <span>4</span>-->
<!--            </div>-->
<!--          </NuxtLink>-->
        </li>
      </ul>
    </div>
  </div>
</template>
