# Justfile for the Q&A Chat App

# Generate HTML from YAML and start server
serve:
    pkill -f "python -m http.server 8000" || true
    source venv-hackathon-25-11/bin/activate && python summarize.py
    python -m http.server 8000

# Restart the server (kill existing and start new)
restart:
    pkill -f "python -m http.server 8000" || true
    source venv-hackathon-25-11/bin/activate && python summarize.py
    python -m http.server 8000 &

# Open the app in browser
open:
    open http://localhost:8000

# Kill the development server
stop:
    pkill -f "python -m http.server 8000" || true

# Rebuild HTML and refresh server
rebuild:
    pkill -f "python -m http.server 8000" || true
    source venv-hackathon-25-11/bin/activate && python summarize.py
    sleep 1
    python -m http.server 8000 &
    sleep 2
    open http://localhost:8000

# Force refresh - kill server, wait, then restart (useful when files are cached)
refresh: rebuild

# Update logo and refresh (for when logo.png is updated)
update-logo: rebuild

# Just rebuild HTML without starting server
build:
    source venv-hackathon-25-11/bin/activate && python summarize.py

# Default recipe
default: serve