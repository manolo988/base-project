import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const ItemForm = ({ item, onSave, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    price: 0,
    is_active: true,
  });

  useEffect(() => {
    if (item) {
      setFormData({
        title: item.title || '',
        description: item.description || '',
        price: item.price || 0,
        is_active: item.is_active !== undefined ? item.is_active : true,
      });
    }
  }, [item]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSave(formData);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="bg-rain-gray border border-rain-gray-light rounded-lg p-8"
    >
      <form onSubmit={handleSubmit} className="space-y-6">
        <h2 className="text-2xl font-light text-rain-text mb-6">
          {item ? 'Edit Item' : 'Create New Item'}
        </h2>

        <div>
          <label htmlFor="title" className="block text-rain-text-dim text-sm mb-2">
            Title
          </label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            required
            className="w-full px-4 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text placeholder-rain-text-dim focus:outline-none focus:border-rain-pink transition-colors"
            placeholder="Enter item title"
          />
        </div>

        <div>
          <label htmlFor="description" className="block text-rain-text-dim text-sm mb-2">
            Description
          </label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            rows="4"
            className="w-full px-4 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text placeholder-rain-text-dim focus:outline-none focus:border-rain-pink transition-colors resize-none"
            placeholder="Enter item description (optional)"
          />
        </div>

        <div>
          <label htmlFor="price" className="block text-rain-text-dim text-sm mb-2">
            Price
          </label>
          <input
            type="number"
            id="price"
            name="price"
            value={formData.price}
            onChange={handleChange}
            step="0.01"
            min="0"
            className="w-full px-4 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text placeholder-rain-text-dim focus:outline-none focus:border-rain-pink transition-colors"
            placeholder="0.00"
          />
        </div>

        <div>
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              name="is_active"
              checked={formData.is_active}
              onChange={handleChange}
              className="sr-only"
            />
            <div className="relative">
              <div className={`block w-12 h-6 rounded-full transition-colors ${
                formData.is_active ? 'bg-rain-pink' : 'bg-rain-gray-lighter'
              }`}></div>
              <div className={`dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform ${
                formData.is_active ? 'translate-x-6' : ''
              }`}></div>
            </div>
            <span className="ml-3 text-rain-text-dim text-sm">Active</span>
          </label>
        </div>

        <div className="flex gap-3 pt-4">
          <motion.button
            type="submit"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            className="px-6 py-3 bg-rain-pink text-white rounded-lg font-medium hover:bg-rain-pink-dark transition-colors"
          >
            {item ? 'Update Item' : 'Create Item'}
          </motion.button>
          <motion.button
            type="button"
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={onCancel}
            className="px-6 py-3 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text hover:border-rain-pink transition-colors font-medium"
          >
            Cancel
          </motion.button>
        </div>
      </form>
    </motion.div>
  );
};

export default ItemForm;