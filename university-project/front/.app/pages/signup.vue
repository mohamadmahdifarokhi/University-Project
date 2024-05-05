<script setup lang="ts">
import {toTypedSchema} from '@vee-validate/zod';
import {Field, useForm} from 'vee-validate';
import {z} from 'zod';
import {ref, computed} from 'vue';
import {useAuthStore} from "@/stores/auth";
import {useAppStore} from "~/stores/app";

const app = useAppStore();
const {t} = useI18n({useScope: "local"})

const apiUrl = `${import.meta.env.VITE_FRONTEND_SERVER_URL}`;

const authStore = useAuthStore();
const router = useRouter();

definePageMeta({
  layout: 'empty',
  title: 'Signup',
  middleware: ['no-authenticated', 'redirect'],
  preview: {
    title: 'Signup 1',
    description: 'For authentication and sign up',
    categories: ['layouts', 'authentication'],
    src: '/img/screens/auth-signup-1.png',
    srcDark: '/img/screens/auth-signup-1-dark.png',
    order: 100,
  },
});
const {locale, locales} = useI18n()

const VALIDATION_TEXT = {
  EMAIL_REQUIRED: 'A valid email is required',
  PASSWORD_LENGTH: 'Password must be at least 8 characters',
  PASSWORD_CONTAINS_EMAIL: 'Password cannot contain your email',
  PASSWORD_MATCH: 'Passwords do not match',
};

const zodSchema = z
  .object({
    email: z.string().email(VALIDATION_TEXT.EMAIL_REQUIRED),
    password: z.string().min(8, VALIDATION_TEXT.PASSWORD_LENGTH),
    confirmPassword: z.string(),
    otp: z.string(),
  })
  .superRefine((data, ctx) => {
    if (data.password.includes(data.email)) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: VALIDATION_TEXT.PASSWORD_CONTAINS_EMAIL,
        path: ['password'],
      });
    }
    if (data.password !== data.confirmPassword) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: VALIDATION_TEXT.PASSWORD_MATCH,
        path: ['confirmPassword'],
      });
    }
  });

type FormInput = z.infer<typeof zodSchema>;

const validationSchema = toTypedSchema(zodSchema);
const initialValues = computed<FormInput>(() => ({
  email: '',
  password: '',
  confirmPassword: '',
  otp: '',
}));

const {handleSubmit, isSubmitting, setFieldError} = useForm({
  validationSchema,
  initialValues,
});

const toaster = useToaster();


const isFormSubmitted = ref(false);

const onSubmit = handleSubmit(async (values) => {
  const send_OTP = await authStore.sendOTP({email: values.email, password: values.password});

  if (send_OTP) {
    isFormSubmitted.value = true;
  }
});
const loginWithGoogle = async () => {
  const route = useRoute();

  const redirect_uri = route.query.callBackUrl || '/dashboard';

  await authStore.loginWithGoogle(redirect_uri);
}
const submitOTP = handleSubmit(async (values) => {
  const route = useRoute();

  const callBackUrl = route.query.callBackUrl || '/dashboard';
  await authStore.verifyOTP({otp: +values.otp, callBackUrl: callBackUrl});
});
</script>

