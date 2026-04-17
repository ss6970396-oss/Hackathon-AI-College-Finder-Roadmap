# College Admission AI Platform - PRD

## Original Problem Statement
Build an AI-Powered College Admission Intelligence Platform - a web-based platform helping JEE/NEET students make informed admission decisions by analyzing their profile and matching it with college data. Features include Student Profile Input, AI Recommendation Engine, Interactive Dashboard, College Comparison, Wishlist, AI Chat Advisor, Cutoff Predictions, and Branch Career Roadmap.

## Architecture
- **Frontend**: React 18 + Tailwind CSS (dark theme) + Chart.js + Lucide React
- **Backend**: FastAPI (Python 3.11) + MongoDB
- **AI**: OpenAI GPT-5.2 via Emergent Universal LLM Key
- **ML**: Scikit-learn (linear regression for cutoff predictions)
- **Database**: MongoDB with 25 colleges, historical cutoffs (2020-2024)

## User Personas
1. **JEE Student** - Rank 1-50000, seeking IIT/NIT/IIIT admission guidance
2. **NEET Student** - Seeking medical college recommendations
3. **Parent** - Exploring affordable options within budget
4. **Counselor** - Using tool to advise multiple students

## Core Requirements (Static)
- Student profile input with multi-step form
- AI-powered recommendation engine with probability scoring
- Safe/Moderate/Ambitious classification
- Historical cutoff comparison
- Budget and location filtering
- College comparison tool
- Wishlist management
- Conversational AI advisor
- Cutoff predictions using ML
- Branch career roadmap

## What's Been Implemented (Jan 2026)
- ✅ Complete 4-step profile form with progress bar
- ✅ AI Recommendation Engine (probability scoring, Safe/Moderate/Ambitious)
- ✅ Interactive Dashboard with bar charts, summary cards, college cards
- ✅ College Comparison Tool (side-by-side, up to 3 colleges)
- ✅ Wishlist feature with heart toggle
- ✅ Conversational AI Chat (GPT-5.2, floating widget)
- ✅ Cutoff Predictions (linear regression with confidence scoring)
- ✅ Branch Career Roadmap (AI-generated)
- ✅ 25 colleges seeded (IITs, NITs, IIITs)
- ✅ Dark theme with cyan/green accents
- ✅ All APIs tested - 100% pass rate (19/19 backend tests)
- ✅ Frontend flows all working - 100% success

## Bug Fix: Wrong REACT_APP_BACKEND_URL
- Fixed frontend .env URL from incorrect domain to correct preview URL
- Fixed recommendation query to be less restrictive (budget filter, city fallback)
- Made AI insights async (parallel for top 5) for faster response times

## Prioritized Backlog

### P0 (Critical) - Done
- ✅ All core features implemented and tested

### P1 (High Priority)
- Add more colleges (100+ target)
- Add Electronics/Mechanical branch cutoff data for more colleges
- State quota analysis
- Email notification system

### P2 (Medium Priority)
- Student authentication/login
- Save/load profile functionality
- Export recommendations as PDF
- Historical trend line chart per college
- Budget vs Fee scatter plot

### P3 (Low Priority)
- Real-time JoSAA cutoff tracking
- Student reviews & testimonials
- Mobile app development
- Social sharing features
- Hostel and campus life ratings

## Next Tasks
1. Add more comprehensive historical cutoff data for all categories
2. Add more colleges (60+ target from current 25)
3. Implement historical trend line chart
4. Add budget scatter plot visualization
5. Polish UI animations and loading states
