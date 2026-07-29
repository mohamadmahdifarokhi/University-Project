<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

const localPath = useLocalePath()
const authStore = useAuthStore()
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
      <TairoSubsidebarHeader />
    </template>
    <TairoSubsidebarMenu :navigation="navigation" />
    <TairoSubsidebarMenu v-if="authStore.isAdmin" :navigation="navigationAdmin" />
  </TairoSubsidebar>
</template>
