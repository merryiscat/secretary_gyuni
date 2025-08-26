# 🍽️ 식사비서 재규니 (Secretary Gyuni)

한국 음식 추천 및 식당 검색 AI 어시스턴트

## 📋 개요

식사비서 재규니는 사용자의 의도를 분석하여 맞춤형 음식 추천과 식당 검색 서비스를 제공하는 AI 어시스턴트입니다. LangGraph와 LangChain을 기반으로 구축되었으며, 자연어 처리를 통해 다양한 대화 상황에 대응합니다.

## ✨ 주요 기능

- 🎯 **지능형 의도 분류**: 사용자 입력을 4가지 카테고리로 자동 분류
- 🍜 **음식 추천**: 개인 취향 기반 맞춤 음식 추천
- 📍 **식당 검색**: 위치 및 조건 기반 맞춤 식당 검색 
- 💬 **일상 대화**: 자연스러운 대화형 인터페이스
- 📊 **구조화된 로깅**: 모든 노드 실행 과정 추적 및 디버깅

## 🏗️ 아키텍처

### 워크플로우
```
사용자 입력 → 의도 분류 → 조건부 라우팅:
├─ 음식추천요청 → 음식 추천 → 종료
├─ 식당검색요청 → 의도 추출 → 키워드 랭킹 → 쿼리 생성 → MCP 검색 → 결과 생성
├─ 일상대화 → 대화 응답 → 종료
└─ 정체성문의 → 정체성 응답 → 종료
```

### 핵심 컴포넌트
- **Graph.py**: LangGraph 워크플로우 정의
- **State.py**: 상태 관리용 TypedDict 스키마
- **Node.py**: 비즈니스 로직 노드 구현
- **Mcp_Tool.py**: 외부 API 연동 (MCP)

## 🚀 설치 및 실행

### 환경 요구사항
- Python >= 3.10
- OpenAI API 키
- Kakao Map API 키
- Smithery API 키

### 설치
```bash
# 프로젝트 클론
git clone <repository-url>
cd secretary_gyuni

# 의존성 설치
pip install -e .
```

### 환경 변수 설정
`.env` 파일 생성:
```env
OPENAI_API_KEY=your_openai_api_key
KAKAO_MAP_API_KEY=your_kakao_map_api_key
SMITHERY_API_KEY=your_smithery_api_key
```

### 실행
```bash
# Streamlit 웹 UI 실행
streamlit run UI/main.py

# 브라우저에서 http://localhost:8501 접속
```

## 💡 사용 예시

### 음식 추천 요청
```
사용자: "오늘 저녁 뭐 먹을까?"
재규니: "오늘 저녁에는 따뜻한 국물 요리는 어떠세요? 김치찌개나 된장찌개를 추천드립니다..."
```

### 식당 검색 요청
```
사용자: "강남역 근처 이탈리안 레스토랑 추천해줘"
재규니: "강남역 근처 이탈리안 레스토랑 추천드립니다:
1. ○○○ 레스토랑 - 파스타 전문, 평점 4.5★
2. △△△ 피자리아 - 정통 이탈리안 피자..."
```

## 🔧 개발 가이드

### 프로젝트 구조
```
secretary_gyuni/
├── Graph.py              # LangGraph 워크플로우
├── State.py              # 상태 정의
├── Node.py               # 노드 구현
├── Mcp_Tool.py          # MCP 도구
├── UI/
│   └── main.py          # Streamlit UI
├── app/
│   ├── chain/           # LangChain 체인
│   │   ├── *.py         # 체인 구현
│   │   └── prompt/      # 프롬프트 템플릿
│   └── logger/          # 로깅 시스템
└── logs/                # 애플리케이션 로그
```

### 의도 분류 카테고리
1. **음식추천요청**: 일반적인 음식 추천 (예: "뭐 먹지?")
2. **식당검색요청**: 특정 조건의 식당 검색 (예: "강남 맛집 추천")
3. **일상대화**: 인사, 감사 등 일반 대화 (예: "안녕하세요")
4. **정체성문의**: AI 어시스턴트에 대한 질문 (예: "넌 누구니?")

### 로그 모니터링
```bash
# 실시간 로그 확인
tail -f logs/app.jsonl

# JSON 형태로 구조화된 로그 출력
```

## 🔌 외부 서비스 연동

### n8n 웹훅 서버
- **URL**: `http://localhost:5678/webhook/...`
- **용도**: 식당 검색 결과 제공
- **요구사항**: n8n 서버가 로컬에서 실행 중이어야 함

### Smithery.ai MCP 서버
- **서비스**: Kakao Map API 연동
- **용도**: 장소 추천 및 지도 정보 제공
- **인증**: SMITHERY_API_KEY 필요

## 🤝 기여하기

1. 이 저장소를 포크합니다
2. 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🐛 문제 해결

### 자주 발생하는 문제
1. **API 키 오류**: `.env` 파일의 API 키 확인
2. **MCP 연결 실패**: n8n 서버 상태 확인
3. **모듈 import 오류**: `pip install -e .` 재실행

### 디버깅
- 구조화된 로그: `logs/app.jsonl` 확인
- Streamlit 콘솔 출력 활용
- 각 노드별 상태 추적 가능

## 📞 지원

문제가 발생하거나 제안사항이 있으시면 이슈를 등록해 주세요.