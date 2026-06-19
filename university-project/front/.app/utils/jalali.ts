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
