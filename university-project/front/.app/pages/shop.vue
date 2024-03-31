<script setup lang="ts">
import {useRoute} from 'vue-router';
import {useAppStore} from "~/stores/app";
import {storeToRefs} from 'pinia';

const localPath = useLocalePath();

const {t} = useI18n({useScope: "local"})
// const config = useRuntimeConfig()

// instead of process.env you will now access config.public.apiBase
const app = useAppStore();
definePageMeta({
  title: "Uuniversity Project",
  middleware: ['authenticated'],

});
const {locale, locales} = useI18n()

const {activeGenre, categories, cart} = storeToRefs(app);
const fetchCategories = app.fetchCategories;
const fetchProducts = app.fetchProducts;
const fetchNotActiveProducts = app.fetchNotActiveProducts;
const fetchCart = app.fetchCart;

const initializeData = async () => {
  await fetchCategories();
  await fetchProducts();
  await fetchNotActiveProducts();
  await fetchCart();
};

initializeData();
const formatPrice = (price: number) => {
  if (price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  }
};
const route = useRoute();
const authority = route.query.Authority || '';
const status = route.query.Status || '';
const id = route.query.Id || '';

if (authority && status && id) {
  (async () => {
    await app.verifyPayment({authority, status, id});
  })();
}


</script>

<template>
  <div>
    <!-- Grid -->
    <div class="grid grid-cols-12 gap-6" :dir="locale === 'en' ? 'ltr' : 'rtl'">
      <!-- Column -->
      <div class="ltablet:col-span-8 col-span-12 lg:col-span-8">
        <div class="flex flex-col gap-6">
          <!-- Header -->
          <!--          <div class="col-span-12" dir="rtl">-->
          <!--            <div-->
          <!--              class="bg-gradient-to-r from-purple-800 via-purple-600 to-purple-800 flex flex-col items-center rounded-2xl p-8 sm:flex-row transform hover:scale-110 transition duration-300 ease-in-out">-->

          <!--              <div class="relative h-[120px] w-[240px] sm:h-[175px] transition-all duration-500 ease-in-out mr-16">-->
          <!--                <img-->
          <!--                  class="pointer-events-none absolute -top-6 start-3 sm:-start-10 sm:-top-2 mt-5 mr-5 rounded-full transform hover:scale-125 transition duration-300 ease-in-out shadow-2xl"-->
          <!--                  src="/img/illustrations/dashboards/delivery/chatgpt.png" alt="ChatGPT Logo"/>-->
          <!--              </div>-->

          <!--              <div class="mt-6 sm:mt-0 transition-all duration-500 ease-in-out">-->
          <!--                <div class="pb-4 text-center sm:text-left">-->
          <!--                  <BaseHeading tag="h1"-->
          <!--                               class="mb-4 text-white font-bold text-4xl transform hover:text-yellow-300 transition duration-300 ease-in-out">-->
          <!--                    <span class="text-yellow-400 transition duration-300 ease-in-out">🎉</span> CHAT GPT-->
          <!--                  </BaseHeading>-->

          <!--                  <BaseParagraph size="md"-->
          <!--                                 class="max-w-md mx-auto text-center sm:text-right text-white opacity-80 transition duration-300 ease-in-out"-->
          <!--                                 dir="ltr">-->
          <!--                    Unleash the power of GPT 3.5 & GPT 4 for your conversations!-->
          <!--                  </BaseParagraph>-->

          <!--                  <BaseParagraph size="md"-->
          <!--                                 class="max-w-md mt-5 mx-auto text-center sm:text-right text-white transition duration-300 ease-in-out">-->
          <!--                    قدرت GPT 3.5 و GPT 4 را برای مکالمات خود آزاد کنید!-->
          <!--                  </BaseParagraph>-->

          <!--                  <div class="mt-4 transition-all duration-300 ease-in-out">-->
          <!--                    <a href="http://5.78.57.46:8011"-->
          <!--                       class="w-full sm:w-auto transform hover:rotate-3 transition duration-300 ease-in-out">-->
          <!--                      <BaseButton size="lg" color="purple" flavor="solid" class="shadow-md hover:shadow-xl">-->
          <!--                        <span class="text-white pr-2">بیا چت کنیم | Let's Chat</span>-->
          <!--                        <Icon name="lucide:arrow-right" class="ml-2 h-5 w-5"/>-->
          <!--                      </BaseButton>-->
          <!--                    </a>-->
          <!--                  </div>-->
          <!--                </div>-->
          <!--              </div>-->

          <!--            </div>-->
          <!--          </div>-->

          <!-- Grid -->
          <div class="relative mt-6">
            <!-- Food types -->
