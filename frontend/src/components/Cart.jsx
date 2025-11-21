import React from 'react'
import { Link } from 'react-router-dom'

function Cart({ cart }) {
    const total = cart.reduce((sum, item) => sum + item.price, 0)

    return (
        <div>
            <h2>Your Cart</h2>
            {cart.length === 0 ? (
                <p>Cart is empty. <Link to="/">Go shopping</Link></p>
            ) : (
                <div>
                    {cart.map((item, index) => (
                        <div key={index} style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', borderBottom: '1px solid #333' }}>
                            <span>{item.name}</span>
                            <span>${item.price}</span>
                        </div>
                    ))}
                    <div style={{ marginTop: '20px', fontWeight: 'bold' }}>
                        Total: ${total}
                    </div>
                    <button className="btn" style={{ marginTop: '20px' }}>Checkout</button>
                </div>
            )}
        </div>
    )
}

export default Cart
