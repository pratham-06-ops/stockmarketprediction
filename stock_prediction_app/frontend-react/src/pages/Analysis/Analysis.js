import React, { useState } from 'react';
import { Search, TrendingUp, TrendingDown, Target, Brain, AlertCircle } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ComposedChart, Bar } from 'recharts';

// Mock prediction data
const predictionData = [
  { date: '2024-01-01', actual: 150, predicted: 148, confidence: 0.85 },
  { date: '2024-01-02', actual: 152, predicted: 154, confidence: 0.78 },
  { date: '2024-01-03', actual: 148, predicted: 149, confidence: 0.82 },
  { date: '2024-01-04', actual: 155, predicted: 153, confidence: 0.88 },
  { date: '2024-01-05', actual: 153, predicted: 156, confidence: 0.75 },
  { date: '2024-01-06', actual: null, predicted: 158, confidence: 0.73 },
  { date: '2024-01-07', actual: null, predicted: 160, confidence: 0.71 },
];

const technicalIndicators = [
  { name: 'RSI', value: 65.4, signal: 'Neutral', color: 'text-yellow-600' },
  { name: 'MACD', value: 2.34, signal: 'Bullish', color: 'text-success-500' },
  { name: 'Moving Average (50)', value: 152.8, signal: 'Bullish', color: 'text-success-500' },
  { name: 'Bollinger Bands', value: 'Upper', signal: 'Overbought', color: 'text-danger-500' },
];

