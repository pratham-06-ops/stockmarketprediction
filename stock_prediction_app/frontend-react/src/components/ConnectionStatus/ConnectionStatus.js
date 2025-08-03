import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, RefreshCw } from 'lucide-react';
import { checkAPIConnection } from '../../services/api';

const ConnectionStatus = () => {
  const [connectionStatus, setConnectionStatus] = useState({
    connected: null,
    message: 'Checking connection...',
    details: ''
  });
  const [isChecking, setIsChecking] = useState(false);

  const checkConnection = async () => {
    setIsChecking(true);
    try {
      const status = await checkAPIConnection();
      setConnectionStatus(status);
    } catch (error) {
      setConnectionStatus({
        connected: false,
        message: 'Connection failed',
        details: error.message
      });
    } finally {
      setIsChecking(false);
    }
  };

  useEffect(() => {
    checkConnection();
    // Check connection every 30 seconds
    const interval = setInterval(checkConnection, 30000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = () => {
    if (connectionStatus.connected === null) return 'text-gray-500';
    return connectionStatus.connected ? 'text-success-500' : 'text-danger-500';
  };

  const getStatusBg = () => {
    if (connectionStatus.connected === null) return 'bg-gray-100';
    return connectionStatus.connected ? 'bg-success-100' : 'bg-danger-100';
  };

  return (
    <div className={`inline-flex items-center px-3 py-1 rounded-full text-sm ${getStatusBg()}`}>
      {isChecking ? (
        <RefreshCw className={`h-4 w-4 mr-2 animate-spin ${getStatusColor()}`} />
      ) : connectionStatus.connected ? (
        <Wifi className={`h-4 w-4 mr-2 ${getStatusColor()}`} />
      ) : (
        <WifiOff className={`h-4 w-4 mr-2 ${getStatusColor()}`} />
      )}
      <span className={`font-medium ${getStatusColor()}`}>
        {connectionStatus.connected === null 
          ? 'Checking...' 
          : connectionStatus.connected 
            ? 'Connected' 
            : 'Disconnected'
        }
      </span>
      <button
        onClick={checkConnection}
        disabled={isChecking}
        className="ml-2 p-1 hover:bg-white hover:bg-opacity-50 rounded transition-colors duration-200"
        title="Refresh connection status"
      >
        <RefreshCw className={`h-3 w-3 ${getStatusColor()} ${isChecking ? 'animate-spin' : ''}`} />
      </button>
    </div>
  );
};

export default ConnectionStatus;