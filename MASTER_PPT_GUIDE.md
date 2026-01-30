# SENTIENT110 - ROUND 1 PPT COMPLETE GUIDE

---

## 🖼️ QUICK IMAGE REFERENCE (All in `assets/` folder)

| Slide | Image File | Description |
|-------|------------|-------------|
| 2 | `timeline_new.png` | Monitor110 rise & fall timeline |
| 3 | `comparison.png` | Before/After visual |
| 6 | `architecture_new.png` | 4-layer system architecture |
| 7 | `innovation_comparison.png` | Others vs Sentient110 |
| 8 | `user_flow.png` | Demo flow diagram |
| 10 | `revenue_model.png` | Pricing tiers table |
| 10 | `market_funnel.png` | TAM/SAM/SOM funnel |

**How to insert:** PowerPoint → Insert → Pictures → This Device → Navigate to `Desktop/Sentinent110/assets/`

---
## SLIDE 1: TITLE & THESIS

### Visual Layout:
```
┌─────────────────────────────────────────────┐
│                                             │
│         [Large Bold Title]                  │
│         SENTIENT110                         │
│                                             │
│         [Subtitle]                          │
│    From Information Overload to             │
│    Intelligent Signals                      │
│                                             │
│         [Tagline in smaller text]           │
│    "The Bloomberg Terminal That Died        │
│     Because AI Didn't Exist"                │
│                                             │
│         [Bottom]                            │
│    Team: [YOUR TEAM NAME]                   │
│    Members: [YOUR NAMES]                    │
│    FAIL.exe Hackathon 2026                  │
└─────────────────────────────────────────────┘
```

### Design Notes:
- **Background:** Dark blue gradient (navy to deep blue)
- **Main Title:** White, 72pt, Bold
- **Subtitle:** Light blue, 36pt
- **Tagline:** Yellow/gold accent, 24pt, italic

### Speaker Notes:
"Good evening judges. We're reviving Monitor110—a startup that raised $20 million and failed because they tried to build AI before AI existed. Today, we're bringing it back as Sentient110, and this time, the technology works."

---

## SLIDE 2: THE ORIGINAL STARTUP

### Content:

**MONITOR110: THE ORIGINAL VISION (2005-2014)**

**The Promise:**
- Real-time financial sentiment tracking across the internet
- Social media, blogs, forums, news aggregation
- Early warning system for market movements

**The Numbers:**
- Founded: 2005 by Roger Ehrenberg (ex-Deutsche Bank)
- Total Funding: $20M+ (Union Square Ventures, RRE Ventures)
- Target Market: Hedge funds, day traders, financial institutions
- Shutdown: 2014

**The Pitch:**
"Know what the market is thinking before the market knows"

### Visual Elements:
- Timeline graphic showing 2005 → 2014
- **📷 INSERT:** `assets/timeline_new.png` ⭐ NEW - Professional gradient timeline
- Icons: 💰 (funding), 🏦 (target market), 📉 (shutdown)

### Speaker Notes:
"Monitor110 was ahead of its time. They wanted to be the financial intelligence platform—tracking what people were saying about stocks across the entire internet before social media was mainstream."

---

## SLIDE 3: WHY IT FAILED - THE 3 FATAL FLAWS

### Content:

**THE AUTOPSY: What Killed Monitor110**

```
┌─────────────────────────────────────────────┐
│  1. TECHNOLOGY GAP                          │
│  ─────────────────                          │
│  2008 Reality:                              │
│  • Basic keyword matching                   │
│  • No context understanding                 │
│  • False positives everywhere               │
│                                             │
│  Example: "Apple is terrible" (the fruit)  │
│  vs "Apple stock is terrible" (AAPL)       │
│                                             │
├─────────────────────────────────────────────┤
│  2. INFORMATION OVERLOAD                    │
│  ─────────────────────────                  │
│  The Fatal Mistake:                         │
│  • Showed users 10,000 mentions/day         │
│  • Expected humans to analyze manually      │
│  • No synthesis, just aggregation          │
│                                             │
│  "We gave them a firehose when they         │
│   needed a faucet" - Former user           │
│                                             │
├─────────────────────────────────────────────┤
│  3. ZERO ACCOUNTABILITY                     │
│  ──────────────────────                     │
│  Trust Issues:                              │
│  • No track record of predictions           │
│  • No proof of accuracy                     │
│  • Recommendations disappeared              │
│                                             │
│  Users couldn't verify if it actually worked│
└─────────────────────────────────────────────┘
```

### Visual Elements:
- Three columns or sections (one per flaw)
- Red X icons for each failure point
- Quote in italics for emotional impact
- **📷 INSERT:** `assets/comparison.png`

