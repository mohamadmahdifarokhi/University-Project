<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

type TourStep = {
  route: string
  selector: string
  title: string
  description: string
  adminOnly?: boolean
  userOnly?: boolean
}

const authStore = useAuthStore()
const route = useRoute()
const isOpen = ref(false)
const currentIndex = ref(0)
const targetRect = ref<DOMRect | null>(null)
const locating = ref(false)
const targetMissing = ref(false)
const viewportWidth = ref(0)

const allSteps: TourStep[] = [
  {
    route: '/dashboard',
    selector: '[data-tour="dashboard-overview"]',
    title: 'داشبورد عملیات انرژی',
    description: 'این صفحه نمای یکپارچه‌ای از تولید خورشیدی، ذخیره‌سازی باتری، مصرف ساختمان و تبادل انرژی ارائه می‌کند و داده‌های خام مصرف را به اطلاعات قابل‌فهم برای پایش، تحلیل و تصمیم‌گیری عملیاتی در ریزشبکه تبدیل می‌کند.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-conversion"]',
    title: 'درصد تبدیل انرژی',
    description: 'این شاخص نشان می‌دهد چه سهمی از انرژی ورودی، پس از عبور از مسیر تولید، مصرف و ذخیره، به انرژی قابل استفاده تبدیل شده است. این عدد شاخص عملکرد ریزشبکه است و افزایش آن به معنی اتلاف کمتر در مسیر تبدیل انرژی است.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-battery"]',
    title: 'انرژی ذخیره‌شده در باتری',
    description: 'موجودی انرژی ذخیره‌شده و قابل استفاده باتری را نمایش می‌دهد. این مقدار از سرویس باتری دریافت می‌شود و مقدار ثابت نمایشی نیست؛ برای پوشش بار در زمان اوج و تصمیم‌گیری درباره عرضه انرژی در بازار کاربرد دارد.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-investment"]',
    title: 'سرمایه‌گذاری و صرفه‌جویی سالانه',
    description: 'برآورد اقتصادی سالانه حاصل از تولید خورشیدی، کاهش مصرف شبکه و تبادل انرژی را به تومان نشان می‌دهد و ارتباط تحلیل انرژی با تصمیم سرمایه‌گذاری را در قالب مالی مشخص می‌کند.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-emissions"]',
    title: 'کاهش انتشار گازهای گلخانه‌ای',
    description: 'کاهش تقریبی انتشار دی‌اکسیدکربن به‌ازای انرژی مدیریت‌شده را نمایش می‌دهد و اثر زیست‌محیطی سامانه را قابل اندازه‌گیری می‌کند. مقدار کمتر مصرف برق آلاینده و استفاده بیشتر از تولید خورشیدی، مستقیماً بر این شاخص اثر می‌گذارد.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-ac-dc"]',
    title: 'نسبت توان متناوب و مستقیم',
    description: 'تعادل توان در مسیرهای جریان متناوب و مستقیم را نشان می‌دهد و برای بررسی معماری ریزشبکه و انتخاب مبدل کاربرد دارد. این نسبت به شناسایی عدم تعادل بار و بررسی عملکرد مبدل تبدیل‌کننده کمک می‌کند.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-efficiency"]',
    title: 'بازده سامانه',
    description: 'نسبت انرژی مفید خروجی به انرژی ورودی را به درصد نشان می‌دهد؛ هرچه این عدد بیشتر باشد، سهم اتلاف کمتر است. این شاخص خلاصه عملکرد کل زنجیره تولید، تبدیل، مصرف و ذخیره است.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-solar"]',
    title: 'تولید پنل خورشیدی',
    description: 'توان یا انرژی محاسبه‌شده تولید پنل‌های خورشیدی را نمایش می‌دهد و یکی از منابع اصلی شارژ باتری و تأمین بار است. میزان تولید با تابش ارتباط دارد و بر مصرف ساختمان و انرژی قابل عرضه در بازار اثر می‌گذارد.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="metric-charge"]',
    title: 'وضعیت شارژ باتری',
    description: 'درصد ظرفیت یا وضعیت شارژ قابل استفاده باتری را نشان می‌دهد و برای تصمیم شارژ، تخلیه و عرضه انرژی مهم است. این درصد مقدار ظرفیت باقی‌مانده برای پشتیبانی از بار یا فروش انرژی را مشخص می‌کند.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="daily-chart"]',
    title: 'مصرف روزانه تجهیزات',
    description: 'مصرف تجهیزات در بازه روزانه کنار هم مقایسه می‌شود تا مصرف‌کننده‌های پرتوان سریع شناسایی شوند. ستون‌های مربوط به کولر، بخاری و سایر وسایل پرمصرف برای مدیریت بار و اولویت‌بندی اقدامات بهینه‌سازی کاربرد دارند.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="monthly-chart"]',
    title: 'تحلیل ماهانه',
    description: 'سال و ماه بدون نیاز به دکمه تأیید تغییر می‌کنند و نمودار همان لحظه از سرویس به‌روزرسانی می‌شود. این بخش روند زمانی و تغییر الگوی مصرف در ماه‌های مختلف را نشان می‌دهد.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="peak-power"]',
    title: 'ساعت اوج و بیشینه توان',
    description: 'سامانه ساعت اوج مصرف و بیشترین توان هم‌زمان تجهیزات را محاسبه می‌کند. این دو عدد ورودی تصمیم برای کاهش پیک، انتخاب باتری و جلوگیری از اضافه‌بار هستند.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="season-comparison"]',
    title: 'مقایسه بهینه‌سازی فصلی',
    description: 'هزینه یا مصرف بهینه‌شده و بهینه‌نشده برای چهار فصل با داده یک سال کامل و هزینه‌های محاسبه‌شده به تومان مقایسه می‌شود. اختلاف دو سری، اثر راهکارهای بهینه‌سازی در هر فصل را مشخص می‌کند.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="season-summary"]',
    title: 'خلاصه وضعیت فصل',
    description: 'خلاصه فصل جاری، وضعیت تولید و مصرف را کنار هم قرار می‌دهد تا تغییرات فصلی سریع‌تر تفسیر شوند و امکان تطبیق آن‌ها با نمودار مقایسه فصلی فراهم باشد.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="add-record"]',
    title: 'ثبت رکورد مصرف',
    description: 'با انتخاب دستگاه و بازه زمانی، یک رکورد مصرف جدید ثبت می‌شود و داده آن در تحلیل‌ها و نمودارهای بعدی وارد می‌شود. فرم پیش از ارسال اعتبارسنجی می‌شود و تاریخ‌ها با تقویم ایرانی قابل ورود هستند.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="selected-devices"]',
    title: 'دستگاه‌های انتخاب‌شده',
    description: 'فهرست تجهیزات متصل به حساب کاربر در این بخش دیده می‌شود و هنگام ثبت رکورد، همین تجهیزات در فهرست انتخاب قرار می‌گیرند. زنجیره داده از تجهیز انتخاب‌شده به رکورد مصرف و سپس نمودارهای داشبورد ادامه پیدا می‌کند.',
    userOnly: true,
  },
  {
    route: '/dashboard',
    selector: '[data-tour="latest-orders"]',
    title: 'آخرین سفارش‌ها',
    description: 'خلاصه آخرین خریدوفروش‌های انرژی با نام کاربر، مقدار، کارمزد، مبلغ به تومان، تاریخ ایرانی و قیمت نمایش داده می‌شود. تراکنش‌ها قابل پیگیری هستند و نام کاربر به‌جای شناسه فنی نمایش داده می‌شود.',
    userOnly: true,
  },
  {
    route: '/profile/blocks',
    selector: '[data-tour="building-resources"]',
    title: 'ساختمان و منابع انرژی',
    description: 'مساحت، شماره واحد، بلوک و تجهیزات متصل، داده پایه محاسبات انرژی ساختمان هستند. مشخصات فیزیکی ساختمان برای تخمین ظرفیت پنل و تحلیل قابل اتکای مصرف ضروری است.',
  },
  {
    route: '/profile/blocks',
    selector: '[data-tour="active-devices"]',
    title: 'تجهیزات فعال',
    description: 'توان جریان متناوب و مستقیم هر مصرف‌کننده ثبت می‌شود و تجهیزات منتسب به حساب در این قسمت دیده می‌شوند. این تفکیک با معماری ریزشبکه مستقیم و محاسبه دقیق‌تر تلفات ارتباط دارد.',
  },
  {
    route: '/profile/products',
    selector: '[data-tour="selectable-devices"]',
    title: 'انتخاب تجهیزات',
    description: 'کاربر تجهیزات ساختمان را از کاتالوگ داده‌دار انتخاب و به پروفایل انرژی خود متصل می‌کند. افزودن تجهیز بدون ثبت تکراری انجام می‌شود.',
  },
  {
    route: '/profile/records',
    selector: '[data-tour="excel-import"]',
    title: 'ورود گروهی از فایل صفحه‌گسترده',
    description: 'فایل صفحه‌گسترده استاندارد برای ورود سریع سوابق کنتور و آزمایش‌های مصرف بارگذاری می‌شود. این روش ورود دستی را کاهش می‌دهد، ستون‌ها را اعتبارسنجی می‌کند و پیام موفقیت را پس از پاسخ سرویس نمایش می‌دهد.',
  },
  {
    route: '/profile/records',
    selector: '[data-tour="consumption-records"]',
    title: 'سوابق مصرف',
    description: 'هر رکورد شامل تجهیز، زمان شروع، پایان و میزان مصرف است و مبنای تمام نمودارها محسوب می‌شود. مسیر داده از رکورد خام به تجمیع سرویس و سپس نمودارها و شاخص‌های تصمیم‌گیری می‌رسد.',
  },
  {
    route: '/shop',
    selector: '[data-tour="energy-market"]',
    title: 'بازار تبادل انرژی',
    description: 'انرژی ذخیره‌شده کاربران دیگر با موجودی و نرخ شفاف عرضه می‌شود؛ پیشنهاد خود کاربر نمایش داده نمی‌شود. کنترل موجودی و جلوگیری از معامله با خود، از قواعد اصلی بازار هستند.',
  },
  {
    route: '/profile/orders',
    selector: '[data-tour="energy-orders"]',
    title: 'تاریخچه خرید و فروش',
    description: 'سفارش‌ها با خریدار، فروشنده، باتری، مقدار، مبلغ و زمان ثبت قابل پیگیری‌اند. ثبت سفارش، موجودی ذخیره و انرژی فروخته‌شده را هم‌زمان به‌روزرسانی می‌کند.',
  },
  {
    route: '/profile/settings',
    selector: '[data-tour="account-security"]',
    title: 'امنیت حساب',
    description: 'تغییر رمز با بررسی رمز فعلی، رمز جدید و تکرار آن انجام می‌شود. توکن دسترسی، کنترل نقش و نگهداری رمز به‌صورت رمزنگاری‌شده، لایه‌های اصلی امنیت حساب هستند.',
  },
  {
    route: '/panel',
    selector: '[data-tour="admin-panel"]',
    title: 'پنل مدیریت سامانه',
    description: 'مدیر کاربران، وضعیت حساب و تجهیزات منتسب به هر کاربر را در یک نمای یکپارچه مدیریت می‌کند. این بخش دید مدیریتی کل سامانه و کنترل دسترسی نقش‌محور را جمع‌بندی می‌کند.',
    adminOnly: true,
  },
]

