import React, { useEffect, useState, useRef, memo } from 'react';
import Globe from 'react-globe.gl';

const GlobeViz = memo(({ alerts }) => {
  const globeEl = useRef();
  const [arcsData, setArcsData] = useState([]);
  const MY_LAT = 40.7128;
  const MY_LON = -74.0060;

  useEffect(() => {
    if (!alerts || alerts.length === 0) return;

    const newArcs = alerts
      .filter(alert => alert.geo && alert.geo.lat)
      .map(alert => {
        const isSat = alert.src_ip.includes("SAT");
        return {
          startLat: alert.geo.lat,
          startLng: alert.geo.lon,
          endLat: MY_LAT,
          endLng: MY_LON,
          color: isSat ? ['#ffd700', '#d946ef'] : (alert.status === "DANGEROUS" ? ['#ff0000', '#ef4444'] : ['#00ffff', '#06b6d4']),
          dashLength: isSat ? 1.0 : 0.4,
          dashGap: isSat ? 0.5 : 4,
          dashSpeed: isSat ? 2.0 : 1.0,
          altitude: isSat ? 0.8 : 0.1, // Satellites arc higher
          name: `${alert.attack_type} | ${alert.src_ip}`
        };
      });
      
    setArcsData(newArcs);
  }, [alerts]);

  return (
    <div className="w-full h-full min-h-[500px] bg-black/10 relative">
      <div className="absolute top-4 left-4 z-10 p-2 text-[9px] text-cyan-500 font-mono tracking-[0.5em] border-l-2 border-cyan-500 uppercase font-black">
        LIVE_SIGNAL_UPLINK
      </div>
      <Globe
        ref={globeEl}
        globeImageUrl="//unpkg.com/three-globe/example/img/earth-night.jpg"
        arcsData={arcsData}
        arcColor="color"
        arcDashLength="dashLength"
        arcDashGap="dashGap"
        arcDashAnimateTime={d => 1000 / d.dashSpeed}
        arcStroke={0.6}
        arcAltitude="altitude"
        pointsData={alerts.filter(a => a.geo).map(a => ({ 
            lat: a.geo.lat, 
            lng: a.geo.lon, 
            color: a.src_ip.includes("SAT") ? "#ffd700" : (a.status === "DANGEROUS" ? "#f00" : "#0ff"), 
            radius: a.src_ip.includes("SAT") ? 1.2 : 0.5,
            alt: a.src_ip.includes("SAT") ? 0.5 : 0.01 // Satellites orbit high
        }))}
        pointColor="color"
        pointRadius="radius"
        pointAltitude="alt"
        pointPulseBm={0.5}
        labelsData={alerts.filter(a => a.geo).map(a => ({ 
            lat: a.geo.lat, 
            lng: a.geo.lon, 
            text: a.src_ip, 
            color: a.src_ip.includes("SAT") ? "#ffd700" : "#fff", 
            size: a.src_ip.includes("SAT") ? 1.0 : 0.5,
            alt: a.src_ip.includes("SAT") ? 0.6 : 0.02 
        }))}
        labelColor="color"
        labelSize="size"
        labelAltitude="alt"
        labelDotRadius={0.2}
        atmosphereColor="#06b6d4"
        atmosphereAltitude={0.15}
        backgroundColor="rgba(0,0,0,0)"
        width={window.innerWidth > 1200 ? 900 : window.innerWidth - 48}
        height={600}
      />
    </div>
  );
});

export default GlobeViz;
