#!/usr/bin/env python
"""
Test the dashboard config endpoint
Get JWT token and test the dashboard configuration endpoint
"""
import requests
import json

BASE_URL = "http://localhost:8000"

# Step 1: Login to get JWT token
print("🔐 Logging in...")
login_response = requests.post(
    f"{BASE_URL}/auth/login",
    json={
        "email": "superadmin@cybersecurity.io",
        "password": "Super@2026!"
    }
)

if login_response.status_code != 200:
    print(f"❌ Login failed: {login_response.text}")
    exit(1)

login_data = login_response.json()
access_token = login_data["access_token"]
print(f"✅ Logged in successfully")
print(f"   Token: {access_token[:50]}...")

# Step 2: Get dashboard config for current user
print("\n📊 Fetching dashboard config...")
headers = {"Authorization": f"Bearer {access_token}"}
config_response = requests.get(
    f"{BASE_URL}/api/internal/dashboard/config",
    headers=headers
)

if config_response.status_code != 200:
    print(f"❌ Failed to get dashboard config: {config_response.text}")
    exit(1)

config = config_response.json()
print(f"✅ Dashboard config retrieved")
print(f"\n   Role: {config['role_type']}")
print(f"   Display Name: {config['display_name']}")
print(f"   Widgets: {len(config['widgets'])}")
print(f"   Menu Items: {len(config['menu_items'])}")
print(f"   Permissions: {len(config['permissions'])}")
print(f"   Quick Actions: {len(config['quick_actions'])}")

# Step 3: Get dashboard stats
print("\n📈 Fetching dashboard stats...")
stats_response = requests.get(
    f"{BASE_URL}/api/internal/dashboard/stats",
    headers=headers
)

if stats_response.status_code == 200:
    stats = stats_response.json()
    print(f"✅ Dashboard stats retrieved")
    print(f"   Total Widgets: {stats['total_widgets']}")
    print(f"   Total Menu Items: {stats['total_menu_items']}")
    print(f"   Permissions: {stats['permissions_count']}")
    print(f"   Metrics: {stats['metrics_count']}")

# Step 4: Show sample widget
print("\n🎨 Sample Widget (first 3):")
for i, widget in enumerate(config['widgets'][:3]):
    print(f"   {i+1}. {widget['title']} ({widget['type']})")
    print(f"      Position: ({widget['grid_x']}, {widget['grid_y']}) Size: {widget['grid_width']}x{widget['grid_height']}")

# Step 5: Show sample menu
print("\n📋 Sample Menu Items (first 5):")
for i, item in enumerate(config['menu_items'][:5]):
    print(f"   {i+1}. {item['label']} -> {item['path']}")
    if item['children']:
        for child in item['children'][:2]:
            print(f"      └─ {child['label']} -> {child['path']}")

print("\n" + "="*60)
print("✅ Dashboard Config API Test PASSED")
print("="*60)

# Save config to file for reference
with open("dashboard_config_sample.json", "w") as f:
    json.dump(config, f, indent=2, default=str)
    print("\n💾 Saved full config to: dashboard_config_sample.json")
