#!/usr/bin/env python3
"""
Performance test script to demonstrate async benefits.
This script sends multiple concurrent requests to test the async implementation.
"""

import asyncio
import httpx
import time
from typing import List


async def send_notification(client: httpx.AsyncClient, user_id: int, message: str) -> dict:
    """Send a single notification request."""
    try:
        response = await client.post(
            "http://localhost:8080/notifications/send",
            headers={
                "Authorization": "Bearer onlyvim2024",
                "Content-Type": "application/json"
            },
            json={
                "userId": user_id,
                "message": message
            }
        )
        return {
            "status_code": response.status_code,
            "response": response.json(),
            "user_id": user_id
        }
    except Exception as e:
        return {
            "status_code": 0,
            "error": str(e),
            "user_id": user_id
        }


async def run_concurrent_test(num_requests: int = 10):
    """Run concurrent notification requests to test async performance."""
    print(f"🚀 Starting performance test with {num_requests} concurrent requests...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Create tasks for concurrent execution
        tasks = []
        for i in range(num_requests):
            user_id = (i % 4) + 1  # Cycle through users 1-4
            message = f"Performance test message #{i+1}"
            tasks.append(send_notification(client, user_id, message))
        
        # Measure execution time
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        # Analyze results
        successful = sum(1 for r in results if isinstance(r, dict) and r.get("status_code") == 200)
        failed = len(results) - successful
        total_time = end_time - start_time
        
        print(f"✅ Test completed in {total_time:.2f} seconds")
        print(f"📊 Results: {successful} successful, {failed} failed")
        print(f"⚡ Average time per request: {total_time/num_requests:.3f} seconds")
        print(f"🔥 Requests per second: {num_requests/total_time:.2f}")
        
        # Show some sample responses
        print("\n📋 Sample responses:")
        for i, result in enumerate(results[:3]):
            if isinstance(result, dict) and "response" in result:
                print(f"  Request {i+1}: {result['response'].get('message', 'Unknown')}")


async def test_sequential_vs_concurrent():
    """Compare sequential vs concurrent performance."""
    print("🔬 Comparing sequential vs concurrent performance...\n")
    
    # Test 1: Sequential requests
    print("1️⃣ Sequential requests:")
    async with httpx.AsyncClient(timeout=30.0) as client:
        start_time = time.time()
        for i in range(5):
            await send_notification(client, 1, f"Sequential test {i+1}")
        sequential_time = time.time() - start_time
        print(f"   Time: {sequential_time:.2f} seconds\n")
    
    # Test 2: Concurrent requests
    print("2️⃣ Concurrent requests:")
    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [send_notification(client, 1, f"Concurrent test {i+1}") for i in range(5)]
        start_time = time.time()
        await asyncio.gather(*tasks)
        concurrent_time = time.time() - start_time
        print(f"   Time: {concurrent_time:.2f} seconds\n")
    
    # Calculate improvement
    improvement = ((sequential_time - concurrent_time) / sequential_time) * 100
    print(f"🎯 Performance improvement: {improvement:.1f}% faster with async!")


if __name__ == "__main__":
    print("🧪 User Notifications Manager - Performance Test\n")
    
    try:
        # Run the tests
        asyncio.run(test_sequential_vs_concurrent())
        print("\n" + "="*60 + "\n")
        asyncio.run(run_concurrent_test(20))
        
    except KeyboardInterrupt:
        print("\n❌ Test interrupted by user")
    except Exception as e:
        print(f"\n💥 Test failed: {e}")
    
    print("\n✨ Performance test completed!") 