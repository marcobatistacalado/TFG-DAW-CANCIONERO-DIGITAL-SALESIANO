
//Metodo para buscar
console.log("Hola desde el main.js")
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');  // El input de búsqueda
    const songListContainer = document.getElementById('song-list');  // El contenedor de las canciones
    const searchForm = document.getElementById('search-form');

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault(); // ✅ Esto evita que el formulario haga submit y recargue la página
    });

    searchInput.addEventListener('input', function() {
        const query = this.value;

        // Solo realiza la búsqueda si hay 3 o más caracteres, o si el campo está vacío
        if (query.length >= 3 || query.length === 0) {
            fetch(`/search/?q=${encodeURIComponent(query)}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'  // Indicamos que es una solicitud AJAX
                }
            })
            .then(response => response.json())
            .then(data => { //esto es lo que he añadido para que cambie el titulo de timepo liturgico a busqueda actual:...
                songListContainer.innerHTML = data.html;
            
                const titleElement = document.getElementById('search-title');
                const defaultTitle = titleElement.dataset.defaultTitle;
            
                if (query.length >= 3) {
                    titleElement.textContent = `Buscando: ${query}`;
                } else {
                    titleElement.textContent = defaultTitle;
                }
            });
            
            
            
        }
    });
    
});


//