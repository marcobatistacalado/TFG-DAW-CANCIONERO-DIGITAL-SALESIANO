
//Metodo para buscar
console.log("Hola desde el main.js")
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');  // El input de búsqueda
    const songListContainer = document.getElementById('song-list');  // El contenedor de las canciones

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
            .then(data => {
                // Aquí actualizamos solo el contenido de #song-list con el nuevo HTML
                songListContainer.innerHTML = data.html;
            });
        }
    });
    
});


//