<script setup lang="ts">
import { useAppStore } from '~/stores/app'
import { storeToRefs } from 'pinia'

definePageMeta({ title: 'مدیریت کاربران', middleware: ['authenticated', 'is-admin'] })
useSeoMeta({ description: 'پنل مدیریت کاربران سامانه انرژی دانشگاه' })

const app = useAppStore()
const { allUsers } = storeToRefs(app)
const loading = ref(true)
const errorMessage = ref('')
const search = ref('')
const page = ref(1)
const perPage = 8
const selectedDevices = ref<any[]>([])
const isModalOpen = ref(false)

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return allUsers.value || []
  return (allUsers.value || []).filter((user: any) =>
    [user.email, user.role, user.status].some(value => String(value || '').toLowerCase().includes(q)),
  )
})
const visible = computed(() => filtered.value.slice((page.value - 1) * perPage, page.value * perPage))
watch(search, () => {
  page.value = 1
})

async function loadUsers() {
  loading.value = true
  errorMessage.value = ''
  try {
    await app.fetchusers()
  }
  catch {
    errorMessage.value = 'دریافت فهرست کاربران ممکن نشد. اتصال سرور را بررسی کنید.'
  }
  finally {
    loading.value = false
  }
}
function showDevices(devices: any[] = []) {
  selectedDevices.value = devices
  isModalOpen.value = true
}
onMounted(loadUsers)
</script>

<template>
  <TairoContentWrapper>
    <template #left>
      <BaseInput
        v-model="search"
        icon="lucide:search"
        placeholder="جست‌وجوی ایمیل، نقش یا وضعیت…"
      />
    </template>
    <div class="mb-6 flex flex-wrap items-end justify-between gap-4">
      <div>
        <BaseHeading
          as="h1"
          size="2xl"
          weight="semibold"
        >
          مدیریت کاربران
        </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
          کنترل دسترسی و منابع انرژی کاربران سامانه
        </BaseParagraph>
      </div>
      <BaseTag color="primary" variant="pastel">
        {{ filtered.length }} کاربر
      </BaseTag>
    </div>
    <BaseCard v-if="loading" class="p-8 text-center">
      <Icon name="svg-spinners:ring-resize" class="text-primary-500 mx-auto size-8" /><p class="mt-3">
        در حال دریافت کاربران…
      </p>
    </BaseCard>
    <BaseMessage v-else-if="errorMessage" type="danger">
      <div class="flex items-center justify-between gap-3">
        <span>{{ errorMessage }}</span><BaseButton size="sm" @click="loadUsers">
          تلاش دوباره
        </BaseButton>
      </div>
    </BaseMessage>
    <BaseCard v-else-if="!visible.length" class="p-10 text-center">
      <Icon name="ph:users-three-duotone" class="text-muted-400 mx-auto size-12" /><BaseHeading class="mt-3">
        کاربری یافت نشد
      </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
        عبارت جست‌وجو را تغییر دهید.
      </BaseParagraph>
    </BaseCard>
    <div v-else class="grid gap-3">
      <BaseCard
        v-for="user in visible"
        :key="user.id || user._id || user.email"
        class="p-4"
      >
        <div class="flex flex-wrap items-center justify-between gap-4">
          <div class="min-w-0">
            <BaseHeading size="sm" class="truncate">
              {{ user.email }}
            </BaseHeading><div class="mt-2 flex flex-wrap gap-2">
              <BaseTag
                size="sm"
                color="primary"
                variant="pastel"
              >
                {{ user.role || user.scope || 'کاربر' }}
              </BaseTag><BaseTag
                size="sm"
                :color="user.is_active === false ? 'danger' : 'success'"
                variant="pastel"
              >
                {{ user.is_active === false ? 'غیرفعال' : 'فعال' }}
              </BaseTag>
            </div>
          </div>
          <BaseButton size="sm" @click="showDevices(user.devices)">
            <Icon name="ph:plugs-connected-duotone" class="me-2" />مشاهده تجهیزات ({{ user.devices?.length || 0 }})
          </BaseButton>
        </div>
      </BaseCard>
    </div>
    <div v-if="filtered.length > perPage" class="mt-6">
      <BasePagination
        :total-items="filtered.length"
        :item-per-page="perPage"
        :current-page="page"
        @update:current-page="page = $event"
      />
    </div>
    <TairoModal
      :open="isModalOpen"
      size="md"
      @close="isModalOpen = false"
    >
      <template #header>
        <BaseHeading>تجهیزات کاربر</BaseHeading>
      </template><div class="p-4">
        <p v-if="!selectedDevices.length" class="text-muted-500">
          تجهیزی برای این کاربر ثبت نشده است.
        </p><ul v-else class="space-y-2">
          <li
            v-for="device in selectedDevices"
            :key="device.id || device.name"
            class="border-muted-200 dark:border-muted-700 rounded-lg border p-3"
          >
            {{ device.name || device.device_name || 'تجهیز بدون نام' }}
          </li>
        </ul>
      </div>
    </TairoModal>
  </TairoContentWrapper>
</template>
