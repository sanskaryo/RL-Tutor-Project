# Frontend-Backend Integration Guide
# RL Educational Tutor

## 🎯 Overview
This guide explains how to integrate the FastAPI backend with the Next.js frontend.

## 📡 Backend API Base URL
- **Development**: `http://localhost:8000`
- **API Version**: `/api/v1`
- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)

## 🔐 Authentication Flow

### 1. Register New User
```typescript
const register = async (userData: {
  email: string;
  username: string;
  password: string;
  full_name?: string;
}) => {
  const response = await fetch('http://localhost:8000/api/v1/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(userData)
  });
  const data = await response.json();
  // data = { access_token: "...", token_type: "bearer" }
  return data;
};
```

### 2. Login User
```typescript
const login = async (username: string, password: string) => {
  const response = await fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password })
  });
  const data = await response.json();
  return data.access_token;
};
```

### 3. Store Token
```typescript
// Store in localStorage
localStorage.setItem('token', data.access_token);
localStorage.setItem('username', username);

// Or use a state management solution (Zustand, Context API)
```

## 📚 Learning Session Flow

### 1. Start Learning Session
```typescript
const startSession = async (username: string, topic?: string) => {
  const params = new URLSearchParams({ username });
  const body = topic ? { topic } : {};
  
  const response = await fetch(
    `http://localhost:8000/api/v1/session/start?${params}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    }
  );
  
  const content = await response.json();
  // content = { id, title, question_text, options, difficulty, topic }
  return content;
};
```

### 2. Submit Answer
```typescript
const submitAnswer = async (
  username: string,
  sessionId: number,
  answer: string,
  timeSpent: number
) => {
  const params = new URLSearchParams({ username });
  
  const response = await fetch(
    `http://localhost:8000/api/v1/session/answer?${params}`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: sessionId,
        student_answer: answer,
        time_spent: timeSpent
      })
    }
  );
  
  const result = await response.json();
  // result = { id, content_id, is_correct, reward, explanation, next_content }
  return result;
};
```

### 3. Get Progress
```typescript
const getProgress = async (username: string) => {
  const params = new URLSearchParams({ username });
  
  const response = await fetch(
    `http://localhost:8000/api/v1/session/progress?${params}`
  );
  
  const progress = await response.json();
  // progress = { progress: {...}, recent_sessions: [...] }
  return progress;
};
```

## 📊 Analytics & Dashboard

### Get Dashboard Data
```typescript
const getDashboard = async (username: string) => {
  const params = new URLSearchParams({ username });
  
  const response = await fetch(
    `http://localhost:8000/api/v1/analytics/dashboard?${params}`
  );
  
  const dashboard = await response.json();
  /*
  dashboard = {
    student: { id, email, username, full_name, created_at },
    knowledge: {
      algebra_score, calculus_score, geometry_score, statistics_score,
      accuracy_rate, preferred_difficulty, learning_style
    },
    progress: {
      total_attempts, correct_answers, accuracy_rate,
      topics_mastered, current_streak, time_spent_today,
      skill_improvements
    },
    recent_sessions: [...]
  }
  */
  return dashboard;
};
```

### Get Performance Chart Data
```typescript
const getPerformanceChart = async (username: string, days: number = 7) => {
  const params = new URLSearchParams({ username, days: days.toString() });
  
  const response = await fetch(
    `http://localhost:8000/api/v1/analytics/performance-chart?${params}`
  );
  
  const chartData = await response.json();
  // chartData = [{ date, attempts, correct, accuracy, avg_time, total_time }]
  return chartData;
};
```

## 🧠 RL Agent Statistics

### Get RL Agent Stats
```typescript
const getRLStats = async () => {
  const response = await fetch(
    'http://localhost:8000/api/v1/analytics/rl-stats'
  );
  
  const stats = await response.json();
  /*
  stats = {
    total_updates, q_table_shape, mean_q_value, max_q_value,
    learning_rate, epsilon
  }
  */
  return stats;
};
```

## 🏗️ Recommended File Structure

```
app/
├── api/
│   └── client.ts          # API client functions
├── contexts/
│   └── AuthContext.tsx    # Authentication context
├── hooks/
│   ├── useAuth.ts         # Authentication hook
│   ├── useSession.ts      # Learning session hook
│   └── useDashboard.ts    # Dashboard data hook
├── types/
│   └── api.ts             # TypeScript types for API responses
├── (auth)/
│   ├── login/
│   │   └── page.tsx
│   └── register/
│       └── page.tsx
├── dashboard/
│   └── page.tsx           # Student dashboard
├── learn/
│   └── page.tsx           # Learning session page
└── page.tsx               # Landing page (existing)
```

## 📝 Example Implementation

### Create API Client (`app/api/client.ts`)
```typescript
const API_BASE = 'http://localhost:8000/api/v1';

