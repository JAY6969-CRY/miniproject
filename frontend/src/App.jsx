import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import AggressivePage from './pages/AggressivePage';
import LongTermPage from './pages/LongTermPage';

function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/aggressive" element={<AggressivePage />} />
      <Route path="/long-term" element={<LongTermPage />} />
    </Routes>
  );
}

export default App;
