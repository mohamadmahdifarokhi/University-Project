import {defineStore} from 'pinia';
import axios from 'axios';


const apiUrl = `${import.meta.env.VITE_BACKEND_SERVER_URL}`;


export const useAppStore = defineStore('app', {
  state: () => ({
    activeGenre: 1,
    categories: [],
    products: [],
    not_active_products: [],
    product: ref(),
    devices: [],
    records: [],
    allUsers: [],
    cal8: {},
    area: ref(''),
    apartment_no: ref(''),
    peakHour: ref(''),
    peakPower: ref(''),
    categories24: ref([]),
    values24: ref([]),
    categoriesMonth: ref([]),
    valuesMonth: ref([]),
    battery: ref(''),
    batteries: [],
    cart: [],
    seasonDatas: [],
    seasonLabels: [],
    orders: [],
    sellOrders: [],
    solarPanels: [],
    buyOrders: [],
    selectedDevice: [],
    graph4op: [],
    graph4Unop: [],
    apartments: [],
    email: '',
    photo: ref(''),
    flag: ref(''),
    isRTL: ref(true), // Default to LTR
    language: ref('fa'), // Default language is English (en)
  }),
  getters: {
    total: (state) => {
      let price = 0;
      if (state.cart && state.cart.cart_items) {
        state.cart.cart_items.forEach((item) => {
          price += item.product?.price;
        });
      }
      return price;
    },
    getDevices: (state) => {
      return state.devices;
    },
    getRecords: (state) => {
      return state.records;
    },
    getCategories24: (state) => {

      return state.categories24;
    },
    getValues24: (state) => {

      return state.values24;
    },
    getCategoriesMonth: (state) => {

      return state.categoriesMonth;
    },
    getValuesMonth: (state) => {

      return state.valuesMonth;
    },
    getBuyOrders: (state) => {

      return state.buyOrders;
    },
    getSellOrders: (state) => {
      return state.sellOrders;
    },
    getselectedDevice: (state) => {
      return state.selectedDevice;
    },
    getApartment: (state) => {
      return state.apartments;
    },
    filteredProducts: (state) => {
      if (state.activeGenre === 1) {
        return state.products;
      } else {
        return state.products.filter((product) => product.category.id === state.activeGenre);
      }
    },
    filteredNotActiveProducts: (state) => {
      if (state.activeGenre === 1) {
        return state.not_active_products;
      } else {
        return state.not_active_products.filter((product) => product.category.id === state.activeGenre);
      }
    },
    textDirection: (state) => {
      return state.isRTL ? 'rtl' : 'ltr';
    },
    getLan: (state) => {
      return state.language;
    },
    getFlag: (state) => {
      return state.flag;
    },
  },
  actions: {
    async fetchProfile() {
      // const { t } = useI18n({ useScope: "local" })

      try {
        const accessToken = useCookie('access_token').value;
        if (accessToken) {
          // If an access token exists, fetch the user's profile from the server.
          const response = await axios.get(`${apiUrl}/users/profiles/`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'accept': 'application/json',
            },
          });

          if (response.data) {
            console.log(
              response.data, "qweqwewww"
            )
            this.email = response.data.user.email;
            this.photo = response.data?.photo || '';
            this.apartment_no = response.data?.apartment_no || '';
            this.area = response.data?.area || '';
          }
        } else {
          // If there's no access token, handle the case.
          console.error('Error fetching user token:');
          // this.showWarningToast(t('fetchProfile.errors.noAccessToken'));
        }
      } catch (error) {
        console.error('Error fetching user profile:', error);
        // this.showErrorToast(t('fetchProfile.errors.fetchFailed'));
      }
    },
    async sendEmail(email, subject, description) {

      try {
        const accessToken = useCookie('access_token').value;
        if (accessToken) {
          // If an access token exists, fetch the user's profile from the server.
          const response = await axios.post(`${apiUrl}/admins/email`,
              {
                email: email,
                subject: subject,
                description: description,
              }
              ,
              {
                headers: {
                  Authorization: `Bearer ${accessToken}`,
                  'accept':
                    'application/json',
                }
                ,
              }
            )
          ;
          console.log(response)
          console.log('response')
          if (response.status === 200) {
            this.showSuccessToast('Success Send');

            return true
          }
        } else {
          // If there's no access token, handle the case.
          console.error('Error fetching user token:');
          // this.showWarningToast(t('fetchProfile.errors.noAccessToken'));
        }
      } catch (error) {
        console.error('Error fetching user profile:', error);
        // this.showErrorToast(t('fetchProfile.errors.fetchFailed'));
      }
    },

    async changePhoto() {

      try {
        const accessToken = useCookie('access_token').value;
        if (accessToken) {
          const response = await axios.patch(`${apiUrl}/users/profiles/update/photo`, {}, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
            },
          });
          if (response.data) {
            this.photo = response.data?.photo || '';
          }
        } else {
          console.error('Error changing user photo:');

        }
      } catch (error) {
        console.error('Error changing user photo:', error);
      }
    },
    async ChangeActiveGenre(categoryID) {
      console.log(categoryID, "qweqwe")
      this.activeGenre = categoryID
    },

    async fetchCategories() {
      const {t} = useI18n({useScope: 'local'});

      try {
        const categoriesResponse = await axios.get(`${apiUrl}/categories`);
        this.categories = [{id: 1, name: {"fa": "همه", "en": "All"}}, ...categoriesResponse.data];
      } catch (error) {
        console.error('Error fetching categories:', error);
        this.showErrorToast(t('fetchCategories.errors.fetchFailed'));
      }
    },


    async fetchProducts() {

      try {
        const productsResponse = await axios.get(`${apiUrl}/products/?page=1&page_size=10`);
        this.products = productsResponse.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },

    async fetchDevices() {

      try {
        const response = await axios.get(`${apiUrl}/device/`);
        this.devices = response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetchSolarPanels() {

      try {
        const response = await axios.get(`${apiUrl}/solar-panels/read`);
        this.solarPanels = response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetch24Records() {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/power-records/24hour-chart`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        if (response.data) {
          this.categories24 = response.data['categories'];
          this.values24 = response.data['values'];
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetch24RecordsAdmin() {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/super-admin/24hour-chart`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        if (response.data) {
          this.categories24 = response.data['categories'];
          this.values24 = response.data['values'];
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetch24RecordsMng() {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/super-admin/24hour-chart-block`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        if (response.data) {
          this.categories24 = response.data['categories'];
          this.values24 = response.data['values'];
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetchMonthRecords(year = 2024, month = 5) {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/power-records/month-chart?year=${year}&month=${month}`,


          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        if (response.data) {
          this.valuesMonth = response.data[0];
          this.categoriesMonth = response.data[1];
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetchMonthRecordsAdmin(year = 2024, month = 5) {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/super-admin/month-chart?year=${year}&month=${month}`,


          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        if (response.data) {
          this.valuesMonth = response.data[0];
          this.categoriesMonth = response.data[1];
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetchMonthRecordsMng(year = 2024, month = 5) {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/super-admin/month-chart-block?year=${year}&month=${month}`,


          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        if (response.data) {
          this.valuesMonth = response.data[0];
          this.categoriesMonth = response.data[1];
        }

      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },

    async deleteDevice(deviceId) {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.delete(`${apiUrl}/device/${deviceId}/delete`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        });
        if (response.status === 200) {
          window.location.reload();

          this.showSuccessToast('Delete');

        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },

    async fetchRecords() {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/power-records/records`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        this.records = response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },


    async fetchBattery() {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/battery/`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        this.battery = response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetchAllBattery() {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/battery/all`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        this.batteries = response.data;
      } catch (error) {
        console.error('Error fetching products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },
    async fetchNotActiveProducts() {

      try {
        const productsResponse = await axios.get(`${apiUrl}/products/isActivate/false/?page=1&page_size=10`);
        this.not_active_products = productsResponse.data;
      } catch (error) {
        console.error('Error fetching not active products:', error);
        const {t} = useI18n({useScope: 'local'});

        this.showErrorToast(t('fetchProducts.errors.fetchFailed'));
      }
    },

    async fetchProductBySlug(slug) {
      const {t} = useI18n({useScope: 'local'});

      try {
        const response = await axios.get(`${apiUrl}/products/${slug}`);
        this.product = response.data;
      } catch (error) {
        console.error('Error fetching product by slug:', error);
        this.showErrorToast(t('fetchProductBySlug.errors.fetchFailed'));
      }
    },

    async fetchCart() {
      const {t} = useI18n({useScope: 'local'});

      const accessToken = useCookie('access_token').value;

      if (accessToken) {
        // If an access token exists, fetch the cart from the server.
        try {
          const cartResponse = await axios.get(`${apiUrl}/users/carts`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            },
          });
          this.cart = cartResponse.data;
        } catch (error) {
          console.error('Error fetching cart:', error);
          this.showErrorToast(t('fetchCart.errors.fetchFailed'));
        }
      } else {
        // If there's no access token, create a new cart (or retrieve it from localStorage).
        const storedCart = localStorage.getItem('cart');

        if (storedCart) {
          // If a cart exists in localStorage, use it.
          this.cart = JSON.parse(storedCart);
        } else {
          // If no cart is found, initialize an empty cart in the store.
          this.cart = {cart_items: []};

          // Save the empty cart in localStorage.
          localStorage.setItem('cart', JSON.stringify(this.cart));
        }
      }
    },


    async fetchEmail() {
      const storedEmail = localStorage.getItem('email');
      this.email = storedEmail;
    },
    async fetchSellOrders() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/users/orders/order/sell`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          // params: {
          //   page: page,
          //   page_size: perPage,
          // },
        });
        // console.log(response.data,'sellsell')
        this.sellOrders = response.data;
        // console.log(this.sellOrders,'sellsellz')

      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetchBuyOrders() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/users/orders/order/buy`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          // params: {
          //   page: page,
          //   page_size: perPage,
          // },
        });
        // console.log(response.data,'buybuy')

        this.buyOrders = response.data;
        // console.log(this.buyOrders,'buybuyz')

      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetchGraph4() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/power-records/cal_graph4`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          // params: {
          //   page: page,
          //   page_size: perPage,
          // },
        });
        // console.log(response.data,'buybuy')

        this.graph4Unop = response.data[0];
        this.graph4op = response.data[1];
        // console.log(this.buyOrders,'buybuyz')

      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetchGraph4Admin() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/super-admin/cal_graph4`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          // params: {
          //   page: page,
          //   page_size: perPage,
          // },
        });
        // console.log(response.data,'buybuy')

        this.graph4Unop = response.data[0];
        this.graph4op = response.data[1];
        // console.log(this.buyOrders,'buybuyz')

      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetchGraph4Mng() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/super-admin/cal_graph4`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          // params: {
          //   page: page,
          //   page_size: perPage,
          // },
        });
        // console.log(response.data,'buybuy')

        this.graph4Unop = response.data[0].map(item => item * 0.75);
        this.graph4op = response.data[1].map(item => item * 0.75);
        // console.log(this.buyOrders,'buybuyz')

      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetchusers() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/super-admin/all_users`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          // params: {
          //   page: page,
          //   page_size: perPage,
          // },
        });
        // console.log(response.data,'buybuy')

        this.allUsers = response.data;
        // console.log(this.buyOrders,'buybuyz')

      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetchusersMng() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/super-admin/all_users-block`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          // params: {
          //   page: page,
          //   page_size: perPage,
          // },
        });
        // console.log(response.data,'buybuy')

        this.allUsers = response.data;
        // console.log(this.buyOrders,'buybuyz')

      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetchOrders(page, perPage) {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/users/orders/order/last-orders`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          params: {
            page: page,
            page_size: perPage,
          },
        });
        this.orders = response.data;
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async fetch8() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/power-records/cal8`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        this.cal8 = response.data;
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async powerConsumption() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/power-records/max_power`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        });
        this.peakHour = response.data[0];
        this.peakPower = response.data[1];
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },


    async addDevice(deviceId) {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.patch(`${apiUrl}/device/select?device_id=${deviceId}`, {}, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        });
        if (response.status === 200) {
          this.showSuccessToast('Add');

        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async importExcel(file) {
      try {
        const accessToken = useCookie('access_token').value;
        const formData = new FormData();
        formData.append('file', file);

        const response = await axios.post(`${apiUrl}/power-records/upload-excel-file`, formData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'multipart/form-data',
          },
        });

        if (response.status === 200) {
          this.showSuccessToast('File uploaded successfully');
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    },
    async deleteRecord(recordId) {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.delete(`${apiUrl}/power-records/delete-record?power_record_id=${recordId}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        });
        if (response.status === 200) {
          window.location.reload();

          this.showSuccessToast('Delete');

        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async addBlock(apartment_no, area, unit) {
      try {
        const recordData = {
          apartment_no: apartment_no,
          unit: unit,
          area: area,
        };
        console.log(recordData, 'kok')
        const accessToken = useCookie('access_token').value;
        const response = await axios.post(`${apiUrl}/blocks/blocks`, recordData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }
        });
        if (response.status === 200) {
          this.showSuccessToast('Add');

        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },

    async addRecord(device_name, start, end, consumption) {
      try {
        const recordData = {
          device_name: device_name,
          start_time: start,
          end_time: end,
          consumption: consumption
        };
        console.log(recordData, 'kok')
        const accessToken = useCookie('access_token').value;
        const response = await axios.post(`${apiUrl}/power-records/add-record`, recordData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }
        });
        if (response.status === 200) {
          this.showSuccessToast('Add');

        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },
    async addOrder(user_id, solar_panel_id, amount, fee) {
      try {
        const orderData = {
          user_id: user_id,
          battery_id: solar_panel_id,
          amount: amount,
          fee: fee
        };

        console.log(orderData, 'kok');
        const accessToken = useCookie('access_token').value;
        const response = await axios.post(`${apiUrl}/users/orders/order/`, orderData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }
        });
        if (response.status === 200) {
          this.showSuccessToast('Add');
        }
      } catch (error) {
        console.error('Error adding order:', error);
      }
    },
    async addBattery(savedEnergy, soldEnergy) {
      try {
        const batteryData = {
          saved_energy: savedEnergy,
          sold_energy: soldEnergy
        };

        const accessToken = useCookie('access_token').value;
        const response = await axios.post(`${apiUrl}/battery/`, batteryData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            'accept': 'application/json'
          }
        });

        if (response.status === 200) {
          this.showSuccessToast('Battery added successfully');
        }
      } catch (error) {
        console.error('Error adding battery:', error);
      }
    },
    async fetchselectedDevice() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/device/user`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        });
        if (response.status === 200) {
          this.selectedDevice = response.data;
        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },

    async fetchSeasonChart(year = 2024, season = 'Spring') {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/power-records/season-chart?year=${year}&season=${season}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }
        });

        if (response.status === 200) {
          const data = response.data;
          const datas = data.map(item => item.total_usage);
          const labels = data.map(item => item._id);
          this.seasonDatas = datas
          this.seasonLabels = labels
          console.log(datas); // list of total_usage
          console.log(labels); // list of _id
          // You can also return these values or set them in the state if using a framework like Vue or React
          return {datas, labels};
        }
      } catch (error) {
        console.error('Error fetching season chart data:', error);
      }
    },
    async fetchSeasonChartAdmin(year = 2024, season = 'Spring') {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/super-admin/season-chart?year=${year}&season=${season}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }
        });

        if (response.status === 200) {
          const data = response.data;
          const datas = data.map(item => item.total_usage);
          const labels = data.map(item => item._id);
          this.seasonDatas = datas
          this.seasonLabels = labels
          console.log(datas); // list of total_usage
          console.log(labels); // list of _id
          // You can also return these values or set them in the state if using a framework like Vue or React
          return {datas, labels};
        }
      } catch (error) {
        console.error('Error fetching season chart data:', error);
      }
    },
    async fetchSeasonChartMng(year = 2024, season = 'Spring') {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/super-admin/season-chart-block?year=${year}&season=${season}`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          }
        });

        if (response.status === 200) {
          const data = response.data;
          const datas = data.map(item => item.total_usage);
          const labels = data.map(item => item._id);
          this.seasonDatas = datas
          this.seasonLabels = labels
          console.log(datas); // list of total_usage
          console.log(labels); // list of _id
          // You can also return these values or set them in the state if using a framework like Vue or React
          return {datas, labels};
        }
      } catch (error) {
        console.error('Error fetching season chart data:', error);
      }
    },

    async fetchApartment() {
      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.get(`${apiUrl}/apartment/all`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/x-www-form-urlencoded',
          }
        });
        if (response.status === 200) {
          this.apartments = response.data;
        }
      } catch (error) {
        console.error('Error fetching orders:', error);
      }
    },


    async addToOrder({email, password, description, userHasAccount}) {
      try {
        if (this.cart.cart_items.length >= 5) {
          this.showErrorToast('Cannot add more than 5 items to the cart');

          throw new Error('Cannot add more than 5 items to the cart');
        } else {
          if (userHasAccount.value) {
            if (email && password) {
              if (this.product) {

                const accessToken = useCookie('access_token').value;
                if (accessToken) {
                  const orderData = {
                    email: email,
                    password: password,
                    description: description,
                    product_id: this.product.id,
                  };
                  // If an accessToken exists, add the order to the server's cart.
                  const response = await axios.post(`${apiUrl}/users/carts/items`, orderData, {
                    headers: {
                      Authorization: `Bearer ${accessToken}`,
                      'Content-Type': 'application/json',
                      accept: 'application/json',
                    },
                  });
                  if (this.cart) {
                    this.cart.cart_items.push(
                      response.data,
                    );
                  }
                } else {
                  const orderData = {
                    email: email,
                    password: password,
                    description: description,
                    product: this.product,
                  };
                  // If there's no accessToken, add the order to the cart in localStorage.
                  this.cart.cart_items.push(
                    orderData
                  );
                  localStorage.setItem('cart', JSON.stringify(this.cart));
                }
              } else {
                console.error('Product not available.');
              }
            } else {
              setFieldError('email', 'Email is required');
              setFieldError('password', 'Password is required');
            }
          } else {
            if (this.product) {

              const accessToken = useCookie('access_token').value;
              if (accessToken) {
                const orderData = {
                  product_id: this.product.id,
                };
                // If an accessToken exists, add the order to the server's cart.
                const response = await axios.post(`${apiUrl}/users/carts/items`, orderData, {
                  headers: {
                    Authorization: `Bearer ${accessToken}`,
                    'Content-Type': 'application/json',
                    accept: 'application/json',
                  },
                });
                if (this.cart) {
                  this.cart.cart_items.push(
                    response.data
                  );
                }
              } else {
                const orderData = {
                  product: this.product,
                };
                this.cart.cart_items.push(
                  orderData,
                );
                localStorage.setItem('cart', JSON.stringify(this.cart));

              }
            } else {
              console.error('Product not available.');
            }
          }
        }

      } catch (error) {
        console.error('Error placing order:', error);
      }


    },
    async removeItem(itemToRemove) {
      try {
        const accessToken = useCookie('access_token').value;

        if (accessToken) {
          // If an accessToken exists, attempt to delete the order from the server's cart.
          const cartItemId = itemToRemove.id;
          const response = await axios.delete(`${apiUrl}/users/carts/items/${cartItemId}`, {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            }
          });

          if (response.status === 204) {
            // Remove the item from the cart in the store.
            const index = this.cart.cart_items.indexOf(itemToRemove);
            if (index !== -1) {
              this.cart.cart_items.splice(index, 1);
            }
          } else {
            console.error('Failed to delete CartItem:', response);
          }
        } else {

          const index = this.cart.cart_items.indexOf(itemToRemove);
          if (index !== -1) {
            this.cart.cart_items.splice(index, 1);
          }
          localStorage.setItem('cart', JSON.stringify(this.cart));

        }
      } catch (error) {
        console.error('Error deleting CartItem:', error);
      }
    },
    async verifyPayment({authority, status, id}) {
      const accessToken = useCookie('access_token').value;
      try {
        const response = await axios.post(`${apiUrl}/users/payments/verify`, {authority, status, id}, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            accept: 'application/json',
          },
        });
        if (response.data.status !== 'failure') {
          this.showSuccessToast('Success Payment');
          return true
        } else {
          this.showErrorToast('Failed Payment');
          return false

        }
      } catch (error) {
        console.error('Error sending data to the backend:', error);
        this.showErrorToast('Error sending data to the backend');
        return false

      }
    },
    showSuccessToast(message) {
      const toaster = useToaster();

      toaster.show({
        title: 'Success',
        message: message,
        color: 'success',
        icon: 'ph:check',
        closable: true,
      })
    },
    showErrorToast(message) {
      const toaster = useToaster();

      toaster.show({
        title: 'Oops!',
        message: message,
        color: 'danger',
        icon: 'lucide:alert-triangle',
        closable: true,
      })
    },
    showWarningToast(message) {
      const toaster = useToaster();
      toaster.show({
        title: 'Warning',
        message: message,
        color: 'warning',
        icon: 'ph:warning',
        closable: true,
      });
    },
    async processPayment() {

      try {
        const accessToken = useCookie('access_token').value;
        const response = await axios.post(`${apiUrl}/users/payments/request`, {}, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            accept: 'application/json',
          },
        });
        if (response.data && response.data.payment_url) {

          window.location.href = response.data.payment_url;
        } else {
          console.error('Payment URL not found in the response.');
        }
      } catch (error) {
        console.error('Error processing payment:', error);
      }
    },
    async setRTL() {
      this.isRTL = true;
      this.language = 'fa'; // Set the language to "fa" for RTL
      this.flag = 'iran.png'; // Set the language to "fa" for RTL
      localStorage.setItem('textDirection', 'rtl'); // Save in session storage
      localStorage.setItem('language', 'fa'); // Save the language in session storage
      localStorage.setItem('flag', 'iran.png'); // Save the language in session storage
    },
    async setLTR() {
      this.isRTL = false;
      this.language = 'en'; // Set the language to "en" for LTR
      this.flag = 'united-states-of-america.svg'; // Set the language to "fa" for RTL
      localStorage.setItem('textDirection', 'ltr'); // Save in session storage
      localStorage.setItem('language', 'en'); // Save the language in session storage
      localStorage.setItem('flag', 'united-states-of-america.svg'); // Save the language in session storage
    },
    async loadTextDirection() {
      const storedDirection = localStorage.getItem('textDirection');
      if (storedDirection === null) {
        if (storedDirection === 'ltr') {
          this.isRTL = false;
          this.language = 'en';
          this.flag = 'united-states-of-america.svg';
        } else {
          this.isRTL = true;
          this.language = 'fa';
          this.flag = 'iran.png';
        }
      } else {
        this.isRTL = true;
        this.language = 'fa';
        this.flag = 'iran.png';
      }

    },
  },
});
