# SuperQuantLab 2.0 Frontend

## Setup

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Visit http://localhost:3000

## Build

```bash
npm run build
npm start
```

## Environment Variables

Create `.env.local`:

```
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Project Structure

- `app/` - Next.js app router pages
- `components/` - React components
- `lib/` - Utilities (API client, i18n)

## Features

- Dark theme UI
- Bilingual support (Chinese/English)
- Real-time charts (Recharts)
- Strategy management
- Behavior analysis
- Market regime visualization

