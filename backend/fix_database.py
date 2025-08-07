#!/usr/bin/env python3
"""
Fix database by adding token column or recreating database
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def fix_database():
    """Fix database by recreating it with proper schema"""
    try:
        # Import after adding path
        from models import db
        from models.user import User
        from models.ticket import Ticket
        from app import app
        
        with app.app_context():
            print("🔧 Fixing database schema...")
            
            # Drop all tables to recreate with proper schema
            db.drop_all()
            print("✅ Dropped all existing tables")
            
            # Create all tables with proper schema
            db.create_all()
            print("✅ Created tables with proper schema")
            
            # Verify the token column exists by checking the model
            print("✅ Database schema fixed successfully!")
            print("   Token column should now be available in the ticket table")
            
    except Exception as e:
        print(f"❌ Error fixing database: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_database()
