# VISUAL DIAGRAMS & FLOWCHARTS FOR PPT

---

## 🖼️ READY-TO-USE IMAGES (All in `assets/` folder)

| Slide | Image File | Description |
|-------|------------|-------------|
| 2 | `timeline_new.png` | Monitor110 rise & fall |
| 3 | `comparison.png` | Before/After visual |
| 6 | `architecture_new.png` | 4-layer system diagram |
| 7 | `innovation_comparison.png` | Others vs Sentient110 |
| 8 | `user_flow.png` | Demo flow diagram |
| 10 | `revenue_model.png` | Pricing tiers |
| 10 | `market_funnel.png` | TAM/SAM/SOM funnel |

> **💡 TIP:** Use these pre-made images instead of creating diagrams manually!

---
## DIAGRAM 1: SYSTEM ARCHITECTURE (Slide 6)

### How to Create in PowerPoint:

**Step 1: Use SmartArt**
1. Insert → SmartArt → Process → Vertical Process
2. Add 4 main boxes (one per layer)

**Step 2: Color Scheme**
- Data Layer: Light Blue (#4A90E2)
- AI Layer: Purple (#9B59B6)
- Trust Layer: Gold (#F39C12)
- Frontend Layer: Green (#27AE60)

### Text for Each Box:

```
┌─────────────────────────────────┐
│   DATA LAYER                    │
│   • NewsAPI                     │
│   • Twitter/X API               │
│   • Reddit API                  │
│   • Alpha Vantage               │
└─────────────────────────────────┘
         ↓ (arrow)
┌─────────────────────────────────┐
│   AI LAYER                      │
│   • RoBERTa (Fast)              │
│   • Claude 3.5 (Smart)          │
└─────────────────────────────────┘
         ↓ (arrow)
┌─────────────────────────────────┐
│   TRUST LAYER                   │
│   • Story Protocol              │
│   • Blockchain Verification     │
└─────────────────────────────────┘
         ↓ (arrow)
┌─────────────────────────────────┐
│   PRESENTATION                  │
│   • React Frontend              │
│   • FastAPI Backend             │
└─────────────────────────────────┘
```

### Alternative: Use Shapes
1. Insert → Shapes → Rectangle
2. Draw 4 rectangles stacked vertically
3. Insert → Shapes → Arrow (between each rectangle)
4. Right-click → Format Shape → Fill Color

**📷 USE THIS:** `assets/architecture_new.png` ⭐ (Professional 4-layer diagram already generated!)

---

## DIAGRAM 2: DATA FLOW (Slide 6 or 7)

### Step-by-Step Flowchart:

```
   [User]
     ↓
   Enters "TSLA"
     ↓
┌─────────────────┐
│  Data Scraper   │
│  Fetches:       │
│  • 50 news      │
│  • 100 tweets   │
│  • Stock price  │
└─────────────────┘
     ↓
┌─────────────────┐
│  RoBERTa AI     │
│  Sentiment:     │
│  0.85/1.0       │
│  (Positive)     │
└─────────────────┘
     ↓
┌─────────────────┐
│  Claude AI      │
│  Synthesizes:   │
│  "BUY - 89%"    │
│  + Reasoning    │
└─────────────────┘
     ↓
┌─────────────────┐
│  Blockchain     │
│  Stores hash    │
│  on Story       │
└─────────────────┘
     ↓
   [Display to User]
   • Signal: BUY
   • Confidence: 89%
   • Reasoning text
   • Verify link
```

### PowerPoint Instructions:
1. Insert → SmartArt → Process → Basic Process
2. Add 6 steps
3. Format each step with icon (Insert → Icons)
4. Add arrows between steps

---

## DIAGRAM 3: COMPARISON TABLE (Slide 4)

### Then vs Now Comparison:

Create a 2-column table in PowerPoint:

| THEN (2008) | NOW (2026) |
|-------------|------------|
| ❌ Keyword matching | ✅ Transformer AI |
| ❌ Manual analysis | ✅ Automated synthesis |
| ❌ No verification | ✅ Blockchain proof |
| ❌ Desktop only | ✅ Mobile-first |
| ❌ Information overload | ✅ One-click signals |

**Formatting:**
- Header row: Dark background, white text
- Use red X (❌) and green check (✅) emojis
- Alternate row colors (light gray/white)

**📷 USE THIS:** `assets/comparison.png` (already generated!)

---

## DIAGRAM 4: REVENUE MODEL (Slide 10)

### Pricing Tier Comparison:

Create a 3-column comparison table:

```
┌─────────────┬─────────────┬─────────────┐
│    FREE     │     PRO     │ ENTERPRISE  │
├─────────────┼─────────────┼─────────────┤
│    $0/mo    │   $29/mo    │  $499/mo    │
├─────────────┼─────────────┼─────────────┤
│ 10 queries/ │  Unlimited  │ API Access  │
│    day      │   queries   │             │
│             │             │             │
│ Basic       │ Real-time   │ Custom      │
│ signals     │  alerts     │  models     │
│             │             │             │
│ Community   │ Historical  │ White-label │
│ features    │   data      │   option    │
│             │             │             │
│             │ Priority    │ Dedicated   │
│             │  support    │  manager    │
├─────────────┼─────────────┼─────────────┤
│   100K      │    10K      │     100     │
│   users     │   users     │  companies  │
└─────────────┴─────────────┴─────────────┘
```

**📷 USE THIS:** `assets/revenue_model.png` ⭐ (Professional pricing table already generated!)

---

## DIAGRAM 5: MARKET FUNNEL (Slide 10)

### TAM/SAM/SOM Visualization:

```
        ┌───────────────────────────┐
        │   TAM: $17.4B/year        │
        │   (50M retail investors)  │
        └───────────┬───────────────┘
                    │
            ┌───────▼───────┐
            │  SAM: $1.74B  │
            │  (5M traders) │
            └───────┬───────┘
                    │
               ┌────▼────┐
               │SOM: $17M│
               │(50K usr)│
               └─────────┘
```

**📷 USE THIS:** `assets/market_funnel.png` ⭐ (Professional funnel already generated!)

---

## DIAGRAM 6: 5-YEAR GROWTH (Slide 10)

### Line Graph:

```
ARR ($M)
  │
200├                            ●
  │                         ●
150│                    ●
  │               ●
100├          ●
  │      ●
 50├  ●
  │●
  0└────────────────────────────
     Y1  Y2  Y3  Y4  Y5
```

**PowerPoint:**
1. Insert → Chart → Line Chart
2. Data points:
   - Year 1: $4M
   - Year 2: $20M
   - Year 3: $60M
   - Year 4: $120M
   - Year 5: $200M
3. Format: Blue line, white background, gridlines

---

## DIAGRAM 7: COMPETITIVE MATRIX (Bonus Slide)

### Feature Comparison Grid:

```
                Bloomberg  Seeking  FinViz  Sentient110
                            Alpha
Price           $24K        Free    Free    $29/mo
AI Analysis       ❌         ❌      ❌       ✅
Real-time         ✅         ❌      ✅       ✅
Blockchain        ❌         ❌      ❌       ✅
Mobile-First      ❌         ✅      ❌       ✅
Reasoning         ❌         ✅      ❌       ✅
```

**PowerPoint:**
1. Insert → Table → 5 columns, 7 rows
2. Use checkmarks (✅) and X marks (❌)
3. Highlight Sentient110 column in light blue
4. Bold the checkmarks in your column

---

## ICON SUGGESTIONS

### Where to Find Icons:
- PowerPoint: Insert → Icons (built-in)
- Free resources: flaticon.com, thenounproject.com

### Recommended Icons by Slide:

**Slide 1-2:**
- 💰 Money bag (funding)
- 📊 Chart (analytics)
- 🏦 Bank building (target market)

**Slide 3:**
- ❌ Red X (failures)
- ⚠️ Warning triangle (problems)
- 💔 Broken heart (shutdown)

**Slide 4:**
- ✅ Green check (solutions)
- 📈 Trending up (growth)
- 🌐 Globe (market)

**Slide 5-6:**
- 🧠 Brain (AI)
- 🔗 Chain link (blockchain)
- ⚡ Lightning bolt (speed)
- 📱 Mobile phone (mobile-first)

**Slide 7:**
- 🎯 Target (precision)
- 🔬 Microscope (analysis)
- 🛡️ Shield (trust)

**Slide 8:**
- ✅ Checkmarks (features complete)
- 🟡 Yellow circle (in progress)
- 🔄 Refresh (real-time)

**Slide 10:**
- 💰 Dollar signs (revenue)
- 📊 Growth chart
- 🎯 Target (goals)

---

## COLOR PALETTE

### Brand Colors for Sentient110:

**Primary:**
- Navy Blue: #1A237E (backgrounds)
- Sky Blue: #4A90E2 (accents)

**Secondary:**
- Gold: #F39C12 (highlights)
- Purple: #9B59B6 (AI elements)
- Green: #27AE60 (success/positive)
- Red: #E74C3C (warnings/negative)

**Neutral:**
- White: #FFFFFF (text on dark)
- Light Gray: #F5F5F5 (backgrounds)
- Dark Gray: #333333 (text on light)

### Usage Guide:
- Slide backgrounds: Navy Blue gradient to Sky Blue
- Text on dark: White
- Headers: Gold or Sky Blue
- AI-related items: Purple
- Positive metrics: Green
- Problems/failures: Red

---

## TYPOGRAPHY RECOMMENDATIONS

### Fonts:
**Primary:** Montserrat (modern, tech-focused)
- Headers: Montserrat Bold
- Body: Montserrat Regular

**Alternative (if Montserrat unavailable):** Arial or Calibri

### Font Sizes:
- Slide Title: 44-54pt
- Section Headers: 32-36pt
- Body Text: 18-24pt
- Captions: 14-16pt

---

## LAYOUT TEMPLATES

### Template 1: Title Slide
```
[Logo/Icon - Top Left]

[Large Title - Center]
SENTIENT110

[Subtitle - Below Title]
From Information Overload to Intelligent Signals

[Tagline - Below Subtitle, Italic]
"The Bloomberg Terminal That Died Because AI Didn't Exist"

[Team Info - Bottom Center]
Team Name | Member Names
FAIL.exe Hackathon 2026
```

### Template 2: Content Slide
```
[Slide Number] - [Slide Title]

[Left Column - 60%]       [Right Column - 40%]
• Bullet points            [Image/Diagram/Chart]
• Key information
• Data points

[Footer]
Sentient110 | FAIL.exe 2026
```

### Template 3: Full-Width Slide
```
[Slide Title]

[Full-width content area]
• Large diagram
• Full table
• Wide chart

[Footer]
```

---

## ANIMATION TIPS (Optional)

### Slide 6 (Architecture):
1. Fade in each layer sequentially
2. Arrows appear after boxes
3. Build from top to bottom

### Slide 8 (Features):
1. Checkmarks appear one by one
2. Each row fades in with sound effect

### Slide 10 (Revenue):
1. Numbers count up (if PowerPoint supports)
2. Graph draws from left to right

**Keep animations MINIMAL for professional look!**

---

## EXPORT SETTINGS

### Before Submitting:

1. **File → Save As**
   - Format: PowerPoint Presentation (.pptx)
   - Name: Sentient110_Round1_[TeamName].pptx

2. **Also Export as PDF**
   - File → Export → Create PDF
   - In case Google Form only accepts PDF

3. **Check File Size**
   - Keep under 10MB
   - Compress images if needed (Picture Tools → Compress)

4. **Test on Another Computer**
   - Open PPT on different device
   - Ensure fonts display correctly
   - Check all images appear

---

## 🖼️ ALL PRE-MADE IMAGES (Use These!)

```
Sentinent110/assets/
├── architecture_new.png  → Slide 6 ⭐
├── timeline_new.png     → Slide 2 ⭐
├── comparison.png       → Slide 3
├── innovation_comparison.png → Slide 7 ⭐
├── user_flow.png        → Slide 8 ⭐
├── revenue_model.png    → Slide 10 ⭐
└── market_funnel.png    → Slide 10 ⭐
```

**How to insert:**
1. PowerPoint → Insert → Pictures → This Device
2. Navigate to `Desktop/Sentinent110/assets/`
3. Select image → Insert → Resize to fit

**These save you 1+ hour of diagram creation!**
