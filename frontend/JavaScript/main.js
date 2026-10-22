// URL base del backend
const API_URL = "http://127.0.0.1:8000";

// Detectar qué página está abierta para cargar sus datos
document.addEventListener("DOMContentLoaded", () => {
    if (document.getElementById("resumen-dashboard")) cargarDashboard();
    if (document.getElementById("lista-clientes")) cargarClientes();
    if (document.getElementById("lista-barberos")) cargarBarberos();
    if (document.getElementById("lista-servicios")) cargarServicios();
    if (document.getElementById("lista-citas")) cargarCitas();
});

// 1. CARGAR DASHBOARD 
async function cargarDashboard() {
    const fechaHoy = new Date().toISOString().split('T')[0];
    try {
        const resResumen = await fetch(`${API_URL}/resumen/${fechaHoy}`);
        if (resResumen.ok) {
            const resumen = await resResumen.json();
            document.getElementById("citas-hoy").innerText = resumen.total_citas;
            document.getElementById("ingresos-hoy").innerText = `$${resumen.ingresos_estimados}`;
        }

        const resAgenda = await fetch(`${API_URL}/agenda/${fechaHoy}`);
        if (resAgenda.ok) {
            const agenda = await resAgenda.json();
            const contenedor = document.getElementById("lista-agenda");
            contenedor.innerHTML = "";

            if (agenda.length === 0) {
                contenedor.innerHTML = "<p>No hay citas programadas para hoy.</p>";
                return;
            }

            agenda.forEach(cita => {
                contenedor.innerHTML += `
                <div class="card" style="margin-bottom: 15px; justify-content: space-between;">
                    <div style="display: flex; align-items: center; gap: 15px;">
                        <div class="icon-box" style="background-color: var(--color-fondo-oscuro); color: white; font-weight:bold;">
                            ${cita.hora.substring(0, 5)}
                        </div>
                        <div>
                            <p class="card-title">Cliente</p>
                            <h3>${cita.cliente}</h3>
                        </div>
                    </div>
                    <div><p class="card-title">Servicio</p><span>${cita.servicio}</span></div>
                    <div><p class="card-title">Barbero</p><span>${cita.barbero}</span></div>
                    <div><p class="card-title">Costo</p><span>$${cita.precio}</span></div>
                    <div>
                        <button class="btn-primary" style="padding: 8px 16px;">Editar</button>
                        <button class="btn-primary" style="padding: 8px 16px; background-color: #8e8e8e;">Cancelar</button>
                    </div>
                </div>`;
            });
        }
    } catch (error) { console.error("Error en Dashboard:", error); }
}

// 2. CARGAR CLIENTES 
async function cargarClientes() {
    try {
        const res = await fetch(`${API_URL}/clientes`);
        const clientes = await res.json();
        const contenedor = document.getElementById("lista-clientes");
        contenedor.innerHTML = ""; 

        clientes.forEach(cliente => {
            const palabras = cliente.nombre.split(' ');
            let iniciales = "";
            if (palabras.length >= 2) {
                iniciales = palabras[0][0] + palabras[1][0];
            } else {
                iniciales = palabras[0].substring(0, 2);
            }
            iniciales = iniciales.toUpperCase();

            contenedor.innerHTML += `
            <div class="card" style="margin-bottom: 15px; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="icon-box" style="background-color: var(--color-fondo-oscuro); color: white;">
                        ${iniciales}
                    </div>
                    <div>
                        <p class="card-title">Cliente</p>
                        <h3>${cliente.nombre}</h3>
                    </div>
                </div>
                <div>
                    <p class="card-title">Teléfono</p>
                    <span>${cliente.telefono}</span>
                </div>
                <div>
                    <p class="card-title">Visitas</p>
                    <span>1 visitas</span> 
                </div>
                <div>
                    <button class="btn-primary" style="padding: 8px 16px;">Editar</button>
                    <button class="btn-primary" style="padding: 8px 16px; background-color: #8e8e8e;">Eliminar</button>
                </div>
            </div>`;
        });
    } catch (error) { console.error("Error al cargar los clientes:", error); }
}

