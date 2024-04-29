<script setup lang="ts">
import {useAppStore} from '~/../.app/stores/app';
import {storeToRefs} from "pinia";

const formatPrice = (price: number) => {
  if (price) {
    return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");

  }
};
const app = useAppStore();

const {flag} = storeToRefs(app);
const {t} = useI18n({useScope: "local"})

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


const {y} = useNinjaWindowScroll()

const gaugePersonal = reactive(useGaugePersonal())
const localPath = useLocalePath();

function useGaugePersonal() {
  const {primary} = useTailwindColors()
  const type = 'radialBar'
  const height = 220

  const options = {
    title: {
      text: undefined,
    },
    chart: {
      sparkline: {
        enabled: true,
      },
      toolbar: {
        show: false,
      },
    },
    colors: [primary.value],
    plotOptions: {
      radialBar: {
        startAngle: -90,
        endAngle: 90,
        track: {
          background: '#e7e7e7',
          strokeWidth: '97%',
          margin: 5, // margin is in pixels
          dropShadow: {
            enabled: false,
            top: 2,
            left: 0,
            color: '#999',
            opacity: 1,
            blur: 2,
          },
        },
        hollow: {
          margin: 0,
          size: '35%',
        },
        dataLabels: {
          name: {
            show: false,
          },
          value: {
            offsetY: -2,
            fontSize: '22px',
          },
        },
      },
    },
    fill: {
      type: 'gradient',
      gradient: {
        shade: 'light',
        shadeIntensity: 0.1,
        inverseColors: false,
        opacityFrom: 1,
        opacityTo: 1,
        stops: [0, 50, 53, 91],
      },
    },
    labels: ['Average Results'],
  }

  const series = shallowRef([76])

  return {
    type,
    height,
    options,
    series,
  }
}

const {locale, locales} = useI18n()

</script>

