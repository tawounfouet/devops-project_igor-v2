#!/bin/bash
# Script de test pour l'application Weather App

echo "🌤️  Testing Weather App API..."
echo

# Test 1: API Health Check
echo "1. Testing API health..."
curl -s http://localhost/api/v1/history/?limit=1 > /dev/null && echo "✅ API is accessible" || echo "❌ API is not accessible"

# Test 2: Weather Search
echo "2. Testing weather search..."
CITY="Berlin"
echo "   Searching weather for $CITY..."
RESULT=$(curl -s "http://localhost/api/v1/weather/?city=$CITY" | jq -r '.data.name // empty')
if [ "$RESULT" = "$CITY" ]; then
    echo "✅ Weather search working"
else
    echo "❌ Weather search failed"
fi

# Test 3: History Check
echo "3. Testing search history..."
HISTORY_COUNT=$(curl -s "http://localhost/api/v1/history/?limit=5" | jq 'length')
if [ "$HISTORY_COUNT" -gt 0 ]; then
    echo "✅ History is working ($HISTORY_COUNT entries found)"
    echo "   Recent searches:"
    curl -s "http://localhost/api/v1/history/?limit=3" | jq -r '.[] | "   - \(.city) (\(.temperature)°C) - \(.searched_at)"'
else
    echo "❌ History is empty"
fi

# Test 4: Frontend Access
echo "4. Testing frontend accessibility..."
curl -s http://localhost > /dev/null && echo "✅ Frontend is accessible" || echo "❌ Frontend is not accessible"

echo
echo "🎉 Testing complete!"
echo "   Access the app at: http://localhost"
echo "   API documentation: http://localhost/api/v1/"
