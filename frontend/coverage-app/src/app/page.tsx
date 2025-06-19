"use client";

import { postCoverageRequest } from "../../lib/api";
import { useState, ChangeEvent, FormEvent } from "react";
import { Upload, FileText, Send, Loader2, CheckCircle, AlertCircle,Download,X,Radio } from "lucide-react";


export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selected = e.target.files?.[0] || null;
    setFile(selected);
    setError(null);
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      if (droppedFile.type === "application/json" || droppedFile.name.endsWith('.json')) {
        setFile(droppedFile);
        setError(null);
      } else {
        setError("Veuillez sélectionner un fichier JSON valide.");
      }
    }
  };

 const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
  e.preventDefault();

  if (!file) {
    setError("Veuillez sélectionner un fichier JSON.");
    return;
  }

  setLoading(true);
  setError(null);

  const reader = new FileReader();
  reader.onload = function (event) {
    try {
      const text = event.target?.result as string;
      const jsonData = JSON.parse(text);
      // 🔥 Appelle l'API avec l'objet JSON
      postCoverageRequest(jsonData)
        .then((data) => {
          setResult(data);
          
        })
        .catch((error) => {
          console.error("Erreur :", error);
          setError("Une erreur est survenue pendant l'analyse. Veuillez réessayer.");
        })
        .finally(() => {
          setLoading(false);
        });
    } catch (err) {
      console.error("Erreur de parsing JSON :", err);
      setError("Le fichier n'est pas un JSON valide.");
      setLoading(false);
    }
  };
  reader.readAsText(file);
};

  const removeFile = () => {
    setFile(null);
    setError(null);
  };


  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Radio className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">COUVERTURE RESEAU</h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-6 py-8">
        <div className="space-y-8">
          
          {/* Upload Section */}
          <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
            <div className="p-6 border-b border-gray-100">
              <h2 className="text-lg font-semibold text-gray-800 flex items-center space-x-2">
                <Upload className="w-5 h-5 text-blue-600" />
                <span>Importer un fichier</span>
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Sélectionnez ou glissez-déposez un fichier JSON contenant les adresses à analyser
              </p>
            </div>

            <form onSubmit={handleSubmit} className="p-6 space-y-6">
              {/* Drop Zone */}
              <div
                className={`relative border-2 border-dashed rounded-lg p-8 text-center transition-all duration-200 ${
                  dragActive
                    ? 'border-blue-500 bg-blue-50'
                    : file
                    ? 'border-green-300 bg-green-50'
                    : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
              >
                <input
                  type="file"
                  accept=".json"
                  onChange={handleFileChange}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  id="file-upload"
                />
                
                {!file ? (
                  <div className="space-y-4">
                    <div className="flex justify-center">
                      <div className="p-3 bg-gray-100 rounded-full">
                        <Upload className="w-8 h-8 text-gray-400" />
                      </div>
                    </div>
                    <div>
                      <p className="text-lg font-medium text-gray-700">
                        Glissez-déposez votre fichier JSON ici
                      </p>
                      <p className="text-sm text-gray-500 mt-1">
                        ou <span className="text-blue-600 font-medium">cliquez pour sélectionner</span>
                      </p>
                    </div>
                    <div className="text-xs text-gray-400">
                      Formats acceptés: .json • Taille max: 10MB
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="flex justify-center">
                      <div className="p-3 bg-green-100 rounded-full">
                        <CheckCircle className="w-8 h-8 text-green-600" />
                      </div>
                    </div>
                    <div>
                      <p className="text-lg font-medium text-green-700">Fichier sélectionné</p>
                      <div className="mt-2 p-3 bg-white rounded-lg border border-green-200">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-3">
                            <FileText className="w-5 h-5 text-green-600" />
                            <div>
                              <p className="font-medium text-gray-800">{file.name}</p>
                              <p className="text-sm text-gray-500">{formatFileSize(file.size)}</p>
                            </div>
                          </div>
                          <button
                            type="button"
                            onClick={removeFile}
                            className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                          >
                            <X className="w-4 h-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Error Message */}
              {error && (
                <div className="flex items-start space-x-3 p-4 bg-red-50 border border-red-200 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm font-medium text-red-800">Erreur</p>
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                </div>
              )}

              {/* Submit Button */}
              <div className="flex justify-center">
                <button
                  type="submit"
                  disabled={!file || loading}
                  className={`flex items-center space-x-2 px-8 py-3 rounded-lg font-semibold transition-all duration-200 ${
                    !file || loading
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
                      : 'bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg transform hover:-translate-y-0.5'
                  }`}
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 animate-spin" />
                      <span>Analyse en cours...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-5 h-5" />
                      <span>Analyser la couverture</span>
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>

          {/*  Section  Resultats */}
          {result && (
            <div className="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
              <div className="p-6 border-b border-gray-100">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <CheckCircle className="w-5 h-5 text-green-600" />
                    <h2 className="text-lg font-semibold text-gray-800">Résultats de l'analyse</h2>
                  </div>
                </div>
                
                <p className="text-sm text-gray-600 mt-1">
                  Analyse terminée avec succès : {Object.keys(result).length} adresse(s) traitée(s)
                </p>
              </div>

              <div className="p-6">
                {/* JSON Display */}
                <div className="space-y-4">
                  <h3 className="font-medium text-gray-800">Données détaillées :</h3>
                  <div className="bg-gray-900 rounded-lg overflow-hidden">
                    <div className="p-4 border-b border-gray-700">
                      <div className="flex items-center space-x-2">
                        <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                        <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                        <span className="text-sm text-gray-400 ml-2">results.json</span>
                      </div>
                    </div>
                    <pre className="p-6 text-sm text-green-400 font-mono overflow-x-auto max-h-96 overflow-y-auto">
                      {JSON.stringify(result, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>


    </div>
  );
}