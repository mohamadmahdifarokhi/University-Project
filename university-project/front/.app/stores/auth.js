import {defineStore} from 'pinia';
import axios from 'axios';

const apiUrl = `${import.meta.env.VITE_BACKEND_SERVER_URL}`;

export const useAuthStore = defineStore('auth', () => {
  const isAuthenticated = ref(false);
  const isAdmin = ref(false);
  const isMng = ref(false);

  function setAuthenticated(auth) {
    isAuthenticated.value = auth;
  }

  function setIsAdmin(auth) {
    isAdmin.value = auth;
  }

  function setIsMng(auth) {
    isMng.value = auth;
  }

  async function checkAccessToken() {
    if (useCookie('refresh_token')) {

      const refreshToken = useCookie('refresh_token').value;
      console.log(refreshToken)
      try {
        const response = await axios.post(`${apiUrl}/users/refresh`, {}, {
          headers: {
            'Authorization': `Bearer ${refreshToken}`,
          },
        });
        console.log(response.data.scopes, "wqqeqwewqe")
        if (response.status === 200) {
          console.log('qwdqwdqwd')

          document.cookie = `access_token=${response.data.access_token}; domain=localhost; path=/`;
          this.setAuthenticated(true);
            console.log(response.data.scopes)
            console.log("asawdeqwewqd")

          if (response.data.scopes.includes('admin')) {
            this.setIsAdmin(true)

          }
          if (response.data.scopes.includes('manager')) {
            this.setIsMng(true)

          }

          console.log(isAuthenticated,"qweqwew")
        }

      } catch (error) {
        console.log(error)

        if (error.response && error.response.status === 401) {
          this.$reset()
        }
      }
    } else {

      this.$reset()

    }
  }

  async function login({email, password, callBackUrl}) {
    const toaster = useToaster();
    const router = useRouter();
    try {

      const response = await axios.post(
        `${apiUrl}/users`,
        {
          username: email,
          password: password,
        },
        {
          headers: {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      if (response.status === 200) {
        localStorage.setItem('refresh_token', response.data.refresh_token);
        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('email', response.data.email);
        // Set cookies
        document.cookie = `refresh_token=${response.data.refresh_token}; domain=localhost; path=/`;
        document.cookie = `access_token=${response.data.access_token}; domain=localhost; path=/`;
        document.cookie = `email=${response.data.email}; domain=localhost; path=/`;

        this.addToOrderFromSession(response.data.access_token)

        setAuthenticated(true);
        if ('admin' in response.data.scopes) {
          this.setIsAdmin(true)
        }
         if ('manager' in response.data.scopes) {
          this.setIsMng(true)
        }
        if (!callBackUrl.startsWith('http')) {
          router.push(callBackUrl);

        } else {
          window.location.replace(callBackUrl);

        }


        toaster.clearAll();
        toaster.show({
          title: 'Success',
          message: 'Welcome back!',
          color: 'success',
          icon: 'ph:user-circle-fill',
          closable: true,
        });

        return true;
      } else {
        // Other client-side errors
        toaster.show({
          title: 'Error',
          message: 'Failed to login. Please try again later.',
          color: 'danger',
          icon: 'ph:x-circle-fill',
          closable: true,
        });
      }
    } catch (error) {
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        if (error.response.status === 400) {
          // Incorrect credentials
          toaster.show({
            title: 'Error',
            message: 'Incorrect credentials',
            color: 'danger',
            icon: 'ph:x-circle-fill',
            closable: true,
          });
        } else {
          // Other client-side errors
          toaster.show({
            title: 'Error',
            message: 'Failed to login. Please try again later.',
            color: 'danger',
            icon: 'ph:x-circle-fill',
            closable: true,
          });
        }
      } else if (error.request) {
        // The request was made but no response was received
        toaster.show({
          title: 'Error',
          message: 'No response from the server. Please try again later.',
          color: 'error',
          icon: 'ph:x-circle-fill',
          closable: true,
        });
      } else {
        // Something happened in setting up the request that triggered an Error
        toaster.show({
          title: 'Error',
          message: 'An unexpected error occurred. Please try again later.',
          color: 'error',
          icon: 'ph:x-circle-fill',
          closable: true,
        });
      }

      throw error; // rethrow the error after handling
    }
  }


  async function loginWithGoogle(redirect_uri) {
    try {
      let redirect_urii; // Define redirect_urii outside the if-else blocks

      if (!redirect_uri.startsWith('http')) {
        redirect_urii = 'http://localhost:3002' + redirect_uri; // Use let to define the variable
      } else {
        redirect_urii = redirect_uri; // Use let to define the variable
      }

      const response = await axios.get(
        `${apiUrl}/auth/login?redirect_uri=${redirect_urii}`, // Use the defined variable
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      // Redirect to Google OAuth endpoint
      window.location.href = response.data;
    } catch (error) {
      // Handle error
      throw error;
    }
  }


  async function addToOrderFromSession(accessToken) {
    try {
      const cart = localStorage.getItem('cart');

      if (cart) {
        const parsedCart = JSON.parse(cart);
        if (parsedCart.cart_items && Array.isArray(parsedCart.cart_items)) {
          for (const order of parsedCart.cart_items) {
            const orderData = {
              email: order.email,
              password: order.password,
              description: order.description,
              product_id: order.product.id, // Make sure to access the product's ID correctly.
            };

            const response = await axios.post(`${apiUrl}/users/carts/items`, orderData, {
              headers: {
                Authorization: `Bearer ${accessToken}`,
                'Content-Type': 'application/json',
                accept: 'application/json',
              },
            });

          }
          localStorage.removeItem('cart');

        } else {
          console.error('cart_items is missing or not an array in the cart.');
        }
      } else {
        console.log('No cart found in localStorage.');
      }
    } catch (error) {
      console.error('Error adding orders from localStorage:', error);
    }
  }


  async function sendOTP({email, password}) {
    try {
      const response = await axios.post(`${apiUrl}/users/otp`, {
        email,
      });

      if (response.status === 200) {
        const responseData = response.data;
        localStorage.setItem('signupData', JSON.stringify({email, password}));
        return email;
      } else {
        throw new Error('Failed registration');
      }
    } catch (error) {
      throw error;
    }
  }

  async function verifyOTP({otp, callBackUrl}) {
    try {
      const signupData = JSON.parse(localStorage.getItem('signupData'));
      const router = useRouter();

      const response = await axios.post(`${apiUrl}/users/otp/verify`, {
        email: signupData.email,
        password: signupData.password,
        otp_code: otp,
      });

      if (response.status === 200) {
        const authStore = useAuthStore();

        await authStore.login({email: signupData.email, password: signupData.password, callBackUrl: callBackUrl});
      } else {
        throw new Error('Failed OTP verification');
      }
    } catch (error) {
      throw error;
    }
  }

  async function initiatePasswordRecovery(success, email) {
    try {

      const response = await axios.post(`${apiUrl}/users/recover/`, {email: email}, {
        headers: {
          'Content-Type': 'application/json',
          accept: 'application/json',
        },
      });

      success.value = true;

    } catch (error) {
    }
  }

  async function verifyToken(isTokenValid, token) {
    try {
      const response = await axios.post(
        `${apiUrl}/users/recover/verify?token=${token}`,
        {},
        {
          headers: {
            'Content-Type': 'application/json',
          },
        }
      );

      if (response.data) {
        isTokenValid.value = true;
      } else {
        isTokenValid.value = false;
      }
    } catch (error) {
    }
  }

  async function changePasswordWithToken({token, newPassword}) {
    const toaster = useToaster();

    try {
      const response = await axios.post(`${apiUrl}/users/recover/password?token=${token}&password=${newPassword}`, {}, {
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 200) {
        toaster.clearAll();
        toaster.show({
          title: 'Success',
          message: 'Your profile has been updated!',
          color: 'success',
          icon: 'ph:check',
          closable: true,
        });
      } else {
        throw new Error('Failed password change');
      }
    } catch (error) {
      throw error;
    }
  }

  async function changePassword({currentPassword, newPassword}) {
    const toaster = useToaster();
    const accessToken = localStorage.getItem('access_token');

    try {
      const response = await axios.post(`${apiUrl}/users/password?password=${currentPassword}&new_password=${newPassword}`, {}, {
        headers: {
          'Authorization': `Bearer ${accessToken}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.status === 200) {
        toaster.clearAll();
        toaster.show({
          title: 'Success',
          message: 'Your profile has been updated!',
          color: 'success',
          icon: 'ph:check',
          closable: true,
        });
      } else {
        throw new Error('Failed password change');
      }
    } catch (error) {
      throw error;
    }
  }

  function deleteCookie(name) {
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; domain=localhost; path=/`;
  }

  function $reset() {
    deleteCookie('refresh_token');
    deleteCookie('access_token');
    deleteCookie('email');
    isAuthenticated.value = false;
    isAdmin.value = false;
    isMng.value = false;
  }

  return {
    isAuthenticated,
    isAdmin,
    isMng,
    setAuthenticated,
    setIsAdmin,
    setIsMng,
    checkAccessToken,
    login,
    loginWithGoogle,
    addToOrderFromSession,
    sendOTP,
    verifyOTP,
    initiatePasswordRecovery,
    verifyToken,
    changePasswordWithToken,
    changePassword,
    $reset,
  };
}, {
  persist: {
    storage: persistedState.cookiesWithOptions({
      sameSite: 'strict',
    }),
  },
});
