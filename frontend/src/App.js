import React, { useState, useEffect } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { itemsApi } from './services/api';
import ItemList from './components/ItemList';
import ItemForm from './components/ItemForm';
import Login from './components/Login';
import Register from './components/Register';
import { motion, AnimatePresence } from 'framer-motion';

function AppContent() {
  const { user, isAuthenticated, logout } = useAuth();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [editingItem, setEditingItem] = useState(null);
  const [showRegister, setShowRegister] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  useEffect(() => {
    if (isAuthenticated) {
      loadItems();
    }
  }, [isAuthenticated, currentPage]);

  const loadItems = async () => {
    try {
      setLoading(true);
      const response = await itemsApi.getAll(currentPage, 10);
      setItems(response.data.items);
      setTotalPages(response.data.pages);
      setError(null);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to load items');
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async (itemData) => {
    try {
      if (editingItem) {
        await itemsApi.update(editingItem.id, itemData);
      } else {
        await itemsApi.create(itemData);
      }

      setShowForm(false);
      setEditingItem(null);
      loadItems();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save item');
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setShowForm(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await itemsApi.delete(id);
        loadItems();
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to delete item');
      }
    }
  };

  const handleCancel = () => {
    setShowForm(false);
    setEditingItem(null);
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-rain-dark flex items-center justify-center p-6">
        <div className="w-full max-w-md">
          <motion.h1
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-light text-rain-text text-center mb-8"
          >
            Base Project
          </motion.h1>
          <AnimatePresence mode="wait">
            {showRegister ? (
              <motion.div
                key="register"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
              >
                <Register onSuccess={() => setShowRegister(false)} />
                <p className="text-center mt-6 text-rain-text-dim">
                  Already have an account?{' '}
                  <button
                    className="text-rain-pink hover:text-rain-pink-dark transition-colors"
                    onClick={() => setShowRegister(false)}
                  >
                    Sign in
                  </button>
                </p>
              </motion.div>
            ) : (
              <motion.div
                key="login"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: 20 }}
              >
                <Login onSuccess={() => {}} />
                <p className="text-center mt-6 text-rain-text-dim">
                  Don't have an account?{' '}
                  <button
                    className="text-rain-pink hover:text-rain-pink-dark transition-colors"
                    onClick={() => setShowRegister(true)}
                  >
                    Create one
                  </button>
                </p>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-rain-dark">
      <nav className="border-b border-rain-gray-light bg-rain-gray/50 backdrop-blur-lg sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex justify-between items-center">
            <motion.h1
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-2xl font-light text-rain-text"
            >
              Base Project
            </motion.h1>
            <div className="flex items-center gap-4">
              <span className="text-rain-text-dim text-sm">
                {user?.full_name || user?.email}
              </span>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="px-4 py-2 bg-rain-dark border border-rain-gray-lighter rounded-lg text-rain-text hover:border-rain-pink transition-colors text-sm"
                onClick={logout}
              >
                Sign Out
              </motion.button>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-6xl mx-auto px-6 py-8">
        {error && (
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            className="bg-red-900/20 border border-red-800/30 text-red-400 px-4 py-3 rounded-lg mb-6"
          >
            {error}
          </motion.div>
        )}

        <AnimatePresence mode="wait">
          {!showForm ? (
            <motion.div
              key="list"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="mb-6 px-6 py-3 bg-rain-pink text-white rounded-lg font-medium hover:bg-rain-pink-dark transition-colors"
                onClick={() => setShowForm(true)}
              >
                Create New Item
              </motion.button>

              <ItemList
                items={items}
                onEdit={handleEdit}
                onDelete={handleDelete}
                loading={loading}
                error={error}
              />

              {totalPages > 1 && (
                <div className="flex justify-center items-center gap-4 mt-8">
                  <motion.button
                    whileHover={{ scale: currentPage === 1 ? 1 : 1.05 }}
                    whileTap={{ scale: currentPage === 1 ? 1 : 0.95 }}
                    disabled={currentPage === 1}
                    onClick={() => setCurrentPage(currentPage - 1)}
                    className="px-4 py-2 bg-rain-gray border border-rain-gray-lighter rounded-lg text-rain-text hover:border-rain-pink transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </motion.button>
                  <span className="text-rain-text-dim">
                    Page {currentPage} of {totalPages}
                  </span>
                  <motion.button
                    whileHover={{ scale: currentPage === totalPages ? 1 : 1.05 }}
                    whileTap={{ scale: currentPage === totalPages ? 1 : 0.95 }}
                    disabled={currentPage === totalPages}
                    onClick={() => setCurrentPage(currentPage + 1)}
                    className="px-4 py-2 bg-rain-gray border border-rain-gray-lighter rounded-lg text-rain-text hover:border-rain-pink transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </motion.button>
                </div>
              )}
            </motion.div>
          ) : (
            <motion.div
              key="form"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
            >
              <ItemForm
                item={editingItem}
                onSave={handleSave}
                onCancel={handleCancel}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;