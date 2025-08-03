import React, { useState } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import { TrendingUp, TrendingDown, DollarSign, Plus, Minus, Filter } from 'lucide-react';

const portfolioData = [
  { name: 'AAPL', value: 35000, shares: 200, price: 175.25, change: 2.45, color: '#3b82f6' },
  { name: 'GOOGL', value: 28000, shares: 10, price: 2800.63, change: -15.32, color: '#10b981' },
  { name: 'MSFT', value: 20000, shares: 60, price: 333.92, change: 4.17, color: '#f59e0b' },
  { name: 'TSLA', value: 15000, shares: 62, price: 242.86, change: -8.14, color: '#ef4444' },
  { name: 'AMZN', value: 12000, shares: 95, price: 127.45, change: 1.23, color: '#8b5cf6' },
];

const performanceData = [
  { month: 'Jan', value: 85000 },
  { month: 'Feb', value: 88000 },
  { month: 'Mar', value: 92000 },
  { month: 'Apr', value: 89000 },
  { month: 'May', value: 95000 },
  { month: 'Jun', value: 110000 },
];

const transactions = [
  { id: 1, type: 'BUY', symbol: 'AAPL', shares: 50, price: 172.30, date: '2024-01-15', total: 8615 },
  { id: 2, type: 'SELL', symbol: 'GOOGL', shares: 5, price: 2850.00, date: '2024-01-14', total: 14250 },
  { id: 3, type: 'BUY', symbol: 'MSFT', shares: 30, price: 335.50, date: '2024-01-13', total: 10065 },
  { id: 4, type: 'BUY', symbol: 'TSLA', shares: 20, price: 245.75, date: '2024-01-12', total: 4915 },
  { id: 5, type: 'SELL', symbol: 'AMZN', shares: 15, price: 125.80, date: '2024-01-11', total: 1887 },
];

