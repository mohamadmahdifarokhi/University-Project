import {defineStore} from 'pinia';
import axios from 'axios';


const apiUrl = `${import.meta.env.VITE_BACKEND_SERVER_URL}`;

// Maps the current date to the season names the backend expects.
function getCurrentSeason(date = new Date()) {
  const m = date.getMonth() + 1; // 1-12
  const d = date.getDate();
  if ((m === 3 && d >= 21) || m === 4 || m === 5 || (m === 6 && d <= 20)) return 'Spring';
  if ((m === 6 && d >= 21) || m === 7 || m === 8 || (m === 9 && d <= 22)) return 'Summer';
  if ((m === 9 && d >= 23) || m === 10 || m === 11 || (m === 12 && d <= 20)) return 'Fall';
  return 'Winter';
}


export const useAppStore = defineStore('app', {
  state: () => ({
    devices: [],
    records: [],
    availablePeriods: { years: [], months: [], seasons: [] },
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
    seasonDatas: [],
    seasonLabels: [],
    solarPanels: [],
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
    getselectedDevice: (state) => {
      return state.selectedDevice;
    },
    getApartment: (state) => {
      return state.apartments;
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
    async fetchMonthRecords(year = new Date().getFullYear(), month = new Date().getMonth() + 1) {
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
    async fetchMonthRecordsAdmin(year = new Date().getFullYear(), month = new Date().getMonth() + 1) {
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
    async fetchMonthRecordsMng(year = new Date().getFullYear(), month = new Date().getMonth() + 1) {
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

    async fetchAvailablePeriods() {
      const accessToken = useCookie('access_token').value;

      try {
        const response = await axios.get(`${apiUrl}/power-records/available-periods`,
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/x-www-form-urlencoded',
            }
          }
        );
        this.availablePeriods = response.data;
        return response.data;
      } catch (error) {
        console.error('Error fetching available periods:', error);
        return null;
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
    async fetchEmail() {
      const storedEmail = localStorage.getItem('email');
      this.email = storedEmail;
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

    async fetchSeasonChart(year = new Date().getFullYear(), season = getCurrentSeason()) {
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
