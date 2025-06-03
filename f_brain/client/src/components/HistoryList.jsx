import "./HistoryList.css";

export default function HistoryList({ history }) {
  return (
    <div className="history-list">
      <h3>Search History</h3>
      {history.length === 0 ? (
        <div className="empty-history">Aucun historique disponible</div>
      ) : (
        history.map((item) => (
          <div key={item.id || item.date} className="history-item">
            <span>📍 {item.city}</span>
            {item.temperature && (
              <span className="temp">{Math.round(item.temperature)}°C</span>
            )}
            {item.description && (
              <span className="desc">{item.description}</span>
            )}
            <span className="timestamp">{item.date}</span>
          </div>
        ))
      )}
    </div>
  );
}
