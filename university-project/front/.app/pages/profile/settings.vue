<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import { Field, useForm } from 'vee-validate'
import { z } from 'zod'
import { useAuthStore } from '~/stores/auth'

definePageMeta({ title: 'امنیت حساب', middleware: 'authenticated' })
const schema = toTypedSchema(z.object({
  currentPassword: z.string().min(1, 'رمز عبور فعلی الزامی است'),
  newPassword: z.string().min(8, 'رمز جدید باید حداقل ۸ نویسه باشد'),
  confirmPassword: z.string(),
}).refine(v => v.newPassword === v.confirmPassword, { message: 'تکرار رمز عبور مطابقت ندارد', path: ['confirmPassword'] }))
const { handleSubmit, isSubmitting, resetForm, setFieldError } = useForm({ validationSchema: schema, initialValues: { currentPassword: '', newPassword: '', confirmPassword: '' } })
const auth = useAuthStore()
const success = ref(false)
const errorMessage = ref('')
const onSubmit = handleSubmit(async (values) => {
  success.value = false
  errorMessage.value = ''
  try {
    await auth.changePassword({ currentPassword: values.currentPassword, newPassword: values.newPassword })
    success.value = true
    resetForm()
  }
  catch (error: any) {
    if (error?.response?.status === 400 || error?.response?.status === 401) {
      setFieldError('currentPassword', 'رمز عبور فعلی صحیح نیست')
    }
    errorMessage.value = error?.response?.data?.detail || 'تغییر رمز عبور انجام نشد. دوباره تلاش کنید.'
  }
})
</script>
<template>
  <form
    class="pb-16"
    novalidate
    @submit.prevent="onSubmit"
  >
    <BaseCard class="overflow-hidden">
      <div class="border-muted-200 dark:border-muted-700 border-b p-5">
        <BaseHeading as="h1" size="xl">
          امنیت حساب
        </BaseHeading><BaseParagraph class="text-muted-500 mt-2">
          برای محافظت از حساب، یک رمز قوی و منحصربه‌فرد انتخاب کنید.
        </BaseParagraph>
      </div><div class="mx-auto max-w-xl space-y-5 p-6">
        <BaseMessage
          v-if="success"
          type="success"
          @close="success=false"
        >
          رمز عبور با موفقیت تغییر کرد.
        </BaseMessage><BaseMessage
          v-if="errorMessage"
          type="danger"
          @close="errorMessage=''"
        >
          {{ errorMessage }}
        </BaseMessage><Field v-slot="{field,errorMessage:fieldError,handleChange,handleBlur}" name="currentPassword">
          <BaseInput
            :model-value="field.value"
            :error="fieldError"
            type="password"
            label="رمز عبور فعلی"
            autocomplete="current-password"
            :disabled="isSubmitting"
            @update:model-value="handleChange"
            @blur="handleBlur"
          />
        </Field><Field v-slot="{field,errorMessage:fieldError,handleChange,handleBlur}" name="newPassword">
          <BaseInput
            :model-value="field.value"
            :error="fieldError"
            type="password"
            label="رمز عبور جدید"
            autocomplete="new-password"
            :disabled="isSubmitting"
            @update:model-value="handleChange"
            @blur="handleBlur"
          />
        </Field><Field v-slot="{field,errorMessage:fieldError,handleChange,handleBlur}" name="confirmPassword">
          <BaseInput
            :model-value="field.value"
            :error="fieldError"
            type="password"
            label="تکرار رمز عبور جدید"
            autocomplete="new-password"
            :disabled="isSubmitting"
            @update:model-value="handleChange"
            @blur="handleBlur"
          />
        </Field><div class="flex justify-end gap-2">
          <BaseButton type="button" @click="resetForm()">
            پاک‌کردن
          </BaseButton><BaseButton
            type="submit"
            color="primary"
            :loading="isSubmitting"
            :disabled="isSubmitting"
          >
            ذخیره رمز جدید
          </BaseButton>
        </div>
      </div>
    </BaseCard>
  </form>
</template>
