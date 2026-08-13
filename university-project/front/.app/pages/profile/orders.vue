<script setup lang="ts">
import { useAppStore } from '~/stores/app'
import { storeToRefs } from 'pinia'
import { toJalaliDateTime } from '~/utils/jalali'
definePageMeta({ title: 'سفارش‌های انرژی', middleware: 'authenticated' })
const app = useAppStore()
const { sellOrders, buyOrders } = storeToRefs(app)
const loading = ref(true)
const errorMessage = ref('')
const filter = ref('')
const active = ref<'buy' | 'sell'>('buy')
const page = ref(1)
const perPage = 6
const source = computed(() => active.value === 'buy' ? buyOrders.value : sellOrders.value)
const rows = computed(() => (source.value || []).filter((x: any) => JSON.stringify(x).toLowerCase().includes(filter.value.toLowerCase())))
const visibleRows = computed(() => rows.value.slice((page.value - 1) * perPage, page.value * perPage))
watch([filter, active], () => {
  page.value = 1
})
const money = (n: any) => new Intl.NumberFormat('fa-IR').format(Number(n || 0))
const date = (v: any) => toJalaliDateTime(v) || '—'
const counterpartyName = (item: any) => {
  const name = active.value === 'buy' ? item.seller_name : item.buyer_name
  return name || 'کاربر ناشناس'
}
async function load() {
  loading.value = true
  errorMessage.value = ''
  try {
    await Promise.all([app.fetchBuyOrders(), app.fetchSellOrders()])
  }
  catch {
    errorMessage.value = 'دریافت تاریخچه سفارش‌ها ممکن نشد.'
  }
  finally {
    loading.value = false
  }
}
onMounted(load)
</script>
<template>
  <section data-tour="energy-orders">
    <div class="mb-6">
      <BaseHeading as="h1" size="xl">
        تاریخچه تبادل انرژی
      </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
        خرید و فروش انرژی ذخیره‌شده را یک‌جا پیگیری کنید.
      </BaseParagraph>
    </div>
    <div class="mb-5 flex flex-wrap gap-2">
      <BaseButton :color="active==='buy'?'primary':'default'" @click="active='buy'">
        خریدها
      </BaseButton><BaseButton :color="active==='sell'?'primary':'default'" @click="active='sell'">
        فروش‌ها
      </BaseButton><BaseInput
        v-model="filter"
        class="sm:ms-auto"
        icon="lucide:search"
        placeholder="جست‌وجوی سفارش…"
      />
    </div>
    <BaseCard v-if="loading" class="p-8 text-center">
      در حال دریافت سفارش‌ها…
    </BaseCard>
    <BaseMessage v-else-if="errorMessage" type="danger">
      {{ errorMessage }} <BaseButton
        size="sm"
        class="ms-2"
        @click="load"
      >
        تلاش دوباره
      </BaseButton>
    </BaseMessage>
    <BaseCard v-else-if="!rows.length" class="p-10 text-center">
      <Icon name="ph:receipt-duotone" class="text-muted-400 mx-auto size-12" /><BaseHeading class="mt-3">
        هنوز سفارشی ثبت نشده است
      </BaseHeading><BaseButton
        to="/shop"
        color="primary"
        class="mt-4"
      >
        مشاهده بازار انرژی
      </BaseButton>
    </BaseCard>
    <div v-else class="space-y-3">
      <BaseCard
        v-for="item in visibleRows"
        :key="item.id || item._id || item.created_at"
        class="p-4"
      >
        <div class="grid gap-4 sm:grid-cols-4">
          <div><small class="text-muted-500">طرف معامله</small><p>{{ counterpartyName(item) }}</p></div><div><small class="text-muted-500">مقدار انرژی</small><p>{{ money(item.amount) }} کیلووات‌ساعت</p></div><div><small class="text-muted-500">مبلغ</small><p>{{ money(item.fee) }} تومان</p></div><div><small class="text-muted-500">زمان ثبت</small><p>{{ date(item.created_at) }}</p></div>
        </div>
      </BaseCard>
    </div>
    <BasePagination
      previous-icon="lucide:chevron-right"
      next-icon="lucide:chevron-left"
      v-if="rows.length > perPage"
      class="mt-6"
      :total-items="rows.length"
      :item-per-page="perPage"
      :current-page="page"
      @update:current-page="page = $event"
    />
  </section>
</template>
