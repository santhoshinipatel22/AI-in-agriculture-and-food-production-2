# Smart Farming API Reference

Base URL: `http://localhost:5000/api`

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <JWT_TOKEN>
```

---

## Authentication Endpoints

### Register User
**POST** `/auth/register`

Create a new farmer account.

**Request Body:**
```json
{
  "firstName": "John",
  "lastName": "Farmer",
  "email": "john@farm.com",
  "password": "SecurePass123!",
  "phone": "9876543210"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "userId": "507f1f77bcf86cd799439011",
    "email": "john@farm.com",
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### Login
**POST** `/auth/login`

Authenticate farmer and get JWT tokens.

**Request Body:**
```json
{
  "email": "john@farm.com",
  "password": "SecurePass123!"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "userId": "507f1f77bcf86cd799439011",
    "firstName": "John",
    "email": "john@farm.com",
    "accessToken": "eyJhbGciOiJIUzI1NiIs...",
    "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### Verify Email
**GET** `/auth/verify/:token`

Verify farmer email address during registration.

**Response (200):**
```json
{
  "success": true,
  "message": "Email verified successfully"
}
```

### Refresh Token
**POST** `/auth/refresh-token`

Get a new access token using refresh token.

**Request Body:**
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "accessToken": "eyJhbGciOiJIUzI1NiIs..."
  }
}
```

### Reset Password
**POST** `/auth/reset-password`

Request a password reset link.

**Request Body:**
```json
{
  "email": "john@farm.com"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Password reset link sent to email"
}
```

### Logout
**POST** `/auth/logout`

Invalidate current session and refresh token.

**Response (200):**
```json
{
  "success": true,
  "message": "Logout successful"
}
```

---

## Crop Management Endpoints

### Create Crop
**POST** `/crops`

Add a new crop to the farmer's field.

**Request Body:**
```json
{
  "cropName": "Rice",
  "fieldName": "Field 1",
  "fieldArea": 10,
  "sowingDate": "2024-01-15",
  "expectedHarvestDate": "2024-05-15"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Crop created successfully",
  "data": {
    "cropId": "507f1f77bcf86cd799439012",
    "cropName": "Rice",
    "status": "planning",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

### Get Crops List
**GET** `/crops`

Retrieve all crops for the logged-in farmer.

**Query Parameters:**
- `page` (optional): Pagination page number (default: 1)
- `limit` (optional): Items per page (default: 20)
- `status` (optional): Filter by status (planning, sowing, growing, harvesting, completed)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "crops": [
      {
        "cropId": "507f1f77bcf86cd799439012",
        "cropName": "Rice",
        "fieldName": "Field 1",
        "fieldArea": 10,
        "status": "growing",
        "sowingDate": "2024-01-15",
        "expectedHarvestDate": "2024-05-15"
      }
    ],
    "pagination": {
      "total": 5,
      "page": 1,
      "pages": 1
    }
  }
}
```

### Get Crop Details
**GET** `/crops/:cropId`

Get detailed information about a specific crop.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "cropId": "507f1f77bcf86cd799439012",
    "cropName": "Rice",
    "fieldName": "Field 1",
    "fieldArea": 10,
    "sowingDate": "2024-01-15",
    "expectedHarvestDate": "2024-05-15",
    "harvestDate": null,
    "status": "growing",
    "estimatedYield": null,
    "actualYield": null,
    "expenses": [
      {
        "amount": 5000,
        "category": "Seeds",
        "date": "2024-01-15"
      }
    ],
    "diseaseAlerts": [
      {
        "diseaseName": "Leaf Blight",
        "severity": "medium",
        "detectionDate": "2024-02-20"
      }
    ]
  }
}
```

### Update Crop
**PUT** `/crops/:cropId`

Update crop information.

**Request Body:**
```json
{
  "status": "harvesting",
  "actualYield": 50,
  "harvestDate": "2024-05-20"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "Crop updated successfully",
  "data": { /* updated crop object */ }
}
```

### Delete Crop
**DELETE** `/crops/:cropId`

Remove a crop record.

**Response (200):**
```json
{
  "success": true,
  "message": "Crop deleted successfully"
}
```

### Get Crop Metrics
**GET** `/crops/metrics`

Get aggregated crop statistics for the farmer's dashboard.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "totalCrops": 5,
    "activeCrops": 3,
    "totalExpense": 45000,
    "totalYield": 150,
    "averageYield": 30,
    "cropBreakdown": {
      "rice": 2,
      "wheat": 1,
      "corn": 2
    }
  }
}
```

