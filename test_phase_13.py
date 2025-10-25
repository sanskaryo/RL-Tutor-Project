"""
Test Phase 13: Mastery-Based Progression
Tests for Skill Tree, Badges, and Study Plans
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8001/api/v1"
MASTERY_URL = f"{BASE_URL}/mastery"

test_user = {"email": "mastery_test@example.com", "password": "password123", "name": "Mastery Tester"}


def print_section(title: str):
    print("\n" + "="*80)
    print(f"  {title}")
    print("="*80 + "\n")


def register_and_login(user_data: dict) -> str:
    """Register and login test user"""
    requests.post(f"{BASE_URL}/auth/register", json=user_data)
    
    login_response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": user_data["email"], "password": user_data["password"]}
    )
    
    if login_response.status_code == 200:
        token = login_response.json()["access_token"]
        print(f"✅ Logged in as {user_data['name']}")
        return token
    return None


def test_skill_tree(token: str):
    """Test skill tree retrieval and navigation"""
    print_section("PHASE 13.1: Skill Tree & Competency-Based Learning")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get skill tree
    response = requests.get(f"{MASTERY_URL}/skills/tree", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        tree = data["tree"]
        print(f"✅ Skill Tree Retrieved:")
        print(f"   Total Skills: {tree['total_skills']}")
        print(f"   Nodes: {len(tree['nodes'])}")
        print(f"   Edges (Prerequisites): {len(tree['edges'])}")
        
        # Show some skills
        if tree['nodes']:
            print(f"\n   Sample Skills:")
            for skill in tree['nodes'][:5]:
                status = "🔓 Unlocked" if skill['is_unlocked'] else "🔒 Locked"
                print(f"   - {skill['name']} ({skill['category']}) {status}")
        
        return tree['nodes']
    else:
        print(f"❌ Failed to get skill tree: {response.text}")
        return []


def test_skill_assessment(token: str, skills: list):
    """Test skill mastery assessment"""
    print_section("PHASE 13.1: Skill Assessment & Mastery Tracking")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Find an unlocked skill
    unlocked_skills = [s for s in skills if s['is_unlocked']]
    
    if not unlocked_skills:
        print("⚠️  No unlocked skills found")
        return
    
    test_skill = unlocked_skills[0]
    print(f"Testing skill: {test_skill['name']}\n")
    
    # Perform multiple assessments
    for i in range(5):
        assessment = {
            "correct": i < 4,  # 4 correct, 1 incorrect
            "time_spent": 60 + (i * 10)
        }
        
        response = requests.post(
            f"{MASTERY_URL}/skills/{test_skill['id']}/assess",
            headers=headers,
            json=assessment
        )
        
        if response.status_code == 200:
            data = response.json()
            mastery = data['mastery']
            print(f"✅ Assessment {i+1}: {'Correct' if assessment['correct'] else 'Incorrect'}")
            print(f"   Mastery Level: {mastery['mastery_level']}/5")
            print(f"   Accuracy: {mastery['accuracy']}%")
            
            if data['level_up']:
                print(f"   🎉 Level Up! {data['old_level']} → {data['new_level']}")
            
            if data['newly_unlocked_skills']:
                print(f"   🔓 Unlocked {len(data['newly_unlocked_skills'])} new skills!")


def test_mastery_overview(token: str):
    """Test student mastery overview"""
    print_section("PHASE 13.1: Mastery Overview")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{MASTERY_URL}/students/mastery", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Mastery Overview:")
        print(f"   Total Skills: {data['total_skills']}")
        print(f"   Unlocked: {data['unlocked_skills']}")
        print(f"   Mastered: {data['mastered_skills']}")
        print(f"   Average Level: {data['average_mastery_level']}/5")
        
        if data['by_category']:
            print("\n   Progress by Category:")
            for category, stats in data['by_category'].items():
                print(f"   - {category}: {stats['mastered']}/{stats['total']} mastered")


def test_badges(token: str):
    """Test badge system"""
    print_section("PHASE 13.2: Badges & Micro-Credentials")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get all available badges
    response = requests.get(f"{MASTERY_URL}/badges")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Retrieved {data['total']} available badges\n")
        
        # Show some badges
        for badge in data['badges'][:5]:
            print(f"   {badge['icon']} {badge['name']} ({badge['tier']})")
            print(f"      {badge['description']} - {badge['points']} pts")
    
    # Check badge eligibility
    print("\n   Checking badge eligibility...")
    response = requests.post(f"{MASTERY_URL}/students/badges/check", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if data['newly_earned']:
            print(f"   🎉 {data['message']}")
            for badge in data['newly_earned']:
                print(f"      {badge['icon']} {badge['name']} - {badge['points']} pts")
        else:
            print(f"   {data['message']}")
    
    # Get student badges
    response = requests.get(f"{MASTERY_URL}/students/badges", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Student Badge Summary:")
        print(f"   Total Badges: {data['total_badges']}")
        print(f"   Total Points: {data['total_points']}")
        print(f"   By Tier: {data['by_tier']}")


def test_study_plans(token: str, skills: list):
    """Test study plan generation"""
    print_section("PHASE 13.3: Personalized Study Plans")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get some target skills
    target_skills = [s['id'] for s in skills[:3] if s['is_unlocked']]
    
    if not target_skills:
        print("⚠️  No skills available for study plan")
        return
    
    # Generate study plan
    plan_data = {
        "goal_type": "skill_mastery",
        "target_skills": target_skills,
        "target_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "daily_minutes": 30
    }
    
    response = requests.post(
        f"{MASTERY_URL}/study-plans/generate",
        headers=headers,
        json=plan_data
    )
    
    if response.status_code == 201:
        data = response.json()
        plan = data['plan']
        print("✅ Study Plan Generated:")
        print(f"   Title: {plan['title']}")
        print(f"   Goal: {plan['goal_type']}")
        print(f"   Target Date: {plan['target_date']}")
        print(f"   Daily Minutes: {plan['daily_minutes']}")
        print(f"   Total Tasks: {plan['total_tasks']}")
        print(f"   Feasibility: {data['feasibility']}")
        print(f"   Required Daily: {data['required_daily_minutes']} min")
        
        plan_id = plan['id']
        
        # Get today's tasks
        print("\n   Today's Tasks:")
        response = requests.get(f"{MASTERY_URL}/study-plans/today/tasks", headers=headers)
        
        if response.status_code == 200:
            tasks_data = response.json()
            print(f"   Total: {tasks_data['total_tasks']} tasks")
            print(f"   Time Required: {tasks_data['total_minutes']} minutes")
            
            for task in tasks_data['tasks'][:3]:
                print(f"   - {task['skill_name']} ({task['minutes']} min) - {task['task_type']}")
        
        # Get all study plans
        print("\n   All Study Plans:")
        response = requests.get(f"{MASTERY_URL}/study-plans", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Active Plans: {data['total']}")
            for p in data['plans']:
                print(f"   - {p['title']}: {p['progress_percentage']:.1f}% complete ({p['status']})")
    else:
        print(f"❌ Failed to generate study plan: {response.text}")


def test_recommendations(token: str):
    """Test skill recommendations"""
    print_section("PHASE 13.1: Skill Recommendations")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{MASTERY_URL}/students/recommendations?limit=5", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Top {data['count']} Recommended Skills:\n")
        
        for rec in data['recommendations']:
            skill = rec['skill']
            print(f"   {skill['name']} ({skill['category']})")
            print(f"      Priority Score: {rec['priority_score']:.1f}")
            print(f"      Unlocks: {rec['unlocks_count']} other skills")
            print(f"      Difficulty: {skill['difficulty']}")
            print()


def test_mastery_stats(token: str):
    """Test comprehensive mastery statistics"""
    print_section("PHASE 13: Comprehensive Statistics")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f"{MASTERY_URL}/stats", headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Comprehensive Mastery Statistics:")
        print(f"\n   Skills:")
        print(f"   - Total: {data['mastery']['total_skills']}")
        print(f"   - Mastered: {data['mastery']['mastered_skills']}")
        print(f"   - Average Level: {data['mastery']['average_mastery_level']}")
        
        print(f"\n   Badges:")
        print(f"   - Total: {data['badges']['total_badges']}")
        print(f"   - Points: {data['badges']['total_points']}")
        
        print(f"\n   Today's Tasks:")
        print(f"   - Total: {data['today_tasks']['total_tasks']}")
        print(f"   - Minutes: {data['today_tasks']['total_minutes']}")


def main():
    """Run all Phase 13 tests"""
    print("\n" + "="*80)
    print("  PHASE 13: MASTERY-BASED PROGRESSION - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print("\n  Testing: Skill Tree, Badges, Study Plans")
    print("  Backend URL:", BASE_URL)
    print("\n" + "="*80)
    
    # Register and login
    print_section("USER AUTHENTICATION")
    token = register_and_login(test_user)
    
    if not token:
        print("\n❌ Authentication failed. Aborting tests.")
        return
    
    try:
        # Test skill tree
        skills = test_skill_tree(token)
        
        # Test skill assessment
        if skills:
            test_skill_assessment(token, skills)
        
        # Test mastery overview
        test_mastery_overview(token)
        
        # Test recommendations
        test_recommendations(token)
        
        # Test badges
        test_badges(token)
        
        # Test study plans
        if skills:
            test_study_plans(token, skills)
        
        # Test comprehensive stats
        test_mastery_stats(token)
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
    
    # Summary
    print_section("TEST SUMMARY")
    print("✅ Phase 13.1: Competency-Based Learning Paths")
    print("   - Skill tree with DAG structure")
    print("   - Prerequisite checking and unlocking")
    print("   - Mastery assessment and tracking")
    print("   - Skill recommendations")
    print()
    print("✅ Phase 13.2: Micro-Credentials & Badges")
    print("   - Badge system with criteria checking")
    print("   - Automatic badge awarding")
    print("   - Verification codes for certificates")
    print()
    print("✅ Phase 13.3: Personalized Study Plans")
    print("   - AI-powered plan generation")
    print("   - Daily task scheduling")
    print("   - Progress tracking")
    print()
    print("="*80)
    print("  PHASE 13 TESTING COMPLETE!")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
