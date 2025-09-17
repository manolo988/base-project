import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { motion } from 'framer-motion';

function Register({ onSuccess }) {
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setLoading(true);
    const result = await register({
      email: formData.email,
      password: formData.password,
      full_name: formData.full_name,
    });
    setLoading(false);

    if (result.success) {
      onSuccess?.();
    } else {
      setError(result.error);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="w-full max-w-md mx-auto"
    >
      <div className="bg-rain-gray border border-rain-gray-light rounded-lg p-8">
        <h2 className="text-2xl font-light text-rain-text mb-8">Create Account</h2>
        {error && (
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-red-900/20 border border-red-800/30 text-red-400 px-4 py-3 rounded-lg mb-6 text-sm"
          >
            {error}
          </motion.div>
        )}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="full_name" className="block text-rain-text-dim text-sm mb-2">
              Full Name
            </label>
            <input
              type="text"
              id="full_name"
              name="full_name"
              value={formData.full_name}
              onChange={handleChange}
              placeholder="John Doe"
              required
              className="w-full px-4 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text placeholder-rain-text-dim focus:outline-none focus:border-rain-pink transition-colors"
            />
          </div>
          <div>
            <label htmlFor="email" className="block text-rain-text-dim text-sm mb-2">
              Email
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="you@example.com"
              required
              className="w-full px-4 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text placeholder-rain-text-dim focus:outline-none focus:border-rain-pink transition-colors"
            />
          </div>
          <div>
            <label htmlFor="password" className="block text-rain-text-dim text-sm mb-2">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="••••••••"
              required
              className="w-full px-4 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text placeholder-rain-text-dim focus:outline-none focus:border-rain-pink transition-colors"
            />
          </div>
          <div>
            <label htmlFor="confirmPassword" className="block text-rain-text-dim text-sm mb-2">
              Confirm Password
            </label>
            <input
              type="password"
              id="confirmPassword"
              name="confirmPassword"
              value={formData.confirmPassword}
              onChange={handleChange}
              placeholder="••••••••"
              required
              className="w-full px-4 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text placeholder-rain-text-dim focus:outline-none focus:border-rain-pink transition-colors"
            />
          </div>
          <motion.button
            type="submit"
            disabled={loading}
            whileHover={{ scale: loading ? 1 : 1.02 }}
            whileTap={{ scale: loading ? 1 : 0.98 }}
            className="w-full py-3 bg-rain-pink text-white rounded-lg font-medium hover:bg-rain-pink-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Creating account...' : 'Create Account'}
          </motion.button>
        </form>
      </div>
    </motion.div>
  );
}

export default Register;