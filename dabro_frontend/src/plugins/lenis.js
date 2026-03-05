import Lenis from 'lenis'

let lenis = null

export function startLenis() {
  const reduced = window.matchMedia &&
    window.matchMedia('(prefers-reduced-motion: reduce)').matches

  if (reduced) return null

  lenis = new Lenis({
    autoRaf: true,     // сам крутит requestAnimationFrame
    smoothWheel: true, // по умолчанию true, оставим явно
  })

  return lenis
}

export function getLenis() {
  return lenis
}

export function stopLenis() {
  if (lenis) {
    lenis.destroy()
    lenis = null
  }
}
