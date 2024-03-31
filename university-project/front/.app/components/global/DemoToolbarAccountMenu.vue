<script setup lang="ts">
import {Menu, MenuButton, MenuItems} from '@headlessui/vue'
import {ref, computed} from 'vue'
import {useAuthStore} from "@/stores/auth";
import {useAppStore} from "~/stores/app";
import {storeToRefs} from 'pinia';

const {locale, locales} = useI18n()
const localPath = useLocalePath();

// const email = computed(() => {
//   return localStorage.getItem('email') || '';
// });
const router = useRouter()
const {t} = useI18n({useScope: "local"})

const authStore = useAuthStore();
const app = useAppStore();
const {email, photo} = storeToRefs(app);
const fetchProfile = app.fetchProfile;
const initializeData = async () => {
  await fetchProfile();
};

initializeData();
const loading = ref(false);

const changePhoto = async () => {
  try {
    loading.value = true;
    await app.changePhoto();
    loading.value = false;

  } finally {
    loading.value = false;
  }
};
const logout = () => {
  authStore.$reset();
  window.location.reload();

};


// Define the avatar source based on the random number
</script>

<template>
  <div class="group inline-flex items-center justify-center text-right">
    <!-- Display profile if authenticated -->
    <div v-if="authStore.isAuthenticated">
      <Menu as="div" class="relative h-9 w-9 text-left" v-slot="{ close }">
        <MenuButton as="template">
          <button
            type="button"
            class="group-hover:ring-primary-500 dark:ring-offset-muted-900 inline-flex h-9 w-9 items-center justify-center rounded-full ring-1 ring-transparent transition-all duration-300 group-hover:ring-offset-4"
          >
            <div
              class="relative inline-flex h-9 w-9 items-center justify-center rounded-full"
            >
              <img
                :src="`/img/avatars/${photo}.svg`"
                :class="{ 'opacity-25': loading }"

                class="max-w-full rounded-full object-cover shadow-sm dark:border-transparent"
                alt=""
              />
            </div>
          </button>
        </MenuButton>

        <Transition
          enter-active-class="transition duration-100 ease-out"
          enter-from-class="transform scale-95 opacity-0"
          enter-to-class="transform scale-100 opacity-100"
          leave-active-class="transition duration-75 ease-in"
          leave-from-class="transform scale-100 opacity-100"
          leave-to-class="transform scale-95 opacity-0"
        >
          <MenuItems
            class="divide-muted-100 border-muted-200 dark:divide-muted-700 dark:border-muted-700 dark:bg-muted-800 absolute end-0 mt-2 w-64 origin-top-right divide-y rounded-md border bg-white shadow-lg focus:outline-none"
          >
            <div class="p-6 text-center">
              <div
                class="relative mx-auto flex h-20 w-20 items-center justify-center rounded-full"
              >
                <img
                  :src="`/img/avatars/${photo}.svg`"
                  :class="{ 'opacity-25': loading }"

                  class="max-w-full rounded-full object-cover shadow-sm dark:border-transparent"
                  alt=""
                />
                <button
                  v-if="authStore.isAuthenticated"
                  @click="changePhoto"
                  class="absolute top-0 right-0 -mt-1 -mr-1 bg-primary-500 text-white rounded-full w-6 h-6 flex items-center justify-center cursor-pointer"
                >
                  <svg
                    class="w-4 h-4"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M15.293 5.293a1 1 0 0 0-1.414-1.414L11 8.586V5a1 1 0 1 0-2 0v3.586L6.414 3.879a1 1 0 1 0-1.414 1.414L8.586 10H5a1 1 0 0 0 0 2h3.586l-3.293 3.293a1 1 0 1 0 1.414 1.414L10 13.414V17a1 1 0 0 0 2 0v-3.586l3.293 3.293a1 1 0 0 0 1.414-1.414L13.414 10H17a1 1 0 0 0 0-2h-3.586l3.293-3.293z"
                    />
                  </svg>
                </button>
              </div>
              <div class="mt-3">
                <h6 v-if="locale==='en'"
                    class="font-heading text-muted-800 text-sm font-medium dark:text-white mb-4"
                >

                  {{ email.substring(0, 23) }}...
                </h6>
                <h6 v-if="locale==='fa'"
                    class="font-heading text-muted-800 text-sm font-medium dark:text-white mb-4"
                >

                  ...{{ email.substring(0, 23) }}
                </h6>
                <BaseButton
                  :to="localPath('/profile/orders')"
                  shape="curved"
                  class="w-full"
                  @click.passive="close"
                >
                  {{ t('Manage') }}
                </BaseButton>
              </div>
            </div>
            <!-- Other profile menu items can be added here if needed -->
            <div class="p-6">
              <BaseButton @click.passive="logout" shape="curved" class="w-full">
                {{ t('Logout') }}
              </BaseButton>
            </div>
          </MenuItems>
        </Transition>
      </Menu>
    </div>
    <!-- Display signup and login buttons if not authenticated -->
    <div v-else>
<!--      <router-link :to="localPath('/signup')">-->
<!--        <BaseButton shape="curved" class="mx-2">-->
<!--          {{ t('Signup') }}-->
<!--        </BaseButton>-->
<!--      </router-link>-->
      <router-link :to="localPath('/login')">
        <BaseButton shape="curved" class="ms-2">
          {{ t('Login') }}
        </BaseButton>
      </router-link>
    </div>
  </div>
</template>