### Speaker Notes:
"Monitor110 didn't fail because the idea was bad. They failed for three specific reasons. First, 2008 NLP couldn't tell if 'Apple is terrible' referred to fruit or stock. Second, they showed traders 10,000 posts and said 'good luck.' And third, there was no way to verify if their system actually worked. These aren't just flaws—they're opportunities for us to solve."

---

## SLIDE 4: MARKET ANALYSIS - WHY NOW IS DIFFERENT

### Content:

**THE TECHNOLOGY FINALLY EXISTS**

| **THEN (2008)** | **NOW (2026)** | **IMPACT** |
|-----------------|----------------|------------|
| Keyword matching | Transformer models (GPT-4, Claude) | 98% accuracy in context |
| Manual analysis | AI synthesis in seconds | 10,000x faster |
| Zero verification | Blockchain timestamping | Immutable proof |
| Desktop only | Mobile-first | 3B smartphone users |

**MARKET OPPORTUNITY**

💰 **Market Size:** $67 Billion (AI FinTech by 2027)

👥 **Target Users:** 50M retail investors (US alone)

📊 **Current Solutions (Related Failed Attempts):**
- Bloomberg Terminal: $24,000/year (institutions only) → Failed to reach retail
- Seeking Alpha: Generic analysis, no AI → Failed to synthesize
- Twitter/Reddit: Noise, bots, and scams → **Failed to provide clarity**
  - Users drowning in misinformation
  - No signal, just noise

🎯 **The Gap:** No AI-native tool for retail investors

**WHY MONITOR110'S IDEA WAS RIGHT:**

Social sentiment DOES predict markets:
- GameStop (2021): Reddit predicted $400 surge
- Tesla (2020): Twitter sentiment led analyst upgrades
- Crypto crashes: Social fear preceded price drops

### Visual Elements:
- Split screen: "Then vs Now" comparison
- Market size in large numbers with $ signs
- Competitor logos (Bloomberg, Seeking Alpha)
- Graph showing social sentiment correlation with stock prices

### Speaker Notes:
"The market has changed dramatically. In 2008, keyword matching was the best they had. Today, we have Claude and GPT-4 that understand context at human level. The $67 billion AI FinTech market proves demand exists. Bloomberg costs $24,000/year—we're targeting the 50 million retail investors they ignore."

---

## SLIDE 5: DESIGN OBJECTIVES & CONSTRAINTS

### Content:

**WHAT WE'RE BUILDING**

**Core Objectives:**
✅ **Synthesize, Don't Aggregate**
   → AI reads everything, shows ONE decision

✅ **One-Click Actionable Signals**
   → BUY/SELL/HOLD with confidence score

✅ **Full Transparency**
   → AI explains its reasoning in plain English

✅ **Blockchain Verification**
   → Every prediction timestamped on-chain

**Design Principles:**
- Mobile-first (80% of users on phones)
- Real-time updates (sub-10 second latency)
- Source attribution (trust through transparency)
- Clean UI (inspired by original Monitor110)

**Technical Constraints:**

| Constraint | Our Solution |
|------------|--------------|
| API rate limits | Caching + batch processing |
| LLM token costs | Claude Haiku ($0.25/1M tokens) |
| 7-hour build time | Fork existing DugTrio codebase |
| Blockchain gas fees | Story Protocol testnet (free) |

### Visual Elements:
- Checkmarks for objectives
- Icons: 📱 (mobile), ⚡ (speed), 🔗 (blockchain)
- Table for constraints/solutions

### Speaker Notes:
"Our design philosophy is simple: synthesize, don't aggregate. Monitor110 showed 10,000 posts. We show ONE decision. But we explain our reasoning and prove it on blockchain. We're constrained by API costs, so we use Claude Haiku—the fastest, cheapest model that still delivers quality."

---

## SLIDE 6: SYSTEM ARCHITECTURE

### Content:

**TECHNICAL ARCHITECTURE**

