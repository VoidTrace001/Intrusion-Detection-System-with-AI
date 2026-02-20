import React, { useState, useEffect, useCallback, memo, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, Database, Zap, Target, Siren, TrendingUp, X, Radio, Shield, Lock, Globe, Cpu, Terminal
} from 'lucide-react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Filler } from 'chart.js';
import { Pie, Line } from 'react-chartjs-2';
import GlobeViz from './components/GlobeViz';
import NetworkGraph from './components/NetworkGraph';
import AIChat from './components/AIChat';

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, PointElement, LineElement, Filler);

const API_BASE = "http://localhost:8000/api";

// 🚀 EXTREME REAL-TIME: HEX STREAM BACKGROUND
const HackerBackground = memo(({ rawStream }) => {
  const [lines, setLines] = useState([]);
  
  useEffect(() => {
    if (rawStream) {
      setLines(prev => [`0x${Math.random().toString(16).slice(2, 8).toUpperCase()} | ${rawStream}`, ...prev].slice(0, 50));
    }
  }, [rawStream]);

  return (
    <div className="terminal-bg opacity-20 font-mono text-[9px] grid grid-cols-3 gap-2 p-4 pointer-events-none transition-all duration-75 fixed inset-0 z-0">
      {lines.map((line, i) => (
        <div key={i} className="text-cyan-600/60 whitespace-nowrap overflow-hidden animate-in fade-in duration-300">
          {`>> ${line}`}
        </div>
      ))}
    </div>
  );
});

const Card = memo(({ title, value, icon, isAlert }) => (
  <div className={`p-4 rounded-lg glass-panel ${isAlert ? 'border-red-500/50 bg-red-950/20' : 'border-cyan-900/30'}`}>
    <div className="flex justify-between items-start mb-2"><div className="text-cyan-500">{icon}</div><span className="text-[9px] text-slate-400 font-bold uppercase tracking-[0.2em]">{title}</span></div>
    <div className={`text-2xl font-black tracking-tighter ${isAlert ? 'text-red-500 shadow-[0_0_15px_rgba(239,68,68,0.4)]' : 'text-slate-200'}`}>{value}</div>
  </div>
));