const steps = computed(() => allSteps.filter(step =>
  (!step.adminOnly || authStore.isAdmin)
  && (!step.userOnly || (!authStore.isAdmin && !authStore.isMng)),
))
const currentStep = computed(() => steps.value[currentIndex.value])
const progress = computed(() => `${currentIndex.value + 1} از ${steps.value.length}`)

function clearHighlight() {
  document.querySelectorAll('[data-presentation-highlight]').forEach((element) => {
    element.removeAttribute('data-presentation-highlight')
  })
  targetRect.value = null
}

async function locateStep() {
  locating.value = true
  targetMissing.value = false
  clearHighlight()
  const step = currentStep.value
  if (!step) {
    locating.value = false
    return
  }
  if (route.path !== step.route) {
    await navigateTo(step.route)
  }
  await nextTick()

  let target: HTMLElement | null = null
  for (let attempt = 0; attempt < 100 && !target; attempt++) {
    target = document.querySelector<HTMLElement>(step.selector)
    if (!target) await new Promise(resolve => setTimeout(resolve, 100))
  }
  if (target) {
    target.scrollIntoView({ behavior: 'smooth', block: 'center' })
    await new Promise(resolve => setTimeout(resolve, 450))
    target.setAttribute('data-presentation-highlight', 'true')
    targetRect.value = target.getBoundingClientRect()
  } else {
    targetMissing.value = true
  }
  locating.value = false
}

