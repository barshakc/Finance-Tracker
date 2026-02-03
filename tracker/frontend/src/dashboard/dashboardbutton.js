import React from "react";

const DashboardButton = ({ onClick }) => {
  return (
    <button
      onClick={onClick}
      className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
    >
      Analytics Dashboard
    </button>
  );
};

export default DashboardButton;
