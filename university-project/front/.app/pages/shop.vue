<script setup lang="ts">
import { useAppStore } from '~/stores/app'
import { storeToRefs } from 'pinia'
definePageMeta({ title: 'بازار انرژی', middleware: 'authenticated' })
const app = useAppStore()
const { batteries, battery } = storeToRefs(app)
const loading = ref(true)
const buying = ref<string | null>(null)
const updatingOffer = ref(false)
const errorMessage = ref('')
const search = ref('')
const page = ref(1)
const perPage = 6
const amounts = reactive<Record<string, number>>({})
const items = computed(() => (batteries.value || []).filter((x: any) => JSON.stringify(x).toLowerCase().includes(search.value.toLowerCase())))
const visibleItems = computed(() => items.value.slice((page.value - 1) * perPage, page.value * perPage))
watch(search, () => {
  page.value = 1
})
const key = (item: any) => String(item.id || item._id || item.battery_id)
const number = (value: any) => new Intl.NumberFormat('fa-IR').format(Number(value || 0))
async function load() {
  loading.value = true
  errorMessage.value = ''
  try {
    await Promise.all([app.fetchAllBattery(), app.fetchBattery()])
  }
  catch {
    errorMessage.value = 'بازار انرژی در دسترس نیست.'
  }
  finally {
    loading.value = false
  }
}
async function toggleOffer() {
  if (!battery.value) {
    errorMessage.value = 'برای ثبت عرضه، ابتدا باید باتری ذخیره‌ساز برای حساب شما تعریف شود.'
    return
  }
  updatingOffer.value = true
  errorMessage.value = ''
  try {
    await app.updateBatteryOffer(battery.value.status !== 'available')
    await load()
  }
  catch (error: any) {
    errorMessage.value = error?.response?.data?.detail === 'Battery not found.'
      ? 'باتری ذخیره‌ساز برای حساب شما پیدا نشد.'
      : 'تغییر وضعیت عرضه انجام نشد.'
  }
  finally {
    updatingOffer.value = false
  }
}
async function buy(item: any) {
  const id = key(item)
  const amount = Number(amounts[id])
  if (!Number.isFinite(amount) || amount <= 0 || amount > Number(item.saved_energy || 0)) {
    errorMessage.value = 'مقدار خرید باید بیشتر از صفر و کمتر از انرژی موجود باشد.'
    return
  }
  buying.value = id
  errorMessage.value = ''
  try {
    const result = await app.addOrder(item.user_id, item.id || item._id, amount, item.fee)
    item.saved_energy = Number(result?.remaining_energy ?? (Number(item.saved_energy) - amount))
    amounts[id] = 0
    await load()
  }
  catch (error: any) {
    const detail = error?.response?.data?.detail
    const messages: Record<string, string> = {
      'Insufficient saved energy.': 'انرژی موجود برای این خرید کافی نیست؛ فهرست بازار به‌روزرسانی شد.',
      'Battery not found.': 'این عرضه دیگر در بازار وجود ندارد.',
      'You cannot buy your own energy.': 'امکان خرید انرژی متعلق به حساب خودتان وجود ندارد.',
      'Order amount must be positive.': 'مقدار خرید باید بیشتر از صفر باشد.',
    }
    errorMessage.value = messages[detail] || 'ثبت سفارش انجام نشد. دوباره تلاش کنید.'
    await load()
  }
  finally {
    buying.value = null
  }
}
onMounted(load)
</script>
<template>
  <TairoContentWrapper data-tour="energy-market">
    <template #left>
      <BaseInput
        v-model="search"
        icon="lucide:search"
        placeholder="جست‌وجوی عرضه‌کننده…"
      />
    </template>
    <div class="mb-7" data-tour="energy-market">
      <BaseHeading as="h1" size="2xl">
        بازار تبادل انرژی
      </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
        انرژی مازاد ذخیره‌شده در ریزشبکه دانشگاه را با قیمت شفاف خریداری کنید.
      </BaseParagraph>
    </div>
    <BaseCard class="mb-6 border-primary-500 border-s-4 p-5">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <BaseHeading size="md">
            عرضه انرژی من
          </BaseHeading>
          <BaseParagraph v-if="battery" class="text-muted-500 mt-1">
            موجودی قابل فروش: {{ number(battery.saved_energy) }} کیلووات‌ساعت
            · وضعیت: {{ battery.status === 'available' ? 'فعال در بازار' : 'متوقف' }}
          </BaseParagraph>
          <BaseParagraph v-else class="text-muted-500 mt-1">
            هنوز باتری ذخیره‌ساز برای این حساب تعریف نشده است.
          </BaseParagraph>
        </div>
        <BaseButton
          :color="battery?.status === 'available' ? 'danger' : 'primary'"
          :loading="updatingOffer"
          :disabled="updatingOffer || !battery"
          @click="toggleOffer"
        >
          {{ battery?.status === 'available' ? 'توقف عرضه' : 'ثبت عرضه در بازار' }}
        </BaseButton>
      </div>
    </BaseCard>
    <BaseMessage
      v-if="errorMessage"
      type="danger"
      class="mb-4"
      @close="errorMessage=''"
    >
      {{ errorMessage }}
    </BaseMessage>
    <BaseCard v-if="loading" class="p-10 text-center">
      در حال دریافت عرضه‌های فعال…
    </BaseCard>
    <BaseCard v-else-if="!items.length" class="p-10 text-center">
      <Icon name="ph:battery-empty-duotone" class="text-muted-400 mx-auto size-12" /><BaseHeading class="mt-3">
        عرضه فعالی وجود ندارد
      </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
        پس از ذخیره انرژی مازاد، پیشنهادها اینجا نمایش داده می‌شوند.
      </BaseParagraph>
    </BaseCard>
    <div v-else class="grid gap-4 lg:grid-cols-2">
      <BaseCard
        v-for="item in visibleItems"
        :key="key(item)"
        class="overflow-hidden"
      >
        <div class="border-success-500 border-s-4 p-5">
          <div class="flex items-start justify-between gap-3">
            <div>
              <BaseHeading>{{ item.email||'عرضه‌کننده ریزشبکه' }}</BaseHeading><BaseTag
                color="success"
                variant="pastel"
                class="mt-2"
              >
                آماده معامله
              </BaseTag>
            </div><Icon name="ph:battery-charging-vertical-duotone" class="text-success-500 size-10" />
          </div><dl class="mt-5 grid grid-cols-2 gap-3">
            <div>
              <dt class="text-muted-500 text-xs">
                انرژی موجود
              </dt><dd class="font-semibold">
                {{ number(item.saved_energy) }} کیلووات‌ساعت
              </dd>
            </div><div>
              <dt class="text-muted-500 text-xs">
                نرخ واحد
              </dt><dd class="font-semibold">
                {{ number(item.fee) }} ریال
              </dd>
            </div>
          </dl><div class="mt-5 flex flex-col gap-2 sm:flex-row">
            <BaseInput
              v-model.number="amounts[key(item)]"
              type="number"
              min="1"
              :max="item.saved_energy"
              placeholder="مقدار خرید"
              class="flex-1"
            /><BaseButton
              color="primary"
              :loading="buying===key(item)"
              :disabled="buying!==null"
              @click="buy(item)"
            >
              ثبت خرید
            </BaseButton>
          </div>
        </div>
      </BaseCard>
    </div>
    <BasePagination
      previous-icon="lucide:chevron-right"
      next-icon="lucide:chevron-left"
      v-if="items.length > perPage"
      class="mt-6"
      :total-items="items.length"
      :item-per-page="perPage"
      :current-page="page"
      @update:current-page="page = $event"
    />
  </TairoContentWrapper>
</template>