<!--            <div class="mb-20 md:mb-40 grid grid-cols-4 gap-4 sm:grid-cols-9">-->
<!--&lt;!&ndash;              <div&ndash;&gt;-->
<!--&lt;!&ndash;                v-for="category in categories"&ndash;&gt;-->
<!--&lt;!&ndash;                :key="category.id"&ndash;&gt;-->
<!--&lt;!&ndash;                role="button"&ndash;&gt;-->
<!--&lt;!&ndash;                class="flex cursor-pointer flex-col items-center rounded-full border p-2 shadow-xl transition-colors duration-500 ease-in-out"&ndash;&gt;-->
<!--&lt;!&ndash;                :class="&ndash;&gt;-->
<!--&lt;!&ndash;                  activeGenre === category.id&ndash;&gt;-->
<!--&lt;!&ndash;                    ? 'bg-yellow-400 border-yellow-400'&ndash;&gt;-->
<!--&lt;!&ndash;                    : 'border-muted-200 dark:border-muted-700 hover:bg-muted-200/80 dark:hover:bg-muted-800/40'&ndash;&gt;-->
<!--&lt;!&ndash;                "&ndash;&gt;-->
<!--&lt;!&ndash;                @click=" app.ChangeActiveGenre(category.id)"&ndash;&gt;-->
<!--&lt;!&ndash;              >&ndash;&gt;-->
<!--&lt;!&ndash;                <div&ndash;&gt;-->
<!--&lt;!&ndash;                  class="rounded-full border p-2 transition-colors duration-500 ease-in-out"&ndash;&gt;-->
<!--&lt;!&ndash;                  :class="&ndash;&gt;-->
<!--&lt;!&ndash;                    activeGenre === category.id&ndash;&gt;-->
<!--&lt;!&ndash;                      ? 'bg-white border-yellow-400'&ndash;&gt;-->
<!--&lt;!&ndash;                      : 'border-muted-200 dark:border-muted-800 bg-white dark:bg-muted-800'&ndash;&gt;-->
<!--&lt;!&ndash;                  "&ndash;&gt;-->
<!--&lt;!&ndash;                >&ndash;&gt;-->
<!--&lt;!&ndash;                  <img v-if="category.id!==1"&ndash;&gt;-->
<!--&lt;!&ndash;                       :src="category.photo"&ndash;&gt;-->
<!--&lt;!&ndash;                       alt="Food type icon"&ndash;&gt;-->
<!--&lt;!&ndash;                  />&ndash;&gt;-->
<!--&lt;!&ndash;                </div>&ndash;&gt;-->
<!--&lt;!&ndash;                <p class="mb-10 mt-3 text-xs font-bold">{{ category.name[locale] }}</p>&ndash;&gt;-->
<!--&lt;!&ndash;              </div>&ndash;&gt;-->