// 3. CARGAR BARBEROS 
async function cargarBarberos() {
    try {
        const res = await fetch(`${API_URL}/barberos`);
        const barberos = await res.json();
        const contenedor = document.getElementById("lista-barberos");
        contenedor.innerHTML = "";

        barberos.forEach(barbero => {
            const iniciales = barbero.nombre.substring(0, 2).toUpperCase();
            contenedor.innerHTML += `
            <div class="card" style="margin-bottom: 15px; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div class="icon-box" style="background-color: var(--color-fondo-oscuro); color: white;">${iniciales}</div>
                    <div><p class="card-title">Barbero</p><h3>${barbero.nombre}</h3></div>
                </div>
                <div>
                    <p class="card-title">Especialidad</p>
                    <span>Corte general</span>
                </div>
                <div>
                    <p class="card-title">Citas hoy</p>
                    <span>0 citas</span>
                </div>
                <div>
                    <button class="btn-primary" style="padding: 8px 16px;">Editar</button>
                    <button class="btn-primary" style="padding: 8px 16px; background-color: #8e8e8e;">Eliminar</button>
                </div>
            </div>`;
        });
    } catch (error) { console.error("Error:", error); }
}

// 4. CARGAR SERVICIOS 
async function cargarServicios() {
    try {
        const res = await fetch(`${API_URL}/servicios`);
        const servicios = await res.json();
        const contenedor = document.getElementById("lista-servicios");
        contenedor.innerHTML = "";

        servicios.forEach(servicio => {
            contenedor.innerHTML += `
            <div class="card" style="margin-bottom: 15px; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div><p class="card-title">Servicio</p><h3>${servicio.nombre}</h3></div>
                </div>
                <div><p class="card-title">Descripción</p><span>${servicio.descripcion}</span></div>
                <div><p class="card-title">Costo</p><span>$${servicio.precio}</span></div>
                <div><p class="card-title">Duración</p><span>${servicio.duracion} min</span></div>
                <div>
                    <button class="btn-primary" style="padding: 8px 16px;">Editar</button>
                    <button class="btn-primary" style="padding: 8px 16px; background-color: #8e8e8e;">Eliminar</button>
                </div>
            </div>`;
        });
    } catch (error) { console.error("Error:", error); }
}

// 5. CARGAR CITAS 
async function cargarCitas() {
    const fechaHoy = new Date().toISOString().split('T')[0];
    const opcionesFecha = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    
    const elementoFecha = document.getElementById("fecha-actual");
    if(elementoFecha) elementoFecha.innerText = new Date().toLocaleDateString('es-ES', opcionesFecha);

    try {
        const resResumen = await fetch(`${API_URL}/resumen/${fechaHoy}`);
        if (resResumen.ok) {
            const resumen = await resResumen.json();
            document.getElementById("stats-citas-hoy").innerText = resumen.total_citas;
            document.getElementById("stats-ingresos-hoy").innerText = `$${resumen.ingresos_estimados}`;
        }

        const resAgenda = await fetch(`${API_URL}/agenda/${fechaHoy}`);
        if (resAgenda.ok) {
            const agenda = await resAgenda.json();
            const contenedor = document.getElementById("lista-citas");
            contenedor.innerHTML = ""; 

            if (agenda.length === 0) {
                document.getElementById("stats-proxima-hora").innerText = "--:--";
                document.getElementById("stats-proxima-cliente").innerText = "Libre";
                contenedor.innerHTML = "<p style='color: white;'>No hay citas programadas para hoy.</p>";
                return;
            }

            document.getElementById("stats-proxima-hora").innerText = agenda[0].hora.substring(0,5);
            document.getElementById("stats-proxima-cliente").innerText = agenda[0].cliente;

            agenda.forEach(cita => {
                const horaSola = cita.hora.substring(0,5); 
                contenedor.innerHTML += `
                <div class="card" style="margin-top: 15px; justify-content: space-between;">
                    <div class="card-data">
                        <h3>${horaSola}</h3>
                        <span>${cita.cliente}</span>
                    </div>
                    <div>
                        <p class="card-title">${cita.servicio}</p>
                        <span>${cita.barbero} - $${cita.precio}</span>
                    </div>
                    <div>
                        <button class="btn-primary" style="padding: 8px 16px;">Editar</button>
                        <button class="btn-primary" style="padding: 8px 16px; background-color: #8e8e8e;">Cancelar</button>
                    </div>
                </div>`;
            });
        }
    } catch (error) { console.error("Error al cargar las citas:", error); }
}

