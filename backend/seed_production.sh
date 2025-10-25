#!/bin/bash

# Database Seeding Script for Production
# Run this after first deployment to populate the database

echo "🌱 Seeding database with JEE questions..."

python populate_jee_questions.py

if [ $? -eq 0 ]; then
    echo "✅ Database seeded successfully with 39 JEE questions!"
else
    echo "❌ Failed to seed database"
    exit 1
fi
