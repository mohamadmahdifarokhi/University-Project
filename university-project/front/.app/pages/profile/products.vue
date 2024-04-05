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

const formatPrice = (price: number) => {
  if (price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  }
};
const {orders} = storeToRefs(app);
const fetchOrders = app.fetchOrders;
fetchOrders(page.value, perPage.value);

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
              <span>Available Products</span>
            </BaseHeading>
<!--            <NuxtLink-->
<!--              to="#"-->
<!--              class="bg-muted-100 hover:bg-muted-200 dark:bg-muted-700 dark:hover:bg-muted-900 text-primary-500 rounded-lg px-4 py-2 font-sans text-sm font-medium underline-offset-4 transition-colors duration-300 hover:underline"-->
<!--            >-->
<!--              View All-->
<!--            </NuxtLink>-->
          </div>
          <div class="mb-2 space-y-5">
            <!-- List item -->
            <div class="flex items-center gap-2">
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-blue-800 text-white shadow-xl shadow-blue-500/20 dark:shadow-blue-800/20"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa6-brands:linkedin-in" class="size-3"/>-->
<!--              </BaseIconBox>-->
              <div>
                <BaseHeading
                  as="h4"
                  size="sm"
                  weight="medium"
                  lead="snug"
                  class="text-muted-800 dark:text-white"
                >
                  <span>Iron</span>
                </BaseHeading>
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Linkedin Corp.</span>-->
<!--                </BaseParagraph>-->
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseButtonIcon rounded="full" small>
          <Icon name="ri:add-circle-fill" />
        </BaseButtonIcon>
<!--                <Icon-->
<!--                  name="ph:check-circle-duotone"-->
<!--                  class="text-success-500 size-4"-->
<!--                />-->
<!--                <span-->
<!--                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"-->
<!--                >-->
<!--                  $1,478.32-->
<!--                </span>-->
              </div>
            </div>
            <!-- List item -->
            <div class="flex items-center gap-2">
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-muted-900 dark:bg-muted-100 dark:text-muted-800 text-white"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa6-brands:github" class="size-3"/>-->
<!--              </BaseIconBox>-->
              <div>
                <BaseHeading
                  as="h4"
                  size="sm"
                  weight="medium"
                  lead="snug"
                  class="text-muted-800 dark:text-white"
                >
                  <span>Refrigerator</span>
                </BaseHeading>
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Github Inc.</span>-->
<!--                </BaseParagraph>-->
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseButtonIcon rounded="full" small>
          <Icon name="ri:add-circle-fill" />
        </BaseButtonIcon>
<!--                <Icon-->
<!--                  name="ph:check-circle-duotone"-->
<!--                  class="text-success-500 size-4"-->
<!--                />-->
<!--                <span-->
<!--                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"-->
<!--                >-->
<!--                  $1,478.32-->
<!--                </span>-->
              </div>

            </div>
            <!-- List item -->
            <div class="flex items-center gap-2">
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-rose-500 text-white shadow-xl shadow-rose-500/20 dark:shadow-rose-800/20"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa6-brands:invision" class="size-4"/>-->
<!--              </BaseIconBox>-->
              <div>
                <BaseHeading
                  as="h4"
                  size="sm"
                  weight="medium"
                  lead="snug"
                  class="text-muted-800 dark:text-white"
                >
                  <span>Oven</span>
                </BaseHeading>
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Invision Corp.</span>-->
<!--                </BaseParagraph>-->
              </div>
              <div class="ms-auto flex items-center gap-1">
                 <BaseButtonIcon rounded="full" small>
          <Icon name="ri:add-circle-fill" />
        </BaseButtonIcon>
<!--                <Icon-->
<!--                  name="ph:check-circle-duotone"-->
<!--                  class="text-success-500 size-4"-->
<!--                />-->
<!--                <span-->
<!--                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"-->
<!--                >-->
<!--                  $1,478.32-->
<!--                </span>-->
              </div>

            </div>
            <!-- List item -->
<!--            <div class="flex items-center gap-2">-->
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-sky-700 text-white shadow-xl shadow-sky-500/20 dark:shadow-sky-800/20"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa-brands:telegram-plane" class="size-4"/>-->
<!--              </BaseIconBox>-->
<!--              <div>-->
<!--                <BaseHeading-->
<!--                  as="h4"-->
<!--                  size="sm"-->
<!--                  weight="medium"-->
<!--                  lead="snug"-->
<!--                  class="text-muted-800 dark:text-white"-->
<!--                >-->
<!--                  <span>TLG</span>-->
<!--                </BaseHeading>-->
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Telegram Inc.</span>-->
<!--                </BaseParagraph>-->
<!--              </div>-->
<!--              <div class="ms-auto flex items-center gap-1">-->
<!--                 <BaseButtonIcon rounded="full" small>-->
<!--          <Icon name="ri:add-circle-fill" />-->
<!--        </BaseButtonIcon>-->
<!--&lt;!&ndash;                <Icon&ndash;&gt;-->
<!--&lt;!&ndash;                  name="ph:check-circle-duotone"&ndash;&gt;-->
<!--&lt;!&ndash;                  class="text-success-500 size-4"&ndash;&gt;-->
<!--&lt;!&ndash;                />&ndash;&gt;-->
<!--&lt;!&ndash;                <span&ndash;&gt;-->
<!--&lt;!&ndash;                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"&ndash;&gt;-->
<!--&lt;!&ndash;                >&ndash;&gt;-->
<!--&lt;!&ndash;                  $1,478.32&ndash;&gt;-->
<!--&lt;!&ndash;                </span>&ndash;&gt;-->
<!--              </div>-->