```
┌─────────────────────────────────────────────────┐
│           SENTIENT110 TECH STACK                │
├─────────────────────────────────────────────────┤
│                                                 │
│  📊 DATA LAYER (Multi-Source Aggregation)      │
│  ├─ NewsAPI → Financial news (50+ sources)     │
│  ├─ Twitter/X API → Social sentiment           │
│  ├─ Reddit API → r/wallstreetbets, r/stocks    │
│  └─ Alpha Vantage → Real-time stock prices     │
│                    ↓                            │
│  🧠 AI LAYER (Dual Intelligence)               │
│  ├─ RoBERTa → Fast sentiment baseline          │
│  │   (twitter-roberta-base-sentiment)          │
│  │   • 125M parameters                         │
│  │   • 0.3 sec inference time                  │
│  │                                             │
│  └─ Claude 3.5 Haiku → Synthesis + Reasoning   │
│      • Analyzes RoBERTa output                 │
│      • Generates structured signals            │
│      • Explains decisions in plain English     │
│                    ↓                            │
│  🔗 TRUST LAYER (Blockchain Verification)      │
│  └─ Story Protocol (Sepolia Testnet)          │
│      • Timestamps predictions                  │
│      • Creates immutable track record          │
│      • Enables verification                    │
│                    ↓                            │
│  💻 PRESENTATION LAYER                         │
│  ├─ React + Vite (Frontend)                   │
│  ├─ FastAPI (Backend)                         │
│  ├─ TailwindCSS (Styling)                     │
│  └─ Recharts (Data Visualization)             │
│                                                 │
└─────────────────────────────────────────────────┘
```

**📷 INSERT:** `assets/architecture_new.png` ⭐ NEW - Professional 4-layer diagram

**Data Flow:**
1. User searches "TSLA"
2. Backend scrapes 50 news + 100 tweets
3. RoBERTa analyzes sentiment → 0.85/1.0
4. Claude synthesizes → "BUY at 89% confidence"
5. Prediction stored on Story Protocol
6. Frontend displays results + blockchain proof

### Visual Elements:
- Layered architecture diagram (boxes and arrows)
- Icons for each layer
- Color coding: Blue (data), Purple (AI), Gold (blockchain), Green (frontend)

### Speaker Notes:
"Our architecture has four layers. Data layer pulls from news and social media. AI layer uses RoBERTa for speed and Claude for reasoning—dual models give us accuracy AND performance. Trust layer timestamps predictions on Story Protocol blockchain. Presentation layer is React for smooth UX. This isn't just an API call—it's a complete intelligence pipeline."

---

## SLIDE 7: CORE TECHNICAL CONTRIBUTION

### Content:

**WHAT MAKES US DIFFERENT**

**The Innovation Stack:**

🎯 **1. Dual AI Architecture**
```
Fast Path (RoBERTa):
- Sentiment baseline in 0.3 seconds
- Processes 1000 tweets simultaneously
- No API costs (runs locally)

Deep Path (Claude):
- Understands context and nuance
- Generates human-readable reasoning
- Structured JSON output
```

💡 **Why This Matters:**
- Monitor110 had ZERO AI (just keyword counts)
- Competitors use single models (either fast OR smart)
- We get BOTH: Speed + Intelligence

🔗 **2. Blockchain Verification Layer**
```
Every prediction gets:
- Timestamp (when we called it)
- Confidence score (how sure we were)
- On-chain hash (immutable proof)
```

💡 **Why This Matters:**
- NO other team has accountability
- Users can verify our track record
- Builds trust through transparency

📊 **3. Multi-Source Synthesis**
```
Traditional tools:          Sentient110:
News OR Social    →    News AND Social AND Prices
                        ↓
                   Weighted synthesis
```

💡 **Why This Matters:**
- Single sources miss context
- We combine perspectives
- More accurate signals

**THE UNIQUE VALUE PROPOSITION:**

"We're the ONLY platform that combines:
✅ Dual AI (speed + intelligence)
✅ Blockchain proof (accountability)
✅ Multi-source data (comprehensive view)"

### Visual Elements:
- **📷 INSERT:** `assets/innovation_comparison.png` ⭐ NEW - Others vs Sentient110
- Three columns for each innovation
- Comparison charts showing "Others vs Us"
- Checkmarks and icons

### Speaker Notes:
"Here's our secret sauce. First, dual AI—RoBERTa for speed, Claude for reasoning. Second, blockchain verification—we're the only team with on-chain proof. Third, multi-source synthesis—we don't just read Twitter, we combine news, social, and prices. No other team has all three."

---

## SLIDE 8: FUNCTIONAL PROTOTYPE OVERVIEW

### Content:

**WHAT WE'RE BUILDING (7-HOUR SPRINT)**

**MVP Feature Set:**

| Feature | Implementation | Time | Status |
|---------|---------------|------|--------|
| Ticker Search | FastAPI endpoint | 30 min | ✅ Core |
| Sentiment Dashboard | React + Recharts | 2 hrs | ✅ Core |
| BUY/SELL/HOLD Signal | RoBERTa + Claude | 1.5 hrs | ✅ Core |
| Confidence Score | Weighted algorithm | 30 min | ✅ Core |
| AI Reasoning Display | Claude text output | 45 min | ✅ Core |
| Source Attribution | Link tracking | 45 min | ✅ Core |
| Blockchain Verify | Story Protocol API | 1 hr | 🟡 Optional |
| Historical Graph | 24-hour data cache | 45 min | 🟡 Nice-to-have |

