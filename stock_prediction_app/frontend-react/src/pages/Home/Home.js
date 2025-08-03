import React from 'react';
import { Link } from 'react-router-dom';
import { TrendingUp, BarChart3, Brain, Shield } from 'lucide-react';

const features = [
  {
    icon: Brain,
    title: 'AI-Powered Predictions',
    description: 'Advanced machine learning algorithms analyze market trends and provide accurate stock predictions.'
  },
  {
    icon: BarChart3,
    title: 'Real-time Analytics',
    description: 'Get real-time market data and comprehensive analytics to make informed trading decisions.'
  },
  {
    icon: TrendingUp,
    title: 'Market Insights',
    description: 'Deep market insights and trend analysis to help you stay ahead of market movements.'
  },
  {
    icon: Shield,
    title: 'Risk Management',
    description: 'Advanced risk assessment tools to help you manage your portfolio and minimize losses.'
  }
];

const Home = () => {
  return (
    <div className="pt-16">
      {/* Hero Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-50 to-primary-100 rounded-2xl p-8 lg:p-12 mb-12">
        <div className="relative z-10">
          <h1 className="text-4xl lg:text-6xl font-bold text-gray-900 mb-6">
            Smart Stock
            <span className="text-primary-600"> Predictions</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl">
            Harness the power of artificial intelligence to make smarter investment decisions. 
            Get accurate predictions, real-time analytics, and comprehensive market insights.
          </p>
          <div className="flex flex-col sm:flex-row gap-4">
            <Link 
              to="/dashboard"
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors duration-200"
            >
              Get Started
              <TrendingUp className="ml-2 h-5 w-5" />
            </Link>
            <Link 
              to="/analysis"
              className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors duration-200"
            >
              View Analysis
            </Link>
          </div>
        </div>
        
        {/* Background decoration */}
        <div className="absolute top-0 right-0 -mt-4 -mr-4 opacity-20">
          <div className="w-32 h-32 bg-primary-600 rounded-full"></div>
        </div>
        <div className="absolute bottom-0 left-0 -mb-8 -ml-8 opacity-10">
          <div className="w-48 h-48 bg-primary-600 rounded-full"></div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="mb-12">
        <div className="text-center mb-12">
          <h2 className="text-3xl lg:text-4xl font-bold text-gray-900 mb-4">
            Why Choose Our Platform?
          </h2>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Our cutting-edge technology combines machine learning, real-time data analysis, 
            and market expertise to give you the edge in stock trading.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="bg-white rounded-xl p-6 shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200">
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center mb-4">
                <feature.icon className="h-6 w-6 text-primary-600" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Stats Section */}
      <div className="bg-white rounded-xl p-8 shadow-sm border border-gray-200 mb-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
          <div>
            <div className="text-3xl font-bold text-primary-600 mb-2">85%</div>
            <div className="text-gray-600">Prediction Accuracy</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary-600 mb-2">10K+</div>
            <div className="text-gray-600">Active Users</div>
          </div>
          <div>
            <div className="text-3xl font-bold text-primary-600 mb-2">$2.5M</div>
            <div className="text-gray-600">Portfolio Value Tracked</div>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-900 rounded-xl p-8 lg:p-12 text-center">
        <h2 className="text-2xl lg:text-3xl font-bold text-white mb-4">
          Ready to Start Trading Smarter?
        </h2>
        <p className="text-gray-300 mb-8 max-w-2xl mx-auto">
          Join thousands of traders who are already using our AI-powered platform 
          to make better investment decisions.
        </p>
        <Link 
          to="/dashboard"
          className="inline-flex items-center px-8 py-4 border border-transparent text-lg font-medium rounded-md text-gray-900 bg-white hover:bg-gray-100 transition-colors duration-200"
        >
          Start Your Journey
          <TrendingUp className="ml-2 h-5 w-5" />
        </Link>
      </div>
    </div>
  );
};

export default Home;