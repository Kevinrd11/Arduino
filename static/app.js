const sensorDefinitions = [
  {
    key: 'temperature_c',
    label: 'Temperatura',
    unit: '°C',
    description: 'Rango térmico del ambiente monitoreado.',
  },
  {
    key: 'humidity_percent',
    label: 'Humedad',
    unit: '%',
    description: 'Porcentaje de humedad relativa detectada.',
  },
  {
    key: 'light_lux',
    label: 'Luz',
    unit: 'lux',
    description: 'Intensidad luminosa recibida por el sensor.',
  },
  {
    key: 'gas_ppm',
    label: 'Gas',
    unit: 'ppm',
    description: 'Concentración simulada para prueba del tablero.',
  },
  {
    key: 'distance_cm',
    label: 'Distancia',
    unit: 'cm',
    description: 'Medición de proximidad del objeto más cercano.',
  },
  {
    key: 'motion_detected',
    label: 'Movimiento',
    unit: '',
    description: 'Estado lógico del detector de presencia.',
  },
];

const cards = document.querySelector('#sensor-cards');
const table = document.querySelector('#readings-table');
const lastUpdated = document.querySelector('#last-updated');
const mode = document.querySelector('#connection-mode');
const message = document.querySelector('#connection-message');
const refreshButton = document.querySelector('#refresh-button');
const tabs = document.querySelectorAll('.tab');
const panels = {
  single: document.querySelector('#single-view'),
  all: document.querySelector('#all-view'),
};

const formatDate = (value) =>
  new Intl.DateTimeFormat('es', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  }).format(new Date(value));

const formatValue = (reading, sensor) => {
  if (sensor.key === 'motion_detected') {
    return reading[sensor.key] ? 'Sí' : 'No';
  }

  return `${reading[sensor.key]} ${sensor.unit}`;
};

function renderCards(reading) {
  cards.innerHTML = sensorDefinitions
    .map(
      (sensor) => `
        <article class="card">
          <span>${sensor.label}</span>
          <strong>${formatValue(reading, sensor)}</strong>
          <p>${sensor.description}</p>
        </article>
      `,
    )
    .join('');
  lastUpdated.textContent = formatDate(reading.timestamp);
}

function renderTable(readings) {
  table.innerHTML = readings
    .map(
      (reading) => `
        <tr>
          <td>${formatDate(reading.timestamp)}</td>
          <td>${reading.temperature_c}</td>
          <td>${reading.humidity_percent}</td>
          <td>${reading.light_lux}</td>
          <td>${reading.gas_ppm}</td>
          <td>${reading.distance_cm}</td>
          <td><span class="badge ${reading.motion_detected ? 'yes' : 'no'}">${reading.motion_detected ? 'Detectado' : 'Sin movimiento'}</span></td>
        </tr>
      `,
    )
    .join('');
}

async function updateDashboard() {
  const readingResponse = await fetch('/api/reading');
  const latestReading = await readingResponse.json();
  renderCards(latestReading);

  const readingsResponse = await fetch('/api/readings');
  const readings = await readingsResponse.json();
  renderTable(readings);
}

async function updateStatus() {
  const response = await fetch('/api/status');
  const status = await response.json();
  mode.textContent = status.mode === 'simulation' ? 'Modo simulación' : 'Arduino conectado';
  message.textContent = status.message;
}

tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    const view = tab.dataset.view;
    tabs.forEach((item) => item.classList.toggle('active', item === tab));
    Object.entries(panels).forEach(([name, panel]) => {
      panel.classList.toggle('active', name === view);
    });
  });
});

refreshButton.addEventListener('click', updateDashboard);

updateStatus();
updateDashboard();
setInterval(updateDashboard, 2500);
