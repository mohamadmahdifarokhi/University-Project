<script setup lang="ts">
import { useAppStore } from '~/stores/app'
import { storeToRefs } from 'pinia'

definePageMeta({ title: 'سوابق مصرف', middleware: 'authenticated' })

const app = useAppStore()
const { records } = storeToRefs(app)
const loading = ref(true)
const errorMessage = ref('')
const deleting = ref<string | null>(null)
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

onMounted(load)
</script>
<template>
  <section>
    <div class="mb-6">
      <BaseHeading as="h1" size="xl">
        سوابق مصرف برق
      </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
        داده‌های ثبت‌شده برای تحلیل الگوی مصرف تجهیزات
      </BaseParagraph>
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
        v-for="x in records"
        :key="x.power_record_id"
        class="p-4"
      >
        <div class="grid items-center gap-4 sm:grid-cols-5">
          <div><small class="text-muted-500">تجهیز</small><p>{{ x.device_name }}</p></div><div><small class="text-muted-500">شروع</small><p>{{ date(x.start_time) }}</p></div><div><small class="text-muted-500">پایان</small><p>{{ date(x.end_time) }}</p></div><div><small class="text-muted-500">مصرف</small><p>{{ x.consumption }} کیلووات‌ساعت</p></div><BaseButton
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
  </section>
</template>
