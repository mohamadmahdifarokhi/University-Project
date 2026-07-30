<script setup lang="ts">
import { useAppStore } from '~/stores/app'
import { storeToRefs } from 'pinia'

definePageMeta({ title: 'سوابق مصرف', middleware: 'authenticated' })

const app = useAppStore()
const { records } = storeToRefs(app)
const loading = ref(true)
const errorMessage = ref('')
const deleting = ref<string | null>(null)
const uploading = ref(false)
const page = ref(1)
const perPage = 20
const visibleRecords = computed(() => records.value.slice((page.value - 1) * perPage, page.value * perPage))
const date = (value: any) => value
  ? new Intl.DateTimeFormat('fa-IR', { dateStyle: 'medium', timeStyle: 'short' }).format(new Date(value))
  : '—'

async function load() {
  loading.value = true
  errorMessage.value = ''
  try {
    await app.fetchRecords()
  }
  catch {
    errorMessage.value = 'سوابق مصرف دریافت نشد.'
  }
  finally {
    loading.value = false
  }
}

async function remove(record: any) {
  if (!confirm('این سابقه مصرف حذف شود؟')) return
  deleting.value = record.power_record_id
  try {
    await app.deleteRecord(record.power_record_id)
    await load()
  }
  catch {
    errorMessage.value = 'حذف سابقه انجام نشد.'
  }
  finally {
    deleting.value = null
  }
}

async function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  uploading.value = true
  errorMessage.value = ''
  try {
    await app.importExcel(file)
    await load()
  }
  catch {
    errorMessage.value = 'بارگذاری فایل انجام نشد. قالب فایل و پاسخ سرور را بررسی کنید.'
  }
  finally {
    uploading.value = false
    input.value = ''
  }
}

onMounted(load)
</script>
<template>
  <section data-tour="consumption-records">
    <div class="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        <BaseHeading as="h1" size="xl">
          سوابق مصرف برق
        </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
          داده‌های ثبت‌شده برای تحلیل الگوی مصرف تجهیزات
        </BaseParagraph>
      </div>
      <div class="flex flex-wrap items-center gap-2" data-tour="excel-import">
        <a
          href="/templates/energy-records-template.xlsx"
          download="نمونه-ورود-سوابق-مصرف.xlsx"
          class="border-muted-300 dark:border-muted-700 text-muted-700 dark:text-muted-200 hover:bg-muted-100 dark:hover:bg-muted-800 inline-flex items-center gap-2 rounded-lg border px-4 py-2 text-sm font-medium transition-colors"
        >
          <Icon name="ph:download-simple-duotone" class="size-5" />
          دانلود فایل نمونه
        </a>
        <label
          class="bg-primary-500 hover:bg-primary-600 inline-flex cursor-pointer items-center gap-2 rounded-lg px-4 py-2 text-sm font-medium text-white"
        >
          <Icon name="ph:file-xls-duotone" class="size-5" />
          {{ uploading ? 'در حال بارگذاری…' : 'ورود سوابق از اکسل' }}
          <input
            class="sr-only"
            type="file"
            accept=".xlsx"
            :disabled="uploading"
            @change="handleFileUpload"
          >
        </label>
      </div>
    </div><BaseCard v-if="loading" class="p-8 text-center">
      در حال دریافت سوابق…
    </BaseCard><BaseMessage v-else-if="errorMessage" type="danger">
      {{ errorMessage }} <BaseButton size="sm" @click="load">
        تلاش دوباره
      </BaseButton>
    </BaseMessage><BaseCard v-else-if="!records.length" class="p-10 text-center">
      هنوز سابقه مصرفی ثبت نشده است.
    </BaseCard><div v-else class="space-y-3">
      <BaseCard
        v-for="x in visibleRecords"
        :key="x.power_record_id"
        class="p-4"
      >
        <div class="grid items-center gap-4 sm:grid-cols-5">
          <div><small class="text-muted-500">تجهیز</small><p>{{ x.device_name }}</p></div><div><small class="text-muted-500">شروع</small><p>{{ date(x.start_time) }}</p></div><div><small class="text-muted-500">پایان</small><p>{{ date(x.end_time) }}</p></div><div><small class="text-muted-500">مصرف</small><p>{{ x.consumption }} وات‌ساعت</p></div><BaseButton
            color="danger"
            size="sm"
            :loading="deleting===x.power_record_id"
            @click="remove(x)"
          >
            حذف
          </BaseButton>
        </div>
      </BaseCard>
    </div>
    <BasePagination
      previous-icon="lucide:chevron-right"
      next-icon="lucide:chevron-left"
      v-if="records.length > perPage"
      class="mt-6"
      :total-items="records.length"
      :item-per-page="perPage"
      :current-page="page"
      @update:current-page="page = $event"
    />
  </section>
</template>