async function startTour() {
  currentIndex.value = 0
  isOpen.value = true
  await locateStep()
}

async function next() {
  if (currentIndex.value >= steps.value.length - 1) {
    close()
    return
  }
  currentIndex.value++
  await locateStep()
}

async function previous() {
  if (currentIndex.value === 0) return
  currentIndex.value--
  await locateStep()
}

function close() {
  clearHighlight()
  isOpen.value = false
}

function updateRect() {
  viewportWidth.value = window.innerWidth
  if (!isOpen.value) return
  const target = document.querySelector(currentStep.value?.selector || '')
  if (target) targetRect.value = target.getBoundingClientRect()
}

onMounted(() => {
  viewportWidth.value = window.innerWidth
  window.addEventListener('resize', updateRect)
  window.addEventListener('scroll', updateRect, true)
})
onUnmounted(() => {
  window.removeEventListener('resize', updateRect)
  window.removeEventListener('scroll', updateRect, true)
  clearHighlight()
})
</script>

<template>
  <BaseButton
    color="primary"
    size="sm"
    data-tour-launcher
    @click="startTour"
  >
    <Icon name="ph:presentation-chart-duotone" class="me-2 size-5" />
    <span class="hidden sm:inline">راهنمای ارائه</span>
    <span class="sm:hidden">راهنما</span>
  </BaseButton>

  <Teleport to="body">
    <div v-if="isOpen" class="presentation-tour" dir="rtl">
      <template v-if="targetRect">
        <div class="tour-shade" :style="{ inset: `0 0 auto 0`, height: `${Math.max(0, targetRect.top - 8)}px` }" />
        <div class="tour-shade" :style="{ top: `${targetRect.bottom + 8}px`, right: '0', bottom: '0', left: '0' }" />
        <div class="tour-shade" :style="{ top: `${Math.max(0, targetRect.top - 8)}px`, right: `${viewportWidth - targetRect.left + 8}px`, height: `${targetRect.height + 16}px`, left: '0' }" />
        <div class="tour-shade" :style="{ top: `${Math.max(0, targetRect.top - 8)}px`, right: '0', height: `${targetRect.height + 16}px`, width: `${Math.max(0, viewportWidth - targetRect.right - 8)}px` }" />
      </template>
      <div v-else class="tour-shade inset-0" />

      <BaseCard class="tour-panel p-5">
        <div class="mb-3 flex items-center justify-between gap-4">
          <BaseTag color="primary" variant="pastel">{{ progress }}</BaseTag>
          <button type="button" aria-label="بستن راهنما" class="text-muted-500 hover:text-danger-500" @click="close">
            <Icon name="ph:x-bold" class="size-5" />
          </button>
        </div>
        <BaseHeading as="h2" size="lg">{{ currentStep?.title }}</BaseHeading>
        <BaseParagraph class="text-muted-600 dark:text-muted-300 mt-2">
          {{ currentStep?.description }}
        </BaseParagraph>
        <BaseMessage v-if="targetMissing" type="warning" class="mt-4">
          این بخش در نقش فعلی یا با داده فعلی در دسترس نیست؛ مرحله بعد را انتخاب کنید.
        </BaseMessage>
        <div class="mt-5 flex items-center justify-between gap-3">
          <BaseButton :disabled="currentIndex === 0 || locating" @click="previous">
            قبلی
          </BaseButton>
          <BaseButton color="primary" :loading="locating" @click="next">
            {{ currentIndex === steps.length - 1 ? 'پایان ارائه' : 'بعدی' }}
          </BaseButton>
        </div>
      </BaseCard>
    </div>
  </Teleport>
</template>

<style>
[data-presentation-highlight] {
  position: relative !important;
  border-radius: 12px;
  outline: 4px solid rgb(var(--color-primary-500));
  outline-offset: 4px;
}
.presentation-tour {
  position: fixed;
  inset: 0;
  z-index: 2147483645;
  pointer-events: none;
}
.tour-shade {
  position: fixed;
  z-index: 10000;
  background: rgb(7 16 33 / 72%);
  pointer-events: auto;
}
.tour-panel {
  position: fixed;
  z-index: 2147483647 !important;
  right: 50%;
  bottom: 24px;
  width: min(560px, calc(100vw - 32px));
  transform: translateX(50%);
  pointer-events: auto;
  box-shadow: 0 24px 70px rgb(0 0 0 / 35%);
  max-height: calc(100dvh - 32px);
  overflow-y: auto;
}
@media (max-width: 639px) {
  .tour-panel {
    bottom: 12px;
    width: calc(100vw - 24px);
  }
}
</style>
