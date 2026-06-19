<script setup lang="ts">
import {useAppStore} from "~/stores/app";
import {storeToRefs} from 'pinia';
import {ref, computed, watch} from 'vue';

const app = useAppStore();
const {records} = storeToRefs(app);

definePageMeta({
  title: 'Records',
  middleware: 'authenticated',
  preview: {
    title: 'Edit profile 4',
    description: 'For editing a user profile',
    categories: ['layouts', 'profile', 'forms'],
    src: '/img/screens/layouts-subpages-profile-4.png',
    srcDark: '/img/screens/layouts-subpages-profile-4-dark.png',
    order: 79,
  }
});

const {t} = useI18n({useScope: "local"})

const page = ref(1);
const perPage = ref(8);

const totalItems = computed(() => records.value?.length ?? 0);
const totalPages = computed(() => Math.max(1, Math.ceil(totalItems.value / perPage.value)));

const paginatedRecords = computed(() => {
  const start = (page.value - 1) * perPage.value;
  return (records.value ?? []).slice(start, start + perPage.value);
});

// Keep the current page in range when the data size changes.
watch(totalPages, (tp) => {
  if (page.value > tp) page.value = tp;
});

function deleteRecord(recordId) {
  app.deleteRecord(recordId)
}

const formatDate = (value) => {
  return toJalaliDateTime(value);
};

const initializeData = async () => {
  await app.fetchRecords();
};
initializeData()
</script>

<template>
  <div>
    <BaseCard rounded="lg" class="p-6">
      <div class="mb-6 flex items-center justify-between">
        <BaseHeading
          as="h3"
          size="md"
          weight="semibold"
          lead="tight"
          class="text-muted-800 dark:text-white"
        >
          <span>{{ t('Records') }}</span>
        </BaseHeading>
        <BaseText size="sm" class="text-muted-400">
          {{ totalItems }}
        </BaseText>
      </div>

      <div v-if="paginatedRecords.length" class="space-y-3">
        <div
          v-for="record in paginatedRecords"
          :key="record.power_record_id"
          class="border-muted-200 dark:border-muted-700 flex items-center gap-2 rounded-lg border p-4"
        >
          <div class="grid grid-cols-2 gap-x-6 gap-y-1 grow">
            <BaseText size="sm" class="text-muted-800 dark:text-white font-medium">
              {{ record.device_name }}
            </BaseText>
            <BaseText size="sm" class="text-muted-500 dark:text-muted-400">
              {{ record.consumption }} Wh
            </BaseText>
            <BaseText size="xs" class="text-muted-400">
              {{ formatDate(record.start_time) }}
            </BaseText>
            <BaseText size="xs" class="text-muted-400">
              {{ formatDate(record.end_time) }}
            </BaseText>
          </div>
          <BaseButtonIcon @click="deleteRecord(record.power_record_id)" rounded="full" small>
            <Icon name="ri:delete-bin-fill"/>
          </BaseButtonIcon>
        </div>
      </div>

      <div v-else class="py-10 text-center">
        <BaseText size="sm" class="text-muted-400">
          {{ t('NoRecords') }}
        </BaseText>
      </div>

      <div v-if="totalPages > 1" class="mt-6 flex items-center justify-center gap-2">
        <BaseButton
          shape="curved"
          size="sm"
          :disabled="page <= 1"
          @click="page--"
        >
          <Icon name="lucide:chevron-right" class="size-4"/>
        </BaseButton>

        <BaseText size="sm" class="text-muted-500 dark:text-muted-400 px-2">
          {{ page }} / {{ totalPages }}
        </BaseText>

        <BaseButton
          shape="curved"
          size="sm"
          :disabled="page >= totalPages"
          @click="page++"
        >
          <Icon name="lucide:chevron-left" class="size-4"/>
        </BaseButton>
      </div>
    </BaseCard>
  </div>
</template>
