<script setup lang="ts">
import { useAuthStore } from '~/stores/auth'

type TourStep = {
  route: string
  selector: string
  title: string
  description: string
  presenter: string
  adminOnly?: boolean
}

const authStore = useAuthStore()
const route = useRoute()
const isOpen = ref(false)
const currentIndex = ref(0)
const targetRect = ref<DOMRect | null>(null)
const locating = ref(false)
const viewportWidth = ref(0)

const allSteps: TourStep[] = [
  {
    route: '/dashboard',
    selector: '[data-tour="dashboard-overview"]',
    title: 'داشبورد عملیات انرژی',
    description: 'این صفحه نمای یکپارچه تولید خورشیدی، ذخیره باتری، مصرف ساختمان و تبادل انرژی را ارائه می‌کند.',
    presenter: 'در شروع ارائه بگویید هدف سامانه تبدیل داده خام مصرف به تصمیم عملیاتی برای ریزشبکه دانشگاه است.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="daily-chart"]',
    title: 'مصرف روزانه تجهیزات',
    description: 'مصرف تجهیزات در بازه روزانه کنار هم مقایسه می‌شود تا مصرف‌کننده‌های پرتوان سریع شناسایی شوند.',
    presenter: 'به ستون‌های کولر، بخاری و وسایل پرمصرف اشاره کنید و کاربرد نمودار در مدیریت بار را توضیح دهید.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="monthly-chart"]',
    title: 'تحلیل ماهانه',
    description: 'سال و ماه بدون نیاز به دکمه تأیید تغییر می‌کنند و نمودار همان لحظه از API به‌روزرسانی می‌شود.',
    presenter: 'توضیح دهید این بخش روند زمانی و تغییر الگوی مصرف در ماه‌های مختلف را نشان می‌دهد.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="peak-power"]',
    title: 'ساعت اوج و بیشینه توان',
    description: 'سامانه ساعت اوج مصرف و بیشترین توان هم‌زمان تجهیزات را محاسبه می‌کند.',
    presenter: 'این دو عدد ورودی تصمیم برای کاهش پیک، انتخاب باتری و جلوگیری از اضافه‌بار هستند.',
  },
  {
    route: '/dashboard',
    selector: '[data-tour="season-comparison"]',
    title: 'مقایسه بهینه‌سازی فصلی',
    description: 'هزینه یا مصرف بهینه‌شده و بهینه‌نشده برای چهار فصل با داده یک سال کامل مقایسه می‌شود.',
    presenter: 'اختلاف دو سری را به‌عنوان اثر راهکار بهینه‌سازی در هر فصل معرفی کنید.',
  },
  {
    route: '/profile/blocks',
    selector: '[data-tour="building-resources"]',
    title: 'ساختمان و منابع انرژی',
    description: 'مساحت، شماره واحد، بلوک و تجهیزات متصل، داده پایه محاسبات انرژی ساختمان هستند.',
    presenter: 'بگویید بدون مشخصات فیزیکی ساختمان، تخمین ظرفیت پنل و تحلیل مصرف قابل اتکا نیست.',
  },
  {
    route: '/profile/blocks',
    selector: '[data-tour="active-devices"]',
    title: 'تجهیزات فعال',
    description: 'توان AC و DC هر مصرف‌کننده ثبت می‌شود و تجهیزات منتسب به حساب در این قسمت دیده می‌شوند.',
    presenter: 'تفکیک AC/DC را به معماری ریزشبکه مستقیم و محاسبه دقیق‌تر تلفات ارتباط دهید.',
  },
  {
    route: '/profile/products',
    selector: '[data-tour="selectable-devices"]',
    title: 'انتخاب تجهیزات',
    description: 'کاربر تجهیزات ساختمان را از کاتالوگ داده‌دار انتخاب و به پروفایل انرژی خود متصل می‌کند.',
    presenter: 'توضیح دهید افزودن تجهیز idempotent است و ثبت تکراری ایجاد نمی‌کند.',
  },
  {
    route: '/profile/records',
    selector: '[data-tour="excel-import"]',
    title: 'ورود گروهی با Excel',
    description: 'فایل استاندارد Excel برای ورود سریع سوابق کنتور و آزمایش‌های مصرف بارگذاری می‌شود.',
    presenter: 'روی کاهش ورود دستی، اعتبارسنجی ستون‌ها و نمایش پیام موفقیت فقط بعد از پاسخ API تأکید کنید.',
  },
  {
    route: '/profile/records',
    selector: '[data-tour="consumption-records"]',
    title: 'سوابق مصرف',
    description: 'هر رکورد شامل تجهیز، زمان شروع، پایان و میزان مصرف است و مبنای تمام نمودارها محسوب می‌شود.',
    presenter: 'زنجیره داده را توضیح دهید: رکورد خام ← تجمیع API ← نمودار و شاخص تصمیم‌گیری.',
  },
  {
    route: '/shop',
    selector: '[data-tour="energy-market"]',
    title: 'بازار تبادل انرژی',
    description: 'انرژی ذخیره‌شده کاربران دیگر با موجودی و نرخ شفاف عرضه می‌شود؛ پیشنهاد خود کاربر نمایش داده نمی‌شود.',
    presenter: 'کنترل موجودی و جلوگیری از معامله با خود را به‌عنوان قواعد اصلی بازار بیان کنید.',
  },
  {
    route: '/profile/orders',
    selector: '[data-tour="energy-orders"]',
    title: 'تاریخچه خرید و فروش',
    description: 'سفارش‌ها با خریدار، فروشنده، باتری، مقدار، مبلغ و زمان ثبت قابل پیگیری‌اند.',
    presenter: 'توضیح دهید ثبت سفارش هم‌زمان موجودی ذخیره و انرژی فروخته‌شده را به‌روزرسانی می‌کند.',
  },
  {
    route: '/profile/settings',
    selector: '[data-tour="account-security"]',
    title: 'امنیت حساب',
    description: 'تغییر رمز با بررسی رمز فعلی، رمز جدید و تکرار آن انجام می‌شود.',
    presenter: 'به احراز هویت Bearer، کنترل نقش و ذخیره hash رمز به‌جای متن خام اشاره کنید.',
  },
  {
    route: '/panel',
    selector: '[data-tour="admin-panel"]',
    title: 'پنل مدیریت سامانه',
    description: 'مدیر کاربران، وضعیت حساب و تجهیزات منتسب به هر کاربر را در یک نمای یکپارچه مدیریت می‌کند.',
    presenter: 'این مرحله جمع‌بندی کنترل دسترسی نقش‌محور و دید مدیریتی کل سامانه است.',
    adminOnly: true,
  },
]

const steps = computed(() => allSteps.filter(step => !step.adminOnly || authStore.isAdmin))
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
  clearHighlight()
  const step = currentStep.value
  if (!step) return
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