const HexModal = ({ alert, onClose }) => {
  const hex = alert.payload ? alert.payload.match(/.{1,2}/g).join(' ') : "NO_DATA";
  return (
    <div className="fixed inset-0 z-[60] flex items-center justify-center bg-black/90 backdrop-blur-md">
      <div className="w-[900px] glass-panel p-6 font-mono rounded-lg border border-cyan-500/50 shadow-[0_0_50px_rgba(6,182,212,0.2)]">
        <div className="flex justify-between mb-6 text-cyan-400 font-bold uppercase tracking-widest border-b border-cyan-900/50 pb-2">
            <span className="flex items-center gap-2"><Cpu size={18}/> Deep Forensic Analysis</span>
            <button onClick={onClose} className="hover:text-white"><X size={18}/></button>
        </div>
        
        <div className="grid grid-cols-2 gap-6 text-xs">
          <div className="space-y-4">
             {/* 🧠 LLM INSIGHT */}
             <div className="bg-purple-900/10 border-l-2 border-purple-500 p-3">
                <div className="text-purple-400 font-bold mb-1 flex justify-between">
                    <span>AI REASONING ENGINE</span>
                    <span>CONF: {(alert.llm_analysis?.confidence * 100).toFixed(0)}%</span>
                </div>
                <div className="text-slate-300 italic">"{alert.llm_analysis?.analysis || "Analyzing payload semantics..."}"</div>
                <div className="text-[9px] text-purple-600 mt-1 uppercase">{alert.llm_analysis?.model || "LLAMA-3-QUANTIZED"}</div>
             </div>

             <div className="grid grid-cols-2 gap-2">
                <div className="bg-black/40 p-2 border border-slate-800">
                    <div className="text-slate-500">SOURCE IP</div>
                    <div className="text-cyan-400 font-bold">{alert.src_ip}</div>
                </div>
                <div className="bg-black/40 p-2 border border-slate-800">
                    <div className="text-slate-500">TARGET</div>
                    <div className="text-slate-300">{alert.dst_ip}</div>
                </div>
             </div>

             <div className="bg-black/40 p-3 border border-slate-800 rounded-sm">
                <h4 className="text-[9px] text-cyan-500 font-bold uppercase mb-2 tracking-widest">Risk Calculation</h4>
                <div className="space-y-1 text-[10px]">
                    <div className="flex justify-between text-slate-500"><span>Base Weight:</span> <span className="text-slate-300">{alert.risk_breakdown?.base_severity}</span></div>
                    <div className="flex justify-between text-slate-500"><span>Model Conf:</span> <span className="text-slate-300">{alert.risk_breakdown?.confidence}%</span></div>
                    <div className="flex justify-between text-slate-500"><span>OSINT Mod:</span> <span className="text-slate-300">+{alert.risk_breakdown?.osint_impact}</span></div>
                    <div className="pt-2 mt-2 border-t border-slate-800 flex justify-between font-bold">
                        <span className="text-cyan-600">Total Score:</span>
                        <code className="text-red-500 text-sm">{alert.risk_score}</code>
                    </div>
                </div>
            </div>
          </div>

          <div className="space-y-2">
             <div className="text-[9px] text-slate-500 uppercase tracking-widest">Payload Hexdump</div>
             <div className="bg-black p-3 border border-slate-800 h-64 overflow-y-auto text-[10px] text-cyan-600/60 break-all font-mono leading-relaxed custom-scrollbar">
                {hex}
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

// 🖥️ BOOT SEQUENCE ANIMATION (Enhanced)
const BootSequence = ({ onComplete }) => {
  const [logs, setLogs] = useState([]);
  const bootLines = [
    "> INITIALIZING QUANTUM_CORE_v3.0.4...",
    "> LOADING VIRTUAL_ENVIRONMENT [ids_env]...",
    "> CHECKING HARDWARE ACCELERATION [CUDA_AVAILABLE]...",
    "> MOUNTING SCRATCH_MEMORY [0x800FF21]...",
    "> LOADING NEURAL WEIGHTS [Llama-3-8B-Quantized]...",
    "> ATTACHING SNIFFER_DAEMON [PID: 15428]...",
    "> SYNCHRONIZING WITH SAT_NODE_ALPHA [ALT: 35,786km]...",
    "> ENCRYPTING COMMAND_TUNNEL [AES-256-GCM]...",
    "> VERIFYING IMMUTABLE_LEDGER [SHA-256_CHAIN]...",
    "> INITIALIZING XAI_EXPLANATION_ENGINE...",
    "> LOADING GEOLOCATION_DATABASE [MAXMIND_LATEST]...",
    "> STARTING HONEYPOT_TRAP_GHOST_PORTS [SSH, SQL, FTP]...",
    "> ENGAGING PREDICTIVE_THREAT_ANALYZER...",
    "> CONNECTING TO GLOBAL_INTEL_FEED [OSINT]...",
    "> ALL SYSTEMS NOMINAL. BOOTSTRAP COMPLETE.",
    "> REDIRECTING TO COMMAND_DASHBOARD..."
  ];
  
  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => { 
        if (i < bootLines.length) { 
            setLogs(p => [...p, bootLines[i]]); 
            i++; 
        } else { 
            clearInterval(interval); 
            setTimeout(onComplete, 800); 
        } 
    }, 150); // Faster scrolling (150ms)
    return () => clearInterval(interval);
  }, [onComplete]);
  
  return (
    <div className="fixed inset-0 z-[500] bg-black p-12 text-cyan-500 font-mono flex flex-col justify-center items-center overflow-hidden">
        <div className="scanline"></div>
        <div className="w-full max-w-2xl space-y-1 h-96 overflow-hidden">
            <div className="text-[10px] text-cyan-800 mb-8 border-b border-cyan-900 pb-2 flex justify-between">
                <span>SYSTEM_BOOT_LOG</span>
                <span className="animate-pulse">STABLE</span>
            </div>
            {logs.map((l, i) => (
                <div key={i} className="text-xs animate-in fade-in slide-in-from-bottom-2 duration-300">
                    <span className="text-cyan-700 mr-2">[{new Date().toLocaleTimeString()}]</span>
                    {l}
                </div>
            ))}
            <div className="h-1 bg-cyan-950 w-full mt-8 overflow-hidden">
                <motion.div 
                    initial={{ width: 0 }}
                    animate={{ width: "100%" }}
                    transition={{ duration: 2.5, ease: "linear" }}
                    className="h-full bg-cyan-500 shadow-[0_0_10px_#06b6d4]"
                />
            </div>
        </div>
    </div>
  );
};

