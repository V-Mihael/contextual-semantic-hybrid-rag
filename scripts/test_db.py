#!/usr/bin/env python3
"""Test Supabase connection with psycopg directly."""
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

try:
    import psycopg
    from src.config import settings
    
    print("=" * 70)
    print("Supabase Connection Test")
    print("=" * 70)
    
    # Parse current URL
    db_url = settings.db_url.replace("postgresql+psycopg://", "postgresql://")
    
    print(f"\n🔍 Testing connection...")
    print(f"Host: {db_url.split('@')[1].split('/')[0] if '@' in db_url else 'unknown'}")
    
    # Test connection
    try:
        conn = psycopg.connect(db_url, connect_timeout=5)
        print("✅ Connected successfully!")
        
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            print(f"PostgreSQL: {version[:60]}...")
            
            cur.execute("SELECT * FROM pg_extension WHERE extname = 'vector';")
            if cur.fetchone():
                print("✅ pgvector extension installed")
            else:
                print("⚠️  pgvector NOT installed. Run: CREATE EXTENSION IF NOT EXISTS vector;")
        
        conn.close()
        
    except psycopg.OperationalError as e:
        error_msg = str(e)
        print(f"❌ Connection failed: {error_msg[:200]}")
        
        if "Network is unreachable" in error_msg or "2600:" in error_msg:
            print("\n💡 IPv6 connection issue detected!")
            print("\n📋 Solutions:")
            print("1. Use Supabase Connection Pooler (recommended):")
            print("   - Go to: Supabase Dashboard → Settings → Database")
            print("   - Copy 'Connection Pooling' string (port 6543)")
            print("   - Update DB_URL in .env")
            print("\n2. Or add to your connection string:")
            print(f"   DB_URL={settings.db_url}?options=-c%20tcp_user_timeout=10000")
            print("\n3. Or disable IPv6 temporarily:")
            print("   sudo sysctl -w net.ipv6.conf.all.disable_ipv6=1")
        
except ImportError:
    print("❌ psycopg not installed. Install dependencies first.")
except Exception as e:
    print(f"❌ Error: {e}")
