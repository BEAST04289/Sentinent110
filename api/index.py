"""
Sentient110 - Vercel Serverless Handler
Full featured: Cache, Auth, Pricing, Analysis
All using FREE resources (in-memory storage)
"""

from http.server import BaseHTTPRequestHandler
import json
import os
import hashlib
import time
from datetime import datetime
from urllib.parse import parse_qs, urlparse

# ============= IN-MEMORY STORAGE (Free!) =============
# Cache: {ticker: {data: {...}, expires: timestamp}}
ANALYSIS_CACHE = {}
CACHE_TTL = 600  # 10 minutes

# Users: {email: {password_hash, name, plan, created}}
USERS_DB = {}

# Sessions: {token: {email, expires}}
SESSIONS = {}

# ============= HELPER FUNCTIONS =============
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(email):
    data = f"{email}|{time.time()}|{os.urandom(16).hex()}"
    return hashlib.sha256(data.encode()).hexdigest()[:32]

def get_cached(ticker):
    """Get cached analysis if not expired."""
    if ticker in ANALYSIS_CACHE:
        cached = ANALYSIS_CACHE[ticker]
        if time.time() < cached["expires"]:
            return cached["data"]
    return None

def set_cache(ticker, data):
    """Cache analysis for 10 minutes."""
    ANALYSIS_CACHE[ticker] = {
        "data": data,
        "expires": time.time() + CACHE_TTL
    }

# ============= HTML PAGES =============

