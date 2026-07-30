export default defineAppConfig({
  nuxtIcon: {},
  tairo: {
    title: 'دانشگاه آزاد اسلامی واحد پردیس',
    sidebar: {
      toolbar: {
        showNavBurger: true,
        tools: [
          {
            component: 'DemoThemeToggle',
            props: {
              disableTransitions: true,
            },
          },
          {
            component: 'DemoToolbarAccountMenu',
          },
        ],
      },
      circularMenu: {
        enabled: true,
        tools: [
          {
            component: 'DemoThemeToggle',
            props: {
              class: 'ms-auto',
              disableTransitions: true,
              inverted: true,
            },
          },
        ],
      },
      navigation: {
        items: [
          {
            title: 'دانشگاه آزاد اسلامی واحد پردیس',
            icon: { name: 'ph:sidebar-duotone', class: 'w-5 h-5' },
            subsidebar: { component: 'DemoSubsidebarDashboards' },
            activePath: '/',
          },
        ],
      },
    },
  },
})
