# AI-Powered College Admission Intelligence Platform 🎓

A comprehensive, AI-powered platform that helps JEE/NEET students make informed college admission decisions through intelligent recommendations, probability analysis, and personalized insights.

## 🌟 Features

### Core Features
- **Smart Profile Input** - Multi-step form with progress tracking
- **AI Recommendation Engine** - Probability-based college suggestions with historical cutoff analysis
- **Interactive Dashboard** - Visual representation of admission chances with charts
- **College Comparison** - Side-by-side comparison of up to 3 colleges
- **Wishlist Management** - Save and track favorite colleges

### Advanced Features
- **Conversational AI Advisor** - Chat with AI counselor for personalized guidance
- **Cutoff Predictions** - ML-powered predictions for next year's cutoffs using linear regression
- **Branch Career Roadmap** - AI-generated career paths for each engineering branch
- **Probability Classification** - Safe/Moderate/Ambitious categorization
- **Historical Trend Analysis** - Visual trends of past cutoffs

## 🛠️ Tech Stack

- **Frontend**: React 18, Tailwind CSS, Chart.js, Axios
- **Backend**: FastAPI, Python 3.11
- **Database**: MongoDB
- **AI**: OpenAI GPT-5.2 (via Emergent Universal LLM Key)
- **Data Analysis**: NumPy, Scikit-learn, Scipy

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 16+
- MongoDB
- Yarn package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd <project-directory>
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
```

3. **Frontend Setup**
```bash
cd frontend
yarn install
```

4. **Environment Variables**

Backend (.env):
```
MONGO_URL=mongodb://localhost:27017/college_admission
EMERGENT_LLM_KEY=your_key_here
```

Frontend (.env):
```
REACT_APP_BACKEND_URL=http://localhost:8001
```

5. **Seed Database**
```bash
python scripts/seed_data.py
```

6. **Run the Application**

Backend:
```bash
cd backend
python server.py
```

Frontend:
```bash
cd frontend
yarn start
```

## 📊 Database

The platform includes data for:
- **25+ colleges** (IITs, NITs, IIITs)
- **Historical cutoffs** (2020-2024)
- **NIRF rankings**
- **Placement statistics**
- **Fee structures**

## 🎯 Key Algorithms

### Admission Probability Calculation
- Compares student rank with 3-year average historical cutoffs
- Considers category-specific data
- Linear interpolation for probability scoring
- 95% probability for ranks within opening rank
- Sliding scale between opening and closing ranks

### Cutoff Prediction
- Linear regression on 3+ years of historical data
- Confidence scoring based on R² score
- Year-over-year trend analysis

### AI Integration
- Personalized insights for each recommendation
- Conversational AI advisor with context awareness
- Branch-specific career roadmaps
- Natural language query processing

## 🎨 UI/UX Highlights

- **Dark Theme** - Cyberpunk-inspired with cyan/green accents
- **Smooth Animations** - Count-up effects, slide-ups, fade-ins
- **Loading Skeletons** - Shimmer effects during data fetching
- **Color-Coded Badges** - Visual classification (Safe/Moderate/Ambitious)
- **Responsive Design** - Mobile-friendly interface
- **Interactive Charts** - Bar charts for probability visualization

## 📱 User Flow

1. **Home Page** - Introduction and feature overview
2. **Profile Building** - 4-step form with progress bar
   - Personal Information
   - Exam Details (Rank, Category)
   - Branch & Location Preferences
   - Budget Configuration
3. **Dashboard** - Personalized recommendations with:
   - Summary cards (Safe/Moderate/Ambitious counts)
   - Probability bar chart
   - College cards with AI insights
   - Comparison selection
   - Wishlist management
4. **Comparison View** - Detailed side-by-side analysis
5. **AI Chat** - Floating chat widget for queries
6. **Branch Roadmap** - Career guidance modal

## 🔧 API Endpoints

- `GET /api/health` - Health check
- `POST /api/recommendations` - Get personalized recommendations
- `POST /api/compare` - Compare selected colleges
- `POST /api/wishlist/add` - Add to wishlist
- `POST /api/wishlist/remove` - Remove from wishlist
- `GET /api/wishlist/{email}` - Get user wishlist
- `POST /api/chat` - AI chat conversation
- `GET /api/branch-roadmap/{branch}` - Get career roadmap
- `GET /api/colleges/search` - Search and filter colleges

## 🏆 Hackathon Winning Features

1. **Real-time AI Insights** - Every recommendation comes with personalized AI analysis
2. **Predictive Analytics** - ML-based cutoff predictions
3. **Conversational Interface** - Natural language chat for queries
4. **Visual Excellence** - Stunning dark theme with smooth animations
5. **Comprehensive Data** - 25+ colleges with 5 years of historical data
6. **Smart Classification** - Intelligent Safe/Moderate/Ambitious categorization
7. **Career Guidance** - AI-generated branch-specific roadmaps

## 📈 Future Enhancements

- Real-time notifications for cutoff changes
- Email alerts system
- More colleges and universities
- State quota analysis
- Hostel and campus life ratings
- Student reviews and testimonials
- Mobile app development

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License

## 👥 Team

Built with ❤️ for hackathon participants

## 📞 Support

For issues and queries, please open an issue on GitHub.

---

**Made for helping students make better admission decisions through AI-powered insights! 🚀**