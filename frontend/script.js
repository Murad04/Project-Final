const API_URL = 'http://localhost:8000';

// State
let cart = JSON.parse(localStorage.getItem('cart')) || [];

// DOM Elements
const cartCountEl = document.getElementById('cart-count');
const productGridEl = document.getElementById('product-grid');
const recommendationsGridEl = document.getElementById('recommendations-grid');
const recommendationsSectionEl = document.getElementById('recommendations-section');
const cartItemsEl = document.getElementById('cart-items');
const cartSummaryEl = document.getElementById('cart-summary');
const emptyCartMsgEl = document.getElementById('empty-cart-msg');
const totalPriceEl = document.getElementById('total-price');

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    updateCartCount();

    if (window.location.pathname.endsWith('index.html') || window.location.pathname === '/' || window.location.pathname.endsWith('/')) {
        fetchProducts();
        fetchRecommendations();
    } else if (window.location.pathname.endsWith('cart.html')) {
        renderCart();
    }
});

// Functions
function updateCartCount() {
    if (cartCountEl) cartCountEl.textContent = `(${cart.length})`;
}

function saveCart() {
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartCount();
}

function addToCart(product) {
    cart.push(product);
    saveCart();
    alert(`${product.name} added to cart!`);
}

function removeFromCart(index) {
    cart.splice(index, 1);
    saveCart();
    renderCart();
}

async function fetchProducts() {
    try {
        // Mock data if API fails (for demonstration)
        const mockProducts = [
            { id: 1, name: 'Quantum Laptop', price: 1299, description: 'Next-gen computing power.', image_url: 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3' },
            { id: 2, name: 'Sonic Headphones', price: 249, description: 'Immersive soundscapes.', image_url: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3' },
            { id: 3, name: 'Ergo Mouse', price: 89, description: 'Precision at your fingertips.', image_url: 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3' },
            { id: 4, name: 'Mech Keyboard', price: 159, description: 'Tactile typing experience.', image_url: 'https://images.unsplash.com/photo-1587829741301-dc798b91a603?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3' },
        ];

        // Try fetching from API, fallback to mock
        let products = mockProducts;
        try {
            const response = await fetch(`${API_URL}/products/`);
            if (response.ok) {
                const data = await response.json();
                if (data.length > 0) products = data;
            }
        } catch (e) {
            console.log('Backend not reachable, using mock data');
        }

        renderProducts(products, productGridEl);

    } catch (error) {
        productGridEl.innerHTML = '<p class="loading">Failed to load products.</p>';
        console.error(error);
    }
}

async function fetchRecommendations() {
    // Mock recommendations
    const mockRecs = [
        { id: 5, name: '4K Monitor', price: 399, description: 'Crystal clear visuals.', image_url: 'https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3' },
        { id: 6, name: 'Webcam Pro', price: 129, description: 'Stream in 1080p.', image_url: 'https://images.unsplash.com/photo-1587826574258-8472d124315e?w=500&auto=format&fit=crop&q=60&ixlib=rb-4.0.3' },
    ];

    // In real app: fetch(`${API_URL}/recommendations/1`)

    if (recommendationsSectionEl) {
        recommendationsSectionEl.style.display = 'block';
        renderProducts(mockRecs, recommendationsGridEl);
    }
}

function renderProducts(products, container) {
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <img src="${product.image_url}" alt="${product.name}" class="product-image">
            <h3 class="product-title">${product.name}</h3>
            <p class="product-desc">${product.description}</p>
            <div class="product-footer">
                <span class="price">$${product.price}</span>
                <button class="btn" onclick='addToCart(${JSON.stringify(product)})'>Add to Cart</button>
            </div>
        </div>
    `).join('');
}

function renderCart() {
    if (cart.length === 0) {
        emptyCartMsgEl.style.display = 'block';
        cartSummaryEl.style.display = 'none';
        cartItemsEl.innerHTML = '';
        return;
    }

    emptyCartMsgEl.style.display = 'none';
    cartSummaryEl.style.display = 'block';

    cartItemsEl.innerHTML = cart.map((item, index) => `
        <div class="cart-item">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <img src="${item.image_url}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;">
                <div>
                    <div style="font-weight: 600;">${item.name}</div>
                    <div style="color: var(--text-secondary);">$${item.price}</div>
                </div>
            </div>
            <button class="btn-outline" onclick="removeFromCart(${index})" style="padding: 0.4rem 0.8rem; border-radius: 4px;">Remove</button>
        </div>
    `).join('');

    const total = cart.reduce((sum, item) => sum + item.price, 0);
    totalPriceEl.textContent = total.toFixed(2);
}

function checkout() {
    alert('Proceeding to checkout... (This is a demo)');
}
