import React from 'react';
import { motion } from 'framer-motion';

const ItemList = ({ items, onEdit, onDelete, loading, error }) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-20">
        <div className="text-rain-text-dim">Loading items...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-900/20 border border-red-800/30 text-red-400 px-4 py-3 rounded-lg mb-6">
        Error loading items: {error}
      </div>
    );
  }

  if (!items || items.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-center py-20"
      >
        <h3 className="text-rain-text text-xl mb-2">No items found</h3>
        <p className="text-rain-text-dim">Create your first item to get started!</p>
      </motion.div>
    );
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-light text-rain-text">Your Items ({items.length})</h2>
      <div className="grid gap-4">
        {items.map((item, index) => (
          <motion.div
            key={item.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
            className="bg-rain-gray border border-rain-gray-light rounded-lg p-6 hover:border-rain-gray-lighter transition-colors"
          >
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-rain-text text-lg font-medium">{item.title}</h3>
              {item.price > 0 && (
                <span className="text-rain-pink text-lg">${item.price.toFixed(2)}</span>
              )}
            </div>

            {item.description && (
              <p className="text-rain-text-dim mb-4 leading-relaxed">{item.description}</p>
            )}

            <div className="flex justify-between items-center">
              <div className="flex items-center gap-4">
                <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                  item.is_active
                    ? 'bg-green-900/30 text-green-400 border border-green-800/30'
                    : 'bg-red-900/30 text-red-400 border border-red-800/30'
                }`}>
                  {item.is_active ? 'Active' : 'Inactive'}
                </span>
                <span className="text-rain-text-dim text-sm">
                  Created {new Date(item.created_at).toLocaleDateString()}
                </span>
              </div>

              <div className="flex gap-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-4 py-2 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text hover:border-rain-pink transition-colors text-sm"
                  onClick={() => onEdit(item)}
                >
                  Edit
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="px-4 py-2 bg-red-900/20 border border-red-800/30 rounded-lg text-red-400 hover:bg-red-900/30 transition-colors text-sm"
                  onClick={() => onDelete(item.id)}
                >
                  Delete
                </motion.button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ItemList;