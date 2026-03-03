import { useState } from "react";
import axios from "axios";

interface Configuracion {
  items_total_variable1: string;
  items_total_variable2: string;
  explorar_dimensiones_de_v1: boolean;
  cantidad_item_por_dimensiones: string;
  numero_maximo_de_escala: string;
}

function App() {
  const [config, setConfig] = useState<Configuracion>({
    items_total_variable1: "",
    items_total_variable2: "",
    explorar_dimensiones_de_v1: true,
    cantidad_item_por_dimensiones: "5,5,5",
    numero_maximo_de_escala: "5",
  });

  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);

  const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfig({
      ...config,
      [e.target.name]: e.target.value,
    });
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfig({
      ...config,
      explorar_dimensiones_de_v1: e.target.checked,
    });
  };

  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setConfig({
      ...config,
      cantidad_item_por_dimensiones: e.target.value,
    });
  };

  const handleSubmit = async () => {
    if (!file) {
      alert("Selecciona un archivo Excel");
      return;
    }

    try {
      setLoading(true);

      const payload = {
        items_total_variable1: Number(config.items_total_variable1),
        items_total_variable2: Number(config.items_total_variable2),
        explorar_dimensiones_de_v1: config.explorar_dimensiones_de_v1,
        cantidad_item_por_dimensiones:
          config.cantidad_item_por_dimensiones
            .split(",")
            .map((n) => Number(n.trim())),
        numero_maximo_de_escala: Number(config.numero_maximo_de_escala),
      };

      const formData = new FormData();
      formData.append("file", file);
      formData.append("config", JSON.stringify(payload));

      const response = await axios.post(
        "http://localhost:8000/procesar",
        formData,
        { responseType: "blob" }
      );

      const blob = new Blob([response.data], { type: "text/csv" });
      const url = window.URL.createObjectURL(blob);

      const link = document.createElement("a");
      link.href = url;
      link.download = "resultado.csv";
      link.click();

      window.URL.revokeObjectURL(url);

    } catch (error) {
      console.error(error);
      alert("Error procesando archivo");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="bg-white shadow-xl rounded-2xl p-8 w-full max-w-xl space-y-6">

        <div className="flex justify-between items-center">
          <h2 className="text-2xl font-bold text-gray-800">
            Procesar Excel
          </h2>

          <a
            href="https://youtube.com"
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-blue-600 hover:underline"
          >
            Ver guía en video
          </a>
        </div>

        <div className="space-y-4">

          <div>
            <label className="block text-sm font-medium text-gray-600">
              Items total variable 1
            </label>
            <input
              type="number"
              name="items_total_variable1"
              value={config.items_total_variable1}
              onChange={handleNumberChange}
              className="mt-1 w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600">
              Items total variable 2
            </label>
            <input
              type="number"
              name="items_total_variable2"
              value={config.items_total_variable2}
              onChange={handleNumberChange}
              className="mt-1 w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              checked={config.explorar_dimensiones_de_v1}
              onChange={handleCheckboxChange}
              className="h-4 w-4"
            />
            <label className="text-sm text-gray-700">
              Explorar dimensiones v1
            </label>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600">
              Cantidad item por dimensiones (ej: 3,3,2)
            </label>
            <input
              type="text"
              value={config.cantidad_item_por_dimensiones}
              onChange={handleTextChange}
              className="mt-1 w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600">
              Número máximo de escala
            </label>
            <input
              type="number"
              name="numero_maximo_de_escala"
              value={config.numero_maximo_de_escala}
              onChange={handleNumberChange}
              className="mt-1 w-full border rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          {/* 🔥 Mejor botón de archivo */}
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-2">
              Archivo Excel
            </label>

            <label className="flex items-center justify-center w-full px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-lg cursor-pointer transition">
              <span className="text-sm font-medium text-gray-700">
                {file ? file.name : "Seleccionar archivo"}
              </span>
              <input
                type="file"
                accept=".xlsx,.xls"
                className="hidden"
                onChange={(e) =>
                  setFile(e.target.files?.[0] || null)
                }
              />
            </label>
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-lg transition disabled:opacity-50"
          >
            {loading ? "Procesando..." : "Procesar"}
          </button>

        </div>
      </div>
    </div>
  );
}

export default App;