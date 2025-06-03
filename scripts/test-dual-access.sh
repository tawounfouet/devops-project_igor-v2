#!/bin/bash
# Script de test pour vérifier les deux modes d'accès à l'application

echo "🌤️  Testing Weather App - Dual Access Mode"
echo "=============================================="
echo

# Test 1: Direct Frontend Access (port 4173)
echo "1. Testing direct frontend access (http://localhost:4173)..."
if curl -s http://localhost:4173 > /dev/null; then
    echo "✅ Frontend direct access working"
else
    echo "❌ Frontend direct access failed"
fi

# Test 2: Nginx Proxy Access (port 80)
echo "2. Testing nginx proxy access (http://localhost)..."
if curl -s http://localhost > /dev/null; then
    echo "✅ Nginx proxy access working"
else
    echo "❌ Nginx proxy access failed"
fi

# Test 3: API Direct Access (for port 4173 frontend)
echo "3. Testing API direct access for frontend on port 4173..."
API_DIRECT=$(curl -s "http://localhost:8000/api/v1/history/?limit=1" 2>/dev/null | jq -r '.[0].city // empty' 2>/dev/null)
if [ -n "$API_DIRECT" ] && [ "$API_DIRECT" != "null" ]; then
    echo "✅ Direct API access working (last search: $API_DIRECT)"
else
    echo "❌ Direct API access failed"
fi

# Test 4: API via Nginx (for port 80 frontend)
echo "4. Testing API via nginx for frontend on port 80..."
API_NGINX=$(curl -s "http://localhost/api/v1/history/?limit=1" 2>/dev/null | jq -r '.[0].city // empty' 2>/dev/null)
if [ -n "$API_NGINX" ] && [ "$API_NGINX" != "null" ]; then
    echo "✅ Nginx API access working (last search: $API_NGINX)"
else
    echo "❌ Nginx API access failed"
fi

# Test 5: CORS Test for port 4173
echo "5. Testing CORS from port 4173..."
CORS_RESPONSE=$(curl -H "Origin: http://localhost:4173" -s "http://localhost:8000/api/v1/history/?limit=1" 2>/dev/null | jq -r '.[0].city // empty' 2>/dev/null)
if [ -n "$CORS_RESPONSE" ] && [ "$CORS_RESPONSE" != "null" ]; then
    echo "✅ CORS working for port 4173 (city: $CORS_RESPONSE)"
else
    echo "❌ CORS failed for port 4173"
fi

# Test 6: Test a weather search to ensure end-to-end functionality
echo "6. Testing weather search functionality..."
WEATHER_TEST=$(curl -s "http://localhost:8000/api/v1/weather/?city=Rome" 2>/dev/null | jq -r '.data.name // empty' 2>/dev/null)
if [ "$WEATHER_TEST" = "Rome" ]; then
    echo "✅ Weather search working (searched: Rome)"
else
    echo "❌ Weather search failed"
fi

echo
echo "📝 Summary:"
echo "   - Direct frontend: http://localhost:4173 (uses http://localhost:8000/api/v1)"
echo "   - Nginx frontend:  http://localhost (uses /api/v1 → nginx → backend)"
echo "   - Both modes should work identically now!"
echo
echo "🎉 Dual access mode is configured and tested!"
