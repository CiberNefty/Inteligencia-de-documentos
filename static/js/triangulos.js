const ROTACIONES = ['top-left', 'top-right', 'bottom-left', 'bottom-right'];
const COLORES = ['#6bff8e', '#2fae54', '#ffb347', '#3d3d5c'];
const TAMANO = 34;
const MAX_TRIANGULOS = 250; // antes =90
const VIDA_MS = 5000;          // cuánto tiempo queda visible cada triángulo
const INTERVALO_NUEVO_MS = 200; // Antes = 500. cada cuánto aparece uno nuevo, en el loop

function crearTriangulo(contenedor) {
  const rotacion = ROTACIONES[Math.floor(Math.random() * ROTACIONES.length)];
  const color = COLORES[Math.floor(Math.random() * COLORES.length)];
  const mitad = TAMANO / 2;

  const x = Math.random() * window.innerWidth;
  const y = Math.random() * window.innerHeight;

  const el = document.createElement('div');
  el.className = `triangulo ${rotacion}`;
  el.style.borderTop = `${mitad}px solid ${color}`;
  el.style.borderLeft = `${mitad}px solid ${color}`;
  el.style.borderBottom = `${mitad}px solid transparent`;
  el.style.borderRight = `${mitad}px solid transparent`;
  el.style.left = `${x}px`;
  el.style.top = `${y}px`;

  contenedor.appendChild(el);

  requestAnimationFrame(() => el.classList.add('visible'));
  setTimeout(() => el.classList.add('rotado'), 200);

  setTimeout(() => {
    el.classList.remove('visible');
    el.classList.add('fade-out');
    setTimeout(() => el.remove(), 1500);
  }, VIDA_MS);
}

function iniciarLoopTriangulos() {
  const contenedor = document.querySelector('.triangulos-container');
  if (!contenedor) {
    console.error('No se encontró .triangulos-container en el HTML');
    return;
  }

  for (let i = 0; i < MAX_TRIANGULOS; i++) {
    setTimeout(() => crearTriangulo(contenedor), i * 150);
  }

  setInterval(() => crearTriangulo(contenedor), INTERVALO_NUEVO_MS);
}

document.addEventListener('DOMContentLoaded', iniciarLoopTriangulos);