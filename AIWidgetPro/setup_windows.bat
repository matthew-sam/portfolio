@echo off
echo AI Widget Setup for Windows
echo ========================

echo Installing Python packages...
pip install Flask Flask-CORS openai

echo.
echo Setup complete!
echo.
echo To set your OpenAI API key:
echo set OPENAI_API_KEY=your-api-key-here
echo.
echo Then run:
echo python run_windows.py
echo.
pause