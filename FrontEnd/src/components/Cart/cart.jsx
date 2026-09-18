import { createContext, useCallback, useContext, useEffect, useState } from "react";
import "./cart.css";

const CartContext = createContext(null);
const API_URL = import.meta.env.VITE_API_URL;

const getAuthHeaders = () => {
    const token = localStorage.getItem('token');
    return token ? { Authorization: `Bearer ${token}` } : {};
};

export const CartProvider = ({ children }) => {
    const [cart, setCart] = useState([]);

    const refreshCart = useCallback(async () => {
        if (!localStorage.getItem('token')) {
            return;
        }

        const [cartResponse, productsResponse] = await Promise.all([
            fetch(`${API_URL}/users/me/cart`, { headers: getAuthHeaders() }),
            fetch(`${API_URL}/product/`),
        ]);

        if (!cartResponse.ok || !productsResponse.ok) {
            throw new Error('Unable to load your saved cart.');
        }

        const cartItems = await cartResponse.json();
        const products = await productsResponse.json();
        const productsById = new Map(products.map((product) => [product.id, product]));

        setCart(cartItems
            .map((item) => ({ ...productsById.get(item.product_id), quantity: item.quantity }))
            .filter((item) => item.id));
    }, []);

    useEffect(() => {
        refreshCart().catch(() => {});

        const handleAuthChange = () => refreshCart().catch(() => {});
        window.addEventListener('auth-change', handleAuthChange);
        return () => window.removeEventListener('auth-change', handleAuthChange);
    }, [refreshCart]);

    const addItem = async (product) => {
        const existingItem = cart.find((item) => item.id === product.id);
        if (product.stock <= 0 || (existingItem && existingItem.quantity >= product.stock)) {
            return { success: false, message: 'This item is out of stock.' };
        }

        if (localStorage.getItem('token')) {
            const response = await fetch(`${API_URL}/users/me/cart`, {
                method: 'POST',
                headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_id: product.id, quantity: 1 }),
            });

            const data = await response.json();
            if (!response.ok) {
                return { success: false, message: data.detail || 'Unable to add item to cart.' };
            }
        }

        setCart((currentCart) => {
            const existingItem = currentCart.find((item) => item.id === product.id);

            if (existingItem) {
                return currentCart.map((item) => item.id === product.id
                    ? { ...item, quantity: item.quantity + 1 }
                    : item);
            }

            return [...currentCart, { ...product, quantity: 1 }];
        });

        return { success: true };
    };

    const removeItem = (productId) => {
        const item = cart.find((cartItem) => cartItem.id === productId);
        const nextQuantity = item ? item.quantity - 1 : 0;

        setCart((currentCart) => currentCart
            .map((item) => item.id === productId
                ? { ...item, quantity: item.quantity - 1 }
                : item)
            .filter((item) => item.quantity > 0));

        if (localStorage.getItem('token')) {
            const request = nextQuantity > 0
                ? fetch(`${API_URL}/users/me/cart/${productId}`, {
                    method: 'PUT',
                    headers: { ...getAuthHeaders(), 'Content-Type': 'application/json' },
                    body: JSON.stringify({ quantity: nextQuantity }),
                })
                : fetch(`${API_URL}/users/me/cart/${productId}`, {
                    method: 'DELETE',
                    headers: getAuthHeaders(),
                });

            request.catch(() => {});
        }
    };

    const clearCart = () => setCart([]);

    return (
        <CartContext.Provider value={{ cart, addItem, removeItem, clearCart, refreshCart }}>
            {children}
        </CartContext.Provider>
    );
};

export const useCart = () => useContext(CartContext);



