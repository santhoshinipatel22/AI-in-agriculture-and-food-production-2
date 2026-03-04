import React, { useState, useRef } from 'react';
import axios from 'axios';
import './DiseaseDetection.css';

export default function DiseaseDetection() {
  const [selectedCrop, setSelectedCrop] = useState('');
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [detection, setDetection] = useState(null);
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  const API_URL = process.env.REACT_APP_API_URL;
  const token = localStorage.getItem('accessToken');

  const handleImageSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImage(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDetect = async () => {
    if (!image || !selectedCrop) {
      alert('Please select a crop and upload an image');
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('image', image);

    try {
      const response = await axios.post(
        `${API_URL}/api/diseases/detect/${selectedCrop}`,
        formData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      setDetection(response.data.data);
    } catch (error) {
      console.error('Detection error:', error);
      alert('Error detecting disease. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="disease-detection">
      <h1>AI Crop Disease Detection</h1>
      <p>Upload a leaf image to detect diseases using advanced AI</p>

      <div className="detection-container">
        <div className="upload-section">
          <div className="form-group">
            <label>Select Your Crop</label>
            <select 
              value={selectedCrop} 
              onChange={(e) => setSelectedCrop(e.target.value)}
            >
              <option>-- Select Crop --</option>
              <option value="rice">Rice</option>
              <option value="wheat">Wheat</option>
              <option value="corn">Corn</option>
              <option value="tomato">Tomato</option>
              <option value="potato">Potato</option>
            </select>
          </div>

          <div className="upload-box" onClick={() => fileInputRef.current.click()}>
            {preview ? (
              <img src={preview} alt="Preview" />
            ) : (
              <>
                <p>📸 Click to upload leaf image</p>
                <p>or drag and drop</p>
              </>
            )}
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageSelect}
              style={{ display: 'none' }}
            />
          </div>

          <button 
            className="detect-btn" 
            onClick={handleDetect}
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Detect Disease'}
          </button>
        </div>

        {/* Detection Results */}
        {detection && (
          <div className="results-section">
            <h2>Detection Result</h2>
            <div className="result-card">
              <div className="severity" style={{ 
                borderColor: detection.severity === 'high' ? '#d32f2f' : 
                            detection.severity === 'medium' ? '#ff9800' : '#4caf50'
              }}>
                <h3>{detection.diseaseName}</h3>
                <p>Severity: <strong>{detection.severity.toUpperCase()}</strong></p>
                <p>Confidence: {detection.confidence}%</p>
                <p>Affected Area: {detection.affectedArea}%</p>
              </div>

              <div className="treatment-section">
                <h4>Treatment Options</h4>
                
                <div className="treatment-type">
                  <h5>Organic Treatment</h5>
                  <ul>
                    {detection.treatment.organic.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="treatment-type">
                  <h5>Chemical Treatment</h5>
                  <ul>
                    {detection.treatment.chemical.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>

                <div className="prevention">
                  <h5>Prevention Measures</h5>
                  <ul>
                    {detection.preventiveMeasures.map((item, idx) => (
                      <li key={idx}>{item}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {detection.recommendedProducts?.length > 0 && (
                <div className="products-section">
                  <h4>Recommended Products</h4>
                  {detection.recommendedProducts.map((product, idx) => (
                    <div key={idx} className="product-item">
                      <p><strong>{product.name}</strong></p>
                      <p>Quantity: {product.quantity} | Price: ₹{product.price}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
