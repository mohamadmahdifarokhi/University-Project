<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { Field, useForm } from 'vee-validate'
import { z } from 'zod'
import { storeToRefs } from 'pinia'
import { useAppStore } from '~/stores/app'

definePageMeta({ title: 'ساختمان و منابع انرژی', middleware: 'authenticated' })
useSeoMeta({ description: 'مدیریت مشخصات ساختمان و تجهیزات مصرف‌کننده انرژی' })

const app = useAppStore()
const { apartments, selectedDevice } = storeToRefs(app)
const loading = ref(true)
const loadError = ref('')
const submitError = ref('')
const successMessage = ref('')
const deletingId = ref<string | null>(null)

const schema = toTypedSchema(z.object({
  apartment: z.coerce.number().int('شماره واحد باید عدد صحیح باشد').positive('شماره واحد الزامی است'),
  area: z.coerce.number().positive('مساحت باید بیشتر از صفر باشد'),
  unit: z.string().min(1, 'نام یا شماره بلوک الزامی است'),
}))
const { handleSubmit, isSubmitting, resetForm } = useForm({
  validationSchema: schema,
  initialValues: { apartment: undefined, area: undefined, unit: '' },
})

async function loadResources() {
  loading.value = true
  loadError.value = ''
  try {
    await Promise.all([app.fetchApartment(), app.fetchselectedDevice()])
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
  catch {
    submitError.value = 'ثبت ساختمان انجام نشد. اطلاعات را بررسی و دوباره تلاش کنید.'
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
    <header class="mb-6">
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
        <div>
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
              v-for="device in selectedDevice"
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
              v-for="item in apartments"
              :key="item.id || item._id || item.apartment_no"
              class="p-4"
            >
              <div class="grid gap-3 sm:grid-cols-3">
                <div><small class="text-muted-500">بلوک</small><p>{{ item.unit || item.block_no || '—' }}</p></div><div><small class="text-muted-500">شماره واحد</small><p>{{ item.apartment_no || '—' }}</p></div><div><small class="text-muted-500">مساحت</small><p>{{ item.area || '—' }} مترمربع</p></div>
              </div>
            </BaseCard>
          </div>
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
                label="نام یا شماره بلوک"
                placeholder="برای نمونه: بلوک A"
                :disabled="isSubmitting"
                @update:model-value="handleChange"
                @blur="handleBlur"
              />
            </Field>
            <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="apartment">
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