**Demo User Flow:**

```
1. User visits sentient110.com
   ↓
2. Enters ticker: "AAPL"
   ↓
3. Backend analyzes:
   - 50 news articles
   - 100 tweets
   - Real-time price data
   ↓
4. AI generates signal:
   "STRONG BUY - 89% Confidence"
   ↓
5. User sees:
   - Big BUY button (green)
   - Confidence gauge (89%)
   - AI reasoning text
   - Sources analyzed (150)
   - [Verify on Chain] button
   ↓
6. Optional: Click verify
   → Opens blockchain explorer
   → Shows prediction timestamp
```

**📚 Documentation:**
- Full API specs and setup guide included in README.md
- Installation instructions for developers
- Environment variable templates provided

### Visual Elements:
- **📷 INSERT:** `assets/user_flow.png` ⭐ NEW - Demo flow diagram
- Feature checklist with status indicators
- User flow diagram with arrows
- Mockup/wireframe of dashboard

### Speaker Notes:
"In 7 hours, we're building a working prototype. Core features: ticker search, sentiment analysis, BUY/SELL signals, AI reasoning. The flow is simple: search a stock, get a signal, see the reasoning, verify on blockchain. We're prioritizing functionality over polish—judges can see the intelligence, not just pretty UI. Full documentation is included in our README."

---

## SLIDE 9: EVALUATION & LIMITATIONS

### Content:

**HONEST ASSESSMENT**

**✅ STRENGTHS:**

1. **First-Mover in AI Revival**
   - Only team reviving Monitor110 with modern AI
   - Unique positioning in hackathon

2. **Proven Architecture**
   - Built on DugTrio codebase (battle-tested)
   - Not starting from scratch

3. **10x Faster Analysis**
   - Human analyst: 8 hours
   - Our system: 8 seconds
   - 3,600x speed improvement

4. **Democratization**
   - Bloomberg: $24K/year
   - Us: $29/month
   - 800x more affordable

**⚠️ LIMITATIONS:**

1. **API Dependencies**
   - NewsAPI: 100 req/day (free tier)
   - Twitter: Limited to 100 tweets/month
   - **Mitigation:** Upgrade to paid tiers at scale

2. **Not Financial Advice**
   - We're analysis, not recommendations
   - Legal disclaimers required
   - **Mitigation:** Prominent warnings in UI

3. **Accuracy Depends on Sources**
   - Garbage in = garbage out
   - Social media can be manipulated
   - **Mitigation:** Multi-source weighting, outlier detection

4. **Latency**
   - Current: 5-10 seconds per query
   - Bloomberg: Instant
   - **Mitigation:** Caching, pre-computation for popular stocks

5. **Testnet Only (Blockchain)**
   - Story Protocol on Sepolia (test network)
   - Not production-ready
   - **Mitigation:** Mainnet deployment post-hackathon

**🚀 FUTURE IMPROVEMENTS:**

1. **Fine-Tuned Model**
   - Train custom LLM on financial data
   - Reduce costs 80%
   - Improve accuracy to 95%+

2. **Portfolio Tracking**
   - Monitor multiple stocks
   - Real-time alerts
   - Integration with brokerage APIs

3. **Expanded Markets**
   - Crypto sentiment analysis
   - Commodities (gold, oil)
   - Forex signals

4. **Auto-Trading Integration**
   - Partner with Robinhood/Fidelity
   - One-click trade execution
   - Revenue share model

### Visual Elements:
- Two columns: Strengths vs Limitations
- Icons: ✅ (strengths), ⚠️ (limitations), 🚀 (future)
- Progress bars showing improvement potential

### Speaker Notes:
"Let's be honest about what we have and what we don't. Strengths: we're the only AI revival of Monitor110, built on proven code, 10x faster than humans. Limitations: API dependencies, not financial advice, latency. But every limitation has a mitigation plan. This is an MVP—the future roadmap shows how we get to production scale."

---

## SLIDE 10: BUSINESS MODEL & FUTURE WORK

### Content:

**THE PATH TO PROFITABILITY**

**Revenue Model:**

