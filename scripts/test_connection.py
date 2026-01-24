#!/usr/bin/env python3
"""Test Supabase connection and suggest fixes."""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine, text
from src.config import settings

def test_connection(db_url: str, description: str):
    """Test database connection."""
    print(f"\n🔍 Testing: {description}")
    print(f"URL: {db_url.split('@')[1] if '@' in db_url else 'invalid'}")
    
    try:
        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Connected! PostgreSQL version: {version[:50]}...")
            
            # Check pgvector
            result = conn.execute(text("SELECT * FROM pg_extension WHERE extname = 'vector';"))
            if result.fetchone():
                print("✅ pgvector extension is installed")
            else:
                print("⚠️  pgvector extension NOT found. Run: CREATE EXTENSION IF NOT EXISTS vector;")
            
            return True
    except Exception as e:
        print(f"❌ Failed: {str(e)[:200]}")
        return False

def main():
    print("=" * 70)
    print("Supabase Connection Test")
    print("=" * 70)
    
    current_url = settings.db_url
    
    # Test 1: Current URL
    if test_connection(current_url, "Current .env configuration"):
        print("\n✅ Connection working! No changes needed.")
        return
    
    # Test 2: Force IPv4
    if "db." in current_url and ".supabase.co" in current_url:
        # Extract parts
        parts = current_url.split("@")
        if len(parts) == 2:
            credentials = parts[0]
            host_part = parts[1]
            
            # Try with hostaddr parameter to force IPv4
            ipv4_url = f"{credentials}@{host_part}?hostaddr=0.0.0.0"
            if test_connection(ipv4_url, "Force IPv4 (hostaddr)"):
                print(f"\n✅ Solution found! Update your .env DB_URL to:")
                print(f"DB_URL={ipv4_url}")
                return
            
            # Try pooler (port 6543)
            pooler_url = current_url.replace(":5432", ":6543").replace("db.", "aws-0-us-west-1.pooler.")
            if test_connection(pooler_url, "Supabase Pooler (port 6543)"):
                print(f"\n✅ Solution found! Update your .env DB_URL to:")
                print(f"DB_URL={pooler_url}")
                return
    
    print("\n" + "=" * 70)
    print("❌ All connection attempts failed.")
    print("\n📋 Troubleshooting steps:")
    print("1. Check Supabase Dashboard → Settings → Database")
    print("2. Verify your password is correct (no special chars issues)")
    print("3. Try the 'Connection Pooling' string (port 6543)")
    print("4. Check if your IP is allowed (Supabase → Settings → Database → Connection pooling)")
    print("5. Disable IPv6 on your system temporarily")
    print("\n💡 Get connection string from:")
    print("   Supabase Dashboard → Settings → Database → Connection string → URI")

if __name__ == "__main__":
    main()
