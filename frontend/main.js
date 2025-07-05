const API_BASE = "http://127.0.0.1:5000";
const token = localStorage.getItem("token");




const tesisSelec = document.getElementById("tesis");
const visorDiv = document.getElementById("visor");
const pdfViewer = document.getElementById("pdfViewer");

if (tesisSelec) {
  fetch(`${API_BASE}/tesis/asignadas`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => {
     tesisSelec.innerHTML = `<option disabled selected>Seleccione una tesis</option>`; 
    data.forEach(t => {
      const opt = document.createElement("option");
      opt.value = t.id;
      opt.textContent = t.title;
      opt.dataset.archivo = t.file; // Guardamos el nombre del archivo
      tesisSelec.appendChild(opt);
    });

    tesisSelec.addEventListener("change", () => {
      const selected = tesisSelec.selectedOptions[0];
      const archivo = selected.dataset.archivo;

      if (archivo) {
        pdfViewer.src = `${API_BASE}/pdfs/${archivo}`;
        visorDiv.classList.remove("hidden");
      } else {
        pdfViewer.src = "";
        visorDiv.classList.add("hidden");
      }
    });
  });
}










// -------------------- LOGIN --------------------
const loginForm = document.getElementById("loginForm");
if (loginForm) {
  loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const res = await fetch(`${API_BASE}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    const data = await res.json();
    if (data.token) {
      localStorage.setItem("token", data.token);
      const payload = JSON.parse(atob(data.token.split('.')[1]));
const rol = payload.rol || (payload.sub && payload.sub.rol);


console.log("TOKEN LOGIN:", data);



    if (data.token) {
  localStorage.setItem("token", data.token);
  const payload = JSON.parse(atob(data.token.split('.')[1]));
  console.log("PAYLOAD JWT:", payload);

  const rol = payload.rol || (payload.sub && payload.sub.rol);
  localStorage.setItem("rol", rol);
  console.log("ROL:", rol);

  // Redirigir según rol
  if (rol === "estudiante") {
    window.location.href = "subir_tesis";
  } else if (rol === "evaluador") {
    window.location.href = "evaluar_tesis";
  } else if (rol === "decano") {
    window.location.href = "certificar_tesis";
  } else {
    window.location.href = "/";
  }
}

    } else {
      alert(data.error || "Login fallido");
    }
  });
}

// -------------------- MENÚ SEGÚN ROL --------------------
document.addEventListener("DOMContentLoaded", () => {
  const menu = document.getElementById("menu");
  const rol = localStorage.getItem("rol");

  if (menu && rol) {
    if (rol === "estudiante") {
      menu.innerHTML = `
        <a href="subir_tesis.html">📤 Subir Tesis</a>
        <a href="estado_tesis.html">📄 Ver Estado</a>
      `;
    } else if (rol === "evaluador") {
      menu.innerHTML = `<a href="evaluar_tesis.html">📝 Evaluar Tesis</a>`;
    } else if (rol === "decano") {
      menu.innerHTML = `<a href="certificar_tesis.html">✅ Certificar Tesis</a>`;
    } else {
      menu.innerHTML = `<p> Rol desconocido.</p>`;
    }
  }
});


// -------------------- SUBIR TESIS --------------------
const uploadForm = document.getElementById("uploadForm");
if (uploadForm) {
  uploadForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = new FormData(uploadForm);
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      headers: { Authorization: `Bearer ${token}` },
      body: form,
    });
    const data = await res.json();
    alert(data.msg || data.error);
  });
}

// -------------------- VER ESTADO DE TESIS --------------------
const estadoDiv = document.getElementById("estado");
if (estadoDiv) {
  fetch(`${API_BASE}/mis_tesis`, {
    headers: { Authorization: `Bearer ${token}` }
  }).then(res => res.json()).then(data => {
    estadoDiv.innerHTML = "";
    data.forEach(t => {
      estadoDiv.innerHTML += `
        <div class="card">
          <h3>${t.title}</h3>
          <p>Estado: ${t.status}</p>
          <p>Nota: ${t.grade || "Sin nota"}</p>
          <p>Retroalimentación: ${t.comment || "Sin comentario"}</p>
        </div>`;
    });
  });
}

function verEstado() {
  const estadoDiv = document.getElementById("estado");
  estadoDiv.classList.remove("hidden"); // Mostrar el div
  estadoDiv.innerHTML = "<p class='text-sm text-gray-500'>Cargando...</p>";

  fetch(`${API_BASE}/mis_tesis`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => {
    if (data.length === 0) {
      estadoDiv.innerHTML = "<p class='text-gray-600'>No tienes tesis registradas aún.</p>";
      return;
    }

    estadoDiv.innerHTML = ""; // Limpiar antes de agregar
    data.forEach(t => {
      estadoDiv.innerHTML += `
        <div class="mb-4 p-4 border rounded bg-white shadow">
          <h3 class="text-lg font-semibold text-blue-700">${t.title}</h3>
          <p>📌 Estado: <strong>${t.status}</strong></p>
          <p>📈 Nota: ${t.grade || "Sin nota"}</p>
          <p>🗒️ Retroalimentación: ${t.comment || "Sin comentario"}</p>
        </div>`;
    });
  });
}


// -------------------- EVALUAR TESIS --------------------
      //tesisSelect.innerHTML = `<option disabled selected>Seleccione una tesis</option>`; 
const tesisSelect = document.getElementById("tesis");
if (tesisSelect) {
  fetch(`${API_BASE}/tesis/asignadas`, {
    headers: { Authorization: `Bearer ${token}` }
  }).then(res => res.json()).then(data => {
   
    data.forEach(t => {
      const opt = document.createElement("option");
      opt.value = t.id;
      opt.textContent = t.title;
      tesisSelect.appendChild(opt);
    });
  });
}

function evaluar() {
  const tesis_id = document.getElementById("tesis").value;
  const comentario = document.getElementById("comentario").value;
  const nota = document.getElementById("nota").value;
  fetch(`${API_BASE}/evaluar`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ tesis_id, comentario, nota })
  }).then(res => res.json()).then(data => alert(data.msg || data.error));






  
}

// -------------------- CERTIFICAR TESIS --------------------
const tabla = document.getElementById("tabla");

if (tabla) {
  fetch(`${API_BASE}/admin/tesis-evaluadas`, {
    headers: { Authorization: `Bearer ${token}` }
  })
  .then(res => res.json())
  .then(data => {
    const tbody = tabla.querySelector("tbody");
    tbody.innerHTML = ""; // Limpiar antes de llenar

    let tesisEncontradas = 0;

    data.forEach(t => {
         if (t.status === "Evaluada" || t.status === "Certificada") {
        const row = tbody.insertRow();
        row.innerHTML = `
          <td class="border p-2">${t.id}</td>
          <td class="border p-2">${t.title}</td>
          <td class="border p-2">${t.status}</td>
          <td class="p-2">
            ${t.signature ? `
              <div>
                <strong>Firmado por:</strong> ${t.signature.signed_by}<br>
                <strong>Fecha:</strong> ${t.signature.date}<br>
                <strong>ID Firma:</strong> ${t.signature.hash}
              </div>
            ` : 'Pendiente'}
          </td>
          <td class="border p-2">
            <button onclick="certificar(${t.id})" class="bg-green-600 text-white px-2 py-1 rounded">Certificar</button>
          </td>
        `;
        tesisEncontradas++;
      }
    });

    if (tesisEncontradas === 0) {
      tbody.innerHTML = `
        <tr><td colspan="4" class="text-center text-gray-500 p-4">No hay tesis evaluadas.</td></tr>
      `;
    }
  })
  .catch(err => {
    console.error("Error al obtener tesis evaluadas:", err);
    alert("No se pudieron cargar las tesis. Asegúrate de estar logueado y que el backend esté corriendo.");
  });
}


function certificar(id) {
  fetch(`${API_BASE}/certificar/${id}`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` }
  }).then(res => res.json()).then(data => alert(data.msg || data.error));
}


function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("rol");
  window.location.href = "login";
}
