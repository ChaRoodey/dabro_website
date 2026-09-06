export default defineNuxtPlugin(async () => {
  const ymaps = await new Promise((resolve, reject) => {
    const existing = document.querySelector(
      'script[data-yandex-maps]'
    )

    if (existing) {
      existing.addEventListener('load', () => resolve(window.ymaps), {
        once: true,
      })
      return
    }

    const script = document.createElement('script')
    script.src =
      'https://api-maps.yandex.ru/2.1/?apikey=05e4a9b6-cdbd-4446-a544-0bcb7d87b386&lang=ru_RU'
    script.async = true
    script.dataset.yandexMaps = 'true'
    script.onload = () => resolve(window.ymaps)
    script.onerror = () => reject(new Error('Не удалось загрузить Яндекс.Карты'))

    document.head.appendChild(script)
  })

  return {
    provide: { ymaps },
  }
})