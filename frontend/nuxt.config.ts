import path from 'path'

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  modules: ['nuxt-primevue', "@nuxtjs/tailwindcss"],
  primevue: {
      options: {
        unstyled: true
      },
      importPT: { 
        from: path.resolve(__dirname, './presets/rl-ui/') 
      } 
  }
})