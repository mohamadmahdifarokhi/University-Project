<script setup lang="ts">
import {onMounted} from "vue";
import {storeToRefs} from "pinia";
import {useAppStore} from "~/stores/app";
const app = useAppStore();

definePageMeta({
  title: 'Table List',
  preview: {
    title: 'Table list 1',
    description: 'For list views and collections',
    categories: ['layouts', 'lists'],
    src: '/img/screens/layouts-table-list-1.png',
    srcDark: '/img/screens/layouts-table-list-1-dark.png',
    order: 44,
  },
})
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

const {solarPanels, batteries} = storeToRefs(app);

const fetchSolarPanels = app.fetchSolarPanels;
const fetchAllBattery = app.fetchAllBattery;


const initializeData = async () => {
  await fetchSolarPanels();
  await fetchAllBattery();
}
onMounted(async () => {
    await initializeData();
  });

</script>

<template>
  <div>
    <TairoContentWrapper>
      <template #left>
        <BaseInput
          v-model="filter"
          icon="lucide:search"
          placeholder="Filter users..."
          :classes="{
            wrapper: 'w-full sm:w-auto',
          }"
        />
      </template>
      <template #right>
        <BaseSelect
          v-model="perPage"
          label=""
          :classes="{
            wrapper: 'w-full sm:w-40',
          }"
        >
          <option :value="10">
            10 per page
          </option>
          <option :value="25">
            25 per page
          </option>
          <option :value="50">
            50 per page
          </option>
          <option :value="100">
            100 per page
          </option>
        </BaseSelect>
      </template>
      <div>
        <div v-if="!pending && data?.data.length === 0">
          <BasePlaceholderPage
            title="No matching results"
            subtitle="Looks like we couldn't find any matching results for your search terms. Try other search terms."
          >
            <template #image>
              <img
                class="block dark:hidden"
                src="/img/illustrations/placeholders/flat/placeholder-search-4.svg"
                alt="Placeholder image"
              >
              <img
                class="hidden dark:block"
                src="/img/illustrations/placeholders/flat/placeholder-search-4-dark.svg"
                alt="Placeholder image"
              >
            </template>
          </BasePlaceholderPage>
        </div>
        <div v-else>
          <div class="w-full">
            <TairoTable rounded="sm" :scrollable="false">
              <template #header>
<!--                <TairoTableHeading-->
<!--                  uppercase-->
<!--                  spaced-->
<!--                  class="p-4"-->

<!--                >-->
<!--                  <div class="flex items-center">-->
<!--                    <BaseCheckbox-->
<!--                      :model-value="isAllVisibleSelected"-->
<!--                      :indeterminate="-->
<!--                        selected.length > 0 && !isAllVisibleSelected-->
<!--                      "-->
<!--                      name="table-1-main"-->
<!--                      rounded="sm"-->
<!--                      color="primary"-->
<!--                      @click="toggleAllVisibleSelection"-->
<!--                    />-->
<!--                  </div>-->
<!--                </TairoTableHeading>-->
                <TairoTableHeading uppercase spaced>
                  Users
                </TairoTableHeading>
                <TairoTableHeading uppercase spaced>
                  Saved
                </TairoTableHeading>
                <TairoTableHeading uppercase spaced>
                  Status
                </TairoTableHeading>
                <TairoTableHeading uppercase spaced>
                  Sold
                </TairoTableHeading>
                <TairoTableHeading
                  uppercase
                  spaced
                  class="text-end"
                >
                  Action
                </TairoTableHeading>
              </template>

              <TairoTableRow v-if="selected.length > 0" :hoverable="false">
                <TairoTableCell
                  colspan="6"
                  class="bg-success-100 text-success-700 dark:bg-success-700 dark:text-success-100 p-4"
                >
                  You have selected {{ selected.length }} items of the total
                  {{ data?.total }} items.
                  <a
                    href="#"
                    class="outline-none hover:underline focus:underline"
                  >Click here to everything</a>
                </TairoTableCell>
              </TairoTableRow>

              <TairoTableRow v-for="item in batteries">
<!--                <TairoTableCell spaced>-->
<!--                  <div class="flex items-center">-->
<!--                    <BaseCheckbox-->
<!--                      v-model="selected"-->
<!--                      :value="item.id"-->
<!--                      :name="`item-checkbox-${item.id}`"-->
<!--                      rounded="sm"-->
<!--                      color="primary"-->
<!--                    />-->
<!--                  </div>-->
<!--                </TairoTableCell>-->
                <TairoTableCell spaced>
                  <div class="flex items-center">
<!--                    <BaseAvatar-->
<!--                      :src="item.picture"-->
<!--                      :text="item.initials"-->
<!--                      :class="getRandomColor()"-->
<!--                    />-->
                    <div class="ms-3 leading-none">
                      <h4 class="font-sans text-sm font-medium">
                        {{ item.email }}
                      </h4>

                    </div>
                  </div>
                </TairoTableCell>
                <TairoTableCell light spaced>
                  {{ item.saved_energy }}
                </TairoTableCell>
                <TairoTableCell spaced class="capitalize">
                  <BaseTag
                    v-if="item.status === 'available'"
                    color="success"
                    variant="pastel"
                    rounded="full"
                    size="sm"
                    class="font-medium"
                  >
                    {{ item.status }}
                  </BaseTag>
                  <BaseTag
                    v-else-if="item.status === 'Unavailable'"
                    color="info"
                    variant="pastel"
                    rounded="full"
                    size="sm"
                    class="font-medium"
                  >
                    {{ item.status }}
                  </BaseTag>
                  <BaseTag
                    v-else-if="item.status === 'busy'"
                    color="warning"
                    variant="pastel"
                    rounded="full"
                    size="sm"
                    class="font-medium"
                  >
                    {{ item.status }}
                  </BaseTag>
                  <BaseTag
                    v-else-if="item.status === 'offline'"
                    color="muted"
                    variant="pastel"
                    rounded="full"
                    size="sm"
                    class="font-medium"
                  >
                    {{ item.status }}
                  </BaseTag>
                </TairoTableCell>
                <TairoTableCell spaced>
                  {{ item.sold_energy }}
                </TairoTableCell>

                <TairoTableCell spaced>
                  <div class="flex justify-center">
                    <BaseInput
    v-model="amount"
    type="number"
    placeholder="Enter amount..."
    :classes="{
      wrapper: 'w-full sm:w-auto',
    }"
  />
                    <BaseButtonIcon class="ms-3" @click="addOrder(item.user_id, item.id, amount, item.fee)" rounded="full" small>
                  <Icon name="ri:add-circle-fill"/>
                </BaseButtonIcon>
<!--                    <BaseDropdown-->
<!--                      variant="context"-->
<!--                      label="Dropdown"-->
<!--                      orientation="end"-->
<!--                      rounded="md"-->
<!--                    >-->
<!--                      <BaseDropdownItem-->
<!--                        to="#"-->
<!--                        title="User"-->
<!--                        text="View details"-->
<!--                        rounded="md"-->
<!--                      />-->
<!--                    </BaseDropdown>-->
                  </div>
                </TairoTableCell>
              </TairoTableRow>
            </TairoTable>
          </div>
          <div class="mt-6">
            <BasePagination
              :total-items="data?.total ?? 0"
              :item-per-page="perPage"
              :current-page="page"
              rounded="lg"
            />
          </div>
        </div>
      </div>
    </TairoContentWrapper>
  </div>
</template>
