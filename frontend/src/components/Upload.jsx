import React, { useState } from "react";

function Upload() {
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");
  const [response, setResponse] = useState(null);

  const upload = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }

    console.log("Uploading file:", file);

    setStatus("Uploading...");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("http://127.0.0.1:8000/songs/upload", {
        method: "POST",
        body: formData
      });

      const data = await res.json();

      console.log("Server response:", data);

      setResponse(data);
      setStatus("Upload successful ✅");

    } catch (error) {
      console.error("Upload error:", error);
      setStatus("Upload failed ❌");
    }
  };

  return (
    <div style={{
      border: "1px solid #ccc",
      padding: "15px",
      margin: "20px auto",
      width: "300px",
      borderRadius: "10px"
    }}>
      <h3>📤 Upload Song</h3>

      <input
        type="file"
        onChange={(e) => {
          const selected = e.target.files[0];
          setFile(selected);
          console.log("Selected file:", selected);
        }}
      />

      <br /><br />

      <button onClick={upload}>Upload</button>

      {/* 🔥 STATUS */}
      <p>{status}</p>

      {/* 🔥 RESPONSE DETAILS */}
      {response && (
        <div>
          <p><strong>Raas:</strong> {response.rass}</p>
          <p><strong>Message:</strong> {response.message}</p>
        </div>
      )}
    </div>
  );
}

export default Upload;