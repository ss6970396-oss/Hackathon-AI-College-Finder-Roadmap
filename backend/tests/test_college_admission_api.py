"""
Backend API Tests for College Admission AI Platform
Tests: Health, Recommendations, Compare, Wishlist, Chat, Branch Roadmap, College Search
"""
import pytest
import requests
import os
import time

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test profile data
TEST_PROFILE = {
    "rank": 5000,
    "exam_type": "JEE",
    "category": "General",
    "home_state": "Maharashtra",
    "preferred_branches": ["Computer Science"],
    "preferred_cities": [],
    "max_budget": 15,
    "name": "Test User",
    "email": "test@example.com"
}

class TestHealthEndpoint:
    """Health check endpoint tests"""
    
    def test_health_returns_200(self):
        """Test /api/health returns 200 and healthy status"""
        response = requests.get(f"{BASE_URL}/api/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "message" in data
        print(f"✓ Health check passed: {data['message']}")


class TestRecommendationsEndpoint:
    """Recommendations endpoint tests"""
    
    def test_recommendations_returns_200(self):
        """Test /api/recommendations returns 200 with valid profile"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "recommendations" in data
        assert "summary" in data
        print(f"✓ Recommendations returned: {len(data['recommendations'])} colleges")
    
    def test_recommendations_has_probability_scores(self):
        """Test recommendations include probability scores and classification"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE}
        )
        assert response.status_code == 200
        data = response.json()
        
        if len(data["recommendations"]) > 0:
            rec = data["recommendations"][0]
            assert "probability" in rec
            assert "classification" in rec
            assert rec["classification"] in ["Safe", "Moderate", "Ambitious"]
            assert 0 <= rec["probability"] <= 100
            print(f"✓ First recommendation: {rec['college_name']} - {rec['probability']}% ({rec['classification']})")
    
    def test_recommendations_summary_counts(self):
        """Test summary contains Safe/Moderate/Ambitious counts"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE}
        )
        assert response.status_code == 200
        data = response.json()
        
        summary = data["summary"]
        assert "safe" in summary
        assert "moderate" in summary
        assert "ambitious" in summary
        assert isinstance(summary["safe"], int)
        assert isinstance(summary["moderate"], int)
        assert isinstance(summary["ambitious"], int)
        print(f"✓ Summary: Safe={summary['safe']}, Moderate={summary['moderate']}, Ambitious={summary['ambitious']}")
    
    def test_recommendations_with_high_rank(self):
        """Test recommendations for high rank student (500)"""
        high_rank_profile = {**TEST_PROFILE, "rank": 500, "email": "topper@example.com"}
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": high_rank_profile}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        # High rank should have more safe options
        print(f"✓ High rank (500) recommendations: {len(data['recommendations'])} colleges")
    
    def test_recommendations_with_obc_category(self):
        """Test recommendations for OBC category student"""
        obc_profile = {**TEST_PROFILE, "category": "OBC", "rank": 8000, "email": "student@example.com"}
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": obc_profile}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print(f"✓ OBC category recommendations: {len(data['recommendations'])} colleges")


class TestCollegeSearchEndpoint:
    """College search endpoint tests"""
    
    def test_search_returns_200(self):
        """Test /api/colleges/search returns 200"""
        response = requests.get(f"{BASE_URL}/api/colleges/search")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "colleges" in data
        print(f"✓ Search returned: {len(data['colleges'])} colleges")
    
    def test_search_by_name(self):
        """Test search by college name"""
        response = requests.get(f"{BASE_URL}/api/colleges/search?name=IIT")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        # All results should contain IIT in name
        for college in data["colleges"]:
            assert "IIT" in college["name"] or "IIIT" in college["name"]
        print(f"✓ Search by name 'IIT': {len(data['colleges'])} results")
    
    def test_search_by_location(self):
        """Test search by location"""
        response = requests.get(f"{BASE_URL}/api/colleges/search?location=Delhi")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        print(f"✓ Search by location 'Delhi': {len(data['colleges'])} results")
    
    def test_search_by_branch(self):
        """Test search by branch"""
        response = requests.get(f"{BASE_URL}/api/colleges/search?branch=Computer%20Science")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        # All results should have Computer Science branch
        for college in data["colleges"]:
            assert "Computer Science" in college["branches"]
        print(f"✓ Search by branch 'Computer Science': {len(data['colleges'])} results")


class TestCompareEndpoint:
    """College comparison endpoint tests"""
    
    def test_compare_requires_college_ids(self):
        """Test /api/compare with valid college IDs"""
        # First get some college IDs
        search_response = requests.get(f"{BASE_URL}/api/colleges/search")
        colleges = search_response.json()["colleges"]
        
        if len(colleges) >= 2:
            college_ids = [colleges[0]["_id"], colleges[1]["_id"]]
            response = requests.post(
                f"{BASE_URL}/api/compare",
                json={"college_ids": college_ids}
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            assert "colleges" in data
            assert len(data["colleges"]) == 2
            print(f"✓ Compare returned {len(data['colleges'])} colleges")
        else:
            pytest.skip("Not enough colleges to compare")
    
    def test_compare_returns_college_details(self):
        """Test compare returns full college details"""
        search_response = requests.get(f"{BASE_URL}/api/colleges/search")
        colleges = search_response.json()["colleges"]
        
        if len(colleges) >= 2:
            college_ids = [colleges[0]["_id"], colleges[1]["_id"]]
            response = requests.post(
                f"{BASE_URL}/api/compare",
                json={"college_ids": college_ids}
            )
            assert response.status_code == 200
            data = response.json()
            
            for college in data["colleges"]:
                assert "name" in college
                assert "location" in college
                assert "type" in college
                assert "fees_per_year" in college
                assert "placement_avg" in college
            print(f"✓ Compare returned full details for colleges")


class TestWishlistEndpoints:
    """Wishlist add/remove endpoint tests"""
    
    def test_add_to_wishlist(self):
        """Test /api/wishlist/add"""
        # Get a college ID first
        search_response = requests.get(f"{BASE_URL}/api/colleges/search")
        colleges = search_response.json()["colleges"]
        
        if len(colleges) > 0:
            college_id = colleges[0]["_id"]
            response = requests.post(
                f"{BASE_URL}/api/wishlist/add",
                json={
                    "student_email": "test@example.com",
                    "college_id": college_id
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            print(f"✓ Added to wishlist: {colleges[0]['name']}")
    
    def test_get_wishlist(self):
        """Test /api/wishlist/{email}"""
        response = requests.get(f"{BASE_URL}/api/wishlist/test@example.com")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "wishlist" in data
        print(f"✓ Wishlist retrieved: {len(data['wishlist'])} items")
    
    def test_remove_from_wishlist(self):
        """Test /api/wishlist/remove"""
        # Get a college ID first
        search_response = requests.get(f"{BASE_URL}/api/colleges/search")
        colleges = search_response.json()["colleges"]
        
        if len(colleges) > 0:
            college_id = colleges[0]["_id"]
            response = requests.post(
                f"{BASE_URL}/api/wishlist/remove",
                json={
                    "student_email": "test@example.com",
                    "college_id": college_id
                }
            )
            assert response.status_code == 200
            data = response.json()
            assert data["success"] == True
            print(f"✓ Removed from wishlist")


class TestChatEndpoint:
    """AI Chat endpoint tests"""
    
    def test_chat_returns_response(self):
        """Test /api/chat returns AI response"""
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "message": "What are the top IITs for Computer Science?",
                "session_id": f"test_session_{int(time.time())}",
                "student_profile": TEST_PROFILE
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "response" in data
        assert len(data["response"]) > 0
        print(f"✓ Chat response received: {data['response'][:100]}...")
    
    def test_chat_without_profile(self):
        """Test chat works without student profile"""
        response = requests.post(
            f"{BASE_URL}/api/chat",
            json={
                "message": "Tell me about NIT Trichy",
                "session_id": f"test_session_no_profile_{int(time.time())}"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "response" in data
        print(f"✓ Chat without profile works")


class TestBranchRoadmapEndpoint:
    """Branch roadmap endpoint tests"""
    
    def test_branch_roadmap_returns_200(self):
        """Test /api/branch-roadmap/{branch} returns 200"""
        response = requests.get(f"{BASE_URL}/api/branch-roadmap/Computer%20Science")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "branch" in data
        assert "roadmap" in data
        assert data["branch"] == "Computer Science"
        print(f"✓ Branch roadmap returned for Computer Science")
    
    def test_branch_roadmap_content(self):
        """Test roadmap contains career information"""
        response = requests.get(f"{BASE_URL}/api/branch-roadmap/Electronics")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert len(data["roadmap"]) > 50  # Should have substantial content
        print(f"✓ Electronics roadmap content length: {len(data['roadmap'])} chars")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
