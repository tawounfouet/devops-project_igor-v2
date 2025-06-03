// Configuration pour l'API backend
// Détecter l'environnement pour choisir la bonne URL
const getBackendUrl = () => {
  // Si on accède directement au frontend (port 4173), utiliser l'URL absolue vers le backend
  if (window.location.port === "4173") {
    return "http://localhost:8000/api/v1";
  }
  // Sinon, utiliser l'URL relative pour nginx
  return import.meta.env.VITE_API_BASE_URL || "/api/v1";
};

const BACKEND_URL = getBackendUrl();

export async function fetchWeatherByCity(city) {
  try {
    // Utiliser notre API Django pour obtenir et enregistrer les données météo
    const res = await fetch(`${BACKEND_URL}/weather/?city=${encodeURIComponent(city)}`);
    if (!res.ok) throw new Error(`Erreur: ${res.status}`);
    const data = await res.json();
    
    // Retourner les données de l'API OpenWeatherMap (conservées par notre backend)
    return data.data;
  } catch (err) {
    console.error("Fetch error:", err.message);
    return null;
  }
}

// Nouvelle fonction pour récupérer l'historique des recherches
export async function fetchSearchHistory(limit = 10) {
  try {
    const res = await fetch(`${BACKEND_URL}/history/?limit=${limit}`);
    if (!res.ok) throw new Error(`Erreur: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error("History fetch error:", err.message);
    return [];
  }
}
