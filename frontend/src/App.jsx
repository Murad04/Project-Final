import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import ProductList from './components/ProductList'
import Cart from './components/Cart'

function App() {
    const [cart, setCart] = useState([])

    const addToCart = (product) => {
        setCart([...cart, product])
    }

    return (
        <Router>
            <div>
                <nav style={{ marginBottom: '20px', borderBottom: '1px solid #444', paddingBottom: '10px' }}>
                    <Link to="/" style={{ marginRight: '20px' }}>Home</Link>
                    <Link to="/cart">Cart ({cart.length})</Link>
                </nav>

                <Routes>
                    <Route path="/" element={<ProductList addToCart={addToCart} />} />
                    <Route path="/cart" element={<Cart cart={cart} />} />
                </Routes>
            </div>
        </Router>
    )
}

export default App