const Cart = () => {
    const { cart, addItem, removeItem, clearCart } = useCart();
    const [isOpen, setIsOpen] = useState(false);
    const [checkoutMessage, setCheckoutMessage] = useState('');
    const itemCount = cart.reduce((total, item) => total + item.quantity, 0);
    const subtotal = cart.reduce((total, item) => total + Number(item.price) * item.quantity, 0);

    const handleCheckout = async () => {
        if (!localStorage.getItem('token')) {
            setCheckoutMessage('Please log in before checking out.');
            return;
        }

        if (!window.confirm(`Confirm purchase for $${subtotal.toFixed(2)}?`)) {
            return;
        }

        try {
            const response = await fetch(`${API_URL}/purchases/checkout`, {
                method: 'POST',
                headers: getAuthHeaders(),
            });
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Unable to complete purchase.');
            }

            clearCart();
            setCheckoutMessage(`Purchase confirmed: $${Number(data.total_price).toFixed(2)}`);
        } catch (error) {
            setCheckoutMessage(error.message);
        }
    };

    return (
        <div className="CartWrapper">
            <button
                className="CartButton"
                type="button"
                aria-label={`Open cart with ${itemCount} items`}
                onClick={() => setIsOpen((open) => !open)}
            >
                <svg className="Icon" xmlns="http://www.w3.org/2000/svg" width="30" height="30" viewBox="0 0 24 24" aria-hidden="true">
                    <path fill="currentColor" d="M17 18a2 2 0 1 1-2 2c0-1.11.89-2 2-2M1 2h3.27l.94 2H20a1 1 0 0 1 1 1c0 .17-.05.34-.12.5l-3.58 6.47c-.34.61-1 1.03-1.75 1.03H8.1l-.9 1.63l-.03.12c0 .14.11.25.25.25H19v2H7a2 2 0 0 1-2-2c0-.35.09-.68.24-.96l1.36-2.45L3 4H1zm6 16a2 2 0 1 1-2 2c0-1.11.89-2 2-2m9-7l2.78-5H6.14l2.36 5z" />
                </svg>
                {itemCount > 0 && <span className="CartCount">{itemCount}</span>}
            </button>

            {isOpen && (
                <div className="CartPanel">
                    <div className="CartPanelHeader">
                        <h2>Your cart</h2>
                        <button type="button" className="CartClose" onClick={() => setIsOpen(false)} aria-label="Close cart">&times;</button>
                    </div>

                    {cart.length === 0 ? (
                        <p className="CartEmpty">Your cart is waiting for something special.</p>
                    ) : (
                        <>
                        <div className="CartItems">
                            {cart.map((item) => (
                                <div className="CartItem" key={item.id}>
                                    <img src={item.image_url} alt="" />
                                    <div className="CartItemDetails">
                                        <h3>{item.name}</h3>
                                        <p>
                                            {item.price} &middot; Qty {item.quantity}
                                            <label>
                                                <span className="sr-only">Size</span>
                                                <select defaultValue="M" aria-label={`Select size for ${item.name}`}>
                                                    <option value="M">M</option>
                                                    <option value="L">L</option>
                                                    <option value="XL">XL</option>
                                                    <option value="2XL">2XL</option>
                                                    <option value="3XL">3XL</option>
                                                </select>
                                            </label>
                                        </p>
                                        {item.stock <= 0 && <span className="CartOutOfStock">Out of stock</span>}
                                        <button type="button" onClick={() => removeItem(item.id)}>Remove one</button>
                                    </div>
                                    <button
                                        className="CartAdd"
                                        type="button"
                                        onClick={() => addItem(item)}
                                        disabled={item.stock <= 0 || item.quantity >= item.stock}
                                        aria-label={`Add another ${item.name}`}
                                    >+</button>
                                </div>
                            ))}
                        </div>
                        <div className="CartSummary">
                            <strong>Subtotal</strong>
                            <strong>${subtotal.toFixed(2)}</strong>
                        </div>
                        <button type="button" className="CartCheckout" onClick={handleCheckout}>Checkout</button>
                        </>
                    )}
                    {checkoutMessage && <p className="CartCheckoutMessage" role="status">{checkoutMessage}</p>}
                </div>
            )}
        </div>
    );
};

export default Cart;