package com.inhabas.api.domain.signUpSchedule;

public class SignUpNotAvailableException extends RuntimeException {

    public SignUpNotAvailableException() {
        super("회원가입 기간이 아닙니다.");
    }
}
