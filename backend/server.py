from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
import os
from dotenv import load_dotenv
import numpy as np
from sklearn.linear_model import LinearRegression
import asyncio
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Load environment variables
load_dotenv()

# Initialize FastAPI
app = FastAPI(title="College Admission AI Platform")

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Connection
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017/college_admission")
client = MongoClient(MONGO_URL)
db = client["college_admission"]

# Collections
colleges_collection = db["colleges"]
profiles_collection = db["student_profiles"]
wishlists_collection = db["wishlists"]
chat_history_collection = db["chat_history"]

# LLM Configuration
EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

# ==================== MODELS ====================

class StudentProfile(BaseModel):
    rank: int
    exam_type: str  # "JEE" or "NEET"
    category: str  # "General", "OBC", "SC", "ST"
    home_state: str
    preferred_branches: List[str]
    preferred_cities: List[str]
    max_budget: float  # in lakhs
    name: Optional[str] = None
    email: Optional[str] = None

class College(BaseModel):
    name: str
    location: str
    state: str
    type: str  # "IIT", "NIT", "IIIT", "GFTI"
    nirf_rank: Optional[int] = None
    branches: List[str]
    fees_per_year: float  # in lakhs
    hostel_fees: float  # in lakhs
    total_fees: float  # 4 year total
    placement_avg: float  # in lakhs
    placement_highest: float
    facilities_rating: float
    campus_size: str
    notable_alumni: List[str]
    historical_cutoffs: List[Dict[str, Any]]  # year, branch, category, opening_rank, closing_rank

class RecommendationRequest(BaseModel):
    profile: StudentProfile

class CompareRequest(BaseModel):
    college_ids: List[str]

class WishlistRequest(BaseModel):
    student_email: str
    college_id: str

class ChatRequest(BaseModel):
    message: str
    session_id: str
    student_profile: Optional[Dict[str, Any]] = None

# ==================== HELPER FUNCTIONS ====================

def calculate_admission_probability(student_rank: int, cutoff_data: Dict[str, Any], category: str) -> float:
    """Calculate admission probability based on historical cutoffs"""
    try:
        category_cutoffs = [c for c in cutoff_data if c.get('category') == category]
        if not category_cutoffs:
            return 0.0
        
        # Get last 3 years average closing rank
        recent_cutoffs = sorted(category_cutoffs, key=lambda x: x['year'], reverse=True)[:3]
        avg_closing = np.mean([c['closing_rank'] for c in recent_cutoffs])
        avg_opening = np.mean([c['opening_rank'] for c in recent_cutoffs])
        
        # Calculate probability
        if student_rank <= avg_opening:
            return 95.0
        elif student_rank <= avg_closing:
            # Linear interpolation
            prob = 95 - ((student_rank - avg_opening) / (avg_closing - avg_opening)) * 50
            return max(prob, 45.0)
        elif student_rank <= avg_closing * 1.1:
            return 35.0
        elif student_rank <= avg_closing * 1.2:
            return 20.0
        else:
            return 5.0
    except:
        return 0.0

def classify_admission_chance(probability: float) -> str:
    """Classify admission chance into Safe/Moderate/Ambitious"""
    if probability >= 70:
        return "Safe"
    elif probability >= 40:
        return "Moderate"
    else:
        return "Ambitious"

def predict_next_year_cutoff(historical_data: List[Dict[str, Any]], category: str) -> Dict[str, Any]:
    """Predict next year's cutoff using linear regression"""
    try:
        category_data = [d for d in historical_data if d.get('category') == category]
        if len(category_data) < 3:
            return {"predicted_closing": None, "confidence": "Low"}
        
        years = np.array([d['year'] for d in category_data]).reshape(-1, 1)
        closing_ranks = np.array([d['closing_rank'] for d in category_data])
        
        model = LinearRegression()
        model.fit(years, closing_ranks)
        
        next_year = np.array([[max(years)[0] + 1]])
        predicted = model.predict(next_year)[0]
        
        # Calculate confidence based on R² score
        r2_score = model.score(years, closing_ranks)
        confidence = "High" if r2_score > 0.8 else "Medium" if r2_score > 0.5 else "Low"
        
        return {
            "predicted_closing": int(predicted),
            "confidence": confidence,
            "year": int(next_year[0][0])
        }
    except:
        return {"predicted_closing": None, "confidence": "Low"}

