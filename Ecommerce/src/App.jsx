import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import ProductList from './pages/ProductList';
import Register from './pages/Register';
import Login from './pages/Login'; 
import './App.css'; 
import CreateProduct from './pages/CreateProduct'; 

function App() {
  return (
    <BrowserRouter>
      <nav style={{ padding: '1rem', borderBottom: '1px solid #ccc' }}>
        <Link to="/" style={{ marginRight: '1rem' }}>Página Inicial</Link>
        <Link to="/register" style={{ marginRight: '1rem' }}>Registrar</Link>
        <Link to="/login">Login</Link> 
        <Link to="/sell">Vender Produto</Link>
      </nav>
      <Routes>
        <Route path="/" element={<ProductList />} />
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} /> 
        <Route path="/sell" element={<CreateProduct />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;