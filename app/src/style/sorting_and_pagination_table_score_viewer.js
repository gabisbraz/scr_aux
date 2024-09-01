document.addEventListener('DOMContentLoaded', function () {
    const rowsPerPage =  str(rows_per_page);
    let currentPage = 1;
    let sortState = 0;
    const maxVisiblePages = 5;

    function renderTable() {
        const rows = Array.from(document.querySelectorAll('#emp-table tbody tr'));
        const start = (currentPage - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        rows.forEach((row, index) => {
            row.style.display = (index >= start && index < end) ? '' : 'none';
        });

        updatePagination();
    }

    function updatePagination() {
        const pagination = document.getElementById('pagination');
        const totalRows = document.querySelectorAll('#emp-table tbody tr').length;
        const totalPages = Math.ceil(totalRows / rowsPerPage);
        let startPage = Math.max(currentPage - Math.floor(maxVisiblePages / 2), 1);
        let endPage = Math.min(startPage + maxVisiblePages - 1, totalPages);

        pagination.innerHTML = '';

        if (totalPages > 1) {
            if (currentPage > 1) {
                const prevButton = document.createElement('button');
                prevButton.textContent = 'Anterior';
                prevButton.addEventListener('click', () => {
                    currentPage--;
                    renderTable();
                });
                pagination.appendChild(prevButton);
            }

            if (startPage > 1) {
                const firstPageButton = document.createElement('button');
                firstPageButton.textContent = '1';
                firstPageButton.addEventListener('click', () => {
                    currentPage = 1;
                    renderTable();
                });
                pagination.appendChild(firstPageButton);

                const leftEllipsis = document.createElement('span');
                leftEllipsis.textContent = '...';
                pagination.appendChild(leftEllipsis);
            }

            for (let i = startPage; i <= endPage; i++) {
                const button = document.createElement('button');
                button.textContent = i;
                if (i === currentPage) {
                    button.classList.add('active');
                }
                button.addEventListener('click', () => {
                    currentPage = i;
                    renderTable();
                });
                pagination.appendChild(button);
            }

            if (endPage < totalPages) {
                const rightEllipsis = document.createElement('span');
                rightEllipsis.textContent = '...';
                pagination.appendChild(rightEllipsis);

                const lastPageButton = document.createElement('button');
                lastPageButton.textContent = totalPages;
                lastPageButton.addEventListener('click', () => {
                    currentPage = totalPages;
                    renderTable();
                });
                pagination.appendChild(lastPageButton);
            }

            if (currentPage < totalPages) {
                const nextButton = document.createElement('button');
                nextButton.textContent = 'Próximo';
                nextButton.addEventListener('click', () => {
                    currentPage++;
                    renderTable();
                });
                pagination.appendChild(nextButton);
            }
        }
    }

    function sortTable(columnClass) {
        const rows = Array.from(document.querySelectorAll('#emp-table tbody tr'));
        const headerCells = Array.from(document.querySelectorAll('#emp-table thead th'));

        if (sortState === 0) {
            rows.sort((a, b) => {
                const idA = parseInt(a.querySelector('td.index').innerText.trim());
                const idB = parseInt(b.querySelector('td.index').innerText.trim());
                return idA - idB;
            });
        } else if (sortState === 1) {
            rows.sort((a, b) => {
                const cellA = a.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
                const cellB = b.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
                const valueA = parseFloat(cellA) || 0;
                const valueB = parseFloat(cellB) || 0;
                return valueA - valueB;
            });
        } else if (sortState === 2) {
            rows.sort((a, b) => {
                const cellA = a.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
                const cellB = b.querySelector(`td[data-column="${columnClass}"]`).innerText.trim();
                const valueA = parseFloat(cellA) || 0;
                const valueB = parseFloat(cellB) || 0;
                return valueB - valueA;
            });
        }

        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = '';
        rows.forEach(row => {
            tableBody.appendChild(row);
        });

        sortState = (sortState + 1) % 3;
        headerCells.forEach((th) => {
            th.classList.remove('th-sort-asc', 'th-sort-desc');
            if (th.dataset.column === columnClass) {
                if (sortState === 2) {
                    th.classList.add('th-sort-asc');
                } else if (sortState === 0) {
                    th.classList.add('th-sort-desc');
                }
            }
        });

        renderTable();
    }

    document.querySelectorAll('th.sortable').forEach(th => {
        th.addEventListener('click', () => {
            sortTable(th.dataset.column);
        });
    });

    renderTable();
});
