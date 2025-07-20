import { createI18n } from 'vue-i18n'

// Import language files
import en from './locales/en.json'
import vi from './locales/vi.json'
import ja from './locales/ja.json'

// Type for supported locales
type SupportedLocale = 'en' | 'vi' | 'ja'

// Get saved language or default to English
const savedLanguage = localStorage.getItem('language') as SupportedLocale || 'en'

// Create i18n instance
export const i18n = createI18n({
  legacy: false,
  locale: savedLanguage,
  fallbackLocale: 'en',
  messages: {
    en,
    vi,
    ja
  }
})

// Helper function to change language
export const changeLanguage = (locale: SupportedLocale) => {
  i18n.global.locale.value = locale
  localStorage.setItem('language', locale)
  document.documentElement.lang = locale
}

// Available languages
export const availableLanguages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'vi', name: 'Tiếng Việt', flag: '🇻🇳' },
  { code: 'ja', name: '日本語', flag: '🇯🇵' }
]
