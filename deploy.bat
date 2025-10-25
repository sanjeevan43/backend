@echo off
echo Deploying LeetCode Solver API to Vercel...
echo.

cd /d "d:\profile\backend"

echo Installing Vercel CLI (if not installed)...
npm install -g vercel

echo.
echo Setting environment variables...
vercel env add GEMINI_API_KEY production
vercel env add API_TIMEOUT production
vercel env add MAX_OUTPUT_TOKENS production
vercel env add TEMPERATURE production
vercel env add TOP_P production

echo.
echo Deploying to Vercel...
vercel --prod

echo.
echo Deployment complete!
echo Check your deployment at: https://vercel.com/dashboard