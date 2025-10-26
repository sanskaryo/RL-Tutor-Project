# Navigation Structure - RL Tutor Platform

```
┌─────────────────────────────────────────────────────────────────────┐
│  🧠 RL Tutor    [Dashboard] [Learn] [Learning Style] [Analytics]   │
│                 [Skill Gaps]                    [@user] [Logout]    │
└─────────────────────────────────────────────────────────────────────┘
```

## Public Routes (Non-authenticated)

```
Home (/)
│
├─ Login (/login)
│  ├─ Form: Username, Password
│  └─ Link to Register
│
└─ Register (/register)
   ├─ Form: Email, Username, Password, Full Name
   └─ Link to Login
```

## Protected Routes (Authenticated)

```
Dashboard (/dashboard)
│
├─ Welcome Header
├─ Stats Grid (4 cards)
│  ├─ Total Attempts
│  ├─ Accuracy Rate
│  ├─ Current Streak
│  └─ Time Spent
│
├─ Learning Style Section 🆕
│  ├─ VARK Scores (Visual, Auditory, Reading, Kinesthetic)
│  └─ Dominant Style Badge
│
├─ Study Tips Section 🆕
│  └─ 3 personalized tips based on learning style
│
├─ Knowledge Gaps Section 🆕
│  └─ Topics needing improvement with scores
│
├─ Recommended Content Section 🆕
│  └─ RL-powered content suggestions with confidence
│
└─ Knowledge State Grid
   ├─ Algebra Score
   ├─ Calculus Score
   ├─ Geometry Score
   └─ Statistics Score

─────────────────────────────────────────────────

Learn (/learn)
│
├─ Header: "Interactive Learning"
├─ Session Stats Bar (questions, accuracy, reward)
├─ Topic Selector
│  ├─ Algebra
│  ├─ Calculus
│  ├─ Geometry
│  └─ Statistics
│
├─ Question Card
│  ├─ Question Text
│  ├─ Multiple Choice Options
│  └─ Submit Button
│
└─ Feedback Panel
   ├─ Correct/Incorrect Badge
   ├─ Explanation
   ├─ Reward Points
   └─ Next Question Button

─────────────────────────────────────────────────

Learning Style (/learning-style-quiz)
│
├─ Header with Progress Bar
├─ Quiz Instructions
├─ Question Card
│  ├─ Question Text
│  ├─ Radio Button Options (4 choices per question)
│  └─ Navigation (Previous / Next / Submit)
│
└─ Results Page (/learning-style-results)
   ├─ VARK Scores
   ├─ Radar Chart
   ├─ Pie Chart
   ├─ Dominant Style Description
   ├─ Study Tips List
   └─ Back to Dashboard Button

─────────────────────────────────────────────────

Skill Gaps (/skill-gaps) 🆕
│
├─ Header with "Analyze Gaps" Button
├─ Summary Stats (4 cards)
│  ├─ Total Gaps
│  ├─ Critical Count
│  ├─ Estimated Time
│  └─ Average Progress
│
└─ Gap List (sorted by priority)
   └─ Each Gap Card:
      ├─ Skill Name
      ├─ Severity Badge (Critical/High/Medium/Low)
      ├─ Priority Score (1-10)
      ├─ Estimated Time
      ├─ Progress Bar (Current → Target)
      └─ Recommendations List

─────────────────────────────────────────────────

Analytics (/analytics)
│
├─ Header: "Learning Analytics"
├─ Time Range Selector (7/14/30 days)
├─ Summary Stats (4 cards)
│  ├─ Overall Accuracy
│  ├─ Preferred Difficulty
│  ├─ Learning Style
│  └─ Total Sessions
│
├─ Charts Grid
│  ├─ Performance Trend (Line Chart)
│  │  └─ Accuracy over time
│  │
│  ├─ Activity Level (Bar Chart)
│  │  └─ Questions attempted per day
│  │
│  └─ Knowledge Distribution (Radar Chart)
│     └─ Scores across 4 topics
│
└─ Key Insights Section
   ├─ Consistency Streak
   └─ Improvement Rate
```

## Navigation Icons Legend

