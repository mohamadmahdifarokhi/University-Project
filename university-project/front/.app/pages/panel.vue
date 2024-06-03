<script setup lang="ts">
import {ref, computed, watch, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {useAppStore} from '~/stores/app'
import {storeToRefs} from 'pinia'
import {useAuthStore} from "~/stores/auth";

definePageMeta({
  title: 'Flex List',
  middleware: ['authenticated'],
  preview: {
    title: 'Flex list 1',
    description: 'For list views and collections',
    categories: ['layouts', 'lists'],
    src: '/img/screens/layouts-list-flex-1.png',
    srcDark: '/img/screens/layouts-list-flex-1-dark.png',
    order: 41,
  },
})

const route = useRoute()
const router = useRouter()

const filter = ref('')
const selectedUserDevices = ref(null)
const isModalOpen = ref(false)




const authStore = useAuthStore();



function statusColor(itemStatus: string) {
  switch (itemStatus) {
    case 'online':
      return 'success'
    case 'working':
      return 'info'
    case 'suspended':
      return 'warning'
    default:
      return 'default'
  }
}

async function fetchUserDevices(devices) {
  try {
    // const response = await fetch(`/api/company/candidates/${userId}/devices`)
    // if (response.ok) {
    selectedUserDevices.value = devices
    // } else {
    // console.error('Error fetching user devices:', response.statusText)
    // }
    isModalOpen.value = true
  } catch (error) {
    console.error('Error fetching user devices:', error)
  }
}

const app = useAppStore()

const {allUsers} = storeToRefs(app)
const fetchusers = app.fetchusers
const fetchusersMng = app.fetchusersMng

async function initializeData() {
  if (authStore.isAdmin) {
    await fetchusers()
  }
  if (authStore.isMng) {
    await fetchusersMng()
  }
}

onMounted(async () => {
  await initializeData()
})
</script>

<template>
  <div>
    <TairoContentWrapper>
      <div>
        <div v-if="!pending && data?.data.length === 0">
          <BasePlaceholderPage
            title="No matching results"
            subtitle="Looks like we couldn't find any matching results for your search terms. Try other search terms."
          >
            <template #image>
              <img
                class="block dark:hidden"
                src="/img/illustrations/placeholders/flat/placeholder-search-4.svg"
                alt="Placeholder image"
              />
              <img
                class="hidden dark:block"
                src="/img/illustrations/placeholders/flat/placeholder-search-4-dark.svg"
                alt="Placeholder image"
              >
            </template>
          </BasePlaceholderPage>
        </div>
        <div v-else class="space-y-2 pt-6">
          <TransitionGroup
            enter-active-class="transform-gpu"
            enter-from-class="opacity-0 -translate-x-full"
            enter-to-class="opacity-100 translate-x-0"
            leave-active-class="absolute transform-gpu"
            leave-from-class="opacity-100 translate-x-0"
            leave-to-class="opacity-0 -translate-x-full"
          >
            <DemoFlexTableRow
              v-for="(item, index) in allUsers"
              :key="index"
              rounded="sm"
              spaced
            >
              <template #start>
                <DemoFlexTableStart
                  label="user"
                  :hide-label="index > 0"
                  :title="item.user.email"
                  :subtitle="item.position"
                  :avatar="`/img/avatars/${item.profile}.svg`"
                  :initials="item.initials"
                />
              </template>
              <template #end>
                <DemoFlexTableCell
                  label="Unit"
                  :hide-label="index > 0"
                  class="w-full sm:w-40"
                >
                  <span
                    class="text-muted-500 dark:text-muted-400 font-sans text-sm"
                  >
                    {{ item.unit }}
                  </span>
                </DemoFlexTableCell>
                <DemoFlexTableCell
                  label="Apartment"
                  :hide-label="index > 0"
                  class="w-full sm:w-40"
                >
                  <span
                    class="text-muted-500 dark:text-muted-400 font-sans text-sm"
                  >
                    {{ item.apartment_number }}
                  </span>
                </DemoFlexTableCell>
                <DemoFlexTableCell
                  label="area"
                  :hide-label="index > 0"
                  class="w-full sm:w-16"
                >
                  <BaseTag
                    :color="statusColor(item.status)"
                    rounded="full"
                    variant="pastel"
                    size="sm"
                    class="capitalize"
                  >
                    {{ item.area }}
                  </BaseTag>
                </DemoFlexTableCell>
                <DemoFlexTableCell label="action" :hide-label="index > 0">
                  <BaseButtonAction color="muted" @click="fetchUserDevices(item.devices)">
                    <span>Devices</span>
                  </BaseButtonAction>
                </DemoFlexTableCell>
              </template>
            </DemoFlexTableRow>
          </TransitionGroup>
        </div>
      </div>
    </TairoContentWrapper>

    <TairoModal
      :open="isModalOpen"
      size="lg"
      @close="isModalOpen = false"
    >
      <template #header>
        <div class="flex w-full items-center justify-between p-4 md:p-6">
          <h3 class="font-heading text-muted-900 text-lg font-medium leading-6 dark:text-white">
            User Devices
          </h3>
          <BaseButtonClose @click="isModalOpen = false"/>
        </div>
      </template>
      <div class="p-4 md:p-6">
        <div v-if="selectedUserDevices && selectedUserDevices.length > 0">
          <ul>
            <li v-for="device in selectedUserDevices" :key="device.id">
              {{ device }}
            </li>
          </ul>
        </div>
        <div v-else>
          Loading devices...
        </div>
      </div>
      <template #footer>
        <div class="p-4 md:p-6">
          <BaseButton @click="isModalOpen = false">Close</BaseButton>
        </div>
      </template>
    </TairoModal>
  </div>
</template>