<!--            </div>-->
<!--            &lt;!&ndash; List item &ndash;&gt;-->
<!--            <div class="flex items-center gap-2">-->
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-emerald-500 text-white shadow-xl shadow-emerald-500/20 dark:shadow-emerald-800/20"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa-brands:kickstarter-k" class="size-4"/>-->
<!--              </BaseIconBox>-->
<!--              <div>-->
<!--                <BaseHeading-->
<!--                  as="h4"-->
<!--                  size="sm"-->
<!--                  weight="medium"-->
<!--                  lead="snug"-->
<!--                  class="text-muted-800 dark:text-white"-->
<!--                >-->
<!--                  <span>KCK</span>-->
<!--                </BaseHeading>-->
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Kickstarter Inc.</span>-->
<!--                </BaseParagraph>-->
<!--              </div>-->
<!--              <div class="ms-auto flex items-center gap-1">-->
<!--                 <BaseButtonIcon rounded="full" small>-->
<!--          <Icon name="ri:add-circle-fill" />-->
<!--        </BaseButtonIcon>-->
<!--&lt;!&ndash;                <Icon&ndash;&gt;-->
<!--&lt;!&ndash;                  name="ph:check-circle-duotone"&ndash;&gt;-->
<!--&lt;!&ndash;                  class="text-success-500 size-4"&ndash;&gt;-->
<!--&lt;!&ndash;                />&ndash;&gt;-->
<!--&lt;!&ndash;                <span&ndash;&gt;-->
<!--&lt;!&ndash;                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"&ndash;&gt;-->
<!--&lt;!&ndash;                >&ndash;&gt;-->
<!--&lt;!&ndash;                  $1,478.32&ndash;&gt;-->
<!--&lt;!&ndash;                </span>&ndash;&gt;-->
<!--              </div>-->

<!--            </div>-->
            <!-- List item -->
<!--            <div class="flex items-center gap-2">-->
<!--              <BaseIconBox-->
<!--                rounded="full"-->
<!--                size="xs"-->
<!--                class="bg-yellow-500 text-white shadow-xl shadow-yellow-500/20 dark:shadow-yellow-800/20"-->
<!--                color="none"-->
<!--              >-->
<!--                <Icon name="fa-brands:google" class="size-4"/>-->
<!--              </BaseIconBox>-->
<!--              <div>-->
<!--                <BaseHeading-->
<!--                  as="h4"-->
<!--                  size="sm"-->
<!--                  weight="medium"-->
<!--                  lead="snug"-->
<!--                  class="text-muted-800 dark:text-white"-->
<!--                >-->
<!--                  <span>GGL</span>-->
<!--                </BaseHeading>-->
<!--                <BaseParagraph lead="none" size="xs">-->
<!--                  <span class="text-muted-400">Google Corp.</span>-->
<!--                </BaseParagraph>-->
<!--              </div>-->
<!--              <div class="ms-auto flex items-center gap-1">-->
<!--                 <BaseButtonIcon rounded="full" small>-->
<!--          <Icon name="ri:add-circle-fill" />-->
<!--        </BaseButtonIcon>-->
<!--&lt;!&ndash;                <Icon&ndash;&gt;-->
<!--&lt;!&ndash;                  name="ph:check-circle-duotone"&ndash;&gt;-->
<!--&lt;!&ndash;                  class="text-success-500 size-4"&ndash;&gt;-->
<!--&lt;!&ndash;                />&ndash;&gt;-->
<!--&lt;!&ndash;                <span&ndash;&gt;-->
<!--&lt;!&ndash;                  class="text-muted-600 dark:text-muted-400 font-sans text-sm font-medium"&ndash;&gt;-->
<!--&lt;!&ndash;                >&ndash;&gt;-->
<!--&lt;!&ndash;                  $1,478.32&ndash;&gt;-->
<!--&lt;!&ndash;                </span>&ndash;&gt;-->
<!--              </div>-->

<!--            </div>-->
          </div>
        </BaseCard>
      </div>
  </div>
</template>
