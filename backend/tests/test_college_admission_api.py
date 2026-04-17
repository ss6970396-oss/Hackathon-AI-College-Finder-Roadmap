"""
Backend API Tests for College Admission AI Platform - Iteration 2
Tests: Health, Recommendations (JEE + EAMCET), Compare, Wishlist, Chat, Branch Roadmap, College Search
New in Iteration 2: EAMCET exam type filtering, 60 colleges (10 IIT, 22 NIT, 9 IIIT, 19 EAMCET)
"""
import pytest
import requests
import os
import time

BASE_URL = os.environ.get('REACT_APP_BACKEND_URL', '').rstrip('/')

# Test profile data - JEE
TEST_PROFILE_JEE = {
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

# Test profile data - EAMCET
TEST_PROFILE_EAMCET = {
    "rank": 3000,
    "exam_type": "EAMCET",
    "category": "General",
    "home_state": "Telangana",
    "preferred_branches": ["Computer Science"],
    "preferred_cities": [],
    "max_budget": 100,
    "name": "Ravi Test",
    "email": "ravi@example.com"
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


class TestRecommendationsJEE:
    """JEE Recommendations endpoint tests - should return IIT/NIT/IIIT colleges"""
    
    def test_jee_recommendations_returns_200(self):
        """Test /api/recommendations with JEE returns 200"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_JEE}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "recommendations" in data
        assert "summary" in data
        print(f"✓ JEE Recommendations returned: {len(data['recommendations'])} colleges")
    
    def test_jee_returns_only_iit_nit_iiit(self):
        """Test JEE recommendations only return IIT/NIT/IIIT/GFTI colleges (not EAMCET)"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_JEE}
        )
        assert response.status_code == 200
        data = response.json()
        
        for rec in data["recommendations"]:
            assert rec["type"] in ["IIT", "NIT", "IIIT", "GFTI"], f"JEE should not return {rec['type']} colleges"
        print(f"✓ JEE correctly returns only IIT/NIT/IIIT colleges")
    
    def test_jee_has_probability_scores(self):
        """Test JEE recommendations include probability scores and classification"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_JEE}
        )
        assert response.status_code == 200
        data = response.json()
        
        if len(data["recommendations"]) > 0:
            rec = data["recommendations"][0]
            assert "probability" in rec
            assert "classification" in rec
            assert rec["classification"] in ["Safe", "Moderate", "Ambitious"]
            assert 0 <= rec["probability"] <= 100
            print(f"✓ JEE First recommendation: {rec['college_name']} - {rec['probability']}% ({rec['classification']})")
    
    def test_jee_summary_counts(self):
        """Test JEE summary contains Safe/Moderate/Ambitious counts"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_JEE}
        )
        assert response.status_code == 200
        data = response.json()
        
        summary = data["summary"]
        assert "safe" in summary
        assert "moderate" in summary
        assert "ambitious" in summary
        print(f"✓ JEE Summary: Safe={summary['safe']}, Moderate={summary['moderate']}, Ambitious={summary['ambitious']}")