<!--&lt;!&ndash;              <div class="hidden items-center justify-center sm:flex">&ndash;&gt;-->
<!--&lt;!&ndash;                <BaseButtonIcon&ndash;&gt;-->
<!--&lt;!&ndash;                  rounded="full"&ndash;&gt;-->
<!--&lt;!&ndash;                  class="hover:border-yellow-500 hover:text-yellow-500"&ndash;&gt;-->
<!--&lt;!&ndash;                  :data-nui-tooltip="t('Categories')"&ndash;&gt;-->
<!--&lt;!&ndash;                  disabled="true"&ndash;&gt;-->
<!--&lt;!&ndash;                >&ndash;&gt;-->
<!--&lt;!&ndash;                  <Icon&ndash;&gt;-->
<!--&lt;!&ndash;                    :name="locale === 'en' ? 'lucide:chevron-right' : 'lucide:chevron-left'"&ndash;&gt;-->
<!--&lt;!&ndash;                    class="size-4"&ndash;&gt;-->
<!--&lt;!&ndash;                  />&ndash;&gt;-->
<!--&lt;!&ndash;                </BaseButtonIcon>&ndash;&gt;-->
<!--&lt;!&ndash;              </div>&ndash;&gt;-->
<!--            </div>-->
            <!-- Meals -->
            <div class="grid gap-x-3 gap-y-6 sm:grid-cols-3">
              <NuxtLink
                v-for="product in app.filteredProducts"
                :key="product.id"
                :to="localPath(`/product/${product.slug}`)"
                class="relative"
              >

                <BaseCard
                  shape="curved"
                  class="hover:border-primary-500 hover:shadow-muted-300/30 dark:hover:shadow-muted-900/40 py-5 px-3 hover:shadow-xl"
                >


                  <div class="ltablet:h-28 relative mb-3 h-36 w-full rounded-xl sm:h-32">

                    <div class="bg-muted-100 dark:bg-muted-900 relative w-full h-full rounded-xl"
                    >
                      <div class="blur-overlay w-full h-full absolute inset-0 bg-cover rounded-xl"
                           style="backdrop-filter: blur(10px);"></div>

                      <!--                      <img class="ltablet:max-w-[75px] h-25 absolute max-w-[60px]"-->
                      <!--                           :src="product.logo"-->
                      <!--                           :alt="product.name[locale]"-->
                      <!--                      />-->
                      <img class="ltablet:max-w-[175px] h-25 absolute bottom-0 inset-x-0 mx-auto max-w-[160px]"
                      <!--                           :src="product.photo"-->
                      src="/img/illustrations/dashboards/delivery/meal-1.png"

                      :alt="product.name[locale]"
                      />

                    </div>
                  </div>

                  <div class="mb-2">
                    <BaseHeading
                      tag="h4"
                      size="sm"
                      weight="medium"
                      class="text-muted-800 dark:text-muted-100"
                    >
                      <span>{{ product.name[locale] }}</span>
                    </BaseHeading>
                    <BaseParagraph
                      size="xs"
                      class="text-muted-500 dark:text-muted-400 line-clamp-1"
                    >
                      <!-- <span><div v-html="product.description[locale]"></div></span> -->
                    </BaseParagraph>
                  </div>
                  <div class="flex items-center justify-between">
                    <div
                      class="divide-muted-200 dark:divide-muted-700 flex items-center divide-x"
                    >
                      <div class="pe-4">
                        <span
                          v-if="product.count > 0" class="text-muted-800 dark:text-muted-100 font-sans font-bold"
                          dir="ltr"
                        >
                                    {{ formatPrice(product.price) }}<span class="letter-t mx-0.5"> T</span>
                        </span>

                      </div>
                    </div>
                    <div>
                      <BaseButtonAction v-if="product?.count > 0" shape="curved">
                        <span>{{ t('Detail') }}</span>
                      </BaseButtonAction>
                      <BaseButtonAction disabled="true" v-else shape="curved">
                        <span class="text-small">{{ t('notExists') }}</span>
                      </BaseButtonAction>

                    </div>
                  </div>
                </BaseCard>
              </NuxtLink>

              <NuxtLink
                v-for="product in app.filteredNotActiveProducts"
                :key="product.id"
                class="relative"
              >
                <BaseCard
                  shape="curved"
                  :data-nui-tooltip="t('Soon')"
                  class="hover:border-primary-500 hover:shadow-muted-300/30 dark:hover:shadow-muted-900/40 py-4 px-3 hover:shadow-xl"

                >


                  <div class="ltablet:h-28 relative mb-3 h-36 w-full rounded-xl sm:h-32 opacity-75 filter blur">
                    <div class="bg-muted-100 dark:bg-muted-900 relative w-full h-full rounded-xl"
                    >
                      <div class="blur-overlay w-full h-full absolute inset-0 bg-cover rounded-xl"
                           style="backdrop-filter: blur(10px);"></div>


                      <img class="ltablet:max-w-[175px] h-25 absolute bottom-0 inset-x-0 mx-auto max-w-[160px]"
                      src="/img/illustrations/dashboards/delivery/meal-1.png"
                           :alt="product.name[locale]"
                      />
                    </div>
                  </div>

                  <div class="mb-2">
                    <BaseHeading
                      tag="h4"
                      size="sm"
                      weight="medium"
                      class="text-muted-800 dark:text-muted-100"
                    >
                      <span>{{ product.name[locale] }}</span>
                    </BaseHeading>
                    <BaseParagraph
                      size="xs"
                      class="text-muted-500 dark:text-muted-400 line-clamp-1"
                    >
                      <span>{{ t("Soon") }}</span>
                    </BaseParagraph>
                    <BaseParagraph
                      size="xs"
                      class="text-muted-500 dark:text-muted-400 line-clamp-1"
                    >
                      <!-- <span><div v-html="product.description[locale]"></div></span> -->
                    </BaseParagraph>
                  </div>
                  <div class="flex items-center justify-between opacity-100 filter blur">
                    <div
                      class="divide-muted-200 dark:divide-muted-700 flex items-center divide-x"
                    >
                      <div class="pe-4">
                        <span
                          class="text-muted-800 dark:text-muted-100 font-sans font-bold" dir="ltr"
                        >
                          {{ formatPrice(product.price) }}<span class="letter-t mx-0.5"> T</span>
                        </span>
                      </div>
                    </div>
                    <!--                    <div>-->
                    <!--                      <BaseButtonAction shape="curved">-->
                    <!--                        <span>{{ t('Detail') }}</span>-->
                    <!--                      </BaseButtonAction>-->
                    <!--                    </div>-->
                  </div>
                </BaseCard>
              </NuxtLink>
            </div>

          </div>
          <div class="my-16 flex items-center justify-center">
            <BaseButton rounded="full" color="default" disabled="true">
              <Icon name="ph:dots-nine-bold" :class="locale==='fa'?'size-4 me-1' :'size-4' "/>
              <span>{{ t('Load') }}</span>
            </BaseButton>
          </div>

        </div>
      </div>
      <!-- Column -->

      <MyOrder/>
    </div>
  </div>

</template>
