// Chart.js 그래프 초기화
const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // x축 레이블
        datasets: [{
            label: '온도',
            data: [], // 온도 데이터
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgba(255, 99, 132, 1)',
            borderWidth: 1
        }, {
            label: '습도',
            data: [], // 습도 데이터
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// 데이터 가져오기 및 차트와 테이블 업데이트
function fetchDataAndUpdate() {
    fetch('/ys2_data')
    .then(response => response.json())
    .then(data => {
        const labels = data.map(item => new Date(item.timestamp).toLocaleString());
        const temperatures = data.map(item => item.temperature);
        const humidities = data.map(item => item.humidity);

        // 차트 업데이트
        updateChart(myChart, labels, temperatures, humidities);

        // 테이블 업데이트
        updateTable(labels, temperatures, humidities);
    })
    .catch(error => console.error('Error fetching data:', error));
}

// 차트 업데이트
function updateChart(chart, labels, temperatures, humidities) {
    chart.data.labels = labels;
    chart.data.datasets[0].data = temperatures;
    chart.data.datasets[1].data = humidities;
    chart.update();
}

// 테이블 업데이트
function updateTable(labels, temperatures, humidities) {
    const tbody = document.getElementById('sensor-data-table').getElementsByTagName('tbody')[0];
    tbody.innerHTML = ''; // 기존 테이블 내용 초기화

    // 데이터를 테이블에 추가
    for (let i = 0; i < labels.length; i++) {
        const row = tbody.insertRow();
        const cellTime = row.insertCell(0);
        const cellTemperature = row.insertCell(1);
        const cellHumidity = row.insertCell(2);

        cellTime.textContent = labels[i];
        cellTemperature.textContent = temperatures[i] + '°C';
        cellHumidity.textContent = humidities[i] + '%';
    }
}

// 주기적으로 데이터 업데이트
setInterval(fetchDataAndUpdate, 10000); // 10초마다 업데이트

// 페이지 로드 시 데이터 즉시 가져오기
fetchDataAndUpdate();

