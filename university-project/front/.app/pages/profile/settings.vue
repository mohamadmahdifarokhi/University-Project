<script setup lang="ts">
import { toTypedSchema } from '@vee-validate/zod'
import IMask from 'imask'
import { Field, useForm } from 'vee-validate'
import { z } from 'zod'
import { useAuthStore } from '~/stores/auth'


const localPath = useLocalePath();


// Validation error messages
const VALIDATION_TEXT = {
  OLD_PASSWORD_REQUIRED: 'Your current password is required',
  NEW_PASSWORD_LENGTH: 'Password must be at least 8 characters',
  NEW_PASSWORD_MATCH: 'Passwords do not match',
}

definePageMeta({
  title: 'Settings',
  middleware: 'authenticated',
  preview: {
    title: 'Edit profile 4',
    description: 'For editing a user profile',
    categories: ['layouts', 'profile', 'forms'],
    src: '/img/screens/layouts-subpages-profile-4.png',
    srcDark: '/img/screens/layouts-subpages-profile-4-dark.png',
    order: 79,
  },
})

// Define the Zod schema for form input
const zodSchema = z.object({
  currentPassword: z.string().min(1, VALIDATION_TEXT.OLD_PASSWORD_REQUIRED),
  newPassword: z.string(),
  confirmPassword: z.string(),
})

// Define TypeScript type based on Zod schema
type FormInput = z.infer<typeof zodSchema>

const { data, pending, error, refresh } = await useFetch('/api/profile')

// Convert Zod schema to VeeValidate schema
const validationSchema = toTypedSchema(zodSchema)
const { locale, locales } = useI18n()

const {t} = useI18n({useScope:"local"})
// Initial form values
const initialValues = computed<FormInput>(() => ({
  currentPassword: 'password',
  newPassword: '',
  confirmPassword: '',
}))

// Form handling using VeeValidate
const {
  handleSubmit,
  isSubmitting,
  setFieldError,
  meta,
  values,
  errors,
  resetForm,
  setFieldValue,
  setErrors,
} = useForm({
  validationSchema,
  initialValues,
})

const success = ref(false)

// Compute the number of fields with errors
const fieldsWithErrors = computed(() => Object.keys(errors.value).length)

// Cleanup IMask on component unmount
const mask = shallowRef<IMask.InputMask<{ mask: string }> | undefined>(undefined)
onBeforeUnmount(() => {
  mask.value?.destroy()
  mask.value = undefined
})

// Ask for confirmation before leaving the page with unsaved changes
onBeforeRouteLeave(() => {
  if (meta.value.dirty) {
    return confirm('You have unsaved changes. Are you sure you want to leave?')
  }
})

const toaster = useToaster()
const auth = useAuthStore()

// Handle form submission
const onSubmit = handleSubmit(
  async (values) => {
    success.value = false
    const currentPassword = values.currentPassword
    const newPassword = values.newPassword

    try {
      // Call a function to change the user's password (assuming it's implemented in the auth store)
      auth.changePassword({ currentPassword, newPassword })

      // Simulated delay for the backend validation
      await new Promise((resolve, reject) => {
        if (values.currentPassword === 'password') {
          // Simulate a backend error
          setTimeout(() => reject(new Error('Fake backend validation error')), 2000)
        }
        setTimeout(resolve, 4000)
      })

      // Show a success message
      toaster.clearAll()
      toaster.show({
        title: 'Success',
        message: 'Your profile has been updated!',
        color: 'success',
        icon: 'ph:check',
        closable: true,
      })
    } catch (error: any) {
      if (error.message === 'Fake backend validation error') {
        // Set an error for the current password field
        setFieldError('currentPassword', 'Your current password is incorrect')

        // Scroll to the top of the page
        document.documentElement.scrollTo({
          top: 0,
          behavior: 'smooth',
        })

        // Show an error message
        toaster.clearAll()
        toaster.show({
          title: 'Oops!',
          message: 'Please review-inactive the errors in the form',
          color: 'danger',
          icon: 'lucide:alert-triangle',
          closable: true,
        })
      }
      return
    }

    resetForm()

    // Scroll to the top of the page
    document.documentElement.scrollTo({
      top: 0,
      behavior: 'smooth',
    })

    success.value = true
    setTimeout(() => {
      success.value = false
    }, 3000)
  },
  (error) => {
    success.value = false
    document.documentElement.scrollTo({
      top: 0,
      behavior: 'smooth',
    })
  },
)
</script>