// 🛠️ SYSTEM RESET SEQUENCE
const ResetSequence = ({ onComplete }) => {
  const [logs, setLogs] = useState([]);
  const [progress, setProgress] = useState(0);
  const [isDone, setIsDone] = useState(false);

  useEffect(() => {
    const codes = [
      "> VERIFYING HARDWARE INTEGRITY...",
      "> FLUSHING MEMORY ADDRESSES...",
      "> RE-ESTABLISHING NEURAL LINK...",
      "> BYPASSING KERNEL LOCKOUT...",
      "> RELOADING SECURITY PROTOCOLS...",
      "> CLEARING VOLATILE BUFFERS...",
      "> SYNCHRONIZING WITH HQ...",
      "> INITIALIZING CORE SERVICES..."
    ];

    let count = 0;
    const interval = setInterval(() => {
      if (count < 10) {
        setLogs(prev => [...prev, codes[count % codes.length]]);
        setProgress(p => p + 10);
        count++;
      } else {
        clearInterval(interval);
        setIsDone(true);
        setTimeout(onComplete, 2000); // 2 second delay after completion message
      }
    }, 1000); // Total 10 seconds

    return () => clearInterval(interval);
  }, [onComplete]);

  return (
    <div className="fixed inset-0 z-[300] bg-black flex flex-col items-center justify-center p-8 font-mono">
      <div className="w-full max-w-2xl glass-panel p-8 border-cyan-500/50">
        <h2 className="text-cyan-400 text-xl font-black mb-6 tracking-widest uppercase">System Restoration In Progress</h2>
        
        <div className="h-64 overflow-y-auto mb-6 bg-black/50 p-4 border border-cyan-900/30 text-[10px] space-y-1 custom-scrollbar">
            {logs.map((log, i) => (
                <div key={i} className="text-green-500 animate-in fade-in slide-in-from-left-2">{log}</div>
            ))}
            {isDone && <div className="text-white font-black text-xs pt-4 tracking-widest">HARD SYSTEM RESET ACTION COMPLETED.</div>}
        </div>

        <div className="w-full h-2 bg-slate-900 rounded-full overflow-hidden">
            <motion.div 
                initial={{ width: 0 }}
                animate={{ width: `${progress}%` }}
                className="h-full bg-cyan-500 shadow-[0_0_15px_rgba(6,182,212,0.8)]"
            />
        </div>
        <div className="flex justify-between mt-2 text-[10px] text-cyan-700 font-black">
            <span>UPLINK_STABILITY: {progress}%</span>
            <span>RESTORE_CMD_EXECUTED</span>
        </div>
      </div>
    </div>
  );
};