<template>
  <div
    class="dark:to-muted-900 relative min-h-screen overflow-hidden bg-gradient-to-b from-transparent to-white"
    :dir="locale === 'en' ? 'ltr' : 'rtl'"
  >
    <div class="gridlines absolute inset-x-0 z-10 -mt-8 py-20"/>
    <div class="absolute inset-x-0 z-20 -mt-24 py-20">
      <div
        class="mt-12 grid grid-cols-2 -space-x-52 opacity-60 2xl:mx-auto 2xl:max-w-6xl dark:opacity-50"
      >
        <div
          class="from-primary-200 to-primary-400 h-40 bg-gradient-to-br blur-3xl dark:from-blue-700"
        />
        <div
          class="dark:to-primary-600 h-24 bg-gradient-to-r from-indigo-400 to-indigo-700 blur-3xl"
        />
      </div>
    </div>
    <div class="mx-auto w-full max-w-7xl px-4">
      <div class="relative z-30 pt-32 text-center">
        <BaseHeading
          as="h1"
          size="5xl"
          weight="light"
          lead="tight"
          class="text-muted-800 xs:!text-4xl mx-auto mb-4 max-w-2xl dark:text-white"
        >
          {{ t('DC Micro-grid Planner') }}
          <!--          <span-->
          <!--            class="text-primary-500 font-hairline underline decoration-dotted"-->
          <!--          >ract</span>-->
        </BaseHeading>
        <BaseParagraph
          size="lg"
          class="text-muted-500 dark:text-muted-100 mx-auto mb-4 max-w-2xl"
        >
          {{ t('AccountOptions') }}
        </BaseParagraph>
        <div class="flex items-center justify-center">
          <BaseButton
            rounded="lg"
            color="primary"
            :to="localPath(`/`)"
            shadow="hover"
            class="!h-12 w-44"
          >
            {{ t('Shop') }}
          </BaseButton>
        </div>

      </div>
      <!-- Components -->
      <fieldset
        disabled
        class="ltablet:min-h-[760px] min-h-[2075px] w-full sm:min-h-[760px] lg:min-h-[750px]"
        aria-hidden="true"
      >
        <div
          class="group-[&.scrolled]/landing:bg-muted-100 group-[&.scrolled]/landing:dark:bg-muted-900 group-[&.scrolled]/landing:border-muted-200 group-[&.scrolled]/landing:dark:border-muted-800 group-[&.scrolled]/landing:ltablet:ps-6 relative z-30 mt-12 overflow-hidden border group-[&.scrolled]/landing:rounded-xl group-[&:not(.scrolled)]/landing:border-transparent group-[&.scrolled]/landing:pb-6 group-[&.scrolled]/landing:pe-6 group-[&.scrolled]/landing:ps-6 group-[&.scrolled]/landing:pt-20 motion-safe:transition-all motion-safe:duration-300 group-[&.scrolled]/landing:lg:ps-6"
        >
          <!-- Fake sidebar -->
          <!-- <div
            class="ltablet:w-16 ltablet:flex dark:bg-muted-800 absolute left-0 top-0 hidden h-full w-20 flex-col bg-white group-[&.scrolled]/landing:translate-x-0 group-[&:not(.scrolled)]/landing:-translate-x-full group-[&.scrolled]/landing:opacity-100 group-[&:not(.scrolled)]/landing:opacity-0 motion-safe:transition-all motion-safe:duration-200 lg:flex"
          >
            <div class="flex h-20 w-full items-center justify-center">
              <TairoLogo class="text-primary-500 size-8" />
            </div>
            <div class="flex h-16 w-full items-center justify-center">
              <div
                class="nui-mask nui-mask-blob bg-primary-500/10 flex size-12 items-center justify-center motion-safe:transition-colors motion-safe:duration-200"
              >
                <Icon
                  name="ph:house-duotone"
                  class="text-primary-500 size-5"
                />
              </div>
            </div>
            <div class="flex h-16 w-full items-center justify-center">
              <div
                class="nui-mask nui-mask-blob hover:bg-muted-100 dark:hover:bg-muted-700/50 flex size-12 items-center justify-center motion-safe:transition-colors motion-safe:duration-200"
              >
                <Icon
                  name="ph:grid-four-duotone"
                  class="text-muted-400 size-5"
                />
              </div>
            </div>
            <div class="flex h-16 w-full items-center justify-center">
              <div
                class="nui-mask nui-mask-blob hover:bg-muted-100 dark:hover:bg-muted-700/50 flex size-12 items-center justify-center motion-safe:transition-colors motion-safe:duration-200"
              >
                <Icon name="ph:users-duotone" class="text-muted-400 size-5" />
              </div>
            </div>
            <div class="flex h-16 w-full items-center justify-center">
              <div
                class="nui-mask nui-mask-blob hover:bg-muted-100 dark:hover:bg-muted-700/50 flex size-12 items-center justify-center motion-safe:transition-colors motion-safe:duration-200"
              >
                <Icon
                  name="ph:chat-circle-duotone"
                  class="text-muted-400 size-5"
                />
              </div>
            </div>
            <div class="mt-auto flex h-16 w-full items-center justify-center">
              <div
                class="nui-mask nui-mask-blob hover:bg-muted-100 dark:hover:bg-muted-700/50 flex size-12 items-center justify-center motion-safe:transition-colors motion-safe:duration-200"
              >
                <Icon
                  name="ph:gear-six-duotone"
                  class="text-muted-400 size-5"
                />
              </div>
            </div>
            <div class="flex h-16 w-full items-center justify-center">
              <div
                class="nui-mask nui-mask-blob hover:bg-muted-100 dark:hover:bg-muted-700/50 flex size-12 items-center justify-center motion-safe:transition-colors motion-safe:duration-200"
              >
                <BaseAvatar
                  rounded="none"
                  size="sm"
                  src="/img/avatars/24.svg"
                  class="nui-mask nui-mask-blob"
                />
              </div>
            </div>
          </div> -->
          <!-- Fake navbar -->
          <div
            class="ltablet:ps-6 absolute left-0 top-0 flex h-20 w-full items-center justify-between pe-6 ps-6 group-[&.scrolled]/landing:translate-y-0 group-[&:not(.scrolled)]/landing:-translate-y-full group-[&.scrolled]/landing:opacity-100 group-[&:not(.scrolled)]/landing:opacity-0 motion-safe:transition-all motion-safe:duration-200 lg:ps-6"
          >
            <div class="flex h-full items-center gap-4">
              <!-- <div
                class="nui-mask nui-mask-blob dark:hover:bg-muted-800 flex size-10 items-center justify-center hover:bg-white motion-safe:transition-colors motion-safe:duration-200"
              >
                <Icon name="lucide:menu" class="text-muted-400 size-5" />
              </div> -->

              <BaseText class="hidden sm:inline-block">
                <img
                  :src="'/img/accountract.png'"
                  alt="GPT Logo"
                  class="md:h-8 md:w-8 md:mb-1 sm:h-11 sm:w-12 h-11 w-12 sm:block hidden"
                />
              </BaseText>
            </div>
            <div class="flex h-full items-center justify-end gap-1">
              <div
                class="nui-mask nui-mask-blob dark:hover:bg-muted-800 flex size-10 items-center justify-center hover:bg-white motion-safe:transition-colors motion-safe:duration-200"
              >
                <!-- <Icon
                  name="ph:circles-four-duotone"
                  class="text-muted-400 size-5"
                /> -->
                <img class="grayscale-100  dark:invert  w-6 h-5" src="/img/icons/.png" alt="flag icon">

              </div>


              <div
                class="nui-mask nui-mask-blob dark:hover:bg-muted-800 flex size-10 items-center justify-center hover:bg-white motion-safe:transition-colors motion-safe:duration-200"
              >
                <!-- <Icon name="ph:bell-duotone" class="text-muted-400 size-5" /> -->
                <BaseThemeToggle/>

              </div>


              <div
                class="nui-mask nui-mask-blob dark:hover:bg-muted-800 flex size-10 items-center justify-center hover:bg-white motion-safe:transition-colors motion-safe:duration-200"
              >
                <!-- <Icon
                  name="ph:translate-duotone"
                  class="text-muted-400 size-5"
                /> -->
                <img
                  v-if="flag"
                  :src="locale === 'en' ? '/img/icons/flags/united-states-of-america.svg' : '/img/icons/flags/iran.png'"
                  :class="locale === 'en' ? 'h-7 w-7 rounded-full' : 'h-8 w-8 rounded-full'"
                  alt=""
                />
              </div>
              <div
                class="nui-mask nui-mask-blob dark:hover:bg-muted-800 flex size-10 items-center justify-center hover:bg-white motion-safe:transition-colors motion-safe:duration-200"
              >
                <BaseAvatar
                  rounded="none"
                  size="xs"
                  src="/img/avatars/1.svg"
                  class="nui-mask nui-mask-blob"
                />
              </div>
            </div>
          </div>
          <div
            class="ltablet:grid-cols-3 ltablet:gap-6 grid grid-cols-1 gap-6 sm:grid-cols-3 sm:gap-3 lg:grid-cols-4 lg:gap-4"
          >
            <!-- Col1 -->
            <div
              class="ltablet:gap-6 group-[&:not(.scrolled)]/landing:ltablet:mt-24 group-[&:not(.scrolled)]/landing:ptablet:mt-24 flex flex-col gap-6 sm:gap-3 lg:gap-4 group-[&:not(.scrolled)]/landing:lg:mt-24"
            >
              <!-- Widget -->
              <!-- <BaseCard
                rounded="lg"
                elevated
                class="flex flex-col p-6"
              >
                <div class="mb-6 flex items-center justify-between">
                  <BaseHeading
                    as="h3"
                    size="sm"
                    weight="semibold"
                    lead="tight"
                    class="text-muted-800 dark:text-white"
                  >
                    <span>Personal Score</span>
                  </BaseHeading>
                </div>
                <div class="flex justify-center py-16">
                  <AddonApexcharts
                    v-bind="gaugePersonal"
                    class="-mt-14 motion-safe:transition-all motion-safe:duration-200"
                  />
                </div>
                <div class="mt-auto text-center">
                  <BaseParagraph size="sm">
                    <span class="text-muted-400">
                      Your score has been calculated based on the latest metrics
                    </span>
                  </BaseParagraph>
                </div>
              </BaseCard> -->

              <NuxtLink
                v-for="product in app.filteredProducts"
                :key="product.id"
                :to="localPath(`/product/${product.slug}`)"
                class="relative"
              >
                <BaseCard
                  rounded="lg"
                  elevated
                  class="flex flex-col p-6 py-10 hover:border-primary-500 hover:shadow-muted-300/30 dark:hover:shadow-muted-900/40 p-3 hover:shadow-xl"
                >


                  <div class="ltablet:h-28 relative mb-3 h-36 w-full rounded-xl sm:h-32">
                    <div class="bg-muted-100 dark:bg-muted-900 relative w-full h-full rounded-xl"
                         :style="{ backgroundImage: `url('${product.background}')`, backgroundSize: 'cover', backgroundPosition: 'center' }">
                      <div class="blur-overlay w-full h-full absolute inset-0 bg-cover rounded-xl"
                           style="backdrop-filter: blur(10px);"></div>
                      <img class="ltablet:max-w-[75px] h-25 absolute   max-w-[60px]"
                           :src="product.logo"
                           :alt="product.name[locale]"
                      />
                      <BasePlaceload class="w-full h-full rounded-xl"></BasePlaceload>
                      <img class="ltablet:max-w-[175px] h-25 absolute bottom-0 inset-x-0 mx-auto max-w-[160px]"
                           :src="product.photo"
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
                          class="text-muted-800 dark:text-muted-100 font-sans font-bold"
                        >
                                    {{ formatPrice(product.price) }}<span class="letter-t mx-0.5"> T</span>
                        </span>
                      </div>
                    </div>
                    <div>
                      <!-- <BaseButtonAction shape="curved"> -->
                      <!-- <span>{{ t('Detail') }}</span> -->
                      <!-- </BaseButtonAction> -->
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
                  rounded="lg"
                  elevated
                  class="flex flex-col p-6 py-10 hover:border-primary-500 hover:shadow-muted-300/30 dark:hover:shadow-muted-900/40 p-3 hover:shadow-xl"
                >
                  <div class="ltablet:h-28 relative mb-3 h-36 w-full rounded-xl sm:h-32 opacity-75 filter blur">
                    <div class="bg-muted-100 dark:bg-muted-900 relative w-full h-full rounded-xl"
                         :style="{ backgroundImage: `url('${product.background}')`, backgroundSize: 'cover', backgroundPosition: 'center' }">
                      <div class="blur-overlay w-full h-full absolute inset-0 bg-cover rounded-xl"
                           style="backdrop-filter: blur(10px);"></div>
                      <img class="ltablet:max-w-[75px] h-25 absolute   max-w-[60px]"
                           :src="product.logo"
                           :alt="product.name[locale]"
                      />
                      <BasePlaceload class="w-full h-full rounded-xl"></BasePlaceload>

                      <img class="ltablet:max-w-[175px] h-25 absolute bottom-0 inset-x-0 mx-auto max-w-[160px]"
                           :src="product.photo"
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
                  </div>
                  <div class="flex items-center justify-between opacity-100 filter blur">
                    <div
                      class="divide-muted-200 dark:divide-muted-700 flex items-center divide-x"
                    >
                      <div class="pe-4">
          <span
            class="text-muted-800 dark:text-muted-100 font-sans font-bold"
          >
                                    {{ formatPrice(product.price) }}<span class="letter-t mx-0.5"> T</span>
          </span>
                      </div>
                    </div>
                    <div>
                      <!-- <BaseButtonAction shape="curved"> -->
                      <!-- <span>{{ t('Detail') }}</span> -->
                      <!-- </BaseButtonAction> -->
                    </div>
                  </div>
                </BaseCard>
              </NuxtLink>

            </div>
            <!-- Col2 -->
            <div

              class="ltablet:gap-6 group-[&:not(.scrolled)]/landing:ltablet:mt-16 group-[&:not(.scrolled)]/landing:ptablet:mt-16 flex flex-col gap-6 sm:hidden sm:gap-3 lg:flex lg:gap-4 group-[&:not(.scrolled)]/landing:lg:mt-16"

            >
              <!-- Widget -->
              <!-- <BaseCard
                rounded="lg"
                elevated
                class="p-6"
              >
                <DemoInboxMessage
                  picture="/img/avatars/10.svg"
                  name="Kendra W."
                  title="Design Project"
                  text="Where are we in terms of design? We need to review the new screens."
                  time="28 minutes"
                  rounded="lg"
                />
              </BaseCard> -->

              <NuxtLink
                v-for="product in app.filteredNotActiveProducts"
                :key="product.id"
                class="relative"
              >
                <BaseCard
                  rounded="lg"
                  elevated
                  class="flex flex-col p-6 py-10 hover:border-primary-500 hover:shadow-muted-300/30 dark:hover:shadow-muted-900/40 p-3 hover:shadow-xl"
                >
                  <div class="ltablet:h-28 relative mb-3 h-36 w-full rounded-xl sm:h-32 opacity-75 filter blur">
                    <div class="bg-muted-100 dark:bg-muted-900 relative w-full h-full rounded-xl"
                         :style="{ backgroundImage: `url('${product.background}')`, backgroundSize: 'cover', backgroundPosition: 'center' }">
                      <div class="blur-overlay w-full h-full absolute inset-0 bg-cover rounded-xl"
                           style="backdrop-filter: blur(10px);"></div>
                      <img class="ltablet:max-w-[75px] h-25 absolute   max-w-[60px]"
                           :src="product.logo"
                           :alt="product.name[locale]"
                      />
                      <BasePlaceload class="w-full h-full rounded-xl"></BasePlaceload>

                      <img class="ltablet:max-w-[175px] h-25 absolute bottom-0 inset-x-0 mx-auto max-w-[160px]"
                           :src="product.photo"
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
                  </div>
                  <div class="flex items-center justify-between opacity-100 filter blur">
                    <div
                      class="divide-muted-200 dark:divide-muted-700 flex items-center divide-x"
                    >
                      <div class="pe-4">
          <span
            class="text-muted-800 dark:text-muted-100 font-sans font-bold"
          >
            {{ product.price }} T
          </span>
                      </div>
                    </div>
                    <div>
                      <!-- <BaseButtonAction shape="curved"> -->
                      <!-- <span>{{ t('Detail') }}</span> -->
                      <!-- </BaseButtonAction> -->
                    </div>
                  </div>
                </BaseCard>
              </NuxtLink>


              <!-- Widget -->
              <!--              <BaseCard-->
              <!--                rounded="lg"-->
              <!--                elevated-->
              <!--                class="p-6"-->
              <!--              >-->
              <!--                <DemoInfoBadges-->
              <!--                  image="/img/illustrations/widgets/1.svg"-->
              <!--                  badge-small="/img/illustrations/widgets/3.svg"-->
              <!--                  badge-medium="/img/illustrations/widgets/2.svg"-->
              <!--                  title="You've unlocked 2 new Achievements"-->
              <!--                  text="Congrats, your efforts have been rewarded. Keep up like this!"-->
              <!--                />-->

              <!--              </BaseCard>-->
            </div>
            <!-- Col3 -->
            <div
              class="ltablet:gap-6 flex flex-col gap-6 sm:gap-3 lg:gap-4"
            >
              <!-- Widget -->
              <BaseCard
                rounded="lg"
                elevated
                class="p-4"
              >
                <DemoTeamSearchCompact rounded="lg"/>
              </BaseCard>
              <!-- Widget -->
              <BaseCard
                rounded="lg"
                elevated
                class="p-3"
              >
                <DemoVideoCompact rounded="lg"/>
              </BaseCard>
            </div>
            <!-- Col4 -->
            <div
              class="ltablet:gap-6 group-[&:not(.scrolled)]/landing:ltablet:mt-10 group-[&:not(.scrolled)]/landing:ptablet:mt-10 flex flex-col gap-6 sm:gap-3 lg:gap-4 group-[&:not(.scrolled)]/landing:lg:mt-10"
              dir="ltr"
            >
              <!-- Widget -->
              <BaseCard
                rounded="lg"
                elevated
                class="p-6"
              >
                <DemoProgressCircle
                  image="/img/avatars/1.svg"
                  :title="`${y < 100 ? Math.trunc(y / 2) : 100}%`"
                  text="Fast delivery 🚀"
                  :value="y < 100 ? Math.trunc(y / 2) : 100"
                />
              </BaseCard>
              <!-- Widget -->
              <BaseCard
                rounded="lg"
                elevated
                class="p-6"
              >
                <DemoFollowersCompact/>
              </BaseCard>
            </div>
          </div>
        </div>
      </fieldset>

      <!-- Components -->
      <!-- <LandingHeroMockup /> -->
    </div>
  </div>
</template>

<style scoped>
.gridlines {
  background-image: url(/img/illustrations/gridlines.svg);
}

.dark .gridlines {
  background-image: url(/img/illustrations/gridlines-dark.svg);
}
</style>