```
🏠 Home           - Home page
📊 LayoutDashboard - Dashboard overview
📚 BookOpen       - Interactive learning
💡 Lightbulb      - Learning style assessment
📈 BarChart3      - Analytics & progress
🎯 Target         - Skill gap analysis
👤 User           - Profile badge
🚪 LogOut         - Sign out
```

## Color Coding System

```
🟣 Purple (#a855f7)  - Primary actions, active states
🔵 Blue (#3b82f6)    - Secondary actions, info
🟢 Green (#4ade80)   - Success, positive metrics
🟡 Yellow (#facc15)  - Warnings, medium priority
🟠 Orange (#fb923c)  - High priority alerts
🔴 Red (#f87171)     - Critical issues, errors
⚪ Gray (#a1a1aa)    - Secondary text, disabled states
```

## Responsive Breakpoints

```
📱 Mobile    : < 768px   - Single column, hamburger menu
💻 Tablet    : 768-1024px - 2 columns, compact nav
🖥️  Desktop   : > 1024px  - 4 columns, full nav bar
```

## User Flow - First Time User

```
1. Landing Page (/)
   ↓
2. Click "Get Started"
   ↓
3. Register (/register)
   ↓
4. Dashboard (/dashboard)
   ↓
5. Take Learning Style Quiz (/learning-style-quiz)
   ↓
6. View Results (/learning-style-results)
   ↓
7. Start Learning (/learn)
   ↓
8. Check Skill Gaps (/skill-gaps)
   ↓
9. View Analytics (/analytics)
```

## User Flow - Returning User

```
1. Login (/login)
   ↓
2. Dashboard (/dashboard)
   ├─ View personalized recommendations
   ├─ Check knowledge gaps
   └─ See updated stats
   ↓
3. Continue Learning (/learn)
   └─ AI adapts based on history + learning style
```

## Feature Availability Matrix

| Feature                    | Public | Authenticated | Phase |
|----------------------------|--------|---------------|-------|
| Landing Page               | ✅     | ✅            | Base  |
| Login/Register             | ✅     | ✅            | Base  |
| Dashboard                  | ❌     | ✅            | Base  |
| Interactive Learning       | ❌     | ✅            | Base  |
| Learning Style Quiz        | ❌     | ✅            | 11.1  |
| Study Tips (personalized)  | ❌     | ✅            | 11.1  |
| Skill Gap Analysis         | ❌     | ✅            | 11.2  |
| RL Recommendations         | ❌     | ✅            | 11.1  |
| Analytics Dashboard        | ❌     | ✅            | Base  |
| Knowledge Graph            | ❌     | ✅            | 11.2* |
| Learning Pace Tracking     | ❌     | ✅            | 11.3* |

*Backend complete, frontend pending

## API Endpoints Referenced by UI

### Authentication
- POST `/auth/register` - Create account
- POST `/auth/login` - Sign in
- GET `/auth/me` - Get profile

### Learning Sessions
- POST `/session/start` - Start learning session
- POST `/session/answer` - Submit answer
- GET `/session/progress` - Get progress

### Analytics
- GET `/analytics/dashboard` - Dashboard data
- GET `/analytics/performance-chart` - Performance over time
- GET `/analytics/rl-stats` - RL agent statistics

### Learning Style
- GET `/quiz` - Get VARK assessment
- POST `/students/{id}/learning-style` - Submit assessment
- GET `/students/{id}/learning-style` - Get results

### Recommendations
- GET `/recommendations/dashboard` - Personalized recommendations

### Skill Gaps
- GET `/skill-gaps/analyze` - Analyze gaps from history
- GET `/skill-gaps/students/{id}` - List all gaps
- POST `/skill-gaps/students/{id}/gaps/{gap_id}/update-progress` - Track progress
- GET `/skill-gaps/knowledge-graph` - Graph data

## Tech Stack Visible to Users

**Frontend Performance:**
- Page Load: < 3 seconds
- API Response: < 500ms
- Chart Rendering: < 1 second
- Smooth 60fps animations

**Data Freshness:**
- Dashboard: Real-time on load
- Analytics: Configurable (7/14/30 days)
- Skill Gaps: On-demand analysis
- Recommendations: Updated per session

**Browser Support:**
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
```