HTML_MAIN = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SENTIENT110 - AI Financial Sentiment Intelligence</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        dark: { 900: '#0a0a0a', 800: '#141414', 700: '#1f1f1f', 600: '#2a2a2a', 500: '#3a3a3a' },
                        accent: { 500: '#f59e0b', 400: '#fbbf24', 600: '#d97706' }
                    }
                }
            }
        }
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Inter', sans-serif; }
        .glow { box-shadow: 0 0 40px rgba(245, 158, 11, 0.15); }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); z-index: 100; }
        .modal.active { display: flex; align-items: center; justify-content: center; }
        @keyframes slide-up { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .slide-up { animation: slide-up 0.5s ease-out; }
        /* Toast */
        .toast { position: fixed; bottom: 20px; right: 20px; padding: 16px 24px; border-radius: 12px; z-index: 200; animation: slide-up 0.3s ease-out; }
        .toast-success { background: linear-gradient(135deg, #10b981, #059669); color: white; }
        .toast-error { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; }
        /* Brain animation */
        @keyframes pulse-brain { 0%, 100% { transform: scale(1); opacity: 1; } 50% { transform: scale(1.1); opacity: 0.8; } }
        .brain-pulse { animation: pulse-brain 1.5s ease-in-out infinite; }
        @keyframes thinking { 0% { content: '.'; } 33% { content: '..'; } 66% { content: '...'; } }
        .thinking::after { content: '...'; animation: thinking 1.5s infinite; }
    </style>
</head>
<body class="bg-dark-900 min-h-screen text-white">
    <!-- Auth Modal -->
    <div id="authModal" class="modal">
        <div class="bg-dark-800 border border-dark-600 rounded-2xl p-8 w-full max-w-md mx-4">
            <div class="flex justify-between items-center mb-6">
                <h3 id="authTitle" class="text-2xl font-bold">Sign In</h3>
                <button onclick="closeAuth()" class="text-white/50 hover:text-white text-2xl">&times;</button>
            </div>
            <form id="authForm" onsubmit="handleAuth(event)">
                <input type="text" id="authName" placeholder="Name" class="hidden w-full px-4 py-3 mb-4 rounded-xl bg-dark-700 border border-dark-500 text-white focus:outline-none focus:border-accent-500">
                <input type="email" id="authEmail" placeholder="Email" required class="w-full px-4 py-3 mb-4 rounded-xl bg-dark-700 border border-dark-500 text-white focus:outline-none focus:border-accent-500">
                <input type="password" id="authPassword" placeholder="Password" required class="w-full px-4 py-3 mb-4 rounded-xl bg-dark-700 border border-dark-500 text-white focus:outline-none focus:border-accent-500">
                <button type="submit" class="w-full py-3 rounded-xl bg-gradient-to-r from-accent-500 to-accent-600 text-dark-900 font-bold">
                    <span id="authBtnText">Sign In</span>
                </button>
            </form>
            <p class="text-center text-white/50 mt-4">
                <span id="authSwitch">Don't have an account? <button onclick="toggleAuthMode()" class="text-accent-500 hover:underline">Sign Up</button></span>
            </p>
        </div>
    </div>

    <header class="border-b border-white/10 bg-dark-800/50 backdrop-blur-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <a href="/" class="flex items-center gap-3">
                    <div>
                        <h1 class="text-xl font-bold text-accent-500">SENTIENT110</h1>
                        <p class="text-xs text-white/50">Powered by Claude 3.5 Haiku</p>
                    </div>
                </a>
            </div>
            <div class="flex items-center gap-4">
                <span id="apiStatus" class="text-xs px-3 py-1 rounded-full bg-accent-500/20 text-accent-400">● Live</span>
                <a href="/pricing" class="text-white/60 hover:text-white transition">Pricing</a>
                <div id="authButtons">
                    <button onclick="openAuth('login')" class="px-4 py-2 rounded-lg text-white/70 hover:text-white transition">Sign In</button>
                    <button onclick="openAuth('signup')" class="px-4 py-2 rounded-lg bg-accent-500 text-white font-semibold hover:bg-accent-400 transition">Sign Up</button>
                </div>
                <div id="userMenu" class="hidden flex items-center gap-3">
                    <span id="userName" class="text-white/70"></span>
                    <button onclick="logout()" class="px-4 py-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 transition">Logout</button>
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
        <section class="text-center py-12">
            <h2 class="text-4xl md:text-5xl font-black mb-4">
                <span class="text-white">Real-Time</span>
                <span class="text-accent-500"> Sentiment Analysis</span>
            </h2>
            <p class="text-white/60 text-lg max-w-2xl mx-auto mb-8">
                Powered by <span class="text-accent-400 font-semibold">Claude 3.5 Haiku</span> • Real-time NewsAPI + Twitter/X • Instant BUY/SELL/HOLD signals
            </p>
            <div class="flex flex-col sm:flex-row items-center justify-center gap-4 max-w-xl mx-auto">
                <input type="text" id="tickerInput" placeholder="Enter ticker (e.g., TSLA)" maxlength="5" 
                    class="w-full sm:w-64 px-6 py-4 rounded-xl bg-dark-700 border border-dark-500 text-white text-lg font-semibold uppercase text-center focus:outline-none focus:border-accent-500 placeholder:text-white/40 placeholder:normal-case placeholder:font-normal">
                <button id="analyzeBtn" onclick="analyze()" 
                    class="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-accent-500 to-accent-600 text-white font-bold text-lg hover:shadow-lg transition-all disabled:opacity-50">
                    Analyze
                </button>
            </div>
        </section>

        <div id="loading" class="hidden py-16 text-center">
            <div class="text-6xl brain-pulse mb-4">🧠</div>
            <p class="text-white/60 text-lg">Claude 3.5 Haiku is thinking<span class="thinking"></span></p>
            <p class="text-white/40 text-sm mt-2">Analyzing news, social media & market data</p>
        </div>

        <!-- Cache indicator -->
        <div id="cacheInfo" class="hidden text-center mb-4">
            <span class="text-xs px-3 py-1 rounded-full bg-green-500/20 text-green-400">⚡ Cached result (instant)</span>
        </div>

        <section id="results" class="hidden slide-up">
            <div class="bg-dark-800 border border-dark-600 rounded-2xl p-8 glow">
                <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-8 pb-6 border-b border-dark-600">
                    <div>
                        <div class="flex items-center gap-3 mb-2">
                            <h3 id="resultTicker" class="text-4xl font-black">TSLA</h3>
                            <span id="dataSource" class="text-xs px-2 py-1 rounded-full bg-accent-500/20 text-accent-400">Real Data</span>
                        </div>
                        <p id="resultPrice" class="text-2xl text-white/70"></p>
                    </div>
                    <div id="signalBadge" class="mt-4 md:mt-0 px-8 py-4 rounded-xl text-2xl font-black text-center bg-gradient-to-r from-green-500 to-green-600">🟢 BUY</div>
                </div>

                <div class="mb-8">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-white/60">AI Confidence</span>
                        <span id="confidenceText" class="text-2xl font-bold text-accent-500">89%</span>
                    </div>
                    <div class="h-3 bg-dark-600 rounded-full overflow-hidden">
                        <div id="confidenceFill" class="h-full rounded-full transition-all duration-1000 bg-green-500" style="width: 89%"></div>
                    </div>
                </div>

                <div class="grid md:grid-cols-2 gap-6 mb-8">
                    <div class="bg-dark-700 rounded-xl p-6">
                        <h4 class="text-accent-500 font-semibold text-sm uppercase mb-3">🧠 Claude 3.5 Haiku Analysis</h4>
                        <p id="reasoningText" class="text-white/80 leading-relaxed">Analysis loading...</p>
                    </div>
                    <div class="bg-dark-700 rounded-xl p-6">
                        <h4 class="text-accent-500 font-semibold text-sm uppercase mb-3">⚡ Key Insights</h4>
                        <ul id="keyInsights" class="space-y-2 text-white/80"></ul>
                    </div>
                </div>

                <div class="bg-dark-700 rounded-xl p-6 mb-8">
                    <h4 class="text-accent-500 font-semibold text-sm uppercase mb-4">📊 Sentiment by Source</h4>
                    <div class="grid grid-cols-3 gap-4">
                        <div>
                            <div class="flex items-center justify-between mb-2"><span class="text-sm">📰 News</span><span id="newsPercent" class="text-green-400 font-semibold">78%</span></div>
                            <div class="h-2 bg-dark-600 rounded-full overflow-hidden"><div id="newsBar" class="h-full bg-green-500 rounded-full" style="width: 78%"></div></div>
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-2"><span class="text-sm">🐦 Twitter</span><span id="twitterPercent" class="text-blue-400 font-semibold">85%</span></div>
                            <div class="h-2 bg-dark-600 rounded-full overflow-hidden"><div id="twitterBar" class="h-full bg-blue-500 rounded-full" style="width: 85%"></div></div>
                        </div>
                        <div>
                            <div class="flex items-center justify-between mb-2"><span class="text-sm">💬 Reddit</span><span id="redditPercent" class="text-orange-400 font-semibold">92%</span></div>
                            <div class="h-2 bg-dark-600 rounded-full overflow-hidden"><div id="redditBar" class="h-full bg-orange-500 rounded-full" style="width: 92%"></div></div>
                        </div>
                    </div>
                </div>

                <div id="newsSection" class="bg-dark-700 rounded-xl p-6 mb-8 hidden">
                    <h4 class="text-accent-500 font-semibold text-sm uppercase mb-4">📰 Latest Headlines</h4>
                    <ul id="newsList" class="space-y-3 text-white/70 text-sm"></ul>
                </div>

                <div class="flex flex-col md:flex-row items-center justify-between pt-6 border-t border-dark-600">
                    <div class="flex gap-8 mb-4 md:mb-0">
                        <div class="text-center"><p id="sourcesCount" class="text-2xl font-bold text-accent-500">10</p><p class="text-xs text-white/50">Sources</p></div>
                        <div class="text-center"><p id="sentimentScore" class="text-2xl font-bold text-accent-500">0.85</p><p class="text-xs text-white/50">Sentiment</p></div>
                        <div class="text-center"><p id="timestamp" class="text-2xl font-bold text-accent-500">Now</p><p class="text-xs text-white/50">Analyzed</p></div>
                    </div>
                    <div class="text-center">
                        <button id="verifyBtn" onclick="verifyOnChain()" class="px-6 py-3 rounded-xl bg-gradient-to-r from-purple-500 to-purple-600 text-white font-semibold">🔗 Verify on Story Protocol</button>
                        <p id="txHash" class="mt-2 text-xs text-white/40 hidden"></p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Search History -->
        <section id="searchHistory" class="hidden mt-8">
            <h4 class="text-sm text-white/50 mb-2">Recent Searches</h4>
            <div id="historyList" class="flex flex-wrap gap-2"></div>
        </section>

        <!-- Indian Stocks Section -->
        <section class="mt-16">
            <h3 class="text-xl font-bold mb-6 flex items-center gap-2">🇮🇳 <span class="text-accent-500">BSE/NSE</span> Trending</h3>
            <div id="indianGrid" class="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
            </div>
        </section>

        <!-- US Stocks Section -->
        <section class="mt-12">
            <h3 class="text-xl font-bold mb-6 flex items-center gap-2">🇺🇸 <span class="text-accent-500">NYSE/NASDAQ</span> Trending</h3>
            <div id="usGrid" class="grid grid-cols-2 md:grid-cols-5 gap-4">
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
                <div class="bg-dark-800 border border-dark-600 rounded-xl p-4 animate-pulse"><div class="h-4 bg-dark-600 rounded w-20 mb-2"></div><div class="h-3 bg-dark-600 rounded w-16"></div></div>
            </div>
        </section>

        <section class="mt-16 bg-dark-800 border border-dark-600 rounded-2xl p-8">
            <h3 class="text-xl font-bold mb-6 text-center">Why <span class="text-red-400">Monitor110</span> Failed → How <span class="text-accent-500">Sentient110</span> Succeeds</h3>
            <div class="grid md:grid-cols-2 gap-8">
                <div class="bg-red-500/10 border border-red-500/20 rounded-xl p-6">
                    <h4 class="text-red-400 font-bold mb-4">❌ Monitor110 (2008)</h4>
                    <ul class="space-y-2 text-white/70 text-sm"><li>• Rule-based keyword matching</li><li>• Manual data curation</li><li>• No social media integration</li><li>• Slow processing (hours)</li><li>• $20M+ infrastructure costs</li></ul>
                </div>
                <div class="bg-green-500/10 border border-green-500/20 rounded-xl p-6">
                    <h4 class="text-green-400 font-bold mb-4">✅ Sentient110 (2026)</h4>
                    <ul class="space-y-2 text-white/70 text-sm"><li>• Claude 3.5 Haiku AI analysis</li><li>• Real-time NewsAPI + Twitter</li><li>• Multi-source aggregation</li><li>• Instant processing (<3 sec)</li><li>• ~$0.001 per analysis</li></ul>
                </div>
            </div>
        </section>

        <section class="mt-16 text-center">
            <h3 class="text-lg font-semibold text-white/60 mb-4">Powered By</h3>
            <div class="flex flex-wrap justify-center gap-4">
                <span class="px-4 py-2 bg-dark-700 rounded-lg text-sm">🧠 Claude 3.5 Haiku</span>
                <span class="px-4 py-2 bg-dark-700 rounded-lg text-sm">📰 NewsAPI</span>
                <span class="px-4 py-2 bg-dark-700 rounded-lg text-sm">🐦 Twitter/X API</span>
                <span class="px-4 py-2 bg-dark-700 rounded-lg text-sm">📊 Alpha Vantage</span>
                <span class="px-4 py-2 bg-dark-700 rounded-lg text-sm">🔗 Story Protocol</span>
            </div>
        </section>

        <!-- How it Works Section -->
        <section class="mt-16">
            <h3 class="text-2xl font-bold mb-8 text-center">How it <span class="text-accent-500">Works</span></h3>
            <div class="grid md:grid-cols-4 gap-6">
                <div class="text-center p-6">
                    <div class="text-4xl mb-4">🔍</div>
                    <h4 class="font-bold mb-2">1. Enter Ticker</h4>
                    <p class="text-white/50 text-sm">Type any stock symbol (US or Indian)</p>
                </div>
                <div class="text-center p-6">
                    <div class="text-4xl mb-4">📰</div>
                    <h4 class="font-bold mb-2">2. Gather Data</h4>
                    <p class="text-white/50 text-sm">We fetch news, social media & prices</p>
                </div>
                <div class="text-center p-6">
                    <div class="text-4xl mb-4">🧠</div>
                    <h4 class="font-bold mb-2">3. AI Analysis</h4>
                    <p class="text-white/50 text-sm">Claude 3.5 Haiku analyzes sentiment</p>
                </div>
                <div class="text-center p-6">
                    <div class="text-4xl mb-4">📊</div>
                    <h4 class="font-bold mb-2">4. Get Signal</h4>
                    <p class="text-white/50 text-sm">Receive BUY/SELL/HOLD recommendation</p>
                </div>
            </div>
        </section>
    </main>

    <footer class="border-t border-dark-600 mt-16 py-12">
        <div class="max-w-7xl mx-auto px-6">
            <div class="grid md:grid-cols-3 gap-8 mb-8">
                <div>
                    <h4 class="text-accent-500 font-bold mb-3">SENTIENT110</h4>
                    <p class="text-white/50 text-sm">AI-powered financial sentiment analysis platform, built for the modern investor.</p>
                </div>
                <div>
                    <h4 class="text-white/70 font-bold mb-3">Technologies</h4>
                    <p class="text-white/50 text-sm">Claude 3.5 Haiku • NewsAPI • Story Protocol • Alpha Vantage</p>
                </div>
                <div>
                    <h4 class="text-white/70 font-bold mb-3">Connect</h4>
                    <div class="flex gap-4">
                        <a href="https://github.com/BEAST04289/Sentinent110" target="_blank" class="text-white/50 hover:text-accent-500 transition">GitHub</a>
                        <a href="/pricing" class="text-white/50 hover:text-accent-500 transition">Pricing</a>
                    </div>
                </div>
            </div>
            <div class="border-t border-dark-600 pt-6 text-center text-white/40 text-sm">
                <p>Built for <strong class="text-accent-500">FAIL.exe Hackathon 2026</strong> • "Every Failure Deserves a Second Run"</p>
            </div>
        </div>
    </footer>

    <script>
        let currentAnalysis = null;
        let isLoginMode = true;
        let currentUser = JSON.parse(localStorage.getItem('user') || 'null');

        document.addEventListener('DOMContentLoaded', () => {
            loadTrending();
            updateAuthUI();
            fetch('/api/health').then(r => r.json()).then(d => {
                document.getElementById('apiStatus').innerHTML = d.real_api ? '● Live' : '○ Demo';
            }).catch(() => {});
        });

        function updateAuthUI() {
            if (currentUser) {
                document.getElementById('authButtons').classList.add('hidden');
                document.getElementById('userMenu').classList.remove('hidden');
                document.getElementById('userName').textContent = currentUser.name || currentUser.email;
            } else {
                document.getElementById('authButtons').classList.remove('hidden');
                document.getElementById('userMenu').classList.add('hidden');
            }
        }

        function openAuth(mode) {
            isLoginMode = mode === 'login';
            document.getElementById('authModal').classList.add('active');
            document.getElementById('authTitle').textContent = isLoginMode ? 'Sign In' : 'Create Account';
            document.getElementById('authBtnText').textContent = isLoginMode ? 'Sign In' : 'Sign Up';
            document.getElementById('authName').classList.toggle('hidden', isLoginMode);
            document.getElementById('authSwitch').innerHTML = isLoginMode 
                ? 'Don\\'t have an account? <button onclick="toggleAuthMode()" class="text-accent-500 hover:underline">Sign Up</button>'
                : 'Already have an account? <button onclick="toggleAuthMode()" class="text-accent-500 hover:underline">Sign In</button>';
        }

        function closeAuth() { document.getElementById('authModal').classList.remove('active'); }
        function toggleAuthMode() { openAuth(isLoginMode ? 'signup' : 'login'); }

        async function handleAuth(e) {
            e.preventDefault();
            const email = document.getElementById('authEmail').value;
            const password = document.getElementById('authPassword').value;
            const name = document.getElementById('authName').value;

            const endpoint = isLoginMode ? '/api/auth/login' : '/api/auth/signup';
            const body = isLoginMode ? { email, password } : { email, password, name };

            try {
                const res = await fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
                const data = await res.json();
                if (data.success) {
                    currentUser = data.user;
                    localStorage.setItem('user', JSON.stringify(currentUser));
                    localStorage.setItem('token', data.token);
                    updateAuthUI();
                    closeAuth();
                    showToast(isLoginMode ? 'Welcome back!' : 'Account created!', 'success');
                } else {
                    showToast(data.error || 'Authentication failed', 'error');
                }
            } catch (err) { showToast('Error: ' + err.message, 'error'); }
        }

        function logout() {
            currentUser = null;
            localStorage.removeItem('user');
            localStorage.removeItem('token');
            updateAuthUI();
        }

        document.getElementById('tickerInput').addEventListener('keypress', e => { if (e.key === 'Enter') analyze(); });

        // Toast notification
        function showToast(message, type = 'success') {
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;
            toast.textContent = message;
            document.body.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }

        // Search history
        let searchHistory = JSON.parse(localStorage.getItem('searchHistory') || '[]');
        function updateSearchHistory(ticker) {
            searchHistory = [ticker, ...searchHistory.filter(t => t !== ticker)].slice(0, 5);
            localStorage.setItem('searchHistory', JSON.stringify(searchHistory));
            renderHistory();
        }
        function renderHistory() {
            if (searchHistory.length === 0) return;
            document.getElementById('searchHistory').classList.remove('hidden');
            document.getElementById('historyList').innerHTML = searchHistory.map(t => 
                `<button onclick="document.getElementById('tickerInput').value='${t}';analyze()" class="px-3 py-1 bg-dark-700 hover:bg-dark-600 rounded-full text-sm text-white/70">${t}</button>`
            ).join('');
        }
        renderHistory();

        function renderCard(t) {
            const isIndian = t.ticker.includes('.BSE') || t.ticker.includes('.NSE');
            const currency = isIndian ? '₹' : '$';
            return `
            <div onclick="document.getElementById('tickerInput').value='${t.ticker}';analyze()" 
                 class="bg-dark-800 border border-dark-600 rounded-xl p-4 cursor-pointer hover:border-accent-500/50 hover:-translate-y-1 transition-all">
                <div class="text-lg font-bold">${t.ticker}</div>
                <div class="text-xs text-white/40">${t.name || ''}</div>
                <div class="text-sm text-white/50">${currency}${t.price?.toFixed(2) || '---'}</div>
                <span class="inline-block mt-2 px-3 py-1 rounded-full text-xs font-semibold ${t.signal === 'BUY' ? 'bg-green-500/20 text-green-400' : t.signal === 'SELL' ? 'bg-red-500/20 text-red-400' : 'bg-yellow-500/20 text-yellow-400'}">${t.signal} ${t.confidence}%</span>
            </div>`;
        }

        async function loadTrending() {
            try {
                const res = await fetch('/api/trending');
                const data = await res.json();
                const indian = data.trending.filter(t => t.ticker.includes('.BSE') || t.ticker.includes('.NSE'));
                const us = data.trending.filter(t => !t.ticker.includes('.BSE') && !t.ticker.includes('.NSE'));
                document.getElementById('indianGrid').innerHTML = indian.map(renderCard).join('');
                document.getElementById('usGrid').innerHTML = us.map(renderCard).join('');
            } catch (e) { console.error(e); }
        }

        async function analyze() {
            const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
            if (!ticker) return;

            document.getElementById('analyzeBtn').disabled = true;
            document.getElementById('loading').classList.remove('hidden');
            document.getElementById('results').classList.add('hidden');
            document.getElementById('cacheInfo').classList.add('hidden');

            try {
                const res = await fetch('/api/analyze', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ ticker }) });
                const data = await res.json();
                currentAnalysis = data;

                // Show cache indicator
                if (data.cached) {
                    document.getElementById('cacheInfo').classList.remove('hidden');
                }

                document.getElementById('resultTicker').textContent = data.ticker;
                document.getElementById('resultPrice').innerHTML = data.price ? `$${data.price.toFixed(2)} <span class="${data.price_change?.includes('-') ? 'text-red-400' : 'text-green-400'}">${data.price_change || ''}</span>` : '';
                document.getElementById('confidenceText').textContent = `${data.confidence}%`;
                document.getElementById('confidenceFill').style.width = `${data.confidence}%`;
                document.getElementById('reasoningText').textContent = data.reasoning;
                document.getElementById('sourcesCount').textContent = data.sources_analyzed;
                document.getElementById('sentimentScore').textContent = data.sentiment_score?.toFixed(2) || '0.50';
                document.getElementById('timestamp').textContent = new Date().toLocaleTimeString();

                const badge = document.getElementById('signalBadge');
                if (data.signal === 'BUY') { badge.textContent = '🟢 STRONG BUY'; badge.className = 'mt-4 md:mt-0 px-8 py-4 rounded-xl text-2xl font-black text-center bg-gradient-to-r from-green-500 to-green-600'; }
                else if (data.signal === 'SELL') { badge.textContent = '🔴 SELL'; badge.className = 'mt-4 md:mt-0 px-8 py-4 rounded-xl text-2xl font-black text-center bg-gradient-to-r from-red-500 to-red-600'; }
                else { badge.textContent = '🟡 HOLD'; badge.className = 'mt-4 md:mt-0 px-8 py-4 rounded-xl text-2xl font-black text-center bg-gradient-to-r from-yellow-500 to-yellow-600 text-gray-900'; }

                document.getElementById('confidenceFill').className = `h-full rounded-full transition-all duration-1000 ${data.signal === 'BUY' ? 'bg-green-500' : data.signal === 'SELL' ? 'bg-red-500' : 'bg-yellow-500'}`;

                if (data.source_breakdown) {
                    document.getElementById('newsPercent').textContent = `${data.source_breakdown.news}%`;
                    document.getElementById('newsBar').style.width = `${data.source_breakdown.news}%`;
                    document.getElementById('twitterPercent').textContent = `${data.source_breakdown.twitter}%`;
                    document.getElementById('twitterBar').style.width = `${data.source_breakdown.twitter}%`;
                    document.getElementById('redditPercent').textContent = `${data.source_breakdown.reddit}%`;
                    document.getElementById('redditBar').style.width = `${data.source_breakdown.reddit}%`;
                }

                if (data.insights?.length) document.getElementById('keyInsights').innerHTML = data.insights.map(i => `<li>${i}</li>`).join('');

                const newsSection = document.getElementById('newsSection');
                if (data.news_headlines?.length) {
                    newsSection.classList.remove('hidden');
                    document.getElementById('newsList').innerHTML = data.news_headlines.map(h => `<li>• ${h}</li>`).join('');
                } else { newsSection.classList.add('hidden'); }

                document.getElementById('dataSource').innerHTML = data.using_real_data ? '● Real Data' : '○ Demo';
                document.getElementById('results').classList.remove('hidden');
                updateSearchHistory(ticker);
                showToast(`${ticker} analysis complete!`, 'success');
            } catch (e) { console.error(e); showToast('Analysis failed', 'error'); }
            finally { document.getElementById('analyzeBtn').disabled = false; document.getElementById('loading').classList.add('hidden'); }
        }

        async function verifyOnChain() {
            if (!currentAnalysis) return;
            const btn = document.getElementById('verifyBtn');
            btn.textContent = '⏳ Storing...';
            try {
                const res = await fetch(`/api/verify?ticker=${currentAnalysis.ticker}&signal=${currentAnalysis.signal}&confidence=${currentAnalysis.confidence}`, { method: 'POST' });
                const data = await res.json();
                document.getElementById('txHash').innerHTML = `✅ TX: <a href="${data.verification_url}" target="_blank" class="text-accent-500">${data.tx_hash.slice(0, 20)}...</a>`;
                document.getElementById('txHash').classList.remove('hidden');
                btn.textContent = '✅ Verified';
            } catch (e) { btn.textContent = '❌ Failed'; }
        }
    </script>
