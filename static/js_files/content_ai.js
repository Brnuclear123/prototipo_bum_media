// Mapeamento das coordenadas das capitais dos estados brasileiros
const stateCoordinates = {
    'AC': { lat: -9.97499, lng: -67.8243 },
    'AL': { lat: -9.66599, lng: -35.735 },
    'AP': { lat: 0.0389, lng: -51.0664 },
    'AM': { lat: -3.119, lng: -60.0217 },
    'BA': { lat: -12.9714, lng: -38.5014 },
    'CE': { lat: -3.71722, lng: -38.5433 },
    'DF': { lat: -15.8267, lng: -47.9218 },
    'ES': { lat: -20.3155, lng: -40.3128 },
    'GO': { lat: -16.6864, lng: -49.2643 },
    'MA': { lat: -2.53073, lng: -44.3068 },
    'MT': { lat: -15.601, lng: -56.0974 },
    'MS': { lat: -20.4697, lng: -54.6201 },
    'MG': { lat: -19.9191, lng: -43.9386 },
    'PA': { lat: -1.45502, lng: -48.5024 },
    'PB': { lat: -7.11509, lng: -34.8631 },
    'PR': { lat: -25.4296, lng: -49.2713 },
    'PE': { lat: -8.04756, lng: -34.877 },
    'PI': { lat: -5.08921, lng: -42.8016 },
    'RJ': { lat: -22.9068, lng: -43.1729 },
    'RN': { lat: -5.79448, lng: -35.211 },
    'RS': { lat: -30.0346, lng: -51.2177 },
    'RO': { lat: -8.76077, lng: -63.9039 },
    'RR': { lat: 2.81972, lng: -60.6733 },
    'SC': { lat: -27.5954, lng: -48.548 },
    'SP': { lat: -23.5505, lng: -46.6333 },
    'SE': { lat: -10.9472, lng: -37.0731 },
    'TO': { lat: -10.184, lng: -48.3336 }
};

document.getElementById('location').addEventListener('change', function() {
    const selectedState = this.value;
    if (stateCoordinates[selectedState]) {
        const { lat, lng } = stateCoordinates[selectedState];
        
        fetch(`/get_weather?lat=${lat}&lng=${lng}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    document.getElementById('weather-info').textContent = 'Erro ao obter clima';
                } else {
                    document.getElementById('weather-info').textContent = `${data.temperatura_atual}°C`;
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                document.getElementById('weather-info').textContent = 'Erro ao obter clima';
            });
    }
});