export const api = {
  // Auth
  register: async (userData: RegisterData) => {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    return res.json();
  },
  
  login: async (credentials: LoginData) => {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    return res.json();
  },
  
  // Session
  startSession: async (username: string, topic?: string) => {
    const params = new URLSearchParams({ username });
    const res = await fetch(`${API_BASE}/session/start?${params}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(topic ? { topic } : {})
    });
    return res.json();
  },
  
  submitAnswer: async (username: string, data: AnswerData) => {
    const params = new URLSearchParams({ username });
    const res = await fetch(`${API_BASE}/session/answer?${params}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });
    return res.json();
  },
  
  // Analytics
  getDashboard: async (username: string) => {
    const params = new URLSearchParams({ username });
    const res = await fetch(`${API_BASE}/analytics/dashboard?${params}`);
    return res.json();
  }
};
```

### Create Auth Hook (`app/hooks/useAuth.ts`)
```typescript
'use client';
import { useState, useEffect } from 'react';
import { api } from '@/app/api/client';

export function useAuth() {
  const [user, setUser] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);
  
  useEffect(() => {
    const storedUser = localStorage.getItem('username');
    const storedToken = localStorage.getItem('token');
    if (storedUser && storedToken) {
      setUser(storedUser);
      setToken(storedToken);
    }
  }, []);
  
  const login = async (username: string, password: string) => {
    const data = await api.login({ username, password });
    localStorage.setItem('username', username);
    localStorage.setItem('token', data.access_token);
    setUser(username);
    setToken(data.access_token);
    return data;
  };
  
  const register = async (userData: RegisterData) => {
    const data = await api.register(userData);
    localStorage.setItem('username', userData.username);
    localStorage.setItem('token', data.access_token);
    setUser(userData.username);
    setToken(data.access_token);
    return data;
  };
  
  const logout = () => {
    localStorage.removeItem('username');
    localStorage.removeItem('token');
    setUser(null);
    setToken(null);
  };
  
  return { user, token, login, register, logout, isAuthenticated: !!user };
}
```

## 🎨 UI Integration Tips

### Add Login/Register Buttons to Landing Page
Update the Hero section CTAs:
```tsx
<Link href="/register">
  <button className="px-8 py-3 bg-white text-black rounded-lg...">
    Get Started
  </button>
</Link>

<Link href="/login">
  <button className="px-8 py-3 border border-gray-700...">
    Sign In
  </button>
</Link>
```

### Show Dashboard Link After Login
```tsx
{isAuthenticated && (
  <Link href="/dashboard">
    <button>Go to Dashboard</button>
  </Link>
)}
```

## 🔄 Real-time Updates (Optional)

For real-time RL agent updates, consider:
1. **Polling**: Fetch dashboard data every 30 seconds
2. **WebSockets**: Implement WebSocket connection for live updates
3. **Server-Sent Events**: Use SSE for one-way updates

## 🧪 Testing Integration

### Test User Credentials
- Username: `testuser`
- Password: `test123`
- Email: `test@example.com`

### Quick Test Commands
```bash
# In backend directory
python test_api.py
```

## 🚀 Next Steps

1. ✅ Backend is running on port 8000
2. ⏭️ Create API client in Next.js
3. ⏭️ Build login/register pages
4. ⏭️ Create dashboard page
5. ⏭️ Build learning session interface
6. ⏭️ Add progress visualization
7. ⏭️ Implement RL visualization

## 📚 Resources

- **API Docs**: http://localhost:8000/docs
- **Backend README**: backend/README.md
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Data Fetching**: https://nextjs.org/docs/app/building-your-application/data-fetching
