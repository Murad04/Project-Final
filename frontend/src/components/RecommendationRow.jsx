import React, { useState, useEffect } from 'react'
import axios from 'axios'

function RecommendationRow({ userId, addToCart }) {
    const [recommendations, setRecommendations] = useState([])

    useEffect(() => {
        // Fetch recommendations for the user
        // axios.get(`/api/recommendations/${userId}`).then(res => setRecommendations(res.data))

        // Mock data
        const mockRecs = [
            { id: 5, name: 'Monitor', price: 299, description: '4K Monitor', image_url: 'https://via.placeholder.com/150' },
            { id: 6, name: 'Webcam', price: 89, description: 'HD Webcam', image_url: 'https://via.placeholder.com/150' },
        ]
        setRecommendations(mockRecs)
    }, [userId])

    if (recommendations.length === 0) return null

    return (
        <div style={{ marginTop: '40px', borderTop: '1px solid #444', paddingTop: '20px' }}>
            <h3>Recommended for You</h3>
            <div className="product-grid">
                {recommendations.map(product => (
                    <div key={product.id} className="product-card" style={{ borderColor: '#646cff' }}>
                        <img src={product.image_url} alt={product.name} />
                        <h3>{product.name}</h3>
                        <p>{product.description}</p>
                        <p>${product.price}</p>
                        <button className="btn" onClick={() => addToCart(product)}>Add to Cart</button>
                    </div>
                ))}
            </div>
        </div>
    )
}

export default RecommendationRow
