import "./WeatherCard.css";

export default function WeatherCard({ data }) {
  // URL de base pour les icônes météo d'OpenWeatherMap
  const iconUrl = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;

  return (
    <div className="weather-card">
      <h2>{data.name} {data.sys.country && <span className="country">({data.sys.country})</span>}</h2>
      <div className="weather-icon">
        <img src={iconUrl} alt={data.weather[0].description} />
      </div>
      <p>{data.weather[0].description}</p>
      <div className="temperature">{Math.round(data.main.temp)}°C</div>
      <p>Feels like {Math.round(data.main.feels_like)}°C</p>
      <div className="metrics">
        <div><strong>Humidity:</strong> {data.main.humidity}%</div>
        <div><strong>Pressure:</strong> {data.main.pressure} hPa</div>
        <div><strong>Wind:</strong> {data.wind.speed} m/s</div>
        <div><strong>Visibility:</strong> {data.visibility / 1000} km</div>
      </div>
    </div>
  );
}