<template>
  <video autoplay muted loop class="absolute inset-0 z-0 object-cover w-full h-full">
    <source src="/auth.mp4" type="video/mp4">
    <!-- Add additional <source> elements for other video formats -->
    Your browser does not support the video tag.
  </video>
  <div class="h-screen md:flex dark:bg-muted-900">

    <div
      class="i group relative hidden w-1/2 items-center justify-around overflow-hidden bg-gradient-to-tr md:flex">
      <div class="mx-auto max-w-xs text-center">
        <img
          class="grayscale-100 dark:invert mb-10"
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

        <BaseHeading as="h2" size="3xl" weight="medium" class="text-white mb-3">
          {{ t('Have') }}
        </BaseHeading>
        <BaseButton :to="`${apiUrl}/login`" shape="curved" class="w-full">{{ t('Login') }}</BaseButton>
      </div>
    </div>


    <div class="dark:bg-muted-900 flex flex-col items-center justify-between bg-white py-10 md:w-1/2">
      <div class="mx-auto flex w-full max-w-xs items-center justify-between">
        <NuxtLink to="/"
                  class="text-muted-400 hover:text-primary-500 dark:text-muted-700 dark:hover:text-primary-500 transition-colors duration-300">
          <span class="text-muted-800 items-center">Personal Dashboard</span>

        </NuxtLink>
        <div>
          <BaseThemeToggle/>
        </div>
      </div>

      <form method="POST" action="" @submit.prevent="onSubmit" class="mx-auto w-full max-w-xs" novalidate
            :class="{ 'hidden': isFormSubmitted }">
        <BaseHeading as="h2" size="3xl" weight="medium">
          <NuxtLink
            to="/"
            aria-label="Go to homepage"
          >
            <!--          <TairoLogoText-->
            <!--            class="text-primary-500 group-[&.scrolled]/landing:h-6 group-[&:not(.scrolled)]/landing:h-7 motion-safe:transition-all motion-safe:duration-200"-->
            <!--          />-->
            <span class="text-muted-800 items-center">Personal Dashboard</span>


          </NuxtLink>

        </BaseHeading>
        <BaseParagraph size="sm" class="text-muted-400 mb-6">
          {{ t('Lets') }}
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
          <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="confirmPassword">
            <BaseInput
              :model-value="field.value"
              :error="errorMessage"
              :disabled="isSubmitting"
              type="password"
              shape="curved"
              :placeholder="t('Confirm')"
              icon="ph:check"
              @update:model-value="handleChange"
              @blur="handleBlur"
            />
          </Field>
          <BaseButton :disabled="isSubmitting" :loading="isSubmitting" type="submit" shape="curved" color="primary"
                      class="!h-11 w-full">{{ t('Confirmation') }}
          </BaseButton>

<!--          <BaseButton @click="loginWithGoogle" shape="curved" color="primary" class="!h-11 w-full mt-4">-->
<!--          <span class="flex items-center justify-center">-->
<!--          <Icon name="ri:google-fill" class="size-5"/>-->

<!--            &lt;!&ndash;            <img class="w-7 h-5" src="/img/google.png"/>&ndash;&gt;-->
<!--            &lt;!&ndash;            <svg class="w-5 h-5 mr-2" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">&ndash;&gt;-->
<!--            &lt;!&ndash;              <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4 13h-4v4h-2v-4H8v-2h4V9h2v4h4v2z"/>&ndash;&gt;-->
<!--            &lt;!&ndash;            </svg>&ndash;&gt;-->
<!--            &lt;!&ndash;            {{ t('Login with Google') }}&ndash;&gt;-->
<!--          </span>-->
<!--          </BaseButton>-->

        </div>

        <p class="text-muted-400 mt-4 flex justify-between font-sans text-sm leading-5">
          <span>{{ t('Have') }}</span>
          <NuxtLink :to="`${apiUrl}/login`"
                    class="text-primary-600 hover:text-primary-500 font-medium underline-offset-4 transition duration-150 ease-in-out hover:underline focus:underline focus:outline-none">
            {{ t('Login2') }}
          </NuxtLink>
        </p>
      </form>

      <form method="POST" action="" @submit.prevent="submitOTP" class="mx-auto w-full max-w-xs" novalidate
            :class="{ 'hidden': !isFormSubmitted }">
        <div class="mb-4 space-y-3">
          <Field v-slot="{ field, errorMessage, handleChange, handleBlur }" name="otp">
            <BaseInput
              :model-value="field.value"
              :error="errorMessage"
              :disabled="isSubmitting"
              type="text"
              shape="curved"
              :placeholder="t('OTP')"
              icon="ph:key-duotone"
              @update:model-value="handleChange"
              @blur="handleBlur"
            />
          </Field>
          <BaseButton :disabled="isSubmitting" :loading="isSubmitting" type="submit" shape="curved" color="primary"
                      class="!h-11 w-full">{{ t('Confirmation') }}
          </BaseButton>
        </div>
      </form>

      <div class="text-center">
        <BaseText size="sm" class="text-muted-400">
          © {{ new Date().getFullYear() }} Accountract
        </BaseText>
      </div>
    </div>


  </div>
</template>
