const categoryIcons = {
    success: '<i class="bx bx-check-circle"></i>',
    error: '<i class="bx bx-x-circle"></i>',
    warning: '<i class="bx bx-error"></i>',
    info: '<i class="bx bx-info-circle"></i>',
};

function showToast(category, message) {
    const toastBox = document.getElementById("toastBox");
    if (!toastBox) {
        console.error("Toast container (toastBox) not found in the DOM.");
        return;
    }

    const icon = categoryIcons[category] || "";
    const toast = document.createElement("div");
    toast.classList.add("toast", category);
    toast.innerHTML = `${icon} ${message}`;

    toastBox.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 5000);
}
