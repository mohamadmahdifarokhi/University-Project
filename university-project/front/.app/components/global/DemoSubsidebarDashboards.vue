<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const localPath = useLocalePath()
const authStore = useAuthStore()
const { isOpen } = useSidebar()
const navigation = [
  { name: 'نمای کلی انرژی', icon: 'ph:gauge-duotone', to: localPath('/dashboard'), exact: true },
  { name: 'بازار انرژی', icon: 'ph:storefront-duotone', to: localPath('/shop') },
  { name: 'ساختمان و منابع', icon: 'ph:buildings-duotone', to: localPath('/profile/blocks') },
  { name: 'سوابق مصرف', icon: 'ph:chart-line-up-duotone', to: localPath('/profile/records') },
  { name: 'سفارش‌ها', icon: 'ph:receipt-duotone', to: localPath('/profile/orders') },
  { name: 'تنظیمات حساب', icon: 'ph:gear-six-duotone', to: localPath('/profile/settings') },
]
const navigationAdmin = [
  { divider: true },
  { name: 'مدیریت سامانه', icon: 'ph:users-three-duotone', to: localPath('/panel') },
]
</script>

<template>
  <TairoSubsidebar>
    <template #header>
      <div class="flex h-20 w-full items-center justify-center px-5">
        <NuxtLink
          to="/dashboard"
          aria-label="دانشگاه آزاد اسلامی واحد پردیس"
          class="flex min-w-0 items-center justify-center"
        >
          <img
            src="/img/azad-pardis-logo.png"
            alt="لوگوی دانشگاه آزاد اسلامی واحد پردیس"
            class="size-14 object-contain"
          >
        </NuxtLink>
        <button
          type="button"
          class="text-muted-400 hover:bg-muted-100 hover:text-muted-600 ms-auto flex size-10 items-center justify-center rounded-full transition-colors duration-300 xl:hidden"
          aria-label="بستن منو"
          @click="isOpen = false"
        >
          <Icon name="feather:chevron-left" class="size-6" />
        </button>
      </div>
    </template>
    <TairoSubsidebarMenu :navigation="navigation" />
    <TairoSubsidebarMenu v-if="authStore.isAdmin" :navigation="navigationAdmin" />
  </TairoSubsidebar>
</template>
