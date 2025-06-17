import React, { useState, useCallback } from 'react';
import { Download, Type, Palette, Space, Loader2, AlertCircle, Sparkles, Maximize2 } from 'lucide-react';

interface GenerationState {
  loading: boolean;
  error: string | null;
  imageUrl: string | null;
}

function App() {
  const [text, setText] = useState('Hello World');
  const [color, setColor] = useState('#FF9300');
  const [spacing, setSpacing] = useState(2);
  const [fontSize, setFontSize] = useState(48);
  const [generationState, setGenerationState] = useState<GenerationState>({
    loading: false,
    error: null,
    imageUrl: null
  });

  // Convert hex to RGB
  const hexToRgb = useCallback((hex: string): string => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!result) return '255,147,0'; // fallback to Dr Agile orange
    
    return [
      parseInt(result[1], 16),
      parseInt(result[2], 16),
      parseInt(result[3], 16)
    ].join(',');
  }, []);

  const generateImage = useCallback(async () => {
    if (!text.trim()) {
      setGenerationState({ loading: false, error: 'Please enter some text', imageUrl: null });
      return;
    }

    setGenerationState({ loading: true, error: null, imageUrl: null });

    try {
      const rgbColor = hexToRgb(color);
      const params = new URLSearchParams({
        text: text.trim(),
        spacing: spacing.toString(),
        color: rgbColor,
        size: fontSize.toString()
      });

      const response = await fetch(`/api/render?${params}`);
      
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }

      const blob = await response.blob();
      const imageUrl = URL.createObjectURL(blob);
      
      setGenerationState({ loading: false, error: null, imageUrl });
    } catch (error) {
      setGenerationState({ 
        loading: false, 
        error: error instanceof Error ? error.message : 'Failed to generate image', 
        imageUrl: null 
      });
    }
  }, [text, color, spacing, fontSize, hexToRgb]);

  const downloadImage = useCallback(() => {
    if (!generationState.imageUrl) return;

    const link = document.createElement('a');
    link.href = generationState.imageUrl;
    link.download = `plasticine-${text.replace(/\s+/g, '-').toLowerCase()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, [generationState.imageUrl, text]);

  const presetColors = ['#FF9300', '#555555', '#EE6B47', '#6366F1', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-gray-50 to-orange-100 p-4">
      <div className="container mx-auto max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <div className="inline-flex items-center gap-4 mb-6">
            <div className="p-3 bg-white rounded-2xl shadow-lg border border-orange-100">
              <img 
                src="/dr-agile-logo.svg" 
                alt="Dr Agile" 
                className="w-16 h-8 object-contain"
              />
            </div>
            <div className="text-left">
              <h1 className="text-4xl md:text-5xl font-bold text-gray-800 leading-tight">
                Plasticine Font Generator
              </h1>
              <div className="w-24 h-1 bg-gradient-to-r from-orange-400 to-orange-600 rounded-full mt-2"></div>
            </div>
          </div>
          <p className="text-gray-600 text-lg max-w-2xl mx-auto">
            Transform your text into beautiful, colorful plasticine-style typography with customizable colors, spacing, and size.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Controls Panel */}
          <div className="bg-white rounded-3xl p-6 md:p-8 border border-gray-200 shadow-xl">
            <h2 className="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
              <Type className="w-6 h-6 text-orange-500" />
              Customize Your Text
            </h2>

            <div className="space-y-6">
              {/* Text Input */}
              <div>
                <label htmlFor="text-input" className="block text-gray-700 font-medium mb-2">
                  Your Text
                </label>
                <input
                  id="text-input"
                  type="text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Enter your text here..."
                  className="w-full px-4 py-3 bg-gray-50 border border-gray-200 rounded-xl text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-transparent transition-all duration-200"
                  maxLength={50}
                />
                <div className="text-gray-500 text-sm mt-1">
                  {text.length}/50 characters
                </div>
              </div>

              {/* Font Size */}
              <div>
                <label htmlFor="size-input" className="block text-gray-700 font-medium mb-2 flex items-center gap-2">
                  <Maximize2 className="w-4 h-4 text-orange-500" />
                  Font Size
                </label>
                <div className="space-y-2">
                  <input
                    id="size-input"
                    type="range"
                    min="16"
                    max="128"
                    value={fontSize}
                    onChange={(e) => setFontSize(parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                  <div className="flex justify-between text-gray-500 text-sm">
                    <span>Small</span>
                    <span className="font-medium text-orange-600">{fontSize}px</span>
                    <span>Large</span>
                  </div>
                </div>
              </div>

              {/* Color Picker */}
              <div>
                <label htmlFor="color-input" className="block text-gray-700 font-medium mb-2 flex items-center gap-2">
                  <Palette className="w-4 h-4 text-orange-500" />
                  Text Color
                </label>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <input
                      id="color-input"
                      type="color"
                      value={color}
                      onChange={(e) => setColor(e.target.value)}
                      className="w-12 h-12 rounded-lg border-2 border-gray-200 cursor-pointer"
                    />
                    <input
                      type="text"
                      value={color}
                      onChange={(e) => setColor(e.target.value)}
                      className="flex-1 px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg text-gray-800 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-orange-400 text-sm"
                      placeholder="#FFFFFF"
                    />
                  </div>
                  
                  {/* Color Presets */}
                  <div className="flex flex-wrap gap-2">
                    {presetColors.map((presetColor) => (
                      <button
                        key={presetColor}
                        onClick={() => setColor(presetColor)}
                        className={`w-8 h-8 rounded-lg border-2 transition-all duration-200 ${
                          color === presetColor 
                            ? 'border-orange-500 scale-110 shadow-lg' 
                            : 'border-gray-200 hover:border-orange-300 hover:scale-105'
                        }`}
                        style={{ backgroundColor: presetColor }}
                        title={presetColor}
                      />
                    ))}
                  </div>
                </div>
              </div>

              {/* Letter Spacing */}
              <div>
                <label htmlFor="spacing-input" className="block text-gray-700 font-medium mb-2 flex items-center gap-2">
                  <Space className="w-4 h-4 text-orange-500" />
                  Letter Spacing
                </label>
                <div className="space-y-2">
                  <input
                    id="spacing-input"
                    type="range"
                    min="0"
                    max="10"
                    value={spacing}
                    onChange={(e) => setSpacing(parseInt(e.target.value))}
                    className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
                  />
                  <div className="flex justify-between text-gray-500 text-sm">
                    <span>Tight</span>
                    <span className="font-medium text-orange-600">{spacing}px</span>
                    <span>Wide</span>
                  </div>
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateImage}
                disabled={generationState.loading || !text.trim()}
                className="w-full py-4 bg-gradient-to-r from-orange-400 to-orange-600 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
              >
                {generationState.loading ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Generating...
                  </>
                ) : (
                  <>
                    <Sparkles className="w-5 h-5" />
                    Generate Plasticine Text
                  </>
                )}
              </button>

              {/* Error Display */}
              {generationState.error && (
                <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-center gap-3">
                  <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                  <p className="text-red-700">{generationState.error}</p>
                </div>
              )}
            </div>
          </div>

          {/* Preview Panel */}
          <div className="bg-white rounded-3xl p-6 md:p-8 border border-gray-200 shadow-xl">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Preview
            </h2>

            <div className="bg-gray-50 rounded-2xl p-6 min-h-[300px] flex items-center justify-center border border-gray-100">
              {generationState.loading ? (
                <div className="text-center">
                  <Loader2 className="w-12 h-12 text-orange-500 animate-spin mx-auto mb-4" />
                  <p className="text-gray-600">Creating your plasticine text...</p>
                </div>
              ) : generationState.imageUrl ? (
                <div className="text-center space-y-4">
                  <img
                    src={generationState.imageUrl}
                    alt="Generated plasticine text"
                    className="max-w-full h-auto rounded-lg shadow-lg"
                  />
                  <button
                    onClick={downloadImage}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-medium rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
                  >
                    <Download className="w-4 h-4" />
                    Download Image
                  </button>
                </div>
              ) : (
                <div className="text-center text-gray-500">
                  <Type className="w-16 h-16 mx-auto mb-4 opacity-50" />
                  <p>Your generated plasticine text will appear here</p>
                  <p className="text-sm mt-2">Enter some text and click "Generate" to get started</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center mt-12 pb-8">
          <div className="flex items-center justify-center gap-2 mb-2">
            <span className="text-gray-500 text-sm">Powered by</span>
            <img 
              src="/dr-agile-logo.svg" 
              alt="Dr Agile" 
              className="w-12 h-6 object-contain opacity-75"
            />
          </div>
          <p className="text-gray-500 text-sm">
            Create beautiful plasticine-style text with custom colors, spacing, and size
          </p>
        </div>
      </div>

      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          background: linear-gradient(135deg, #FF9300, #FF7A00);
          border-radius: 50%;
          cursor: pointer;
          box-shadow: 0 2px 8px rgba(255, 147, 0, 0.3);
          border: 2px solid white;
        }
        
        .slider::-moz-range-thumb {
          width: 20px;
          height: 20px;
          background: linear-gradient(135deg, #FF9300, #FF7A00);
          border-radius: 50%;
          cursor: pointer;
          border: 2px solid white;
          box-shadow: 0 2px 8px rgba(255, 147, 0, 0.3);
        }
      `}</style>
    </div>
  );
}

export default App;