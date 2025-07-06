start:
	@echo "Starting..."
	@mkdir -p logs
	@nohup python3 src/record_and_stream.py > logs/record_and_stream.log 2>&1 &
	@nohup python3 src/translation.py > logs/translation.log 2>&1 &
	@echo "Started."


stop:
	@echo "Stopping..."
	-pkill -f "src/record_and_stream.py" || true
	-pkill -f "src/translation.py" || true
	-pkill -f "ffmpeg" || true
	@echo "Stopped."

clean:
	@echo "Cleaning..."
	rm -rf archive
	rm -rf live
	rm -rf logs
	@echo "Claened."

status_8080_check:
	@sudo lsof -i :8080 || true

