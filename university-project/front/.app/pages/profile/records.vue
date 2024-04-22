<script setup lang="ts">
import {useAppStore} from "~/stores/app";
import {storeToRefs} from 'pinia';
import {ref, watch} from 'vue';
import {useRoute, useRouter} from 'vue-router';

const app = useAppStore();
const router = useRouter();

definePageMeta({
  title: 'Orders',
  middleware: 'authenticated',
  preview: {
    title: 'Edit profile 4',
    description: 'For editing a user profile',
    categories: ['layouts', 'profile', 'forms'],
    src: '/img/screens/layouts-subpages-profile-4.png',
    srcDark: '/img/screens/layouts-subpages-profile-4-dark.png',
    order: 79,
  }
});
const route = useRoute();

const page = computed(() => parseInt((route.query.page as string) ?? '1'))
const filter = ref('')

const perPage = ref(2)

watch([page, perPage], () => {
  fetchOrders(page.value, perPage.value);
});

const {locale, locales} = useI18n()

const {t} = useI18n({useScope: "local"})
const query = computed(() => {
  return {
    filter: filter.value,
    perPage: perPage.value,
    page: page.value,
  }
})
function deleteRecord(recordId){
  app.deleteRecord(recordId)
}
const formatPrice = (price: number) => {
  if (price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  }
};
const fetchRecords = app.fetchRecords;


function statusColor(itemStatus: string) {
  switch (itemStatus) {
    case 'online':
      return 'success'
    case 'working':
      return 'info'
    case 'suspended':
      return 'warning'
    default:
      break
  }
}


const getOrderProgress = (order) => {
  const statusOrderMap = {
    not_processed: 0,
    processed: 100,
    cancelled: 100,
  };

  return statusOrderMap[order.status];
};

const getItemProgress = (item) => {
  const statusItemMap = {
    not_processed: 0,
    processed: 100,
    cancelled: 100,
  };

  return statusItemMap[item.status];
};
const initializeData = async () => {
  await fetchRecords();
};
initializeData()

</script>

<style scoped>
.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #ccc;
  margin-top: 4px;
  border-radius: 4px;
}

.progress-bar > div {
  height: 100%;
  background-color: #007BFF;
  border-radius: 4px;
  transition: width 0.3s ease-in-out;
}
</style>

<template>
  <div>
    <div class="ltablet:col-span-6 col-span-6 md:col-span-6 lg:col-span-6">
      <BaseCard rounded="lg" class="p-6">
        <div class="mb-6 flex items-center justify-between">
          <BaseHeading
            as="h3"
            size="md"
            weight="semibold"
            lead="tight"
            class="text-muted-800 dark:text-white"
          >
            <span>Records</span>
          </BaseHeading>

        </div>
        <div class="mb-2 space-y-5">

          <div v-for="record in app.getRecords" class="flex items-center gap-2">
                          <div>
                          <BaseHeading
                            as="h4"
                            size="sm"
                            weight="medium"
                            lead="snug"
                            class="text-muted-800 dark:text-white mb-10"
                          >
                            <div>Device Name: {{ record.device_name }}</div>
                            <div>Start Time: {{ record.start_time }}</div>
                            <div>End Time: {{ record.end_time }}</div>
                            <div>Consumption: {{ record.consumption }}</div>
                          </BaseHeading>
                        </div>
                        <div class="ms-auto flex items-center gap-1">
                          <BaseButtonIcon @click="deleteRecord(record.power_record_id)" rounded="full" small>
                            <Icon name="ri:delete-bin-fill" />
                          </BaseButtonIcon>
                        </div>

          </div>
        </div>
      </BaseCard>
    </div>
  </div>
</template>
