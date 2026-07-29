<script setup lang="ts">
import { useAppStore } from '~/stores/app'
import { storeToRefs } from 'pinia'

definePageMeta({ title: 'تجهیزات قابل انتخاب', middleware: 'authenticated' })

const app = useAppStore()
const { devices } = storeToRefs(app)
const loading = ref(true)
const errorMessage = ref('')
const adding = ref<string | null>(null)

async function load() {
  loading.value = true
  errorMessage.value = ''
  try {
    await app.fetchDevices()
  }
  catch {
    errorMessage.value = 'فهرست تجهیزات دریافت نشد.'
  }
  finally {
    loading.value = false
  }
}

async function add(device: any) {
  adding.value = String(device.id)
  try {
    await app.addDevice(device.id)
  }
  catch {
    errorMessage.value = 'افزودن تجهیز انجام نشد.'
  }
  finally {
    adding.value = null
  }
}

onMounted(load)
</script>
<template>
  <section>
    <div class="mb-6">
      <BaseHeading as="h1" size="xl">
        تجهیزات قابل انتخاب
      </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
        مصرف‌کننده‌های ساختمان را برای ثبت و تحلیل مصرف انرژی فعال کنید.
      </BaseParagraph>
    </div><BaseCard v-if="loading" class="p-8 text-center">
      در حال دریافت تجهیزات…
    </BaseCard><BaseMessage v-else-if="errorMessage" type="danger">
      {{ errorMessage }} <BaseButton size="sm" @click="load">
        تلاش دوباره
      </BaseButton>
    </BaseMessage><BaseCard v-else-if="!devices.length" class="p-10 text-center">
      تجهیز فعالی در سامانه تعریف نشده است.
    </BaseCard><div v-else class="space-y-3">
      <BaseCard
        v-for="x in devices"
        :key="x.id"
        class="p-4"
      >
        <div class="flex items-center justify-between gap-4">
          <div>
            <BaseHeading size="sm">
              {{ x.name }}
            </BaseHeading><BaseParagraph class="text-muted-500 mt-1">
              توان نامی: {{ x.power||x.consumption||'—' }} وات
            </BaseParagraph>
          </div><BaseButton
            color="primary"
            size="sm"
            :loading="adding===String(x.id)"
            @click="add(x)"
          >
            افزودن
          </BaseButton>
        </div>
      </BaseCard>
    </div>
  </section>
</template>
