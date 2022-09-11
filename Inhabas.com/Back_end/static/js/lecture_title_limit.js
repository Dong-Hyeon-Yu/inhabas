window.onload = function () {
    //게시글 최 상단 div를 가리킴
    var lectNum = document.getElementsByClassName("lectTitle").length;

    // 게시글 개수만큼 for문을 돌림
    for (var j = 0; j < lectNum; j++) {

        var lectTitle = document.getElementsByClassName("lectTitle")[j].innerHTML;

        // 게시글 제목이 23보다 길면 ...붙임
        if (lectTitle.length >= 20) {
            lectTitle = lectTitle.substr(0, 20) + "...";
            document.getElementsByClassName("lectTitle")[j].innerHTML = lectTitle
        }

    }

    for (var k = 0; k < lectNum; k++) {

        var lectDay = document.getElementsByClassName("lectDay")[k].innerHTML;

        document.getElementsByClassName("lectDay")[k].innerHTML = lectDay.padEnd(14, '\u00A0')

    }

}
