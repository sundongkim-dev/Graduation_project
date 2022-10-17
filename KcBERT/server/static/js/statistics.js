const CalcObj = {
    _result: null,

    _showResult: function(dataFromDB) {

        var table = document.getElementById("postsInfoTable")

        for (var i = 0; i<this._result.length; i++){
            for (var j = 0; j<dataFromDB[i].comments.length; j++){
                var row = `<tr>
                            <td>${i}</td>
                            <td>${dataFromDB[i].date}</td>
                            <td>${dataFromDB[i].board}</td>
                            <td>${dataFromDB[i].title}</td>
                            <td>${dataFromDB[i].content}</td>                            
                            <td>${dataFromDB[i].comments[j].message}</td>
                            <td>${dataFromDB[i].comments[j].result}</td>
                            <td>${dataFromDB[i].comments[j].precision}</td>
                            <td>${dataFromDB[i].tags}</td>
                </tr>`
                table.innerHTML += row
            }            
        }        
    },

	displayCommentsInfo: function() {
		var httpRequest = new XMLHttpRequest();

		httpRequest.addEventListener("load", () => {
			this._result = JSON.parse(httpRequest.responseText)["data"];
            console.log(this._result);
            console.log(this._result.length)
			this._showResult(this._result); // 데이터 가져오고 화면에 뿌림
		});
        // console.log(targetSentence);
		httpRequest.open("GET", "/statistics");
		httpRequest.send();
	}
}

const EventObj = {
    loadData: function () {
        CalcObj.displayCommentsInfo();
    }
}

function initConfig() {
    EventObj.loadData();
}

document.addEventListener("DOMContentLoaded", () => {
    initConfig();
});