// MODAL DE CLIENTES
function abrirModalCliente() {
    document.getElementById("modal-cliente").style.display = "block";
}

function cerrarModalCliente() {
    document.getElementById("modal-cliente").style.display = "none";
    document.getElementById("form-cliente").reset(); 
}

async function guardarCliente(evento) {
    evento.preventDefault(); 
    
    const nombre = document.getElementById("cliente-nombre").value;
    const telefono = document.getElementById("cliente-telefono").value;

    try {
        const res = await fetch(`${API_URL}/clientes`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre, telefono: telefono })
        });

        if (res.ok) {
            alert("¡Cliente guardado con éxito!");
            cerrarModalCliente(); 
            cargarClientes();     
        } else {
            alert("Hubo un error al comunicarse con el servidor.");
        }
    } catch (error) { console.error("Error:", error); }
}

// MODAL DE BARBEROS
function abrirModalBarbero() {
    document.getElementById("modal-barbero").style.display = "block";
}

function cerrarModalBarbero() {
    document.getElementById("modal-barbero").style.display = "none";
    document.getElementById("form-barbero").reset();
}

async function guardarBarbero(evento) {
    evento.preventDefault(); 
    const nombre = document.getElementById("barbero-nombre").value;

    try {
        const res = await fetch(`${API_URL}/barberos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ nombre: nombre }) 
        });

        if (res.ok) {
            alert("¡Barbero guardado con éxito!");
            cerrarModalBarbero();
            cargarBarberos(); 
        } else {
            alert("Hubo un error al comunicarse con el servidor.");
        }
    } catch (error) { console.error("Error:", error); }
}


// MODAL DE CITAS

async function abrirModalCita() {
    try {
        const [resClientes, resBarberos, resServicios] = await Promise.all([
            fetch(`${API_URL}/clientes`),
            fetch(`${API_URL}/barberos`),
            fetch(`${API_URL}/servicios`)
        ]);

        const clientes = await resClientes.json();
        const barberos = await resBarberos.json();
        const servicios = await resServicios.json();

        const selCliente = document.getElementById("cita-cliente");
        selCliente.innerHTML = "<option value=''>-- Selecciona un cliente --</option>";
        clientes.forEach(c => selCliente.innerHTML += `<option value="${c.id}">${c.nombre}</option>`);

        const selBarbero = document.getElementById("cita-barbero");
        selBarbero.innerHTML = "<option value=''>-- Selecciona un barbero --</option>";
        barberos.forEach(b => selBarbero.innerHTML += `<option value="${b.id}">${b.nombre}</option>`);

        const selServicio = document.getElementById("cita-servicio");
        selServicio.innerHTML = "<option value=''>-- Selecciona un servicio --</option>";
        servicios.forEach(s => selServicio.innerHTML += `<option value="${s.id}">${s.nombre} ($${s.precio})</option>`);

        document.getElementById("modal-cita").style.display = "block";
    } catch (error) {
        console.error("Error al cargar datos para el modal:", error);
        alert("Error al cargar las listas. Verifica que el servidor esté encendido.");
    }
}

function cerrarModalCita() {
    document.getElementById("modal-cita").style.display = "none";
    document.getElementById("form-cita").reset(); 
}

async function guardarCita(evento) {
    evento.preventDefault(); 

    const nuevaCita = {
        cliente_id: parseInt(document.getElementById("cita-cliente").value),
        barbero_id: parseInt(document.getElementById("cita-barbero").value),
        servicio_id: parseInt(document.getElementById("cita-servicio").value),
        fecha: document.getElementById("cita-fecha").value,
        hora: document.getElementById("cita-hora").value + ":00" 
    };

    try {
        const res = await fetch(`${API_URL}/citas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(nuevaCita)
        });

        if (res.ok) {
            alert("¡Cita agendada con éxito!");
            cerrarModalCita();
            cargarCitas(); 
        } else {
            const error = await res.json();
            alert("Error: " + error.detail);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}