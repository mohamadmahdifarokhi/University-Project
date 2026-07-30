<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { Field, useForm } from 'vee-validate'
import { z } from 'zod'
import { storeToRefs } from 'pinia'
import { useAppStore } from '~/stores/app'

definePageMeta({ title: 'ساختمان و منابع انرژی', middleware: 'authenticated' })
useSeoMeta({ description: 'مدیریت مشخصات ساختمان و تجهیزات مصرف‌کننده انرژی' })

const app = useAppStore()
const { apartments, availableApartments, selectedDevice } = storeToRefs(app)
const loading = ref(true)
const loadError = ref('')
const submitError = ref('')
const successMessage = ref('')
const deletingId = ref<string | null>(null)
const devicePage = ref(1)
const apartmentPage = ref(1)
const devicePerPage = 4
const apartmentPerPage = 4
const visibleDevices = computed(() => selectedDevice.value.slice(
  (devicePage.value - 1) * devicePerPage,
  devicePage.value * devicePerPage,
))
const visibleApartments = computed(() => apartments.value.slice(
  (apartmentPage.value - 1) * apartmentPerPage,
  apartmentPage.value * apartmentPerPage,
))

const backendErrorTranslations: Record<string, string> = {
  'apartment not found': 'ساختمان انتخاب‌شده در سامانه پیدا نشد.',
  'unit number is not acceptable': 'شماره واحد از تعداد واحدهای تعریف‌شده برای این ساختمان بیشتر است.',
  'this block is not available': 'این شماره واحد قبلاً به کاربر دیگری اختصاص داده شده است.',
}

function getSubmitErrorMessage(error: any) {
  if (!error?.response) {
    return 'ارتباط با سرور برقرار نشد. اتصال شبکه و فعال‌بودن بک‌اند را بررسی کنید.'
  }

  const status = Number(error.response.status)
  const detail = error.response.data?.detail

  if (Array.isArray(detail)) {
    const fieldNames: Record<string, string> = {
      apartment_no: 'شماره ساختمان',
      unit: 'شماره واحد',
      area: 'مساحت مفید',
    }
    const issues = detail.map((issue: any) => {
      const field = fieldNames[String(issue?.loc?.at(-1))] || 'اطلاعات فرم'
      const type = String(issue?.type || '')
      if (type.includes('int')) return `${field} باید عدد صحیح باشد.`
      if (type.includes('string')) return `${field} باید به‌صورت مقدار متنی معتبر ارسال شود.`
      if (type.includes('float') || type.includes('number')) return `${field} باید عدد معتبر باشد.`
      if (type.includes('missing')) return `${field} الزامی است.`
      return `${field}: مقدار واردشده معتبر نیست.`
    })
    return `اطلاعات فرم معتبر نیست: ${issues.join(' ')}`
  }

  if (typeof detail === 'string') {
    return backendErrorTranslations[detail] || `خطای سرور: ${detail}`
  }

  if (status === 401) return 'نشست ورود منقضی شده است؛ دوباره وارد حساب شوید.'
  if (status === 403) return 'حساب شما اجازه ثبت ساختمان را ندارد.'
  if (status >= 500) return `سرور هنگام ثبت ساختمان دچار خطای داخلی شد (کد ${status}).`
  return `ثبت ساختمان ناموفق بود (کد پاسخ ${status}).`
}

const schema = toTypedSchema(z.object({
  apartment: z.coerce.number().int('شماره ساختمان باید عدد صحیح باشد').positive('شماره ساختمان الزامی است'),
  area: z.coerce.number().positive('مساحت باید بیشتر از صفر باشد'),
  unit: z.coerce.number().int('شماره واحد باید عدد صحیح باشد').positive('شماره واحد الزامی است'),
}))
const { handleSubmit, isSubmitting, resetForm } = useForm({
  validationSchema: schema,
  initialValues: { apartment: undefined, area: undefined, unit: undefined },
})

async function loadResources() {
  loading.value = true
  loadError.value = ''
  try {
    await Promise.all([
      app.fetchApartment(),
      app.fetchAvailableApartments(),
      app.fetchselectedDevice(),
    ])
  }
  catch {
    loadError.value = 'اطلاعات ساختمان و تجهیزات دریافت نشد. اتصال سرور را بررسی کنید.'
  }
  finally {
    loading.value = false
  }
}

