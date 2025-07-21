<template>
  <div class="space-y-6">
    <!-- Page Header -->
    <div class="flex justify-between items-center mb-2">
      <h1 class="text-2xl font-bold text-gray-900">{{ $t('reports.title') }}</h1>
      <div class="flex items-center space-x-3">
        <button 
          @click="refreshData" 
          class="px-3 py-1.5 bg-white border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 flex items-center space-x-1"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>
          <span>{{ $t('reports.refresh') }}</span>
        </button>
        <div class="dropdown relative">
          <button 
            @click="exportMenuOpen = !exportMenuOpen"
            class="px-4 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md shadow-sm text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 flex items-center space-x-1"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" /></svg>
            <span>{{ $t('reports.export') }}</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" /></svg>
          </button>
          
          <div 
            v-if="exportMenuOpen" 
            class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5 p-1 z-10"
          >
            <button 
              v-for="format in exportFormats" 
              :key="format.id"
              @click="exportReport(format.id)"
              class="w-full text-left block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900 rounded-md"
            >
              <div class="flex items-center space-x-2">
                <span class="w-5 h-5" v-html="format.icon"></span>
                <span>{{ format.label }}</span>
              </div>
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-10 w-10 border-2 border-indigo-500 border-t-transparent"></div>
    </div>
    
    <!-- Report filters -->
    <div v-else class="bg-white rounded-lg shadow p-5 border border-gray-200">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <!-- Time period filter -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('reports.filters.period') }}</label>
          <select 
            v-model="filters.period" 
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
            <option v-for="period in periods" :key="period.id" :value="period.id">{{ $t(period.label) }}</option>
          </select>
        </div>
        
        <!-- Custom date range (only show if custom period is selected) -->
        <div v-if="filters.period === 'custom'" class="sm:col-span-2">
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('reports.filters.dateRange') }}</label>
          <div class="grid grid-cols-2 gap-2">
            <input 
              v-model="filters.startDate" 
              type="date"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
            <input 
              v-model="filters.endDate" 
              type="date"
              class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </div>
        </div>
        
        <!-- Group filter -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ $t('reports.filters.groupBy') }}</label>
          <select 
            v-model="filters.groupBy" 
            class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
          >
            <option v-for="group in groupOptions" :key="group.id" :value="group.id">{{ $t(group.label) }}</option>
          </select>
        </div>
        
        <!-- Filter button -->
        <div class="flex items-end">
          <button 
            @click="applyFilters"
            class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-md shadow-sm text-sm font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 w-full"
          >
            {{ $t('reports.filters.apply') }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Reports Dashboard -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Key Statistics Cards -->
      <div v-for="(stat, index) in statistics" :key="index" class="bg-white rounded-lg shadow border border-gray-200 p-5 flex items-center">
        <div class="p-3 rounded-lg" :class="stat.bgColor">
          <span class="text-white" v-html="stat.icon"></span>
        </div>
        <div class="ml-4">
          <p class="text-sm font-medium text-gray-500">{{ $t(stat.label) }}</p>
          <div class="flex items-end">
            <p class="text-2xl font-bold text-gray-900">{{ stat.value }}</p>
            <p class="ml-2 text-sm" :class="stat.trend > 0 ? 'text-green-500' : stat.trend < 0 ? 'text-red-500' : 'text-gray-500'">
              <span class="flex items-center">
                <svg v-if="stat.trend > 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12 7a1 1 0 10-2 0v5.586l-1.293-1.293a1 1 0 00-1.414 1.414l3 3a1 1 0 001.414 0l3-3a1 1 0 00-1.414-1.414L12 12.586V7z" clip-rule="evenodd" />
                </svg>
                <svg v-else-if="stat.trend < 0" class="w-3 h-3 mr-1" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M12 13a1 1 0 10-2 0v-5.586l-1.293 1.293a1 1 0 01-1.414-1.414l3-3a1 1 0 011.414 0l3 3a1 1 0 01-1.414 1.414L12 7.414V13z" clip-rule="evenodd" />
                </svg>
                {{ Math.abs(stat.trend) }}%
              </span>
            </p>
          </div>
          <p class="text-xs text-gray-500">{{ $t('reports.comparedTo') }} {{ $t('reports.filters.periods.last_month') }}</p>
        </div>
      </div>
    </div>
    
    <!-- Enrollment Trend Chart -->
    <div class="bg-white rounded-lg shadow border border-gray-200 p-5">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-lg font-medium text-gray-900">{{ $t('reports.charts.enrollmentTrend') }}</h2>
        <div class="flex space-x-2">
          <button 
            v-for="option in chartViewOptions" 
            :key="option.id"
            @click="enrollmentChartView = option.id"
            class="px-3 py-1 text-xs rounded-md"
            :class="enrollmentChartView === option.id ? 'bg-indigo-100 text-indigo-700' : 'text-gray-500 hover:bg-gray-100'"
          >
            {{ $t(option.label) }}
          </button>
        </div>
      </div>
      
      <div class="h-64 flex items-center justify-center">
        <!-- Chart placeholder - In real implementation, use a charting library like Chart.js -->
        <div class="w-full h-full bg-gray-50 rounded-lg flex items-center justify-center">
          <div class="text-center">
            <p class="text-gray-400">{{ $t('reports.charts.enrollmentTrendDescription') }}</p>
            <p class="text-gray-500 text-sm">{{ $t('reports.placeholders.chart') }}</p>
          </div>
        </div>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Student Distribution -->
      <div class="bg-white rounded-lg shadow border border-gray-200 p-5">
        <h2 class="text-lg font-medium text-gray-900 mb-4">{{ $t('reports.charts.studentDistribution') }}</h2>
        <div class="h-64 flex items-center justify-center">
          <!-- Chart placeholder - In real implementation, use a charting library like Chart.js -->
          <div class="w-full h-full bg-gray-50 rounded-lg flex items-center justify-center">
            <div class="text-center">
              <p class="text-gray-400">{{ $t('reports.charts.studentDistributionDescription') }}</p>
              <p class="text-gray-500 text-sm">{{ $t('reports.placeholders.pieChart') }}</p>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Performance Metrics -->
      <div class="bg-white rounded-lg shadow border border-gray-200 p-5">
        <h2 class="text-lg font-medium text-gray-900 mb-4">{{ $t('reports.charts.performanceMetrics') }}</h2>
        <div class="h-64 flex items-center justify-center">
          <!-- Chart placeholder - In real implementation, use a charting library like Chart.js -->
          <div class="w-full h-full bg-gray-50 rounded-lg flex items-center justify-center">
            <div class="text-center">
              <p class="text-gray-400">{{ $t('reports.charts.performanceMetricsDescription') }}</p>
              <p class="text-gray-500 text-sm">{{ $t('reports.placeholders.barChart') }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Recent Activities Table -->
    <div class="bg-white rounded-lg shadow border border-gray-200 overflow-hidden">
      <div class="px-5 py-4 border-b border-gray-200">
        <h2 class="text-lg font-medium text-gray-900">{{ $t('reports.tables.recentActivities') }}</h2>
        <p class="text-sm text-gray-500">{{ $t('reports.tables.recentActivitiesDescription') }}</p>
      </div>
      
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ $t('reports.tables.headers.date') }}</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ $t('reports.tables.headers.studentId') }}</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ $t('reports.tables.headers.name') }}</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ $t('reports.tables.headers.activity') }}</th>
              <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">{{ $t('reports.tables.headers.details') }}</th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="(activity, index) in recentActivities" :key="index" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ activity.date }}</td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ activity.studentId }}</td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div class="flex-shrink-0 h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 text-sm font-medium">
                    {{ activity.initials }}
                  </div>
                  <div class="ml-4">
                    <div class="text-sm font-medium text-gray-900">{{ activity.name }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="activity.statusColor">
                  {{ activity.activity }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ activity.details }}</td>
            </tr>
            
            <!-- When no activities -->
            <tr v-if="recentActivities.length === 0">
              <td colspan="5" class="px-6 py-12 text-center">
                <p class="text-gray-500">{{ $t('reports.tables.noActivities') }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <div class="px-5 py-3 border-t border-gray-200 flex items-center justify-between">
        <div class="text-sm text-gray-500">
          {{ $t('reports.tables.showingResults', { from: 1, to: 5, total: 20 }) }}
        </div>
        <div class="flex space-x-2">
          <button class="px-3 py-1 border border-gray-300 rounded-md text-sm text-gray-700 hover:bg-gray-50">{{ $t('common.previous') }}</button>
          <button class="px-3 py-1 bg-indigo-600 text-white rounded-md text-sm hover:bg-indigo-700">{{ $t('common.next') }}</button>
        </div>
      </div>
    </div>
    
    <!-- Click outside handler for export menu -->
    <div v-if="exportMenuOpen" @click="exportMenuOpen = false" class="fixed inset-0 z-5"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { useI18n } from 'vue-i18n'

const toast = useToast()
const { t } = useI18n()

// State
const loading = ref(false)
const exportMenuOpen = ref(false)
const enrollmentChartView = ref('monthly')

// Filter options
const periods = [
  { id: 'current_month', label: 'reports.filters.periods.current_month' },
  { id: 'last_month', label: 'reports.filters.periods.last_month' },
  { id: 'last_3_months', label: 'reports.filters.periods.last_3_months' },
  { id: 'last_6_months', label: 'reports.filters.periods.last_6_months' },
  { id: 'current_year', label: 'reports.filters.periods.current_year' },
  { id: 'last_year', label: 'reports.filters.periods.last_year' },
  { id: 'custom', label: 'reports.filters.periods.custom' }
]

const groupOptions = [
  { id: 'day', label: 'reports.filters.groups.day' },
  { id: 'week', label: 'reports.filters.groups.week' },
  { id: 'month', label: 'reports.filters.groups.month' },
  { id: 'year', label: 'reports.filters.groups.year' }
]

const chartViewOptions = [
  { id: 'daily', label: 'reports.filters.chartViews.daily' },
  { id: 'weekly', label: 'reports.filters.chartViews.weekly' },
  { id: 'monthly', label: 'reports.filters.chartViews.monthly' },
  { id: 'yearly', label: 'reports.filters.chartViews.yearly' }
]

const exportFormats = [
  { 
    id: 'pdf', 
    label: 'PDF', 
    icon: '<svg class="w-5 h-5 text-red-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 2v12h8V6H6z" clip-rule="evenodd" /></svg>'
  },
  { 
    id: 'excel', 
    label: 'Excel', 
    icon: '<svg class="w-5 h-5 text-green-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 2v12h8V6H6z" clip-rule="evenodd" /></svg>'
  },
  { 
    id: 'csv', 
    label: 'CSV', 
    icon: '<svg class="w-5 h-5 text-gray-600" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 2v12h8V6H6z" clip-rule="evenodd" /></svg>' 
  },
  { 
    id: 'image', 
    label: 'Image', 
    icon: '<svg class="w-5 h-5 text-blue-500" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 2v12h8V6H6z" clip-rule="evenodd" /></svg>'
  }
]

// Filters state
const filters = reactive({
  period: 'current_month',
  startDate: '',
  endDate: '',
  groupBy: 'month'
})

// Statistics
const statistics = ref([
  {
    label: 'reports.stats.totalStudents',
    value: '2,845',
    trend: 12.5,
    icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" /></svg>',
    bgColor: 'bg-blue-600'
  },
  {
    label: 'reports.stats.newEnrollments',
    value: '487',
    trend: 8.2,
    icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" /></svg>',
    bgColor: 'bg-green-600'
  },
  {
    label: 'reports.stats.completionRate',
    value: '94.2%',
    trend: -2.4,
    icon: '<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>',
    bgColor: 'bg-purple-600'
  }
])

// Sample recent activities data
const recentActivities = ref([
  {
    date: '2023-11-15 13:45',
    studentId: 'STD-2023-001',
    name: 'Nguyễn Văn A',
    initials: 'NA',
    activity: 'Enrollment',
    statusColor: 'bg-green-100 text-green-800',
    details: 'Enrolled in Computer Science'
  },
  {
    date: '2023-11-15 10:20',
    studentId: 'STD-2023-042',
    name: 'Trần Thị B',
    initials: 'TB',
    activity: 'Update',
    statusColor: 'bg-blue-100 text-blue-800',
    details: 'Contact information updated'
  },
  {
    date: '2023-11-14 16:35',
    studentId: 'STD-2022-156',
    name: 'Lê Văn C',
    initials: 'LC',
    activity: 'Graduation',
    statusColor: 'bg-purple-100 text-purple-800',
    details: 'Completed Business Administration'
  },
  {
    date: '2023-11-14 09:15',
    studentId: 'STD-2023-087',
    name: 'Phạm Thị D',
    initials: 'PD',
    activity: 'Transfer',
    statusColor: 'bg-yellow-100 text-yellow-800',
    details: 'Transferred from Engineering to Design'
  },
  {
    date: '2023-11-13 14:50',
    studentId: 'STD-2022-231',
    name: 'Hoàng Văn E',
    initials: 'HE',
    activity: 'Withdrawal',
    statusColor: 'bg-red-100 text-red-800',
    details: 'Withdrew from Mathematics program'
  }
])

// Methods
const refreshData = async () => {
  loading.value = true
  
  try {
    // Here you would fetch fresh data from your API
    await new Promise(resolve => setTimeout(resolve, 800)) // Simulate API call
    toast.success(t('reports.dataRefreshed'))
  } catch (error) {
    toast.error(t('reports.refreshError'))
    console.error('Error refreshing data:', error)
  } finally {
    loading.value = false
  }
}

const applyFilters = async () => {
  loading.value = true
  
  try {
    // Here you would apply the filters and fetch filtered data from your API
    await new Promise(resolve => setTimeout(resolve, 800)) // Simulate API call
    toast.success(t('reports.filtersApplied'))
  } catch (error) {
    toast.error(t('reports.filtersError'))
    console.error('Error applying filters:', error)
  } finally {
    loading.value = false
  }
}

const exportReport = (format: string) => {
  exportMenuOpen.value = false
  
  toast.info(`${t('reports.exporting')} ${format.toUpperCase()}...`)
  
  // Here you would implement the export functionality for different formats
  setTimeout(() => {
    toast.success(`${t('reports.exportedAs')} ${format.toUpperCase()}`)
  }, 1500)
}

// Lifecycle
onMounted(() => {
  refreshData()
})
</script> 