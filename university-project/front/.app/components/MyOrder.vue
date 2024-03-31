<script setup lang="ts">
import {useAppStore} from "~/stores/app";
import {storeToRefs} from 'pinia';
import {ref, computed} from 'vue';
import axios from 'axios';
import {Field, useForm} from "vee-validate";
import {z} from "zod";
import {toTypedSchema} from "@vee-validate/zod";

const {locale, locales} = useI18n()
const formatPrice = (price: number) => {
  if (price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  }
};
const app = useAppStore();
const {cart, language} = storeToRefs(app);
const fetchCart = app.fetchCart;
const initializeData = async () => {
  await fetchCart();
};


onMounted(initializeData);
const localPath = useLocalePath();

const removeItem = async (itemToRemove) => {
  const removeItem = app.removeItem(itemToRemove);
};

const {t} = useI18n({useScope: "local"})
</script>


<template>
  <div class="ltablet:col-span-4 col-span-12 lg:col-span-4 hidden md:block">
    <div class="bg-muted-200 dark:bg-muted-800 flex flex-col gap-6 rounded-2xl p-6">
      <div>
        <BaseHeading tag="h3" size="xl" weight="medium" class="text-muted-800 dark:text-muted-100">
          <span>{{ t('Order') }}</span>
        </BaseHeading>
      </div>
      <!-- Items -->
      <ul class="space-y-4">
        <li v-for="item in cart.cart_items" :key="item.product?.id">
          <div class="flex items-center gap-3">
            <div class="relative flex h-14 w-14 items-center justify-center">
              <div class="border-muted-200 dark:border-muted-700 dark:bg-muted-900 relative rounded-xl border bg-white">
                <img
                  :src="item.product?.logo"
                  :alt="item.product?.name[locale]"
                  class="h-12 w-12 object-contain rounded-xl"
                />
                <!-- Circular Remove Button -->
                <button @click="removeItem(item)"
                        class="absolute mt-7 top-0 right-0 rounded-full bg-primary-500 text-white hover:bg-primary-600 w-8 h-8 flex items-center justify-center">
                  <span>-</span>
                </button>
              </div>
            </div>
            <div>
              <p class="text-muted-800 dark:text-muted-100 font-sans text-sm">
                {{ item.product?.name[locale] }}
              </p>
              <!--              <p class="text-muted-400 font-sans text-xs mt-1">-->
              <!--                {{ t('Price') }}: {{ item.product?.price }}T-->
              <!--              </p>-->
              <p class="text-muted-400 font-sans text-xs mt-1">
                {{ t('Email') }}: {{ item.email?.substring(0, 10) }}...
              </p>
            </div>
            <div class="ms-auto">
              <p class="text-muted-800 dark:text-muted-100 font-sans text-sm font-semibold">
                {{ formatPrice(item.product?.price) }}<span class="letter-t mx-2">T</span>
              </p>
            </div>
          </div>
        </li>
      </ul>
      <div class="border-muted-300 dark:border-muted-800 flex grow flex-col justify-end border-t py-4">
        <ul class="my-4 space-y-2 font-sans">
          <li>
            <div class="flex items-center justify-between">
              <span>{{ t('Total') }} :</span>
              <div>
  <span class="text-muted-800 dark:text-muted-100 text-xl font-semibold">
    {{ formatPrice(app.total) }}<span class="letter-t mx-2">T</span>
  </span>
              </div>
            </div>
          </li>
        </ul>
        <div class="mt-4 flex justify between text-xs font-bold">

          <NuxtLink :to="localPath('/payment')">
            <BaseButton :disabled="!cart ||cart.cart_items?.length === 0" color="none" shape="curved"
                        class="text-muted-800 group !h-14 w-full !gap-3 bg-yellow-400 hover:!shadow-xl hover:!shadow-yellow-400/20">
              <span class="text-base font-medium">{{ t('Checkout') }}</span>

              <Icon
                :name="locale === 'en' ? 'lucide:arrow-right' : 'lucide:arrow-left'"
                class="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1"
              />
            </BaseButton>
          </NuxtLink>
        </div>
      </div>
    </div>
  </div>
</template>
