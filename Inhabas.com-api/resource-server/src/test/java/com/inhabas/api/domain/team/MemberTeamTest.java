package com.inhabas.api.domain.team;

import static org.assertj.core.api.Assertions.assertThat;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.inhabas.api.domain.member.domain.entity.Member;
import com.inhabas.api.domain.member.domain.valueObject.IbasInformation;
import com.inhabas.api.domain.member.domain.valueObject.MemberId;
import com.inhabas.api.domain.member.domain.valueObject.Role;
import com.inhabas.api.domain.member.domain.valueObject.SchoolInformation;
import com.inhabas.api.domain.member.repository.MemberRepository;
import com.inhabas.api.domain.team.domain.MemberTeam;
import com.inhabas.api.domain.team.domain.Team;
import com.inhabas.api.domain.team.repository.MemberTeamRepository;
import com.inhabas.api.domain.team.repository.TeamRepository;
import com.inhabas.testAnnotataion.DefaultDataJpaTest;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.TestEntityManager;

@DefaultDataJpaTest
public class MemberTeamTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private MemberTeamRepository memberTeamRepository;

    @Autowired
    private TeamRepository teamRepository;

    @Autowired
    MemberRepository memberRepository;

    private Team IT;
    private Member member;

    @BeforeEach
    public void setUp() {
        IT = entityManager.persist(new Team("IT 부서"));

        member = entityManager.persist(
                new Member(new MemberId(12171652), "유동현", "010-0000-0000", "my@gmail.com","",
                        SchoolInformation.ofUnderGraduate("건축공학과", 3),
                        new IbasInformation(Role.BASIC_MEMBER)));

        memberTeamRepository.save(new MemberTeam(member, IT));

        entityManager.flush();
        entityManager.clear();
    }

    @DisplayName("팀을 삭제하면, 해당 팀에 속한 멤버들이 팀에서 방출된다.")
    @Test
    public void expelledByDeletingTeamsTest() {

        //when
        teamRepository.deleteById(IT.getId());
        entityManager.flush();
        entityManager.clear();

        //then
        assertThat(entityManager.find(Team.class, IT.getId())).isNull();
        assertTrue(memberTeamRepository.findAll().isEmpty());

    }

    @DisplayName("회원을 삭제하면, 해당 팀에 소속된 회원 목록에서 사라진다.")
    @Test
    public void vanishedByDeletingMemberProfileTest() {

        //when
        memberRepository.deleteById(member.getId());
        entityManager.flush();
        entityManager.clear();

        //then
        assertThat(entityManager.find(Member.class, member.getId())).isNull();
        assertTrue(memberTeamRepository.findAll().isEmpty());

    }

}
