import React, { useState, useEffect } from 'react';
import { TrendingUp, TrendingDown, DollarSign, Activity, ArrowUpRight, ArrowDownRight } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

// Mock data for demonstration
const stockData = [
  { time: '9:00', price: 150, volume: 1200 },
  { time: '10:00', price: 152, volume: 1400 },
  { time: '11:00', price: 148, volume: 1100 },
  { time: '12:00', price: 155, volume: 1600 },
  { time: '1:00', price: 153, volume: 1300 },
  { time: '2:00', price: 158, volume: 1800 },
  { time: '3:00', price: 160, volume: 2000 },
];

const watchlistStocks = [
  { symbol: 'AAPL', name: 'Apple Inc.', price: 175.25, change: 2.45, changePercent: 1.42 },
  { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 2847.63, change: -15.32, changePercent: -0.53 },
  { symbol: 'MSFT', name: 'Microsoft Corp.', price: 338.92, change: 4.17, changePercent: 1.25 },
  { symbol: 'TSLA', name: 'Tesla Inc.', price: 242.86, change: -8.14, changePercent: -3.24 },
  { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 127.45, change: 1.23, changePercent: 0.97 },
];

const Dashboard = () => {
  const [selectedTimeframe, setSelectedTimeframe] = useState('1D');
  
  return (
    <div className="pt-16 space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-600">Monitor your investments and market trends</p>
        </div>
        <div className="mt-4 lg:mt-0">
          <div className="flex space-x-2">
            {['1D', '1W', '1M', '3M', '1Y'].map((timeframe) => (
              <button
                key={timeframe}
                onClick={() => setSelectedTimeframe(timeframe)}
                className={`px-3 py-1 text-sm font-medium rounded-md transition-colors duration-200 ${
                  selectedTimeframe === timeframe
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {timeframe}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Portfolio Value</p>
              <p className="text-2xl font-bold text-gray-900">$125,430</p>
              <div className="flex items-center mt-2">
                <ArrowUpRight className="h-4 w-4 text-success-500" />
                <span className="text-sm text-success-500 ml-1">+2.4% today</span>
              </div>
            </div>
            <div className="p-3 bg-primary-100 rounded-lg">
              <DollarSign className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Day's Gain/Loss</p>
              <p className="text-2xl font-bold text-success-500">+$2,845</p>
              <div className="flex items-center mt-2">
                <TrendingUp className="h-4 w-4 text-success-500" />
                <span className="text-sm text-success-500 ml-1">+2.32%</span>
              </div>
            </div>
            <div className="p-3 bg-success-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-success-500" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Active Positions</p>
              <p className="text-2xl font-bold text-gray-900">12</p>
              <div className="flex items-center mt-2">
                <Activity className="h-4 w-4 text-primary-500" />
                <span className="text-sm text-gray-500 ml-1">8 profitable</span>
              </div>
            </div>
            <div className="p-3 bg-primary-100 rounded-lg">
              <Activity className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Accuracy Rate</p>
              <p className="text-2xl font-bold text-gray-900">87.5%</p>
              <div className="flex items-center mt-2">
                <ArrowUpRight className="h-4 w-4 text-success-500" />
                <span className="text-sm text-success-500 ml-1">+1.2% this week</span>
              </div>
            </div>
            <div className="p-3 bg-success-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-success-500" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Performance Chart */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Portfolio Performance</h2>
            <span className="text-sm text-gray-500">Last 7 days</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={stockData}>
              <defs>
                <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2}/>
                  <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="time" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip />
              <Area 
                type="monotone" 
                dataKey="price" 
                stroke="#3b82f6" 
                fillOpacity={1} 
                fill="url(#colorPrice)" 
                strokeWidth={2}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        {/* Trading Volume Chart */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Trading Volume</h2>
            <span className="text-sm text-gray-500">Today</span>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={stockData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="time" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="volume" 
                stroke="#10b981" 
                strokeWidth={2}
                dot={{ fill: '#10b981', strokeWidth: 2, r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Watchlist */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Watchlist</h2>
        </div>
        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="text-left text-sm font-medium text-gray-500">
                  <th className="pb-3">Symbol</th>
                  <th className="pb-3">Company</th>
                  <th className="pb-3 text-right">Price</th>
                  <th className="pb-3 text-right">Change</th>
                  <th className="pb-3 text-right">% Change</th>
                </tr>
              </thead>
              <tbody className="space-y-2">
                {watchlistStocks.map((stock, index) => (
                  <tr key={stock.symbol} className="border-t border-gray-100">
                    <td className="py-3">
                      <div className="font-medium text-gray-900">{stock.symbol}</div>
                    </td>
                    <td className="py-3">
                      <div className="text-gray-600">{stock.name}</div>
                    </td>
                    <td className="py-3 text-right">
                      <div className="font-medium text-gray-900">${stock.price.toFixed(2)}</div>
                    </td>
                    <td className="py-3 text-right">
                      <div className={`flex items-center justify-end ${
                        stock.change >= 0 ? 'text-success-500' : 'text-danger-500'
                      }`}>
                        {stock.change >= 0 ? (
                          <ArrowUpRight className="h-4 w-4 mr-1" />
                        ) : (
                          <ArrowDownRight className="h-4 w-4 mr-1" />
                        )}
                        ${Math.abs(stock.change).toFixed(2)}
                      </div>
                    </td>
                    <td className="py-3 text-right">
                      <div className={`font-medium ${
                        stock.changePercent >= 0 ? 'text-success-500' : 'text-danger-500'
                      }`}>
                        {stock.changePercent >= 0 ? '+' : ''}{stock.changePercent.toFixed(2)}%
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;