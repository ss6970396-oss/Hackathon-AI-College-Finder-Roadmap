import React, { useState } from 'react';
import axios from 'axios';
import { 
  GraduationCap, 
  TrendingUp, 
  Award, 
  MapPin, 
  DollarSign, 
  Heart, 
  MessageCircle, 
  X, 
  Send, 
  ChevronRight,
  Star,
  Users,
  Building2,
  ArrowUpRight,
  CheckCircle2,
  AlertCircle,
  Target,
  BarChart3,
  Calendar,
  Sparkles
} from 'lucide-react';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, ArcElement } from 'chart.js';
import { Bar } from 'react-chartjs-2';
import './App.css';

ChartJS.register(CategoryScale, LinearScale, BarElement, LineElement, PointElement, Title, Tooltip, Legend, ArcElement);

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentStep, setCurrentStep] = useState('home');
  const [profileData, setProfileData] = useState({
    rank: '',
    exam_type: 'JEE',
    category: 'General',
    home_state: '',
    preferred_branches: [],
    preferred_cities: [],
    max_budget: '',
    name: '',
    email: ''
  });
  const [formStep, setFormStep] = useState(1);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState(null);
  const [selectedForComparison, setSelectedForComparison] = useState([]);
  const [comparisonData, setComparisonData] = useState([]);
  const [wishlist, setWishlist] = useState([]);
  const [showChat, setShowChat] = useState(false);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [sessionId] = useState(`session_${Date.now()}`);
  const [selectedCollege, setSelectedCollege] = useState(null);
  const [branchRoadmap, setBranchRoadmap] = useState(null);

  const branches = [
    'Computer Science',
    'Electronics',
    'Electrical',
    'Mechanical',
    'Civil',
    'Chemical',
    'Information Technology',
    'Aerospace',
    'Biotechnology',
    'Architecture',
    'Mathematics & Computing',
    'Instrumentation',
    'Metallurgy',
    'Mining'
  ];

  const indianStates = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chhattisgarh',
    'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram',
    'Nagaland', 'Odisha', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu',
    'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal', 'Delhi'
  ];

  const cities = [
    'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
    'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow', 'Kanpur', 'Nagpur',
    'Indore', 'Bhopal', 'Patna', 'Vadodara', 'Coimbatore', 'Kochi',
    'Visakhapatnam', 'Mangalore', 'Tiruchirappalli', 'Warangal', 'Rourkela',
    'Durgapur', 'Silchar', 'Kurukshetra', 'Allahabad', 'Roorkee', 'Kharagpur',
    'Kozhikode', 'Prayagraj', 'Jamshedpur'
  ];

  const handleInputChange = (field, value) => {
    setProfileData(prev => ({ ...prev, [field]: value }));
  };

  const toggleArrayField = (field, value) => {
    setProfileData(prev => {
      const currentArray = prev[field];
      if (currentArray.includes(value)) {
        return { ...prev, [field]: currentArray.filter(item => item !== value) };
      } else {
        return { ...prev, [field]: [...currentArray, value] };
      }
    });
  };

  const handleSubmitProfile = async () => {
    if (!profileData.rank || !profileData.email || profileData.preferred_branches.length === 0) {
      alert('Please fill all required fields');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`${BACKEND_URL}/api/recommendations`, {
        profile: {
          ...profileData,
          rank: parseInt(profileData.rank),
          max_budget: parseFloat(profileData.max_budget) || 15
        }
      });

      setRecommendations(response.data.recommendations);
      setSummary(response.data.summary);
      setCurrentStep('dashboard');
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      alert('Failed to fetch recommendations. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleComparison = (collegeId) => {
    setSelectedForComparison(prev => {
      if (prev.includes(collegeId)) {
        return prev.filter(id => id !== collegeId);
      } else if (prev.length < 3) {
        return [...prev, collegeId];
      } else {
        alert('You can compare up to 3 colleges only');
        return prev;
      }
    });
  };

  const handleCompare = async () => {
    if (selectedForComparison.length < 2) {
      alert('Please select at least 2 colleges to compare');
      return;
    }

    try {
      const response = await axios.post(`${BACKEND_URL}/api/compare`, {
        college_ids: selectedForComparison
      });
      setComparisonData(response.data.colleges);
      setCurrentStep('comparison');
    } catch (error) {
      console.error('Error comparing colleges:', error);
    }
  };

  const toggleWishlist = async (collegeId) => {
    try {
      if (wishlist.includes(collegeId)) {
        await axios.post(`${BACKEND_URL}/api/wishlist/remove`, {
          student_email: profileData.email,
          college_id: collegeId
        });
        setWishlist(prev => prev.filter(id => id !== collegeId));
      } else {
        await axios.post(`${BACKEND_URL}/api/wishlist/add`, {
          student_email: profileData.email,
          college_id: collegeId
        });
        setWishlist(prev => [...prev, collegeId]);
      }
    } catch (error) {
      console.error('Error updating wishlist:', error);
    }
  };

  const sendChatMessage = async () => {
    if (!chatInput.trim()) return;

    const userMessage = chatInput;
    setChatMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setChatInput('');

    try {
      const response = await axios.post(`${BACKEND_URL}/api/chat`, {
        message: userMessage,
        session_id: sessionId,
        student_profile: profileData
      });

      setChatMessages(prev => [...prev, { role: 'assistant', content: response.data.response }]);
    } catch (error) {
      console.error('Error sending chat message:', error);
      setChatMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Please try again.' }]);
    }
  };

  const fetchBranchRoadmap = async (branch) => {
    try {
      const response = await axios.get(`${BACKEND_URL}/api/branch-roadmap/${encodeURIComponent(branch)}`);
      setBranchRoadmap({ branch, roadmap: response.data.roadmap });
    } catch (error) {
      console.error('Error fetching roadmap:', error);
    }
  };

  const getClassificationColor = (classification) => {
    switch (classification) {
      case 'Safe':
        return 'bg-green-500/20 text-green-400 border-green-500';
      case 'Moderate':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500';
      case 'Ambitious':
        return 'bg-red-500/20 text-red-400 border-red-500';
      default:
        return 'bg-gray-500/20 text-gray-400 border-gray-500';
    }
  };

  const getClassificationIcon = (classification) => {
    switch (classification) {
      case 'Safe':
        return <CheckCircle2 className="w-4 h-4" />;
      case 'Moderate':
        return <AlertCircle className="w-4 h-4" />;
      case 'Ambitious':
        return <Target className="w-4 h-4" />;
      default:
        return null;
    }
  };

  // Home Page
  if (currentStep === 'home') {
    return (
      <div className="min-h-screen bg-dark">
        <div className="container mx-auto px-4 py-16">
          <div className="text-center mb-16 animate-fade-in" data-testid="home-page">
            <div className="flex items-center justify-center mb-6">
              <GraduationCap className="w-20 h-20 text-primary" />
            </div>
            <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent" data-testid="app-title">
              College Admission AI
            </h1>
            <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
              Your intelligent companion for making informed admission decisions. 
              Get personalized college recommendations powered by advanced AI.
            </p>
            <div className="flex items-center justify-center gap-8 mb-12">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                <span className="text-gray-300">AI-Powered Insights</span>
              </div>
              <div className="flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-primary" />
                <span className="text-gray-300">Probability Analysis</span>
              </div>
              <div className="flex items-center gap-2">
                <TrendingUp className="w-5 h-5 text-primary" />
                <span className="text-gray-300">Cutoff Predictions</span>
              </div>
            </div>
            <button
              onClick={() => setCurrentStep('profile')}
              className="bg-gradient-to-r from-primary to-secondary text-dark px-12 py-4 rounded-lg font-bold text-lg hover:shadow-lg hover:shadow-primary/50 transition-all transform hover:scale-105"
              data-testid="get-started-btn"
            >
              Get Started <ArrowUpRight className="inline w-5 h-5 ml-2" />
            </button>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mt-20">
            <div className="bg-dark-light p-8 rounded-xl border border-primary/20 hover:border-primary/50 transition-all">
              <Award className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-xl font-bold mb-2">Smart Recommendations</h3>
              <p className="text-gray-400">Get personalized college suggestions based on your rank, preferences, and budget.</p>
            </div>
            <div className="bg-dark-light p-8 rounded-xl border border-primary/20 hover:border-primary/50 transition-all">
              <TrendingUp className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-xl font-bold mb-2">Admission Probability</h3>
              <p className="text-gray-400">Analyze your chances with historical data and AI-powered probability scoring.</p>
            </div>
            <div className="bg-dark-light p-8 rounded-xl border border-primary/20 hover:border-primary/50 transition-all">
              <MessageCircle className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-xl font-bold mb-2">AI Advisor</h3>
              <p className="text-gray-400">Chat with our AI counselor for personalized guidance and instant answers.</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Profile Input Form
  if (currentStep === 'profile') {
    const totalSteps = 4;
    const progress = (formStep / totalSteps) * 100;

    return (
      <div className="min-h-screen bg-dark py-12">
        <div className="container mx-auto px-4 max-w-3xl">
          {/* Progress Bar */}
          <div className="mb-8" data-testid="profile-form">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-2xl font-bold text-primary">Build Your Profile</h2>
              <span className="text-gray-400">Step {formStep} of {totalSteps}</span>
            </div>
            <div className="w-full bg-dark-light rounded-full h-3">
              <div 
                className="bg-gradient-to-r from-primary to-secondary h-3 rounded-full transition-all duration-500"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>

          <div className="bg-dark-light p-8 rounded-xl border border-primary/20 animate-slide-up">
            {formStep === 1 && (
              <div>
                <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Users className="w-6 h-6 text-primary" />
                  Personal Information
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-gray-300 mb-2">Name *</label>
                    <input
                      type="text"
                      value={profileData.name}
                      onChange={(e) => handleInputChange('name', e.target.value)}
                      className="w-full bg-dark border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-primary focus:outline-none"
                      placeholder="Enter your full name"
                      data-testid="name-input"
                    />
                  </div>
                  <div>
                    <label className="block text-gray-300 mb-2">Email *</label>
                    <input
                      type="email"
                      value={profileData.email}
                      onChange={(e) => handleInputChange('email', e.target.value)}
                      className="w-full bg-dark border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-primary focus:outline-none"
                      placeholder="your.email@example.com"
                      data-testid="email-input"
                    />
                  </div>
                  <div>
                    <label className="block text-gray-300 mb-2">Home State</label>
                    <select
                      value={profileData.home_state}
                      onChange={(e) => handleInputChange('home_state', e.target.value)}
                      className="w-full bg-dark border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-primary focus:outline-none"
                      data-testid="state-select"
                    >
                      <option value="">Select State</option>
                      {indianStates.map(state => (
                        <option key={state} value={state}>{state}</option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>
            )}

            {formStep === 2 && (
              <div>
                <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Award className="w-6 h-6 text-primary" />
                  Exam Details
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-gray-300 mb-2">Exam Type *</label>
                    <div className="grid grid-cols-2 gap-4">
                      {['JEE', 'NEET'].map(exam => (
                        <button
                          key={exam}
                          onClick={() => handleInputChange('exam_type', exam)}
                          className={`py-3 rounded-lg font-semibold transition-all ${
                            profileData.exam_type === exam
                              ? 'bg-primary text-dark'
                              : 'bg-dark border border-gray-600 text-white hover:border-primary'
                          }`}
                          data-testid={`exam-${exam.toLowerCase()}-btn`}
                        >
                          {exam}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="block text-gray-300 mb-2">Your Rank *</label>
                    <input
                      type="number"
                      value={profileData.rank}
                      onChange={(e) => handleInputChange('rank', e.target.value)}
                      className="w-full bg-dark border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-primary focus:outline-none"
                      placeholder="Enter your rank"
                      data-testid="rank-input"
                    />
                  </div>
                  <div>
                    <label className="block text-gray-300 mb-2">Category *</label>
                    <div className="grid grid-cols-4 gap-3">
                      {['General', 'OBC', 'SC', 'ST'].map(cat => (
                        <button
                          key={cat}
                          onClick={() => handleInputChange('category', cat)}
                          className={`py-3 rounded-lg font-semibold transition-all ${
                            profileData.category === cat
                              ? 'bg-primary text-dark'
                              : 'bg-dark border border-gray-600 text-white hover:border-primary'
                          }`}
                          data-testid={`category-${cat.toLowerCase()}-btn`}
                        >
                          {cat}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {formStep === 3 && (
              <div>
                <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Building2 className="w-6 h-6 text-primary" />
                  Preferences
                </h3>
                <div className="space-y-6">
                  <div>
                    <label className="block text-gray-300 mb-3">Preferred Branches * (Select at least 1)</label>
                    <div className="grid grid-cols-2 gap-3 max-h-64 overflow-y-auto">
                      {branches.map(branch => (
                        <button
                          key={branch}
                          onClick={() => toggleArrayField('preferred_branches', branch)}
                          className={`py-2 px-4 rounded-lg font-medium transition-all text-left ${
                            profileData.preferred_branches.includes(branch)
                              ? 'bg-primary text-dark'
                              : 'bg-dark border border-gray-600 text-white hover:border-primary'
                          }`}
                          data-testid={`branch-${branch.toLowerCase().replace(/\s+/g, '-')}-btn`}
                        >
                          {branch}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div>
                    <label className="block text-gray-300 mb-3">Preferred Cities (Optional)</label>
                    <div className="grid grid-cols-3 gap-2 max-h-48 overflow-y-auto">
                      {cities.map(city => (
                        <button
                          key={city}
                          onClick={() => toggleArrayField('preferred_cities', city)}
                          className={`py-2 px-3 rounded-lg text-sm font-medium transition-all ${
                            profileData.preferred_cities.includes(city)
                              ? 'bg-secondary text-dark'
                              : 'bg-dark border border-gray-600 text-white hover:border-secondary'
                          }`}
                          data-testid={`city-${city.toLowerCase().replace(/\s+/g, '-')}-btn`}
                        >
                          {city}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {formStep === 4 && (
              <div>
                <h3 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <DollarSign className="w-6 h-6 text-primary" />
                  Budget
                </h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-gray-300 mb-2">Maximum Budget (4-year total in lakhs)</label>
                    <input
                      type="number"
                      value={profileData.max_budget}
                      onChange={(e) => handleInputChange('max_budget', e.target.value)}
                      className="w-full bg-dark border border-gray-600 rounded-lg px-4 py-3 text-white focus:border-primary focus:outline-none"
                      placeholder="e.g., 10 for ₹10 lakhs"
                      data-testid="budget-input"
                    />
                    <p className="text-gray-400 text-sm mt-2">Leave blank for no budget limit</p>
                  </div>

                  <div className="mt-8 p-6 bg-dark/50 rounded-lg border border-primary/30">
                    <h4 className="font-bold text-lg mb-4 text-primary">Profile Summary</h4>
                    <div className="space-y-2 text-sm">
                      <p><span className="text-gray-400">Name:</span> <span className="text-white font-medium">{profileData.name || 'Not provided'}</span></p>
                      <p><span className="text-gray-400">Email:</span> <span className="text-white font-medium">{profileData.email || 'Not provided'}</span></p>
                      <p><span className="text-gray-400">Rank:</span> <span className="text-white font-medium">{profileData.rank || 'Not provided'}</span></p>
                      <p><span className="text-gray-400">Category:</span> <span className="text-white font-medium">{profileData.category}</span></p>
                      <p><span className="text-gray-400">Branches:</span> <span className="text-white font-medium">{profileData.preferred_branches.length > 0 ? profileData.preferred_branches.join(', ') : 'None selected'}</span></p>
                      <p><span className="text-gray-400">Budget:</span> <span className="text-white font-medium">{profileData.max_budget ? `₹${profileData.max_budget} lakhs` : 'No limit'}</span></p>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Navigation Buttons */}
            <div className="flex justify-between mt-8">
              {formStep > 1 ? (
                <button
                  onClick={() => setFormStep(formStep - 1)}
                  className="px-6 py-3 bg-dark border border-gray-600 text-white rounded-lg hover:border-primary transition-all"
                  data-testid="back-btn"
                >
                  Back
                </button>
              ) : (
                <button
                  onClick={() => setCurrentStep('home')}
                  className="px-6 py-3 bg-dark border border-gray-600 text-white rounded-lg hover:border-primary transition-all"
                  data-testid="home-back-btn"
                >
                  Home
                </button>
              )}

              {formStep < totalSteps ? (
                <button
                  onClick={() => setFormStep(formStep + 1)}
                  className="px-6 py-3 bg-primary text-dark font-bold rounded-lg hover:shadow-lg hover:shadow-primary/50 transition-all"
                  data-testid="next-btn"
                >
                  Next <ChevronRight className="inline w-5 h-5" />
                </button>
              ) : (
                <button
                  onClick={handleSubmitProfile}
                  disabled={loading}
                  className="px-8 py-3 bg-gradient-to-r from-primary to-secondary text-dark font-bold rounded-lg hover:shadow-lg hover:shadow-primary/50 transition-all disabled:opacity-50"
                  data-testid="submit-profile-btn"
                >
                  {loading ? 'Finding Colleges...' : 'Get Recommendations'}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Dashboard
  if (currentStep === 'dashboard') {
    const chartData = {
      labels: recommendations.slice(0, 10).map(r => `${r.college_name.split(' ')[0]} ${r.branch.split(' ')[0]}`),
      datasets: [{
        label: 'Admission Probability (%)',
        data: recommendations.slice(0, 10).map(r => r.probability),
        backgroundColor: recommendations.slice(0, 10).map(r => {
          if (r.classification === 'Safe') return 'rgba(34, 197, 94, 0.6)';
          if (r.classification === 'Moderate') return 'rgba(234, 179, 8, 0.6)';
          return 'rgba(239, 68, 68, 0.6)';
        }),
        borderColor: recommendations.slice(0, 10).map(r => {
          if (r.classification === 'Safe') return 'rgb(34, 197, 94)';
          if (r.classification === 'Moderate') return 'rgb(234, 179, 8)';
          return 'rgb(239, 68, 68)';
        }),
        borderWidth: 2
      }]
    };

    const chartOptions = {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: { display: true, text: 'Top 10 Recommendations by Probability', color: '#fff' }
      },
      scales: {
        y: { 
          beginAtZero: true, 
          max: 100,
          ticks: { color: '#9ca3af' },
          grid: { color: '#1e2442' }
        },
        x: { 
          ticks: { color: '#9ca3af' },
          grid: { color: '#1e2442' }
        }
      }
    };

    return (
      <div className="min-h-screen bg-dark py-8">
        <div className="container mx-auto px-4">
          {/* Header */}
          <div className="mb-8 flex justify-between items-center" data-testid="dashboard-page">
            <div>
              <h1 className="text-4xl font-bold text-primary mb-2">Your Recommendations</h1>
              <p className="text-gray-400">Based on your profile: Rank {profileData.rank} • {profileData.category} • {profileData.preferred_branches[0]}</p>
            </div>
            <button
              onClick={() => setCurrentStep('profile')}
              className="px-6 py-3 bg-dark-light border border-primary text-primary rounded-lg hover:bg-primary hover:text-dark transition-all"
              data-testid="edit-profile-btn"
            >
              Edit Profile
            </button>
          </div>

          {/* Summary Cards */}
          {summary && (
            <div className="grid md:grid-cols-3 gap-6 mb-8">
              <div className="bg-gradient-to-br from-green-500/20 to-green-600/10 p-6 rounded-xl border border-green-500/30">
                <div className="flex items-center justify-between mb-2">
                  <CheckCircle2 className="w-8 h-8 text-green-400" />
                  <span className="text-3xl font-bold text-green-400">{summary.safe}</span>
                </div>
                <h3 className="text-white font-bold">Safe Colleges</h3>
                <p className="text-gray-400 text-sm">High admission probability</p>
              </div>
              <div className="bg-gradient-to-br from-yellow-500/20 to-yellow-600/10 p-6 rounded-xl border border-yellow-500/30">
                <div className="flex items-center justify-between mb-2">
                  <AlertCircle className="w-8 h-8 text-yellow-400" />
                  <span className="text-3xl font-bold text-yellow-400">{summary.moderate}</span>
                </div>
                <h3 className="text-white font-bold">Moderate Colleges</h3>
                <p className="text-gray-400 text-sm">Good chances</p>
              </div>
              <div className="bg-gradient-to-br from-red-500/20 to-red-600/10 p-6 rounded-xl border border-red-500/30">
                <div className="flex items-center justify-between mb-2">
                  <Target className="w-8 h-8 text-red-400" />
                  <span className="text-3xl font-bold text-red-400">{summary.ambitious}</span>
                </div>
                <h3 className="text-white font-bold">Ambitious Colleges</h3>
                <p className="text-gray-400 text-sm">Reach options</p>
              </div>
            </div>
          )}

          {/* Chart */}
          <div className="bg-dark-light p-6 rounded-xl border border-primary/20 mb-8">
            <Bar data={chartData} options={chartOptions} />
          </div>

          {/* Comparison Button */}
          {selectedForComparison.length >= 2 && (
            <div className="fixed bottom-8 right-8 z-50">
              <button
                onClick={handleCompare}
                className="bg-gradient-to-r from-primary to-secondary text-dark px-8 py-4 rounded-full font-bold shadow-2xl shadow-primary/50 hover:scale-110 transition-all flex items-center gap-2"
                data-testid="compare-selected-btn"
              >
                <BarChart3 className="w-5 h-5" />
                Compare ({selectedForComparison.length})
              </button>
            </div>
          )}

          {/* College Cards */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recommendations.map((rec, index) => (
              <div
                key={index}
                className="bg-dark-light p-6 rounded-xl border border-primary/20 hover:border-primary/50 transition-all hover:shadow-xl hover:shadow-primary/10 animate-slide-up"
                style={{ animationDelay: `${index * 0.05}s` }}
                data-testid={`college-card-${index}`}
              >
                {/* College Header */}
                <div className="flex justify-between items-start mb-4">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="text-xs px-2 py-1 bg-primary/20 text-primary rounded">{rec.type}</span>
                      {rec.nirf_rank && (
                        <span className="text-xs px-2 py-1 bg-secondary/20 text-secondary rounded">
                          NIRF #{rec.nirf_rank}
                        </span>
                      )}
                    </div>
                    <h3 className="text-xl font-bold text-white mb-1">{rec.college_name}</h3>
                    <p className="text-primary font-semibold">{rec.branch}</p>
                  </div>
                  <button
                    onClick={() => toggleWishlist(rec.college_id)}
                    className="text-gray-400 hover:text-red-500 transition-colors"
                    data-testid={`wishlist-btn-${index}`}
                  >
                    <Heart className={`w-6 h-6 ${wishlist.includes(rec.college_id) ? 'fill-red-500 text-red-500' : ''}`} />
                  </button>
                </div>

                {/* Probability Badge */}
                <div className="mb-4">
                  <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full border-2 ${getClassificationColor(rec.classification)}`}>
                    {getClassificationIcon(rec.classification)}
                    <span className="font-bold">{rec.probability}% - {rec.classification}</span>
                  </div>
                </div>

                {/* Location & Fees */}
                <div className="space-y-2 mb-4 text-sm">
                  <div className="flex items-center gap-2 text-gray-300">
                    <MapPin className="w-4 h-4 text-primary" />
                    <span>{rec.location}, {rec.state}</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-300">
                    <DollarSign className="w-4 h-4 text-primary" />
                    <span>₹{rec.total_fees}L total (₹{rec.fees_per_year}L/year)</span>
                  </div>
                  <div className="flex items-center gap-2 text-gray-300">
                    <TrendingUp className="w-4 h-4 text-primary" />
                    <span>Avg Package: ₹{rec.placement_avg}L</span>
                  </div>
                </div>

                {/* AI Insight */}
                <div className="bg-dark/50 p-3 rounded-lg mb-4 border border-primary/10">
                  <div className="flex items-start gap-2">
                    <Sparkles className="w-4 h-4 text-primary mt-1 flex-shrink-0" />
                    <p className="text-xs text-gray-300 leading-relaxed">{rec.ai_insight}</p>
                  </div>
                </div>

                {/* Cutoff Info */}
                <div className="text-xs text-gray-400 mb-4">
                  <p>Last Year Closing: <span className="text-white font-semibold">{rec.last_year_closing}</span></p>
                  {rec.predicted_cutoff.predicted_closing && (
                    <p className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      Predicted {rec.predicted_cutoff.year}: <span className="text-primary font-semibold">{rec.predicted_cutoff.predicted_closing}</span>
                      <span className="text-gray-500">({rec.predicted_cutoff.confidence} confidence)</span>
                    </p>
                  )}
                </div>

                {/* Actions */}
                <div className="flex gap-2">
                  <button
                    onClick={() => toggleComparison(rec.college_id)}
                    className={`flex-1 py-2 px-4 rounded-lg font-medium transition-all ${
                      selectedForComparison.includes(rec.college_id)
                        ? 'bg-primary text-dark'
                        : 'bg-dark border border-gray-600 text-white hover:border-primary'
                    }`}
                    data-testid={`select-compare-btn-${index}`}
                  >
                    {selectedForComparison.includes(rec.college_id) ? 'Selected' : 'Compare'}
                  </button>
                  <button
                    onClick={() => {
                      setSelectedCollege(rec);
                      fetchBranchRoadmap(rec.branch);
                    }}
                    className="py-2 px-4 bg-secondary/20 text-secondary rounded-lg hover:bg-secondary hover:text-dark transition-all font-medium"
                    data-testid={`roadmap-btn-${index}`}
                  >
                    Roadmap
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Floating Chat Button */}
        <button
          onClick={() => setShowChat(!showChat)}
          className="fixed bottom-8 left-8 bg-gradient-to-r from-primary to-secondary text-dark p-4 rounded-full shadow-2xl hover:scale-110 transition-all z-50"
          data-testid="chat-toggle-btn"
        >
          <MessageCircle className="w-6 h-6" />
        </button>

        {/* Chat Widget */}
        {showChat && (
          <div className="fixed bottom-24 left-8 w-96 h-[500px] bg-dark-light border-2 border-primary rounded-xl shadow-2xl z-50 flex flex-col" data-testid="chat-widget">
            <div className="bg-gradient-to-r from-primary to-secondary text-dark p-4 rounded-t-xl flex justify-between items-center">
              <h3 className="font-bold flex items-center gap-2">
                <MessageCircle className="w-5 h-5" />
                AI Advisor
              </h3>
              <button onClick={() => setShowChat(false)} data-testid="chat-close-btn">
                <X className="w-5 h-5" />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {chatMessages.length === 0 && (
                <div className="text-center text-gray-400 mt-8">
                  <p>Ask me anything about college admissions!</p>
                  <p className="text-sm mt-2">e.g., "Which college is best for robotics in South India?"</p>
                </div>
              )}
              {chatMessages.map((msg, i) => (
                <div
                  key={i}
                  className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-lg ${
                      msg.role === 'user'
                        ? 'bg-primary text-dark'
                        : 'bg-dark border border-gray-600 text-white'
                    }`}
                    data-testid={`chat-message-${i}`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
            </div>
            <div className="p-4 border-t border-gray-600">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendChatMessage()}
                  placeholder="Type your question..."
                  className="flex-1 bg-dark border border-gray-600 rounded-lg px-4 py-2 text-white focus:border-primary focus:outline-none"
                  data-testid="chat-input"
                />
                <button
                  onClick={sendChatMessage}
                  className="bg-primary text-dark p-2 rounded-lg hover:shadow-lg hover:shadow-primary/50 transition-all"
                  data-testid="chat-send-btn"
                >
                  <Send className="w-5 h-5" />
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Branch Roadmap Modal */}
        {selectedCollege && branchRoadmap && (
          <div className="fixed inset-0 bg-black/80 flex items-center justify-center z-50 p-4" onClick={() => { setSelectedCollege(null); setBranchRoadmap(null); }}>
            <div className="bg-dark-light border-2 border-primary rounded-xl p-8 max-w-2xl w-full" onClick={(e) => e.stopPropagation()} data-testid="roadmap-modal">
              <div className="flex justify-between items-start mb-6">
                <div>
                  <h3 className="text-2xl font-bold text-primary mb-2">{selectedCollege.branch} Career Roadmap</h3>
                  <p className="text-gray-400">{selectedCollege.college_name}</p>
                </div>
                <button onClick={() => { setSelectedCollege(null); setBranchRoadmap(null); }} data-testid="roadmap-close-btn">
                  <X className="w-6 h-6 text-gray-400 hover:text-white" />
                </button>
              </div>
              <div className="bg-dark p-6 rounded-lg border border-primary/20">
                <p className="text-gray-300 whitespace-pre-line leading-relaxed">{branchRoadmap.roadmap}</p>
              </div>
              <div className="mt-6 p-4 bg-primary/10 rounded-lg border border-primary/30">
                <p className="text-sm text-gray-400">
                  💡 <span className="text-primary font-semibold">Pro Tip:</span> Start building relevant skills early and participate in internships to maximize your career opportunities.
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // Comparison Page
  if (currentStep === 'comparison') {
    return (
      <div className="min-h-screen bg-dark py-8">
        <div className="container mx-auto px-4">
          <div className="mb-8 flex justify-between items-center" data-testid="comparison-page">
            <h1 className="text-4xl font-bold text-primary">College Comparison</h1>
            <button
              onClick={() => setCurrentStep('dashboard')}
              className="px-6 py-3 bg-dark-light border border-primary text-primary rounded-lg hover:bg-primary hover:text-dark transition-all"
              data-testid="back-to-dashboard-btn"
            >
              Back to Dashboard
            </button>
          </div>

          <div className="bg-dark-light rounded-xl border border-primary/20 overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-600">
                  <th className="p-4 text-left text-gray-400 font-semibold sticky left-0 bg-dark-light z-10">Attribute</th>
                  {comparisonData.map((college, i) => (
                    <th key={i} className="p-4 text-center min-w-[250px]" data-testid={`comparison-college-${i}`}>
                      <div className="text-white font-bold text-lg mb-1">{college.name}</div>
                      <div className="text-primary text-sm">{college.location}</div>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Type</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center">
                      <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">{c.type}</span>
                    </td>
                  ))}
                </tr>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">NIRF Rank</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center text-white">#{c.nirf_rank || 'N/A'}</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Fees (4 years)</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center text-white">₹{c.total_fees}L</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Avg Placement</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center text-green-400 font-semibold">₹{c.placement_avg}L</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Highest Placement</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center text-primary font-semibold">₹{c.placement_highest}Cr</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Facilities Rating</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center">
                      <div className="flex items-center justify-center gap-1">
                        <Star className="w-4 h-4 text-yellow-400 fill-yellow-400" />
                        <span className="text-white font-semibold">{c.facilities_rating}/10</span>
                      </div>
                    </td>
                  ))}
                </tr>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Campus Size</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center text-white">{c.campus_size}</td>
                  ))}
                </tr>
                <tr className="border-b border-gray-700">
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Branches Offered</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center text-gray-400 text-sm">{c.branches.length} branches</td>
                  ))}
                </tr>
                <tr>
                  <td className="p-4 font-semibold text-gray-300 sticky left-0 bg-dark-light">Notable Alumni</td>
                  {comparisonData.map((c, i) => (
                    <td key={i} className="p-4 text-center text-gray-400 text-sm">{c.notable_alumni.slice(0, 2).join(', ')}</td>
                  ))}
                </tr>
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
