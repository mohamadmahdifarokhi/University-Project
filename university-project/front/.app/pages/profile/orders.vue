<script setup lang="ts">
import {useAppStore} from "~/stores/app";
import {storeToRefs} from "pinia";
import {onMounted} from "vue";
const app = useAppStore();

// definePageMeta({
//   title: 'Flex List',
//   preview: {
//     title: 'Flex list 3',
//     description: 'For list views and collections',
//     categories: ['layouts', 'lists'],
//     src: '/img/screens/layouts-list-flex-3.png',
//     srcDark: '/img/screens/layouts-list-flex-3-dark.png',
//     order: 43,
//   },
// })


const {sellOrders, buyOrders} = storeToRefs(app);


const fetchSellOrders = app.fetchSellOrders;
const fetchBuyOrders = app.fetchBuyOrders;



const initializeData = async () => {
  await fetchSellOrders();
  await fetchBuyOrders();
}
onMounted(async () => {
    await initializeData();
  });

</script>

<template>
  <div>
    <TairoContentWrapperTabbed
      :labels="['Buy', 'Sell']"
      reverse
      rounded="lg"
    >
      <template #left>
        <BaseInput
          v-model="filter"
          rounded="lg"
          icon="lucide:search"
          placeholder="Filter courses..."
          :classes="{
            wrapper: 'w-full sm:w-auto',
          }"
        />
      </template>
      <template #tab-1>
<!--{{sellOrders}}-->
<!--            {{buyOrders}}-->
<!--            {{ app.getSellOrders }}-->
<!--            {{ app.getBuyOrders }}-->
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
              v-for="(item, index) in app.getSellOrders"
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

          <div v-if="!pending && data?.data.length !== 0" class="pt-6">
            <BasePagination
              :total-items="data?.total ?? 0"
              :item-per-page="perPage"
              :current-page="page"
              rounded="full"
            />
          </div>
        </div>
      </template>


      <template #tab-2>
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
              v-for="(item, index) in app.getBuyOrders"
              :key="index"
              rounded="sm"
            >
              <template #start>
                <DemoFlexTableStart
                  label="Seller"
                  :hide-label="index > 0"
                  :title="item.seller_id"
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

          <div v-if="!pending && data?.data.length !== 0" class="pt-6">
            <BasePagination
              :total-items="data?.total ?? 0"
              :item-per-page="perPage"
              :current-page="page"
              rounded="full"
            />
          </div>
        </div>
      </template>
    </TairoContentWrapperTabbed>
  </div>
</template>
