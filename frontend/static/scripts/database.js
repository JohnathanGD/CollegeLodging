function toggleSelectAll(source) {
    const checkboxes = document.querySelectorAll('.select-checkbox');
    checkboxes.forEach(checkbox => {
        checkbox.checked = source.checked;
    });
}

function changePage(action) {
    let currentPage = window.currentPage;
    const totalPages = window.totalPages;
    
    if (action === 'next') {
        if (currentPage < totalPages) {
            currentPage += 1;
        }
    } else if (action === 'prev') {
        if (currentPage > 1) {
            currentPage -= 1;
        }
    } else {
        currentPage = action;
    }

    window.location.href = `?page=${currentPage}`;
}

function hideModal() {
    document.querySelector(".bg-modal").style.display = "none";
}

function showModal() {
    document.querySelector(".bg-modal").style.display = "flex";
}

function showModalContent(queryName, button) {
    showModal();
    document.querySelector(queryName).style.display = "block";
    document.querySelector(queryName).style.visibility = "visible";
}

function hideModalContent(queryName) {
    document.querySelector(queryName).style.display = "none";
    document.querySelector(queryName).style.visibility = "hidden";
}

function hideAllModalContent() {
    var modals = [".modal-edit-content"];

    for (var i = 0; i < modals.length; i++) {
        hideModalContent(modals[i]);
    }

    hideModal();
}

const openEditModal = (id) => { 
    const url = `get_user/${id}`;

    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json();
        })
        .then(data => {
            document.getElementById("user-id").value = data.id;
            document.getElementById("first-name").value = data.firstname;
            document.getElementById("last-name").value = data.lastname;
            document.getElementById("email").value = data.email;
            document.getElementById("roles").value = data.roles;
            document.getElementById("created-at").value = data.created_at;

            showModalContent(".modal-edit-content");
            document.querySelector(".submit-button").disabled = true;
        })
        .catch(error => {
            console.error("Error fetching user data:", error);
        });
};

const deleteUser = (id) => {
    const url = `delete_user/${id}`;

    fetch(url, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then(data => {
        console.log(data);
        if (data.success) {
            const userRow = document.getElementById(`user-row-${id}`);
            if (userRow) {
                userRow.remove();
                alert("User deleted successfully");
            } else {
                console.error(`User row with ID user-row-${id} not found`);
            }
        } else {
            alert("Failed to delete user");
        }
    })
    .catch(error => {
        console.error("Error deleting user:", error);
    });
};

document.getElementById("edit-user-form").addEventListener("input", function () {
    document.querySelector(".submit-button").disabled = false;
});