<template>
  <form method="POST" action="" class="w-full pb-16" @submit.prevent="onSubmit">
    <BaseCard>
      <div class="flex items-center justify-between p-4">
        <div>
          <BaseHeading
            tag="h2"
            size="sm"
            weight="medium"
            lead="normal"
            class="uppercase tracking-wider"
          >
            {{ t("Settings") }}
          </BaseHeading>
<!--          <BaseText size="xs" class="text-muted-400">-->
<!--            Edit your account prefs and settings-->
<!--          </BaseText>-->
        </div>
        <div class="flex items-center gap-2">
          <BaseButton class="w-24" :to="localPath('/profile/orders')">{{ t("Cancel") }}</BaseButton>
          <BaseButton
            type="submit"
            color="primary"
            class="w-24"
            :disabled="isSubmitting"
            :loading="isSubmitting"
          >
            {{ t("Save") }}
          </BaseButton>
        </div>
      </div>
      <div class="p-4">
        <div class="mx-auto max-w-lg space-y-12 py-8">
          <BaseMessage v-if="success" @close="success = false">
            Your settings have been saved!
          </BaseMessage>
          <BaseMessage
            v-if="fieldsWithErrors"
            type="danger"
            @close="() => setErrors({})"
          >
            This form has {{ fieldsWithErrors }} errors, please check them before submitting
          </BaseMessage>

          <TairoFormGroup
            :label="t('Change')"
<!--            sublabel="For improved account security"-->
          >
            <div class="grid grid-cols-12 gap-4">
              <div class="col-span-12">
                <Field
                  v-slot="{ field, errorMessage, handleChange, handleBlur }"
                  name="currentPassword"
                >
                  <BaseInput
                    :model-value="field.value"
                    :error="errorMessage"
                    :disabled="isSubmitting"
                    type="password"
                    icon="ph:lock-duotone"
                    :placeholder="t('OPassowrd')"
                    autocomplete="current-password"
                    @update:model-value="handleChange"
                    @blur="handleBlur"
                  />
                </Field>
              </div>
              <div class="col-span-12">
                <Field
                  v-slot="{ field, errorMessage, handleChange, handleBlur }"
                  name="newPassword"
                >
                  <BaseInput
                    :model-value="field.value"
                    :error="errorMessage"
                    :disabled="isSubmitting"
                    type="password"
                    icon="ph:lock-duotone"
                    :placeholder="t('NPassowrd')"
                    autocomplete="new-password"
                    @update:model-value="handleChange"
                    @blur="handleBlur"
                  />
                </Field>
              </div>
              <div class="col-span-12">
                <Field
                  v-slot="{ field, errorMessage, handleChange, handleBlur }"
                  name="confirmPassword"
                >
                  <BaseInput
                    :model-value="field.value"
                    :error="errorMessage"
                    :disabled="isSubmitting"
                    type="password"
                    icon="ph:lock-duotone"
                    :placeholder="t('RNPassowrd')"
                    @update:model-value="handleChange"
                    @blur="handleBlur"
                  />
                </Field>
              </div>
            </div>
          </TairoFormGroup>
          <!-- Commented out sections for 2 Factor Auth and Notifications -->
        </div>
      </div>
    </BaseCard>
    <TairoFormSave
      :disabled="isSubmitting"
      :loading="isSubmitting"
      @reset="resetForm"
    />
  </form>
</template>