async def generate_ai_insight(college_name: str, branch: str, probability: float, 
                               student_rank: int, category: str, closing_rank: int) -> str:
    """Generate personalized AI insight using GPT-5.2"""
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"insight_{datetime.now().timestamp()}",
            system_message="You are an expert college admission counselor. Provide brief, personalized insights."
        ).with_model("openai", "gpt-5.2")
        
        prompt = f"""Generate a 2-3 sentence personalized admission insight for:
College: {college_name}
Branch: {branch}
Student Rank: {student_rank}
Category: {category}
Admission Probability: {probability:.1f}%
Last Year Closing Rank: {closing_rank}

Make it encouraging, data-driven, and actionable."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        return response
    except Exception as e:
        return f"Based on your rank of {student_rank} and {category} category, you have a {probability:.1f}% chance. Last year's closing rank was {closing_rank}."

async def generate_branch_roadmap(branch: str) -> str:
    """Generate AI-powered branch career roadmap"""
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"roadmap_{datetime.now().timestamp()}",
            system_message="You are a career counselor expert. Provide concise career roadmaps."
        ).with_model("openai", "gpt-5.2")
        
        prompt = f"""Create a brief career roadmap for {branch} engineering:
- Top 3 career roles
- Top 5 recruiting companies
- Average package range
- Key skills to develop
Keep it under 150 words."""
        
        user_message = UserMessage(text=prompt)
        response = await chat.send_message(user_message)
        return response
    except Exception as e:
        return f"Career opportunities in {branch} include roles in software development, research, and core engineering positions."

# ==================== API ENDPOINTS ====================

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "College Admission AI Platform is running"}

@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """Get personalized college recommendations"""
    try:
        profile = request.profile
        
        # Find matching colleges - broad query first
        query = {
            "branches": {"$in": profile.preferred_branches}
        }
        
        # Only apply budget filter if budget is set and reasonable
        if profile.max_budget and profile.max_budget > 0:
            query["total_fees"] = {"$lte": profile.max_budget}
        
        # Try with city filter first, fall back to all colleges if no results
        if profile.preferred_cities and len(profile.preferred_cities) > 0:
            city_query = {**query, "location": {"$in": profile.preferred_cities}}
            colleges = list(colleges_collection.find(city_query).limit(30))
            # If no results with city filter, search all colleges
            if not colleges:
                colleges = list(colleges_collection.find(query).limit(30))
        else:
            colleges = list(colleges_collection.find(query).limit(30))
        
        recommendations = []
        
        for college in colleges:
            for branch in profile.preferred_branches:
                if branch not in college.get('branches', []):
                    continue
                
                # Get cutoff data for this branch
                branch_cutoffs = [c for c in college.get('historical_cutoffs', []) 
                                  if c.get('branch') == branch]
                
                if not branch_cutoffs:
                    continue
                
                # Calculate probability
                probability = calculate_admission_probability(
                    profile.rank, branch_cutoffs, profile.category
                )
                
                if probability < 5:
                    continue
                
                # Get last year's closing rank
                latest_cutoff = max(branch_cutoffs, key=lambda x: x['year'])
                category_cutoff = next((c for c in branch_cutoffs 
                                       if c['year'] == latest_cutoff['year'] 
                                       and c['category'] == profile.category), None)
                
                closing_rank = category_cutoff['closing_rank'] if category_cutoff else 0
                
                # Predict next year cutoff
                prediction = predict_next_year_cutoff(branch_cutoffs, profile.category)
                
                recommendations.append({
                    "college_id": str(college['_id']),
                    "college_name": college['name'],
                    "location": college['location'],
                    "state": college['state'],
                    "branch": branch,
                    "type": college['type'],
                    "nirf_rank": college.get('nirf_rank'),
                    "fees_per_year": college['fees_per_year'],
                    "total_fees": college['total_fees'],
                    "hostel_fees": college['hostel_fees'],
                    "placement_avg": college['placement_avg'],
                    "placement_highest": college['placement_highest'],
                    "probability": round(probability, 1),
                    "classification": classify_admission_chance(probability),
                    "last_year_closing": closing_rank,
                    "ai_insight": f"Based on your rank of {profile.rank} ({profile.category} category), you have a {probability:.1f}% chance at {college['name']} {branch}. Last year's closing rank was {closing_rank}.",
                    "predicted_cutoff": prediction,
                    "historical_trend": branch_cutoffs[-3:] if len(branch_cutoffs) >= 3 else branch_cutoffs
                })
        
        # Sort by probability
        recommendations.sort(key=lambda x: x['probability'], reverse=True)
        top_recs = recommendations[:15]
        
        # Generate AI insights asynchronously for top recommendations (limit to 5 for speed)
        async def enrich_insight(rec):
            try:
                insight = await generate_ai_insight(
                    rec['college_name'], rec['branch'], rec['probability'],
                    profile.rank, profile.category, rec['last_year_closing']
                )
                rec['ai_insight'] = insight
            except:
                pass
        
        # Only generate AI insights for top 5 to keep response fast
        tasks = [enrich_insight(rec) for rec in top_recs[:5]]
        await asyncio.gather(*tasks)
        
        # Save profile
        profile_dict = profile.dict()
        profile_dict['created_at'] = datetime.now()
        profiles_collection.insert_one(profile_dict)
        
        return {
            "success": True,
            "recommendations": top_recs,
            "summary": {
                "safe": len([r for r in top_recs if r['classification'] == 'Safe']),
                "moderate": len([r for r in top_recs if r['classification'] == 'Moderate']),
                "ambitious": len([r for r in top_recs if r['classification'] == 'Ambitious'])
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/compare")
async def compare_colleges(request: CompareRequest):
    """Compare multiple colleges side-by-side"""
    try:
        from bson import ObjectId
        colleges = []
        
        for college_id in request.college_ids[:3]:
            college = colleges_collection.find_one({"_id": ObjectId(college_id)})
            if college:
                college['_id'] = str(college['_id'])
                colleges.append(college)
        
        return {"success": True, "colleges": colleges}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/wishlist/add")
async def add_to_wishlist(request: WishlistRequest):
    """Add college to wishlist"""
    try:
        wishlist_entry = {
            "student_email": request.student_email,
            "college_id": request.college_id,
            "added_at": datetime.now()
        }
        
        # Check if already exists
        exists = wishlists_collection.find_one({
            "student_email": request.student_email,
            "college_id": request.college_id
        })
        
        if exists:
            return {"success": True, "message": "Already in wishlist"}
        
        wishlists_collection.insert_one(wishlist_entry)
        return {"success": True, "message": "Added to wishlist"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/wishlist/{student_email}")
async def get_wishlist(student_email: str):
    """Get student's wishlist"""
    try:
        from bson import ObjectId
        wishlist_items = list(wishlists_collection.find({"student_email": student_email}))
        
        colleges = []
        for item in wishlist_items:
            college = colleges_collection.find_one({"_id": ObjectId(item['college_id'])})
            if college:
                college['_id'] = str(college['_id'])
                colleges.append(college)
        
        return {"success": True, "wishlist": colleges}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/wishlist/remove")
