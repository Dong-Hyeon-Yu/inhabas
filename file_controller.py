import shutil
from DB.models import Board, BoardFile, ContestBoard, ContestFile, Lect, Bank, BankFile,UserDelete,UserDeleteFile
import os
from IBAS.settings import MEDIA_ROOT
from django.conf import settings


# 1. 파일 폼이 여기 있기 때문에, 파일 컨트롤러도 여기 있는게 좋지 않을까요..?
# 2. 클래스로 선언하는게 더 좋을 듯??
#       다른 곳에서 FileBaseForm 을 상속받아 정의할 때, 파일 컨트롤러를 사용한다면,
#       FileController.is_image() 처럼 사용할텐데,
#       위처럼 사용하는게, 단순히 is_image() 로 사용하는 것보다 출처가 명확하게 표현되는 장점이 있을듯
class FileController:
    # 이미지인지 확인하는 함수. 파라미터(파일 경로)
    @staticmethod
    def is_image(file_path):
        path, ext = os.path.splitext(str(file_path))

        if ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
            return True
        else:
            return False

    # 파일인지 확인 하는 함수 파라미터(파일 경로).
    @staticmethod
    def is_code_file(file_path):
        path, ext = os.path.splitext(str(file_path))
        if ext in ['.py', '.java', '.css', 'js', '.html', '.r', '.ipynb', 'txt']:
            return True
        else:
            return False

    @staticmethod
    def is_file(file_path):
        return not FileController.is_image(file_path)

    # ------ get_code_in_file ------- #
    # INPUT : 해석할 파일 경로(미디어 루트 제외)
    # OUTPUT : 없음
    # RETURN : 파일에 있던 코드가 STR형으로 반환
    # 최종 수정일시 : 21.05.28
    # 설명: JS code view API에 코드 파일을 str형으로 넣기 위해서 코드를 해석하기 위한 함수
    # 작성자: 양태영
    @staticmethod
    def get_code_in_file(file_path):
        with open(os.path.join(settings.MEDIA_ROOT, file_path), mode="r") as file:
            lines = file.read()
            return lines

    # ---- get_images_and_files_of_ ---- #
    # INPUT : Board 객체 or ContestBoard 객체
    # OUTPUT : 없음
    # RETURN : tuple type / (게시글전체파일 리스트,게시글이미지파일 리스트,게시글문서파일 리스트)
    # :
    # 마지막 수정 일시 : 2021.04.13
    # 작성자 : 유동현
    @staticmethod
    def get_images_and_files_of_(object):
        image_list = []
        doc_list = []

        files = set()  # 쿼리셋을 담기 위한 empty Set 생성
        try:
            # Board 객체
            if isinstance(object, Board):
                files = BoardFile.objects.filter(board_no=object.board_no)
            # ContestBoard 객체
            elif isinstance(object, ContestBoard):
                files = ContestFile.objects.filter(contest_no=object.contest_no)
            elif isinstance(object, UserDelete):
                files = UserDeleteFile.objects.filter(user_delete_no=object.user_delete_no)
            else:  # 객체가 잘못 전달된 경우
                raise Exception

            # 파일을 이미지 파일과 일반 문서 따로 분리
            for file in files:
                if FileController.is_image(file.file_path):
                    image_list.append(file)
                else:
                    doc_list.append(file)

            return files, image_list, doc_list

        # 잘못된 객체가 전달될 경우
        except Exception as error:
            print(error)  # LOGGING :: 로그 파일 생성하는 코드 나중에 수정해야 함.

    # ---- delete_all_files_of_ ---- #
    # INPUT : HttpRequest 객체, File 객체 리스트
    # OUTPUT : 없음
    # RETURN : 없음
    # : 게시글 수정하는 과정에서 사용자가 제거한 파일들을 삭제함.
    # 마지막 수정 일시 : 2021.04.13
    # 작성자 : 유동현
    @staticmethod
    def remove_files_by_user(request, files):
        for file in files:
            # exist_file_path_{파일id}가 없는 경우: 사용자가 기존에 있던 파일을 삭제하기로 결정하였음 (input tag가 없어지면서 값이 전송되지 않음)
            if request.POST.get("exist_file_path_" + str(file.file_id)) is None:
                location = os.path.join(MEDIA_ROOT, str(file.file_path))
                # 해당 파일이 존재하면 삭제 (존재하지 않는 경우 에러 발생)
                if os.path.exists(location):
                    os.remove(location)  # 기존에 있던 저장소에 파일 삭제

                file.delete()  # db 기록 삭제

    # ---- delete_all_files_of_ ---- #
    # INPUT : Board 객체 or ContestBoard 객체
    # OUTPUT : 없음
    # RETURN : 없음
    # : 해당 게시글의 모든 파일을 삭제한다.
    # 마지막 수정 일시 : 2021.05.18
    # 작성자 : 유동현
    @staticmethod
    def delete_all_files_of_(obj):
        location = obj.get_file_path  # get_file_path : DB model 별 멤버변수로 선언해줘야함.

        try:
            if os.path.exists(location):  # 해당 경로가 존재하지 않는 경우에는 db 에서만 지워주면 된다.
                shutil.rmtree(location, ignore_errors=False)  # 해당 디렉토리를 포함하여 하위 폴더/파일 삭제
        except Exception as error:
            print(error)  # LOGGING :: 로그 파일 생성하는 코드 나중에 수정해야 함.

    # ---- upload_new_files_of_contest ---- #
    # INPUT : InMemoryUploadedFile 객체 리스트 / Board 또는 ContestBoard 객체
    # OUTPUT : 없음
    # RETURN : 없음
    # : 새로 입력받은 파일들을 업로드
    # 마지막 수정 일시 : 2021.04.30
    # 작성자 : 유동현
    @staticmethod
    def upload_new_files(files_to_upload, instance):
        # 새로 사용자가 파일을 첨부한 경우
        # files_to_upload : InMemoryUploadedFile 객체 리스트를 넘겨 받는다.
        #                   파일 폼에서 save() 할 때 이 함수를 호출!
        if isinstance(instance, ContestBoard):
            for file in files_to_upload:  # 각각의 파일을 InMemoryUploadedFile 객체로 받아옴
                ContestFile.objects.create(
                    contest_no=ContestBoard.objects.get(pk=instance.contest_no),
                    file_path=file,  # uploadedFile 객체를 imageField 객체 할당
                    file_name=file.name.replace(' ', '_')  # imageField 객체에 의해 파일 이름 공백이 '_'로 치환되어 서버 저장
                    # 따라서 db 에도 이름 공백을 '_'로 치환하여 저장
                )
        elif isinstance(instance, Board):
            for file in files_to_upload:
                BoardFile.objects.create(
                    board_no=Board.objects.get(pk=instance.board_no),
                    file_path=file,  # uploadedFile 객체를 imageField 객체 할당
                    file_name=file.name.replace(' ', '_')  # imageField 객체에 의해 파일 이름 공백이 '_'로 치환되어 서버 저장
                    # 따라서 db 에도 이름 공백을 '_'로 치환하여 저장
                )
        elif isinstance(instance, Bank):
            for file in files_to_upload:
                BankFile.objects.create(
                    bank_no=Bank.objects.get(pk=instance.bank_no),
                    file_path=file,
                    file_name=file.name.replace(' ', '_')
                )

        elif isinstance(instance, UserDelete):
            for file in files_to_upload:
                print(instance.user_delete_no)
                print(UserDelete.objects.get(pk=instance.user_delete_no))
                UserDeleteFile.objects.create(
                    user_delete_no=UserDelete.objects.get(pk=instance.user_delete_no),
                    file_path=file,
                    file_name=file.name.replace(' ', '_')
                )