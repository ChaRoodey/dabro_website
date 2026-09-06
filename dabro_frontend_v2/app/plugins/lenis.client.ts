import 'lenis/dist/lenis.css'
import { startLenis, stopLenis } from '~/utils/lenis'

export default defineNuxtPlugin((nuxtApp) => {
  startLenis()

  nuxtApp.hook('app:beforeUnmount', () => {
    stopLenis()
  })
})
