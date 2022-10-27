const ShowObj = {
    _chartSet: {'postDailyChart': null, 'commentDailyChart': null, 'lineDailyChart': null,
                'postMonthlyChart': null, 'commentMonthlyChart': null, 'lineMonthlyChart': null},

    displayChart: function() {
        this._chartSet.postDailyChart = new Chart(document.getElementById('postDailyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '혐오조장'],
                datasets: [{
                    label: '일간 게시글 분석',
                    data: [123, 12], // [정상게시글수, 혐오조장게시글수]
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        this._chartSet.commentDailyChart = new Chart(document.getElementById('commentDailyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '악플', '혐오'],
                datasets: [{
                    label: '일간 댓글 분석',
                    data: [1234, 123, 123], // [정상댓글수, 악플댓글수, 혐오댓글수]
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        this._chartSet.lineDailyChart = new Chart(document.getElementById('lineDailyChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
                datasets: [{
                    label: '전일 혐오조장글 수',
                    data: [15, 20, 25, 30, 15, 25, 30, 15, 15, 20, 25, 30, 15, 25, 30, 15, 15, 20, 25, 30, 15, 25, 30, 15], // 전일 시간별 악성 댓글 수 배열
                    fill: true,
                    borderColor: 'rgb(211, 211, 211)',
                    tension: 0.05
                    }, {
                    label: '금일 혐오조장글 수',
                    data: [10, 25, 40, 50, 30, 15], // 금일 시간별 혐오조장 게시글 수 배열
                    fill: true,
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.05
                    }
                ]
            }
        });

        this._chartSet.postMonthlyChart = new Chart(document.getElementById('postMonthlyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '혐오조장'],
                datasets: [{
                    label: '월간 게시글 분석',
                    data: [1234, 123], // [정상게시글수, 혐오조장게시글수]
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        this._chartSet.commentMonthlyChart = new Chart(document.getElementById('commentMonthlyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '악플', '혐오'],
                datasets: [{
                    label: '월간 게시글 분석',
                    data: [12345, 1234, 123], // [정상댓글수, 악플댓글수, 혐오댓글수]
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        this._chartSet.lineMonthlyChart = new Chart(document.getElementById('lineMonthlyChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: ["1일", "2일", "3일", "4일", "5일", "6일", "7일", "8일", "9일", "10일",
                        "11일", "12일", "13일", "14일", "15일", "16일", "17일", "18일", "19일", "20일",
                        "21일", "22일", "23일", "24일", "25일", "26일", "27일", "28일", "29일", "30일", "31일"],
                datasets: [{
                    label: '전월 혐오조장글 수',
                    data: [125, 201, 232, 220, 120, 94], // 전월 일별 혐오조장글 수 배열
                    fill: true,
                    borderColor: 'rgb(211, 211, 211)',
                    tension: 0.05
                    }, {
                    label: '금월 혐오조장글 수',
                    data: [153, 195, 200], // 금월 일별 혐오조장글 수 배열
                    fill: true,
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.05
                    }
                ]
            }
          });
    },
    modifyChartData: function(chartName, dataArr, idx=0){ // (바꿀차트명, 바꿀데이터배열, 대상라벨번째수)
        this._chartSet[chartName].data.datasets[idx].data = dataArr;
        this._chartSet[chartName].update();
    }
}

const CalcObj = {
    _year: 22, // 테스트용, 실제로는 new Date().getFullYear() % 100
    _month: 10, // 테스트용, 실제로는 new Date().getMonth() + 1
    _date: 20, // 테스트용, 실제로는 new Date().getDate()
    _getDateQuery: function(yy = this._year, mm = this._month, dd = this._date) {
        return "?yy={{year}}&mm={{month}}&dd={{date}}".replace("{{year}}", yy).replace("{{month}}", mm).replace("{{date}}", dd);
    },
    _getYesterdayQuery: function() {
        const targetDay = new Date(2000 + this._year, this._month - 1, this._date - 1); // 생성자의 월 자리에 1을 빼주어야 함
        const yy = targetDay.getFullYear() % 100;
        const mm = targetDay.getMonth() + 1;
        const dd = targetDay.getDate();
        return this._getDateQuery(yy, mm, dd)
    },
    _getLastMonthQuery: function() {
        const targetDay = new Date(2000 + this._year, this._month - 2, this._date); // 생성자의 월 자리에 1을 빼주어야 함
        const yy = targetDay.getFullYear() % 100;
        const mm = targetDay.getMonth() + 1;
        const dd = targetDay.getDate();
        return this._getDateQuery(yy, mm, dd)
    },

    loadData: function() {
        // 일간 조회

        // 오늘 날짜에 대한 댓글 통계 조회
        var httpRequest = new XMLHttpRequest();
		httpRequest.addEventListener("load", () => {
			const result = JSON.parse(httpRequest.responseText);
            // 일간 댓글 통계 그래프
            ShowObj.modifyChartData("commentDailyChart", [result.cleanComment, result.curseComment, result.hateComment]);
		});
		httpRequest.open("GET", "/graphdata/everytime/dailycomment" + this._getDateQuery());
		httpRequest.send();

        // 오늘 날짜에 대한 글 통계 조회
        var httpRequest2 = new XMLHttpRequest();
		httpRequest2.addEventListener("load", () => {
			const result = JSON.parse(httpRequest2.responseText);
            // 일간 게시글 통계 그래프
            ShowObj.modifyChartData("postDailyChart", [result.cleanPost, result.hatePost]);
		});
		httpRequest2.open("GET", "/graphdata/everytime/dailypost" + this._getDateQuery());
		httpRequest2.send();

        // 오늘 날짜에 대한 시간별 글 통계 조회
        var httpRequest3 = new XMLHttpRequest();
		httpRequest3.addEventListener("load", () => {
			const result = JSON.parse(httpRequest3.responseText);
            // 일간 시간별 글 통계 그래프
            ShowObj.modifyChartData('lineDailyChart', result.hatePost, 1);
		});
		httpRequest3.open("GET", "/graphdata/everytime/dailyhourlystat" + this._getDateQuery());
		httpRequest3.send();

        // 어제 날짜에 대한 시간별 글 통계 조회
        var httpRequest4 = new XMLHttpRequest();
		httpRequest4.addEventListener("load", () => {
			const result = JSON.parse(httpRequest4.responseText);
            // 일간 시간별 글 통계 그래프
            ShowObj.modifyChartData('lineDailyChart', result.hatePost, 0);
		});
		httpRequest4.open("GET", "/graphdata/everytime/dailyhourlystat" + this._getYesterdayQuery());
		httpRequest4.send();

        // 월간 조회

        // 이번달 날짜에 대한 댓글 통계 조회
        var httpRequest5 = new XMLHttpRequest();
		httpRequest5.addEventListener("load", () => {
			const result = JSON.parse(httpRequest5.responseText);
            // 월간 댓글 통계 그래프
            ShowObj.modifyChartData("commentMonthlyChart", [result.cleanComment, result.curseComment, result.hateComment]);
		});
		httpRequest5.open("GET", "/graphdata/everytime/monthlycomment" + this._getDateQuery());
		httpRequest5.send();

        // 이번달 날짜에 대한 글 통계 조회
        var httpRequest6 = new XMLHttpRequest();
		httpRequest6.addEventListener("load", () => {
			const result = JSON.parse(httpRequest6.responseText);
            // 월간 게시글 통계 그래프
            ShowObj.modifyChartData("postMonthlyChart", [result.cleanPost, result.hatePost]);
		});
		httpRequest6.open("GET", "/graphdata/everytime/monthlypost" + this._getDateQuery());
		httpRequest6.send();

        // 이번달 날짜에 대한 시간별 글 통계 조회
        var httpRequest7 = new XMLHttpRequest();
		httpRequest7.addEventListener("load", () => {
			const result = JSON.parse(httpRequest7.responseText);
            // 월간 날짜별 글 통계 그래프
            ShowObj.modifyChartData('lineMonthlyChart', result.hatePost, 1);
		});
		httpRequest7.open("GET", "/graphdata/everytime/monthlydailystat" + this._getDateQuery());
		httpRequest7.send();

        // 저번달 날짜에 대한 시간별 글 통계 조회
        var httpRequest8 = new XMLHttpRequest();
		httpRequest8.addEventListener("load", () => {
			const result = JSON.parse(httpRequest8.responseText);
            // 월간 날짜별 글 통계 그래프
            ShowObj.modifyChartData('lineMonthlyChart', result.hatePost, 0);
		});
		httpRequest8.open("GET", "/graphdata/everytime/monthlydailystat" + this._getLastMonthQuery());
		httpRequest8.send();
    }
}

const EventObj = {
    showAndLoadData: function () {
        ShowObj.displayChart();
        CalcObj.loadData();
    },
    setEventListeners: function() {
        document.getElementById("dailyButton").addEventListener("click", () => {
            document.getElementById("dailyAnalysis").classList.remove("d-none");
            document.getElementById("monthlyAnalysis").classList.add("d-none");
        });
        document.getElementById("monthlyButton").addEventListener("click", () => {
            document.getElementById("monthlyAnalysis").classList.remove("d-none");
            document.getElementById("dailyAnalysis").classList.add("d-none");
        });
    }
}

function initConfig() {
    EventObj.showAndLoadData();
    EventObj.setEventListeners();
}

document.addEventListener("DOMContentLoaded", () => {
    initConfig();
});