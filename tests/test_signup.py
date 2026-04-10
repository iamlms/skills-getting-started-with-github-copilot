"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_new_student_happy_path(client):
    """Test happy path: new student successfully signs up for an activity."""
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": "newstudent@mergington.edu"}
    )
    
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Signed up newstudent@mergington.edu for Chess Club" in result["message"]
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_multiple_students_same_activity(client):
    """Test that multiple different students can sign up for the same activity."""
    # First signup
    response1 = client.post(
        "/activities/Art%20Studio/signup",
        params={"email": "student1@mergington.edu"}
    )
    assert response1.status_code == 200
    
    # Second signup
    response2 = client.post(
        "/activities/Art%20Studio/signup",
        params={"email": "student2@mergington.edu"}
    )
    assert response2.status_code == 200
    
    # Verify both were added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participants = activities["Art Studio"]["participants"]
    assert "student1@mergington.edu" in participants
    assert "student2@mergington.edu" in participants


def test_signup_duplicate_student_fails(client):
    """Test edge case: student cannot sign up twice for the same activity."""
    email = "duplicate@mergington.edu"
    
    # First signup succeeds
    response1 = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email}
    )
    assert response2.status_code == 400
    result = response2.json()
    assert "already signed up" in result["detail"]


def test_signup_invalid_activity_not_found(client):
    """Test error case: signing up for non-existent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent%20Club/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]


def test_signup_at_capacity_exceeds_limit(client):
    """Test that backend allows signups beyond max capacity (current behavior)."""
    # Drama Club has max_participants=25 with 1 current participant
    # Fill it up to capacity and beyond
    
    # Sign up 25 new students (25 - 1 existing = 24 spots to max, + 1 over)
    for i in range(25):
        response = client.post(
            "/activities/Drama%20Club/signup",
            params={"email": f"fill{i}@mergington.edu"}
        )
        assert response.status_code == 200
    
    # Verify we exceeded capacity (26 participants > 25 max)
    activities_response = client.get("/activities")
    activities = activities_response.json()
    drama_club_count = len(activities["Drama Club"]["participants"])
    
    # Current behavior: backend allows going over capacity
    assert drama_club_count == 26
    assert drama_club_count > activities["Drama Club"]["max_participants"]


def test_signup_preserves_existing_participants(client):
    """Test that signup doesn't remove existing participants."""
    # Get initial state
    response = client.get("/activities")
    initial_drama_participants = response.json()["Drama Club"]["participants"].copy()
    
    # Sign up new student
    client.post(
        "/activities/Drama%20Club/signup",
        params={"email": "newmember@mergington.edu"}
    )
    
    # Check that all existing participants are still there
    response = client.get("/activities")
    drama_participants = response.json()["Drama Club"]["participants"]
    
    for existing_participant in initial_drama_participants:
        assert existing_participant in drama_participants
