function toggleSelectAll(source) {
    const checkboxes = document.querySelectorAll('.select-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = source.checked;
    });
}

function changePage(action) {
    const paginationDiv = document.querySelector('.pagination');
    const currentPage = parseInt(paginationDiv.getAttribute('data-current-page'));
    const totalPages = parseInt(paginationDiv.getAttribute('data-total-pages'));

    let newPage = currentPage;

    if (action === 'next') {
        if (newPage < totalPages) {
            newPage += 1;
        }
    } else if (action === 'prev') {
        if (newPage > 1) {
            newPage -= 1;
        }
    } else {
        newPage = action;
    }

    window.location.href = `?page=${newPage}`;
}