const Portfolio = () => {
  const [selectedTimeframe, setSelectedTimeframe] = useState('6M');
  const [showTransactions, setShowTransactions] = useState(false);

  const totalValue = portfolioData.reduce((sum, item) => sum + item.value, 0);
  const totalChange = portfolioData.reduce((sum, item) => sum + (item.change * item.shares), 0);
  const totalChangePercent = (totalChange / totalValue) * 100;

  return (
    <div className="pt-16 space-y-6">
      {/* Header */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Portfolio</h1>
          <p className="text-gray-600">Track your investments and performance</p>
        </div>
        
        <div className="flex space-x-2 mt-4 lg:mt-0">
          <button className="flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors duration-200">
            <Plus className="h-4 w-4 mr-2" />
            Add Position
          </button>
          <button 
            onClick={() => setShowTransactions(!showTransactions)}
            className="flex items-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors duration-200"
          >
            <Filter className="h-4 w-4 mr-2" />
            {showTransactions ? 'Hide' : 'Show'} Transactions
          </button>
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Total Portfolio Value</p>
              <p className="text-2xl font-bold text-gray-900">${totalValue.toLocaleString()}</p>
              <div className={`flex items-center mt-2 ${totalChange >= 0 ? 'text-success-500' : 'text-danger-500'}`}>
                {totalChange >= 0 ? <TrendingUp className="h-4 w-4 mr-1" /> : <TrendingDown className="h-4 w-4 mr-1" />}
                <span className="text-sm">
                  ${Math.abs(totalChange).toFixed(2)} ({totalChangePercent >= 0 ? '+' : ''}{totalChangePercent.toFixed(2)}%)
                </span>
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
              <p className={`text-2xl font-bold ${totalChange >= 0 ? 'text-success-500' : 'text-danger-500'}`}>
                ${totalChange >= 0 ? '+' : ''}${totalChange.toFixed(2)}
              </p>
              <div className="flex items-center mt-2 text-gray-500">
                <span className="text-sm">Based on current positions</span>
              </div>
            </div>
            <div className={`p-3 ${totalChange >= 0 ? 'bg-success-100' : 'bg-danger-100'} rounded-lg`}>
              {totalChange >= 0 ? 
                <TrendingUp className="h-6 w-6 text-success-500" /> : 
                <TrendingDown className="h-6 w-6 text-danger-500" />
              }
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Number of Holdings</p>
              <p className="text-2xl font-bold text-gray-900">{portfolioData.length}</p>
              <div className="flex items-center mt-2 text-gray-500">
                <span className="text-sm">Diversified across sectors</span>
              </div>
            </div>
            <div className="p-3 bg-primary-100 rounded-lg">
              <TrendingUp className="h-6 w-6 text-primary-600" />
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Portfolio Allocation */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Portfolio Allocation</h2>
          </div>
          
          <div className="flex items-center">
            <div className="w-1/2">
              <ResponsiveContainer width="100%" height={200}>
                <PieChart>
                  <Pie
                    data={portfolioData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={80}
                    paddingAngle={2}
                    dataKey="value"
                  >
                    {portfolioData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Value']} />
                </PieChart>
              </ResponsiveContainer>
            </div>
            
            <div className="w-1/2 pl-6">
              <div className="space-y-2">
                {portfolioData.map((item, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div 
                        className="w-3 h-3 rounded-full mr-2" 
                        style={{ backgroundColor: item.color }}
                      ></div>
                      <span className="text-sm font-medium text-gray-900">{item.name}</span>
                    </div>
                    <span className="text-sm text-gray-600">
                      {((item.value / totalValue) * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Performance Chart */}
        <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Performance</h2>
            <div className="flex space-x-2">
              {['1M', '3M', '6M', '1Y'].map((timeframe) => (
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
          
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={performanceData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
              <XAxis dataKey="month" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Portfolio Value']} />
              <Bar dataKey="value" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Holdings Table */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Current Holdings</h2>
        </div>
        <div className="p-6">
          <div className="overflow-x-auto">
            <table className="min-w-full">
              <thead>
                <tr className="text-left text-sm font-medium text-gray-500">
                  <th className="pb-3">Symbol</th>
                  <th className="pb-3 text-right">Shares</th>
                  <th className="pb-3 text-right">Current Price</th>
                  <th className="pb-3 text-right">Market Value</th>
                  <th className="pb-3 text-right">Day Change</th>
                  <th className="pb-3 text-right">% of Portfolio</th>
                </tr>
              </thead>
              <tbody>
                {portfolioData.map((holding, index) => (
                  <tr key={holding.name} className="border-t border-gray-100">
                    <td className="py-3">
                      <div className="font-medium text-gray-900">{holding.name}</div>
                    </td>
                    <td className="py-3 text-right">
                      <div className="text-gray-900">{holding.shares}</div>
                    </td>
                    <td className="py-3 text-right">
                      <div className="text-gray-900">${holding.price.toFixed(2)}</div>
                    </td>
                    <td className="py-3 text-right">
                      <div className="font-medium text-gray-900">${holding.value.toLocaleString()}</div>
                    </td>
                    <td className="py-3 text-right">
                      <div className={`font-medium ${
                        holding.change >= 0 ? 'text-success-500' : 'text-danger-500'
                      }`}>
                        {holding.change >= 0 ? '+' : ''}${(holding.change * holding.shares).toFixed(2)}
                      </div>
                    </td>
                    <td className="py-3 text-right">
                      <div className="text-gray-900">
                        {((holding.value / totalValue) * 100).toFixed(1)}%
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Transaction History */}
      {showTransactions && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-semibold text-gray-900">Recent Transactions</h2>
          </div>
          <div className="p-6">
            <div className="overflow-x-auto">
              <table className="min-w-full">
                <thead>
                  <tr className="text-left text-sm font-medium text-gray-500">
                    <th className="pb-3">Date</th>
                    <th className="pb-3">Type</th>
                    <th className="pb-3">Symbol</th>
                    <th className="pb-3 text-right">Shares</th>
                    <th className="pb-3 text-right">Price</th>
                    <th className="pb-3 text-right">Total</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map((transaction) => (
                    <tr key={transaction.id} className="border-t border-gray-100">
                      <td className="py-3">
                        <div className="text-gray-900">{transaction.date}</div>
                      </td>
                      <td className="py-3">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          transaction.type === 'BUY' 
                            ? 'bg-success-100 text-success-800' 
                            : 'bg-danger-100 text-danger-800'
                        }`}>
                          {transaction.type === 'BUY' ? <Plus className="h-3 w-3 mr-1" /> : <Minus className="h-3 w-3 mr-1" />}
                          {transaction.type}
                        </span>
                      </td>
                      <td className="py-3">
                        <div className="font-medium text-gray-900">{transaction.symbol}</div>
                      </td>
                      <td className="py-3 text-right">
                        <div className="text-gray-900">{transaction.shares}</div>
                      </td>
                      <td className="py-3 text-right">
                        <div className="text-gray-900">${transaction.price.toFixed(2)}</div>
                      </td>
                      <td className="py-3 text-right">
                        <div className="font-medium text-gray-900">${transaction.total.toLocaleString()}</div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Portfolio;