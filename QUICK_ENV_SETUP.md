# 📋 QUICK COPY-PASTE FORMAT FOR HOSTING PLATFORMS

## 🎯 ESSENTIAL VARIABLES (Copy and paste these)

### For Render/Railway/Heroku Environment Variables:

```
TIMEZONE=Asia/Kolkata
ENVIRONMENT=production
GEMINI_API_KEY=AIzaSyDOI3hQ7-oubeNvqKbT4owPy4UOYr9i6Ww
GOOGLE_API_KEY=AIzaSyD4j_iCgS3CkbTi_lvA1ju-CS2cDKQNUvg
WEATHER_API_KEY=ff2cbe677bbfc325d2b615c86a20daef
LOG_LEVEL=INFO
DEBUG=False
```

## 🚀 STEP-BY-STEP FOR RENDER

1. **Go to**: [render.com](https://render.com) → Your BUDDY AI service
2. **Click**: "Environment" tab
3. **Add these variables one by one**:

```
Key: TIMEZONE              Value: Asia/Kolkata
Key: ENVIRONMENT           Value: production
Key: GEMINI_API_KEY        Value: AIzaSyDOI3hQ7-oubeNvqKbT4owPy4UOYr9i6Ww
Key: GOOGLE_API_KEY        Value: AIzaSyD4j_iCgS3CkbTi_lvA1ju-CS2cDKQNUvg
Key: WEATHER_API_KEY       Value: ff2cbe677bbfc325d2b615c86a20daef
Key: LOG_LEVEL             Value: INFO
Key: DEBUG                 Value: False
```

4. **Click**: "Save Changes"
5. **Wait**: 5-10 minutes for automatic redeploy
6. **Test**: Ask "what time is it" to verify fix

## 🎯 MOST IMPORTANT

**The #1 priority is setting TIMEZONE=Asia/Kolkata** - this fixes your time display issue!

---

## ✅ After Setup - Test These:

1. **"what time is it"** → Should show correct Indian time
2. **"what's the weather"** → Should work with weather API
3. **"tell me a joke"** → Should work with Gemini AI
4. **"hello buddy"** → Should respond normally

**If time is still wrong**: Double-check TIMEZONE variable is exactly `Asia/Kolkata`
