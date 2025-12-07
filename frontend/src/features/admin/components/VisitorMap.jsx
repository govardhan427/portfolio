import React from 'react';
import { ComposableMap, Geographies, Geography, Marker, ZoomableGroup } from "react-simple-maps";

const geoUrl = "https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json";

const VisitorMap = ({ visitors }) => {
  const markers = visitors.map(v => {
      // Safety Check: Ensure lat/lng exist and are numbers
      const hasLoc = v.location && v.location.lat && v.location.lng;
      return { 
          coordinates: hasLoc 
            ? [parseFloat(v.location.lng), parseFloat(v.location.lat)] 
            : [79.4192, 13.6288] // Default: Tirupati
      };
  });

  return (
    <div style={{ 
        width: "100%", 
        height: "100%", 
        minHeight: "500px", 
        background: "#0a0a0a", 
        borderRadius: "8px", 
        overflow: "hidden", 
        border: "1px solid rgba(255,255,255,0.1)"
    }}>
      <ComposableMap 
        projection="geoMercator" 
        projectionConfig={{ scale: 1000, center: [78.9, 22.0] }}
        style={{ width: "100%", height: "100%" }} 
      >
        <ZoomableGroup center={[78.9, 22.0]} zoom={1} minZoom={0.5} maxZoom={4}>
            <Geographies geography={geoUrl}>
            {({ geographies }) =>
                geographies.map((geo) => {
                if (geo.id !== "356") return null; // India Only
                return (
                    <Geography
                    key={geo.rsmKey}
                    geography={geo}
                    fill="#1a1a1a"
                    stroke="#333"
                    strokeWidth={1}
                    style={{
                        default: { outline: "none" },
                        hover: { fill: "#222", outline: "none", cursor: "grab" },
                        pressed: { outline: "none", cursor: "grabbing" },
                    }}
                    />
                );
                })
            }
            </Geographies>

            {/* Real Visitors Only */}
            {markers.map((marker, i) => (
                <Marker key={i} coordinates={marker.coordinates}>
                    <circle r={8} fill="rgba(57, 255, 20, 0.3)" />
                    <circle r={4} fill="#39ff14" stroke="#fff" strokeWidth={1} />
                </Marker>
            ))}

        </ZoomableGroup>
      </ComposableMap>
    </div>
  );
};

export default VisitorMap;