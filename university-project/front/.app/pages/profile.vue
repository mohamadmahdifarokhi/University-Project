<script setup lang="ts">
import { storeToRefs } from "pinia";
import { useAppStore } from "~/stores/app";
import { onMounted } from "vue";
import axios from 'axios';
const app = useAppStore();

const localPath = useLocalePath();
const { locale, locales } = useI18n();

definePageMeta({
  title: 'Accountract',
  middleware: 'authenticated',
  preview: {
    title: 'Invoice',
    description: 'For accounting and invoices',
    categories: ['layouts'],
    src: '/img/screens/layouts-utility-invoice.png',
    srcDark: '/img/screens/layouts-utility-invoice-dark.png',
    order: 90,
  },
});

const { email, photo } = storeToRefs(app);
const { t } = useI18n({ useScope: "local" });

const handleFileUpload = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  if (file) {
    await app.importExcel(file);
  window.location.reload();

  }
};

// const importExcel = async (file: File) => {
//   try {
//     const accessToken = useCookie('access_token').value;
//     const formData = new FormData();
//     formData.append('file', file);
//
//     const response = await axios.post('http://127.0.0.1:8002/power-records/upload-excel-file', formData, {
//       headers: {
//         Authorization: `Bearer ${accessToken}`,
//         'Content-Type': 'multipart/form-data',
//       },
//     });
//
//     if (response.status === 200) {
//       app.showSuccessToast('File uploaded successfully');
//     }
//   } catch (error) {
//     console.error('Error uploading file:', error);
//   }
// };
</script>

<template>
  <div class="min-h-screen overflow-hidden">
    <div class="grid gap-8 sm:grid-cols-12">
      <div class="col-span-12 sm:col-span-4">
        <div class="flex w-full items-center gap-2">
          <BaseAvatar
            :src="`/img/avatars/${photo}.svg`"
            size="md"
          />
          <div class="">
            <BaseHeading tag="h2" size="md" weight="medium" lead="none">
              {{ email }}
            </BaseHeading>
            <BaseHeading class="mt-2" tag="h1" size="sm" weight="medium" lead="none">
              Block 2
            </BaseHeading>
          </div>
        </div>
        <div class="mt-8 max-w-[240px]">
          <ul class="space-y-1 font-sans text-sm">
            <BaseCard class="p-6 mb-10">
              <DemoNotificationsCompact />
            </BaseCard>
            <li>
              <NuxtLink
                :to="localPath('/profile/blocks')"
                exact-active-class="!text-primary-500 !bg-primary-500/10"
                class="text-muted-400 hover:text-muted-600 dark:hover:text-muted-200 hover:bg-muted-50 dark:hover:bg-muted-700/50 flex items-center gap-2 rounded-lg p-3 transition-colors duration-300"
              >
                <Icon name="ph:buildings-duotone" class="h-4 w-4"/>
                <span>{{ t('Blocks') }}</span>
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="localPath('/profile/orders')"
                exact-active-class="!text-primary-500 !bg-primary-500/10"
                class="text-muted-400 hover:text-muted-600 dark:hover:text-muted-200 hover:bg-muted-50 dark:hover:bg-muted-700/50 flex items-center gap-2 rounded-lg p-3 transition-colors duration-300"
              >
                <Icon name="ph:buildings-duotone" class="h-4 w-4"/>
                <span>{{ t('Orders') }}</span>
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="localPath('/profile/records')"
                exact-active-class="!text-primary-500 !bg-primary-500/10"
                class="text-muted-400 hover:text-muted-600 dark:hover:text-muted-200 hover:bg-muted-50 dark:hover:bg-muted-700/50 flex items-center gap-2 rounded-lg p-3 transition-colors duration-300"
              >
                <Icon name="ri:git-commit-fill" class="size-5"/>
                <span>{{ t('Records') }}</span>
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="localPath('/profile/settings')"
                exact-active-class="!text-primary-500 !bg-primary-500/10"
                class="text-muted-400 hover:text-muted-600 dark:hover:text-muted-200 hover:bg-muted-50 dark:hover:bg-muted-700/50 flex items-center gap-2 rounded-lg p-3 transition-colors duration-300"
              >
                <Icon name="ph:gear-six-duotone" class="h-4 w-4"/>
                <span>{{ t('Settings') }}</span>
              </NuxtLink>
            </li>
            <li>
              <NuxtLink
                :to="localPath('/profile/products')"
                exact-active-class="!text-primary-500 !bg-primary-500/10"
                class="text-muted-400 hover:text-muted-600 dark:hover:text-muted-200 hover:bg-muted-50 dark:hover:bg-muted-700/50 flex items-center gap-2 rounded-lg p-3 transition-colors duration-300"
              >
                <Icon name="ri:product-hunt-fill" class="size-5"/>
                <span>Available Products</span>
              </NuxtLink>
            </li>
            <li>
              <div
                exact-active-class="!text-primary-500 !bg-primary-500/10"
                class="text-muted-400 hover:text-muted-600 dark:hover:text-muted-200 hover:bg-muted-50 dark:hover:bg-muted-700/50 flex items-center gap-2 rounded-lg p-3 transition-colors duration-300"
              >
                <Icon name="ri:product-hunt-fill" class="size-5"/>
                <span>Upload Excel</span>
                <input type="file" @change="handleFileUpload" class="ml-2"/>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <div class="col-span-12 sm:col-span-8">
        <RouterView v-slot="{ Component }">
          <Transition
            enter-active-class="transition-all duration-500 ease-out"
            enter-from-class="translate-y-20 opacity-0"
            enter-to-class="translate-y-0 opacity-100"
            leave-active-class="transition-all duration-200 ease-in"
            leave-from-class="translate-y-0 opacity-100"
            leave-to-class="translate-y-20 opacity-0"
          >
            <component :is="Component"/>
          </Transition>
        </RouterView>
      </div>
    </div>
  </div>
</template>
