<script setup lang="ts">
import { onMounted, watch } from 'vue';
import { useAppStore } from '~/stores/app';
import { storeToRefs } from 'pinia';

const app = useAppStore();
const { peakHour, peakPower } = storeToRefs(app);
const powerConsumption = app.powerConsumption;

async function initializeData() {
  await powerConsumption();
}

onMounted(async () => {
  await initializeData();
});

const skills = ref([
  {
    id: 0,
    name: 'Peak Hour Consumption',
    count: `${peakHour.value} w`,
    icon: 'ri:time-fill',
  },
  {
    id: 1,
    name: 'Peak Power Consumption',
    count: `${peakPower.value} w`,
    icon: 'ri:flashlight-fill',
  },
]);

watch([peakHour, peakPower], () => {
  skills.value = [
    {
      id: 0,
      name: 'Peak Hour Consumption',
      count: `${peakHour.value} w`,
      icon: 'ri:time-fill',
    },
    {
      id: 1,
      name: 'Peak Power Consumption',
      count: `${peakPower.value} w`,
      icon: 'ri:flashlight-fill',
    },
  ];
});
</script>

<template>
  <div class="mb-2 space-y-5">
    <div
      v-for="skill in skills"
      :key="skill.id"
      class="flex items-center gap-3"
    >
      <div
        class="border-muted-200 dark:border-muted-700 flex size-10 items-center justify-center rounded-full border"
      >
        <Icon :name="skill.icon" class="size-5"/>
      </div>
      <div>
        <BaseHeading
          as="h4"
          size="sm"
          weight="light"
          lead="tight"
          class="text-muted-800 dark:text-white"
        >
          <span>{{ skill.name }}</span>
        </BaseHeading>
        <BaseParagraph size="xs">
          <span class="text-muted-400">
            {{ skill.count }}
          </span>
        </BaseParagraph>
      </div>
    </div>
  </div>
</template>
