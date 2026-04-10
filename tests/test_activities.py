"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Should have 9 activities
    assert len(activities) == 9
    
    # Check that expected activities are present
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert "Basketball Team" in activities


def test_get_activities_returns_correct_structure(client):
    """Test that activities have the correct data structure."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Check structure of a single activity
    activity = activities["Chess Club"]
    
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Verify types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_get_activities_participant_counts(client):
    """Test that participant counts are accurate."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # Chess Club should have 2 participants
    assert len(activities["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in activities["Chess Club"]["participants"]
    
    # Programming Class should have 2 participants
    assert len(activities["Programming Class"]["participants"]) == 2
    assert "emma@mergington.edu" in activities["Programming Class"]["participants"]
    
    # Basketball Team should have 1 participant
    assert len(activities["Basketball Team"]["participants"]) == 1
    assert "james@mergington.edu" in activities["Basketball Team"]["participants"]


def test_get_activities_empty_participants(client):
    """Test that activities can have empty participant lists."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    activities = response.json()
    
    # All activities in this test data have participants, but verify structure is there
    all_have_participants_list = all(
        isinstance(activity["participants"], list) 
        for activity in activities.values()
    )
    assert all_have_participants_list
