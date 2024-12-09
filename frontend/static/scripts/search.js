let baseUrl = '/university/api/v1';
let debounceTimer;

function titleCase(s) {
    return s.toLowerCase().replace(/(^|\s|-)\S/g, (match) => match.toUpperCase());
}

function redirectToSearchPage(state='fl', city='Tallahassee', university='florida-state-university') {
    window.location.href = `apartment-search/${state}/${city}/${university}`;
}

document.addEventListener('DOMContentLoaded', () => {
    const searchBar = document.getElementById('search-bar');
    const suggestions = document.getElementById('suggestions');

    searchBar.addEventListener('input', () => {
        const query = searchBar.value.trim().toLowerCase();
        suggestions.innerHTML = '';

        if (query) {
            // Clear previous timer
            clearTimeout(debounceTimer);

            // Set a new timer
            debounceTimer = setTimeout(() => {
                fetch(`${baseUrl}/autocomplete/query=${encodeURIComponent(query)}`)
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data && data.length > 0) {
                            suggestions.style.display = 'block';
                            data.forEach(university => {
                                const suggestionItem = document.createElement('div');
                                suggestionItem.textContent = titleCase(university.name);
                                suggestionItem.addEventListener('click', () => {
                                    searchBar.value = titleCase(university.name);
                                    suggestions.innerHTML = '';
                                    suggestions.style.display = 'none';
                                    
                                    redirectToSearchPage(university.state, university.city, university.name);
                                });
                                suggestions.appendChild(suggestionItem);
                            });
                        } else {
                            suggestions.style.display = 'none';
                        }
                    })
                    .catch(error => {
                        console.error('Error fetching universities:', error);
                        suggestions.style.display = 'none';
                    });
            }, 300); // 300ms debounce delay
        } else {
            suggestions.style.display = 'none';
        }
    });

    document.addEventListener('click', (event) => {
        if (!searchBar.contains(event.target) && !suggestions.contains(event.target)) {
            suggestions.innerHTML = '';
            suggestions.style.display = 'none';
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && searchBar.value.trim()) {
            redirectToSearchPage();
        }
    });

    document.getElementById('home-search-btn').addEventListener('click', () => {
        if (searchBar.value.trim()) {
            redirectToSearchPage();
        }
    });
});
