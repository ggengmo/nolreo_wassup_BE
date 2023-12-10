# CONVENTION

## 목차
[1. COMMIT 컨벤션](#1-COMMIT-컨벤션)<br>
[2. 코드 컨벤션](#2-코드-컨벤션)<br>
&ensp;[2-1. Python](#2-1-python)<br>
&ensp;[2-2. HTML/CSS](#2-2-htmlcss)<br>
&ensp;[2-3. JavaScript](#2-3-javascript)

## 1. COMMIT 컨벤션
### 태그
|이모지 |이모지 태그             |태그 이름        |설명                                                               |
|-------|-----------------------|----------------|------------------------------------------------------------------|
|✨    |`:sparkles:`           |Feat            |새로운 기능을 추가할 경우                                            |
|🐛    |`:bug:`                |Fix             |버그를 고친 경우                                                    |
|💄    |`:lipstick:`           |Design          |CSS 등 사용자 UI 디자인 변경                                         |
|🎨    |`:art:`                |Style           |코드 포맷 변경, 세미 콜론 누락, 코드 수정이 없는 경우                  |
|♻️     |`:recycle:`            |Refactor        |프로덕션 코드 리팩토링                                               |
|💡    |`:bulb:`               |Comment         |필요한 주석 추가 및 변경                                             |
|📝    |`:memo:`               |Docs            |문서를 수정한 경우                                                   |
|🧪    |`:test_tube:`          |Test            |테스트 추가, 테스트 리팩토링(프로덕션 코드 변경 X)                     |
|👷    |`:construction_worker:`|Chore           |빌드 태스트 업데이트, 패키지 매니저를 설정하는 경우(프로덕션 코드 변경 X)|
|🚚    |`:truck:`              |Rename          |파일 혹은 폴더명을 수정하거나 옮기는 작업만인 경우                     |
|🔥    |`:fire:`               |Remove          |파일을 삭제하는 작업만 수행한 경우                                    |
|👽️    |`:alien:`              |!BREAKING CHANGE|커다란 API 변경의 경우                                               |
|🐛    |`:bug:`                |!HOTFIX         |급하게 치명적인 버그를 고쳐야하는 경우                                |


### Commit 예시(Feat)
```
(커밋 이모지)Feat: 제목(추가한 기능 / 변경한 기능) (# 이슈번호)
✨Feat: Login 기능 개발 (#13)

- 수정 파일
main.py
index.py

- 추가한 기능
Login 기능 추가

(필요한 경우) - 비고
```
### Commit 예시(Fix)
```
Fix 변경한 기능 (#이슈번호)
🐛Fix: type_message_and_enter (#3)

- 수정 파일
main.py
index.py

- 원인
스터디 멤버들 호출 시 @'이름'에서 'tab'이 안눌림

- 수정
호출 인원이 많을 시 디스코드 반응이 늦어지는 것이 원인으로, sleep(0.1)을 sleep(0.3)으로 수정. 이후 또 안되면 0.5로 수정

(필요한 경우) - 비고
```

## 2. 코드 컨벤션
 ## 2-1. Python
  - 전체적인 컨벤션 기준은 [PEP 8](https://peps.python.org/pep-0008/)로 한다.

  ### 공통
   - 탭 간격 들여쓰기 4칸
   - 기본적으로 문자형은 '' 사용
   - 주석 위치: def, class 다음 라인에 ''' '''
   - import * 지양 (개별적으로 import)
   - 라인별 최대 길이는 72(왠만하면 가독성있는 방향)
   - 소스 코드 파일 마지막 라인은 enter 한번 추가해서 끝내기
   - protected 인스턴스 속성 : 시작은 _ 이후는 스네이크(예시 _leading_underscore)
   - private 인스턴스 속성 : 시작은 __ 이후는 스네이크(__double_leading_underscore)
   
  ### 변수
   - 네이밍: 스네이크(예시 hello_world) & only 소문자
   - 'l'(소문자 엘), 'O'(대문자 오) 또는 'I'(대문자 아이) 문자를 단일 문자 변수 이름으로 사용 금지(예시 I, l, O <- 이렇게 사용 X)

  ### 함수
   - 네이밍: 스네이크 & only 소문자(예시 create_app)
   - 함수 끝난 이후 다음 코드 시작시 enter 1칸

  ### Django 코드
  - Settings.py의 SECRET_KEY는 절대로 외부로 유출되지 않게 한다. PostgreSQL을 쓸 경우에도 포함

  - URL 패턴, 템플릿 블록 이름에는 대시(-) 대신 밑줄(_)을 이용한다
  - template 변수 적용 시 변수 이름 앞 뒤 띄어쓰기 => {{ foo }} 와 같은 형태로 사용한다 ({{foo}} 처럼 사용 X)
  - Model 필드 설정 시 소문자로만 작성한다
    - Model에서 Meta 사용 시 class의 변수를 설정한 후 Meta를 설정한다.
        
  - [이외의 Django 컨벤션 기준](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
  
 ### 클래스
 - 네이밍: CapWards
 - 함수 끝난 이후 다음 코드 시작시 enter 2칸
 - 인스턴스 메서드 첫 파라미터 이름은 self
 - 클래스 메서드 첫 파라미터 이름은 cls

 ### 예외
 - 네이밍: CapWards

 ### 상수
 - 네이밍: ALL_CAPS
 - 관리: APP별 상수 파일에서 관리

 ## 2-2. HTML/CSS
 ## HTML
 - " 먼저 ' 이후
 ### 가독성: 유효하고 읽기 쉬운 DOM 작성
 - 모든 태그는 lowercase
 - 들여쓰기 2칸
 - HTML에서 주석 사용은 지양하기
 - 컴포넌트 시작과 끝에 주석 달기
    ```html
    <!-- BEGIN NAVBAR --> <!-- END NAVBAR -->
    ```
 
 ### script 태그
 - 맨 아래 배치
 - 본문과 스크립트의 로딩 순서의 문제로 오류 발생 가능
 - script를 아래 두고도 해결이 안되면 defer 태그 추가

 ### 접근성
 - 이미지에 alt 태그 사용
   - 로드, 경로 문제 등으로 이미지가 나오지 않을 때 텍스트가 표시되도록
 - 하나의 페이지에는 하나의 h1
   - h1~h5 순서대로 나올 수 있도록하고 글자 크기가 마음에 안 들 경우 CSS에서 수정
 - 제목 및 메타 태그 사용
 - 페이지 완성 시 HTML [유효성 확인 (w3c 유효성 검사기)](https://validator.w3.org/)
   
 ##  CSS
 - " 먼저 ' 이후
 - 들여쓰기 2칸
 - 인라인 스타일 사용 지양
   - (예외) 인라인 크리티컬 CSS : 중요한 CSS의 경우 맨 위에 배치

 ## 2-3. JavaScript
 - " 먼저 ' 이후
 - 들여쓰기 2칸
 - 소스파일의 이름은 알파벳 소문자, 대쉬(-), 밑줄(_)으로만 작성 (예시 main_function.js)
 - 인라인 스크립트 사용 지양

 ### 중괄호의 사용은 Kernighan and Ritchie Style에 따른다.
 - 여는 중괄호 전에는 줄을 바꾸지 않으며, 이후에 줄을 바꾼다.
 - 닫는 중괄호 전에 줄을 바꾸며, 이후에 줄을 바꿔준다.
    ```JavaScript
    //  예시
    class InnerClass {
      constructor() {}

      /** @param {number} foo */
      method(foo) {
        if (condition(foo)) {
          try {
            something();
          } catch (err) {
            recover();
          }
        }
      }
    }
    ```
 ### 변수 선언
 - 가능하면 const를 사용한다.
 - const 변수를 먼저 선언하고 그룹화한 뒤 let 변수를 선언한다.
    ```JavaScript
    // 예시
    const goSportsTeam = true;
    const items = getItems();
    let dragonball;
    let i;
    let length;
    ```

<!-- # 문서 컨벤션 -->