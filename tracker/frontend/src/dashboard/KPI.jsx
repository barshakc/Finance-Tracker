export default function KPI({ title, value, suffix }) {
  return (
    <div
      style={{
        background: "#1e1e1e",   
        color: "#e0e0e0",       
        padding: "14px 16px",        
        borderRadius: "12px",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        boxShadow: "0 6px 16px rgba(0,0,0,0.5)",
        border: "1px solid #2c2c2c",
        minHeight: "90px",           
        textAlign: "center",
        transition: "transform 0.2s, box-shadow 0.2s",
      }}
    >
      <p style={{ fontSize: "12px", fontWeight: 500, marginBottom: "6px", color: "#b0b0b0" }}>
        {title}
      </p>
      <h3 style={{ fontSize: "18px", fontWeight: 600, color: "#fff" }}>
        {value}{suffix || ""}
      </h3>
    </div>
  );
}
