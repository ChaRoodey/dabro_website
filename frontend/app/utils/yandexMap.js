let desktopMap, mobileMap;

function createPlacemark() {
  return new ymaps.Placemark(
    [56.743450, 60.565472],
    {
      hintContent: 'ДаБро Барбершоп',
      balloonContent: 'г. Екатеринбург, мкр. Солнечный, ул. Лучистая 6',
    },
    {
      preset: 'islands#icon',
      iconColor: '#E9D478',
    },
  )
}

export function mapInit() {
  desktopMap = new ymaps.Map('map', {
    center: [56.743450, 60.565472],
    zoom: 17,
    controls: ['zoomControl', 'geolocationControl'],
  })

  mobileMap = new ymaps.Map('mobile-map', {
    center: [56.743450, 60.565472],
    zoom: 17,
    controls: ['zoomControl', 'geolocationControl'],
  })

  desktopMap.geoObjects.add(createPlacemark())
  mobileMap.geoObjects.add(createPlacemark())
}

export function mapDestroy() {
    desktopMap?.destroy();
    desktopMap = null;

    mobileMap?.destroy();
    mobileMap = null;
}
