import { useI18n } from 'vue-i18n'
import { changeLanguage, availableLanguages } from '@/i18n'

export function useLanguage() {
  const { locale, t } = useI18n()

  const currentLanguage = locale
  
  const setLanguage = (lang: 'en' | 'vi' | 'ja') => {
    changeLanguage(lang)
  }

  const getCurrentLanguageName = () => {
    const current = availableLanguages.find(lang => lang.code === locale.value)
    return current?.name || 'English'
  }

  return {
    currentLanguage,
    availableLanguages,
    setLanguage,
    getCurrentLanguageName,
    t
  }
}
