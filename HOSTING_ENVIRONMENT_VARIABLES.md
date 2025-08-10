# 🌐 BUDDY AI Assistant - Environment Variables for Hosting

## 📋 Complete List of Environment Variables for Production Hosting

### 🕐 TIMEZONE CONFIGURATION (REQUIRED)
TIMEZONE=Asia/Kolkata

### 🚀 APPLICATION SETTINGS
PORT=8000
ENVIRONMENT=production
DEBUG=False
APP_NAME=BUDDY AI Assistant
VERSION=2.0.0
MAX_MEMORY_SIZE=1000

### 🔑 API KEYS (Optional but Recommended)
GEMINI_API_KEY=AIzaSyDOI3hQ7-oubeNvqKbT4owPy4UOYr9i6Ww
GOOGLE_API_KEY=AIzaSyD4j_iCgS3CkbTi_lvA1ju-CS2cDKQNUvg
WEATHER_API_KEY=ff2cbe677bbfc325d2b615c86a20daef

### 🛡️ SECURITY SETTINGS
ALLOWED_HOSTS=*
CORS_ORIGINS=*

### 📊 LOGGING
LOG_LEVEL=INFO

---

## 🌍 Common Timezone Values

### Asia
- India: Asia/Kolkata
- Japan: Asia/Tokyo
- China: Asia/Shanghai
- Singapore: Asia/Singapore
- UAE: Asia/Dubai

### North America
- Eastern Time: America/New_York
- Central Time: America/Chicago
- Mountain Time: America/Denver
- Pacific Time: America/Los_Angeles
- Canada Eastern: America/Toronto

### Europe
- UK: Europe/London
- Central Europe: Europe/Paris
- Germany: Europe/Berlin
- Italy: Europe/Rome
- Spain: Europe/Madrid

### Australia/Oceania
- Sydney: Australia/Sydney
- Melbourne: Australia/Melbourne
- Perth: Australia/Perth
- New Zealand: Pacific/Auckland

---

## 🔧 Platform-Specific Setup Instructions

### 🎯 RENDER (Recommended)
1. Go to your Render dashboard
2. Select your BUDDY AI service
3. Click "Environment" tab
4. Add each variable one by one:

```
Key: TIMEZONE              Value: Asia/Kolkata
Key: ENVIRONMENT           Value: production
Key: GEMINI_API_KEY        Value: [your-actual-key]
Key: GOOGLE_API_KEY        Value: [your-actual-key]
Key: WEATHER_API_KEY       Value: [your-actual-key]
Key: LOG_LEVEL             Value: INFO
```

5. Click "Save Changes" after adding all variables
6. Render will automatically redeploy

### 🚂 RAILWAY
1. Go to your Railway dashboard
2. Select your project
3. Go to "Variables" tab
4. Add variables:

```
TIMEZONE = Asia/Kolkata
ENVIRONMENT = production
GEMINI_API_KEY = [your-actual-key]
GOOGLE_API_KEY = [your-actual-key]
WEATHER_API_KEY = [your-actual-key]
LOG_LEVEL = INFO
```

### 🟣 HEROKU
1. Go to your Heroku dashboard
2. Select your app
3. Go to "Settings" → "Config Vars"
4. Click "Reveal Config Vars"
5. Add each variable:

```
TIMEZONE: Asia/Kolkata
ENVIRONMENT: production
GEMINI_API_KEY: [your-actual-key]
GOOGLE_API_KEY: [your-actual-key]
WEATHER_API_KEY: [your-actual-key]
LOG_LEVEL: INFO
```

### ☁️ VERCEL
1. Go to your Vercel dashboard
2. Select your project
3. Go to "Settings" → "Environment Variables"
4. Add variables for each environment (Production, Preview, Development)

---

## 🔑 Your Actual API Keys

Based on your .env file, here are your API keys:

```
GEMINI_API_KEY=AIzaSyDOI3hQ7-oubeNvqKbT4owPy4UOYr9i6Ww
GOOGLE_API_KEY=AIzaSyD4j_iCgS3CkbTi_lvA1ju-CS2cDKQNUvg
WEATHER_API_KEY=ff2cbe677bbfc325d2b615c86a20daef
```

## ⚠️ SECURITY REMINDER

1. **Never commit API keys to Git**
2. **Use environment variables only**
3. **Keep your .env file local**
4. **Regenerate keys if accidentally exposed**

---

## ✅ Quick Setup Checklist

- [ ] Set TIMEZONE (fixes time display issue)
- [ ] Set ENVIRONMENT=production
- [ ] Add GEMINI_API_KEY (for AI responses)
- [ ] Add GOOGLE_API_KEY (for enhanced features)
- [ ] Add WEATHER_API_KEY (for weather features)
- [ ] Set LOG_LEVEL=INFO
- [ ] Save and redeploy
- [ ] Test "what time is it" to verify timezone fix

---

## 🎯 Priority Environment Variables

### Must Have (Required):
1. **TIMEZONE** - Fixes time display issue
2. **ENVIRONMENT** - Sets production mode

### Highly Recommended:
3. **GEMINI_API_KEY** - Enables AI responses
4. **WEATHER_API_KEY** - Enables weather features
5. **GOOGLE_API_KEY** - Enhanced search capabilities

### Optional:
6. **LOG_LEVEL** - Better debugging
7. **DEBUG** - Should be False for production

---

## 🧪 Testing After Setup

After adding environment variables:

1. **Wait 5-10 minutes** for redeploy
2. **Test timezone**: Ask "what time is it"
3. **Test AI**: Ask any general question
4. **Test weather**: Ask "weather in [city]"
5. **Verify logs**: Check for any errors

**Expected Results:**
- ✅ Correct local time display
- ✅ AI responses working
- ✅ Weather information available
- ✅ No timezone-related errors
