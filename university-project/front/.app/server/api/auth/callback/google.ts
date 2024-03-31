import axios from 'axios';

const apiUrl = `${import.meta.env.VITE_BACKEND_SERVER_URL}`;

export default defineEventHandler(async (event) => {
  try {
    const query = getQuery(event);
    const {code, scope, authuser, prompt, state} = query;
    const response = await axios.get(
      `${apiUrl}/auth/callback?code=${code}&scope=${scope}&authuser=${authuser}&prompt=${prompt}`,
      {code, scope, authuser, prompt},
      {
        headers: {
          'Content-Type': 'application/json',
        },
      }
    );

    // Handle successful response
    if (response.status === 200) {
      const responseData = response.data;

      // Store tokens and user information in localStorage
      // localStorage.setItem('refresh_token', responseData.refresh_token);
      // localStorage.setItem('access_token', responseData.access_token);
      // localStorage.setItem('email', responseData.email);
      await setCookie(event, 'refresh_token', responseData.refresh_token)
      await setCookie(event, 'access_token', responseData.access_token)
      await setCookie(event, 'email', responseData.email)

      // Set cookies
      // document.cookie = `refresh_token=${responseData.refresh_token}; domain=localhost`;
      // document.cookie = `access_token=${responseData.access_token}; domain=localhost`;
      // document.cookie = `email=${responseData.email}; domain=localhost`;

      // Perform any additional necessary actions
      // e.g., call addToOrderFromSession or any other function
      await sendRedirect(event, state)
      // await navigateTo(state, {
      //   external: true
      // })

      // setAuthenticated(true);
      // navigateTo('/')
      // Redirect or perform any other action after successful login
      // ...


    }
  } catch (error) {
    // Handle error case
    console.error('Google authentication failed:', error);
    // Throw error or handle it accordingly
  }
});
