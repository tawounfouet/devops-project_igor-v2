import { useState, useEffect } from "react";
import "./App.css";
import SearchBar from "./components/SearchBar";
import WeatherCard from "./components/WeatherCard";
import HistoryList from "./components/HistoryList";
import { fetchWeatherByCity, fetchSearchHistory } from "./services/weatherService";

function App() {
  const [weatherData, setWeatherData] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  // Charger l'historique des recherches au chargement de l'application
  useEffect(() => {
    const loadHistory = async () => {
      setLoading(true);
      try {
        const historyData = await fetchSearchHistory();
        if (historyData.length) {
          // Convertir les données d'API au format attendu par HistoryList
          const formattedHistory = historyData.map(item => ({
            id: item.id,
            city: item.city,
            date: new Date(item.searched_at).toLocaleString(),
            temperature: item.temperature,
            description: item.description
          }));
          setHistory(formattedHistory);
        }
      } catch (err) {
        console.error("Impossible de charger l'historique:", err);
      } finally {
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  const handleSearch = async (city) => {
    setLoading(true);
    try {
      const data = await fetchWeatherByCity(city);
      if (data) {
        setWeatherData(data);
        // Rafraîchir l'historique après recherche
        const historyData = await fetchSearchHistory();
        if (historyData.length) {
          const formattedHistory = historyData.map(item => ({
            id: item.id,
            city: item.city,
            date: new Date(item.searched_at).toLocaleString(),
            temperature: item.temperature,
            description: item.description
          }));
          setHistory(formattedHistory);
        }
      }
    } catch (err) {
      console.error("Erreur lors de la recherche:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <HistoryList history={history} />
      </div>
      <div className="main">
        <h1>☁️ Weather App</h1>
        <SearchBar onSearch={handleSearch} />
        {weatherData && <WeatherCard data={weatherData} />}
      </div>
    </div>
  );
}

export default App;
