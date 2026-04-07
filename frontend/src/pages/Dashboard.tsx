import { useState, useEffect } from 'react';
import { tagsApi, linksApi, getError } from '../api';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import type { Tag, Link } from '../types';
import {
  Plus, Search, Tag as TagIcon, Link2, ExternalLink,
  Trash2, Edit2, X, Check, LogOut, Hash, Sun, Moon
} from 'lucide-react';

export default function Dashboard() {
  const { user, logout } = useAuth();
  const { dark, toggle } = useTheme();
  const [links, setLinks] = useState<Link[]>([]);
  const [tags, setTags] = useState<Tag[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddLink, setShowAddLink] = useState(false);
  const [showAddTag, setShowAddTag] = useState(false);
  const [editingLink, setEditingLink] = useState<Link | null>(null);
  const [newLink, setNewLink] = useState({ url: '', title: '', description: '' });
  const [selectedTagIds, setSelectedTagIds] = useState<number[]>([]);
  const [editTagIds, setEditTagIds] = useState<number[]>([]);
  const [newTag, setNewTag] = useState({ name: '', color: '#3B82F6' });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [linksData, tagsData] = await Promise.all([
        linksApi.getAll(),
        tagsApi.getAll()
      ]);
      setLinks(linksData.links || []);
      setTags(tagsData.tags || []);
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const toggleTag = (tagId: number) => {
    setSelectedTagIds(prev =>
      prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
    );
  };

  const toggleEditTag = (tagId: number) => {
    setEditTagIds(prev =>
      prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
    );
  };

  const handleAddLink = async () => {
    try {
      const link = await linksApi.create(
        newLink.url,
        newLink.title || undefined,
        newLink.description || undefined,
        selectedTagIds
      );
      setLinks([link, ...links]);
      setNewLink({ url: '', title: '', description: '' });
      setSelectedTagIds([]);
      setShowAddLink(false);
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Failed to add link');
    }
  };

  const handleUpdateLink = async () => {
    if (!editingLink) return;
    try {
      const updated = await linksApi.update(editingLink.id, {
        url: editingLink.url,
        title: editingLink.title || undefined,
        description: editingLink.description || undefined,
        tag_ids: editTagIds
      });
      setLinks(links.map(l => l.id === updated.id ? updated : l));
      setEditingLink(null);
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Failed to update link');
    }
  };

  const handleAddTag = async () => {
    try {
      const tag = await tagsApi.create(newTag.name, newTag.color);
      setTags([...tags, tag]);
      setNewTag({ name: '', color: '#3B82F6' });
      setShowAddTag(false);
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Failed to add tag');
    }
  };

  const handleDeleteLink = async (id: number) => {
    try {
      await linksApi.delete(id);
      setLinks(links.filter(l => l.id !== id));
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Failed to delete link');
    }
  };

  const handleDeleteTag = async (id: number) => {
    try {
      await tagsApi.delete(id);
      setTags(tags.filter(t => t.id !== id));
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Failed to delete tag');
    }
  };

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      loadData();
      return;
    }
    try {
      const result = await linksApi.searchByQuery(searchQuery);
      setLinks(result.links || []);
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Search failed');
    }
  };

  const handleSearchByTag = async (tagName: string) => {
    try {
      const result = await linksApi.searchByTags(tagName);
      setLinks(result.links || []);
    } catch (err) {
      const apiError = getError(err);
      setError(apiError?.message || 'Search failed');
    }
  };

  const openEditModal = (link: Link) => {
    setEditingLink({ ...link });
    setEditTagIds(link.tags?.map(t => t.id) || []);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center">
        <div className="text-gray-500 dark:text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <Link2 className="w-8 h-8 text-indigo-600 dark:text-indigo-400" />
            <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Link Manager</h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-gray-600 dark:text-gray-300">Welcome, <strong>{user?.username}</strong></span>
            <button
              onClick={toggle}
              className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition"
              title={dark ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {dark ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
            </button>
            <button
              onClick={logout}
              className="flex items-center gap-2 px-4 py-2 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition"
            >
              <LogOut className="w-4 h-4" />
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        {/* Search Bar */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 mb-6">
          <div className="flex gap-3">
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Search links by title, description, or URL..."
                className="w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent outline-none"
              />
            </div>
            <button
              onClick={handleSearch}
              className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-semibold"
            >
              Search
            </button>
            <button
              onClick={() => setShowAddLink(true)}
              className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition font-semibold flex items-center gap-2"
            >
              <Plus className="w-5 h-5" />
              Add Link
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Tags Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-white flex items-center gap-2">
                  <TagIcon className="w-5 h-5" />
                  Tags
                </h2>
                <button
                  onClick={() => setShowAddTag(true)}
                  className="p-2 text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-lg transition"
                >
                  <Plus className="w-5 h-5" />
                </button>
              </div>

              {showAddTag && (
                <div className="mb-4 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <input
                    type="text"
                    value={newTag.name}
                    onChange={(e) => setNewTag({ ...newTag, name: e.target.value })}
                    placeholder="Tag name"
                    className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-600 text-gray-900 dark:text-white rounded mb-2 text-sm"
                  />
                  <div className="flex gap-2">
                    <input
                      type="color"
                      value={newTag.color}
                      onChange={(e) => setNewTag({ ...newTag, color: e.target.value })}
                      className="w-10 h-10 rounded cursor-pointer"
                    />
                    <button
                      onClick={handleAddTag}
                      className="flex-1 px-3 py-2 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700"
                    >
                      Add
                    </button>
                    <button
                      onClick={() => setShowAddTag(false)}
                      className="px-3 py-2 bg-gray-300 dark:bg-gray-500 text-gray-700 dark:text-gray-200 rounded text-sm hover:bg-gray-400 dark:hover:bg-gray-400"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              )}

              <div className="space-y-2">
                <button
                  onClick={loadData}
                  className="w-full flex items-center gap-2 p-3 bg-indigo-50 dark:bg-indigo-900/30 text-indigo-700 dark:text-indigo-300 rounded-lg hover:bg-indigo-100 dark:hover:bg-indigo-900/50 transition font-medium text-sm"
                >
                  <Hash className="w-4 h-4" />
                  All
                </button>
                {tags && tags.map(tag => (
                  <div
                    key={tag.id}
                    className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg group hover:bg-gray-100 dark:hover:bg-gray-600 transition"
                  >
                    <button
                      onClick={() => handleSearchByTag(tag.name)}
                      className="flex items-center gap-2 flex-1 text-left"
                    >
                      <Hash className="w-4 h-4" style={{ color: tag.color }} />
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-200">{tag.name}</span>
                    </button>
                    <button
                      onClick={() => handleDeleteTag(tag.id)}
                      className="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 transition"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
                {tags.length === 0 && (
                  <p className="text-gray-500 dark:text-gray-400 text-sm text-center py-4">No tags yet</p>
                )}
              </div>
            </div>
          </div>

          {/* Links List */}
          <div className="lg:col-span-3">
            <div className="space-y-4">
              {links && links.map(link => (
                <div
                  key={link.id}
                  className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 hover:shadow-md transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-gray-800 dark:text-white mb-1">
                        {link.title || 'Untitled'}
                      </h3>
                      <a
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-700 dark:hover:text-indigo-300 text-sm flex items-center gap-1 mb-2"
                      >
                        {link.url}
                        <ExternalLink className="w-3 h-3" />
                      </a>
                      {link.description && (
                        <p className="text-gray-600 dark:text-gray-400 text-sm mb-3">{link.description}</p>
                      )}
                      {link.tags && link.tags.length > 0 && (
                        <div className="flex flex-wrap gap-2">
                          {link.tags.map(tag => (
                            <span
                              key={tag.id}
                              className="px-3 py-1 rounded-full text-xs font-medium text-white"
                              style={{ backgroundColor: tag.color }}
                            >
                              {tag.name}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => openEditModal(link)}
                        className="text-gray-400 hover:text-indigo-500 dark:hover:text-indigo-400 transition"
                      >
                        <Edit2 className="w-5 h-5" />
                      </button>
                      <button
                        onClick={() => handleDeleteLink(link.id)}
                        className="text-gray-400 hover:text-red-500 transition"
                      >
                        <Trash2 className="w-5 h-5" />
                      </button>
                    </div>
                  </div>
                </div>
              ))}
              {links.length === 0 && (
                <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-12 text-center">
                  <Link2 className="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-600 dark:text-gray-400 mb-2">No links yet</h3>
                  <p className="text-gray-500 dark:text-gray-500">Click "Add Link" to get started</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>

      {/* Add Link Modal */}
      {showAddLink && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-full max-w-md p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white">Add New Link</h2>
              <button onClick={() => setShowAddLink(false)} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">URL *</label>
                <input
                  type="url"
                  value={newLink.url}
                  onChange={(e) => setNewLink({ ...newLink, url: e.target.value })}
                  placeholder="https://example.com"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Title</label>
                <input
                  type="text"
                  value={newLink.title}
                  onChange={(e) => setNewLink({ ...newLink, title: e.target.value })}
                  placeholder="Optional title"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
                <textarea
                  value={newLink.description}
                  onChange={(e) => setNewLink({ ...newLink, description: e.target.value })}
                  placeholder="Optional description"
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none resize-none"
                />
              </div>

              {/* Tag Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Tags</label>
                <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto p-2 border border-gray-200 dark:border-gray-600 rounded-lg">
                  {(!tags || tags.length === 0) ? (
                    <p className="text-gray-500 dark:text-gray-400 text-sm">No tags available</p>
                  ) : (
                    (tags || []).map(tag => (
                      <button
                        key={tag.id}
                        onClick={() => toggleTag(tag.id)}
                        className={`px-3 py-1.5 rounded-full text-xs font-medium transition flex items-center gap-1 ${
                          selectedTagIds.includes(tag.id)
                            ? 'text-white ring-2 ring-offset-1 ring-gray-400 dark:ring-gray-500'
                            : 'bg-gray-100 dark:bg-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-500'
                        }`}
                        style={selectedTagIds.includes(tag.id) ? { backgroundColor: tag.color } : {}}
                      >
                        <Hash className="w-3 h-3" />
                        {tag.name}
                      </button>
                    ))
                  )}
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={handleAddLink}
                  disabled={!newLink.url}
                  className="flex-1 bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  <Check className="w-5 h-5" />
                  Add Link
                </button>
                <button
                  onClick={() => setShowAddLink(false)}
                  className="px-6 py-3 bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 font-semibold"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Edit Link Modal */}
      {editingLink && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-2xl w-full max-w-md p-6 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-gray-800 dark:text-white">Edit Link</h2>
              <button onClick={() => setEditingLink(null)} className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">URL *</label>
                <input
                  type="url"
                  value={editingLink.url}
                  onChange={(e) => setEditingLink({ ...editingLink, url: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Title</label>
                <input
                  type="text"
                  value={editingLink.title || ''}
                  onChange={(e) => setEditingLink({ ...editingLink, title: e.target.value })}
                  placeholder="Optional title"
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Description</label>
                <textarea
                  value={editingLink.description || ''}
                  onChange={(e) => setEditingLink({ ...editingLink, description: e.target.value })}
                  placeholder="Optional description"
                  rows={3}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none resize-none"
                />
              </div>

              {/* Tag Selection */}
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Tags</label>
                <div className="flex flex-wrap gap-2 max-h-32 overflow-y-auto p-2 border border-gray-200 dark:border-gray-600 rounded-lg">
                  {(!tags || tags.length === 0) ? (
                    <p className="text-gray-500 dark:text-gray-400 text-sm">No tags available</p>
                  ) : (
                    (tags || []).map(tag => (
                      <button
                        key={tag.id}
                        onClick={() => toggleEditTag(tag.id)}
                        className={`px-3 py-1.5 rounded-full text-xs font-medium transition flex items-center gap-1 ${
                          editTagIds.includes(tag.id)
                            ? 'text-white ring-2 ring-offset-1 ring-gray-400 dark:ring-gray-500'
                            : 'bg-gray-100 dark:bg-gray-600 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-500'
                        }`}
                        style={editTagIds.includes(tag.id) ? { backgroundColor: tag.color } : {}}
                      >
                        <Hash className="w-3 h-3" />
                        {tag.name}
                      </button>
                    ))
                  )}
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={handleUpdateLink}
                  className="flex-1 bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 flex items-center justify-center gap-2"
                >
                  <Check className="w-5 h-5" />
                  Save Changes
                </button>
                <button
                  onClick={() => setEditingLink(null)}
                  className="px-6 py-3 bg-gray-200 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-500 font-semibold"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
