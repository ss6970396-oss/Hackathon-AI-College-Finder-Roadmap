import React, { useState } from 'react';
import axios from 'axios';
import {
  GraduationCap, TrendingUp, Award, MapPin, DollarSign, Heart, MessageCircle,
  X, Send, ChevronRight, Star, Users, Building2, ArrowUpRight, CheckCircle2,
  AlertCircle, Target, BarChart3, Calendar, Sparkles, ChevronLeft, Bell
} from 'lucide-react';
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell,
  ScatterChart, Scatter, LineChart, Line, CartesianGrid, Legend
} from 'recharts';
import './App.css';

const API = process.env.REACT_APP_BACKEND_URL || '';

// ─── Color Tokens ───
const C = {
  safe: '#10b981', moderate: '#f59e0b', ambitious: '#ef4444',
  ai: '#3b82f6', bg: '#09090B', card: '#18181B', border: '#27272a',
};

function App() {
  const [step, setStep] = useState('home');
  const [profile, setProfile] = useState({
    rank: '', exam_type: 'JEE', category: 'General', home_state: '',
    preferred_branches: [], preferred_cities: [], max_budget: '', name: '', email: ''
  });
  const [formStep, setFormStep] = useState(1);
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);
  const [compareIds, setCompareIds] = useState([]);
  const [compareData, setCompareData] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [chatMsgs, setChatMsgs] = useState([]);
  const [chatIn, setChatIn] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [sessionId] = useState(`s_${Date.now()}`);
  const [selCollege, setSelCollege] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [trendCollege, setTrendCollege] = useState(null);

  const branches = ['Computer Science','Electronics','Electrical','Mechanical','Civil','Chemical','Information Technology','Aerospace','Biotechnology','Architecture','Mathematics & Computing','Instrumentation','Metallurgy','Mining'];
  const states = ['Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'];
  const cities = ['Mumbai','Delhi','Bangalore','Hyderabad','Chennai','Kolkata','Pune','Ahmedabad','Jaipur','Lucknow','Kanpur','Nagpur','Indore','Bhopal','Patna','Surat','Coimbatore','Kochi','Visakhapatnam','Mangalore','Tiruchirappalli','Warangal','Rourkela','Durgapur','Silchar','Kurukshetra','Roorkee','Kharagpur','Kozhikode','Prayagraj','Jamshedpur','Guwahati','Varanasi','Agartala','Hamirpur','Srinagar','Raipur','Goa','Kakinada','Anantapur','Vellore','Manipal','Chittoor','Kottayam','Gwalior','Kurnool'];

  const set = (k, v) => setProfile(p => ({ ...p, [k]: v }));
  const toggle = (k, v) => setProfile(p => {
    const a = p[k];
    return { ...p, [k]: a.includes(v) ? a.filter(i => i !== v) : [...a, v] };
  });

  const submit = async () => {
    if (!profile.rank || !profile.email || profile.preferred_branches.length === 0) {
      alert('Please fill required fields: email, rank, and at least one branch');
      return;
    }
    setLoading(true);
    try {
      const res = await axios.post(`${API}/api/recommendations`, {
        profile: { ...profile, rank: parseInt(profile.rank), max_budget: parseFloat(profile.max_budget) || 100 }
      });
      setRecs(res.data.recommendations);
      setSummary(res.data.summary);
      setStep('dashboard');
    } catch (e) {
      console.error(e);
      alert('Failed to fetch recommendations');
    } finally { setLoading(false); }
  };

  const compare = async () => {
    if (compareIds.length < 2) { alert('Select at least 2'); return; }
    try {
      const res = await axios.post(`${API}/api/compare`, { college_ids: compareIds });
      setCompareData(res.data.colleges);
      setStep('compare');
    } catch (e) { console.error(e); }
  };

  const toggleWL = async (id) => {
    try {
      if (wishlist.includes(id)) {
        await axios.post(`${API}/api/wishlist/remove`, { student_email: profile.email, college_id: id });
        setWishlist(w => w.filter(i => i !== id));
      } else {
        await axios.post(`${API}/api/wishlist/add`, { student_email: profile.email, college_id: id });
        setWishlist(w => [...w, id]);
      }
    } catch (e) { console.error(e); }
  };

  const sendChat = async () => {
    if (!chatIn.trim()) return;
    const msg = chatIn;
    setChatMsgs(m => [...m, { role: 'user', content: msg }]);
    setChatIn('');
    setChatLoading(true);
    try {
      const res = await axios.post(`${API}/api/chat`, { message: msg, session_id: sessionId, student_profile: profile });
      setChatMsgs(m => [...m, { role: 'assistant', content: res.data.response }]);
    } catch (e) {
      setChatMsgs(m => [...m, { role: 'assistant', content: 'Sorry, something went wrong. Please try again.' }]);
    } finally { setChatLoading(false); }
  };

  const fetchRoadmap = async (branch) => {
    try {
      const res = await axios.get(`${API}/api/branch-roadmap/${encodeURIComponent(branch)}`);
      setRoadmap({ branch, text: res.data.roadmap });
    } catch (e) { console.error(e); }
  };

  const cls = (c) => c === 'Safe' ? 'text-emerald-500 bg-emerald-500/10 border-emerald-500/30'
    : c === 'Moderate' ? 'text-amber-500 bg-amber-500/10 border-amber-500/30'
    : 'text-red-500 bg-red-500/10 border-red-500/30';

  const clsIcon = (c) => c === 'Safe' ? <CheckCircle2 className="w-3.5 h-3.5" />
    : c === 'Moderate' ? <AlertCircle className="w-3.5 h-3.5" />
    : <Target className="w-3.5 h-3.5" />;

  // ═══════════════════════ HOME ═══════════════════════
  if (step === 'home') return (
    <div className="min-h-screen bg-[#09090B]" data-testid="home-page">
      <div className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-blue-500/5 to-transparent" />
        <div className="max-w-6xl mx-auto px-6 pt-24 pb-20 relative">
          <p className="text-xs font-bold uppercase tracking-[0.25em] text-zinc-500 mb-6">AI-Powered Platform</p>
          <h1 className="text-5xl sm:text-6xl lg:text-7xl font-black tracking-tighter leading-none mb-6" data-testid="app-title">
            College Admission<br/><span className="text-blue-500">Intelligence</span>
          </h1>
          <p className="text-lg text-zinc-400 max-w-xl mb-10 leading-relaxed">
            Data-driven recommendations for JEE, NEET & EAMCET students. Probability scoring, AI insights, and cutoff predictions — all in one place.
          </p>
          <div className="flex gap-4 mb-16">
            <button onClick={() => setStep('profile')} className="bg-white text-black px-8 py-3.5 rounded-md font-semibold text-sm hover:bg-zinc-200 transition-colors" data-testid="get-started-btn">
              Get Started <ArrowUpRight className="inline w-4 h-4 ml-1" />
            </button>
          </div>
          <div className="grid grid-cols-3 gap-px bg-zinc-800 rounded-md overflow-hidden border border-zinc-800">
            {[
              { icon: <Sparkles className="w-5 h-5 text-blue-500" />, t: 'AI Insights', d: 'GPT-5.2 personalized guidance for every recommendation' },
              { icon: <BarChart3 className="w-5 h-5 text-emerald-500" />, t: 'Probability Scoring', d: 'Historical cutoff analysis with Safe / Moderate / Ambitious classification' },
              { icon: <TrendingUp className="w-5 h-5 text-amber-500" />, t: 'Cutoff Predictions', d: 'ML-powered predictions for next year\'s closing ranks' },
            ].map((f, i) => (
              <div key={i} className="bg-[#18181B] p-6" data-testid={`feature-card-${i}`}>
                {f.icon}
                <h3 className="font-semibold mt-3 mb-1">{f.t}</h3>
                <p className="text-sm text-zinc-500 leading-relaxed">{f.d}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );

  // ═══════════════════════ PROFILE FORM ═══════════════════════
  if (step === 'profile') {
    const total = 4;
    return (
      <div className="min-h-screen bg-[#09090B] py-12" data-testid="profile-form">
        <div className="max-w-2xl mx-auto px-6">
          <div className="flex items-center justify-between mb-2">
            <p className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500">Build Profile</p>
            <p className="text-xs text-zinc-500">{formStep}/{total}</p>
          </div>
          <div className="w-full bg-zinc-900 h-1 mb-8 rounded-full overflow-hidden">
            <div className="bg-blue-500 h-1 transition-all duration-500 ease-out" style={{ width: `${(formStep / total) * 100}%` }} />
          </div>

          <div className="bg-[#18181B] border border-zinc-800 rounded-md p-8">
            {formStep === 1 && (
              <div className="space-y-5">
                <h3 className="text-xl font-semibold tracking-tight flex items-center gap-2"><Users className="w-5 h-5 text-zinc-400" /> Personal Info</h3>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-2">Name *</label>
                  <input value={profile.name} onChange={e => set('name', e.target.value)} className="w-full bg-zinc-900 border border-zinc-800 rounded-md px-4 py-3 text-white focus:border-blue-500 focus:outline-none text-sm" placeholder="Full name" data-testid="name-input" />
                </div>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-2">Email *</label>
                  <input type="email" value={profile.email} onChange={e => set('email', e.target.value)} className="w-full bg-zinc-900 border border-zinc-800 rounded-md px-4 py-3 text-white focus:border-blue-500 focus:outline-none text-sm" placeholder="you@email.com" data-testid="email-input" />
                </div>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-2">Home State</label>
                  <select value={profile.home_state} onChange={e => set('home_state', e.target.value)} className="w-full bg-zinc-900 border border-zinc-800 rounded-md px-4 py-3 text-white focus:border-blue-500 focus:outline-none text-sm" data-testid="state-select">
                    <option value="">Select State</option>
                    {states.map(s => <option key={s} value={s}>{s}</option>)}
                  </select>
                </div>
              </div>
            )}

            {formStep === 2 && (
              <div className="space-y-5">
                <h3 className="text-xl font-semibold tracking-tight flex items-center gap-2"><Award className="w-5 h-5 text-zinc-400" /> Exam Details</h3>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-2">Exam Type *</label>
                  <div className="grid grid-cols-3 gap-3">
                    {['JEE', 'NEET', 'EAMCET'].map(e => (
                      <button key={e} onClick={() => set('exam_type', e)} className={`py-3 rounded-md font-semibold text-sm transition-all ${profile.exam_type === e ? 'bg-white text-black' : 'bg-zinc-900 border border-zinc-800 text-zinc-300 hover:border-zinc-600'}`} data-testid={`exam-${e.toLowerCase()}-btn`}>{e}</button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-2">Your Rank *</label>
                  <input type="number" value={profile.rank} onChange={e => set('rank', e.target.value)} className="w-full bg-zinc-900 border border-zinc-800 rounded-md px-4 py-3 text-white focus:border-blue-500 focus:outline-none text-sm" placeholder="Enter rank" data-testid="rank-input" />
                </div>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-2">Category *</label>
                  <div className="grid grid-cols-4 gap-3">
                    {['General', 'OBC', 'SC', 'ST'].map(c => (
                      <button key={c} onClick={() => set('category', c)} className={`py-3 rounded-md font-semibold text-sm transition-all ${profile.category === c ? 'bg-white text-black' : 'bg-zinc-900 border border-zinc-800 text-zinc-300 hover:border-zinc-600'}`} data-testid={`category-${c.toLowerCase()}-btn`}>{c}</button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {formStep === 3 && (
              <div className="space-y-5">
                <h3 className="text-xl font-semibold tracking-tight flex items-center gap-2"><Building2 className="w-5 h-5 text-zinc-400" /> Preferences</h3>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-3">Branches * (select at least 1)</label>
                  <div className="grid grid-cols-2 gap-2 max-h-56 overflow-y-auto pr-2">
                    {branches.map(b => (
                      <button key={b} onClick={() => toggle('preferred_branches', b)} className={`py-2 px-3 rounded-md text-sm text-left transition-all ${profile.preferred_branches.includes(b) ? 'bg-blue-500/20 border border-blue-500/40 text-blue-400' : 'bg-zinc-900 border border-zinc-800 text-zinc-400 hover:border-zinc-600'}`} data-testid={`branch-${b.toLowerCase().replace(/\s+/g, '-')}-btn`}>{b}</button>
                    ))}
                  </div>
                </div>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-3">Cities (optional)</label>
                  <div className="grid grid-cols-3 gap-2 max-h-44 overflow-y-auto pr-2">
                    {cities.map(c => (
                      <button key={c} onClick={() => toggle('preferred_cities', c)} className={`py-2 px-2 rounded-md text-xs transition-all ${profile.preferred_cities.includes(c) ? 'bg-blue-500/20 border border-blue-500/40 text-blue-400' : 'bg-zinc-900 border border-zinc-800 text-zinc-500 hover:border-zinc-600'}`} data-testid={`city-${c.toLowerCase().replace(/\s+/g, '-')}-btn`}>{c}</button>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {formStep === 4 && (
              <div className="space-y-5">
                <h3 className="text-xl font-semibold tracking-tight flex items-center gap-2"><DollarSign className="w-5 h-5 text-zinc-400" /> Budget</h3>
                <div>
                  <label className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-400 block mb-2">Max Budget (4-year total, lakhs)</label>
                  <input type="number" value={profile.max_budget} onChange={e => set('max_budget', e.target.value)} className="w-full bg-zinc-900 border border-zinc-800 rounded-md px-4 py-3 text-white focus:border-blue-500 focus:outline-none text-sm" placeholder="e.g. 15" data-testid="budget-input" />
                  <p className="text-zinc-600 text-xs mt-2">Leave blank for no limit</p>
                </div>
                <div className="bg-zinc-900 border border-zinc-800 rounded-md p-5 space-y-1.5 text-sm">
                  <p className="text-xs font-bold uppercase tracking-[0.2em] text-blue-500 mb-3">Profile Summary</p>
                  <p><span className="text-zinc-500">Name:</span> <span className="text-white">{profile.name || '—'}</span></p>
                  <p><span className="text-zinc-500">Exam:</span> <span className="text-white">{profile.exam_type}</span></p>
                  <p><span className="text-zinc-500">Rank:</span> <span className="text-white">{profile.rank || '—'}</span></p>
                  <p><span className="text-zinc-500">Category:</span> <span className="text-white">{profile.category}</span></p>
                  <p><span className="text-zinc-500">Branches:</span> <span className="text-white">{profile.preferred_branches.join(', ') || '—'}</span></p>
                  <p><span className="text-zinc-500">Budget:</span> <span className="text-white">{profile.max_budget ? `₹${profile.max_budget}L` : 'No limit'}</span></p>
                </div>
              </div>
            )}

            <div className="flex justify-between mt-8 pt-6 border-t border-zinc-800">
              <button onClick={() => formStep > 1 ? setFormStep(formStep - 1) : setStep('home')} className="flex items-center gap-1 text-sm text-zinc-400 hover:text-white transition-colors" data-testid="back-btn">
                <ChevronLeft className="w-4 h-4" /> {formStep > 1 ? 'Back' : 'Home'}
              </button>
              {formStep < total ? (
                <button onClick={() => setFormStep(formStep + 1)} className="bg-white text-black px-6 py-2.5 rounded-md font-semibold text-sm hover:bg-zinc-200 transition-colors" data-testid="next-btn">
                  Next <ChevronRight className="inline w-4 h-4" />
                </button>
              ) : (
                <button onClick={submit} disabled={loading} className="bg-blue-500 text-white px-8 py-2.5 rounded-md font-semibold text-sm hover:bg-blue-600 transition-colors disabled:opacity-50" data-testid="submit-profile-btn">
                  {loading ? 'Analyzing...' : 'Get Recommendations'}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ═══════════════════════ DASHBOARD ═══════════════════════
  if (step === 'dashboard') {
    const barData = recs.slice(0, 10).map(r => ({
      name: `${r.college_name.replace(/^(NIT|IIT|IIIT)\s/, '').split(' ')[0]}`,
      prob: r.probability,
      fill: r.classification === 'Safe' ? C.safe : r.classification === 'Moderate' ? C.moderate : C.ambitious
    }));

    const scatterData = recs.map(r => ({
      x: r.total_fees,
      y: r.placement_avg,
      name: r.college_name,
      prob: r.probability,
      fill: r.classification === 'Safe' ? C.safe : r.classification === 'Moderate' ? C.moderate : C.ambitious
    }));

    const wlRecs = recs.filter(r => wishlist.includes(r.college_id));
    const wlSummary = { safe: wlRecs.filter(r => r.classification === 'Safe').length, moderate: wlRecs.filter(r => r.classification === 'Moderate').length, ambitious: wlRecs.filter(r => r.classification === 'Ambitious').length };

    return (
      <div className="min-h-screen bg-[#09090B]" data-testid="dashboard-page">
        {/* Header */}
        <div className="border-b border-zinc-800">
          <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <GraduationCap className="w-6 h-6 text-blue-500" />
              <span className="font-bold tracking-tight">College AI</span>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-xs text-zinc-500">Rank {profile.rank} &bull; {profile.category} &bull; {profile.exam_type}</span>
              <button onClick={() => setStep('profile')} className="text-xs text-zinc-400 hover:text-white border border-zinc-800 px-3 py-1.5 rounded-md transition-colors" data-testid="edit-profile-btn">Edit</button>
            </div>
          </div>
        </div>

        <div className="max-w-7xl mx-auto px-6 py-8">
          {/* Summary row */}
          {summary && (
            <div className="grid grid-cols-4 gap-px bg-zinc-800 rounded-md overflow-hidden border border-zinc-800 mb-8">
              {[
                { label: 'Safe', value: summary.safe, color: 'text-emerald-500', icon: <CheckCircle2 className="w-5 h-5" /> },
                { label: 'Moderate', value: summary.moderate, color: 'text-amber-500', icon: <AlertCircle className="w-5 h-5" /> },
                { label: 'Ambitious', value: summary.ambitious, color: 'text-red-500', icon: <Target className="w-5 h-5" /> },
                { label: 'Shortlisted', value: wishlist.length, color: 'text-blue-500', icon: <Heart className="w-5 h-5" /> },
              ].map((s, i) => (
                <div key={i} className="bg-[#18181B] p-5" data-testid={`summary-${s.label.toLowerCase()}`}>
                  <div className="flex items-center justify-between">
                    <span className={`${s.color}`}>{s.icon}</span>
                    <span className={`text-3xl font-black tracking-tighter ${s.color}`}>{s.value}</span>
                  </div>
                  <p className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500 mt-2">{s.label}</p>
                </div>
              ))}
            </div>
          )}

          {/* Wishlist summary */}
          {wishlist.length > 0 && (
            <div className="bg-blue-500/10 border border-blue-500/20 rounded-md p-4 mb-8 flex items-center justify-between" data-testid="wishlist-summary">
              <p className="text-sm text-blue-400">
                You've shortlisted <span className="font-bold text-white">{wishlist.length}</span> colleges — {wlSummary.safe} Safe, {wlSummary.moderate} Moderate, {wlSummary.ambitious} Ambitious
              </p>
              <button className="text-xs text-blue-400 flex items-center gap-1 border border-blue-500/30 px-3 py-1.5 rounded-md hover:bg-blue-500/20 transition-colors" data-testid="alert-btn">
                <Bell className="w-3 h-3" /> Alert me on cutoff changes
              </button>
            </div>
          )}

          {/* Charts Row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-px bg-zinc-800 rounded-md overflow-hidden border border-zinc-800 mb-8">
            {/* Probability Bar Chart */}
            <div className="bg-[#18181B] p-6" data-testid="probability-chart">
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500 mb-4">Top 10 — Admission Probability</p>
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={barData} layout="vertical" margin={{ left: 0, right: 10 }}>
                  <XAxis type="number" domain={[0, 100]} tick={{ fill: '#71717a', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <YAxis dataKey="name" type="category" width={80} tick={{ fill: '#a1a1aa', fontSize: 11 }} axisLine={false} tickLine={false} />
                  <Tooltip contentStyle={{ background: '#18181B', border: '1px solid #27272a', borderRadius: '4px', fontSize: '12px' }} formatter={(v) => [`${v}%`, 'Probability']} />
                  <Bar dataKey="prob" radius={[0, 3, 3, 0]} barSize={18}>
                    {barData.map((d, i) => <Cell key={i} fill={d.fill} />)}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            {/* Budget vs Placement Scatter */}
            <div className="bg-[#18181B] p-6" data-testid="scatter-chart">
              <p className="text-xs font-bold uppercase tracking-[0.2em] text-zinc-500 mb-4">Fees vs Avg Placement (₹ Lakhs)</p>
              <ResponsiveContainer width="100%" height={280}>
                <ScatterChart margin={{ left: 0, right: 10 }}>
                  <XAxis dataKey="x" name="Total Fees" tick={{ fill: '#71717a', fontSize: 11 }} axisLine={false} tickLine={false} label={{ value: 'Fees (L)', position: 'insideBottom', offset: -2, style: { fill: '#52525b', fontSize: 10 } }} />
                  <YAxis dataKey="y" name="Avg Package" tick={{ fill: '#71717a', fontSize: 11 }} axisLine={false} tickLine={false} label={{ value: 'Package (L)', angle: -90, position: 'insideLeft', style: { fill: '#52525b', fontSize: 10 } }} />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ background: '#18181B', border: '1px solid #27272a', borderRadius: '4px', fontSize: '12px' }} formatter={(v, n) => [n === 'x' ? `₹${v}L` : `₹${v}L`, n === 'x' ? 'Fees' : 'Package']} labelFormatter={(l) => ''} />
                  <Scatter data={scatterData} shape="circle">
                    {scatterData.map((d, i) => <Cell key={i} fill={d.fill} fillOpacity={0.7} r={6} />)}
                  </Scatter>
                </ScatterChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Compare bar */}
          {compareIds.length >= 2 && (
            <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-50">
              <button onClick={compare} className="bg-white text-black px-8 py-3 rounded-md font-semibold text-sm shadow-2xl hover:bg-zinc-200 transition-colors flex items-center gap-2" data-testid="compare-selected-btn">
                <BarChart3 className="w-4 h-4" /> Compare {compareIds.length} Colleges
              </button>
            </div>
          )}

          {/* College Cards */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-px bg-zinc-800 rounded-md overflow-hidden border border-zinc-800">
            {recs.map((r, i) => (
              <div key={i} className="bg-[#18181B] p-5 relative group" data-testid={`college-card-${i}`}>
                {/* Top accent bar */}
                <div className={`absolute top-0 left-0 right-0 h-0.5 ${r.classification === 'Safe' ? 'bg-emerald-500' : r.classification === 'Moderate' ? 'bg-amber-500' : 'bg-red-500'}`} />

                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className="text-[10px] font-bold uppercase tracking-[0.15em] px-2 py-0.5 bg-zinc-900 border border-zinc-800 rounded text-zinc-400">{r.type}</span>
                      {r.nirf_rank && <span className="text-[10px] font-bold uppercase tracking-[0.15em] px-2 py-0.5 bg-zinc-900 border border-zinc-800 rounded text-zinc-400">NIRF #{r.nirf_rank}</span>}
                    </div>
                    <h3 className="font-semibold tracking-tight text-white">{r.college_name}</h3>
                    <p className="text-sm text-blue-400 font-medium">{r.branch}</p>
                  </div>
                  <button onClick={() => toggleWL(r.college_id)} className="text-zinc-600 hover:text-red-500 transition-colors" data-testid={`wishlist-btn-${i}`}>
                    <Heart className={`w-5 h-5 ${wishlist.includes(r.college_id) ? 'fill-red-500 text-red-500' : ''}`} />
                  </button>
                </div>

                {/* Badge */}
                <div className={`inline-flex items-center gap-1.5 px-3 py-1.5 rounded-md border text-xs font-semibold mb-3 ${cls(r.classification)}`} data-testid={`badge-${i}`}>
                  {clsIcon(r.classification)} {r.probability}% — {r.classification}
                </div>

                {/* Details */}
                <div className="space-y-1.5 text-xs text-zinc-400 mb-3">
                  <p className="flex items-center gap-1.5"><MapPin className="w-3 h-3" /> {r.location}, {r.state}</p>
                  <p className="flex items-center gap-1.5"><DollarSign className="w-3 h-3" /> ₹{r.total_fees}L total (₹{r.fees_per_year}L/yr)</p>
                  <p className="flex items-center gap-1.5"><TrendingUp className="w-3 h-3" /> Avg: ₹{r.placement_avg}L</p>
                </div>

                {/* AI Insight */}
                <div className="bg-blue-500/5 border border-blue-500/10 rounded-md p-3 mb-3">
                  <p className="text-[11px] text-zinc-400 leading-relaxed"><Sparkles className="w-3 h-3 text-blue-500 inline mr-1" />{r.ai_insight}</p>
                </div>

                {/* Cutoff data */}
                <div className="text-[11px] text-zinc-500 mb-3 space-y-0.5">
                  <p>Last closing: <span className="text-zinc-300 font-medium">{r.last_year_closing}</span></p>
                  {r.predicted_cutoff?.predicted_closing && (
                    <p><Calendar className="w-3 h-3 inline mr-0.5" /> Predicted {r.predicted_cutoff.year}: <span className="text-blue-400 font-medium">{r.predicted_cutoff.predicted_closing}</span> <span className="text-zinc-600">({r.predicted_cutoff.confidence})</span></p>
                  )}
                </div>

                {/* Actions */}
                <div className="flex gap-2 pt-3 border-t border-zinc-800">
                  <button onClick={() => { setCompareIds(p => p.includes(r.college_id) ? p.filter(id => id !== r.college_id) : p.length < 3 ? [...p, r.college_id] : p); }} className={`flex-1 py-2 rounded-md text-xs font-medium transition-all ${compareIds.includes(r.college_id) ? 'bg-white text-black' : 'bg-zinc-900 border border-zinc-800 text-zinc-400 hover:border-zinc-600'}`} data-testid={`select-compare-btn-${i}`}>
                    {compareIds.includes(r.college_id) ? 'Selected' : 'Compare'}
                  </button>
                  <button onClick={() => { setTrendCollege(r); }} className="py-2 px-3 bg-zinc-900 border border-zinc-800 text-zinc-400 rounded-md text-xs hover:border-zinc-600 transition-colors" data-testid={`trend-btn-${i}`}>
                    Trend
                  </button>
                  <button onClick={() => { setSelCollege(r); fetchRoadmap(r.branch); }} className="py-2 px-3 bg-zinc-900 border border-zinc-800 text-zinc-400 rounded-md text-xs hover:border-zinc-600 transition-colors" data-testid={`roadmap-btn-${i}`}>
                    Roadmap
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chat Toggle */}
        <button onClick={() => setShowChat(!showChat)} className="fixed bottom-6 left-6 bg-blue-500 text-white p-3.5 rounded-md shadow-2xl hover:bg-blue-600 transition-colors z-50" data-testid="chat-toggle-btn">
          <MessageCircle className="w-5 h-5" />
        </button>

        {/* Chat Widget */}
        {showChat && (
          <div className="fixed bottom-20 left-6 w-96 h-[480px] bg-black/80 backdrop-blur-xl border border-zinc-800 rounded-md shadow-2xl z-50 flex flex-col" data-testid="chat-widget">
            <div className="bg-zinc-900 border-b border-zinc-800 p-4 flex justify-between items-center rounded-t-md">
              <h3 className="text-sm font-semibold flex items-center gap-2"><Sparkles className="w-4 h-4 text-blue-500" /> AI Advisor</h3>
              <button onClick={() => setShowChat(false)} className="text-zinc-500 hover:text-white" data-testid="chat-close-btn"><X className="w-4 h-4" /></button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {chatMsgs.length === 0 && (
                <div className="text-center text-zinc-500 text-sm mt-8">
                  <p>Ask anything about admissions</p>
                  <p className="text-xs mt-1 text-zinc-600">"Best CS college in South India under 10L?"</p>
                </div>
              )}
              {chatMsgs.map((m, i) => (
                <div key={i} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[80%] p-3 rounded-md text-sm ${m.role === 'user' ? 'bg-blue-500 text-white' : 'bg-zinc-900 border border-zinc-800 text-zinc-300'}`} data-testid={`chat-message-${i}`}>
                    {m.content}
                  </div>
                </div>
              ))}
              {chatLoading && <div className="flex justify-start"><div className="bg-zinc-900 border border-zinc-800 px-4 py-2 rounded-md text-xs text-zinc-500">Thinking...</div></div>}
            </div>
            <div className="p-3 border-t border-zinc-800">
              <div className="flex gap-2">
                <input value={chatIn} onChange={e => setChatIn(e.target.value)} onKeyDown={e => e.key === 'Enter' && sendChat()} placeholder="Type your question..." className="flex-1 bg-zinc-900 border border-zinc-800 rounded-md px-3 py-2 text-sm text-white focus:border-blue-500 focus:outline-none" data-testid="chat-input" />
                <button onClick={sendChat} className="bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 transition-colors" data-testid="chat-send-btn"><Send className="w-4 h-4" /></button>
              </div>
            </div>
          </div>
        )}

        {/* Historical Trend Modal */}
        {trendCollege && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => setTrendCollege(null)}>
            <div className="bg-[#18181B] border border-zinc-800 rounded-md p-6 max-w-xl w-full" onClick={e => e.stopPropagation()} data-testid="trend-modal">
              <div className="flex justify-between items-start mb-5">
                <div>
                  <h3 className="text-xl font-semibold tracking-tight">{trendCollege.college_name}</h3>
                  <p className="text-sm text-blue-400">{trendCollege.branch} — Cutoff Trend</p>
                </div>
                <button onClick={() => setTrendCollege(null)} className="text-zinc-500 hover:text-white" data-testid="trend-close-btn"><X className="w-5 h-5" /></button>
              </div>
              {(() => {
                const trend = (trendCollege.historical_trend || []).filter(t => t.category === profile.category).sort((a, b) => a.year - b.year);
                if (trend.length < 2) return <p className="text-zinc-500 text-sm">Not enough historical data for this category.</p>;
                const lineData = trend.map(t => ({ year: t.year, opening: t.opening_rank, closing: t.closing_rank }));
                return (
                  <ResponsiveContainer width="100%" height={260}>
                    <LineChart data={lineData} margin={{ left: 0, right: 10 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#27272a" />
                      <XAxis dataKey="year" tick={{ fill: '#71717a', fontSize: 11 }} axisLine={false} />
                      <YAxis reversed tick={{ fill: '#71717a', fontSize: 11 }} axisLine={false} label={{ value: 'Rank', angle: -90, position: 'insideLeft', style: { fill: '#52525b', fontSize: 10 } }} />
                      <Tooltip contentStyle={{ background: '#18181B', border: '1px solid #27272a', borderRadius: '4px', fontSize: '12px' }} />
                      <Legend wrapperStyle={{ fontSize: '11px' }} />
                      <Line type="monotone" dataKey="opening" stroke={C.safe} strokeWidth={2} dot={{ r: 4 }} name="Opening Rank" />
                      <Line type="monotone" dataKey="closing" stroke={C.ambitious} strokeWidth={2} dot={{ r: 4 }} name="Closing Rank" />
                    </LineChart>
                  </ResponsiveContainer>
                );
              })()}
              <div className="mt-4 text-xs text-zinc-500">
                <p>Your rank: <span className="text-white font-medium">{profile.rank}</span> | Category: {profile.category}</p>
              </div>
            </div>
          </div>
        )}

        {/* Roadmap Modal */}
        {selCollege && roadmap && (
          <div className="fixed inset-0 bg-black/80 backdrop-blur-sm flex items-center justify-center z-50 p-4" onClick={() => { setSelCollege(null); setRoadmap(null); }}>
            <div className="bg-[#18181B] border border-zinc-800 rounded-md p-6 max-w-2xl w-full" onClick={e => e.stopPropagation()} data-testid="roadmap-modal">
              <div className="flex justify-between items-start mb-5">
                <div>
                  <h3 className="text-xl font-semibold tracking-tight">{roadmap.branch}</h3>
                  <p className="text-sm text-zinc-400">Career Roadmap — {selCollege.college_name}</p>
                </div>
                <button onClick={() => { setSelCollege(null); setRoadmap(null); }} className="text-zinc-500 hover:text-white" data-testid="roadmap-close-btn"><X className="w-5 h-5" /></button>
              </div>
              <div className="bg-zinc-900 border border-zinc-800 rounded-md p-5">
                <p className="text-sm text-zinc-300 whitespace-pre-line leading-relaxed">{roadmap.text}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // ═══════════════════════ COMPARISON ═══════════════════════
  if (step === 'compare') {
    const attrs = [
      { label: 'Type', fn: c => <span className="px-2 py-0.5 bg-zinc-900 rounded text-xs">{c.type}</span> },
      { label: 'NIRF Rank', fn: c => `#${c.nirf_rank || 'N/A'}` },
      { label: 'Total Fees (4yr)', fn: c => `₹${c.total_fees}L` },
      { label: 'Avg Placement', fn: c => <span className="text-emerald-500 font-semibold">₹{c.placement_avg}L</span> },
      { label: 'Highest Package', fn: c => <span className="text-blue-400">₹{c.placement_highest}Cr</span> },
      { label: 'Facilities', fn: c => <span className="flex items-center gap-1"><Star className="w-3 h-3 text-amber-500 fill-amber-500" />{c.facilities_rating}/10</span> },
      { label: 'Campus Size', fn: c => c.campus_size },
      { label: 'Branches', fn: c => `${c.branches.length} offered` },
      { label: 'Notable Alumni', fn: c => <span className="text-zinc-500">{c.notable_alumni.slice(0, 2).join(', ')}</span> },
    ];

    return (
      <div className="min-h-screen bg-[#09090B] py-8" data-testid="comparison-page">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex items-center justify-between mb-6">
            <h1 className="text-3xl font-bold tracking-tighter">Comparison</h1>
            <button onClick={() => setStep('dashboard')} className="text-sm text-zinc-400 hover:text-white border border-zinc-800 px-4 py-2 rounded-md transition-colors" data-testid="back-to-dashboard-btn">
              <ChevronLeft className="inline w-4 h-4 mr-1" /> Dashboard
            </button>
          </div>
          <div className="border border-zinc-800 rounded-md overflow-x-auto" data-testid="comparison-table">
            <table className="w-full">
              <thead>
                <tr className="border-b border-zinc-800">
                  <th className="p-4 text-left text-xs font-bold uppercase tracking-[0.2em] text-zinc-500 bg-[#18181B] sticky left-0 z-10 min-w-[160px]">Attribute</th>
                  {compareData.map((c, i) => (
                    <th key={i} className="p-4 text-center bg-[#18181B] min-w-[220px] border-l border-zinc-800" data-testid={`comparison-college-${i}`}>
                      <div className="font-semibold text-white">{c.name}</div>
                      <div className="text-xs text-zinc-500 mt-0.5"><MapPin className="w-3 h-3 inline mr-0.5" />{c.location}</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {attrs.map((a, ai) => (
                  <tr key={ai} className="border-b border-zinc-800/50">
                    <td className="p-4 text-xs font-bold uppercase tracking-[0.15em] text-zinc-500 bg-[#18181B] sticky left-0 z-10">{a.label}</td>
                    {compareData.map((c, ci) => (
                      <td key={ci} className="p-4 text-center text-sm text-zinc-300 border-l border-zinc-800/50">{a.fn(c)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    );
  }

  return null;
}

export default App;
