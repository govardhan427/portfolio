import React, { useState, useEffect } from 'react';
import { getFiles, uploadFile, deleteFile } from '../../../services/vaultService';
import { FileText, UploadCloud, Trash2, Copy, Check } from 'lucide-react';
import './FileManager.css';

const FileManager = () => {
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);

  useEffect(() => {
    loadFiles();
  }, []);

  const loadFiles = async () => {
    try {
      const data = await getFiles();
      setFiles(data);
    } catch (error) {
      console.error("Failed to load vault", error);
    }
  };

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    try {
      // 1. Upload
      await uploadFile(file, 'RESUME');
      // 2. Refresh List
      await loadFiles(); 
      // 3. Clear Input (allows re-uploading same file)
      e.target.value = ''; 
    } catch (error) {
      console.error("Upload Error:", error);
      // Show real error message from Backend
      alert(`Upload Failed: ${error.response?.data?.detail || error.message}`);
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (id) => {
    if(!window.confirm("Delete this file permanently?")) return;
    try {
      await deleteFile(id);
      setFiles(files.filter(f => f.id !== id));
    } catch (error) {
      console.error("Delete failed", error);
      alert("Could not delete file.");
    }
  };

  const copyLink = (url, id) => {
    navigator.clipboard.writeText(url);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="vault-panel">
      <div className="vault-header">
        <h3>Secure Cloud Vault</h3>
        <div className="upload-wrapper">
          <input 
            type="file" 
            id="file-upload" 
            onChange={handleUpload} 
            disabled={uploading} 
            hidden 
          />
          <label htmlFor="file-upload" className={`upload-btn ${uploading ? 'disabled' : ''}`}>
            <UploadCloud size={16} />
            {uploading ? 'Uploading...' : 'Upload File'}
          </label>
        </div>
      </div>

      <div className="file-grid">
        {files.length === 0 ? (
          <div className="empty-vault">Vault is empty. Upload your Resume.</div>
        ) : (
          files.map((file) => (
            <div key={file.id} className="file-card">
              <div className="file-icon">
                <FileText size={30} color="var(--neon-purple)" />
              </div>
              <div className="file-info">
                <div className="file-name" title={file.name}>{file.name}</div>
                <div className="file-meta">
                   {file.size} • {new Date(file.uploaded_at).toLocaleDateString()}
                </div>
              </div>
              <div className="file-actions">
                <button 
                    onClick={() => copyLink(file.file_url, file.id)} 
                    className="action-btn"
                    title="Copy Link"
                >
                  {copiedId === file.id ? <Check size={16} color="var(--neon-green)"/> : <Copy size={16} />}
                </button>
                <button 
                    onClick={() => handleDelete(file.id)} 
                    className="action-btn delete"
                    title="Delete"
                >
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default FileManager;