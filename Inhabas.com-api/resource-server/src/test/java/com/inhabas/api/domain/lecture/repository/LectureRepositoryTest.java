package com.inhabas.api.domain.lecture.repository;

import com.inhabas.api.domain.lecture.domain.Lecture;
import com.inhabas.api.domain.lecture.domain.valueObject.LectureStatus;
import com.inhabas.api.domain.lecture.dto.LectureDetailDto;
import com.inhabas.api.domain.lecture.dto.LectureListDto;
import com.inhabas.api.domain.member.domain.entity.Member;
import com.inhabas.testAnnotataion.DefaultDataJpaTest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.util.ReflectionTestUtils;

import java.time.LocalDateTime;
import java.util.ArrayList;

import static com.inhabas.api.domain.member.domain.MemberTest.MEMBER1;
import static org.assertj.core.api.Assertions.assertThat;

@DefaultDataJpaTest
public class LectureRepositoryTest {

    @Autowired
    private TestEntityManager em;

    @Autowired
    private LectureRepository repository;

    private Member chief;

    @BeforeEach
    public void setUp() {
        chief = em.persist(MEMBER1());
    }

    @DisplayName("강의글 단일 조회")
    @Test
    public void getTest() {

        //given
        Lecture entity = Lecture.builder()
                .title("절권도 배우기")
                .chief(chief.getId())
                .applyDeadline(LocalDateTime.of(9011, 1, 1, 1, 1, 1))
                .curriculumDetails("1주차: 빅데이터에 기반한 공격패턴분석<br> 2주차: ...")
                .daysOfWeek("월 금")
                .introduction("호신술을 배워보자")
                .method(1)
                .participantsLimits(30)
                .place("6호관 옥상")
                .build();
        entity = repository.save(entity);

        //when
        Integer id = (Integer) ReflectionTestUtils.getField(entity, "id");
        LectureDetailDto detailDto = repository.getDetails(id)
                .orElse(null);

        //then
        assertThat(detailDto).isNotNull();
        assertThat(detailDto.getChief().getId()).isEqualTo(12171234);
        assertThat(detailDto.getChief().getMajor()).isEqualTo("건축공학과");
        assertThat(detailDto.getChief().getName()).isEqualTo("유동현");
    }

    @DisplayName("강의글 목록 조회")
    @Test
    public void getListTest() {

        ArrayList<Lecture> lectures = new ArrayList<>();

        for (int i = 0; i < 4; i++) {
            Lecture lecture = Lecture.builder()
                    .title("절권도 배우기" + i)
                    .chief(chief.getId())
                    .applyDeadline(LocalDateTime.of(9011, 1, 1, 1, 1, 1))
                    .curriculumDetails("1주차: 빅데이터에 기반한 공격패턴분석<br> 2주차: ...")
                    .daysOfWeek("월 금")
                    .introduction("호신술을 배워보자")
                    .method(1)
                    .participantsLimits(30)
                    .place("6호관 옥상")
                    .build();
            ReflectionTestUtils.setField(lecture, "status", LectureStatus.values()[i]);
            lectures.add(lecture);
        }
        repository.saveAll(lectures);

        //when
        Page<LectureListDto> page = repository.getList(PageRequest.of(0, 6));

        //then
        assertThat(page.getTotalElements()).isEqualTo(2);
        assertThat(page.getNumberOfElements()).isEqualTo(2);
        assertThat(page.getTotalPages()).isEqualTo(1);
        assertThat(page.getContent().get(0)).extracting("title").isEqualTo("절권도 배우기3");
    }
}
