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
const isCreateModalOpen = ref(false)
const creating = ref(false)
const createError = ref('')
const createForm = reactive({ email: '', password: '', isAdmin: false })

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
function openCreateModal() {
  createError.value = ''
  createForm.email = ''
  createForm.password = ''
  createForm.isAdmin = false
  isCreateModalOpen.value = true
}
async function createUser() {
  createError.value = ''
  if (!createForm.email || !createForm.password) {
    createError.value = 'ایمیل و رمز عبور را وارد کنید.'
    return
  }
  if (createForm.password.length < 6) {
    createError.value = 'رمز عبور باید حداقل ۶ کاراکتر باشد.'
    return
  }
  creating.value = true
  try {
    await app.createManagedUser({
      email: createForm.email,
      password: createForm.password,
      is_admin: createForm.isAdmin,
    })
    isCreateModalOpen.value = false
    await loadUsers()
  }
  catch (error: any) {
    createError.value = error?.response?.data?.detail || 'ثبت کاربر انجام نشد. اطلاعات را بررسی کنید.'
  }
  finally {
    creating.value = false
  }
}
onMounted(loadUsers)
</script>

<template>
  <TairoContentWrapper data-tour="admin-panel">
    <template #left>
      <BaseInput
        v-model="search"
        icon="lucide:search"
        placeholder="جست‌وجوی ایمیل، نقش یا وضعیت…"
      />
    </template>
    <div class="mb-6 flex flex-wrap items-end justify-between gap-4" data-tour="admin-panel">
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
      <div class="flex items-center gap-2">
        <BaseTag color="primary" variant="pastel">
          {{ filtered.length }} کاربر
        </BaseTag>
        <BaseButton color="primary" size="sm" @click="openCreateModal">
          <Icon name="ph:user-plus-duotone" class="me-1 size-4" />افزودن کاربر
        </BaseButton>
      </div>
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
        previous-icon="lucide:chevron-right"
        next-icon="lucide:chevron-left"
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
        <div dir="rtl" class="w-full text-right">
          <BaseHeading>تجهیزات کاربر</BaseHeading>
        </div>
      </template><div dir="rtl" class="p-4 text-right">
        <p v-if="!selectedDevices.length" class="text-muted-500">
          تجهیزی برای این کاربر ثبت نشده است.
        </p><ul v-else class="space-y-2">
          <li
            v-for="device in selectedDevices"
            :key="device.id || device.name"
            class="border-muted-200 dark:border-muted-700 rounded-lg border p-3 text-right"
          >
            {{ device.name || device.device_name || 'تجهیز بدون نام' }}
          </li>
        </ul>
      </div>
    </TairoModal>
    <TairoModal
      :open="isCreateModalOpen"
      size="sm"
      @close="isCreateModalOpen = false"
    >
      <template #header>
        <div dir="rtl" class="w-full text-right">
          <BaseHeading>افزودن کاربر جدید</BaseHeading>
        </div>
      </template>
      <form dir="rtl" class="space-y-4 p-4 text-right" @submit.prevent="createUser">
        <BaseMessage v-if="createError" type="danger">
          {{ createError }}
        </BaseMessage>
        <BaseInput
          v-model="createForm.email"
          type="email"
          label="ایمیل"
          placeholder="user@example.com"
          autocomplete="email"
          :disabled="creating"
        />
        <BaseInput
          v-model="createForm.password"
          type="password"
          label="رمز عبور"
          placeholder="حداقل ۶ کاراکتر"
          autocomplete="new-password"
          :disabled="creating"
        />
        <BaseCheckbox
          v-model="createForm.isAdmin"
          label="این کاربر دسترسی مدیر داشته باشد"
          :disabled="creating"
        />
        <div class="flex justify-end gap-2 pt-2">
          <BaseButton type="button" :disabled="creating" @click="isCreateModalOpen = false">
            انصراف
          </BaseButton>
          <BaseButton type="submit" color="primary" :loading="creating" :disabled="creating">
            ثبت کاربر
          </BaseButton>
        </div>
      </form>
    </TairoModal>
  </TairoContentWrapper>
</template>