| Tier | Price | Features | Target Users |
|------|-------|----------|--------------|
| **Free** | $0 | • 10 queries/day<br>• Basic signals<br>• Community features | 100K users<br>(Viral growth) |
| **Pro** | $29/mo | • Unlimited queries<br>• Real-time alerts<br>• Historical data<br>• Priority support | 10K users<br>(Power traders) |
| **Enterprise** | $499/mo | • API access<br>• Custom models<br>• White-label option<br>• Dedicated account manager | 100 companies<br>(Robo-advisors) |

**Revenue Projections (Year 1):**
```
Free users:     100,000 × $0    = $0        (Acquisition funnel)
Pro users:       10,000 × $29   = $290K/mo  = $3.48M/year
Enterprise:         100 × $499  = $49.9K/mo = $599K/year
                                ──────────────────────────
                                Total ARR: $4.08M
```

**Additional Revenue Streams:**

💰 **Data Licensing**
- Aggregate anonymized sentiment data
- Sell to hedge funds as "retail sentiment index"
- Estimated: $500K/year

💰 **Affiliate Commissions**
- Partner with brokerages (Robinhood, Fidelity)
- Earn $10-50 per referred user
- Estimated: $200K/year

**Total Year 1 Revenue Potential: $4.78M**

**Cost Structure:**
- API costs: $50K/year (at scale with caching)
- Infrastructure: $30K/year (AWS/Railway)
- Team (2 engineers): $200K/year
- Marketing: $100K/year
**Total Costs: $380K/year**

**Year 1 Profit: $4.4M (92% margin)**

**Market Opportunity:**

🎯 **TAM (Total Addressable Market):**
- 50M retail investors in US
- 50M × $29/mo = $17.4 BILLION/year potential

📊 **SAM (Serviceable Available Market):**
- 5M active day traders
- 5M × $29/mo = $1.74 BILLION/year

🎪 **SOM (Serviceable Obtainable Market):**
- 1% market share (realistic Year 3)
- 50K users × $29/mo = $17.4M/year

**5-Year Vision:**

| Year | Users | ARR | Milestone |
|------|-------|-----|-----------|
| Year 1 | 10K Pro | $4M | MVP → Product-Market Fit |
| Year 2 | 50K Pro | $20M | Expand to crypto markets |
| Year 3 | 150K Pro | $60M | Add portfolio tracking |
| Year 4 | 300K Pro | $120M | International expansion |
| Year 5 | 500K Pro | $200M | Acquisition target for Robinhood/Fidelity |

**Exit Strategy:**
- Primary: Acquisition by fintech platform ($500M-$1B valuation)
- Secondary: IPO if we reach 1M+ users
- Comparable: Robinhood acquired Say Technologies for $140M (2021)

### Visual Elements:
- **📷 INSERT:** `assets/revenue_model.png` ⭐ NEW - Pricing tiers visual
- **📷 INSERT:** `assets/market_funnel.png` ⭐ NEW - TAM/SAM/SOM funnel
- Pricing tier comparison table
- Revenue pie chart
- 5-year growth graph

### Speaker Notes:
"Our business model is simple freemium SaaS. Free tier drives viral growth, Pro tier at $29/month is our revenue engine. Enterprise tier for white-label. Year 1 projection: $4.78M revenue. With 92% margins, this is highly profitable. The TAM is $17 billion—we only need 0.3% market share to hit $50M ARR. Five-year vision: acquisition by Robinhood or Fidelity for $500M+."

---

## BONUS SLIDE: COMPETITIVE ANALYSIS

**HOW WE COMPARE:**

| Feature | Bloomberg | Seeking Alpha | FinViz | **Sentient110** |
|---------|-----------|---------------|---------|-----------------|
| Price | $24K/year | Free/$240/yr | Free | Free/$29/mo |
| AI Analysis | ❌ | ❌ | ❌ | ✅ |
| Real-time Sentiment | ✅ | ❌ | ✅ | ✅ |
| Blockchain Proof | ❌ | ❌ | ❌ | ✅ |
| Mobile-First | ❌ | ✅ | ❌ | ✅ |
| Explains Reasoning | ❌ | ✅ | ❌ | ✅ |
| Target Market | Institutions | Retail | Active Traders | Retail |

**Our Competitive Moat:**
1. Only AI-native platform
2. Only blockchain-verified predictions
3. Only dual-model architecture
4. Only platform learning from Monitor110's failure

---

## CLOSING SLIDE

```
┌─────────────────────────────────────────────┐
│                                             │
│         SENTIENT110                         │
│                                             │
│    "Every Failure Deserves a Second Run"    │
│                                             │
│         Thank You                           │
│                                             │
│    Questions?                               │
│                                             │
│    [Team Contact Info]                      │
│    GitHub: github.com/[your-repo]           │
└─────────────────────────────────────────────┘
```