### Get Crop Diseases
**GET** `/crops/:cropId/diseases`

Get all disease detections for a specific crop.

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "diseaseId": "507f1f77bcf86cd799439013",
      "diseaseName": "Leaf Blight",
      "severity": "medium",
      "confidence": 92,
      "detectionDate": "2024-02-20",
      "treatment": {
        "organic": "Neem oil spray",
        "chemical": "Mancozeb 75% WP"
      },
      "recoveryStatus": "in_progress"
    }
  ]
}
```

---

## Disease Detection Endpoints

### Detect Disease
**POST** `/diseases/detect/:cropId`

Upload crop leaf image for AI-based disease detection.

**Request:**
- Content-Type: `multipart/form-data`
- Field: `image` (file) - JPEG/PNG image

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/diseases/detect/507f1f77bcf86cd799439012 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@leaf.jpg"
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "diseaseId": "507f1f77bcf86cd799439013",
    "diseaseName": "Powdery Mildew",
    "confidence": 94,
    "severity": "high",
    "affectedArea": 35,
    "treatment": {
      "organic": [
        "Spray sulfur dust",
        "Use potassium bicarbonate"
      ],
      "chemical": [
        "Mancozeb 75% WP",
        "Hexaconazole 5% EC"
      ],
      "integrated": [
        "Remove infected leaves",
        "Improve air circulation",
        "Apply fungicide"
      ]
    },
    "preventiveMeasures": [
      "Maintain optimal temperature",
      "Reduce humidity levels",
      "Practice crop rotation"
    ],
    "productRecommendations": [
      {
        "name": "Neem Oil Organic Spray",
        "price": 250,
        "seller": "Local Agro Shop"
      }
    ],
    "recovery": {
      "status": "not_started",
      "progress": 0
    }
  }
}
```

### Get Diseases List
**GET** `/diseases`

Get all disease detections for the logged-in farmer.

**Query Parameters:**
- `status` (optional): Filter by recovery status (not_started, in_progress, completed)
- `severity` (optional): Filter by severity (low, medium, high, critical)

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "diseaseId": "507f1f77bcf86cd799439013",
      "cropName": "Rice",
      "diseaseName": "Leaf Blight",
      "severity": "medium",
      "detectionDate": "2024-02-20",
      "recoveryStatus": "in_progress"
    }
  ]
}
```

### Update Disease Status
**PATCH** `/diseases/:diseaseId`

Update disease recovery status.

**Request Body:**
```json
{
  "status": "in_progress",
  "progressPercent": 50
}
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "diseaseId": "507f1f77bcf86cd799439013",
    "status": "in_progress",
    "progress": 50
  }
}
```

### Get Disease Statistics
**GET** `/diseases/stats`

Get disease detection statistics for analytics.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "totalDetections": 15,
    "bySeverity": {
      "low": 5,
      "medium": 7,
      "high": 2,
      "critical": 1
    },
    "byRecoveryStatus": {
      "not_started": 4,
      "in_progress": 8,
      "completed": 3
    },
    "mostCommonDiseases": [
      { "name": "Leaf Blight", "count": 6 },
      { "name": "Rust", "count": 4 }
    ]
  }
}
```

---

## Weather Advisory Endpoints

### Get Weather Data
**GET** `/weather/data`

Get current weather conditions for the farmer's location.

**Query Parameters:**
- `lat` (required): Latitude
- `lon` (required): Longitude

**Example:**
```
GET /weather/data?lat=11.1234&lon=78.5678
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "date": "2024-02-20",
    "temperature": 28,
    "humidity": 65,
    "windSpeed": 12,
    "rainfall": 0,
    "uvIndex": 7,
    "cloudiness": 30,
    "location": {
      "district": "Villupuram",
      "state": "Tamil Nadu"
    }
  }
}
```

### Get Weather Forecast
**GET** `/weather/forecast`

Get 10-day weather forecast.

**Query Parameters:**
- `lat`: Latitude
- `lon`: Longitude

**Response (200):**
```json
{
  "success": true,
  "data": {
    "forecast": [
      {
        "date": "2024-02-21",
        "maxTemp": 32,
        "minTemp": 24,
        "rainfall": 5,
        "humidity": 70,
        "windSpeed": 15
      }
    ]
  }
}
```

