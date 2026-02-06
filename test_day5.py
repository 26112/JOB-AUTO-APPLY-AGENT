"""
Day 5 Test - Test config and memory system without requiring PDF
"""

from config.loader import load_settings
from memory.memory import load_memory, mark_job_applied, job_already_applied, get_applied_count


def test_day5():
    print("=" * 50)
    print("Day 5 Test - Config & Memory System")
    print("=" * 50)
    
    # Test 1: Load Settings
    print("\n✅ Test 1: Loading Settings")
    settings = load_settings()
    print(f"   Job Title: {settings['job']['title']}")
    print(f"   Location: {settings['job']['location']}")
    print(f"   Portals: {settings['job']['portals']}")
    print(f"   Max Jobs: {settings['job']['max_jobs_per_session']}")
    print(f"   Slow Mode: {settings['behavior']['slow_mode']}")
    
    # Test 2: Load Memory
    print("\n✅ Test 2: Loading Memory")
    memory = load_memory()
    print(f"   Applied Jobs Count: {len(memory['applied_jobs'])}")
    
    # Test 3: Memory Operations
    print("\n✅ Test 3: Memory Operations")
    
    # Test job URLs
    test_jobs = [
        "https://indeed.com/job/123",
        "https://indeed.com/job/456",
        "https://indeed.com/job/789"
    ]
    
    for job_url in test_jobs:
        if not job_already_applied(job_url):
            print(f"   ➕ Marking as applied: {job_url}")
            mark_job_applied(job_url)
        else:
            print(f"   ⏭️  Already applied: {job_url}")
    
    # Test 4: Duplicate Prevention
    print("\n✅ Test 4: Duplicate Prevention")
    duplicate_test = "https://indeed.com/job/123"
    
    if job_already_applied(duplicate_test):
        print(f"   ✅ Duplicate detected: {duplicate_test}")
        print(f"   ✅ Will skip this job")
    else:
        print(f"   ❌ Duplicate not detected (should have been)")
    
    # Test 5: Final Count
    print("\n✅ Test 5: Final Memory Status")
    final_count = get_applied_count()
    print(f"   Total jobs applied: {final_count}")
    
    # Display all applied jobs
    memory = load_memory()
    print(f"\n📋 All Applied Jobs:")
    for i, job in enumerate(memory['applied_jobs'], 1):
        print(f"   {i}. {job}")
    
    print("\n" + "=" * 50)
    print("✅ Day 5 Test Completed!")
    print("=" * 50)


if __name__ == "__main__":
    test_day5()
