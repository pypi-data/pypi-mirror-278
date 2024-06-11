import os

# 필요한 환경 변수 목록
required_env_vars = [
    "MLFLOW_S3_ENDPOINT_URL",
    "MLFLOW_TRACKING_URI",
    "AWS_ACCESS_KEY_ID",
    "AWS_SECRET_ACCESS_KEY",
    "RABBIT_ENDPOINT_URL",
    "RABBIT_MODEL_UPLOAD_TOPIC",
    "TRAIN_ID",
    "MODEL_NAME",
]

# 환경 변수 검증
missing_vars = [var for var in required_env_vars if not os.environ.get(var)]

# 누락된 환경 변수가 있다면 에러 발생
if missing_vars:
    error_message = f"다음 환경 변수들이 설정되지 않았습니다: {', '.join(missing_vars)}"
    raise EnvironmentError(error_message)