### Get Agricultural Advisory
**GET** `/weather/advisory`

Get crop-specific agricultural recommendations.

**Query Parameters:**
- `lat`: Latitude
- `lon`: Longitude
- `cropId` (optional): Specific crop ID

**Response (200):**
```json
{
  "success": true,
  "data": {
    "irrigation": {
      "recommendedWater": 25,
      "unit": "mm",
      "frequency": "Every 5 days",
      "timing": "Early morning"
    },
    "pesticide": "Avoid spraying today - high wind speed",
    "harvesting": "Not recommended - rainfall expected",
    "sowingRecommendation": "Conditions not suitable",
    "bestCropsForSeason": [
      "Rice",
      "Sugarcane",
      "Cotton"
    ]
  }
}
```

### Get Weather Alerts
**GET** `/weather/alerts`

Get weather-related alerts and warnings.

**Query Parameters:**
- `lat`: Latitude
- `lon`: Longitude

**Response (200):**
```json
{
  "success": true,
  "data": {
    "alerts": [
      {
        "type": "heavy_rain",
        "severity": "high",
        "message": "Heavy rainfall expected in next 6 hours",
        "recommendation": "Harvest before rain starts"
      }
    ]
  }
}
```

---

## Price Prediction Endpoints

### Get Price Prediction
**GET** `/prices/prediction`

Get current and predicted prices for crops.

**Query Parameters:**
- `crop` (required): Crop name (rice, wheat, corn, etc.)
- `region` (optional): Region/district name

**Example:**
```
GET /prices/prediction?crop=rice&region=Villupuram
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "crop": "Rice",
    "currentPrice": 2850,
    "predictedPrice": 2950,
    "currency": "INR/quintal",
    "trend": "uptrend",
    "confidence": 87,
    "recommendation": "sell",
    "expectedProfit": 500,
    "bestSellDate": "2024-02-25",
    "marketInsights": {
      "avgPriceThisMonth": 2780,
      "highest": 2950,
      "lowest": 2600
    }
  }
}
```

### Get Price History
**GET** `/prices/history`

Get historical price data for analysis.

**Query Parameters:**
- `crop`: Crop name
- `days` (optional): Number of past days (default: 30)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "date": "2024-02-20",
        "price": 2820
      },
      {
        "date": "2024-02-21",
        "price": 2850
      }
    ]
  }
}
```

### Get Market Insights
**GET** `/prices/insights`

Get top crop recommendations and market analysis.

**Query Parameters:**
- `region` (optional): Region filter

**Response (200):**
```json
{
  "success": true,
  "data": {
    "topCrops": [
      {
        "crop": "Rice",
        "score": 9.2,
        "reason": "High demand, stable prices",
        "avgPrice": 2850,
        "profitMargin": "25-30%"
      }
    ],
    "marketTrends": "Growing demand for organic rice",
    "seasonalAdvice": "Optimal time to plant wheat"
  }
}
```

---

## IoT Device Endpoints

### Register Device
**POST** `/iot/register`

Register a new IoT sensor device.

**Request Body:**
```json
{
  "deviceId": "SOIL-001",
  "deviceName": "Field 1 Soil Sensor",
  "deviceType": "soil_moisture",
  "location": {
    "fieldName": "Field 1",
    "coordinates": [11.1234, 78.5678]
  }
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Device registered successfully",
  "data": {
    "deviceId": "SOIL-001",
    "status": "active"
  }
}
```

### Get Device Status
**GET** `/iot/:deviceId/status`

Get current status and readings of a device.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "deviceId": "SOIL-001",
    "deviceName": "Field 1 Soil Sensor",
    "status": "active",
    "lastUpdate": "2024-02-21T10:15:00Z",
    "currentReadings": {
      "soilMoisture": 65,
      "temperature": 28,
      "humidity": 72,
      "ph": 6.8,
      "ec": 1.2,
      "nitrogen": 45,
      "phosphorus": 32,
      "potassium": 180
    },
    "batteryLevel": 85,
    "signalStrength": -70
  }
}
```

### Get Device History
**GET** `/iot/:deviceId/history`

Get historical sensor data.

**Query Parameters:**
- `days` (optional): Number of past days (default: 7)
- `limit` (optional): Number of records (default: 100)

