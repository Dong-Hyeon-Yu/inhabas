package com.inhabas.api.web;

import com.inhabas.api.web.argumentResolver.Authenticated;
import com.inhabas.api.auth.domain.oauth2.userInfo.OAuth2UserInfoAuthentication;
import com.inhabas.api.domain.member.domain.valueObject.MemberId;
import com.inhabas.api.domain.majorInfo.dto.MajorInfoDto;
import com.inhabas.api.domain.member.dto.AnswerDto;
import com.inhabas.api.domain.member.dto.MemberDuplicationQueryCondition;
import com.inhabas.api.domain.questionaire.dto.QuestionnaireDto;
import com.inhabas.api.domain.member.dto.SignUpDto;
import com.inhabas.api.domain.member.usecase.SignUpService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import io.swagger.v3.oas.annotations.responses.ApiResponses;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@Tag(name = "회원가입", description = "회원가입 기간이 아니면 403 Forbidden")
@RestController
@RequiredArgsConstructor
public class SignUpController {

    private final SignUpService signUpService;

    /* profile */

    @PostMapping("/signUp")
    @Operation(summary = "회원가입 시 개인정보를 저장한다.")
    @ApiResponses({
            @ApiResponse(responseCode = "204"),
            @ApiResponse(responseCode = "400", description = "잘못된 폼 데이터")
    })
    public ResponseEntity<?> saveStudentProfile(
            @Authenticated OAuth2UserInfoAuthentication authentication, @Valid @RequestBody SignUpDto form) {

        signUpService.saveSignUpForm(form, authentication);  //

        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    @GetMapping("/signUp")
    @Operation(summary = "임시저장한 학생의 개인정보를 불러온다.")
    @ApiResponse(responseCode = "200")
    public ResponseEntity<SignUpDto> loadProfile(
            @Authenticated OAuth2UserInfoAuthentication authentication, @Authenticated MemberId memberId) {

        SignUpDto form = signUpService.loadSignUpForm(memberId, authentication);

        return ResponseEntity.ok(form);
    }


    @GetMapping("/signUp/majorInfo")
    @Operation(summary = "회원가입에 필요한 전공 정보를 모두 불러온다.")
    @ApiResponse(responseCode = "200")
    public ResponseEntity<List<MajorInfoDto>> loadAllMajorInfo() {

        return ResponseEntity.ok(signUpService.getMajorInfo());
    }

    @GetMapping("/signUp/isDuplicated")
    @Operation(summary = "회원가입 시 필요한 중복검사를 진행한다.")
    @ApiResponses({
            @ApiResponse(responseCode = "200"),
            @ApiResponse(responseCode = "400", description = "하나도 안넘기거나, 타입이 잘못된 경우")
    })
    public ResponseEntity<?> validateDuplication(
            MemberDuplicationQueryCondition condition) {

            boolean isDuplicated = signUpService.validateFieldsDuplication(condition);

            return ResponseEntity.ok(isDuplicated);
    }

    /* questionnaire */

    @GetMapping("/signUp/questionnaires")
    @Operation(summary = "회원가입에 필요한 질문들을 불러온다.")
    @ApiResponse(responseCode = "200")
    public ResponseEntity<List<QuestionnaireDto>> loadQuestionnaire() {

        return ResponseEntity.ok(signUpService.getQuestionnaire());
    }

    /* answer */

    @GetMapping("/signUp/answers")
    @Operation(summary = "회원가입 도중 임시 저장한 질문지 답변을 불러온다.")
    @ApiResponse(responseCode = "200")
    public ResponseEntity<List<AnswerDto>> loadAnswers(@Authenticated MemberId memberId) {

        List<AnswerDto> answers = signUpService.getAnswers(memberId);

        return ResponseEntity.ok(answers);
    }

    @PostMapping("/signUp/answers")
    @Operation(summary = "회원가입 시 작성한 답변을 저장한다.")
    @ApiResponses({
            @ApiResponse(responseCode = "204"),
            @ApiResponse(responseCode = "400", description = "답변이 길이제한을 초과했을 경우")
    })
    public ResponseEntity<?> saveAnswers(
            @Authenticated MemberId memberId, @Valid @RequestBody List<AnswerDto> answers) {

        signUpService.saveAnswers(answers, memberId);

        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }

    /* finish signUp */
    @PutMapping("/signUp")
    @Operation(summary = "회원가입을 완료한다")
    @ApiResponse(responseCode = "204")
    public ResponseEntity<?> finishSignUp(@Authenticated MemberId memberId) {

        signUpService.completeSignUp(memberId);
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
