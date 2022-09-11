# 빅데이터 동아리 LMS 홈페이지 개발기 

---

## :writing_hand: 1. 서비스 구축
### 개발 기간
  : 2021.04.01 ~ 2021.08.31
### github
  : https://github.com/YangTaeyoung/IBAS  
### 기술 스택
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=NGINX&logoColor=white"> <img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=MariaDB&logoColor=white"> <img src="https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=Vue.js&logoColor=white"> <img src="https://img.shields.io/badge/GoDaddy-1BDBDB?style=for-the-badge&logo=GoDaddy&logoColor=white">
#### 특징 
  - 개발 처음 해보는 사람들끼리 보여서, 굴러가는 서비스를 어떻게든 만들어보자는 취지에서 제작.
  - 회원 관리, 게시판, 댓글, 강의, 스터디, 취미 모임, 소셜로그인, 마이페이지 등의 기능을 구현.
#### 맡은 일
1. 강의 CRUD, 수강생 관리, 출석 및 과제 관리 등 기능 구현
2. 코드를 깨끗하게 작성하고자 하는 노력 -> `django form` 을 공부하여 팀 내에 도입. [[블로그 글 참고]](https://letsmakemyselfprogrammer.tistory.com/27)
3. BaseFile 클래스를 상속받도록 하여 파일 처리 `코드 중복 최소화` -> [[블로그 글 참고]](https://letsmakemyselfprogrammer.tistory.com/28)
4. `(django rest + vue.js)` 댓글 부분만 vue.js 로 먼저 빌드한 다음에 django 에서 임포트하는 형식으로 ssr 구현. [[블로그 글 참고]](https://letsmakemyselfprogrammer.tistory.com/41)
4. javascript 로 사용자 입력 폼 validation 코드 작성
  
---

## :smile: 2. 첫 운영 시작
### 개발기간
  : 2021.09.01 ~ 2021.12.31
### github
  : https://github.com/InhaBas/Inhabas.com
### 기술 스택
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=Django&logoColor=white"> <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=NGINX&logoColor=white"> <img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=MariaDB&logoColor=white"> <img src="https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=Vue.js&logoColor=white"> <img src="https://img.shields.io/badge/Sentry-362D59?style=for-the-badge&logo=Sentry&logoColor=white"> <img src="https://img.shields.io/badge/GoDaddy-1BDBDB?style=for-the-badge&logo=GoDaddy&logoColor=white"> <img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white">
### 특징
 - 서비스를 런칭하고 실제 발생하는 장애에 대응.
 - 유지보수를 위한 아키텍쳐 고안 및 버그 개선
### 맡은 일
  1. 팀장을 맡게 됨.
  2. 효율적인 협업과 이슈 관리를 위해 `github flow` 도입 [[당시 노션 공지]](https://fragrant-comfort-49c.notion.site/Git-Convention-ba9845b725934591878627f25554cf37)
  3. 깃헙의 issue 와 discussion 기능을 활용하고자 함. jira 대신 issue 를 사용. 
  4. 브라우저의 정적파일 캐시로 인해 수정된 파일이 업데이트 되지 않는 이슈 -> `static file name hashing` 기능 추가 [[블로그 글]](https://letsmakemyselfprogrammer.tistory.com/42)
  5. [[새로운 아키텍쳐 고안]](https://github.com/InhaBas/Inhabas.com/discussions/76) : `DB`, `views`, `권한` 간의 의존성이 커서 유지보수가 힘듦 -> 파이썬으로 `layered architecture` 구현. [(링크)](https://github.com/Dong-Hyeon-Yu/Inhabas.com/commit/6520c3041bccb5dea9f76c2ca9f83a42442e676a)
  6. [[새로운 권한체계 고안]](https://github.com/InhaBas/Inhabas.com/discussions/77) : 현재 권한 검사하는 로직이 여기저기 흩어져 있어서 유지보수가 힘듦 -> django 기본 권한 기능을 활용하는 방식으로 재설계하여 `AuthUser` 추가
  7. 어플 제작을 위한 rest api 서버로의 전환 결정 [[블로그 글]](https://letsmakemyselfprogrammer.tistory.com/64)
  8. 운영서버와 개발서버 분리 -> 개발 결과물을 미리 테스트
#### 장애 대응
  1. (2021-09-13) 특정 페이지에서 파일에 접근 할 수 없다는 오류 -> uwsgi 메인 프로세스가 여러개 돌아가면서 발생했던 문제. [[블로그 글]](https://letsmakemyselfprogrammer.tistory.com/47)
  2. 기타 자잘한 버그 개선 및 기능 추가.
  
  ---
  
## :airplane: 3. Spring Rest Server 개발
### 개발기간
  : 2021.01.01 ~ 2021.08.09
### github
  : https://github.com/InhaBas/Inhabas.com-api
### 기술 스택
  <img src="https://img.shields.io/badge/SpringBoot-6DB33F?style=for-the-badge&logo=SpringBoot&logoColor=white"> <img src="https://img.shields.io/badge/Swagger-85EA2D?style=for-the-badge&logo=Swagger&logoColor=white"> <img src="https://img.shields.io/badge/SpringSecurity-6DB33F?style=for-the-badge&logo=SpringSecurity&logoColor=white"> <img src="https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white"> <img src="https://img.shields.io/badge/githubActions-2088FF?style=for-the-badge&logo=GithubActions&logoColor=white"> <img src="https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=Vue.js&logoColor=white"> <img src="https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=NGINX&logoColor=white"> <img src="https://img.shields.io/badge/mariadb-003545?style=for-the-badge&logo=MariaDB&logoColor=white"> <img src="https://img.shields.io/badge/Amazon-FF9900?style=for-the-badge&logo=AmazonEC2&logoColor=white"> <img src="https://img.shields.io/badge/JUnit5-25A162?style=for-the-badge&logo=JUnit5&logoColor=white"> <img src="https://img.shields.io/badge/Cloudflare-F38020?style=for-the-badge&logo=Cloudflare&logoColor=white">
#### 특징
  - 어플 제작을 가능하게 하기 위한 rest api 서버 개발
  - 기존 유지보수에 관한 고민을 녹여냄. `객체지향 설계 원칙(SOLID)`, `layered architecture`, `MultiModule vs MSA`, `인증 코드 분리 -> 인증 모듈 개발`, `DDD`, `table 재설계` 등 
  - 졸업준비로 더이상 시간을 낼 수 없어서 진행률 75% 정도에서 중단.
  - 혼자 작성한 순수 알짜 코드량 ***2만 3천줄*** 이상, 개발 중에 갈아엎었던 코드 포함하면 ***약 3만줄 이상 코드*** 작성. 
#### 맡은 일
  1. 기존에 `django`로 제공하던 서비스를 `layered architecture` + `SOLID` + `DDD` 를 적용하여 `spring`으로 구현.
  2. 모든 `usecase(serivce)` 와 `api endpoint(controller)` 에 대한 테스트 코드 작성
  3. 인증 모듈 개발(Oauth2.0 구글, 네이버, 카카오 + JWT 토큰) [(SpringSecurity 공부 글)](https://github.com/InhaBas/Inhabas.com-api/issues/3), [(완성된 인증 모듈 docs)](https://letsmakemyselfprogrammer.tistory.com/121)
  4. spring security 인가 관련 테스트 코드 작성 (spring security context 테스트용 모킹 어노테이션 등)
  5. 개발용 원격 db 접속 ssh tunneling 설정.
  6. `spring cloud config` 를 통해서 운영환경별 설정파일 관리.
  7. `github action` 을 통한 배포 자동화.
  8. `on-premise` 에서 `aws` 로 전환, savings_plan 적용하여 비용 절약
  9. 게시글 관련 테이블 재설계 [[블로그 글 참고]](https://letsmakemyselfprogrammer.tistory.com/38)
  10. `swagger` 명세 작성.
  11. 백엔드 팀원 교육 [[교육 자료]](https://letsmakemyselfprogrammer.tistory.com/83)
#### 장애 대응
  1. `(2022.01.11)` tls 인증서 적용 갑자기 안되는 문제 [[블로그 글]](https://letsmakemyselfprogrammer.tistory.com/48)
  2. `(2022.03.13)` 로그인 관련 오류 [[블로그 글]](https://letsmakemyselfprogrammer.tistory.com/65)
  3. `(2022.03.14~15)` 호환성을 고려한 소셜로그인 버그 수정 [[블로그 글]](https://letsmakemyselfprogrammer.tistory.com/69)
  4. `(2022.04.01)` mariadb 죽음 [[블로그 글]](https://letsmakemyselfprogrammer.tistory.com/84)
  5. `(2022.06.21)` cloudflare 관련 520 error [[블로그 글 참고]](https://letsmakemyselfprogrammer.tistory.com/118)
  
  
