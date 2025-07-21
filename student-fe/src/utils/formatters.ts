/**
 * Format a date to the specified format
 * @param date The date to format
 * @param format The format to use (default: YYYY-MM-DD)
 * @returns Formatted date string
 */
export function formatDate(date: Date | string, format: string = 'YYYY-MM-DD'): string {
  if (!date) return '';
  
  const d = typeof date === 'string' ? new Date(date) : date;
  
  if (isNaN(d.getTime())) {
    console.error('Invalid date:', date);
    return '';
  }
  
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  
  let result = format;
  result = result.replace('YYYY', year.toString());
  result = result.replace('MM', month);
  result = result.replace('DD', day);
  
  return result;
}

/**
 * Format a number with thousand separators
 * @param value The number to format
 * @returns Formatted number string
 */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat().format(value);
}

/**
 * Format a percentage value
 * @param value The percentage value (e.g., 0.75 for 75%)
 * @param decimals Number of decimal places
 * @returns Formatted percentage string
 */
export function formatPercent(value: number, decimals: number = 1): string {
  return new Intl.NumberFormat(undefined, {
    style: 'percent',
    minimumFractionDigits: decimals,
    maximumFractionDigits: decimals
  }).format(value);
}

/**
 * Format a currency value
 * @param value The value to format
 * @param currency The currency code (default: USD)
 * @param locale The locale (default: browser locale)
 * @returns Formatted currency string
 */
export function formatCurrency(value: number, currency: string = 'USD', locale?: string): string {
  return new Intl.NumberFormat(locale, {
    style: 'currency',
    currency: currency
  }).format(value);
} 