# log/logger.py
import logging, os, json
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def safe_json_serializer(obj):
    """JSON 직렬화할 수 없는 객체들을 안전하게 변환"""
    try:
        # LangChain 메시지 객체 처리
        if hasattr(obj, 'content') and hasattr(obj, 'type'):
            return {
                "type": obj.type if hasattr(obj, 'type') else obj.__class__.__name__,
                "content": str(obj.content),
                "id": getattr(obj, 'id', None)
            }
        # 기타 객체들
        elif hasattr(obj, '__dict__'):
            return f"<{obj.__class__.__name__} object>"
        else:
            return str(obj)
    except:
        return f"<unserializable {type(obj).__name__}>"

class JsonLineFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "time": self.formatTime(record, "%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "_extra"):
            base.update(record._extra)
        return json.dumps(base, ensure_ascii=False, default=safe_json_serializer)

def get_logger(name="app"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        # 날짜별 로그 파일: app-2025-08-27.jsonl 형식
        today = datetime.now().strftime("%Y-%m-%d")
        log_filename = f"{name}-{today}.jsonl"
        LOG_PATH = os.path.join(LOG_DIR, log_filename)
        
        # 매일 자정에 새 파일 생성 (when='midnight', interval=1)
        fh = TimedRotatingFileHandler(
            LOG_PATH, 
            when='midnight',
            interval=1,
            backupCount=30,  # 30일간 보관
            encoding="utf-8"
        )
        fh.suffix = "%Y-%m-%d"  # 백업 파일 형식
        fh.setFormatter(JsonLineFormatter())
        logger.addHandler(fh)
    return logger
