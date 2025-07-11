start:
	@echo "Starting..."
	@mkdir -p logs
	@nohup python3 src/translation.py > logs/translation.log 2>&1 &
	@echo "Started."


stop:
	@echo "Stopping..."
	-pkill -f "src/record_and_stream.py" || true
	-pkill -f "ffmpeg" || true
	@echo "Stopped."

clean:
	@echo "Cleaning logs and live..."
	-rm -f logs/*
	-rm -rf src/__pycache__
	-rm -f live/*
	@echo "Logs and live claened."

clean_hard:
	@echo "Cleaning data..."
	-rm -f archive/*
	-rm -f live/*
	-rm -f logs/*
	-rm -rf src/__pycache__
	@echo "Data claened."

status_8080_check:
	@sudo lsof -i :8080 || true

git:
	@git status
	@git add .
	@git commit -m "default commit"
	@git push 

