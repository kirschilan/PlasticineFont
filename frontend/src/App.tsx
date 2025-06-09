const API_BASE = import.meta.env.VITE_API_BASE || "";
import React, { useState, useCallback } from 'react';
import { Download, Type, Palette, Space, Loader2, AlertCircle, Sparkles } from 'lucide-react';

interface GenerationState {
  loading: boolean;
  error: string | null;
  imageUrl: string | null;
}

function App() {
  const [text, setText] = useState('Hello World');
  const [color, setColor] = useState('#EE6B47');
  const [spacing, setSpacing] = useState(2);
  const [generationState, setGenerationState] = useState<GenerationState>({
    loading: false,
    error: null,
    imageUrl: null
  });

  // Convert hex to RGB
  const hexToRgb = useCallback((hex: string): string => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    if (!result) return '238,174,104'; // fallback
    
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
        color: rgbColor
      });

      const response = await fetch(`${API_BASE}/api/render?${params}`);
      
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
  }, [text, color, spacing, hexToRgb]);

  const downloadImage = useCallback(() => {
    if (!generationState.imageUrl) return;

    const link = document.createElement('a');
    link.href = generationState.imageUrl;
    link.download = `plasticine-${text.replace(/\s+/g, '-').toLowerCase()}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }, [generationState.imageUrl, text]);

  const presetColors = ['#EE6B47', '#6366F1', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6', '#06B6D4', '#F97316'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-400 via-pink-400 to-red-400 p-4">
      <div className="container mx-auto max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8 pt-8">
          <div className="inline-flex items-center gap-3 mb-4">
            <div className="p-3 bg-white/20 backdrop-blur-sm rounded-2xl">
              <Sparkles className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-white">
              Plasticine Font Generator
            </h1>
          </div>
          <p className="text-white/80 text-lg max-w-2xl mx-auto">
            Transform your text into beautiful, colorful plasticine-style typography with customizable colors and spacing.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Controls Panel */}
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 md:p-8 border border-white/20 shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-2">
              <Type className="w-6 h-6" />
              Customize Your Text
            </h2>

            <div className="space-y-6">
              {/* Text Input */}
              <div>
                <label htmlFor="text-input" className="block text-white font-medium mb-2">
                  Your Text
                </label>
                <input
                  id="text-input"
                  type="text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  placeholder="Enter your text here..."
                  className="w-full px-4 py-3 bg-white/20 border border-white/30 rounded-xl text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 focus:border-transparent transition-all duration-200"
                  maxLength={50}
                />
                <div className="text-white/60 text-sm mt-1">
                  {text.length}/50 characters
                </div>
              </div>

              {/* Color Picker */}
              <div>
                <label htmlFor="color-input" className="block text-white font-medium mb-2 flex items-center gap-2">
                  <Palette className="w-4 h-4" />
                  Text Color
                </label>
                <div className="space-y-3">
                  <div className="flex items-center gap-3">
                    <input
                      id="color-input"
                      type="color"
                      value={color}
                      onChange={(e) => setColor(e.target.value)}
                      className="w-12 h-12 rounded-lg border-2 border-white/30 cursor-pointer"
                    />
                    <input
                      type="text"
                      value={color}
                      onChange={(e) => setColor(e.target.value)}
                      className="flex-1 px-3 py-2 bg-white/20 border border-white/30 rounded-lg text-white placeholder-white/60 focus:outline-none focus:ring-2 focus:ring-white/50 text-sm"
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
                            ? 'border-white scale-110' 
                            : 'border-white/30 hover:border-white/60 hover:scale-105'
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
                <label htmlFor="spacing-input" className="block text-white font-medium mb-2 flex items-center gap-2">
                  <Space className="w-4 h-4" />
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
                    className="w-full h-2 bg-white/20 rounded-lg appearance-none cursor-pointer slider"
                  />
                  <div className="flex justify-between text-white/60 text-sm">
                    <span>Tight</span>
                    <span className="font-medium text-white">{spacing}px</span>
                    <span>Wide</span>
                  </div>
                </div>
              </div>

              {/* Generate Button */}
              <button
                onClick={generateImage}
                disabled={generationState.loading || !text.trim()}
                className="w-full py-4 bg-gradient-to-r from-orange-400 to-pink-400 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center gap-2"
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
                <div className="bg-red-500/20 border border-red-400/30 rounded-xl p-4 flex items-center gap-3">
                  <AlertCircle className="w-5 h-5 text-red-300 flex-shrink-0" />
                  <p className="text-red-100">{generationState.error}</p>
                </div>
              )}
            </div>
          </div>

          {/* Preview Panel */}
          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-6 md:p-8 border border-white/20 shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-6">
              Preview
            </h2>

            <div className="bg-white/5 rounded-2xl p-6 min-h-[300px] flex items-center justify-center">
              {generationState.loading ? (
                <div className="text-center">
                  <Loader2 className="w-12 h-12 text-white animate-spin mx-auto mb-4" />
                  <p className="text-white/80">Creating your plasticine text...</p>
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
                    className="inline-flex items-center gap-2 px-6 py-3 bg-green-500 hover:bg-green-600 text-white font-medium rounded-lg transition-colors duration-200"
                  >
                    <Download className="w-4 h-4" />
                    Download Image
                  </button>
                </div>
              ) : (
                <div className="text-center text-white/60">
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
          <p className="text-white/60 text-sm">
            Create beautiful plasticine-style text with custom colors and spacing
          </p>
        </div>
      </div>

      <style>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          width: 20px;
          height: 20px;
          background: white;
          border-radius: 50%;
          cursor: pointer;
          box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
        
        .slider::-moz-range-thumb {
          width: 20px;
          height: 20px;
          background: white;
          border-radius: 50%;
          cursor: pointer;
          border: none;
          box-shadow: 0 2px 8px rgba(0,0,0,0.2);
        }
      `}</style>
    </div>
  );
}

export default App;