**Response (200):**
```json
{
  "success": true,
  "data": {
    "history": [
      {
        "timestamp": "2024-02-21T10:00:00Z",
        "soilMoisture": 65,
        "temperature": 28
      },
      {
        "timestamp": "2024-02-21T10:15:00Z",
        "soilMoisture": 64,
        "temperature": 29
      }
    ]
  }
}
```

### Get Latest Readings
**GET** `/iot/:deviceId/readings`

Get latest sensor readings.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "soilMoisture": 65,
    "temperature": 28,
    "humidity": 72,
    "ph": 6.8,
    "timestamp": "2024-02-21T10:15:00Z"
  }
}
```

---

## Subsidy Endpoints

### Get All Subsidies
**GET** `/subsidies`

Get list of all available government subsidies.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "subsidies": [
      {
        "subsidyId": "GOV-2024-001",
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "description": "Crop insurance scheme",
        "amount": 15000,
        "currency": "INR",
        "deadline": "2024-12-31",
        "status": "active"
      }
    ]
  }
}
```

### Get Applicable Subsidies
**GET** `/subsidies/applicable`

Get subsidies applicable to the farmer's crops and region.

**Response (200):**
```json
{
  "success": true,
  "data": [
    {
      "subsidyId": "GOV-2024-001",
      "name": "Pradhan Mantri Fasal Bima Yojana",
      "amount": 15000,
      "eligibilityMatch": "You grow Rice and Cotton"
    }
  ]
}
```

### Apply for Subsidy
**POST** `/subsidies/apply/:subsidyId`

Submit application for a subsidy.

**Request Body:**
```json
{
  "documents": [
    {
      "type": "land_certificate",
      "url": "/uploads/land_cert.pdf"
    }
  ]
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "Application submitted successfully",
  "data": {
    "applicationId": "APP-2024-001",
    "status": "submitted",
    "appliedDate": "2024-02-21"
  }
}
```

### Get Farmer Applications
**GET** `/subsidies/applications`

Get all subsidy applications submitted by farmer.

**Response (200):**
```json
{
  "success": true,
  "data": {
    "applications": [
      {
        "applicationId": "APP-2024-001",
        "subsidyName": "Pradhan Mantri Fasal Bima Yojana",
        "status": "under_review",
        "appliedDate": "2024-02-21",
        "expectedAmount": 15000
      }
    ]
  }
}
```

---

## Admin Endpoints

### Get Farm Statistics
**GET** `/admin/stats`

Get overall platform statistics (admin only).

**Response (200):**
```json
{
  "success": true,
  "data": {
    "totalFarmers": 1250,
    "activeCrops": 3450,
    "diseaseDetections": 890,
    "totalYield": "125000 quintals",
    "iotDevices": 670,
    "subsidyApplications": 340
  }
}
```

### Get System Health
**GET** `/admin/health`

Check system status and service health (admin only).

**Response (200):**
```json
{
  "success": true,
  "data": {
    "database": "healthy",
    "cache": "healthy",
    "api": "healthy",
    "uptime": "45 days",
    "memoryUsage": "62%",
    "cpuUsage": "25%"
  }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `INVALID_INPUT` | 400 | Invalid request data |
| `UNAUTHORIZED` | 401 | Missing or invalid JWT token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `DUPLICATE_ENTRY` | 409 | Resource already exists |
| `SERVER_ERROR` | 500 | Internal server error |
| `SERVICE_UNAVAILABLE` | 503 | Service temporarily unavailable |

---

## Pagination

List endpoints support pagination:

**Query Parameters:**
- `page` (default: 1) - Page number
- `limit` (default: 20) - Items per page

**Response includes:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

## Rate Limiting

API endpoints are rate-limited: **100 requests per 15 minutes** per IP address.

When limit is exceeded:
- HTTP Status: 429 Too Many Requests
- Header: `Retry-After: 300` (seconds)

---

## WebSocket Events (Real-Time)

Connect to WebSocket endpoint: `ws://localhost:5000`

### Subscribe to Events
```javascript
socket.on('connect', () => {
  socket.emit('subscribe', {
    channel: 'farmer_notifications',
    farmerId: 'USER_ID'
  });
});

// Listen for disease alerts
socket.on('disease_alert', (data) => {
  console.log('New disease detected:', data);
});

// Listen for weather alerts
socket.on('weather_alert', (data) => {
  console.log('Weather warning:', data);
});

// Listen for price updates
socket.on('price_update', (data) => {
  console.log('Price changed:', data);
});
```

---

**Last Updated**: 2024
**Version**: 1.0.0
