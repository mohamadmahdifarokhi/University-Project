export default defineEventHandler(async (event) => {
  const query = getQuery(event)
  const perPage = parseInt((query.perPage as string) || '5', 10)
  const page = parseInt((query.page as string) || '1', 10)
  const filter = (query.filter as string) || ''

  if (perPage >= 50) {
    // Create an artificial delay
    await new Promise(resolve => setTimeout(resolve, 1000))
  }

  const data = await getDemoData()
  const offset = (page - 1) * perPage
  const filterRe = new RegExp(filter, 'i')

  return {
    total: data.length,
    data: !filter
      ? data.slice(offset, offset + perPage)
      : data
        .filter((item) => {
          return [item.name, item.category].some(item => item.match(filterRe))
        })
        .slice(offset, offset + perPage),
  }
})

async function getDemoData() {
  return Promise.resolve([
    {
      id: 0,
      name: 'Introduction to Html5',
      picture: '/img/illustrations/layouts/course-1.jpg',
      category: 'Web Development',
      difficulty: 1,
      price: 26,
      skill: {
        icon: 'uiw:html5',
        name: 'Html5',
      },
      author: {
        id: 8,
        picture: '/images/avatars/svg/vuero-1.svg',
        username: 'Erik K.',
        initials: 'EK',
        color: 'info',
      },
    },
    {
      id: 1,
      name: 'Mastering VueJS and Typescript',
      picture: '/img/illustrations/layouts/course-2.png',
      category: 'Web Development',
      difficulty: 4,
      price: 12,
      skill: {
        icon: 'teenyicons:vue-solid',
        name: 'Vue',
      },
      author: {
        id: 12,
        picture: '/img/avatars/12.jpg',
        username: 'Joshua S.',
        initials: 'JS',
        color: 'info',
      },
    },
    {
      id: 2,
      name: 'Discovering CSS3 and Stylesheets',
      picture: '/img/illustrations/layouts/course-3.jpg',
      category: 'Web Development',
      difficulty: 2,
      price: 16,
      skill: {
        icon: 'simple-icons:css3',
        name: 'CSS3',
      },
      author: {
        id: 12,
        picture: '/img/avatars/5.jpg',
        username: 'Mary L.',
        initials: 'ML',
        color: 'info',
      },
    },
  ])
}
