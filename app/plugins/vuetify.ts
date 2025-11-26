import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import '../../assets/styles/main.scss'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

export default defineNuxtPlugin((app) => {
  const vuetify = createVuetify({
    components,
    directives,
    theme: {
      defaultTheme: 'light',
      themes: {
        light: {
          colors: {
            // Cream/Beige tones from the palette
            primary: '#2E7D32', // Primary green
            'primary-darken-1': '#1B5E20', // Darker green
            'primary-darken-2': '#27421D', // Very dark green

            // Green tones from the palette
            secondary: '#2E7D32', // Primary green (same as primary)
            'secondary-darken-1': '#1B5E20', // Darker green
            'secondary-darken-2': '#27421D', // Very dark green

            // Additional browns
            accent: '#2C2416', // Very dark brown
            'accent-lighten-1': '#5C4A2F', // Medium brown
            'accent-lighten-2': '#8B6F47', // Light brown

            // Backgrounds
            background: '#FFF8E7', // Very light cream (body background)
            surface: '#FFFBF0', // Slightly darker cream

            // Additional greens for variety
            success: '#6B8E23', // Olive green
            'success-lighten-1': '#8FBC8F', // Light olive green

            // Supporting colors
            info: '#4CAF50',
            warning: '#FFC107',
            error: '#F44336'
          }
        }
      }
    },
    defaults: {
      VBtn: {
        color: 'secondary',
        variant: 'elevated'
      },
      VCard: {
        elevation: 2
      }
    }
  })

  app.vueApp.use(vuetify)
})