class TestRecommendationsEAMCET:
    """EAMCET Recommendations endpoint tests - should return only EAMCET colleges"""
    
    def test_eamcet_recommendations_returns_200(self):
        """Test /api/recommendations with EAMCET returns 200"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_EAMCET}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0, "EAMCET should return at least 1 college"
        print(f"✓ EAMCET Recommendations returned: {len(data['recommendations'])} colleges")
    
    def test_eamcet_returns_only_eamcet_colleges(self):
        """Test EAMCET recommendations only return EAMCET type colleges"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_EAMCET}
        )
        assert response.status_code == 200
        data = response.json()
        
        for rec in data["recommendations"]:
            assert rec["type"] == "EAMCET", f"EAMCET should only return EAMCET colleges, got {rec['type']}"
        print(f"✓ EAMCET correctly returns only EAMCET colleges")
    
    def test_eamcet_includes_known_colleges(self):
        """Test EAMCET returns known colleges like CBIT, JNTU, Osmania"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_EAMCET}
        )
        assert response.status_code == 200
        data = response.json()
        
        college_names = [rec["college_name"] for rec in data["recommendations"]]
        # Check at least one known EAMCET college is present
        known_eamcet = ["CBIT", "JNTU", "Osmania", "VNR", "Vasavi", "MGIT", "BVRIT"]
        found = any(any(known in name for known in known_eamcet) for name in college_names)
        assert found, f"Expected at least one known EAMCET college in results"
        print(f"✓ EAMCET includes known colleges: {college_names[:3]}")
    
    def test_eamcet_has_probability_scores(self):
        """Test EAMCET recommendations include probability scores"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_EAMCET}
        )
        assert response.status_code == 200
        data = response.json()
        
        if len(data["recommendations"]) > 0:
            rec = data["recommendations"][0]
            assert "probability" in rec
            assert "classification" in rec
            assert "ai_insight" in rec
            assert "historical_trend" in rec
            print(f"✓ EAMCET First recommendation: {rec['college_name']} - {rec['probability']}%")


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
    
    def test_search_returns_60_colleges(self):
        """Test search returns approximately 60 colleges (limit 50 per query)"""
        response = requests.get(f"{BASE_URL}/api/colleges/search")
        assert response.status_code == 200
        data = response.json()
        # API limits to 50, but we have 60 total
        assert len(data["colleges"]) >= 40, "Should have at least 40 colleges"
        print(f"✓ Total colleges in search: {len(data['colleges'])}")
    
    def test_search_by_name_iit(self):
        """Test search by college name IIT"""
        response = requests.get(f"{BASE_URL}/api/colleges/search?name=IIT")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        # Should find IIT and IIIT colleges
        for college in data["colleges"]:
            assert "IIT" in college["name"] or "IIIT" in college["name"]
        print(f"✓ Search by name 'IIT': {len(data['colleges'])} results")
    
    def test_search_by_name_eamcet_college(self):
        """Test search by EAMCET college name (CBIT)"""
        response = requests.get(f"{BASE_URL}/api/colleges/search?name=CBIT")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert len(data["colleges"]) >= 1, "Should find at least 1 CBIT college"
        print(f"✓ Search by name 'CBIT': {len(data['colleges'])} results")
    
    def test_search_by_location(self):
        """Test search by location Hyderabad (many EAMCET colleges)"""
        response = requests.get(f"{BASE_URL}/api/colleges/search?location=Hyderabad")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        assert len(data["colleges"]) >= 5, "Hyderabad should have many colleges"
        print(f"✓ Search by location 'Hyderabad': {len(data['colleges'])} results")
    
    def test_search_by_branch(self):
        """Test search by branch"""
        response = requests.get(f"{BASE_URL}/api/colleges/search?branch=Computer%20Science")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] == True
        for college in data["colleges"]:
            assert "Computer Science" in college["branches"]
        print(f"✓ Search by branch 'Computer Science': {len(data['colleges'])} results")


class TestCompareEndpoint:
    """College comparison endpoint tests"""
    
    def test_compare_requires_college_ids(self):
        """Test /api/compare with valid college IDs"""
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
                "student_profile": TEST_PROFILE_JEE
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


class TestHistoricalTrendData:
    """Test historical trend data for charts"""
    
    def test_recommendations_include_historical_trend(self):
        """Test recommendations include historical_trend for line charts"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_JEE}
        )
        assert response.status_code == 200
        data = response.json()
        
        if len(data["recommendations"]) > 0:
            rec = data["recommendations"][0]
            assert "historical_trend" in rec, "Should include historical_trend for charts"
            if len(rec["historical_trend"]) > 0:
                trend = rec["historical_trend"][0]
                assert "year" in trend
                assert "opening_rank" in trend
                assert "closing_rank" in trend
            print(f"✓ Historical trend data present: {len(rec['historical_trend'])} years")
    
    def test_recommendations_include_predicted_cutoff(self):
        """Test recommendations include predicted_cutoff for ML predictions"""
        response = requests.post(
            f"{BASE_URL}/api/recommendations",
            json={"profile": TEST_PROFILE_JEE}
        )
        assert response.status_code == 200
        data = response.json()
        
        if len(data["recommendations"]) > 0:
            rec = data["recommendations"][0]
            assert "predicted_cutoff" in rec, "Should include predicted_cutoff"
            print(f"✓ Predicted cutoff data present")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
