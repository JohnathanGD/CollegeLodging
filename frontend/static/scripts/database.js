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
            if (!response.ok) { throw new Error("Network response was not ok"); }
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

            const submitButton = document.querySelector(".submit-button");
            submitButton.disabled = true;

            const newSubmitButton = submitButton.cloneNode(true);
            submitButton.parentNode.replaceChild(newSubmitButton, submitButton);


            newSubmitButton.addEventListener("click", function () {
                updateUser(id);
            });
        })
        .catch(error => {
            console.error("Error fetching user data:", error);
            showToast("error", "An error occurred while fetching user data.");
        });
};


if (document.getElementById("edit-user-form")) {
    document.getElementById("edit-user-form").addEventListener("input", function (event) {
        document.querySelector(".submit-button").disabled = false;
        event.preventDefault();
    });

    document.getElementById("edit-user-form").addEventListener("input", function () {
        document.querySelector(".submit-button").disabled = false;
    });
}

const updateUser = (id) => {
    const url = `/admin/update_user/${id}`;

    const formData = new FormData(document.getElementById("edit-user-form"));

    const updatedData = {
        id: formData.get("user-id"),
        firstname: formData.get("first-name"),
        lastname: formData.get("last-name"),
        email: formData.get("email"),
        roles: formData.get("roles"),
    };

    console.log("Updating user:", updatedData);

    fetch(url, {
        method: 'PUT',
        body: JSON.stringify(updatedData),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => { return response.json(); })
    .then(data => {
        if (data.error) { throw new Error(data.message); }
        console.log("User updated successfully:", data);
        hideAllModalContent();
        showToast("success", "User updated successfully.");

        const userRow = document.getElementById(`user-row-${id}`);
        if (userRow) {
            userRow.querySelector(".user-firstname").textContent = updatedData.firstname;
            userRow.querySelector(".user-lastname").textContent = updatedData.lastname;
            userRow.querySelector(".user-email").textContent = updatedData.email;
        } else {
            console.error("Failed to update user:", data.message);
        }
    })
    .catch(error => {
        console.error("Error updating user:", error);
        showToast("error", "An error occurred while updating the user.");
    });
}

const deleteUser = (id) => {
    const url = `/admin/delete_user/${id}`;

    fetch(url, {
        method: 'DELETE',
    })
    .then(response => {
        if (!response.ok) { throw new Error("Network response was not ok"); }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            console.log("User deleted successfully:", id);
            const userRow = document.getElementById(`user-row-${id}`);
            if (userRow) {
                userRow.remove();
            }
        } else {
            console.error("Failed to delete user:", data.message);
        }

        fetchFlashMessages();
    })
    .catch(error => {
        console.error("Error deleting user:", error);
        showToast("error", "An error occurred while deleting the user.");
    });
};

function fetchFlashMessages() {
    fetch(`get_flash_messages`, { 
        method: 'GET', 
    })
    .then(response => {
        if (response.status === 404) { return; }
        if (!response.ok) { throw new Error("Network response was not ok"); }
        return response.json();
    })
    .then(data => {
        data.messages.forEach(([category, message]) => {
            showToast(category, message);
        });
    })
    .catch(error => {
        console.error("Error fetching flash messages:", error);
        showToast("error", "An error occurred while fetching flash messages.");
    });
}


document.querySelectorAll('.delete-button').forEach(button => {
    button.addEventListener('click', function() {
        const id = button.getAttribute('data-user-id');
        console.log(`Deleting user with ID: ${id}`);
        deleteUser(id);
    });
});

document.querySelector('.delete-button').addEventListener('click', (event) => {
    event.preventDefault();
    deleteUser(event.target.dataset.userId);
});

const openEditListingModal = (id) => { 
    const url = `get_property/${id}`;
    console.log("Is it on");

    fetch(url)
        .then(response => {
            if (!response.ok) { throw new Error("Network response was not ok"); }
            return response.json();
        })
        .then(data => {
            // Populate the form fields with the retrieved property data
            document.getElementById("title").value = data.title;
            document.getElementById("description").value = data.description;
            document.getElementById("street_address").value = data.street_address;
            document.getElementById("city").value = data.city;
            document.getElementById("state").value = data.state;
            document.getElementById("postal_code").value = data.postal_code;
            document.getElementById("country").value = data.country;
            document.getElementById("price").value = data.price;
            document.getElementById("bedroom_count").value = data.bedroom_count;
            document.getElementById("bathroom_count").value = data.bathroom_count;
            document.getElementById("type").value = data.type;
            document.querySelector("input[name='furnished']").checked = data.furnished;
            document.querySelector("input[name='pets_allowed']").checked = data.pets_allowed;
            document.querySelector("input[name='utilities_included']").checked = data.utilities_included;

            // Show the modal content
            showModalContent(".modal-edit-content");

            // Enable form submission after cloning the submit button
            const submitButton = document.querySelector(".submit-button");
            submitButton.disabled = true;

            const newSubmitButton = submitButton.cloneNode(true);
            submitButton.parentNode.replaceChild(newSubmitButton, submitButton);

            // Add event listener for the new button
            newSubmitButton.addEventListener("click", function () {
                updateProperty(id);
            });
        })
        .catch(error => {
            console.error("Error fetching property data:", error);
            showToast("error", "An error occurred while fetching property data.");
        });
};

if (document.getElementById("edit-listing-form")) {
    document.getElementById("edit-listing-form").addEventListener("input", function (event) {
        document.querySelector(".submit-button").disabled = false;
        event.preventDefault();
    });

    document.getElementById("edit-listing-form").addEventListener("submit", function (event) {
        event.preventDefault();
    });
}

const updateProperty = (id) => {
    const url = `/admin/update_property/${id}`;

    const formData = new FormData(document.getElementById("edit-listing-form"));

    const updatedData = {
        title: formData.get("title"),
        description: formData.get("description"),
        street_address: formData.get("street_address"),
        city: formData.get("city"),
        state: formData.get("state"),
        postal_code: formData.get("postal_code"),
        country: formData.get("country"),
        price: parseFloat(formData.get("price")),
        bedroom_count: parseInt(formData.get("bedroom_count")),
        bathroom_count: parseInt(formData.get("bathroom_count")),
        type: formData.get("type"),
        furnished: formData.get("furnished") === "on",
        pets_allowed: formData.get("pets_allowed") === "on",
        utilities_included: formData.get("utilities_included") === "on",
    };

    console.log("Updating property:", updatedData);

    fetch(url, {
        method: 'PUT',
        body: JSON.stringify(updatedData),
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => { return response.json(); })
    .then(data => {
        if (data.error) { throw new Error(data.message); }
        console.log("Property updated successfully:", data);
        hideAllModalContent();
        showToast("success", "Property updated successfully.");

        // Update the listing UI dynamically
        const propertyRow = document.getElementById(`property-row-${id}`);
        if (propertyRow) {
            propertyRow.querySelector(".property-title").textContent = updatedData.title;
            propertyRow.querySelector(".property-price").textContent = `$${updatedData.price}`;
            propertyRow.querySelector(".property-address").textContent = updatedData.street_address;
        } else {
            console.error("Failed to update property:", data.message);
        }
    })
    .catch(error => {
        console.error("Error updating property:", error);
        showToast("error", "An error occurred while updating the property.");
    });
};