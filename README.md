# Liquirizia.DataAccessObject.Implements.PostgreSQL

DataAccessObject of PostgreSQL for Liquirizia

## 일반적인 사용 방법

- [샘플 코드](sample/Sample.py)

## 데이터 모델과 함께 사용

- [샘플 코드](sample/Sample.Model.py)
- [타입 샘플 코드](sample/Sample.Model.Type.py)

## 도커 빌드 및 실행

```shell
> docker image build --file=res/PostgreSQL.15.docker --tag=postgresql:15 .
> docker container run --name=postgresql --detach --publish=5432:5432 postgresql:15
```