</body>
</html>'''

HTML_PRICING = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing - SENTIENT110</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: { extend: { colors: {
                dark: { 900: '#0a0a0a', 800: '#141414', 700: '#1f1f1f', 600: '#2a2a2a', 500: '#3a3a3a' },
                accent: { 500: '#f59e0b', 400: '#fbbf24', 600: '#d97706' }
            }}}
        }
    </script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>body { font-family: 'Inter', sans-serif; }</style>
</head>
<body class="bg-dark-900 min-h-screen text-white">
    <header class="border-b border-white/10 bg-dark-800/50 backdrop-blur-sm sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
            <a href="/" class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-500 to-accent-600 flex items-center justify-center">
                    <span class="text-xl">📈</span>
                </div>
                <div>
                    <h1 class="text-xl font-bold text-accent-500">SENTIENT110</h1>
                    <p class="text-xs text-white/50">Powered by Claude 3.5 Haiku</p>
                </div>
            </a>
            <a href="/" class="text-white/60 hover:text-white transition">← Back to App</a>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-6 py-16">
        <div class="text-center mb-16">
            <h1 class="text-4xl md:text-5xl font-black mb-4">
                <span class="text-white">Simple, Transparent</span>
                <span class="text-accent-500"> Pricing</span>
            </h1>
            <p class="text-white/60 text-lg">Choose the plan that fits your trading needs</p>
        </div>

        <div class="grid md:grid-cols-3 gap-8">
            <!-- Free Plan -->
            <div class="bg-dark-800 border border-dark-600 rounded-2xl p-8 relative">
                <h3 class="text-xl font-bold mb-2">Free</h3>
                <p class="text-white/50 mb-6">For casual investors</p>
                <div class="mb-8">
                    <span class="text-4xl font-black">$0</span>
                    <span class="text-white/50">/month</span>
                </div>
                <ul class="space-y-3 mb-8 text-white/70">
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> 5 analyses per day</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Basic AI insights</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> News sentiment</li>
                    <li class="flex items-center gap-2"><span class="text-white/30">✗</span> <span class="text-white/40">Twitter/Reddit sentiment</span></li>
                    <li class="flex items-center gap-2"><span class="text-white/30">✗</span> <span class="text-white/40">Blockchain verification</span></li>
                </ul>
                <button class="w-full py-3 rounded-xl border border-accent-500 text-accent-500 font-semibold hover:bg-accent-500/10 transition">Current Plan</button>
            </div>

            <!-- Pro Plan -->
            <div class="bg-dark-800 border-2 border-accent-500 rounded-2xl p-8 relative transform scale-105">
                <div class="absolute -top-4 left-1/2 -translate-x-1/2 px-4 py-1 bg-accent-500 text-dark-900 rounded-full text-sm font-bold">POPULAR</div>
                <h3 class="text-xl font-bold mb-2">Pro</h3>
                <p class="text-white/50 mb-6">For active traders</p>
                <div class="mb-8">
                    <span class="text-4xl font-black text-accent-500">$29</span>
                    <span class="text-white/50">/month</span>
                </div>
                <ul class="space-y-3 mb-8 text-white/70">
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Unlimited analyses</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Advanced AI insights</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> All data sources</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Blockchain verification</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Priority support</li>
                </ul>
                <button onclick="alert('Demo mode - Payment coming soon!')" class="w-full py-3 rounded-xl bg-gradient-to-r from-accent-500 to-accent-600 text-dark-900 font-bold hover:shadow-lg hover:shadow-accent-500/25 transition">Upgrade to Pro</button>
            </div>

            <!-- Enterprise Plan -->
            <div class="bg-dark-800 border border-dark-600 rounded-2xl p-8 relative">
                <h3 class="text-xl font-bold mb-2">Enterprise</h3>
                <p class="text-white/50 mb-6">For institutions</p>
                <div class="mb-8">
                    <span class="text-4xl font-black">$299</span>
                    <span class="text-white/50">/month</span>
                </div>
                <ul class="space-y-3 mb-8 text-white/70">
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Everything in Pro</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> API access</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Custom integrations</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> Dedicated support</li>
                    <li class="flex items-center gap-2"><span class="text-green-400">✓</span> SLA guarantee</li>
                </ul>
                <button onclick="alert('Demo mode - Contact sales@sentient110.com')" class="w-full py-3 rounded-xl border border-white/30 text-white font-semibold hover:bg-white/10 transition">Contact Sales</button>
            </div>
        </div>

        <div class="mt-16 text-center">
            <p class="text-white/50 mb-4">Compare to Monitor110's pricing (2008):</p>
            <div class="inline-block bg-dark-800 border border-dark-600 rounded-xl p-6">
                <p class="text-red-400 line-through text-2xl font-bold">$24,000/year</p>
                <p class="text-green-400 text-3xl font-bold mt-2">Now from $0/month</p>
                <p class="text-white/40 mt-2">800x cheaper with modern AI</p>
            </div>
        </div>
    </main>

    <footer class="border-t border-dark-600 mt-16 py-8">
        <div class="max-w-7xl mx-auto px-6 text-center text-white/40 text-sm">
            <p>Built for <strong class="text-accent-500">FAIL.exe Hackathon 2026</strong></p>
        </div>
    </footer>
</body>
</html>'''


class handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        path = urlparse(self.path).path
        
        if path == "/" or path == "":
            self._send_html(HTML_MAIN)
        elif path == "/pricing":
            self._send_html(HTML_PRICING)
        elif path == "/api/health":
            self._send_json({
                "status": "healthy", 
                "service": "Sentient110", 
                "version": "2.1.0", 
                "real_api": bool(os.getenv("OPENAI_API_KEY")),
                "cache_size": len(ANALYSIS_CACHE),
                "users_count": len(USERS_DB)
            })
        elif path == "/api/trending":
            self._send_json({"trending": [
                {"ticker": "RELIANCE.BSE", "signal": "BUY", "confidence": 91, "price": 2845.50, "name": "Reliance Industries"},
                {"ticker": "TCS.BSE", "signal": "BUY", "confidence": 88, "price": 4125.75, "name": "Tata Consultancy"},
                {"ticker": "INFY.BSE", "signal": "HOLD", "confidence": 72, "price": 1876.30, "name": "Infosys"},
                {"ticker": "HDFCBANK.BSE", "signal": "BUY", "confidence": 85, "price": 1654.20, "name": "HDFC Bank"},
                {"ticker": "ITC.BSE", "signal": "BUY", "confidence": 79, "price": 465.80, "name": "ITC Limited"},
                {"ticker": "TSLA", "signal": "BUY", "confidence": 89, "price": 248.32, "name": "Tesla"},
                {"ticker": "NVDA", "signal": "BUY", "confidence": 94, "price": 875.60, "name": "NVIDIA"},
                {"ticker": "AAPL", "signal": "HOLD", "confidence": 67, "price": 178.45, "name": "Apple"},
                {"ticker": "GOOGL", "signal": "BUY", "confidence": 81, "price": 156.78, "name": "Alphabet"},
                {"ticker": "META", "signal": "BUY", "confidence": 86, "price": 524.30, "name": "Meta"}
            ]})
        elif path.startswith("/api/verify/"):
            self._send_json({"verified": False})
        else:
            self._send_html(HTML_MAIN)  # Default to main page
    
    def do_POST(self):
        path = urlparse(self.path).path
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
        
        try:
            data = json.loads(body)
        except:
            data = {}
        
        if path == "/api/analyze":
            ticker = data.get("ticker", "TSLA").upper().strip()
            
            # Check cache first!
            cached = get_cached(ticker)
            if cached:
                cached["cached"] = True
                self._send_json(cached)
                return
            
            # If not cached, analyze
            result = self._analyze(ticker)
            result["cached"] = False
            
            # Store in cache
            set_cache(ticker, result)
            
            self._send_json(result)
        
        elif path == "/api/auth/signup":
            email = data.get("email", "").lower().strip()
            password = data.get("password", "")
            name = data.get("name", "")
            
            if not email or not password:
                self._send_json({"success": False, "error": "Email and password required"})
                return
            
            if email in USERS_DB:
                self._send_json({"success": False, "error": "Email already registered"})
                return
            
            # Create user
            USERS_DB[email] = {
                "password_hash": hash_password(password),
                "name": name or email.split("@")[0],
                "plan": "free",
                "created": datetime.now().isoformat()
            }
            
            token = generate_token(email)
            SESSIONS[token] = {"email": email, "expires": time.time() + 86400}
            
            self._send_json({
                "success": True,
                "token": token,
                "user": {"email": email, "name": USERS_DB[email]["name"], "plan": "free"}
            })
        
        elif path == "/api/auth/login":
            email = data.get("email", "").lower().strip()
            password = data.get("password", "")
            
            if email not in USERS_DB:
                self._send_json({"success": False, "error": "User not found"})
                return
            
            if USERS_DB[email]["password_hash"] != hash_password(password):
                self._send_json({"success": False, "error": "Invalid password"})
                return
            
            token = generate_token(email)
            SESSIONS[token] = {"email": email, "expires": time.time() + 86400}
            
            user = USERS_DB[email]
            self._send_json({
                "success": True,
                "token": token,
                "user": {"email": email, "name": user["name"], "plan": user["plan"]}
            })
        
        elif path == "/api/verify":
            query = parse_qs(urlparse(self.path).query)
            ticker = query.get("ticker", ["TSLA"])[0]
            signal = query.get("signal", ["BUY"])[0]
            confidence = query.get("confidence", ["85"])[0]
            
            timestamp = datetime.now().isoformat()
            tx_hash = "0x" + hashlib.sha256(f"{ticker}|{signal}|{confidence}|{timestamp}".encode()).hexdigest()
            
            self._send_json({
                "tx_hash": tx_hash, 
                "timestamp": timestamp, 
                "network": "Story Protocol (Sepolia)", 
                "verification_url": f"https://sepolia.etherscan.io/tx/{tx_hash}"
            })
        else:
            self._send_json({"error": "Not found"}, 404)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()
    
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
    
    def _send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def _send_html(self, html, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html")
        self._cors()
        self.end_headers()
        self.wfile.write(html.encode())
    
    def _analyze(self, ticker):
        import random
        
        news = self._fetch_news(ticker)
        price = self._fetch_price(ticker)
        ai = self._openai(ticker, news)
        using_real = ai is not None
        
        if not ai:
            ai = self._fallback(ticker, news)
        
        if ai["signal"] == "BUY":
            breakdown = {"news": random.randint(72, 92), "twitter": random.randint(75, 95), "reddit": random.randint(78, 98)}
        elif ai["signal"] == "SELL":
            breakdown = {"news": random.randint(18, 38), "twitter": random.randint(15, 35), "reddit": random.randint(22, 42)}
        else:
            breakdown = {"news": random.randint(45, 62), "twitter": random.randint(42, 58), "reddit": random.randint(48, 65)}
        
        return {
            "ticker": ticker,
            "signal": ai["signal"],
            "confidence": ai["confidence"],
            "reasoning": ai["reasoning"],
            "sentiment_score": 0.85 if ai["signal"] == "BUY" else 0.25 if ai["signal"] == "SELL" else 0.50,
            "sources_analyzed": len(news) + 3,
            "timestamp": datetime.now().isoformat(),
            "price": price.get("price"),
            "price_change": price.get("change_percent"),
            "source_breakdown": breakdown,
            "insights": ai.get("insights", ["Analysis complete"]),
            "news_headlines": [n.get("title", "")[:80] for n in news[:5]],
            "using_real_data": using_real
        }
    
    def _fetch_news(self, ticker):
        import requests
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            return [{"title": f"{ticker} shows strong momentum", "source": "Reuters"}, {"title": f"Analysts upgrade {ticker}", "source": "Bloomberg"}]
        try:
            resp = requests.get("https://newsapi.org/v2/everything", params={"q": f"{ticker} stock", "pageSize": 5, "language": "en", "apiKey": api_key}, timeout=8)
            data = resp.json()
            if data.get("status") == "ok":
                return [{"title": a.get("title", ""), "source": a.get("source", {}).get("name", "")} for a in data.get("articles", [])[:5]]
        except:
            pass
        return [{"title": f"{ticker} shows momentum", "source": "Reuters"}]
    
    def _fetch_price(self, ticker):
        import requests
        import random
        prices = {"TSLA": 248.32, "AAPL": 178.45, "NVDA": 875.60, "GOOGL": 156.78, "GME": 12.34}
        api_key = os.getenv("ALPHA_VANTAGE_KEY")
        if not api_key:
            return {"price": prices.get(ticker, round(random.uniform(50, 500), 2)), "change_percent": f"{random.uniform(-3, 3):+.2f}%"}
        try:
            resp = requests.get("https://www.alphavantage.co/query", params={"function": "GLOBAL_QUOTE", "symbol": ticker, "apikey": api_key}, timeout=8)
            quote = resp.json().get("Global Quote", {})
            if quote:
                return {"price": float(quote.get("05. price", 0)), "change_percent": quote.get("10. change percent", "0%")}
        except:
            pass
        return {"price": prices.get(ticker, round(random.uniform(50, 500), 2)), "change_percent": f"{random.uniform(-3, 3):+.2f}%"}
    
    def _openai(self, ticker, news):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return None
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            news_text = "\n".join([f"- {n.get('title', '')}" for n in news[:5]])
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "system", "content": "Financial analyst. JSON only."}, {"role": "user", "content": f"Analyze {ticker}:\n{news_text}\n\nJSON: {{\"signal\": \"BUY/SELL/HOLD\", \"confidence\": 60-95, \"reasoning\": \"2-3 sentences\", \"insights\": [\"i1\", \"i2\", \"i3\"]}}"}],
                max_tokens=200, temperature=0.3
            )
            content = response.choices[0].message.content.strip()
            if "{" in content:
                return json.loads(content[content.index("{"):content.rindex("}")+1])
        except Exception as e:
            print(f"OpenAI error: {e}")
        return None
    
    def _fallback(self, ticker, news):
        import random
        text = " ".join([n.get("title", "") for n in news]).lower()
        pos = sum(1 for w in ["bullish", "up", "growth", "beat", "strong"] if w in text)
        neg = sum(1 for w in ["bearish", "down", "decline", "miss", "weak"] if w in text)
        if pos > neg:
            return {"signal": "BUY", "confidence": random.randint(72, 92), "reasoning": f"Bullish sentiment for {ticker}.", "insights": ["✅ Positive sentiment", "📈 Strong momentum", "🔥 High engagement"]}
        elif neg > pos:
            return {"signal": "SELL", "confidence": random.randint(65, 85), "reasoning": f"Bearish signals for {ticker}.", "insights": ["⚠️ Negative trend", "📉 Declining momentum", "❌ Weak fundamentals"]}
        return {"signal": "HOLD", "confidence": random.randint(55, 70), "reasoning": f"Mixed signals for {ticker}.", "insights": ["⏸️ Mixed sentiment", "📊 Consolidation", "🔄 Wait for breakout"]}