const addBlock = handleSubmit(async (values) => {
  submitError.value = ''
  successMessage.value = ''
  try {
    await app.addBlock(values.apartment, values.area, values.unit)
    successMessage.value = 'مشخصات ساختمان با موفقیت ثبت شد.'
    resetForm()
    await loadResources()
  }
  catch (error) {
    submitError.value = getSubmitErrorMessage(error)
  }
})

async function deleteDevice(device: any) {
  const id = String(device.id || device._id)
  if (!confirm(`تجهیز «${device.name}» از منابع این حساب حذف شود؟`)) return
  deletingId.value = id
  submitError.value = ''
  try {
    await app.deleteDevice(id)
    successMessage.value = 'تجهیز از فهرست منابع حذف شد.'
    await loadResources()
  }
  catch {
    submitError.value = 'حذف تجهیز انجام نشد.'
  }
  finally {
    deletingId.value = null
  }
}

onMounted(loadResources)
</script>

<template>
  <section>
    <header class="mb-6" data-tour="building-resources">
      <BaseHeading as="h1" size="xl">
        ساختمان و منابع انرژی
      </BaseHeading>
      <BaseParagraph class="text-muted-500 mt-2">
        مشخصات واحد و تجهیزات مصرف‌کننده را برای محاسبه دقیق تولید و مصرف مدیریت کنید.
      </BaseParagraph>
    </header>

    <BaseCard v-if="loading" class="p-10 text-center">
      <Icon name="svg-spinners:ring-resize" class="text-primary-500 mx-auto size-8" />
      <p class="mt-3">
        در حال دریافت منابع انرژی…
      </p>
    </BaseCard>
    <BaseMessage v-else-if="loadError" type="danger">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span>{{ loadError }}</span><BaseButton size="sm" @click="loadResources">
          تلاش دوباره
        </BaseButton>
      </div>
    </BaseMessage>
    <template v-else>
      <BaseMessage
        v-if="successMessage"
        type="success"
        class="mb-4"
        @close="successMessage = ''"
      >
        {{ successMessage }}
      </BaseMessage>
      <BaseMessage
        v-if="submitError"
        type="danger"
        class="mb-4"
        @close="submitError = ''"
      >
        {{ submitError }}
      </BaseMessage>

      <div class="grid gap-5 xl:grid-cols-[minmax(0,1fr)_340px]">
        <div data-tour="active-devices">
          <div class="mb-4 flex items-end justify-between gap-3">
            <div>
              <BaseHeading size="md">
                تجهیزات فعال
              </BaseHeading><BaseParagraph class="text-muted-500 mt-1">
                مصرف‌کننده‌های متصل به این حساب
              </BaseParagraph>
            </div>
            <BaseTag color="success" variant="pastel">
              {{ selectedDevice.length }} تجهیز
            </BaseTag>
          </div>
          <BaseCard v-if="!selectedDevice.length" class="p-10 text-center">
            <Icon name="ph:plugs-connected-duotone" class="text-muted-400 mx-auto size-12" />
            <BaseHeading class="mt-3">
              هنوز تجهیزی انتخاب نشده است
            </BaseHeading>
            <BaseParagraph class="text-muted-500 mt-2">
              از صفحه تجهیزات، مصرف‌کننده‌های ساختمان را اضافه کنید.
            </BaseParagraph>
            <BaseButton
              to="/profile/products"
              color="primary"
              class="mt-4"
            >
              انتخاب تجهیزات
            </BaseButton>
          </BaseCard>
          <div v-else class="grid gap-3 sm:grid-cols-2">
            <BaseCard
              v-for="device in visibleDevices"
              :key="device.id || device._id"
              class="border-success-500 border-s-4 p-4"
            >
              <div class="flex items-start justify-between gap-3">
                <div>
                  <BaseHeading size="sm">
                    {{ device.name }}
                  </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
                    مصرف AC: {{ device.AC_power_consumption || 0 }} وات
                  </BaseParagraph><BaseParagraph class="text-muted-500">
                    مصرف DC: {{ device.DC_power_consumption || 0 }} وات
                  </BaseParagraph>
                </div>
                <BaseButtonIcon
                  color="danger"
                  :loading="deletingId === String(device.id || device._id)"
                  aria-label="حذف تجهیز"
                  @click="deleteDevice(device)"
                >
                  <Icon name="ph:trash-duotone" />
                </BaseButtonIcon>
              </div>
            </BaseCard>
          </div>
          <BasePagination
            previous-icon="lucide:chevron-right"
            next-icon="lucide:chevron-left"
            v-if="selectedDevice.length > devicePerPage"
            class="mt-5"
            :total-items="selectedDevice.length"
            :item-per-page="devicePerPage"
            :current-page="devicePage"
            @update:current-page="devicePage = $event"
          />

          <div class="mt-7">
            <BaseHeading size="md">
              واحدهای ثبت‌شده
            </BaseHeading><BaseParagraph class="text-muted-500 mt-1">
              اطلاعات ساختمانی موجود در سامانه
            </BaseParagraph>
          </div>
          <BaseCard v-if="!apartments.length" class="mt-4 p-8 text-center">
            هنوز واحدی ثبت نشده است؛ فرم روبه‌رو را تکمیل کنید.
          </BaseCard>
          <div v-else class="mt-4 space-y-3">
            <BaseCard
              v-for="item in visibleApartments"
              :key="item.id || item._id || item.apartment_no"
              class="p-4"
            >
              <div class="grid gap-3 sm:grid-cols-3">
                <div><small class="text-muted-500">بلوک</small><p>{{ item.unit || item.block_no || '—' }}</p></div><div><small class="text-muted-500">شماره واحد</small><p>{{ item.apartment_no || '—' }}</p></div><div><small class="text-muted-500">مساحت</small><p>{{ item.area || '—' }} مترمربع</p></div>
              </div>
            </BaseCard>
          </div>
          <BasePagination
            previous-icon="lucide:chevron-right"
            next-icon="lucide:chevron-left"
            v-if="apartments.length > apartmentPerPage"
            class="mt-5"
            :total-items="apartments.length"
            :item-per-page="apartmentPerPage"
            :current-page="apartmentPage"
            @update:current-page="apartmentPage = $event"
          />
        </div>

        <BaseCard class="h-fit p-5">
          <BaseHeading size="md">
            ثبت مشخصات ساختمان
          </BaseHeading>
          <BaseParagraph class="text-muted-500 mt-2">
            این داده‌ها مبنای محاسبه ظرفیت خورشیدی هستند.
          </BaseParagraph>
          <form
            class="mt-5 space-y-4"
            novalidate
            @submit.prevent="addBlock"
          >
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="unit">
              <BaseInput
                :model-value="field.value"
                :error="errorMessage"
                type="number"
                min="1"
                label="شماره واحد"
                placeholder="برای نمونه: ۱۲"
                :disabled="isSubmitting"
                @update:model-value="handleChange"
                @blur="handleBlur"
              />
            </Field>
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="apartment">
              <BaseSelect
                :model-value="field.value"
                :error="errorMessage"
                label="شماره ساختمان"
                :disabled="isSubmitting"
                @update:model-value="handleChange"
                @blur="handleBlur"
              >
                <option value="" disabled>
                  یک ساختمان را انتخاب کنید
                </option>
                <option
                  v-for="building in availableApartments"
                  :key="building.id"
                  :value="building.apartment_no"
                >
                  ساختمان {{ building.apartment_no }} (حداکثر {{ building.block_no }} واحد)
                </option>
              </BaseSelect>
            </Field>
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="area">
              <BaseInput
                :model-value="field.value"
                :error="errorMessage"
                type="number"
                min="1"
                label="مساحت مفید (مترمربع)"
                placeholder="برای نمونه: ۹۵"
                :disabled="isSubmitting"
                @update:model-value="handleChange"
                @blur="handleBlur"
              />
            </Field>
            <BaseButton
              type="submit"
              color="primary"
              class="w-full"
              :loading="isSubmitting"
              :disabled="isSubmitting"
            >
              ثبت ساختمان
            </BaseButton>
          </form>
        </BaseCard>
      </div>
    </template>
  </section>
</template>