const Analysis = () => {
  const [selectedStock, setSelectedStock] = useState('AAPL');
  const [analysisType, setAnalysisType] = useState('prediction');

  return (
    <div className="pt-16 space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Stock Analysis</h1>
          <p className="text-gray-600">AI-powered predictions and technical analysis</p>
        </div>
        
        {/* Stock Search */}
        <div className="mt-4 lg:mt-0">
          <div className="relative">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <input
              type="text"
              placeholder="Search stocks (e.g., AAPL)"
              value={selectedStock}
              onChange={(e) => setSelectedStock(e.target.value)}
              className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            />
          </div>
        </div>
      </div>

      {/* Analysis Type Selector */}
      <div className="flex space-x-4">
        {[
          { id: 'prediction', label: 'AI Predictions', icon: Brain },
          { id: 'technical', label: 'Technical Analysis', icon: TrendingUp },
          { id: 'sentiment', label: 'Market Sentiment', icon: Target },
        ].map((type) => (
          <button
            key={type.id}
            onClick={() => setAnalysisType(type.id)}
            className={`flex items-center px-4 py-2 rounded-lg font-medium transition-colors duration-200 ${
              analysisType === type.id
                ? 'bg-primary-600 text-white'
                : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-200'
            }`}
          >
            <type.icon className="h-4 w-4 mr-2" />
            {type.label}
          </button>
        ))}
      </div>

      {/* Stock Overview Card */}
      <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h2 className="text-xl font-bold text-gray-900">{selectedStock}</h2>
            <p className="text-gray-600">Apple Inc.</p>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold text-gray-900">$175.25</div>
            <div className="flex items-center text-success-500">
              <TrendingUp className="h-4 w-4 mr-1" />
              <span>+2.45 (+1.42%)</span>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600">Open</div>
            <div className="font-semibold text-gray-900">$172.80</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600">High</div>
            <div className="font-semibold text-gray-900">$176.95</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600">Low</div>
            <div className="font-semibold text-gray-900">$172.15</div>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <div className="text-sm text-gray-600">Volume</div>
            <div className="font-semibold text-gray-900">2.4M</div>
          </div>
        </div>
      </div>

      {/* Main Analysis Content */}
      {analysisType === 'prediction' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Prediction Chart */}
          <div className="lg:col-span-2 bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-gray-900">AI Price Predictions</h3>
              <div className="flex items-center space-x-2">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-primary-600 rounded-full mr-2"></div>
                  <span className="text-sm text-gray-600">Actual</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-success-500 rounded-full mr-2"></div>
                  <span className="text-sm text-gray-600">Predicted</span>
                </div>
              </div>
            </div>
            
            <ResponsiveContainer width="100%" height={400}>
              <ComposedChart data={predictionData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="date" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  connectNulls={false}
                  dot={{ fill: '#3b82f6', strokeWidth: 2, r: 4 }}
                />
                <Line 
                  type="monotone" 
                  dataKey="predicted" 
                  stroke="#10b981" 
                  strokeWidth={2}
                  strokeDasharray="5 5"
                  dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
                />
                <Bar dataKey="confidence" fill="#e5e7eb" opacity={0.3} />
              </ComposedChart>
            </ResponsiveContainer>
          </div>

          {/* Prediction Summary */}
          <div className="space-y-6">
            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Prediction Summary</h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Next Day</span>
                  <div className="text-right">
                    <div className="font-semibold text-success-500">$158.00</div>
                    <div className="text-sm text-gray-500">73% confidence</div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Next Week</span>
                  <div className="text-right">
                    <div className="font-semibold text-success-500">$162.50</div>
                    <div className="text-sm text-gray-500">68% confidence</div>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Next Month</span>
                  <div className="text-right">
                    <div className="font-semibold text-primary-600">$168.00</div>
                    <div className="text-sm text-gray-500">61% confidence</div>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Insights</h3>
              
              <div className="space-y-3">
                <div className="p-3 bg-success-50 rounded-lg border border-success-200">
                  <div className="flex items-start">
                    <TrendingUp className="h-4 w-4 text-success-500 mt-0.5 mr-2" />
                    <div className="text-sm text-success-700">
                      Strong upward momentum detected in recent trading patterns.
                    </div>
                  </div>
                </div>
                
                <div className="p-3 bg-yellow-50 rounded-lg border border-yellow-200">
                  <div className="flex items-start">
                    <AlertCircle className="h-4 w-4 text-yellow-500 mt-0.5 mr-2" />
                    <div className="text-sm text-yellow-700">
                      High volatility expected due to upcoming earnings report.
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {analysisType === 'technical' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Technical Indicators */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Technical Indicators</h3>
            
            <div className="space-y-4">
              {technicalIndicators.map((indicator, index) => (
                <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div>
                    <div className="font-medium text-gray-900">{indicator.name}</div>
                    <div className="text-sm text-gray-600">Value: {indicator.value}</div>
                  </div>
                  <div className={`font-semibold ${indicator.color}`}>
                    {indicator.signal}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Support & Resistance */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Support & Resistance</h3>
            
            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Resistance Levels</span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">R3</span>
                    <span className="font-medium text-danger-500">$180.25</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">R2</span>
                    <span className="font-medium text-danger-500">$178.50</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">R1</span>
                    <span className="font-medium text-danger-500">$177.00</span>
                  </div>
                </div>
              </div>
              
              <div className="border-t pt-4">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Support Levels</span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600">S1</span>
                    <span className="font-medium text-success-500">$172.80</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">S2</span>
                    <span className="font-medium text-success-500">$170.25</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-600">S3</span>
                    <span className="font-medium text-success-500">$168.50</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {analysisType === 'sentiment' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Market Sentiment */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">Market Sentiment</h3>
            
            <div className="text-center mb-6">
              <div className="text-4xl font-bold text-success-500 mb-2">Bullish</div>
              <div className="text-gray-600">Overall market sentiment</div>
            </div>
            
            <div className="grid grid-cols-3 gap-4 text-center">
              <div className="p-3 bg-success-50 rounded-lg">
                <div className="text-2xl font-bold text-success-500">68%</div>
                <div className="text-sm text-gray-600">Bullish</div>
              </div>
              <div className="p-3 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-gray-500">22%</div>
                <div className="text-sm text-gray-600">Neutral</div>
              </div>
              <div className="p-3 bg-danger-50 rounded-lg">
                <div className="text-2xl font-bold text-danger-500">10%</div>
                <div className="text-sm text-gray-600">Bearish</div>
              </div>
            </div>
          </div>

          {/* News Sentiment */}
          <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">News Sentiment Analysis</h3>
            
            <div className="space-y-4">
              <div className="p-4 border-l-4 border-success-500 bg-success-50">
                <div className="font-medium text-success-700">Positive News</div>
                <div className="text-sm text-success-600 mt-1">
                  Strong quarterly earnings report released
                </div>
              </div>
              
              <div className="p-4 border-l-4 border-primary-500 bg-primary-50">
                <div className="font-medium text-primary-700">Neutral News</div>
                <div className="text-sm text-primary-600 mt-1">
                  Market analysts maintain price targets
                </div>
              </div>
              
              <div className="p-4 border-l-4 border-yellow-500 bg-yellow-50">
                <div className="font-medium text-yellow-700">Market Watch</div>
                <div className="text-sm text-yellow-600 mt-1">
                  Federal Reserve meeting scheduled next week
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analysis;