function App() {
  const [stats, setStats] = useState({
    total_packets: 0, total_attacks: 0, live_feed: [],
    attack_distribution: {}, is_active: false, auto_block: false,
    defcon: 5, system_health: { cpu: 0, ram: 0 },
    ledger_integrity: true, honeypot_hits: 0, forecast: [], raw_hex_stream: "",
    topology: { nodes: [], links: [] }, kill_switch_engaged: false
  });
  const [selectedAlert, setSelectedAlert] = useState(null);
  const [isBooting, setIsBooting] = useState(false);
  const [isResetting, setIsResetting] = useState(false);
  const [viewMode, setViewMode] = useState("GLOBE"); // GLOBE | GRID
  const [killSwitch, setKillSwitch] = useState(false);
  const statsRef = useRef(stats);

  useEffect(() => {
    let socket;
    let reconnectTimer;
    const connect = () => {
      socket = new WebSocket('ws://localhost:8000/ws/stats');
      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.kill_switch_engaged) setKillSwitch(true);
          else setKillSwitch(false);
          setStats(data);
          statsRef.current = data;
        } catch (err) { console.error("Socket Parse Error", err); }
      };
      socket.onclose = () => { reconnectTimer = setTimeout(connect, 2000); };
    };
    connect();
    return () => { if (socket) socket.close(); clearTimeout(reconnectTimer); };
  }, []);

  const handleBoot = useCallback(() => {
    if (stats.is_active) axios.post(`${API_BASE}/stop`).catch(err => console.error("Stop failed:", err));
    else setIsBooting(true);
  }, [stats.is_active]);

  const finalizeBoot = useCallback(() => {
    axios.post(`${API_BASE}/start`).catch(err => alert("Start Failed")).finally(() => setIsBooting(false));
  }, []);

  const engageKillSwitch = async () => {
    if (window.confirm("⚠️ CONFIRM PHYSICAL DISCONNECT?")) {
        setKillSwitch(true);
        await axios.post(`${API_BASE}/killswitch`);
    }
  };

  const finalizeReset = useCallback(() => {
    setKillSwitch(false);
    setIsResetting(false);
    axios.post(`${API_BASE}/reset-killswitch`).catch(() => {});
    axios.get(`${API_BASE}/set-defcon`, {params: {level: 5}}).catch(() => {});
  }, []);

  return (
    <div className="min-h-screen bg-[#020617] text-slate-300 p-4 md:p-6 font-mono relative overflow-hidden retro-container">
      <AnimatePresence>{isBooting && <BootSequence onComplete={finalizeBoot} />}</AnimatePresence>
      <AnimatePresence>{isResetting && <ResetSequence onComplete={finalizeReset} />}</AnimatePresence>
      
      <HackerBackground rawStream={stats.raw_hex_stream} />
      <div className="scanline"></div>
      
      <AnimatePresence>
        {killSwitch && !isResetting && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="fixed inset-0 z-[200] bg-red-950/95 flex flex-col items-center justify-center text-red-500">
            <h1 className="text-9xl font-black tracking-tighter animate-pulse">TERMINATED</h1>
            <p className="text-2xl tracking-[1em] mt-4 uppercase">Network Severed</p>
            <button onClick={() => setIsResetting(true)} className="mt-12 px-8 py-4 border border-red-500 hover:bg-red-500 hover:text-white transition-all uppercase tracking-widest font-black">Hard Reset System</button>
          </motion.div>
        )}
      </AnimatePresence>

      {selectedAlert && <HexModal alert={selectedAlert} onClose={() => setSelectedAlert(null)} />}

      <header className="flex flex-col xl:flex-row justify-between items-center mb-6 gap-4 p-4 glass-panel sticky top-0 z-40">
        <div className="flex items-center gap-6">
          <motion.div animate={{ boxShadow: stats.is_active ? `0 0 20px #06b6d4` : "none" }} className={`p-3 rounded-full border ${stats.defcon === 1 ? 'border-red-600 bg-red-950' : 'border-cyan-500/30 bg-black'}`}><Target size={24} className={stats.defcon === 1 ? 'text-red-500 animate-pulse' : 'text-cyan-500'} /></motion.div>
          <div>
            <h1 className="text-2xl font-black tracking-[0.2em] text-cyan-100 flex items-center gap-2">QUANTUM<span className="text-cyan-500">IDS</span><span className="text-[10px] bg-cyan-900/50 px-2 py-0.5 rounded text-cyan-300 tracking-normal border border-cyan-500/30">v3.0</span></h1>
            <div className="flex gap-4 text-[10px] text-slate-500 font-bold uppercase tracking-[0.2em] mt-1"><span>CPU: {stats.system_health.cpu}%</span><span>RAM: {stats.system_health.ram}%</span><span className={stats.ledger_integrity ? "text-green-500" : "text-red-500"}>LEDGER: {stats.ledger_integrity ? "SECURE" : "CORRUPT"}</span></div>
          </div>
        </div>
        <div className="flex items-center gap-4">
             <div className="flex border border-slate-700 rounded-sm overflow-hidden">
                <button onClick={() => setViewMode("GLOBE")} className={`px-4 py-2 text-[10px] font-bold ${viewMode === "GLOBE" ? "bg-cyan-600 text-white" : "bg-black text-slate-500 hover:text-white"}`}><Globe size={14}/></button>
                <button onClick={() => setViewMode("GRID")} className={`px-4 py-2 text-[10px] font-bold ${viewMode === "GRID" ? "bg-cyan-600 text-white" : "bg-black text-slate-500 hover:text-white"}`}><Activity size={14}/></button>
             </div>
             <div className="hidden xl:flex gap-1 bg-black/60 p-1 border border-slate-800">
                {[5, 4, 3, 2, 1].map((l) => (
                    <button key={l} onClick={() => axios.post(`${API_BASE}/set-defcon`, {level: l})} className={`px-3 py-1 text-[9px] font-black transition-all ${stats.defcon === l ? 'bg-cyan-600 text-white shadow-[0_0_10px_rgba(6,182,212,0.5)]' : 'text-slate-600 hover:text-white'}`}>L{l}</button>
                ))}
             </div>
            <button onClick={engageKillSwitch} className="bg-red-950/30 border border-red-600/50 text-red-500 hover:bg-red-600 hover:text-white px-6 py-2 text-xs font-black tracking-widest uppercase transition-all duration-300 shadow-[0_0_15px_rgba(239,68,68,0.2)]">KILL SWITCH</button>
            <button onClick={handleBoot} className={`px-8 py-2 font-black text-xs tracking-widest border transition-all ${stats.is_active ? 'border-red-500 text-red-100 bg-red-950/30' : 'border-cyan-500 text-cyan-100 bg-cyan-950/30'}`}>{stats.is_active ? 'DEACTIVATE' : 'INITIALIZE'}</button>
        </div>
      </header>

      <main className="max-w-[1920px] mx-auto p-6 grid grid-cols-12 gap-6 relative z-10 h-[calc(100vh-140px)]">
        <div className="col-span-12 lg:col-span-3 flex flex-col gap-6 h-full overflow-hidden">
            <div className="glass-panel p-4 flex-shrink-0">
                <div className="grid grid-cols-2 gap-4">
                    <Card title="PACKETS" value={stats.total_packets} icon={<Activity size={16}/>} />
                    <Card title="THREATS" value={stats.total_attacks} icon={<Siren size={16}/>} isAlert={stats.total_attacks > 0} />
                </div>
                <div className="mt-4 p-3 bg-black/40 border border-slate-800 rounded-lg">
                    <div className="text-[10px] text-slate-500 uppercase tracking-widest mb-2">Threat Vector Forecast</div>
                     <div className="h-16"><Line data={{ labels: Array(10).fill(''), datasets: [{ data: stats.forecast || [], borderColor: '#06b6d4', borderWidth: 1, pointRadius: 0, tension: 0.4 }] }} options={{ maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { display: false }, y: { display: false, min: 0 } } }} /></div>
                </div>
            </div>
            <div className="glass-panel p-1 flex-grow overflow-hidden flex flex-col">
                <div className="p-2 border-b border-cyan-900/30 text-[10px] font-bold text-cyan-500 uppercase tracking-widest bg-cyan-950/20">SYSTEM_LOG_MONITOR</div>
                <div className="flex-grow p-4 font-mono text-[10px] text-slate-500 overflow-y-auto custom-scrollbar bg-black/20">
                    <div className="text-green-500/50">> Initializing log sequence...</div>
                    <div className="text-cyan-500/50">> Kernel: Secure Boot Active</div>
                    <div className="text-slate-600">> Hardware: All nodes reporting nominal...</div>
                </div>
            </div>
        </div>

        <div className="col-span-12 lg:col-span-6 h-full glass-panel p-0 overflow-hidden relative border-cyan-500/30 shadow-[0_0_30px_rgba(6,182,212,0.1)]">
            <div className="absolute top-4 left-4 z-20 flex gap-2"><span className="text-[9px] bg-black/80 text-cyan-500 px-2 py-1 border border-cyan-800 font-mono">LIVE_FEED: {stats.raw_hex_stream ? "RECEIVING" : "IDLE"}</span></div>
            {viewMode === "GLOBE" ? <GlobeViz alerts={stats.live_feed} /> : <NetworkGraph topology={stats.topology} />}
        </div>

        <div className="col-span-12 lg:col-span-3 h-full flex flex-col gap-6 overflow-hidden">
            <div className="glass-panel p-0 flex-[2] overflow-hidden flex flex-col border-cyan-500/30">
                <div className="p-3 border-b border-cyan-900/30 text-[10px] font-bold text-cyan-400 uppercase tracking-[0.3em] bg-cyan-950/20 flex items-center gap-2"><Terminal size={14} className="animate-pulse" />AI COMMAND ASSISTANT</div>
                <div className="flex-grow relative overflow-hidden"><AIChat /></div>
            </div>
            <div className="glass-panel p-0 flex-[3] flex flex-col overflow-hidden border-cyan-900/30">
                <div className="p-4 border-b border-cyan-900/30 bg-cyan-950/10 flex justify-between items-center"><span className="text-[10px] font-bold text-cyan-400 uppercase tracking-widest">Signal Intercepts</span><span className="text-[9px] text-slate-500">{stats.live_feed.length} ACTIVE</span></div>
                <div className="flex-grow overflow-y-auto custom-scrollbar p-2 space-y-2">
                    {stats.live_feed.map((packet, idx) => (
                      <div key={idx} onClick={() => setSelectedAlert(packet)} className={`p-3 border-l-2 cursor-pointer transition-all hover:bg-white/5 ${packet.status === "DANGEROUS" ? "border-red-500 bg-red-950/10" : "border-cyan-500 bg-cyan-950/10"}`}>
                        <div className="flex justify-between items-center mb-1"><span className={`text-xs font-bold ${packet.status === "DANGEROUS" ? "text-red-400" : "text-cyan-400"}`}>{packet.src_ip}</span><span className="text-[9px] text-slate-500">{packet.timestamp.split(" ")[1]}</span></div>
                        <div className="flex justify-between items-center"><span className="text-[10px] text-slate-400">{packet.attack_type}</span>{packet.llm_analysis && <span className="text-[9px] text-purple-400 font-bold flex items-center gap-1"><Cpu size={10}/> AI</span>}</div>
                      </div>
                    ))}
                </div>
            </div>
        </div>
      </main>
    </div>
  );
}

export default App;
