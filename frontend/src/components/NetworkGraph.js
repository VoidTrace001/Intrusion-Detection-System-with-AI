import React, { useRef, useEffect } from 'react';
import ForceGraph3D from 'react-force-graph-3d';

const NetworkGraph = ({ topology }) => {
  const fgRef = useRef();

  useEffect(() => {
    // Rotate camera slowly
    let angle = 0;
    const interval = setInterval(() => {
      angle += Math.PI / 300;
      if (fgRef.current) {
        fgRef.current.cameraPosition({
          x: 100 * Math.sin(angle),
          z: 100 * Math.cos(angle)
        });
      }
    }, 50);
    return () => clearInterval(interval);
  }, []);

  const nodes = topology?.nodes || [];
  const links = topology?.links || [];

  return (
    <div className="w-full h-full min-h-[500px] bg-black/10 relative overflow-hidden rounded-lg border border-cyan-900/30">
        <div className="absolute top-4 left-4 z-10 p-2 text-[9px] text-purple-500 font-mono tracking-[0.5em] border-l-2 border-purple-500 uppercase font-black">
        NEURAL_TOPOLOGY_GRID
      </div>
      <ForceGraph3D
        ref={fgRef}
        graphData={{ nodes, links }}
        nodeLabel="id"
        nodeColor={node => node.group === 1 ? '#06b6d4' : (node.group === 2 ? '#ef4444' : '#10b981')}
        nodeRelSize={4}
        linkColor={() => 'rgba(6, 182, 212, 0.2)'}
        linkWidth={1}
        linkOpacity={0.5}
        backgroundColor="rgba(0,0,0,0)"
        showNavInfo={false}
        width={window.innerWidth > 1200 ? 900 : window.innerWidth - 48}
        height={600}
      />
    </div>
  );
};

export default NetworkGraph;
