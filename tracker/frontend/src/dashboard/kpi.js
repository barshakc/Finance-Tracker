export default function KPI({ title, value, suffix = "" }) {
  return (
    <div
      style={{
        flex: "1 1 22%",
        background: "#f8f9fa",
        padding: "20px",
        borderRadius: "12px",
        boxShadow: "0 4px 10px rgba(0,0,0,0.05)",
      }}
    >
      <span style={{ color: "#555" }}>{title}</span>
      <div
        style={{
          fontSize: "22px",
          fontWeight: "bold",
          marginTop: "8px",
        }}
      >
        {value}
        {suffix}
      </div>
    </div>
  );
}
