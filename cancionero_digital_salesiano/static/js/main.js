console.log("📦 main.js cargado correctamente");

document.addEventListener("DOMContentLoaded", function () {
    // ============================
    // 🎯 ELEMENTOS DEL DOM
    // ============================
    // Capturamos los elementos del DOM que vamos a usar
    const searchInput = document.getElementById("search-input");
    const searchForm = document.getElementById("search-form");
    const songListContainer = document.getElementById("song-list");
    const searchTitle = document.getElementById("search-title");
    const defaultTitle = searchTitle ? searchTitle.dataset.defaultTitle : "";

    const btnUp = document.getElementById("btn-up"); // Botón subir tono
    const btnDown = document.getElementById("btn-down"); // Botón bajar tono
    const letraDiv = document.querySelector(".letra-movil"); // Contenedor de la letra

    const aumentarBtn = document.getElementById("btn-zoom-in"); // Botón para aumentar zoom
    const reducirBtn = document.getElementById("btn-zoom-out"); // Botón para reducir zoom
    const letraContenedor = document.querySelector(".letra-movil"); // Contenedor que tendrá el tamaño de letra modificado

    const soloLetraBtn = document.getElementById("btn-solo-letra"); // Botón para mostrar solo letra sin acordes
    console.log("Botón soloLetraBtn:", soloLetraBtn);

    // ============================
    // 🔍 BÚSQUEDA EN VIVO (AJAX)
    // ============================
    // Cuando hay un formulario y un input, activamos búsqueda en vivo
    if (searchForm && searchInput && songListContainer) {
        // Evita que el formulario se envíe tradicionalmente (recarga)
        searchForm.addEventListener("submit", function (e) {
            e.preventDefault();
        });

        // Escuchamos cuando el usuario escribe en el input de búsqueda
        searchInput.addEventListener("input", function () {
            const query = this.value.trim();

            // Solo buscar si el texto tiene 3+ caracteres o si está vacío (para resetear)
            if (query.length >= 3 || query.length === 0) {
                // Petición AJAX para buscar canciones en backend
                fetch(`/search/?q=${encodeURIComponent(query)}`, {
                    headers: {
                        "X-Requested-With": "XMLHttpRequest",
                    },
                })
                    .then((response) => response.json())
                    .then((data) => {
                        // Actualizamos el listado de canciones con la respuesta HTML recibida
                        songListContainer.innerHTML = data.html;

                        // Cambiamos el título para reflejar que se está buscando
                        if (searchTitle) {
                            searchTitle.textContent =
                                query.length >= 3 ? `Buscando: ${query}` : defaultTitle;
                        }
                    })
                    .catch((err) => console.error("Error en búsqueda AJAX:", err));
            }
        });
    }

    // ============================
    // 🎵 TRANSPOSICIÓN DE ACORDES
    // ============================
    // Permite subir o bajar el tono de la canción
    if (btnUp && btnDown && letraDiv) {
        let transpose = 0; // Valor actual de transposición

        // Función para pedir al backend la letra transpuesta según valor actual
        function updateSongTone() {
            const url = new URL(window.location.href);
            url.searchParams.set("transpose", transpose); // Actualizamos parámetro transpose en URL

            fetch(url, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest",
                },
            })
                .then((response) => response.json())
                .then((data) => {
                    // Reemplazamos el HTML de la letra con la versión transpuesta
                    letraDiv.innerHTML = data.html;
                })
                .catch((err) => console.error("Error al transponer:", err));
        }

        // Al hacer clic en subir tono, aumentamos la transposición y actualizamos la letra
        btnUp.addEventListener("click", () => {
            transpose += 1;
            updateSongTone();
        });

        // Al hacer clic en bajar tono, disminuimos la transposición y actualizamos la letra
        btnDown.addEventListener("click", () => {
            transpose -= 1;
            updateSongTone();
        });
    }

    // ============================
    // 🔍 ZOOM DE LETRA
    // ============================
    // Controlamos el tamaño de fuente de la letra para aumentar o reducir zoom
    const maxFontSize = 30; // Tamaño máximo permitido
    const minFontSize = 10; // Tamaño mínimo permitido
    let fontSize = localStorage.getItem("fontSize"); // Intentamos recuperar tamaño guardado
    fontSize = fontSize ? parseInt(fontSize) : 16; // Si no hay, tamaño por defecto 16px
    letraContenedor.style.fontSize = fontSize + "px";

    // Función para habilitar o deshabilitar botones según el tamaño actual
    function actualizarBotones() {
        if (fontSize >= maxFontSize) {
            aumentarBtn.setAttribute("disabled", "true");
        } else {
            aumentarBtn.removeAttribute("disabled");
        }

        if (fontSize <= minFontSize) {
            reducirBtn.setAttribute("disabled", "true");
        } else {
            reducirBtn.removeAttribute("disabled");
        }
    }
    actualizarBotones();

    // Evento para aumentar tamaño de letra y guardar preferencia
    aumentarBtn.addEventListener("click", function () {
        if (fontSize < maxFontSize) {
            fontSize += 2;
            letraContenedor.style.fontSize = fontSize + "px";
            localStorage.setItem("fontSize", fontSize);
            actualizarBotones();
        }
    });

    // Evento para reducir tamaño de letra y guardar preferencia
    reducirBtn.addEventListener("click", function () {
        if (fontSize > minFontSize) {
            fontSize -= 2;
            letraContenedor.style.fontSize = fontSize + "px";
            localStorage.setItem("fontSize", fontSize);
            actualizarBotones();
        }
    });

    // ============================
    // 🎸 BOTÓN SOLO LETRA (TOGGLE ACORDES)
    // ============================
    // Permite ocultar o mostrar los acordes de la canción
    let acordesVisibles = true; // Estado inicial: acordes visibles

    if (soloLetraBtn) {
        soloLetraBtn.addEventListener("click", function () {
            acordesVisibles = !acordesVisibles; // Cambiar estado
            console.log("Estado de acordes visibles:", acordesVisibles);

            // Mostrar u ocultar elementos con clase .acordes según estado
            document.querySelectorAll(".acordes").forEach((el) => {
                el.style.display = acordesVisibles ? "block" : "none";
            });

            // Cambiar texto e icono del botón según el estado
            soloLetraBtn.innerHTML = acordesVisibles
                ? `<i class="svg bi bi-file-earmark-font icono"></i><span>Solo letra</span>`
                : `<i class="svg bi bi-plus-circle"></i> <span>Añadir acordes</span>`;
        });
    }

    // ============================
    // 🚀 AUTO SCROLL DE LETRA
    // ============================
    // Permite hacer scroll automático en la letra a una velocidad ajustable
    const scrollBtn = document.getElementById("btn-scroll");
    let scrollInterval = null;
    let isScrolling = false;
    let velocidad = 1; // Velocidad inicial del scroll
    const velocidadDisplay = document.getElementById("velocidad-actual");

    // Botones para aumentar o disminuir la velocidad de scroll
    const plusBtn = document.getElementById("btn-pls-speed");
    const minusBtn = document.getElementById("btn-mn-speed");

    // Aumentar velocidad si no se pasa del máximo (10)
    if (plusBtn) {
        plusBtn.addEventListener("click", () => {
            if (velocidad < 10) {
                velocidad++;
                actualizarVelocidadDisplay();
                console.log("Velocidad aumentada a:", velocidad);
            }
        });
    }

    // Disminuir velocidad si no se pasa del mínimo (1)
    if (minusBtn) {
        minusBtn.addEventListener("click", () => {
            if (velocidad > 1) {
                velocidad--;
                actualizarVelocidadDisplay();
                console.log("Velocidad disminuida a:", velocidad);
            }
        });
    }

    // Actualiza el texto que muestra la velocidad actual
    function actualizarVelocidadDisplay() {
        if (velocidadDisplay) {
            velocidadDisplay.textContent = velocidad;
        }
    }

    // Lógica para iniciar/detener el scroll automático al pulsar el botón
    if (scrollBtn && letraContenedor) {
        scrollBtn.addEventListener("click", () => {
            if (!isScrolling) {
                scrollBtn.innerHTML = `<i class="bi bi-pause-circle"></i> Detener scroll`;
                isScrolling = true;

                scrollInterval = setInterval(() => {
                    // Scroll suave hacia abajo
                    letraContenedor.scrollBy({
                        top: velocidad,
                        behavior: "smooth",
                    });

                    // Si llegamos al final del contenido, paramos el scroll automático
                    if (
                        letraContenedor.scrollTop + letraContenedor.clientHeight >=
                        letraContenedor.scrollHeight
                    ) {
                        clearInterval(scrollInterval);
                        isScrolling = false;
                        scrollBtn.innerHTML = `<i class="svg bi bi-file-earmark-font icono"></i><span>scroll</span>`;
                    }
                }, 50); // Intervalo de tiempo entre cada desplazamiento (ms)
            } else {
                // Si ya está en scroll, detenerlo al pulsar el botón
                clearInterval(scrollInterval);
                isScrolling = false;
                scrollBtn.innerHTML = `<i class=" svg bi bi-file-earmark-font icono"></i><span>scroll</span>`;
            }
        });
    }


    //Boton de añadir o quitar de favoritos
    const btnFavorito = document.getElementById('btn-favorito');

    if (btnFavorito) {
        btnFavorito.addEventListener('click', function () {
            const cancionId = this.dataset.cancionId;
            fetch(window.toggleFavoritoUrl, {  // usa la variable global definida en el template
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': window.csrfToken  // token también desde la variable global
                },
                body: new URLSearchParams({
                    'cancion_id': cancionId
                })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'agregado') {
                        btnFavorito.innerHTML = '<i class="bi bi-heart-fill"></i> Quitar de Favoritos';
                    } else if (data.status === 'eliminado') {
                        btnFavorito.innerHTML = '<i class="bi bi-heart"></i> Añadir a Favoritos';
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }


    // Abrir modal de quitar
    const btnRemoveList = document.getElementById('btn-remove-list');
    console.log("Botón de quitar lista:", btnRemoveList);
    const btnAddList = document.getElementById('btn-add-list');
    if (btnAddList) {
        btnAddList.addEventListener('click', function () {
            const modal = new bootstrap.Modal(document.getElementById('modalListas'));
            console.log("Modal de agregar listas abierto", modal);
            modal.show();
        });
    }

    if (btnRemoveList) {
        btnRemoveList.addEventListener('click', function () {
            console.log("Botón de quitar lista presionado");
            const modal = new bootstrap.Modal(document.getElementById('modalQuitarLista'));
            console.log("Modal de quitar listas abierto", modal);
            modal.show();
        });
    }

    // Enviar formulario de quitar
    const formQuitar = document.getElementById('form-quitar-lista');
    if (formQuitar) {
        formQuitar.addEventListener('submit', function (e) {
            e.preventDefault();

            const formData = new FormData(formQuitar);

            fetch(window.toggleListoUrl, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': window.csrfToken
                },
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    // Usa el ID correcto del modal
                    const modal = bootstrap.Modal.getInstance(document.getElementById('modalQuitar'));
                    modal.hide();

                    if (data.status === 'eliminado') {
                        alert('Canción eliminada de la lista.');
                        location.reload();  // Para actualizar el estado
                    } else {
                        alert('Error al quitar la canción.');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }

});
