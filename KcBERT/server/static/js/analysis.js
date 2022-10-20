const ShowObj = {
    _result: null,

    displayDailyChart: function() {
        const postDailyChart = new Chart(document.getElementById('postDailyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '혐오조장'],
                datasets: [{
                    label: '일간 게시글 분석',
                    data: [500, 50],
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        const commentDailyChart = new Chart(document.getElementById('commentDailyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '악플', '혐오'],
                datasets: [{
                    label: '일간 게시글 분석',
                    data: [5000, 300, 200],
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        const lineDailyChart = new Chart(document.getElementById('lineDailyChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: ["0:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00", "9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"].slice(0, 24),
                datasets: [{
                    label: '전일 악성 댓글 수',
                    data: [15, 20, 25, 30, 15, 25, 30, 15, 15, 20, 25, 30, 15, 25, 30, 15, 15, 20, 25, 30, 15, 25, 30, 15],
                    fill: true,
                    borderColor: 'rgb(211, 211, 211)',
                    tension: 0.05
                    }, {
                    label: '금일 악성 댓글 수',
                    data: [10, 25, 40, 50, 30, 15],
                    fill: true,
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.05
                    }
                ]
            }
          });
    },
    displayMonthlyChart: function() {
        const postMonthlyChart = new Chart(document.getElementById('postMonthlyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '혐오조장'],
                datasets: [{
                    label: '월간 게시글 분석',
                    data: [2211, 142],
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        const commentMonthlyChart = new Chart(document.getElementById('commentMonthlyChart').getContext('2d'), {
            type: 'doughnut',
            data: {
                labels: ['정상', '악플', '혐오'],
                datasets: [{
                    label: '월간 게시글 분석',
                    data: [15000, 1300, 800],
                    backgroundColor: ['rgb(54, 162, 235)', 'rgb(255, 205, 86)', 'rgb(255, 99, 132)'],
                    hoverOffset: 4
                }]
            }
        });

        const lineMonthlyChart = new Chart(document.getElementById('lineMonthlyChart').getContext('2d'), {
            type: 'line',
            data: {
                labels: ["1일-5일", "6일-10일", "11일-15일", "16일-20일", "21일-25일", "26일-"].slice(0, 6),
                datasets: [{
                    label: '전월 악성 댓글 수',
                    data: [125, 201, 232, 220, 120, 94],
                    fill: true,
                    borderColor: 'rgb(211, 211, 211)',
                    tension: 0.05
                    }, {
                    label: '금월 악성 댓글 수',
                    data: [153, 195, 200],
                    fill: true,
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.05
                    }
                ]
            }
          });
    }
}

const EventObj = {
    loadData: function () {
        ShowObj.displayDailyChart();
        ShowObj.displayMonthlyChart();
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
    EventObj.loadData();
    EventObj.setEventListeners();
}

document.addEventListener("DOMContentLoaded", () => {
    initConfig();
});