import React, { useEffect, useState } from "react";
import {
  GoogleMap,
  Marker,
  MarkerClusterer,
  useJsApiLoader,
} from "@react-google-maps/api";
import Info from "./info";

const containerStyle = {
  width: "100vw",
  height: "100vh",
};

const center = {
  lat: 43,
  lng: -79,
};

function App(props) {
  const [markers, setMarkers] = useState([]);
  const { isLoaded } = useJsApiLoader({
    id: "google-map-script",
    googleMapsApiKey: "AIzaSyBtf1Nw40XzgDCRmtm0lkduBgAoEKyoiQU",
  });
  const [popupIndex, setPopupIndex] = useState(null);
  const [map, setMap] = React.useState(null);

  const onLoad = React.useCallback(function callback(map) {
    const bounds = new window.google.maps.LatLngBounds();
    map.fitBounds(bounds);
    setMap(map);
  }, []);

  const onUnmount = React.useCallback(function callback(map) {
    setMap(null);
  }, []);

  const openMarker = (event) => {
    markers.map((marker, i) => {
      if (
        marker.lat === event.latLng.lat() &&
        marker.lng === event.latLng.lng()
      ) {
        setPopupIndex(i);
      }
    });
    console.log(event.latLng.lat());
  };

  return isLoaded ? (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={center}
      zoom={10}
      onLoad={onLoad}
      onUnmount={onUnmount}
      onClick={(event) => {
        setMarkers([
          ...markers,
          {
            lat: event.latLng.lat(),
            lng: event.latLng.lng(),
            time: new Date(),
          },
        ]);
        console.log(markers);
      }}
    >
      {markers.map((marker) => (
        <>
          <Marker
            onClick={openMarker}
            position={{ lat: marker.lat, lng: marker.lng }}
          />
        </>
      ))}

      {markers.map((marker, i) => {
        return (
          popupIndex === i && (
            <Info latitude={marker.lat} longitude={marker.lng} />
          )
        );
      })}
    </GoogleMap>
  ) : (
    <></>
  );
}

export default App;