async def remove_from_wishlist(request: WishlistRequest):
    """Remove college from wishlist"""
    try:
        wishlists_collection.delete_one({
            "student_email": request.student_email,
            "college_id": request.college_id
        })
        return {"success": True, "message": "Removed from wishlist"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/branch-roadmap/{branch}")
async def get_branch_roadmap(branch: str):
    """Get AI-generated career roadmap for a branch"""
    try:
        roadmap = await generate_branch_roadmap(branch)
        return {"success": True, "branch": branch, "roadmap": roadmap}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat_with_ai(request: ChatRequest):
    """Conversational AI advisor"""
    try:
        # Get chat history
        history = list(chat_history_collection.find(
            {"session_id": request.session_id}
        ).sort("timestamp", 1).limit(10))
        
        # Build context
        context = "You are an expert college admission counselor for JEE/NEET students in India."
        if request.student_profile:
            profile = request.student_profile
            context += f"\nStudent Profile: Rank {profile.get('rank')}, Category: {profile.get('category')}, Preferred branches: {', '.join(profile.get('preferred_branches', []))}"
        
        # Initialize chat
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=request.session_id,
            system_message=context
        ).with_model("openai", "gpt-5.2")
        
        user_message = UserMessage(text=request.message)
        response = await chat.send_message(user_message)
        
        # Save to history
        chat_history_collection.insert_one({
            "session_id": request.session_id,
            "user_message": request.message,
            "ai_response": response,
            "timestamp": datetime.now()
        })
        
        return {"success": True, "response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/colleges/search")
async def search_colleges(
    name: Optional[str] = None,
    location: Optional[str] = None,
    branch: Optional[str] = None,
    max_fees: Optional[float] = None
):
    """Search and filter colleges"""
    try:
        query = {}
        
        if name:
            query["name"] = {"$regex": name, "$options": "i"}
        if location:
            query["location"] = {"$regex": location, "$options": "i"}
        if branch:
            query["branches"] = branch
        if max_fees:
            query["total_fees"] = {"$lte": max_fees}
        
        colleges = list(colleges_collection.find(query).limit(50))
        
        for college in colleges:
            college['_id'] = str(college['_id'])
        
        return {"success": True, "colleges": colleges}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
