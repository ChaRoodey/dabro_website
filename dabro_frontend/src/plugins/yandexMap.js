

let myMap;

export function mapInit() {
    myMap = new ymaps.Map("map", {
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

    myMap.geoObjects.add(myPlacemark);
}

export function mapDestroy() {
    myMap?.destroy();
    myMap = null;
}
