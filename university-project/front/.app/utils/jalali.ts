// Jalali (Persian / Shamsi) date helpers built on the native Intl API.
// No external dependency required: modern V8/Node supports the
// "persian" calendar through Intl.DateTimeFormat.

const FA_LOCALE = 'fa-IR-u-ca-persian'

function toDate(value?: any): Date | null {
  if (!value && value !== 0) return null
  if (value instanceof Date) return isNaN(value.getTime()) ? null : value
  const d = new Date(value)
  return isNaN(d.getTime()) ? null : d
}

// Full date + time, e.g. "۱۴۰۵/۰۳/۲۹، ۱۴:۳۰"
export function toJalaliDateTime(value?: any): string {
  const d = toDate(value)
  if (!d) return ''
  return new Intl.DateTimeFormat(FA_LOCALE, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(d)
}

// Date only, e.g. "۱۴۰۵/۰۳/۲۹"
export function toJalaliDate(value?: any): string {
  const d = toDate(value)
  if (!d) return ''
  return new Intl.DateTimeFormat(FA_LOCALE, {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).format(d)
}

// Day + Persian month name, e.g. "۲۹ خرداد"
export function toJalaliDayMonth(value?: any): string {
  const d = toDate(value)
  if (!d) return ''
  return new Intl.DateTimeFormat(FA_LOCALE, {
    day: 'numeric',
    month: 'long',
  }).format(d)
}

// Persian month label for a Gregorian (year, month=1-12) pair, using the
// first day of that month. Useful for the dashboard month selector.
export function gregorianMonthToJalaliLabel(year: number, month: number): string {
  const d = new Date(Date.UTC(year, month - 1, 1))
  return new Intl.DateTimeFormat(FA_LOCALE, {
    year: 'numeric',
    month: 'long',
  }).format(d)
}

// Persian (Jalali) year label for a Gregorian year. A Gregorian year spans
// two Jalali years; we show the Jalali year that covers most of it (mid-year).
export function gregorianYearToJalaliLabel(year: number): string {
  const d = new Date(Date.UTC(year, 6, 1)) // 1 July -> safely inside one Jalali year
  return new Intl.DateTimeFormat(FA_LOCALE, { year: 'numeric' }).format(d)
}

// Convert digits in a string to Persian numerals.
export function toPersianDigits(value: any): string {
  const map = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
  return String(value).replace(/[0-9]/g, (d) => map[Number(d)])
}

// ---------------------------------------------------------------------------
// Jalali <-> Gregorian conversion (algorithmic, no dependency).
// Based on the well-known jalaali-js algorithm.
// ---------------------------------------------------------------------------

function div(a: number, b: number) {
  // jalaali-js uses integer division that truncates toward zero (like ~~),
  // which differs from Math.floor for negative operands.
  return Math.trunc(a / b)
}

function jalCal(jy: number) {
  const breaks = [
    -61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 1635, 2060, 2097,
    2192, 2262, 2324, 2394, 2456, 3178,
  ]
  const bl = breaks.length
  const gy = jy + 621
  let leapJ = -14
  let jp = breaks[0]
  let jm = 0
  let jump = 0
  let leap = 0
  let n = 0
  let i = 1
  for (; i < bl; i += 1) {
    jm = breaks[i]
    jump = jm - jp
    if (jy < jm) break
    leapJ += div(jump, 33) * 8 + div(jump % 33, 4)
    jp = jm
  }
  n = jy - jp
  leapJ += div(n, 33) * 8 + div((n % 33) + 3, 4)
  if (jump % 33 === 4 && jump - n === 4) leapJ += 1
  const leapG = div(gy, 4) - div((div(gy, 100) + 1) * 3, 4) - 150
  const march = 20 + leapJ - leapG
  if (jump - n < 6) n = n - jump + div(jump + 4, 33) * 33
  leap = (((n + 1) % 33) - 1) % 4
  if (leap === -1) leap = 4
  return { leap, gy, march }
}

function g2d(gy: number, gm: number, gd: number) {
  let d =
    div((gy + div(gm - 8, 6) + 100100) * 1461, 4) +
    div(153 * ((gm + 9) % 12) + 2, 5) +
    gd -
    34840408
  d = d - div(div(gy + 100100 + div(gm - 8, 6), 100) * 3, 4) + 752
  return d
}

function d2g(jdn: number) {
  let j = 4 * jdn + 139361631
  j = j + div(div(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908
  const i = div(j % 1461, 4) * 5 + 308
  const gd = div(i % 153, 5) + 1
  const gm = (div(i, 153) % 12) + 1
  const gy = div(j, 1461) - 100100 + div(8 - gm, 6)
  return { gy, gm, gd }
}

export function jalaaliToGregorian(jy: number, jm: number, jd: number) {
  const r = jalCal(jy)
  const jdn = g2d(r.gy, 3, r.march) + (jm - 1) * 31 - div(jm, 7) * (jm - 7) + jd - 1
  return d2g(jdn)
}

export function gregorianToJalaali(gy: number, gm: number, gd: number) {
  const jdn = g2d(gy, gm, gd)
  let jy = gy - 621
  const r = jalCal(jy)
  const gregFirst = g2d(r.gy, 3, r.march)
  let k = jdn - gregFirst
  if (k >= 0) {
    if (k <= 185) {
      const jm = 1 + div(k, 31)
      const jd = (k % 31) + 1
      return { jy, jm, jd }
    }
    k -= 186
  } else {
    jy -= 1
    k += 179
    if (r.leap === 1) k += 1
  }
  const jm = 7 + div(k, 30)
  const jd = (k % 30) + 1
  return { jy, jm, jd }
}

export const JALALI_MONTHS = [
  'فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور',
  'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند',
]

// Days in a given Jalali month.
export function jalaliMonthLength(jy: number, jm: number): number {
  if (jm <= 6) return 31
  if (jm <= 11) return 30
  // Esfand: 30 in leap years, else 29. A Jalali year is leap when 12/30 exists,
  // i.e. converting (jy,12,30) back round-trips to month 12.
  const g = jalaaliToGregorian(jy, 12, 30)
  const back = gregorianToJalaali(g.gy, g.gm, g.gd)
  return back.jm === 12 && back.jd === 30 ? 30 : 29
}
