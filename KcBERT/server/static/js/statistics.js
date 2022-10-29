const CalcObj = {
    _result: null,

    _showResult: function() {
        var table = document.getElementById("postsInfoTable");

        for (var i = 0; i<this._result.length; i++){
            var row = `<tr onclick="EventObj.hoverComment(this);">
                            <td>${i}</td>
                            <td>${this._result[i].date}</td>
                            <td>${this._result[i].board}</td>
                            <td>${this._result[i].title}</td>
                            <td>${this._result[i].content}</td>                            
                            <td>${this._result[i].tags}</td>
                        </tr>`;
            table.innerHTML += row;

            var row = `
                <tr class="comment d-none table-active" onclick="EventObj.hoverComment(this.previousElementSibling);">
                    <td colspan="12">
                        <table class = "table table-secondary table-hover table-bordered align-middle">
                            <thead>
                                <tr>
                                    <th scope="col">댓글 내용</th>
                                    <th scope="col">예측 결과</th>
                                    <th scope="col">신뢰도</th>
                                </tr>
                            </thead>
                            <tbody>
                                {{tbody}}
                            </tbody>
                        </table>
                    </td>
                </tr>
            `;
            var tbody = "";
            for (var j = 0; j<this._result[i].comments.length; j++){
                    tbody += `<tr>                           
                            <td>${this._result[i].comments[j].message}</td>
                            <td>${this._result[i].comments[j].result}</td>
                            <td>${this._result[i].comments[j].precision}</td>
                        </tr>`
            }

            if (tbody) {
                table.innerHTML += row.replace("{{tbody}}", tbody);
            }
        }
    },

	displayCommentsInfo: function() {
		var httpRequest = new XMLHttpRequest();

		httpRequest.addEventListener("load", () => {
			this._result = JSON.parse(httpRequest.responseText)["data"];
            console.log(this._result);
            console.log(this._result.length)
			this._showResult(); // 데이터 가져오고 화면에 뿌림
		});
		httpRequest.open("GET", "/statistics");
		httpRequest.send();
	}
}

const EventObj = {
    loadData: function () {
        CalcObj.displayCommentsInfo();
    },
    hoverComment: function(obj) {
        // tr을 눌렀을 때 그 다음 행이 댓글행인 경우 on/off
        if (obj.nextElementSibling.classList.contains("comment")) {
            if (obj.nextElementSibling.classList.contains("d-none")) {
                obj.nextElementSibling.classList.remove("d-none");
                obj.classList.add("table-active");
            } else {
                obj.nextElementSibling.classList.add("d-none");
                obj.classList.remove("table-active");
            }
        }
        console.log(obj.nextElementSibling);
    }
}

function initConfig() {
    EventObj.loadData();
}

document.addEventListener("DOMContentLoaded", () => {
    initConfig();
});