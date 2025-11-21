import React, { useState, useEffect } from 'react'
import axios from 'axios'
import RecommendationRow from './RecommendationRow'

function ProductList({ addToCart }) {
    const [products, setProducts] = useState([])
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        // In a real app, fetch from API
        // axios.get('/api/products').then(res => setProducts(res.data))

        // Mock data for demonstration since backend might not be running
        const mockProducts = [
            { id: 1, name: 'Laptop', price: 999, description: 'High performance laptop', image_url: 'https://via.placeholder.com/150' },
            { id: 2, name: 'Headphones', price: 199, description: 'Noise cancelling', image_url: 'https://via.placeholder.com/150' },
            { id: 3, name: 'Mouse', price: 49, description: 'Wireless mouse', image_url: 'https://via.placeholder.com/150' },
            { id: 4, name: 'Keyboard', price: 129, description: 'Mechanical keyboard', image_url: 'https://via.placeholder.com/150' },
        ]
        setProducts(mockProducts)
        setLoading(false)
    }, [])

    if (loading) return <div>Loading...</div>

    return (
        <div>
            <h2>Products</h2>
            <div className="product-grid">
                {products.map(product => (
                    <div key={product.id} className="product-card">
                        <img src={product.image_url} alt={product.name} />
                        <h3>{product.name}</h3>
                        <p>{product.description}</p>
                        <p>${product.price}</p>
                        <button className="btn" onClick={() => addToCart(product)}>Add to Cart</button>
                    </div>
                ))}
            </div>

            <RecommendationRow userId={1} addToCart={addToCart} />
        </div>
    )
}

export default ProductList
