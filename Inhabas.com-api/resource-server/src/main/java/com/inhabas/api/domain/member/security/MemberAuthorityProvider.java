package com.inhabas.api.domain.member.security;

import com.inhabas.api.auth.domain.exception.InvalidUserInfoException;
import com.inhabas.api.auth.domain.exception.UserNotFoundException;
import com.inhabas.api.auth.domain.oauth2.userAuthorityProvider.UserAuthorityProvider;
import com.inhabas.api.auth.domain.oauth2.userInfo.OAuth2UserInfo;
import com.inhabas.api.auth.domain.oauth2.userInfo.OAuth2UserInfoAuthentication;
import com.inhabas.api.auth.domain.token.securityFilter.UserPrincipalService;
import com.inhabas.api.domain.member.domain.valueObject.MemberId;
import com.inhabas.api.domain.member.repository.MemberRepository;
import com.inhabas.api.domain.team.domain.Team;
import com.inhabas.api.domain.member.domain.valueObject.Role;
import lombok.RequiredArgsConstructor;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;

@Component
@RequiredArgsConstructor
public class MemberAuthorityProvider implements UserAuthorityProvider {

    private final UserPrincipalService userPrincipalService;
    private final MemberRepository memberRepository;
    private static final String ROLE_PREFIX = "ROLE_";
    private static final String TEAM_PREFIX = "TEAM_";

    @Override
    @Transactional
    public Collection<SimpleGrantedAuthority> determineAuthorities(OAuth2UserInfo oAuth2UserInfo) {

        OAuth2UserInfoAuthentication authentication =
                new OAuth2UserInfoAuthentication(oAuth2UserInfo.getId(), oAuth2UserInfo.getProvider().toString(), oAuth2UserInfo.getEmail());
        MemberId memberId = (MemberId) userPrincipalService.loadUserPrincipal(authentication);

        if (Objects.isNull(memberId)) {  // 기존회원이 아니면, 로그인 불가!
            throw new UserNotFoundException();
        }
        else { // 기존회원이면,
            RoleAndTeamDto roleAndTeamDto = memberRepository.fetchRoleAndTeamsByMemberId(memberId);

            if (roleAndTeamDto.isEmpty())
                throw new InvalidUserInfoException();  // 가입된 소셜 계정으로 회원 프로필을 찾을 수 없는 경우.

            Role role = roleAndTeamDto.getRole();
            Collection<Team> teamList = roleAndTeamDto.getTeams();

            return new HashSet<>() {{
                add(new SimpleGrantedAuthority(ROLE_PREFIX + role.toString()));
                teamList.forEach(team -> add(new SimpleGrantedAuthority(TEAM_PREFIX + team.getName())));
            }};

        }
    }

    public static class RoleAndTeamDto {
        private final Role role;
        private final List<Team> teams;

        public RoleAndTeamDto(Role role, List<Team> teams) {
            this.role = role;
            this.teams = teams;
        }

        public Role getRole() {
            return role;
        }

        public List<Team> getTeams() {
            return teams;
        }

        boolean isEmpty() {
            return role == null && teams == null;
        }
    }

}
