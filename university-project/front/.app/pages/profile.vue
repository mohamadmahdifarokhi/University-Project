<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useAppStore } from '~/stores/app'

definePageMeta({ title: 'پروفایل انرژی', middleware: 'authenticated' })
const app = useAppStore()
const localPath = useLocalePath()
const { email, area, apartment_no: apartmentNo } = storeToRefs(app)
const uploading = ref(false)
const uploadError = ref('')
const navigation = [
  { label: 'ساختمان و منابع', icon: 'ph:buildings-duotone', to: '/profile/blocks' },
  { label: 'سفارش‌های انرژی', icon: 'ph:receipt-duotone', to: '/profile/orders' },
  { label: 'سوابق مصرف', icon: 'ph:chart-line-up-duotone', to: '/profile/records' },
  { label: 'تجهیزات قابل انتخاب', icon: 'ph:plugs-connected-duotone', to: '/profile/products' },
  { label: 'امنیت حساب', icon: 'ph:shield-check-duotone', to: '/profile/settings' },
]

async function handleFileUpload(event: Event) {
  const file = (event.target as HTMLInputElement).files?.[0]
  if (!file) return
  uploading.value = true
  uploadError.value = ''
  try {
    await app.importExcel(file)
  }
  catch {
    uploadError.value = 'بارگذاری فایل انجام نشد. قالب و اتصال سرور را بررسی کنید.'
  }
  finally {
    uploading.value = false
  }
}

onMounted(() => app.fetchProfile())
</script>

<template>
  <div class="grid min-h-screen gap-8 lg:grid-cols-[260px_minmax(0,1fr)]">
    <aside>
      <BaseCard class="p-5">
        <div class="border-muted-200 dark:border-muted-700 border-b pb-4">
          <BaseHeading size="sm">
            {{ email || 'حساب کاربری' }}
          </BaseHeading>
          <BaseParagraph class="text-muted-500 mt-2">
            مساحت: {{ area || '—' }} مترمربع
          </BaseParagraph>
          <BaseParagraph class="text-muted-500">
            شماره واحد: {{ apartmentNo || '—' }}
          </BaseParagraph>
        </div>
        <nav class="mt-4" aria-label="منوی پروفایل">
          <NuxtLink
            v-for="item in navigation"
            :key="item.to"
            :to="localPath(item.to)"
            exact-active-class="!text-primary-600 !bg-primary-500/10"
            class="text-muted-500 hover:text-primary-600 focus-visible:ring-primary-500 flex items-center gap-2 rounded-lg p-3 transition-colors focus-visible:ring-2"
          >
            <Icon :name="item.icon" class="size-5" /><span>{{ item.label }}</span>
          </NuxtLink>
        </nav>
        <label class="border-muted-300 dark:border-muted-600 mt-4 block cursor-pointer rounded-lg border border-dashed p-3 text-center text-sm">
          <Icon name="ph:file-xls-duotone" class="text-success-500 me-1 size-5" />
          {{ uploading ? 'در حال بارگذاری…' : 'ورود سوابق از اکسل' }}
          <input
            class="sr-only"
            type="file"
            accept=".xlsx,.xls"
            :disabled="uploading"
            @change="handleFileUpload"
          >
        </label>
        <BaseMessage
          v-if="uploadError"
          type="danger"
          class="mt-3"
        >
          {{ uploadError }}
        </BaseMessage>
      </BaseCard>
    </aside>
    <main class="min-w-0">
      <NuxtPage />
    </main>
  </div>
</template>
