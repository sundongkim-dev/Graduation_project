const CalcObj = {
    _result: null,

    _showResult: function() {
        // console.log(this._result);
        var classes = this._result["classes"];
        var maxClass = this._result["maxClass"];
        var reliability = this._result["reliability"];
        var scores = this._result["scores"];

        // 결과 표에 입력
        for (var i = 0; i < classes.length; i++) {
            document.getElementById("value" + (i + 1)).innerText = Math.round(scores[i] * 100) / 100;
        }

        // 신뢰도 입력
        document.getElementById("reliability").innerText = Math.round(reliability * 100 * 10) / 10;

        if (maxClass == "clean") {
            document.getElementById("classResult").innerText = "정상";
            document.querySelector(".alert").className = "alert alert-primary";
        } else if (maxClass == "curse") {
            document.getElementById("classResult").innerText = "악플";
            document.querySelector(".alert").className = "alert alert-warning";
        } else {
            document.getElementById("classResult").innerText = "혐오";
            document.querySelector(".alert").className = "alert alert-danger";
        }

        document.querySelector(".result").style.display = "block";
    },

	predictSentence: function(targetSentence) {
		var httpRequest = new XMLHttpRequest();

		httpRequest.addEventListener("load", () => {
            console.log(httpRequest.responseText);
			this._result = JSON.parse(httpRequest.responseText);

			this._showResult();
		});
        console.log(targetSentence);
		httpRequest.open("GET", "/predict/{targetSentence}".replace("{targetSentence}", targetSentence));
		httpRequest.send();
	}
}

const EventObj = {
    setEventListeners: function () {
        document.getElementById("calcButton").addEventListener("click", () => {
            CalcObj.predictSentence(document.getElementById("targetSentence").value);
        });
    }
}

function initConfig() {
    EventObj.setEventListeners();
}

document.addEventListener("DOMContentLoaded", () => {
    initConfig();
});