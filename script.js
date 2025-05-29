// Lưu trạng thái trước khi reload
window.addEventListener('beforeunload', function () {
    const formData = {
        home: {
            timeRange: document.querySelector('select')?.value || '', // Lấy giá trị từ select trong home.html
            temperature: document.querySelector('#temperature')?.innerText || '--',
            humidity: document.querySelector('#humidity')?.innerText || '--',
            soilMoisture: document.querySelector('#soilMoisture')?.innerText || '--',
            nh3: document.querySelector('#nh3')?.innerText || '--',
            rainfall: document.querySelector('#rainfall')?.innerText || '--'
        },
        dataAnalist: {
            fromDate: document.querySelector('#fromDate')?.value || '',
            toDate: document.querySelector('#toDate')?.value || '',
            tableData: getTableData() // Lấy dữ liệu từ bảng lịch sử
        }
    };

    try {
        localStorage.setItem('appState', JSON.stringify(formData));
    } catch (e) {
        console.error('Lỗi khi lưu trạng thái:', e);
    }
});

// Lấy dữ liệu từ bảng lịch sử
function getTableData() {
    const rows = document.querySelectorAll('#dataTable tr');
    const data = [];
    rows.forEach(row => {
        const cells = row.querySelectorAll('td');
        if (cells.length >= 7) {
            data.push({
                stt: cells[0].innerText,
                time: cells[1].innerText,
                temperature: cells[2].innerText,
                humidity: cells[3].innerText,
                rainfall: cells[4].innerText,
                nh3: cells[5].innerText,
                soilMoisture: cells[6].innerText
            });
        }
    });
    return data.slice(0, 1000); // Giới hạn 1000 bản ghi để tránh vượt dung lượng localStorage
}

// Khôi phục trạng thái sau khi tải trang
window.addEventListener('load', function () {
    try {
        const savedState = localStorage.getItem('appState');
        if (savedState) {
            const formData = JSON.parse(savedState);

            // Khôi phục cho home.html
            if (document.querySelector('select')) {
                document.querySelector('select').value = formData.home.timeRange;
                document.querySelector('#temperature').innerText = formData.home.temperature;
                document.querySelector('#humidity').innerText = formData.home.humidity;
                document.querySelector('#soilMoisture').innerText = formData.home.soilMoisture;
                document.querySelector('#nh3').innerText = formData.home.nh3;
                document.querySelector('#rainfall').innerText = formData.home.rainfall;
            }

            // Khôi phục cho dataanalist.html
            if (document.querySelector('#fromDate')) {
                document.querySelector('#fromDate').value = formData.dataAnalist.fromDate;
                document.querySelector('#toDate').value = formData.dataAnalist.toDate;
                restoreTableData(formData.dataAnalist.tableData);
            }
        }
    } catch (e) {
        console.error('Lỗi khi khôi phục trạng thái:', e);
    }
});

// Khôi phục dữ liệu bảng lịch sử
function restoreTableData(tableData) {
    const tableBody = document.querySelector('#dataTable tbody');
    if (tableBody && tableData && tableData.length > 0) {
        tableBody.innerHTML = ''; // Xóa bảng hiện tại
        tableData.forEach(row => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${row.stt}</td>
                <td>${row.time}</td>
                <td>${row.temperature}</td>
                <td>${row.humidity}</td>
                <td>${row.rainfall}</td>
                <td>${row.nh3}</td>
                <td>${row.soilMoisture}</td>
            `;
            tableBody.appendChild(tr);
        });
    }
}

// Xóa trạng thái khi đăng xuất
function logout() {
    localStorage.removeItem('appState');
    window.location.href = 'index.html';
}