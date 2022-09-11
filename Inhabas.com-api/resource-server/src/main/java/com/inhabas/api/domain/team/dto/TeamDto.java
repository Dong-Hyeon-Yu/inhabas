package com.inhabas.api.domain.team.dto;

import com.inhabas.api.domain.team.domain.Team;
import com.inhabas.api.domain.team.domain.valueObject.TeamName;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;

@Setter
@NoArgsConstructor
public class TeamDto {

    @NotNull @Positive
    private Integer id;

    @NotNull
    private TeamName teamName;


    public TeamDto(Integer id, String teamName) {
        this.id = id;
        this.teamName = new TeamName(teamName);
    }

    public TeamDto(Team team) {
        this(team.getId(), team.getName());
    }

    public Integer getId() {
        return id;
    }

    public String getTeamName() {
        return teamName.getValue();
    }

    public static TeamDto from(Team team) {
        return new TeamDto(team.getId(), team.getName());
    }
}
