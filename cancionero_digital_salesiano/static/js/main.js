console.log("📦 main.js cargado correctamente");

document.addEventListener('DOMContentLoaded', function () {

    // === Elementos del DOM ===
    const searchInput = document.getElementById('search-input');
    const searchForm = document.getElementById('search-form');
    const songListContainer = document.getElementById('song-list');
    const searchTitle = document.getElementById('search-title');
    const defaultTitle = searchTitle ? searchTitle.dataset.defaultTitle : '';

    const btnUp = document.getElementById('btn-up');
    const btnDown = document.getElementById('btn-down');
    const letraDiv = document.querySelector('.letra-movil');

    // === 🔍 FUNCIONALIDAD DE BÚSQUEDA EN VIVO ===
    if (searchForm && searchInput && songListContainer) {

        // Evita que el formulario recargue la página al hacer submit
        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
        });

        // Al escribir en el input, hacer una búsqueda AJAX si hay 3+ caracteres o está vacío
        searchInput.addEventListener('input', function () {
            const query = this.value.trim();

            if (query.length >= 3 || query.length === 0) {
                fetch(`/search/?q=${encodeURIComponent(query)}`, {
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    songListContainer.innerHTML = data.html;

                    // Cambiar el título dinámicamente según la búsqueda
                    if (searchTitle) {
                        searchTitle.textContent = (query.length >= 3)
                            ? `Buscando: ${query}`
                            : defaultTitle;
                    }

                    // Si cambia el listado de canciones, puede que haya que reactivar otras funciones JS
                })
                .catch(err => console.error("Error en búsqueda AJAX:", err));
            }
        });
    }

    // === 🎵 FUNCIONALIDAD DE TRANSPOSICIÓN DE ACORDES ===
    if (btnUp && btnDown && letraDiv) {
        let transpose = 0;

        function updateSongTone() {
            const url = new URL(window.location.href);
            url.searchParams.set('transpose', transpose);  // Actualiza el parámetro en la URL

            fetch(url, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                letraDiv.innerHTML = data.html;  // Reemplaza el HTML con los acordes transpuestos
            })
            .catch(err => console.error("Error al transponer:", err));
        }

        // Botón para subir tono
        btnUp.addEventListener('click', () => {
            transpose += 1;
            updateSongTone();
        });

        // Botón para bajar tono
        btnDown.addEventListener('click', () => {
            transpose -= 1;
            updateSongTone();
        });
    }

});
