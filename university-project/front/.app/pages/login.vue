<script setup lang="ts">
import {toTypedSchema} from '@vee-validate/zod'
import {Field, useForm} from 'vee-validate'
import {z} from 'zod'
import {useAuthStore} from "@/stores/auth"


import {useAppStore} from "~/stores/app";
const {t} = useI18n({useScope: "local"})

const apiUrl = `${import.meta.env.VITE_FRONTEND_SERVER_URL}`;

const app = useAppStore();


const loginWithGoogle = async () => {
  const route = useRoute();
  const redirect_uri = route.query.callBackUrl || '/';
  await authStore.loginWithGoogle(redirect_uri);
}

const initializeData = async () => {
  await loadTextDirection();
};

initializeData();
const authStore = useAuthStore()
const router = useRouter()


definePageMeta({
  layout: 'empty',
  title: 'Login',
  middleware: ['no-authenticated', 'redirect'],
  preview: {
    title: 'Login 2',
    description: 'For authentication and sign in',
    categories: ['layouts', 'authentication'],
    src: '/img/screens/auth-login-2.png',
    srcDark: '/img/screens/auth-login-2-dark.png',
    order: 97,
  },
})


const VALIDATION_TEXT = {
  EMAIL_REQUIRED: t('emailRequired'), // Translate email required text
  PASSWORD_REQUIRED: t('passwordRequired'), // Translate password required text
}

const zodSchema = z.object({
  email: z.string().email(VALIDATION_TEXT.EMAIL_REQUIRED),
  password: z.string().min(1, VALIDATION_TEXT.PASSWORD_REQUIRED),
  trustDevice: z.boolean(),
})

type FormInput = z.infer<typeof zodSchema>

const validationSchema = toTypedSchema(zodSchema)
const initialValues = computed<FormInput>(() => ({
  email: '',
  password: '',
  trustDevice: false,
}))

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


const onSubmit = handleSubmit(async (values) => {
  const route = useRoute();
  const callBackUrl = route.query.callBackUrl || '/';


  await authStore.login({email: values.email, password: values.password, callBackUrl: callBackUrl});
})

</script>

<template>
  <video autoplay muted loop class="absolute inset-0 z-0 object-cover w-full h-full">
    <source src="/auth.mp4" type="video/mp4">
    <!-- Add additional <source> elements for other video formats -->
    Your browser does not support the video tag.
  </video>
  <div class="h-screen md:flex dark:bg-muted-900">


    <div class="relative hidden w-1/2 items-center justify-around overflow-hidden bg-gradient-to-tr md:flex">
      <div class="mx-auto max-w-xs text-center">
        <img
          class="grayscale-100 dark:invert mb-20"
          src="/logo.png"
        >
         <div class="text-start mb-20">
          <BaseHeading as="h2" size="3xl" weight="medium" class="text-white">
          MICRO GRID ENERGEY
        </BaseHeading>
        <BaseHeading as="h2" size="3xl" weight="medium" class="text-white">
          MANAGEMENT
        </BaseHeading>
        <BaseHeading as="h2" size="3xl" weight="medium" class="text-white">
          SYSTEM
        </BaseHeading>
        </div>
        <BaseHeading as="h2" size="3xl" weight="medium" class="relative text-white mb-3">
          {{ t('Dont') }}
        </BaseHeading>
        <BaseButton  :to="`${apiUrl}/signup`" shape="curved">{{ t('Signup') }}</BaseButton>
      </div>
    </div>

    <div class="dark:bg-muted-900 flex flex-col items-center justify-between bg-white py-10 md:w-1/2">
      <div class="mx-auto flex w-full max-w-xs items-center justify-between">
        <NuxtLink to="/"
                  class="text-muted-400 hover:text-primary-500 dark:text-muted-700 dark:hover:text-primary-500 transition-colors duration-300">
          <AccountractLogo class="h-10 w-10"/>
        </NuxtLink>
        <div>
          <BaseThemeToggle/>
        </div>
      </div>

      <form method="POST" action="" @submit.prevent="onSubmit" class="mx-auto w-full max-w-xs" novalidate>
        <BaseHeading as="h2" size="3xl" weight="medium">
          <NuxtLink
            to="/"
            aria-label="Go to homepage"
          >
            <span class="text-muted-800 dark:text-white items-center">DC Micro-grid Planner</span>
          </NuxtLink>
        </BaseHeading>
        <BaseParagraph size="sm" class="text-muted-400 mb-6">
          {{ t('Welcome') }}
        </BaseParagraph>

        <div class="mb-4 space-y-3">
          <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="email">
            <BaseInput
              :model-value="field.value"
              :error="errorMessage"
              :disabled="isSubmitting"
              type="email"
              shape="curved"
              :placeholder="t('Email')"
              icon="ph:at-duotone"
              @update:model-value="handleChange"
              @blur="handleBlur"
            />
          </Field>
          <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="password">
            <BaseInput
              :model-value="field.value"
              :error="errorMessage"
              :disabled="isSubmitting"
              type="password"
              shape="curved"
              :placeholder="t('Password')"
              icon="ph:lock-duotone"
              @update:model-value="handleChange"
              @blur="handleBlur"
            />
          </Field>
        </div>

        <BaseButton :disabled="isSubmitting" :loading="isSubmitting" type="submit" shape="curved" color="primary"
                    class="!h-11 w-full">{{ t('Login') }}
        </BaseButton>

        <!-- Button for Google provider -->
<!--        <BaseButton @click="loginWithGoogle" shape="curved" color="primary" class="!h-11 w-full mt-4">-->
<!--          <span class="flex items-center justify-center">-->
<!--          <Icon name="ri:google-fill" class="size-5"/>-->

<!--            &lt;!&ndash;            <img class="w-7 h-5" src="/img/google.png"/>&ndash;&gt;-->
<!--            &lt;!&ndash;            <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">&ndash;&gt;-->
<!--            &lt;!&ndash;              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4 13h-4v4h-2v-4H8v-2h4V9h2v4h4v2z"/>&ndash;&gt;-->
<!--            &lt;!&ndash;            </svg>&ndash;&gt;-->
<!--            &lt;!&ndash;            {{ t('Login with Google') }}&ndash;&gt;-->
<!--          </span>-->
<!--        </BaseButton>-->

        <p class="text-muted-400 mt-4 flex justify-between font-sans text-sm leading-5">
          <span>{{ t('Dont') }}</span>
          <NuxtLink :to="`${apiUrl}/signup`"
                    class="text-primary-600 hover:text-primary-500 font-medium underline-offset-4 transition duration-150 ease-in-out hover:underline focus:underline focus:outline-none">
            {{ t('Signup') }}
          </NuxtLink>
        </p>
      </form>

      <div class="text-center">
        <BaseText size="sm" class="text-muted-400">© {{ new Date().getFullYear() }} Uuniversity Project</BaseText>
      </div>
    </div>
  </div>
</template>
