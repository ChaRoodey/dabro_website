let desktopMap, mobileMap;

export function mapInit() {
    desktopMap = new ymaps.Map("map", {
        center: [56.743450, 60.565472],
        zoom: 17,
        controls: ['zoomControl', 'geolocationControl']
    });

    mobileMap = new ymaps.Map("mobile-map", {
        center: [56.743450, 60.565472],
        zoom: 17,
        controls: ['zoomControl', 'geolocationControl']
    });

    const myPlacemark = new ymaps.Placemark([56.743450, 60.565472], {
        hintContent: 'ДаБро Барбершоп',
        balloonContent: 'г. Екатеринбург, мкр. Солнечный, ул. Лучистая 6'
    }, {
        preset: 'islands#icon',
        iconColor: '#E9D478'
    });

    desktopMap.geoObjects.add(myPlacemark);
    mobileMap.geoObjects.add(myPlacemark);
}

export function mapDestroy() {
    desktopMap?.destroy();
    desktopMap = null;

    mobileMap?.destroy();
    mobileMap = null;
}
