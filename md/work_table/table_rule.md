* 모든 개발 작업(develop task)는 table 개념 단위로 관리된다.
* table 정의는 다음과 같다.
  * 작업의 목표와 범위를 반드시 명시한다.
    * purpose: 이 테이블이 해결하고자 하는 문제
    * range: 이 테이블이 관할하는 범위
  * 작업의 소 작업 (feature)를 리스트를 구성한다.
    * 각 소 작업에 대해서 목표(feature_purpose)와 범위(feature_range)를 명시한다.
  * 작업 간 완료/진행 중/ 진행 완료 작업을 기록한다
* table.md는 md/work_table/<task_name>/table.md 형태로 존재한다. 
  * task name은 kebab-case를 사용한다.